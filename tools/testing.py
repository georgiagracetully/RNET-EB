import torch
import pandas as pd
from torch.utils.data import DataLoader
from tqdm import tqdm
from rna_datasets import RNA_Dataset
import os


def test_from_checkpoint(checkpoint_path, test_df, model, criterion=None, 
                        batch_size=1, device='cuda', save_predictions=True, 
                        output_dir=None):
    """
    Load a model checkpoint and run inference on test data.
    
    Args:
        checkpoint_path: Path to the saved checkpoint file
        test_df: Test dataframe with same format as training/validation data
        model: Model instance (architecture should match checkpoint)
        criterion: Loss function (optional, for computing test loss)
        batch_size: Batch size for test loader
        device: Device to run inference on ('cuda' or 'cpu')
        save_predictions: Whether to save predictions to CSV
        output_dir: Directory to save predictions (if None, uses checkpoint directory)
    
    Returns:
        test_data_with_preds: DataFrame with original data and predictions
        test_loss: Average test loss (if criterion provided, else None)
        checkpoint_info: Dictionary with checkpoint metadata
    """
    
    # Load checkpoint
    print(f"Loading checkpoint from: {checkpoint_path}")
    checkpoint = torch.load(checkpoint_path, map_location=device)
    
    # Load model state
    model.load_state_dict(checkpoint['model_state_dict'])
    model = model.to(device)
    model.eval()
    
    # Print checkpoint info
    checkpoint_info = {
        'epoch': checkpoint['epoch'],
        'train_loss': checkpoint.get('train_loss', 'N/A'),
        'val_loss': checkpoint.get('val_loss', 'N/A'),
        'best_loss': checkpoint.get('best_loss', 'N/A')
    }
    
    print(f"\n{'='*60}")
    print(f"Checkpoint Information:")
    print(f"  Epoch: {checkpoint_info['epoch'] + 1}")
    print(f"  Training Loss: {checkpoint_info['train_loss']}")
    print(f"  Validation Loss: {checkpoint_info['val_loss']}")
    print(f"  Best Loss: {checkpoint_info['best_loss']}")
    print(f"{'='*60}\n")
    
    # Create test dataset and loader
    test_dataset = RNA_Dataset(test_df)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    
    # Run inference
    print("Running inference on test data...")
    tbar = tqdm(test_loader, desc="Testing")
    test_preds = []
    test_loss = 0.0
    num_batches = 0
    
    with torch.no_grad():
        for idx, batch in enumerate(tbar):
            sequence = batch['sequence'].to(device)
            labels = batch['labels'].to(device)
            
            # Forward pass
            output = model(sequence)
            labels = labels.view_as(output)
            
            # Compute loss if criterion provided
            if criterion is not None:
                loss = criterion(output, labels)
                loss = loss.mean()
                test_loss += loss.item()
                num_batches += 1
                tbar.set_postfix({'loss': f'{test_loss / num_batches:.4f}'})
            
            # Store predictions
            test_preds.append([output.cpu().numpy()])
    
    # Calculate average test loss
    avg_test_loss = test_loss / num_batches if criterion is not None and num_batches > 0 else None
    
    if avg_test_loss is not None:
        print(f"\nAverage Test Loss: {avg_test_loss:.4f}")
    
    # Extract predictions
    print("\nProcessing predictions...")
    log_kfold_est_lig_Z = []
    log_kfold_est_nolig_Z = []
    
    for pred in test_preds:
        # Assuming output has shape [batch_size, 2] where:
        # Index 0 is logkd_lig_pred, Index 1 is logkd_no_lig_pred
        output_array = pred[0]
        
        # Handle batch dimension
        if output_array.ndim == 2:
            for i in range(output_array.shape[0]):
                log_kfold_est_lig_Z.append(output_array[i, 0])
                log_kfold_est_nolig_Z.append(output_array[i, 1])
        else:
            log_kfold_est_lig_Z.append(output_array[0])
            log_kfold_est_nolig_Z.append(output_array[1])
    
    # Create DataFrame with predictions
    test_data_with_preds = test_df.copy()
    test_data_with_preds['log_kfold_est_lig_Z'] = log_kfold_est_lig_Z
    test_data_with_preds['log_kfold_est_nolig_Z'] = log_kfold_est_nolig_Z
    
    # Add test loss column if available
    if avg_test_loss is not None:
        test_data_with_preds['test_loss'] = avg_test_loss
    
    # Save predictions
    if save_predictions:
        if output_dir is None:
            output_dir = os.path.dirname(checkpoint_path)
        
        # Create output filename based on checkpoint
        checkpoint_name = os.path.splitext(os.path.basename(checkpoint_path))[0]
        output_path = os.path.join(output_dir, f'RS_{checkpoint_name}_Z.json')
        
        
        test_data_with_preds.to_json(output_path, index=False)
        print(f"\nPredictions saved to: {output_path}")
    
    print(f"\n{'='*60}")
    print(f"Testing Complete!")
    print(f"Total test samples: {len(test_data_with_preds)}")
    print(f"{'='*60}\n")
    
    return test_data_with_preds, avg_test_loss, checkpoint_info


