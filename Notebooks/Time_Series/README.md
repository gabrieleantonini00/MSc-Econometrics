# Time Series (Tutorial V)

Two notebooks develop the old exercises 14-16. They follow the same structure
as the OLS notebooks: environment setup, libraries, local data, analysis and
explanations. Sections are unnumbered; assignment prompts stay in this README.

## Autocorrelations (old exercise 14)

Notebook: [Autocorrelations.ipynb](Autocorrelations.ipynb)

Analyse 1,255 daily US market log returns in 2021-2025. Plot the returns and their ACF
at lags 1-15, then test whether the first five autocorrelations are jointly zero.
Calculate the Ljung-Box statistic explicitly using this single sample.
A short squared-return comparison distinguishes dependence in
signed returns from dependence in movement magnitudes. Squared returns proxy
conditional variance when the conditional mean is close to zero.

### Relevant concepts

- Trading-session lags; simple and log returns; total and excess returns.
- Weak stationarity; population and sample autocorrelations; pointwise bands.
- Joint hypotheses; Ljung-Box statistic; reference distribution; p-values.
- Linear dependence versus independence; changing volatility; limits of inference.
- Squared returns as a conditional-variance proxy; variance versus volatility.

### To do

State the five-lag null and alternative, interpret the observed statistic and
p-value at the 5% level for the 2021-2025 sample.
Explain why neither rejection nor failure to reject establishes a profitable
strategy or validates market efficiency. Compare the ACF of returns with the
ACF of squared demeaned returns.

## GDP growth dynamics and forecasting (old exercises 15 and 16)

Notebook: [GDP_Growth_AR_Forecasting.ipynb](GDP_Growth_AR_Forecasting.ipynb)

Analyse quarterly real GDP log growth in the United States, Germany and Italy
for 1996Q2-2025Q4 (119 quarters per country). Compare ACF/PACF plots, choose
contiguous AR orders 0-8 using a common estimation sample, and interpret
coefficients, long-run means and residual diagnostics. Estimate AR(1) and AR(2)
benchmarks alongside the BIC-selected models, with a sample-ending sensitivity
comparison through 2019Q4.

Examine impulse responses and dynamic eigenvalues. Complex modes can imply a
damped oscillation; its period is not automatically the average duration of
the business cycle. This sample does not support a sustained multi-year cycle
from the fitted growth AR models. Do not force an order or average short,
rapidly damped oscillations across countries to obtain a desired duration.

Evaluate eight sequential one-step forecasts for 2024Q1-2025Q4, with order
selection and coefficients estimated only through 2023Q4. Compare them with
historical-mean and last-observation forecasts. Then use the full dataset for
a next-quarter forecast, 2026Q1 from origin 2025Q4, and a five-quarter path with
conditional prediction intervals. These are historical teaching forecasts
using revised data, not a current economic outlook or a real-time backtest.

### Relevant concepts

- Real GDP levels versus quarterly growth; annual-rate levels versus annualised growth.
- ACF and PACF; AR(p); conditional OLS; intercept and long-run mean.
- AIC/BIC; common hold-back; order selection versus residual adequacy.
- Stability; persistence; impulse responses; roots and dynamic eigenvalues.
- Oscillatory periods versus business-cycle durations; damping; sample sensitivity.
- Forecast origins; one-step versus multi-step forecasts; holdout leakage; MAE/RMSE.
- Prediction intervals; parameter uncertainty; revised versus real-time observations.

### To do

Explain why candidate orders must be compared on the same dependent-variable
sample and why AR(0) can be selected. Compare the estimated AR(1) persistence
through 2019 and through 2025. For an AR(2) with a complex pair, calculate the
implied period in years and the envelope half-life, then assess whether those
numbers describe a sustained business cycle. Interpret the held-out forecast
errors and the next-quarter forecast, distinguishing a flat conditional mean
from constant realised growth.

## Data

`daily_us_market_returns.csv` contains 4,024 trading sessions, 2010-2025, with
`Mkt-RF`, `RF` and `market_return = Mkt-RF + RF`, all as decimal simple returns.
The notebook selects 2021-2025 (1,255 sessions) for all calculations and plots,
and computes `100 * log(1 + market_return)`. Data are extracted from
the existing course dataset, originally retrieved on 9 October 2026 from the
[Kenneth French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html).
Dates without French market returns are excluded; no market holiday is filled.
The market is the broad value-weighted US CRSP equity market, not a price index.

`quarterly_real_gdp.csv` contains 120 complete quarters, 1996Q1-2025Q4. The first
quarter is a growth base. US GDP comes from the BEA's
[GDPC1](https://fred.stlouisfed.org/series/GDPC1), in billions of chained 2017
dollars at a seasonally adjusted annual rate. Germany and Italy come directly
from [Eurostat's quarterly national accounts](https://ec.europa.eu/eurostat/databrowser/view/namq_10_gdp/default/table?lang=en),
`namq_10_gdp`, with `freq=Q`, `unit=CLV20_MEUR`, `s_adj=SCA`, `na_item=B1GQ`
and `geo=DE/IT`: chain-linked volumes (2020), million euro, seasonally and
calendar adjusted. Sources were retrieved on 13 October 2026; the US extract
was already downloaded for the Okun notebook on that date. There is no Italian
1995 data in this Eurostat extract, so the common level sample begins in 1996.

Eurostat flags German 2023Q1-2025Q4 observations as provisional, and Italian
2010Q1 as a break in the time series. All these values remain in the analysis;
the flags are disclosed without an invented adjustment. No missing quarters
are interpolated. Growth is `100 * diff(log(GDP))`, without annualisation.
Source URLs, retrieval dates, source flags, transformations and SHA-256 hashes
are recorded in `data_sources.json`. Eurostat/European Union attribution is
retained; the US series is public-domain data with BEA/FRED attribution.

## Running the notebooks

Follow the [shared setup instructions](../README.md). In Colab, upload the full
`Notebooks` folder to My Drive and preserve `Time_Series` and its CSV files.
The setup also supports local Jupyter from the course, `Notebooks` or tutorial
folder. No live data download or API key is required.

