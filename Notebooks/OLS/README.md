# OLS tutorials

## Simple and multiple regression (Tutorial II)

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

## Heteroskedasticity (Tutorial III)

Notebook: [Heteroskedasticity.ipynb](Heteroskedasticity.ipynb)

Analyse the relationship between annual income and food expenditure for 235
working-class Belgian households in 1857. Both variables are in Belgian francs.
Estimate a simple OLS regression, inspect residual dispersion and compare
conventional and HC3 standard errors on the same observations.

### Relevant concepts

- Homoskedasticity versus heteroskedasticity; conditional mean versus conditional variance.
- Residual plots; interpretation of vertical dispersion at comparable income levels.
- Studentised Breusch-Pagan test: null hypothesis, LM statistic and p-value.
- OLS coefficients versus their estimated uncertainty; robust standard errors.
- Confidence intervals; statistical versus economic significance; limits of robust inference.

### To do

Describe the pattern in the residual plots and distinguish a changing spread
from a changing conditional mean. Interpret the variance-test p-value and
compare the income coefficient's standard error and confidence interval before
and after HC3. Explain why the coefficient and fitted line remain unchanged.

The full-sample plot contains all households. A second panel enlarges the range
covering the lowest 95% of incomes, with different axis ranges. This affects only
the display: all regressions, tests and grouped summaries use all 235 observations.
The highest-income observation is influential; it is retained throughout.
The notebook contains the analysis and explanations, with no numbered sections
or separate assignment prompts.

## Monte Carlo simulation

Notebook: [Monte_Carlo_Simulation.ipynb](Monte_Carlo_Simulation.ipynb)

Generate independent observations from a known simple-regression model with
zero conditional mean and heteroskedastic errors. Run 10,000 replications for
sample sizes of 250 and 1,000. Compare conventional, HC1 and HC3 standard errors
using the same samples and the same approximate t reference.

The notebook shows the OLS sampling distribution, empirical sampling SD,
average estimated SE, interval width, 95% confidence-interval coverage and
rejection rates for the true null that the slope equals 0.5. Monte Carlo SEs
help distinguish simulation noise from departures from nominal coverage.
Data are generated in the notebook, with a fixed seed; no additional CSV is needed.

## Rolling CAPM (Tutorial IV)

Notebook: [Rolling_CAPM.ipynb](Rolling_CAPM.ipynb)

Analyse IBM's monthly excess returns and the broad US market excess return for
January 2000-December 2025 (312 months). Compare the full-sample CAPM regression
with 60-month rolling regressions, each with its own intercept and slope.
The 253 complete windows include both the first and the last available window.
All estimates use OLS coefficients with Newey-West HAC standard errors (Bartlett
weights, three monthly lags, sample-size correction and approximate t inference).

### Relevant concepts

- Simple and excess returns; alpha; market beta; coefficient units.
- Standard errors; zero-coefficient tests; p-values; confidence intervals; R-squared.
- Full-sample versus rolling estimates; window length; precision and recency.
- Parameter stability; pointwise intervals; overlapping windows; sampling variation.

### To do

Calculate the fitted IBM excess return when the market excess return is 1%,
using first the full-sample coefficients and then those for the window ending
in December 2025. Interpret the difference and comment on the rolling beta plot.
Explain why beta equal to 1 means market-like sensitivity and why a changing
estimate alone does not establish a structural break.

Adjacent windows share 59 of their 60 observations. The plotted 95% intervals
are pointwise coefficient intervals, not a simultaneous band or a formal test
of coefficient equality. Assignment prompts stay here and in the tutorial PDF;
the notebook contains the analysis and explanations.

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

`engel_data.csv` contains the two original Engel variables, `income` and
`foodexp`, with 235 rows and no missing values. The CSV comes from the
[official statsmodels repository](https://github.com/statsmodels/statsmodels/blob/v0.14.4/statsmodels/datasets/engel/engel.csv);
the [dataset documentation](https://www.statsmodels.org/stable/datasets/generated/engel.html)
defines the annual amounts in Belgian francs. All observations and source values
are preserved, without inflation adjustment or standardisation. These are
historical teaching data. `additional_datasets.engel_food_expenditure` in
`data_sources.json` records their source, units, public-domain licence and hash.

`monthly_capm_data.csv` contains 313 month-end rows, December 1999 to December
2025. The first row supplies the stock's base price; estimation uses the subsequent
312 months. IBM adjusted prices come from
[Alpha Vantage](https://www.alphavantage.co/documentation/), and the market excess
return and matched monthly RF come from the
[Kenneth French factor data](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html).
Prices are adjusted for dividends and splits; the notebook computes simple stock
returns without adding dividends again. Market excess returns and RF are stored
as decimals. RF is subtracted once from the stock return, and is not subtracted
again from the already-excess market return. The original stock observation date
is retained alongside the month-end label. `rolling_capm_data_sources.json`
records the sources, units, transformations and file hashes. No live download
or API key is needed.

## Running the notebook

Follow the [shared setup instructions](../README.md). For Colab, upload the complete
`Notebooks` folder to My Drive, preserving the `OLS` subfolder and its data.
**Environment setup** is the second cell and can be collapsed after execution.

The market-only regression is CAPM-style; adding Brent gives an extended return
regression. Neither regression alone validates the CAPM or identifies a causal
oil-price effect. Two two-dimensional slices illustrate each multiple-regression
coefficient while holding the other regressor fixed at zero, with identical axis
scales to compare the slopes. Both lines meet the same intercept because both
regressors are zero there. A supplementary
three-dimensional plane shows the same slices without the observation cloud.
The model comparison retains the summary table and gives the formulas for
R-squared, adjusted R-squared and omitted variable bias, including the exact
sample identity linking the two market slopes.

The energy-return models use OLS coefficients with the same Newey–West HAC standard errors
(Bartlett weights, three monthly lags, sample-size correction and an approximate
t reference). Only this HAC specification is included in the notebook.
The technical treatment of robust inference is reserved for the later tutorial.
Assignment prompts are kept in this exercise description; the notebook contains
the analysis and explanatory notes.
