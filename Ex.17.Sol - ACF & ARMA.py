# %% IMPORT LIBRARIES AND SETUP

# Import the numpy library for array handling and numerical operations
import numpy as np
# Import the pyplot module from matplotlib for creating visualizations
import matplotlib.pyplot as plt
# Import the ArmaProcess class to automatically generate theoretical ARMA structures
from statsmodels.tsa.arima_process import ArmaProcess
# Import the warnings module to handle warning messages
import warnings

# Suppress all warnings to keep the console output clean
warnings.filterwarnings("ignore")

# Define the number of lags to plot for our correlograms (0 to 10)
lags_plot = 10
# Create an array of integers representing the x-axis for our plots
lags_x = np.arange(lags_plot + 1)

print("Setup complete. Using statsmodels ArmaProcess for theoretical ACF.")


# %% PLOT MA(1) AUTOCORRELATION FUNCTION

# Print a separator line for the MA section
print("\n" + "="*50)
# Print the title for the MA(1) analysis
print("1. MA(1) PROCESS ACF ANALYSIS")
# Print the closing separator line
print("="*50)

# Define the specific theta values requested by the exercise
thetas = [-0.75, -0.5, 0, 0.5, 0.75]

# Initialize a figure with 5 subplots arranged horizontally, sharing the y-axis
fig, axes = plt.subplots(1, 5, figsize=(20, 4), sharey=True)
# Set the main title for the entire figure
fig.suptitle('Theoretical ACF of MA(1) Process: $y_t = c + \epsilon_t + \\theta\epsilon_{t-1}$', fontsize=16, y=1.05)

# Loop over the enumeration of the theta values to plot each one
for i, theta in enumerate(thetas):
    
    # Define the Autoregressive (AR) array. For a pure MA process, this is just [1]
    ar_params = np.array([1])
    # Define the Moving Average (MA) array. Structure is [1, theta_1]
    ma_params = np.array([1, theta])
    
    # Initialize the theoretical ARMA process object
    process = ArmaProcess(ar_params, ma_params)
    # Extract the theoretical autocorrelation function up to the specified lags
    acf_vals = process.acf(lags=lags_plot + 1)
    
    # Create a stem plot (lollipop chart) typical for correlograms
    axes[i].stem(lags_x, acf_vals, basefmt="black")
    # Set the title of the individual subplot to show the current theta
    axes[i].set_title(f'$\\theta = {theta}$')
    # Label the x-axis
    axes[i].set_xlabel('Lag')
    # Force the y-axis limits to be strictly between -1.1 and 1.1 for all plots
    axes[i].set_ylim(-1.1, 1.1)
    # Enable a light grid for better visual readability
    axes[i].grid(True, alpha=0.3)
    # Add a solid black horizontal line at y=0
    axes[i].axhline(0, color='black', linewidth=1)

# Set the y-axis label only for the leftmost plot
axes[0].set_ylabel('Autocorrelation $\\rho_k$')
# Adjust padding between subplots to avoid overlapping elements
plt.tight_layout()
# Display the final MA(1) figure
plt.show()

"""
DISCUSSION (MA(1)):
- Cut-off: The defining characteristic of the Moving Average process of order 1 is 
  that it has memory exactly equal to 1 lag. Visually, the theoretical ACF cuts off 
  abruptly and drops exactly to 0 from lag 2 onwards, matching our paper derivations.
- Sign: The sign of the first autocorrelation strictly matches the sign of the theta parameter.
"""


# %% PLOT AR(1) AUTOCORRELATION FUNCTION

# Print a separator line for the AR section
print("\n" + "="*50)
# Print the title for the AR(1) analysis
print("2. AR(1) PROCESS ACF ANALYSIS")
# Print the closing separator line
print("="*50)

# Define the specific rho values requested by the exercise
rhos = [-0.75, -0.5, 0, 0.5, 0.75]

# Initialize a figure with 5 horizontal subplots for the AR(1) process
fig, axes = plt.subplots(1, 5, figsize=(20, 4), sharey=True)
# Set the main title for the figure
fig.suptitle('Theoretical ACF of AR(1) Process: $y_t = c + \\rho y_{t-1} + \epsilon_t$', fontsize=16, y=1.05)

# Loop over the enumeration of the rho values
for i, rho_param in enumerate(rhos):
    
    # CRITICAL: statsmodels AR parameters require an inverted sign!
    # The library solves 1 - phi*L = 0, so we must input [1, -rho_param]
    ar_params = np.array([1, -rho_param])
    # The MA array is just [1] for a pure AR process
    ma_params = np.array([1])
    
    # Initialize the theoretical ARMA process object
    process = ArmaProcess(ar_params, ma_params)
    # Extract the theoretical autocorrelation function up to the specified lags
    acf_vals = process.acf(lags=lags_plot + 1)
    
    # Create the stem plot for the correlogram
    axes[i].stem(lags_x, acf_vals, basefmt="black")
    # Set the subplot title indicating the rho parameter
    axes[i].set_title(f'$\\rho = {rho_param}$')
    # Label the x-axis
    axes[i].set_xlabel('Lag')
    # Standardize the y-axis limits
    axes[i].set_ylim(-1.1, 1.1)
    # Enable the background grid
    axes[i].grid(True, alpha=0.3)
    # Add the zero-reference horizontal line
    axes[i].axhline(0, color='black', linewidth=1)

# Label the y-axis on the first subplot
axes[0].set_ylabel('Autocorrelation $\\rho_k$')
# Adjust the layout spacing
plt.tight_layout()
# Display the AR(1) figure
plt.show()

"""
DISCUSSION (AR(1)):
- Geometric Decay: Unlike the MA(1), the AR(1) process has infinite memory. The ACF 
  never drops exactly to zero; instead, it decays geometrically (exponentially).
- Alternating signs: When rho is positive (e.g., 0.75), the decay is smooth and 
  monotonically positive. When rho is negative (e.g., -0.75), the ACF alternates 
  signs (positive for even lags, negative for odd lags).
"""


# %% PLOT ARMA(1,1) AUTOCORRELATION FUNCTION

# Print a separator line for the ARMA section
print("\n" + "="*50)
# Print the title for the ARMA(1,1) analysis
print("3. ARMA(1,1) PROCESS ACF ANALYSIS")
# Print the closing separator line
print("="*50)

# Define the specific theta values requested for the ARMA grid
thetas_arma = [-0.8, -0.4, 0, 0.4, 0.8]

# Initialize a large grid figure (5 rows for rhos, 5 columns for thetas)
fig, axes = plt.subplots(len(rhos), len(thetas_arma), figsize=(20, 15), sharex=True, sharey=True)
# Set the overarching main title
fig.suptitle('Theoretical ACF of ARMA(1,1) Process', fontsize=20, y=1.02)

# Loop over the rows (rho parameters)
for i, rho_param in enumerate(rhos):
    # Loop over the columns (theta parameters)
    for j, theta in enumerate(thetas_arma):
        
        # Define AR parameters with the inverted sign convention for statsmodels
        ar_params = np.array([1, -rho_param])
        # Define MA parameters with standard sign convention
        ma_params = np.array([1, theta])
        
        # Initialize the theoretical process and calculate the ACF
        process = ArmaProcess(ar_params, ma_params)
        acf_vals = process.acf(lags=lags_plot + 1)
        
        # Plot the correlogram in the specific grid cell
        axes[i, j].stem(lags_x, acf_vals, basefmt="black")
        
        # If we are on the top row, set the column titles to show the theta values
        if i == 0:
            axes[i, j].set_title(f'$\\theta = {theta}$', fontsize=14)
        
        # If we are on the leftmost column, set the row labels to show the rho values
        if j == 0:
            axes[i, j].set_ylabel(f'$\\rho = {rho_param}$', fontsize=14)
            
        # Enable the grid for readability
        axes[i, j].grid(True, alpha=0.3)
        # Force uniform y-axis limits
        axes[i, j].set_ylim(-1.1, 1.1)
        # Add the zero-reference line
        axes[i, j].axhline(0, color='black', linewidth=1)

# Loop through the bottom row specifically to add the x-axis labels
for j in range(len(thetas_arma)):
    axes[-1, j].set_xlabel('Lag')

# Optimize the layout to handle the large grid smoothly
plt.tight_layout()
# Display the massive ARMA(1,1) comparative grid
plt.show()

"""
DISCUSSION (ARMA(1,1)):
- Hybrid Structure: The ARMA(1,1) ACF is a combination of both behaviors. 
- Lag 1: The first lag is a complex mix dictated by both rho and theta. 
- Lag > 1: From lag 2 onwards, the Moving Average memory strictly expires. The decay 
  pattern from that point forward behaves identically to an AR(1) process, governed 
  solely by the autoregressive parameter (rho). The theta parameter merely dictates 
  the 'starting height' of this geometric decay.
"""