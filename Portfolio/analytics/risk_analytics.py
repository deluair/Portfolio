import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple

class RiskAnalytics:
    def __init__(self, confidence_level=0.95):
        self.confidence_level = confidence_level
        
    def historical_var(self, returns: pd.Series, confidence_level=None) -> float:
        """Calculate historical Value at Risk"""
        if confidence_level is None:
            confidence_level = self.confidence_level
        return np.percentile(returns, (1 - confidence_level) * 100)
    
    def monte_carlo_var(self, returns: pd.Series, n_simulations=10000, 
                       confidence_level=None) -> float:
        """Calculate Monte Carlo VaR using normal distribution assumption"""
        if confidence_level is None:
            confidence_level = self.confidence_level
        
        mean_return = returns.mean()
        std_return = returns.std()
        
        # Generate random returns
        simulated_returns = np.random.normal(mean_return, std_return, n_simulations)
        return np.percentile(simulated_returns, (1 - confidence_level) * 100)
    
    def conditional_var(self, returns: pd.Series, confidence_level=None) -> float:
        """Calculate Conditional Value at Risk (Expected Shortfall)"""
        if confidence_level is None:
            confidence_level = self.confidence_level
        
        var_threshold = self.historical_var(returns, confidence_level)
        tail_returns = returns[returns <= var_threshold]
        return tail_returns.mean()
    
    def stress_test(self, portfolio_returns: pd.Series, 
                   stress_scenarios: Dict[str, float]) -> Dict[str, float]:
        """Perform stress testing with different scenarios"""
        results = {}
        base_value = 1000  # Base portfolio value
        
        for scenario_name, stress_factor in stress_scenarios.items():
            stressed_returns = portfolio_returns * stress_factor
            stressed_value = base_value * (1 + stressed_returns.sum())
            loss = base_value - stressed_value
            results[scenario_name] = loss
            
        return results
    
    def factor_analysis(self, asset_returns: pd.DataFrame, 
                       factor_returns: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Perform factor analysis to decompose asset returns"""
        # Simple linear regression for each asset against factors
        betas = {}
        alphas = {}
        r_squared = {}
        
        for asset in asset_returns.columns:
            # Prepare data
            y = asset_returns[asset].dropna()
            X = factor_returns.loc[y.index].dropna()
            
            if len(y) > 0 and len(X) > 0:
                # Align data
                common_index = y.index.intersection(X.index)
                y = y.loc[common_index]
                X = X.loc[common_index]
                
                if len(common_index) > 0:
                    # Add constant for alpha
                    X_with_const = pd.concat([pd.Series(1, index=X.index), X], axis=1)
                    
                    # Linear regression
                    try:
                        coeffs = np.linalg.lstsq(X_with_const, y, rcond=None)[0]
                        alpha = coeffs[0]
                        beta = coeffs[1:]
                        
                        # Calculate R-squared
                        y_pred = X_with_const @ coeffs
                        ss_res = np.sum((y - y_pred) ** 2)
                        ss_tot = np.sum((y - y.mean()) ** 2)
                        r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
                        
                        betas[asset] = beta
                        alphas[asset] = alpha
                        r_squared[asset] = r2
                    except:
                        continue
        
        return {
            'betas': betas,
            'alphas': alphas,
            'r_squared': r_squared
        }
    
    def correlation_analysis(self, returns: pd.DataFrame, 
                           rolling_window=60) -> pd.DataFrame:
        """Calculate rolling correlations between assets"""
        return returns.rolling(window=rolling_window).corr()
    
    def volatility_forecasting(self, returns: pd.Series, 
                             model='ewma', lambda_param=0.94) -> pd.Series:
        """Forecast volatility using different models"""
        if model == 'ewma':
            # Exponentially Weighted Moving Average
            weights = np.array([(1 - lambda_param) * lambda_param**i 
                              for i in range(len(returns))])
            weights = weights / weights.sum()
            
            # Calculate weighted variance
            mean_return = returns.mean()
            squared_returns = (returns - mean_return) ** 2
            forecasted_variance = np.convolve(squared_returns, weights, mode='valid')
            return np.sqrt(forecasted_variance)
        
        elif model == 'garch':
            # Simple GARCH(1,1) implementation
            omega = 0.000001
            alpha = 0.1
            beta = 0.8
            
            variance = np.zeros(len(returns))
            variance[0] = returns.var()
            
            for t in range(1, len(returns)):
                variance[t] = omega + alpha * returns.iloc[t-1]**2 + beta * variance[t-1]
            
            return np.sqrt(variance)
        
        return pd.Series(np.nan, index=returns.index) 