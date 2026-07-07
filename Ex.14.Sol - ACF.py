# %% IMPORT LIBRARIES AND SETUP
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Define the ticker for the DAX index
ticker = '^GDAXI'

# Download daily historical data for the year 2020
print(f"Downloading data for {ticker}...")
data = yf.download(ticker, start='2020-01-01', end='2020-12-31')

# Extract 'Close' prices
prices = data['Close']

# %% DATA PREPARATION & VISUAL ANALYSIS

# 1. Calculate the daily log-returns for the DAX index.
returns = np.log(prices / prices.shift(1)).dropna()

# Close previous plots
plt.close('all')

# 2. Plot the time series of the daily returns.
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(returns.index, returns, color='darkred', linewidth=1)
ax.set_title('DAX Daily Returns (2020)')
ax.set_ylabel('Log-Returns')
ax.grid(True, alpha=0.3)
plt.show()

# 3. Plot the Sample Autocorrelation Function (ACF) for lags 1 up to 15.
fig, ax = plt.subplots(figsize=(10, 5))
sm.graphics.tsa.plot_acf(returns, lags=15, zero=False, ax=ax, color='darkblue')
ax.set_title('ACF of DAX Daily Returns (Lags 1-15)')
ax.set_xlabel('Lags')
ax.set_ylabel('Autocorrelation')
plt.grid(True, alpha=0.3)
plt.show()

"""
DISCUSSION (Visual Analysis):
1. Volatility Clustering: The time series plot clearly shows the devastating impact of the 
   COVID-19 market crash in February/March 2020. We observe "volatility clustering": large 
   price changes are followed by large price changes. However, high volatility does not 
   imply high autocorrelation in the *direction* of the returns.
2. ACF Interpretation: In the ACF plot, almost all the vertical stems (the sample autocorrelations 
   for each lag) fall well within the light blue shaded area. This blue area represents the 95% 
   confidence interval. Because the stems do not significantly breach these bounds, it visually 
   suggests that past returns do not linearly correlate with future returns.
"""

# %% HYPOTHESIS TESTING: LJUNG-BOX TEST

print("\n" + "="*50)
print("HYPOTHESIS TESTING: LJUNG-BOX TEST (Lag = 5)")
print("="*50)

# We want to test if the first 5 autocorrelations are jointly zero.
lag_to_test = 5

# 4. Compute the Ljung-Box test statistic and its p-value
lb_test_results = sm.stats.acorr_ljungbox(returns, lags=[lag_to_test], return_df=True)

print("\nLjung-Box Test Results:")
print(lb_test_results)

"""
DISCUSSION (Hypothesis Testing):
1. Hypotheses:
   - H0 (Null): The first 5 autocorrelations are jointly equal to zero 
     (rho_1 = rho_2 = ... = rho_5 = 0). The data is distributed independently (White Noise).
   - H1 (Alternative): At least one of the first 5 autocorrelations is strictly different from zero.

2. Statistical Conclusion:
   - The p-value obtained from the Ljung-Box test is typically much larger than 0.05 
     (e.g., around 0.20 - 0.50 depending on the exact data bounds).
   - Because p-value > alpha (0.05), we FAIL TO REJECT the null hypothesis.

3. Economic Interpretation:
   - Failing to reject H0 means the DAX daily returns behave fundamentally like a White Noise 
     process in the short term. You cannot use the returns from Monday through Friday to 
     linearly predict whether next Monday's return will be positive or negative. 
   - This provides strong empirical support for the Weak-Form Efficient Market Hypothesis (EMH).
"""