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