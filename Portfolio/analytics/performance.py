import numpy as np
import pandas as pd

class PerformanceAnalyzer:
    @staticmethod
    def total_return(returns):
        # returns: pd.Series or np.array of periodic returns
        return np.prod(1 + returns) - 1

    @staticmethod
    def volatility(returns):
        return np.std(returns) * np.sqrt(len(returns))

    @staticmethod
    def sharpe_ratio(returns, risk_free_rate=0.0):
        excess = returns - risk_free_rate / len(returns)
        return np.mean(excess) / np.std(excess)

    @staticmethod
    def max_drawdown(returns):
        cumulative = (1 + returns).cumprod()
        peak = cumulative.cummax()
        drawdown = (cumulative - peak) / peak
        return drawdown.min() 