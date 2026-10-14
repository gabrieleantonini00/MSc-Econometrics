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

Analyse quarterly real GDP log growth in the United States and Germany for
1996Q2-2019Q4 (95 quarters per country), before the pandemic. Follow the OLS
notebook structure: data, ACF/PACF, model and lag selection, estimates,
coefficient interpretation, persistence and a next-quarter forecast.

Compare contiguous AR orders 0-8 on the same 87 estimation quarters. BIC
selects AR(1) for both countries. Interpret the intercept, lag coefficient,
long-run mean, coefficient uncertainty and residual Ljung-Box p-value.
Plot the decay of a one-percentage-point growth innovation. Forecast 2020Q1
from origin 2019Q4 and compare with the held-out observation; the prediction
interval conditions on the estimated model. This historical exercise uses
revised data and illustrates the difficulty of forecasting an exceptional event.

A single final table extends the sample through 2025Q4. It shows how lag
selection and AR(1) estimates depend on the sample. The main analysis uses
every pre-2020 quarter; the comparison retains every quarter through 2025.
Positive AR(1) persistence describes decay, not an average business-cycle period.

### Relevant concepts

- Real GDP levels versus quarterly growth; annual-rate levels versus annualised growth.
- ACF and PACF; AR(p); conditional OLS; intercept and long-run mean.
- AIC/BIC; common hold-back; order selection versus residual adequacy.
- Stability; persistence; impulse responses; sample sensitivity.
- Forecast origin; one-step forecasts; held-out observations; forecast errors.
- Prediction intervals; parameter uncertainty; revised versus real-time observations.

### To do

Explain why candidate orders must be compared on the same dependent-variable
sample. Interpret the AR(1) coefficients and long-run means, and calculate the
effect of a one-point growth innovation after one and two quarters. Interpret
the 2020Q1 forecasts and errors, distinguishing model uncertainty from an
exceptional event. Explain why adding 2020-2025 changes the selected order and
why AR(0) selection is not proof of an absence of economic dynamics.

## Data

`daily_us_market_returns.csv` contains 4,024 trading sessions, 2010-2025, with
`Mkt-RF`, `RF` and `market_return = Mkt-RF + RF`, all as decimal simple returns.
The notebook selects 2021-2025 (1,255 sessions) for all calculations and plots,
and computes `100 * log(1 + market_return)`. Data are extracted from
the existing course dataset, originally retrieved on 9 October 2026 from the
[Kenneth French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html).
Dates without French market returns are excluded; no market holiday is filled.
The market is the broad value-weighted US CRSP equity market, not a price index.

`quarterly_real_gdp.csv` contains US and German GDP for 120 complete quarters,
1996Q1-2025Q4. The first quarter is a growth base. Main analysis stops at 2019Q4;
later observations are used only for the held-out forecast outcome and final
sensitivity comparison. US GDP comes from the BEA's
[GDPC1](https://fred.stlouisfed.org/series/GDPC1), in billions of chained 2017
dollars at a seasonally adjusted annual rate. Germany comes directly
from [Eurostat's quarterly national accounts](https://ec.europa.eu/eurostat/databrowser/view/namq_10_gdp/default/table?lang=en),
`namq_10_gdp`, with `freq=Q`, `unit=CLV20_MEUR`, `s_adj=SCA`, `na_item=B1GQ`
and `geo=DE`: chain-linked volumes (2020), million euro, seasonally and
calendar adjusted. Sources were retrieved on 13 October 2026; the US extract
was already downloaded for the Okun notebook on that date. The German values
are extracted from the archived Eurostat response. The fixed level sample
begins in 1996Q1.

Eurostat flags German 2023Q1-2025Q4 observations as provisional; these remain
in the final sensitivity comparison. No missing quarters
are interpolated. Growth is `100 * diff(log(GDP))`, without annualisation.
Source URLs, retrieval dates, source flags, transformations and SHA-256 hashes
are recorded in `data_sources.json`. Eurostat/European Union attribution is
retained; the US series is public-domain data with BEA/FRED attribution.

## Running the notebooks

Follow the [shared setup instructions](../README.md). In Colab, upload the full
`Notebooks` folder to My Drive and preserve `Time_Series` and its CSV files.
The setup also supports local Jupyter from the course, `Notebooks` or tutorial
folder. No live data download or API key is required.

