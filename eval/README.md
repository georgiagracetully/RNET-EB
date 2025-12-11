# Steps for Benchmarking Results Against Other Riboswitch Calculations

## 1) Clone EternaBench Repository

```bash
git clone https://github.com/eternagame/EternaBench.git
```
**Note:** Instead of rerunning EternaBench with requirements in archived folder, I just patched individual files and then ran scripts (this mainly just involved changing any instance of `pd.append` to `pd.concat`).

## 2) Copy Saved Test Predictions to EternaBench

Move the saved test predictions to `EternaBench/data/RiboswitchCalculations`

**Example:**
```bash
cp path/to/RNET-EB/results/test_preds/RS_RNet_EB_000_Z.json /path/to/EternaBench/data/RiboswitchCalculations
```

And then zip those files:

```python
import pandas as pd
import zipfile

# Zip the NPT file
with zipfile.ZipFile('RS_RNet_EB_000_NPT_Z.json.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write('RS_RNet_EB_000_NPT_Z.json')

# Zip the standard file
with zipfile.ZipFile('RS_RNet_EB_000_Z.json.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write('RS_RNet_EB_000_Z.json')
```
## 3) Compile Riboswitch Metadata

I used Anthropic's model claude 4-5 to generate a starter script called `CompileRiboswitchMetadata.py` that I added to my `EternaBench/scripts` folder. This compiles all the `nolig_Z` columns (inner, to remove training samples that are present in all other package calculation predictions except in teh RNet preds dataframe) into one dataframe with metadata included. 

```bash
python scripts/CompileRiboswitchMetadata.py data/RiboswitchCalculations --output 'RS_nolig_compiled_preds.json'
```

## 4) Bootstrap and Evaluate

Now I want to bootstrap all correlations from every dataset type with n=1000 iterations and then get a `BOOTSTRAPS.json.zip` for each package evaluated (In this example, I just get one BOOTSTRAPS.json.zip because I am using a compiled .json file in step 2, but traditionally you run this step using each individual package calculation file). To do this, I will use a modified `ScoreRiboswitches.py` (in GT EB-EVAL repository, modification is just patched for Python 3 compatibility). 

However, I notice that the scoring is based on `logkd_nolig`, `logkd_lig`, and `log_AR`, but I first just want to score based on the `logkd_nolig`, so I am going to modify the x and y inputs:

**Original:**
```python
elif args.method == 'Z':
    x_inputs = ['logkd_nolig_scaled', 'logkd_lig_scaled', 'log_AR']
    y_inputs = ['log_kfold_est_nolig_Z', 'log_kfold_est_lig_Z', 'log_AR_est']
```

**Modified to:**
```python
elif args.method == 'Z':
    x_inputs = ['logkd_nolig_scaled']
    y_inputs = ['log_kfold_est_nolig_Z']
```

I renamed this modified scoring script as `ScoreRiboswitches_nolig_Metadata.py`. 

## Understanding the ScoreRiboswitches.py Script

The `ScoreRiboswitches.py` script iterates over all unique Datasets in the `ScoreRiboswitches` function, and then over each package in a list in the `calculate_metric` function in the `stats.py` script within eternabench source code.

## 5) Score the Compiled Predictions

I then ran the `ScoreRiboswitches_nolig_Metadata.py` script to get `RS_nolig_compiled_preds_BOOTSTRAPS.json.zip` which I temporarily stored in my main EternaBench directory:

```bash
python scripts/ScoreRiboswitches_nolig_Metadata.py RS_nolig_compiled_preds.json --n_bootstraps=1000 --metric='pearson' --method='Z'
```

## 6) Compile Bootstrapped Results

Then I ran `CompileBootstrappedResults.py` with `package_list_000.txt`:

```bash
python scripts/CompileBootstrappedResults.py 'RS' -o RS_no_lig_assessment_with_rnet_eb_000_and_NPT --calculate_Z_scores package_list_000.txt
```

This generated `RS_no_lig_assessment_with_rnet_eb_000_and_NPT_pearson_ranking.csv` and `RS_no_lig_assessment_with_rnet_eb_000_and_NPT_pearson_zscores_by_Dataset.csv`.

## 7) Generate Z-Score Figure

Once I had this saved, I ran the following code block (copying code cell Riboswitch Data from the Jupyter notebook `3_EternaFold_TestSets`):

```python
# Original line:
# zscores = pd.read_csv(os.environ['ETERNABENCH_PATH']+'/scoring_data/RS_bps_pearson_zscores_Fig3_efold_testset.csv')

# Modified to:
zscores = pd.read_csv(os.environ['ETERNABENCH_PATH']+'/scoring_data/RS_no_lig_assessment_with_rnet_eb_000_and_NPT_pearson_zscores_by_Dataset.csv')

eb.plot.ranked_heatmap(zscores, vmin=-2, vmax=2, size=2)
savefig('FIGURES/3/Figure_3D_replicate_with_RNet_EB_000.pdf', bbox_inches='tight')
```

This generated the z-score figure that I named `Figure_3D_Replicate_with_RNet_EB_000.pdf`.

**Note:** For this figure to generate, you need to manually edit the eternabench `package_metadata.csv` to include RNet_EB_000 and 
RNet_EB_000_NPT. (I also saved a copy within this repo).

