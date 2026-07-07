# %% IMPORT LIBRARIES AND SETUP
# Import the necessary libraries for downloading data and data manipulation
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import statsmodels for econometric regressions
import statsmodels.api as sm
import warnings

warnings.filterwarnings("ignore")

# Define the tickers: Apple (Stock), S&P 500 (Market), and 13-Week T-Bill (Risk-Free Rate)
tickers = ['AAPL', '^GSPC', '^IRX']

# Download monthly historical data from Jan 2000 to Dec 2025
# We use interval='1mo' to get monthly data directly
print("Downloading data...")
data = yf.download(tickers, start='2000-01-01', end='2025-12-31', interval='1mo')

# Extract only the 'Close' prices and drop rows with missing values
prices = data['Close'].dropna()

# Print the first few rows to verify
print("Monthly Prices Head:")
print(prices.head())


# %% DATA PREPARATION: LOG RETURNS AND EXCESS RETURNS

# 1. Calculate the monthly log-returns for the stock (AAPL) and the market (^GSPC)
log_returns = np.log(prices[['AAPL', '^GSPC']] / prices[['AAPL', '^GSPC']].shift(1))

# Handle the Risk-Free Rate (^IRX)
# ^IRX is quoted in annualized percentage points (e.g., 5.0 means 5%). 
# Convert to decimal and then to a monthly rate.
rf_monthly = (prices['^IRX'] / 100) / 12

# Drop the first row (NaN due to the shift in returns calculation)
log_returns = log_returns.dropna()
rf_monthly = rf_monthly.loc[log_returns.index]

# 2. Calculate the Excess Returns for the stock (rt) and the market (rm,t)
excess_ret_stock = log_returns['AAPL'] - rf_monthly
excess_ret_market = log_returns['^GSPC'] - rf_monthly

# Combine into a single DataFrame for easier handling
excess_returns = pd.DataFrame({
    'Stock': excess_ret_stock,
    'Market': excess_ret_market
})


# %% ROLLING WINDOW REGRESSION (CAPM)

# Set the rolling window size (60 months = 5 years)
window = 60

# Initialize lists to store our results
rolling_betas = []
rolling_se = []
dates = []

print(f"\nRunning {window}-month rolling regressions...")

# Loop from the end of the first window to the end of the dataset
for i in range(window, len(excess_returns)):
    
    # 3. Extract the data for the current 60-month window
    y_window = excess_returns['Stock'].iloc[i-window : i]
    X_window = excess_returns['Market'].iloc[i-window : i]
    
    # Add a constant (alpha) to the independent variable
    X_window = sm.add_constant(X_window)
    
    # 4. Fit the OLS model using statsmodels
    model = sm.OLS(y_window, X_window).fit()
    
    # Extract the slope coefficient (Beta) and its standard error
    beta = model.params['Market']
    se = model.bse['Market']
    
    # Store the results and the corresponding date (end of the window)
    rolling_betas.append(beta)
    rolling_se.append(se)
    dates.append(excess_returns.index[i-1])

# Convert lists to numpy arrays
rolling_betas = np.array(rolling_betas)
rolling_se = np.array(rolling_se)


# %% VISUALIZATION: ROLLING BETA AND CONFIDENCE BANDS

# 5. Calculate the 95% Confidence Intervals
# Using the critical value of 1.96 for a 95% confidence level
upper_band = rolling_betas + (1.96 * rolling_se)
lower_band = rolling_betas - (1.96 * rolling_se)

# Plotting
plt.figure(figsize=(12, 6))

# Plot the Rolling Beta
plt.plot(dates, rolling_betas, label='Rolling 60-Month Market Beta', color='blue', linewidth=2)

# Plot the Confidence Bands
plt.fill_between(dates, lower_band, upper_band, color='blue', alpha=0.2, label='95% Confidence Band')

# Formatting the plot
plt.axhline(1.0, color='red', linestyle='--', label='Beta = 1.0 (Market Neutral)')
plt.title('Rolling 60-Month CAPM Beta for AAPL (2000 - 2025)', fontsize=14)
plt.xlabel('Date (End of Window)', fontsize=12)
plt.ylabel('Estimated Beta', fontsize=12)
plt.legend(loc='best')
plt.grid(True, linestyle=':', alpha=0.7)

plt.tight_layout()
plt.show()

"""
DISCUSSION (Parameter Stability & Structural Shifts):
1. Stability: The assumption of a static, constant Beta over a 25-year horizon is strongly rejected visually. The Beta fluctuates significantly, starting high in the early 2000s and undergoing various structural shifts over the decades. This highlights the risk of using full-sample static OLS in long time-series financial data.

2. Structural Shifts & Economics: 
   - Early 2000s (Tech Bubble aftermath): AAPL behaves like a high-growth, highly volatile tech stock with a Beta > 1.5.
   - 2010s (Maturation): AAPL matures. Beta converge towards 1.0 (moving closer to the broader market risk profile).
   - Shocks: Brief spikes or dips in Beta often correspond to specific crisis periods where correlation structures break down (e.g., 2008 Financial Crisis, 2020 COVID-19 shock). When rolling windows ingest these extreme outliers, the estimated parameters shift abruptly.

3. Confidence Bands: 
   - A wider confidence band indicates higher standard errors for the Beta estimate in that specific 5-year window. This typically occurs during periods of high idiosyncratic volatility (the residual variance 'u_t' increases) or when market returns lack variation. 
   - Conversely, narrower bands indicate a tighter, more precise relationship between the stock and the market during calmer macro environments.
"""