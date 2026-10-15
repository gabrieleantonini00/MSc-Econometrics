# Time Series (Tutorials V, VII and VIII)

Four notebooks develop the old exercises 14-16 and 19-22. They follow the same structure
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

## Volatility clustering, ARCH and GARCH (Tutorial VIII, old exercises 19, 21 and 22)

Notebook: [Volatility_Clustering.ipynb](Volatility_Clustering.ipynb)

Use 1,249 daily EUR/USD log changes in 2021-2025. Compare signed changes and
squared demeaned changes through time, in the empirical distribution and in
their ACFs. Compare AR orders 0-10 on the same 1,239 observations. Both AIC and
BIC select AR(0) for signed changes; for squared changes AIC selects AR(9)
and BIC AR(1). Report the distinct selected models with five-lag HAC inference.

Derive Gaussian ARCH(1) unconditional variance and kurtosis, distinguishing
the finite-variance condition from the stronger finite-fourth-moment condition.
Then test 10-lag ARCH effects in constant-mean residuals and estimate Gaussian
constant-variance, ARCH(1), ARCH(2) and GARCH(1,1), (1,2), (2,1), (2,2) models
on all 1,249 observations. AIC selects GARCH(2,2), while BIC selects GARCH(1,1).
Check convergence and inspect robust parameter uncertainty and standardised
residual diagnostics.

Compare conditional standard deviations with lagged rolling estimates over
10, 20 and 50 observations and explicit EWMA recursions with lambda 0.94 and
0.97. All curves use daily percentage units and compatible information timing.
A parametric-bootstrap LR comparison uses 199 replications to compare the
AIC-selected order with the reduced order, while explaining boundary and
post-selection limitations. Forecast standard deviations one and two observed
quotations ahead from the historical origin 31 December 2025.

### Relevant concepts

- Exchange-rate quotations and log changes; volatility clustering; noisy variance proxies.
- AR order selection; AIC versus BIC; coefficient interpretation and HAC inference.
- Gaussian ARCH(1); conditional versus unconditional moments; variance versus kurtosis existence.
- ARCH LM test; conditional-variance constraints; Gaussian likelihood and robust covariance.
- GARCH persistence; standardised residuals; model adequacy versus information-criterion selection.
- Rolling standard deviations; EWMA recursions; variance versus standard deviation; information timing.
- Likelihood-ratio statistic; boundary restrictions; bootstrap reference and Monte Carlo uncertainty.
- Historical-origin forecasts; one- and two-step variance propagation; model and order uncertainty.

### To do

Choose an asset and carry out a similar analysis of its daily returns,
adapting the notebook's code. Use prices from an official or primary source
and document the source, sample period and relevant price adjustments.
Plot log returns and compare their ACF with that of squared demeaned returns.
Model volatility using ARCH(1) and GARCH(1,1) with the same mean specification
and estimation sample; compare AIC and BIC. For your preferred model, plot the
fitted conditional volatility, inspect the ACF of squared standardised
residuals and comment briefly on persistence and any remaining volatility
clustering. Compare the main findings with EUR/USD.

## Unit-root testing: EUR/USD levels and changes (Tutorial VII, old exercise 20)

Notebook: [Unit_Root_Testing.ipynb](Unit_Root_Testing.ipynb)

Analyse 192 monthly observations, January 2010-December 2025. Calculate log
changes from the last published USD-per-EUR quotation of each month. Plot
levels and changes, then apply ADF tests with AIC/BIC selection of up to
12 augmentation lags. Both criteria choose zero here. The level test does not
reject a unit root at 5%; the log-change test rejects. A further comparison
includes a deterministic linear trend in the level test.

### Relevant concepts

- Exchange-rate levels versus log changes; monthly observation dates and quotation units.
- Unit-root null; ADF regression; AIC/BIC augmentation-lag selection and nonstandard critical values.
- Rejection versus non-rejection; deterministic terms; unit roots versus broader stationarity requirements.

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

`daily_eur_usd.csv` contains 4,023 published daily quotations from December 2009
through December 2025, extracted directly from the
[Federal Reserve Board's H.10 historical euro table](https://www.federalreserve.gov/releases/h10/hist/dat00_eu.htm).
The equivalent FRED series is [DEXUSEU](https://fred.stlouisfed.org/series/DEXUSEU).
The rate is US dollars per euro, not seasonally adjusted: a rise means euro
appreciation against the dollar. These are New York noon buying rates, not
exchange closing prices. Dates labelled ND by the source are omitted without
interpolation, forward filling or inserted zero changes. The volatility notebook
selects all 1,249 published quotations in 2021-2025 after calculating daily log changes.

`monthly_eur_usd.csv` contains 193 observations derived from the same daily
source by retaining the last published quotation and its actual date in each
calendar month. December 2009 supplies only the first change's base, leaving
192 months in 2010-2025 for the unit-root analysis. Both notebooks calculate
`100 * diff(log(usd_per_eur))`; these are exchange-rate changes rather than
interest-inclusive investment returns.

The official source was retrieved on 15 October 2026. Its URL, raw-response hash,
omitted-observation count, transformations, definitions and CSV hashes are
recorded in `tutorial7_data_sources.json`. These are public-domain Federal Reserve
data, with Federal Reserve/FRED attribution retained.

## Running the notebooks

Follow the [shared setup instructions](../README.md). In Colab, upload the full
`Notebooks` folder to My Drive and preserve `Time_Series` and its CSV files.
The setup also supports local Jupyter from the course, `Notebooks` or tutorial
folder. No live data download or API key is required.

The volatility notebook uses `arch>=8.0,<9`. Its library cell installs this
dependency only if missing; local users can also install the shared requirements.
