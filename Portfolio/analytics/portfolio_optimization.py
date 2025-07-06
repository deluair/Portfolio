import numpy as np
import pandas as pd
from scipy.optimize import minimize
from typing import Dict, List, Tuple, Optional

class PortfolioOptimizer:
    def __init__(self, risk_free_rate=0.02):
        self.risk_free_rate = risk_free_rate
    
    def calculate_efficient_frontier(self, returns: pd.DataFrame, 
                                   n_portfolios=100) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Calculate efficient frontier using mean-variance optimization"""
        mean_returns = returns.mean()
        cov_matrix = returns.cov()
        
        # Generate random portfolios
        portfolio_returns = []
        portfolio_volatilities = []
        portfolio_weights = []
        
        for _ in range(n_portfolios):
            weights = np.random.random(len(returns.columns))
            weights = weights / np.sum(weights)
            
            portfolio_return = np.sum(mean_returns * weights)
            portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            
            portfolio_returns.append(portfolio_return)
            portfolio_volatilities.append(portfolio_vol)
            portfolio_weights.append(weights)
        
        return np.array(portfolio_returns), np.array(portfolio_volatilities), np.array(portfolio_weights)
    
    def optimize_sharpe_ratio(self, returns: pd.DataFrame, 
                             constraints: Optional[Dict] = None) -> Dict:
        """Optimize portfolio for maximum Sharpe ratio"""
        mean_returns = returns.mean()
        cov_matrix = returns.cov()
        
        def negative_sharpe(weights):
            portfolio_return = np.sum(mean_returns * weights)
            portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            sharpe = (portfolio_return - self.risk_free_rate) / portfolio_vol
            return -sharpe
        
        # Constraints
        n_assets = len(returns.columns)
        
        # Default constraints
        if constraints is None:
            constraints = [
                {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # weights sum to 1
            ]
        
        # Bounds: 0 <= weight <= 1 for each asset
        bounds = tuple((0, 1) for _ in range(n_assets))
        
        # Initial guess: equal weights
        initial_weights = np.array([1/n_assets] * n_assets)
        
        # Optimize
        result = minimize(negative_sharpe, initial_weights, 
                        method='SLSQP', bounds=bounds, constraints=constraints)
        
        if result.success:
            optimal_weights = result.x
            optimal_return = np.sum(mean_returns * optimal_weights)
            optimal_vol = np.sqrt(np.dot(optimal_weights.T, np.dot(cov_matrix, optimal_weights)))
            optimal_sharpe = (optimal_return - self.risk_free_rate) / optimal_vol
            
            return {
                'weights': optimal_weights,
                'expected_return': optimal_return,
                'volatility': optimal_vol,
                'sharpe_ratio': optimal_sharpe,
                'success': True
            }
        else:
            return {'success': False, 'message': result.message}
    
    def black_litterman_optimization(self, returns: pd.DataFrame, 
                                   market_caps: pd.Series,
                                   views: Dict[str, float],
                                   confidence: Dict[str, float],
                                   tau=0.05) -> Dict:
        """Black-Litterman optimization with investor views"""
        # Calculate market equilibrium returns
        cov_matrix = returns.cov()
        market_weights = market_caps / market_caps.sum()
        
        # Market equilibrium returns (reverse optimization)
        risk_aversion = 3.0  # Typical value
        pi = risk_aversion * np.dot(cov_matrix, market_weights)
        
        # Create view matrix P and view vector Q
        assets = returns.columns.tolist()
        n_assets = len(assets)
        n_views = len(views)
        
        P = np.zeros((n_views, n_assets))
        Q = np.zeros(n_views)
        Omega = np.zeros((n_views, n_views))
        
        for i, (view_asset, view_return) in enumerate(views.items()):
            if view_asset in assets:
                asset_idx = assets.index(view_asset)
                P[i, asset_idx] = 1
                Q[i] = view_return
                Omega[i, i] = 1 / confidence[view_asset]
        
        # Black-Litterman formula
        tau_cov = tau * cov_matrix
        M1 = np.linalg.inv(tau_cov)
        M2 = np.dot(P.T, np.dot(np.linalg.inv(Omega), P))
        M3 = np.dot(P.T, np.dot(np.linalg.inv(Omega), Q))
        
        mu_bl = np.linalg.inv(M1 + M2) @ (np.dot(M1, pi) + M3)
        sigma_bl = np.linalg.inv(M1 + M2)
        
        # Optimize with Black-Litterman expected returns
        mean_returns_bl = pd.Series(mu_bl, index=assets)
        
        return self.optimize_sharpe_ratio(returns, constraints=None)
    
    def risk_parity_optimization(self, returns: pd.DataFrame) -> Dict:
        """Risk parity optimization - equal risk contribution"""
        cov_matrix = returns.cov()
        
        def risk_contribution(weights):
            portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            marginal_risk = np.dot(cov_matrix, weights) / portfolio_vol
            risk_contrib = weights * marginal_risk
            return risk_contrib
        
        def risk_parity_objective(weights):
            risk_contrib = risk_contribution(weights)
            target_risk = 1.0 / len(weights)  # Equal risk contribution
            return np.sum((risk_contrib - target_risk) ** 2)
        
        # Constraints
        n_assets = len(returns.columns)
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # weights sum to 1
        ]
        
        bounds = tuple((0, 1) for _ in range(n_assets))
        initial_weights = np.array([1/n_assets] * n_assets)
        
        result = minimize(risk_parity_objective, initial_weights,
                        method='SLSQP', bounds=bounds, constraints=constraints)
        
        if result.success:
            optimal_weights = result.x
            portfolio_vol = np.sqrt(np.dot(optimal_weights.T, np.dot(cov_matrix, optimal_weights)))
            mean_returns = returns.mean()
            portfolio_return = np.sum(mean_returns * optimal_weights)
            
            return {
                'weights': optimal_weights,
                'expected_return': portfolio_return,
                'volatility': portfolio_vol,
                'risk_contributions': risk_contribution(optimal_weights),
                'success': True
            }
        else:
            return {'success': False, 'message': result.message}
    
    def minimum_variance_optimization(self, returns: pd.DataFrame) -> Dict:
        """Minimum variance portfolio optimization"""
        cov_matrix = returns.cov()
        
        def portfolio_variance(weights):
            return np.dot(weights.T, np.dot(cov_matrix, weights))
        
        n_assets = len(returns.columns)
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
        ]
        
        bounds = tuple((0, 1) for _ in range(n_assets))
        initial_weights = np.array([1/n_assets] * n_assets)
        
        result = minimize(portfolio_variance, initial_weights,
                        method='SLSQP', bounds=bounds, constraints=constraints)
        
        if result.success:
            optimal_weights = result.x
            portfolio_vol = np.sqrt(portfolio_variance(optimal_weights))
            mean_returns = returns.mean()
            portfolio_return = np.sum(mean_returns * optimal_weights)
            
            return {
                'weights': optimal_weights,
                'expected_return': portfolio_return,
                'volatility': portfolio_vol,
                'success': True
            }
        else:
            return {'success': False, 'message': result.message} 