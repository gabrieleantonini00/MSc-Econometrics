# %% IMPORT LIBRARIES AND SETUP
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.diagnostic import het_arch
from statsmodels.graphics.tsaplots import plot_acf
from arch import arch_model
from scipy.stats import chi2
import warnings

warnings.filterwarnings("ignore")

tickers = ['^GSPC', '^IXIC', '^GDAXI']

print("Downloading data...")
data = yf.download(tickers, start='2010-01-01', end='2022-08-01', auto_adjust=True)
prices = data['Close']
returns = prices.pct_change().dropna()

print("\nReturns head:")
print(returns.head(3))


# %% 1. VISUAL ANALYSIS & ACF
fig, axes = plt.subplots(3, 2, figsize=(12, 10))

for i, asset in enumerate(tickers):
    # Histogram
    axes[i, 0].hist(returns[asset], bins=100, color='steelblue', edgecolor='white')
    axes[i, 0].set_title(f"{asset} - Histogram")
    # Returns plot
    axes[i, 1].plot(returns[asset], color='darkslategray', linewidth=0.5)
    axes[i, 1].set_title(f"{asset} - Returns")

plt.tight_layout()
plt.show()

# ACF of Squared Returns
fig, axes = plt.subplots(3, 1, figsize=(8, 10))
for i, asset in enumerate(tickers):
    plot_acf(returns[asset]**2, ax=axes[i], lags=20, zero=False, title=f"{asset} - ACF of Squared Returns")

plt.tight_layout()
plt.show()

"""
DISCUSSION
- Returns are not normally distributed (fat tails, excess kurtosis).
- The ACF of squared returns shows significant persistence.
- Volatility clustering is highly visible in the plots.
"""


# %% 2. ARCH TEST
print("\n--- ARCH TEST ---")

for asset in tickers:
    # Perform the ARCH LM Test
    arch_test = het_arch(returns[asset])
    print(f"{asset}: p-value = {arch_test[1]:.5f}")

"""
DISCUSSION
- Very low p-values (≈ 0.000) for all series.
- We strongly reject the null hypothesis of no ARCH effects.
- Strong evidence of conditional heteroskedasticity; GARCH models are appropriate.
"""


# %% 3. GARCH MODEL ESTIMATION (GRID SEARCH)
print("\n--- GARCH ESTIMATION (AIC GRID SEARCH) ---")
garch_models = {}

for asset in tickers:
    best_aic = np.inf
    best_order = None
    best_model = None
    
    for p in range(1, 3):
        for q in range(1, 3):
            try:
                # Scale returns by 100 for convergence
                model = arch_model(returns[asset]*100, vol='GARCH', p=p, q=q)
                res = model.fit(disp='off')
                
                if res.aic < best_aic:
                    best_aic = res.aic
                    best_order = (p, q)
                    best_model = res
            except:
                continue
    
    garch_models[asset] = best_model
    print(f"{asset}: best (p,q) = {best_order}, AIC = {best_aic:.2f}")
    
    """
DISCUSSION (GARCH Parameters & Shock Persistence):
- Alpha (α) captures the ARCH effect: the immediate reaction to new market shocks (news).
- Beta (β) captures the GARCH effect: the persistence or memory of past volatility.
- Stationarity Condition: For the volatility to be mean-reverting (not exploding to infinity), 
  the sum of alpha and beta must be strictly less than 1 (α + β < 1). In daily financial data, 
  we typically observe a very high beta (>0.85) and a low alpha (<0.15). This indicates that 
  volatility shocks are highly persistent and decay slowly over time.
"""


# %% 4. VOLATILITY COMPARISON (FIXED SCALE)
lam1 = 0.94
lam2 = 0.97

for asset in tickers:
    plt.figure(figsize=(10, 5))
    
    # --- GARCH volatility (RESCALED by /100 to match raw returns)
    garch_vol = garch_models[asset].conditional_volatility / 100
    
    # --- Rolling std
    roll_20 = returns[asset].rolling(20).std()
    
    # --- EWMA
    ewma1 = returns[asset].ewm(alpha=1-lam1).std()
    
    # --- Plot
    plt.plot(garch_vol, label='GARCH', color='black', linewidth=1.5)
    plt.plot(roll_20, label='Rolling (20)', color='red', linestyle='--', alpha=0.7)
    plt.plot(ewma1, label='EWMA (0.94)', color='blue', linestyle=':', alpha=0.7)
    
    plt.title(f"{asset} - Volatility Comparison (Aligned Scale)")
    plt.legend()
    plt.show()


# %% 5. ZOOM ON CRISIS (COVID 2020)
print("\n--- ZOOMING IN: 2020 COVID CRISIS ---")
for asset in tickers:
    plt.figure(figsize=(10, 5))
    
    garch_vol = garch_models[asset].conditional_volatility / 100
    roll_20 = returns[asset].rolling(20).std()
    ewma1 = returns[asset].ewm(alpha=1-lam1).std()
    
    # Focus on 2020
    plt.plot(garch_vol['2020'], label='GARCH', color='black', linewidth=2)
    plt.plot(roll_20['2020'], label='Rolling (20)', color='red', linestyle='--')
    plt.plot(ewma1['2020'], label='EWMA (0.94)', color='blue', linestyle=':')
    
    plt.title(f"{asset} - Volatility (Crisis Zoom 2020)")
    plt.legend()
    plt.show()


# %% 6. MODEL SPECIFICATION TEST (LR TEST)
print("\n--- MODEL SPECIFICATION (LR TEST) ---")
# We test the specification for ^GSPC
target = '^GSPC'
opt_model = garch_models[target]

# Safely extract the optimal p and q from the model object
p_opt = opt_model.model.volatility.p
q_opt = opt_model.model.volatility.q

# Restricted orders: max{0, p-1} and max{0, q-1}
p_rest = max(0, p_opt - 1)
q_rest = max(0, q_opt - 1)

print(f"Testing optimal GARCH({p_opt},{q_opt}) vs restricted GARCH({p_rest},{q_rest}) for {target}...")

# CRITICAL FIX: The arch library crashes if you ask for vol='GARCH' with p=0 and q=0.
# A GARCH(0,0) is mathematically just a Constant Volatility model.
if p_rest == 0 and q_rest == 0:
    rest_model = arch_model(returns[target]*100, vol='Constant').fit(disp='off')
else:
    rest_model = arch_model(returns[target]*100, vol='GARCH', p=p_rest, q=q_rest).fit(disp='off')

# Calculate the Likelihood Ratio (LR) test statistic
loglik_opt = opt_model.loglikelihood
loglik_rest = rest_model.loglikelihood

lr_stat = 2 * (loglik_opt - loglik_rest)

# Degrees of freedom is the difference in number of estimated variance parameters
df_diff = (p_opt + q_opt) - (p_rest + q_rest)

# Calculate p-value
p_val_lr = 1 - chi2.cdf(lr_stat, df=df_diff)

print(f"LR Statistic: {lr_stat:.4f}")
print(f"p-value:      {p_val_lr:.4f}")

"""
DISCUSSION
- The p-value is close to 0.0000. 
- At a 5% type I error rate, we strongly reject the restricted model. 
- The AIC-selected optimal model captures volatility dynamics significantly better.
"""


# %% 7. FORECASTING
print("\n--- VOLATILITY FORECASTS (Out-of-Sample) ---")

for asset in tickers:
    res = garch_models[asset]
    forecasts = res.forecast(horizon=2)
    
    print(f"{asset}:")
    # Rescaling variance back to raw return space before taking sqrt
    print(f"  h=1: {np.sqrt(forecasts.variance.values[-1,0]) / 100:.5f}")
    print(f"  h=2: {np.sqrt(forecasts.variance.values[-1,1]) / 100:.5f}")

"""
DISCUSSION
- h=1 forecast reacts strongly to the latest shock.
- h=2 moves toward the unconditional (long-run) variance.
- This reflects the strong mean-reversion property of GARCH processes.
"""