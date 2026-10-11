# OLS tutorials

## Exercise 1. Simple and multiple regression

Notebook: [Simple_Multiple_Regression.ipynb](Simple_Multiple_Regression.ipynb)

Analyse monthly US energy-sector excess returns for 2011–2025. Estimate a market-only
regression, then add monthly changes in the Brent spot price. State your expectations
before estimation. Interpret the coefficient signs, sizes and units, standard errors,
p-values and confidence intervals. Compare the two models on the same sample,
distinguishing economic significance, statistical significance and explanatory power.

### Relevant concepts

- Simple and multiple regression; intercept and slope coefficients; units.
- Partial associations and interpretation holding other regressors constant.
- Standard errors; t-tests; p-values; confidence intervals; Type I error.
- Statistical versus economic significance.
- Fitted values and residuals; R-squared and adjusted R-squared; omitted variable bias.

### To do

Using the estimated multiple-regression coefficients, calculate the fitted energy
excess return when market excess return is 1% and the Brent price change is 10%.
Compare it with the fitted value when both regressors are zero. Explain the
contribution of each coefficient and why the fitted value is not a guaranteed
realised return.

## Data

`monthly_energy_market_data.csv` contains 181 month-end observations, December 2010
to December 2025. December 2010 supplies the base price for the first Brent change;
both regressions use the subsequent 180 months.

- Energy portfolio: value-weighted `Enrgy` monthly returns from the
  [Kenneth French 12 industry portfolios](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_12_ind_port.html).
  This is a portfolio of energy stocks, rather than an individual company.
- Market excess return and matched monthly risk-free return:
  [Kenneth French factor data](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html).
  Market is the broad value-weighted US CRSP equity-market return minus RF,
  not the S&P 500. RF is subtracted from Energy, but not again from Market.
- Brent: last available daily [EIA/FRED spot price](https://fred.stlouisfed.org/series/DCOILBRENTEU)
  in each calendar month. The original observation date is included in the CSV.

Returns are supplied as decimals; spot prices are in USD per barrel. The notebook
expresses its regression variables in percent. No live download or API key is
needed. `data_sources.json` records sources, units, transformations and file hashes.

## Running the notebook

Follow the [shared setup instructions](../README.md). For Colab, upload the complete
`Notebooks` folder to My Drive, preserving the `OLS` subfolder and its data.
**Environment setup** is the second cell and can be collapsed after execution.

The market-only regression is CAPM-style; adding Brent gives an extended return
regression. Neither regression alone validates the CAPM or identifies a causal
oil-price effect. A three-dimensional fitted plane illustrates the multiple model;
observed-versus-fitted plots compare the fit of both models in two dimensions.

The main output uses OLS coefficients with Newey–West HAC standard errors
(Bartlett weights, three monthly lags, sample-size correction and an approximate
t reference). A final comparison includes conventional, HC1 and six-lag HAC
standard errors. Residual checks show heteroskedasticity in the multiple model;
serial-correlation checks do not establish that errors are independent.
The technical treatment of robust inference is reserved for the later tutorial.
Assignment prompts are kept in this exercise description; the notebook contains
the analysis and explanatory notes.
