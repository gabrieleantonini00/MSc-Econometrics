# MSc Econometrics notebooks

This is the single folder to distribute to students. Keep each tutorial's notebooks
and data in its own subfolder. Additional tutorials can be added as sibling folders.

```text
Notebooks/
  README.md
  requirements.txt
  Financial_Returns/
    Prices_Returns_Distributions.ipynb
    Rolling_Equity_Premium.ipynb
    Tail_Risk_VaR.ipynb
    daily_market_data.csv
    monthly_market_data.csv
    data_sources.json
  OLS/
    README.md
    Simple_Multiple_Regression.ipynb
    Heteroskedasticity.ipynb
    Monte_Carlo_Simulation.ipynb
    Rolling_CAPM.ipynb
    monthly_energy_market_data.csv
    monthly_capm_data.csv
    engel_data.csv
    data_sources.json
    rolling_capm_data_sources.json
```

## Google Colab

1. Upload the complete `Notebooks` folder to **My Drive** in Google Drive. Preserve
   the tutorial subfolders; upload the folder itself, not only the `.ipynb` files.
2. Open the desired notebook with Google Colab.
3. Run the cells in order, starting with **Environment setup**,
   or choose **Run all**. Authorize the Google Drive connection when prompted.

The setup uses `/content/drive/MyDrive/Notebooks` by default. If the folder is
renamed or placed elsewhere, change `NOTEBOOKS_ROOT` in the setup cell to its full
path. All data reads use the tutorial's `DATA_DIR`, so the runtime's working
directory does not need to be changed. Upload the complete folder once; all
tutorials can use it.

Alternatively, if the complete folder is already uploaded and extracted in the
Colab runtime, set `NOTEBOOKS_ROOT = "/content/Notebooks"`. Files stored only in
the runtime must be uploaded again after the runtime is reset.

Colab provides the analysis libraries used here. Data are included as CSV files,
so no data-source download or API key is required. See the official
[Colab file and Google Drive examples](https://colab.research.google.com/notebooks/io.ipynb)
and [Colab FAQ](https://research.google.com/colaboratory/faq.html).

## Local Jupyter

From `Notebooks`, install the dependencies with
`python -m pip install -r requirements.txt`, then run `jupyter lab` and open a
notebook in its tutorial subfolder. The setup also works when Jupyter runs from
the course folder or the tutorial folder. Set `NOTEBOOKS_ROOT` explicitly if
Jupyter uses a different working directory.

## Financial Returns

[Financial Returns](Financial_Returns/) contains:

- [Prices, returns and distributions](Financial_Returns/Prices_Returns_Distributions.ipynb): simple and log returns, empirical distributions and a Normal benchmark.
- [Rolling equity premium](Financial_Returns/Rolling_Equity_Premium.ipynb): monthly excess returns, rolling statistics and t-tests.
- [Tail risk and VaR](Financial_Returns/Tail_Risk_VaR.ipynb): historical and Normal thresholds, with a holdout comparison.

The two CSV datasets are shared by the notebooks in this tutorial. Sources are
linked in the notebooks and recorded in `data_sources.json`. Each dataset needs
only one copy in this subfolder.

## OLS

[OLS](OLS/) contains the regression exercises:

- [Simple and multiple regression](OLS/Simple_Multiple_Regression.ipynb): monthly
  energy-sector excess returns, market exposure and Brent-price changes; interpretation
  of coefficients, standard errors, p-values, confidence intervals and model fit.

- [Heteroskedasticity](OLS/Heteroskedasticity.ipynb): household income and food
  expenditure; residual plots, a variance test, and conventional versus HC3
  standard errors and confidence intervals.

- [Monte Carlo simulation](OLS/Monte_Carlo_Simulation.ipynb): repeated samples
  from a known heteroskedastic model; conventional, HC1 and HC3 standard errors,
  confidence-interval coverage, Type I error and simulation uncertainty.

- [Rolling CAPM](OLS/Rolling_CAPM.ipynb): IBM and the broad US market;
  full-sample and 60-month rolling betas, HAC confidence intervals and
  interpretation of parameter stability.

See the [exercise and data description](OLS/README.md). Empirical notebooks use
the included data; the Monte Carlo notebook generates its own observations.
