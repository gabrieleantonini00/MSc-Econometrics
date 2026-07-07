# %% IMPORT LIBRARIES AND SETUP
# Import the necessary library for downloading financial data
import yfinance as yf
# Import pandas for data manipulation and analysis
import pandas as pd
# Import numpy for numerical operations and array manipulation
import numpy as np
# Import matplotlib.pyplot for creating visualizations
import matplotlib.pyplot as plt
# Import skew and kurtosis functions from scipy for statistical analysis
from scipy.stats import skew, kurtosis

# Define a dictionary containing the tickers grouped by sector
tickers = {
    'IT': ['AAPL', 'MSFT', 'GOOGL'],
    'Energy': ['XOM', 'CVX', 'COP'],
    'Healthcare': ['JNJ', 'PFE', 'MRK']
}

# Flatten the dictionary into a single list of tickers using list comprehension
flat_tickers = [ticker for sector in tickers.values() for ticker in sector]

# Download historical stock data for all tickers from Jan 2010 to Dec 2022
# auto_adjust=True automatically adjusts prices for splits and dividends
data = yf.download(flat_tickers, start='2010-01-01', end='2025-12-31', auto_adjust=True)

# Extract only the 'Close' prices from the downloaded multi-level DataFrame
data = data['Close']

# Print the first 3 rows of the dataset to verify the download
print(data.head(3))


# %% PLOT PRICES AND NORMALIZED PRICES
# Create a figure and a 3x3 grid of subplots, setting the overall size to 18x12 inches
fig, axes = plt.subplots(3, 3, figsize=(18, 12))

# Flatten the 3x3 axes matrix into a 1D array to easily loop through it
axes = np.ravel(axes)

# Loop through each ticker and its corresponding index
for i, ticker in enumerate(flat_tickers):
    # Select the current subplot axis
    ax = axes[i]
    # Extract the price series for the current ticker
    series = data[ticker]

    # Plot the original price series on the primary y-axis
    ax.plot(series.index, series, label='Price')
    # Set the title of the subplot to the ticker symbol
    ax.set_title(ticker)

    # Create a secondary y-axis that shares the same x-axis
    ax2 = ax.twinx()
    # Calculate the normalized price (base 100 at the first available date)
    normalized = series / series.iloc[0] * 100
    # Plot the normalized price on the secondary y-axis with a dashed line
    ax2.plot(series.index, normalized, linestyle='--', alpha=0.6, label='Normalized to 100')
    # Reduce the font size of the secondary y-axis labels for better readability
    ax2.tick_params(axis='y', labelsize=8)

# Loop through any remaining empty subplots (if tickers are less than 9)
for j in range(len(flat_tickers), len(axes)):
    # Turn off the axis for empty subplots to keep the figure clean
    axes[j].axis('off')

# Automatically adjust subplots to fit into the figure area without overlapping
plt.tight_layout()

# Display the figure in the Spyder Plots pane
plt.show()

"""
DISCUSSION (Prices):
All stock price series display a clear upward trend over time, especially IT stocks. 
This indicates non-stationarity, meaning the mean and variance of the series are not constant over time.
- IT stocks show strong and consistent growth from 2010 to 2022.
- Energy stocks exhibit higher relative volatility, with noticeable drops during oil price shocks.
- Healthcare stocks have fewer extreme movements compared to Energy.
- Market corrections (e.g., 2020 COVID-19 crash) are visible across all sectors.
"""


# %% CALCULATE AND PLOT SIMPLE RETURNS
# Calculate daily simple returns (percentage change) and drop the first row (NaN)
returns = data.pct_change().dropna()

# Create a new figure and a 3x3 grid of subplots for returns
fig, axes = plt.subplots(3, 3, figsize=(18, 12))
# Flatten the axes array
axes = np.ravel(axes)

# Loop through each ticker to plot its returns
for i, ticker in enumerate(flat_tickers):
    # Plot the daily returns for the current ticker
    axes[i].plot(returns.index, returns[ticker])
    # Set the title of the subplot
    axes[i].set_title(f"{ticker} - Daily Returns")

# Hide any unused subplots
for j in range(len(flat_tickers), len(axes)):
    axes[j].axis('off')

# Adjust layout to prevent overlapping
plt.tight_layout()

# Display the figure in the Spyder Plots pane
plt.show()

"""
DISCUSSION (Returns):
- Technology stocks clearly exhibit the highest and most persistent volatility.
- Energy shows periods of both high and low volatility depending on market conditions.
- Healthcare remains the most stable sector overall, with consistently lower volatility.
"""


# %% PLOT BOXPLOTS OF RETURNS
# Create a new figure and a 3x3 grid of subplots for boxplots
fig, axes = plt.subplots(3, 3, figsize=(18, 12))
# Flatten the axes array
axes = np.ravel(axes)

# Loop through each ticker to create a boxplot
for i, ticker in enumerate(flat_tickers):
    # Draw a boxplot of the returns for the current ticker
    axes[i].boxplot(returns[ticker])
    # Set the title of the subplot
    axes[i].set_title(f"{ticker} - Returns Boxplot")

# Hide any unused subplots
for j in range(len(flat_tickers), len(axes)):
    axes[j].axis('off')

# Adjust layout to prevent overlapping
plt.tight_layout()

# Display the figure in the Spyder Plots pane
plt.show()

"""
DISCUSSION (Boxplots):
The median daily return is close to zero for all sectors, consistent with efficient market behavior.
All sectors occasionally experience severe daily returns, with Technology and Energy showing more extreme outliers.
"""


# %% PLOT HISTOGRAMS OF RETURNS
# Create a new figure and a 3x3 grid of subplots for histograms
fig, axes = plt.subplots(3, 3, figsize=(18, 12))
# Flatten the axes array
axes = np.ravel(axes)

# Loop through each ticker to create a histogram
for i, ticker in enumerate(flat_tickers):
    # Draw a histogram using 50 bins and add a black edge to the bars for clarity
    axes[i].hist(returns[ticker], bins=50, edgecolor='black')
    # Set the title of the subplot
    axes[i].set_title(f"{ticker} - Returns Histogram")

# Hide any unused subplots
for j in range(len(flat_tickers), len(axes)):
    axes[j].axis('off')

# Adjust layout to prevent overlapping
plt.tight_layout()

# Display the figure in the Spyder Plots pane
plt.show()

"""
DISCUSSION (Histograms):
- Return distributions are not perfectly normal, though the mean is near zero.
- Technology and Energy stocks have wider distributions with heavier tails.
- Healthcare returns are more concentrated.
"""


# %% CALCULATE SKEWNESS AND KURTOSIS
# Initialize an empty DataFrame to store the statistical results, using tickers as the index
stats_df = pd.DataFrame(index=returns.columns)

# Calculate the skewness for each column (ticker) and store it in the DataFrame
stats_df['Skewness'] = returns.apply(skew)
# Calculate the excess kurtosis for each column and store it in the DataFrame
stats_df['Kurtosis'] = returns.apply(kurtosis)

# Print a header for the results
print("\n--- Skewness and Kurtosis of daily returns ---")
# Print the final DataFrame containing the statistics
print(stats_df)

"""
DISCUSSION (Moments):
Most stocks have skewness near zero, so returns are roughly symmetric.
Kurtosis is above 3 for all stocks, indicating fat tails (leptokurtic distributions) 
and a higher probability of extreme returns than a normal distribution would predict. 
Energy stocks in this case show particularly high kurtosis.
"""