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

## US real GNP growth dynamics and forecasting (old exercises 15 and 16)

Notebook: [GNP_Growth_AR_Forecasting.ipynb](GNP_Growth_AR_Forecasting.ipynb)

Analyse quarterly US real Gross National Product (GNP) log growth for
1947Q2-2019Q4 (291 quarters), before the pandemic. Follow the OLS
notebook structure: data, ACF/PACF, model and lag selection, estimates,
coefficient interpretation, persistence and a next-quarter forecast.

Compare contiguous AR orders 0-8 on the same 283 estimation quarters. BIC
selects AR(1), while AIC selects AR(3). Compare both models' intercepts, lag coefficients,
long-run mean, coefficient uncertainty and residual Ljung-Box p-value.
Compare their responses to a one-percentage-point growth innovation, with a
separate enlarged view of the small oscillatory tail. The AR(3) complex pair
implies a period of about 10.7 quarters (2.7 years), with an envelope half-life
of about one quarter. Its rapid damping makes this a model-implied oscillation,
rather than an estimate of the average duration of observed business cycles.
Forecast 2020Q1 with both models
from origin 2019Q4 and compare with the held-out observation; the prediction
interval conditions on the estimated model. This historical exercise uses
revised data and does not reproduce a real-time forecast.

A single final table extends the sample through 2025Q4. It shows how lag
selection and AR(1) estimates depend on the sample. The main analysis uses
every pre-2020 quarter; the comparison retains every quarter through 2025.
Positive AR(1) persistence describes decay, not an average business-cycle period.

### Relevant concepts

- GNP versus GDP; levels versus quarterly growth; annual-rate levels versus annualised growth.
- ACF and PACF; AR(p); conditional OLS; intercept and long-run mean.
- AIC/BIC; common hold-back; order selection versus residual adequacy.
- Stability; persistence; impulse responses; sample sensitivity.
- Complex dynamic eigenvalues; oscillatory period and damping; model-implied periods versus observed cycles.
- Forecast origin; one-step forecasts; held-out observations; forecast errors.
- Prediction intervals; parameter uncertainty; revised versus real-time observations.

### To do

Explain why candidate orders must be compared on the same dependent-variable
sample. Interpret both models' coefficients and long-run means, and calculate the
effect of a one-point growth innovation after one and two quarters. Calculate
the AR(3) oscillatory period and envelope half-life, explaining why the former
is not the mean duration of dated business cycles. Interpret
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

`quarterly_real_gnp.csv` contains US real GNP for 316 complete quarters,
1947Q1-2025Q4. The first quarter is a growth base. Main analysis stops at 2019Q4;
later observations are used only for the held-out forecast outcome and final
sensitivity comparison. Values come from the BEA's
[NIPA Table 1.7.6 workbook](https://apps.bea.gov/national/Release/XLS/Survey/Section1All_xls.xlsx),
quarterly worksheet `T10706-Q`, line 4, code `A001RX`, retrieved on 14 October
2026 (data published 30 September 2026). Divide its millions of chained 2017
dollars by 1,000 to store billions, matching the equivalent
[GNPC96 series on FRED](https://fred.stlouisfed.org/series/GNPC96). The levels
are seasonally adjusted annual rates. Several observations were cross-checked
against FRED. GNP concerns production attributable to US residents, domestically
and abroad; GDP concerns production within the country's borders.

No missing quarters are interpolated. Growth is `100 * diff(log(GNP))`, without annualisation.
Source URLs, retrieval dates, source flags, transformations and SHA-256 hashes
are recorded in `data_sources.json`. The series is public-domain BEA data with
BEA/FRED attribution. Current revised values are not the original data vintage
of historical GNP papers; this notebook fits a linear AR model, not a replication
of threshold or Markov-switching models.

## Running the notebooks

Follow the [shared setup instructions](../README.md). In Colab, upload the full
`Notebooks` folder to My Drive and preserve `Time_Series` and its CSV files.
The setup also supports local Jupyter from the course, `Notebooks` or tutorial
folder. No live data download or API key is required.
