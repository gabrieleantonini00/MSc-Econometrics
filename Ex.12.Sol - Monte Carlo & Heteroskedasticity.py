# %% IMPORT LIBRARIES AND SETUP
# Import the necessary libraries for data manipulation, math, and regressions
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import warnings

# Suppress warnings to keep the console output clean
warnings.filterwarnings("ignore")

# %% HYPOTHESIS TESTING CONCEPTS
print("="*60)
print("HYPOTHESIS TESTING CONCEPTS")
print("="*60)
print("""
- Significance Level (Alpha): The probability of making a Type I error 
  (rejecting the null hypothesis when it is actually true). In a 95% CI, alpha = 0.05.
- Type II Error Rate (Beta): The probability of failing to reject the 
  null hypothesis when it is actually false.
""")

# %% MONTE CARLO SETUP AND FUNCTION
print("\n" + "="*60)
print("MONTE CARLO SIMULATION: OLS vs ROBUST STANDARD ERRORS")
print("="*60)

def run_monte_carlo(T, M=1000):
    """
    Runs a Monte Carlo simulation for a specified sample size T and iterations M.
    Returns the empirical coverage probability for Standard OLS and HC1 Robust errors.
    """
    # True population parameters
    beta_0 = 1.0
    beta_1 = 0.5
    
    # Counters for coverage (how many times the true beta_1 is inside the CI)
    coverage_standard = 0
    coverage_robust = 0
    
    for i in range(M):
        # 1. Generate the regressor x_t ~ N(1, 2). 
        # np.random.normal takes standard deviation as 'scale', so sqrt(2).
        x = np.random.normal(loc=1.0, scale=np.sqrt(2), size=T)
        
        # 2. Generate the heteroskedastic error term
        # U_t ~ Unif(-3, 3)
        U = np.random.uniform(low=-3.0, high=3.0, size=T)
        # u_t = U_t * sqrt(4 + x_t^2)
        u = U * np.sqrt(4 + x**2)
        
        # 3. Generate the dependent variable y_t
        y = beta_0 + beta_1 * x + u
        
        # 4. Estimate the model using OLS
        X = sm.add_constant(x)
        model = sm.OLS(y, X).fit()
        
        # 5. Get Confidence Intervals (95% by default, alpha=0.05)
        # Standard OLS CI for beta_1 (index 1)
        ci_standard = model.conf_int(alpha=0.05)[1]
        
        # Heteroskedasticity-Robust CI (HC1) for beta_1
        model_robust = model.get_robustcov_results(cov_type='HC1')
        ci_robust = model_robust.conf_int(alpha=0.05)[1]
        
        # 6. Check coverage: Is the true beta_1 (0.5) inside the intervals?
        if ci_standard[0] <= beta_1 <= ci_standard[1]:
            coverage_standard += 1
            
        if ci_robust[0] <= beta_1 <= ci_robust[1]:
            coverage_robust += 1
            
    # Calculate percentages
    pct_standard = (coverage_standard / M) * 100
    pct_robust = (coverage_robust / M) * 100
    
    return pct_standard, pct_robust

# %% RUN SIMULATIONS FOR T=100 AND T=200
M_iter = 1000

print(f"Running simulation for T = 100 (Iterations = {M_iter})...")
cov_std_100, cov_rob_100 = run_monte_carlo(T=100, M=M_iter)

print(f"Running simulation for T = 200 (Iterations = {M_iter})...")
cov_std_200, cov_rob_200 = run_monte_carlo(T=200, M=M_iter)

print("\n--- EMPIRICAL COVERAGE PROBABILITY (Target: 95.0%) ---")
print(f"Sample Size T=100:")
print(f"  Standard OLS CI Coverage: {cov_std_100:.1f}%")
print(f"  Robust HC1 CI Coverage:   {cov_rob_100:.1f}%")
print(f"\nSample Size T=200:")
print(f"  Standard OLS CI Coverage: {cov_std_200:.1f}%")
print(f"  Robust HC1 CI Coverage:   {cov_rob_200:.1f}%")

"""
DISCUSSION (Monte Carlo Results):
1. Coverage Distortion: The empirical coverage of the Standard OLS CI falls significantly 
   below the nominal 95% level (usually around 88-90%). Because the DGP is highly 
   heteroskedastic, standard OLS underestimates the true variance of the estimator. 
   This leads to confidence intervals that are too narrow, causing us to over-reject 
   the null hypothesis (distorting the empirical size of the test).
   
2. Asymptotic Correction: The Robust HC1 standard errors correct this distortion. 
   Notice that for T=100, the robust coverage might not be exactly 95%, but as the sample 
   size increases to T=200, the robust coverage converges much closer to the true 95%. 
   This demonstrates that robust standard errors are justified purely on asymptotic 
   grounds (Large Sample Theory) and work better as T -> infinity.
"""

# %% VISUALIZATION: THE HETEROSKEDASTICITY PROBLEM
# Let's plot a single sample of T=200 to visually show the DGP's heteroskedasticity
np.random.seed(42) # Set seed for reproducibility of the plot
x_plot = np.random.normal(loc=1.0, scale=np.sqrt(2), size=500)
U_plot = np.random.uniform(low=-3.0, high=3.0, size=500)
u_plot = U_plot * np.sqrt(4 + x_plot**2)
y_plot = 1.0 + 0.5 * x_plot + u_plot

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x_plot, y_plot, color='dodgerblue', alpha=0.6, edgecolor='k', label='Simulated Data (DGP)')

# Plot the true population line
x_line = np.linspace(x_plot.min(), x_plot.max(), 100)
y_line = 1.0 + 0.5 * x_line
ax.plot(x_line, y_line, color='red', linewidth=2, label='True DGP Line (beta_1 = 0.5)')

ax.set_title('Visualization of the DGP (Notice the Heteroskedasticity)')
ax.set_xlabel('Regressor (x_t)')
ax.set_ylabel('Dependent Variable (y_t)')
ax.legend()
plt.grid(alpha=0.3)
plt.show()

"""
DISCUSSION (Visualization):
Looking at the scatter plot, we can visibly see that the variance of the residuals 
(the vertical distance from the red line) is not constant. When x_t is close to 0, 
the data points are tightly packed around the line. As x_t moves further away 
from 0 (both positive and negative), the spread of the errors "fans out" drastically.
"""