import matplotlib.pyplot as plt
import seaborn as sns
import os


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
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['font.size'] = 14
    
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
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['font.size'] = 14
    
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

def plot_prediction_comparison(test_data, save_dir=None, show_plots=True):
    """
    Create scatter plots comparing experimental and predicted logKd values.
    
    Args:
        test_data: DataFrame containing experimental and predicted values
        save_dir: Directory to save figures (optional)
        show_plots: Whether to display plots (default: True)
    
    Returns:
        dict: Dictionary containing correlation coefficients
    """
    # Set matplotlib parameters for Times New Roman and LaTeX
    # Set font to Times New Roman
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['font.size'] = 14
    plt.rcParams['text.usetex'] = True
    plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'
    
    # Colorblind-friendly colors from Wong palette
    scatter_color_lig = '#0072B2'      # Blue
    scatter_color_nolig = '#009E73'    # Teal/green
    regline_color = '#D55E00'          # Vermillion/red-orange
    
    # Calculate correlation coefficients
    corr_lig = np.corrcoef(test_data['logkd_lig_scaled'], 
                           test_data['log_kfold_est_lig_Z'])[0, 1]
    corr_nolig = np.corrcoef(test_data['logkd_nolig_scaled'], 
                             test_data['log_kfold_est_nolig_Z'])[0, 1]
    
    # ========================================================================
    # First plot: logkd_lig vs. logkd_lig_pred
    # ========================================================================
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    
    # Scatter plot
    ax1.scatter(test_data['logkd_lig_scaled'], 
                test_data['log_kfold_est_lig_Z'],
                color=scatter_color_lig, 
                s=100, 
                alpha=0.6,
                edgecolors='black',
                linewidth=0.5)
    
    # Regression line
    z = np.polyfit(test_data['logkd_lig_scaled'], 
                   test_data['log_kfold_est_lig_Z'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(test_data['logkd_lig_scaled'].min(), 
                         test_data['logkd_lig_scaled'].max(), 100)
    ax1.plot(x_line, p(x_line), 
             color=regline_color, 
             linewidth=2.5, 
             label=f'$r = {corr_lig:.3f}$')
    
    # Labels with LaTeX
    ax1.set_xlabel(r'Experimental $\log K_\mathrm{d}$ (ligand)', fontsize=14)
    ax1.set_ylabel(r'Predicted $\log K_\mathrm{d}$ (ligand)', fontsize=14)
    ax1.set_title(r'RNET-EB: Ligand-bound State', fontsize=16)
    
    # Legend
    ax1.legend(fontsize=12, frameon=False, loc='best')
    
    # Remove grid
    ax1.grid(False)
    
    # Thick black outline
    for spine in ax1.spines.values():
        spine.set_linewidth(2)
        spine.set_edgecolor('black')
    
    # Increase tick width
    ax1.tick_params(width=2, length=6, color='black')
    
    plt.tight_layout()
    
    # Save figure
    if save_dir:
        fig1.savefig(f'{save_dir}/logkd_lig_comparison.svg', 
                     format='svg', dpi=300, bbox_inches='tight')
        fig1.savefig(f'{save_dir}/logkd_lig_comparison.png', 
                     format='png', dpi=300, bbox_inches='tight')
    
    if show_plots:
        plt.show()
    else:
        plt.close(fig1)
    
    # ========================================================================
    # Second plot: logkd_nolig vs. logkd_no_lig_pred
    # ========================================================================
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    
    # Scatter plot
    ax2.scatter(test_data['logkd_nolig_scaled'], 
                test_data['log_kfold_est_nolig_Z'],
                color=scatter_color_nolig, 
                s=100, 
                alpha=0.6,
                edgecolors='black',
                linewidth=0.5)
    
    # Regression line
    z = np.polyfit(test_data['logkd_nolig_scaled'], 
                   test_data['log_kfold_est_nolig_Z'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(test_data['logkd_nolig_scaled'].min(), 
                         test_data['logkd_nolig_scaled'].max(), 100)
    ax2.plot(x_line, p(x_line), 
             color=regline_color, 
             linewidth=2.5, 
             label=f'$r = {corr_nolig:.3f}$')
    
    # Labels with LaTeX
    ax2.set_xlabel(r'Experimental $\log K_\mathrm{d}$ (no ligand)', fontsize=14)
    ax2.set_ylabel(r'Predicted $\log K_\mathrm{d}$ (no ligand)', fontsize=14)
    ax2.set_title(r'RNET-EB: Ligand-free State', fontsize=16)
    
    # Legend
    ax2.legend(fontsize=12, frameon=False, loc='best')
    
    # Remove grid
    ax2.grid(False)
    
    # Thick black outline
    for spine in ax2.spines.values():
        spine.set_linewidth(2)
        spine.set_edgecolor('black')
    
    # Increase tick width
    ax2.tick_params(width=2, length=6, color='black')
    
    plt.tight_layout()
    
    # Save figure
    if save_dir:
        fig2.savefig(f'{save_dir}/logkd_nolig_comparison.svg', 
                     format='svg', dpi=300, bbox_inches='tight')
        fig2.savefig(f'{save_dir}/logkd_nolig_comparison.png', 
                     format='png', dpi=300, bbox_inches='tight')
    
    if show_plots:
        plt.show()
    else:
        plt.close(fig2)
    
    # Reset matplotlib parameters
    plt.rcParams.update(plt.rcParamsDefault)
    
    # Return correlation coefficients
    return {
        'correlation_lig': corr_lig,
        'correlation_nolig': corr_nolig
    }