import numpy as np
import pandas as pd

class SyntheticMarketDataGenerator:
    def __init__(self, seed=42):
        np.random.seed(seed)

    def generate_equity_returns(self, n_assets=10, n_periods=252):
        # Simulate equity returns using a multi-factor model
        factors = np.random.normal(0, 0.01, (n_periods, 3))
        betas = np.random.normal(1, 0.2, (n_assets, 3))
        returns = factors @ betas.T + np.random.normal(0, 0.02, (n_periods, n_assets))
        return pd.DataFrame(returns, columns=[f'Equity_{i+1}' for i in range(n_assets)])

    def generate_fixed_income(self, n_bonds=5, n_periods=252):
        # Simulate bond yields and returns
        base_yield = np.linspace(0.01, 0.05, n_bonds)
        yield_changes = np.random.normal(0, 0.001, (n_periods, n_bonds))
        yields = base_yield + np.cumsum(yield_changes, axis=0)
        return pd.DataFrame(yields, columns=[f'Bond_{i+1}' for i in range(n_bonds)])

    def generate_alternatives(self, n_assets=3, n_periods=252):
        # Simulate alternative asset returns (e.g., private equity, real estate)
        returns = np.random.normal(0.0005, 0.01, (n_periods, n_assets))
        return pd.DataFrame(returns, columns=[f'Alt_{i+1}' for i in range(n_assets)])

    def generate_macroeconomic(self, n_periods=252):
        # Simulate macroeconomic variables: GDP growth, inflation, interest rates
        gdp = np.cumsum(np.random.normal(0.002, 0.01, n_periods))
        inflation = np.cumsum(np.random.normal(0.001, 0.005, n_periods))
        rates = np.cumsum(np.random.normal(0.0005, 0.002, n_periods)) + 0.02
        return pd.DataFrame({
            'GDP_Growth': gdp,
            'Inflation': inflation,
            'Interest_Rate': rates
        }) 