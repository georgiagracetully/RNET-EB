import pandas as pd
import zipfile
import json
import os
from pathlib import Path

def compile_z_metadata_with_metadata(directory, metadata_cols=None):
    """
    Extended version that keeps specified metadata columns.
    
    Parameters:
    -----------
    directory : str or Path
        Path to directory containing the zip files
    metadata_cols : list, optional
        List of metadata columns to keep (from first file)
        Default: ['Puzzle_Name', 'Design', 'Player', 'Round', 'Dataset']
    """
    
    if metadata_cols is None:
        metadata_cols = ['Puzzle_Name', 'Design', 'Player', 'Round', 'Dataset', 'logkd_nolig_scaled']
    
    directory = Path(directory)
    z_files = sorted(directory.glob('*_Z.json.zip'))
    
    merged_df = None
    
    for i, zip_path in enumerate(z_files):
        filename = zip_path.stem.replace('.json', '')
        package_name = filename.replace('RS_', '').replace('_Z', '')
        
        print(f"Processing: {zip_path.name}")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            json_filename = zip_ref.namelist()[0]
            with zip_ref.open(json_filename) as json_file:
                df = pd.read_json(json_file)
        
        nolig_col = f'log_kfold_est_nolig_Z_{package_name}'
        lig_col = f'log_kfold_est_lig_Z_{package_name}'
        
        if nolig_col not in df.columns:
            print(f"  Warning: {nolig_col} not found")
            continue
        
        if i == 0:
            # First file - keep metadata
            cols_to_keep = ['sequence'] + [c for c in metadata_cols if c in df.columns]
            merged_df = df[cols_to_keep].copy()
            merged_df[nolig_col] = df[nolig_col]
            if lig_col in df.columns:
                merged_df[lig_col] = df[lig_col]
        else:
            temp_df = df[['sequence', nolig_col]].copy()
            if lig_col in df.columns:
                temp_df[lig_col] = df[lig_col]
            merged_df = merged_df.merge(temp_df, on='sequence', how='inner')
    
    return merged_df

import argparse

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Compile Z metadata from multiple _Z.json.zip files'
    )
    parser.add_argument(
        'data_directory',
        type=str,
        help='Path to directory containing _Z.json.zip files'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='compiled_Z_metadata.json',
        help='Output CSV filename (default: compiled_Z_metadata.json)'
    )

    
    args = parser.parse_args()
    
    # Compile the metadata
    metadata_df = compile_z_metadata_with_metadata(args.data_directory)
    
    # Save to json file 
    metadata_df.to_json(args.output, index=False)
    print(f"\nSaved to {args.output}")
    
    # Show summary statistics
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print(f"Total sequences: {len(metadata_df)}")
    print(f"Total prediction columns: {len([c for c in metadata_df.columns if 'log_kfold' in c])}")
    print(f"\nFirst few rows:")
    print(metadata_df.head())