# %% IMPORT LIBRARIES AND SETUP
# Import the necessary library for downloading financial data
import yfinance as yf
# Import pandas for data manipulation and analysis
import pandas as pd
# Import numpy for numerical operations and array manipulation
import numpy as np
# Import matplotlib.pyplot for creating visualizations
import matplotlib.pyplot as plt
# Import the 1-sample t-test function from scipy for hypothesis testing
from scipy.stats import ttest_1samp
# Import warnings to suppress unnecessary output messages during rolling windows
import warnings

# Suppress warnings to keep the console output clean
warnings.filterwarnings("ignore")

# Define a list containing the tickers: NYSE Composite Index and 13-week T-Bill
tickers = ['^NYA', '^IRX']

# Download historical data from Jan 2011 to Dec 2025 at a monthly frequency ('1mo')
data = yf.download(tickers, start='1990-01-01', end='2025-12-31', interval='1mo')

# Extract only the 'Close' prices from the downloaded multi-level DataFrame
data = data['Close'].dropna()

# Print the first 3 rows of the dataset to verify the download
print(data.head(3))


# %% CALCULATE EXCESS RETURNS
# Calculate the monthly log-returns for the NYSE index
nyse_ret = np.log(data['^NYA'] / data['^NYA'].shift(1))

# The ^IRX is quoted as an annualized percentage (e.g., a value of 5.0 means 5%).
# Convert the annualized percentage to a monthly decimal rate.
# Formula: (1 + Annual_Rate/100)^(1/12) - 1
rf_monthly = (1 + data['^IRX'] / 100)**(1/12) - 1

# Calculate the Monthly Excess Returns (Market Risk Premium)
# This represents the return of the market over the risk-free rate
excess_ret = (nyse_ret - rf_monthly).dropna()

# Print the first 3 rows of the calculated excess returns
print("\n--- Monthly Excess Returns ---")
print(excess_ret.head(3))


# %% CALCULATE AND PLOT ROLLING STATISTICS
# Define the list of window sizes (in months) to analyze
windows = [30, 40, 50, 60]

# Calculate the full-sample mean and standard deviation for comparison
full_mean = excess_ret.mean()
full_std = excess_ret.std()

# Create a figure with 2 subplots (stacked vertically) sharing the same x-axis
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# Loop through each window size to compute and plot rolling statistics
for w in windows:
    # Compute the rolling mean for the current window size
    rolling_mean = excess_ret.rolling(window=w).mean()
    # Compute the rolling standard deviation for the current window size
    rolling_std = excess_ret.rolling(window=w).std()
    
    # Plot the rolling mean on the first subplot
    ax1.plot(rolling_mean, label=f'w={w} months', alpha=0.8)
    # Plot the rolling standard deviation on the second subplot
    ax2.plot(rolling_std, label=f'w={w} months', alpha=0.8)

# Add a horizontal dashed line representing the full-sample mean
ax1.axhline(full_mean, color='black', linestyle='--', linewidth=2, label='Full Sample Mean')
# Set the title and y-axis label for the mean subplot
ax1.set_title('Dynamic Estimation: Rolling Average of Excess Returns')
ax1.set_ylabel('Rolling Mean')
# Display the legend
ax1.legend()
# Add a light grid for readability
ax1.grid(True, alpha=0.3)

# Add a horizontal dashed line representing the full-sample standard deviation
ax2.axhline(full_std, color='black', linestyle='--', linewidth=2, label='Full Sample Std Dev')
# Set the title, x-axis, and y-axis labels for the standard deviation subplot
ax2.set_title('Dynamic Estimation: Rolling Standard Deviation')
ax2.set_ylabel('Rolling Std Dev')
ax2.set_xlabel('Date')
# Display the legend
ax2.legend()
# Add a light grid for readability
ax2.grid(True, alpha=0.3)

# Adjust layout to prevent overlapping
plt.tight_layout()

# Display the figure in the Spyder Plots pane
plt.show()

"""
DISCUSSION (Rolling Statistics):
- The rolling mean shows that the 'average' excess monthly return is highly unstable over time.
- Smaller windows (w=30) react very quickly to market shocks but are extremely noisy.
- Larger windows (w=60) provide a smoother, more stable estimate of the parameter, 
  but they are slower to adapt to regime changes.
- The rolling standard deviation highlights periods of market stress where volatility spikes.
"""


# %% PERFORM ROLLING HYPOTHESIS TESTING (T-TEST)
# Define the window size for the hypothesis test (5 years = 60 months)
w_test = 60

# Define a custom function to perform the t-test on a given slice of data
def rolling_ttest(series):
    # Perform a 1-sample t-test testing if the population mean is 0
    t_stat, p_val = ttest_1samp(series, 0)
    # Return only the p-value
    return p_val

# Apply the custom t-test function to the rolling window of excess returns
rolling_pvals = excess_ret.rolling(window=w_test).apply(rolling_ttest)

# We also need the rolling mean to plot it on the same chart alongside the p-value
rolling_mean = excess_ret.rolling(window=w_test).mean()

# Create a new figure and primary axis for the plot
fig, ax1 = plt.subplots(figsize=(12, 6))

# --- PRIMARY Y-AXIS (p-values) ---
# Plot the rolling p-values on the left y-axis
ax1.plot(rolling_pvals, color='purple', linewidth=1.5, label='Rolling p-value (w=60)')

# Add a horizontal dashed line at the 0.05 (5%) significance threshold
ax1.axhline(0.05, color='red', linestyle='--', linewidth=2, label='Significance Level (5%)')

# Set the title and primary axis labels
ax1.set_title('Statistical Inference: ERP Significance vs. Magnitude')
ax1.set_ylabel('p-value', color='purple')
ax1.set_xlabel('Date')
# Set the primary y-axis limits from 0 to slightly above 1
ax1.set_ylim(0, 1.05)
# Add a light grid for readability linked to the primary axis
ax1.grid(True, alpha=0.3)

# --- SECONDARY Y-AXIS (Rolling Mean) ---
# Create a secondary y-axis that shares the same x-axis
ax2 = ax1.twinx()

# Plot the rolling mean on the right y-axis
ax2.plot(rolling_mean, color='teal', linewidth=1.5, linestyle='-.', alpha=0.8, label='Rolling Mean (w=60)')

# Add a horizontal dotted line at 0 to show when the mean itself goes negative
ax2.axhline(0, color='black', linestyle=':', alpha=0.6, label='Zero Mean')

# Set the secondary y-axis label
ax2.set_ylabel('Rolling Mean Excess Return', color='teal')

# --- COMBINE LEGENDS ---
# Extract lines and labels from both axes to create a single unified legend
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')

# Automatically adjust layout to fit both axes cleanly
plt.tight_layout()

# Display the figure in the Spyder Plots pane
plt.show()

"""
DISCUSSION (Hypothesis Testing & Asymptotic Validity):
- What are we exactly testing?: It is crucial to understand that the rolling window 
  (w=60) is the sample size (n=60 months), NOT the holding period. The t-test answers 
  this specific question: "Given these specific 5 years, 
  if I had invested in the market for a single randomly chosen month, would my expected 
  excess return have been statistically greater than zero?".
- Signal vs Noise (The Dual Axis): Looking at the chart, the teal line (mean) often 
  stays visibly above zero. However, the purple line (p-value) rarely drops below 0.05. 
  This teaches a fundamental lesson in econometrics: a positive average return is meaningless 
  if the variance (noise) is so high that the t-statistic collapses. The market often fails 
  to reward risk with statistical certainty over 5-year macro regimes.
- Asymptotic Validity: Financial returns have fat tails 
  and violate the Normality assumption. We can still use a t-test here because of 
  the Central Limit Theorem (CLT). By using a rolling window of w=60 months, 'n' is large 
  enough to rely on the asymptotic normality of the estimator.
"""


# %% DYNAMIC HOLDING PERIOD: NON-OVERLAPPING RETURNS
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_1samp

# --- 1. PARAMETERS ---
H = 6  # Holding period in months
w_test = 60  # Rolling window size (number of INDEPENDENT periods needed)

# --- 2. CALCULATE NON-OVERLAPPING RETURNS ---
# To get strictly non-overlapping market returns, we slice the price series every H months
prices_h = data['^NYA'].iloc[::H]
market_ret_h = prices_h.pct_change().dropna()

# To align the risk-free rate, we calculate the H-month rolling compounded return
rf_gross = 1 + rf_monthly
rf_ret_rolling = rf_gross.rolling(window=H).apply(np.prod, raw=True) - 1

# And then we extract ONLY the exact dates that match our non-overlapping price slices
rf_ret_h = rf_ret_rolling.loc[market_ret_h.index]

# Calculate Non-overlapping Excess Returns
excess_h = (market_ret_h - rf_ret_h).dropna()

print(f"--- NON-OVERLAPPING ANALYSIS: {H}-MONTH HORIZON ---")
print(f"Total independent observations available: {len(excess_h)}")
print(f"Observations required for rolling window: {w_test}")

# --- 3. STANDARD INFERENCE (NO HAC NEEDED) ---
# Since observations are independent, we safely return to the standard t-test
def simple_ttest(series):
    t_stat, p_val = ttest_1samp(series, 0)
    return p_val

if len(excess_h) >= w_test:
    print("\nSufficient data found. Computing Rolling t-test...\n")
    
    # Calculate rolling p-values and means
    rolling_pvals = excess_h.rolling(window=w_test).apply(simple_ttest)
    rolling_mean = excess_h.rolling(window=w_test).mean()
    
    # Plotting
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Primary Axis: p-values
    ax1.plot(rolling_pvals, color='purple', linewidth=1.5, label=f'Rolling p-value (w={w_test})')
    ax1.axhline(0.05, color='red', linestyle='--', linewidth=2, label='5% Significance')
    ax1.set_title(f'Rolling Inference for NON-OVERLAPPING {H}-Month Returns')
    ax1.set_ylabel('p-value', color='purple')
    ax1.set_ylim(0, 1.05)
    ax1.grid(True, alpha=0.3)
    
    # Secondary Axis: Rolling Mean
    ax2 = ax1.twinx()
    ax2.plot(rolling_mean, color='teal', linewidth=1.5, linestyle='-.', alpha=0.8, label='Rolling Mean')
    ax2.axhline(0, color='black', linestyle=':', alpha=0.6)
    ax2.set_ylabel('Mean Excess Return', color='teal')
    
    # Combine legends
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')
    
    plt.tight_layout()
    plt.show()

else:
    print("\nNot enough data for rolling windows. Proceeding with FULL SAMPLE t-test...\n")
    
    t_stat, p_val = ttest_1samp(excess_h, 0)
    mean_ret = excess_h.mean()
    win_rate = (excess_h > 0).mean() * 100
    
    print(f"Empirical Win Rate:  {win_rate:.1f}%")
    print(f"Mean Excess Return:  {mean_ret:.4f}")
    print(f"Standard t-statistic: {t_stat:.4f}")
    print(f"Standard p-value:     {p_val:.4f}")
    
    # Plotting Distribution
    plt.figure(figsize=(9, 5))
    # We use fewer bins since we have fewer observations in the non-overlapping sample
    plt.hist(excess_h, bins=15, color='dodgerblue', edgecolor='black', alpha=0.7)
    plt.axvline(0, color='red', linestyle='--', linewidth=2, label='Zero Premium')
    plt.axvline(mean_ret, color='green', linestyle='-', linewidth=2, label=f'Mean: {mean_ret:.2%}')
    plt.title(f'Distribution of Independent {H}-Month Returns\n(t-stat: {t_stat:.2f} | p-val: {p_val:.3f})')
    plt.xlabel('Excess Return')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()

"""
DISCUSSION (Non-Overlapping Returns):
- Independent Observations: By sampling the data strictly every H months, we 
  eliminate the overlap. The return from Jan-Jun shares no data with Jul-Dec.
- Econometric Simplicity: Because the observations are now independent, the 
  serial correlation issue disappears. We no longer need robust HAC standard errors 
  and can rely on the standard Student's t-test for inference.
- The Data Trade-off: The cost of using non-overlapping data is sample size. 
  A 6-month holding period reduces our available data points by a factor of 6. 
  To perform a rolling test with a window of 60 independent observations, we need 
  at least 360 months of history.
"""