import matplotlib.pyplot as plt
import seaborn as sns


def plot_logkd_histograms(df, figsize=(14, 6), color1='#2E86AB', color2='#A23B72', bins=30):
    """
    Plot side-by-side histograms for logkd_lig and logkd_nolig.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing 'logkd_lig' and 'logkd_nolig' columns
    figsize : tuple, optional
        Figure size (width, height). Default is (14, 6)
    color1 : str, optional
        Color for logkd_lig histogram. Default is '#2E86AB' (blue)
    color2 : str, optional
        Color for logkd_nolig histogram. Default is '#A23B72' (magenta)
    bins : int, optional
        Number of bins for histograms. Default is 30
    
    Returns:
    --------
    fig, axes : matplotlib figure and axes objects
    """
  
    
    # Set the style to remove grid lines
    sns.set_style("white")
    
    # Set font to Times New Roman
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['font.size'] = 14
    
    # Create figure with subplots
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Plot the histogram for 'logkd_lig'
    sns.histplot(df['logkd_lig'], kde=True, color=color1, bins=bins, 
                 ax=axes[0], edgecolor='black', linewidth=0.5)
    axes[0].set_xlabel(r'$\log(K_d)_{\mathrm{lig}}$', fontsize=24)
    axes[0].set_ylabel('Frequency', fontsize=24)
    
    # Add thick border to first subplot
    for spine in axes[0].spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(2)
    
    # Plot the histogram for 'logkd_nolig'
    sns.histplot(df['logkd_nolig'], kde=True, color=color2, bins=bins, 
                 ax=axes[1], edgecolor='black', linewidth=0.5)
    axes[1].set_xlabel(r'$\log(K_d)_{\mathrm{no\_lig}}$', fontsize=24)
    axes[1].set_ylabel('Frequency', fontsize=24)
    
    # Add thick border to second subplot
    for spine in axes[1].spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(2)
    
    # Remove grid lines
    axes[0].grid(False)
    axes[1].grid(False)
    
    # Adjust layout to make space for titles and labels
    plt.tight_layout()
    
    return fig, axes

def plot_loss_curve(train_losses, val_losses, figure_dir, filename='loss_curve'):
    """
    Plot and save training and validation loss curves.
    
    Args:
        train_losses: List of training losses
        val_losses: List of validation losses
        figure_dir: Directory to save figures
        filename: Base filename (without extension)
    """
    # Set font to Times New Roman
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 12
    
    fig, ax = plt.subplots(figsize=(10, 6))
    epochs_range = range(1, len(train_losses) + 1)
    
    # Colorblind-friendly colors: teal and vermillion
    train_color = '#009E73'  # Teal/green
    val_color = '#D55E00'    # Vermillion/red-orange
    
    ax.plot(epochs_range, train_losses, label='Training Loss', 
            marker='o', linewidth=2.5, markersize=5, color=train_color)
    ax.plot(epochs_range, val_losses, label='Validation Loss', 
            marker='s', linewidth=2.5, markersize=5, color=val_color)
    
    ax.set_xlabel('Epoch', fontsize=14)
    ax.set_ylabel('Loss', fontsize=14)
    ax.set_title('Training and Validation Loss', fontsize=16)
    ax.legend(fontsize=12, frameon=False)
    
    # Thick plot outline
    for spine in ax.spines.values():
        spine.set_linewidth(2)
    
    # Remove grid
    ax.grid(False)
    
    # Increase tick width
    ax.tick_params(width=2, length=6)
    
    plt.tight_layout()
    
    # Save as SVG
    svg_path = os.path.join(figure_dir, f'{filename}.svg')
    plt.savefig(svg_path, format='svg', dpi=300, bbox_inches='tight')
    
    # Also save as PNG for quick viewing
    png_path = os.path.join(figure_dir, f'{filename}.png')
    plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Reset to defaults
    plt.rcParams.update(plt.rcParamsDefault)


def plot_final_summary(train_losses, val_losses, figure_dir, filename='final_loss_curve'):
    """
    Plot final summary with both linear and log scale views.
    
    Args:
        train_losses: List of training losses
        val_losses: List of validation losses
        figure_dir: Directory to save figures
        filename: Base filename (without extension)
    """
    # Set font to Times New Roman
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 12
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    epochs_range = range(1, len(train_losses) + 1)
    
    # Colorblind-friendly colors: teal and vermillion
    train_color = '#009E73'  # Teal/green
    val_color = '#D55E00'    # Vermillion/red-orange
    
    # Linear scale
    ax1.plot(epochs_range, train_losses, label='Training Loss', 
             marker='o', linewidth=2.5, markersize=5, color=train_color)
    ax1.plot(epochs_range, val_losses, label='Validation Loss', 
             marker='s', linewidth=2.5, markersize=5, color=val_color)
    ax1.set_xlabel('Epoch', fontsize=14)
    ax1.set_ylabel('Loss', fontsize=14)
    ax1.set_title('Loss Curve (Linear Scale)', fontsize=16)
    ax1.legend(fontsize=12, frameon=False)
    ax1.grid(False)
    
    # Thick outline for ax1
    for spine in ax1.spines.values():
        spine.set_linewidth(2)
    ax1.tick_params(width=2, length=6)
    
    # Log scale
    ax2.plot(epochs_range, train_losses, label='Training Loss', 
             marker='o', linewidth=2.5, markersize=5, color=train_color)
    ax2.plot(epochs_range, val_losses, label='Validation Loss', 
             marker='s', linewidth=2.5, markersize=5, color=val_color)
    ax2.set_xlabel('Epoch', fontsize=14)
    ax2.set_ylabel('Loss (log scale)', fontsize=14)
    ax2.set_title('Loss Curve (Log Scale)', fontsize=16)
    ax2.set_yscale('log')
    ax2.legend(fontsize=12, frameon=False)
    ax2.grid(False)
    
    # Thick outline for ax2
    for spine in ax2.spines.values():
        spine.set_linewidth(2)
    ax2.tick_params(width=2, length=6)
    
    plt.tight_layout()
    
    # Save as SVG
    svg_path = os.path.join(figure_dir, f'{filename}.svg')
    plt.savefig(svg_path, format='svg', dpi=300, bbox_inches='tight')
    
    # Save as PNG
    png_path = os.path.join(figure_dir, f'{filename}.png')
    plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Reset to defaults
    plt.rcParams.update(plt.rcParamsDefault)