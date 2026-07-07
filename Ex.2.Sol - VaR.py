# %% IMPORT LIBRARIES AND SETUP
# Import the necessary library for downloading financial data
import yfinance as yf
# Import pandas for data manipulation and analysis
import pandas as pd
# Import numpy for numerical operations
import numpy as np
# Import matplotlib.pyplot for visualizations
import matplotlib.pyplot as plt
# Import normal distribution to calculate parametric risk metrics
from scipy.stats import norm

# Define the tickers: S&P 500 Index and Bitcoin
tickers = ['^GSPC', 'BTC-USD']

# Download historical data (using 2015-2023 to capture significant BTC history)
data = yf.download(tickers, start='2015-01-01', end='2025-12-31', auto_adjust=True)

# Extract only the 'Close' prices
prices = data['Close']

# Calculate daily simple returns and drop the initial NaN row
returns = prices.pct_change().dropna()

# Print the first few rows to verify
print("Daily Returns Head:")
print(returns.head())


# %% CALCULATE VALUE AT RISK (VaR) AT 1% LEVEL
# Set the confidence level for the left tail (alpha = 0.01 means 99% Confidence Level)
alpha = 0.01

# Initialize dictionaries to store our risk metrics
var_historical = {}
var_parametric = {}

# Loop through each asset to calculate the VaR
for asset in tickers:
    asset_returns = returns[asset].dropna()
    
    # 1. HISTORICAL VaR: The actual empirical 1st percentile of the data
    # This makes no assumptions about the distribution shape
    var_historical[asset] = np.percentile(asset_returns, alpha * 100)
    
    # 2. PARAMETRIC VaR: Assumes returns follow a Normal distribution
    # VaR = mean + (Z-score * standard_deviation)
    mu = np.mean(asset_returns)
    sigma = np.std(asset_returns, ddof=1)
    z_score = norm.ppf(alpha) # Critical value for 1% left tail (approx -2.33)
    
    var_parametric[asset] = mu + (z_score * sigma)

print("\n--- 1% Daily Value at Risk (VaR) ---")
for asset in tickers:
    print(f"{asset}:")
    print(f"  Historical VaR (Actual):     {var_historical[asset]:.4%}")
    print(f"  Parametric VaR (Normal):     {var_parametric[asset]:.4%}")


# %% (OPTIONAL) PLOT HISTOGRAMS AND TAIL RISK (VaR COMPARISON)
# Create a figure with 1 row and 2 columns for the subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for i, asset in enumerate(tickers):
    ax = axes[i]
    asset_returns = returns[asset].dropna()
    
    # Plot the histogram of returns with 100 bins for granularity
    ax.hist(asset_returns, bins=100, density=True, alpha=0.6, color='steelblue', edgecolor='black')
    
    # Overlay the Parametric Normal Distribution curve for comparison
    mu = np.mean(asset_returns)
    sigma = np.std(asset_returns, ddof=1)
    x = np.linspace(asset_returns.min(), asset_returns.max(), 1000)
    ax.plot(x, norm.pdf(x, mu, sigma), 'k--', linewidth=2, label='Normal Dist fit')
    
    # Draw vertical lines for the VaR thresholds
    ax.axvline(var_parametric[asset], color='red', linestyle='dashed', linewidth=2, 
               label=f'Normal VaR (1%): {var_parametric[asset]:.2%}')
    ax.axvline(var_historical[asset], color='purple', linestyle='solid', linewidth=2, 
               label=f'Historical VaR (1%): {var_historical[asset]:.2%}')
    
    # Focus the x-axis slightly on the left tail to make the difference visible
    ax.set_xlim([asset_returns.min(), np.percentile(asset_returns, 95)])
    
    # Labels and title
    ax.set_title(f"{asset} - Return Distribution & Tail Risk")
    ax.set_xlabel("Daily Returns")
    ax.set_ylabel("Frequency (Density)")
    ax.legend(loc='upper left')

plt.tight_layout()
# Display the figure in the Spyder Plots pane
plt.show()

"""
DISCUSSION (Tail Risk & VaR):
- The parametric approach assumes returns are normally distributed.
- The red dashed line shows the Normal VaR: where the model "thinks" the 1% worst days begin.
- The purple solid line shows the Historical VaR: where the actual 1% worst days began.
- For both S&P 500 and Bitcoin, the Historical VaR is further to the left (more negative) 
  than the Normal VaR. This visually proves that the Normal distribution has "thinner tails" 
  than reality, drastically underestimating the magnitude of extreme market crashes.
"""


# %% BACKTESTING: EXPECTED VS ACTUAL EXCEEDANCES
# Let's count how many times the real returns actually breached the Normal VaR threshold.
# Under the normal distribution assumption, this should happen exactly 1% of the time.

print("\n--- Backtesting: Breaches of Parametric Normal VaR ---")

for asset in tickers:
    asset_returns = returns[asset].dropna()
    total_days = len(asset_returns)
    
    # Expected number of breaches (1% of total trading days)
    expected_breaches = total_days * alpha
    
    # Actual number of days where the return was worse than the Parametric VaR
    actual_breaches = np.sum(asset_returns < var_parametric[asset])
    
    # Calculate the empirical probability of a breach
    empirical_prob = actual_breaches / total_days
    
    print(f"\nAsset: {asset} (Total Days: {total_days})")
    print(f"  Expected crashes (worse than Normal VaR):  {expected_breaches:.1f} days ({alpha:.2%})")
    print(f"  Actual crashes (worse than Normal VaR):    {actual_breaches} days ({empirical_prob:.2%})")

"""
DISCUSSION (Backtesting & Risk Underestimation):
- If the world were normally distributed, the actual breaches would closely match the expected breaches.
- In reality, the actual number of crashes exceeding the Normal VaR is significantly higher.
- For example, if the empirical probability is around 1.8% or 2.0% instead of 1.0%, 
  it means extreme crashes happen nearly twice as often as a Gaussian model predicts.
- This is the danger of "fat tails" (excess kurtosis): using basic OLS or standard normal 
  assumptions in risk management (without robust methods or alternative distributions like 
  Student-t) can lead to catastrophic under-capitalization during market distress.
"""