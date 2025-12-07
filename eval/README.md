Here's the cleaned-up README.md file:

```markdown
# Benchmarking RNET-EB

## Generating Z-scores for Model Comparison

To benchmark RNET-EB against other models, I used the EternaBench scoring system to calculate Z-scores.

### Step 1: Compile Bootstrapped Results

Run the following command to generate Z-scores:

```bash
python scripts/CompileBootstrappedResults.py 'RS' -o no_lig_assessment_with_rnet_eb_000 --calculate_Z_scores package_list_000.txt
```

This generates the output file:
```
no_lig_assessment_with_rnet_eb_000_pearson_zscores_by_Dataset.csv
```

### Step 2: Generate Heatmap Figure

Once the Z-scores CSV file is saved, run the following code block (adapted from code cell "Riboswitch Data" in the Jupyter notebook `3_EternaFold_TestSets`):

```python
# Load the Z-scores data
zscores = pd.read_csv(os.environ['ETERNABENCH_PATH'] + '/scoring_data/no_lig_assessment_with_rnet_eb_000_pearson_zscores_by_Dataset.csv')

# Generate ranked heatmap
eb.plot.ranked_heatmap(zscores, vmin=-2, vmax=2, size=2)

# Save figure
savefig('FIGURES/3/Figure_3D_replicate_with_eb.pdf', bbox_inches='tight')
```

This generates a heatmap visualization named `Figure_3D_replicate_with_eb.pdf` comparing RNET-EB performance to other models.

## Notes

- The Z-score calculation is based on Pearson correlation coefficients
- The heatmap uses a color scale from -2 to +2 standard deviations
- Results are organized by dataset for easy comparison
```

**Key changes made:**
- Separated all code blocks with proper markdown code fences
- Preserved all underscores as literal characters (not markdown formatting)
- Added clear section headers
- Formatted file paths and commands in code blocks
- Added explanatory text for clarity
- Organized the workflow into logical steps
- Added a Notes section at the end
