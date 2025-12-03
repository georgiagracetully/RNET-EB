import torch
import os 

def save_checkpoint(epoch, model, optimizer, schedule, avg_train_loss, val_loss, 
                   train_losses, val_losses, best_loss, checkpoint_dir, 
                   checkpoint_name='latest_checkpoint.pt'):
    """
    Save model checkpoint.
    
    Args:
        epoch: Current epoch number
        model: Model to save
        optimizer: Optimizer state
        schedule: Learning rate scheduler
        avg_train_loss: Average training loss for current epoch
        val_loss: Validation loss for current epoch
        train_losses: List of all training losses
        val_losses: List of all validation losses
        best_loss: Best validation loss so far
        checkpoint_dir: Directory to save checkpoint
        checkpoint_name: Name of checkpoint file
    """
    checkpoint = {
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'scheduler_state_dict': schedule.state_dict() if schedule is not None else None,
        'train_loss': avg_train_loss,
        'val_loss': val_loss,
        'train_losses': train_losses,
        'val_losses': val_losses,
        'best_loss': best_loss
    }
    
    checkpoint_path = os.path.join(checkpoint_dir, checkpoint_name)
    torch.save(checkpoint, checkpoint_path)
    return checkpoint_path