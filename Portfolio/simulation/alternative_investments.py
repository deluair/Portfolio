import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class AlternativeInvestment:
    asset_id: str
    asset_type: str  # 'Private Equity', 'Real Estate', 'Hedge Fund'
    vintage_year: int
    lock_up_period: int  # in years
    management_fee: float
    performance_fee: float
    initial_commitment: float
    current_value: float = 0.0
    distributions: List[float] = None
    capital_calls: List[float] = None

class AlternativeInvestmentSimulator:
    def __init__(self):
        self.j_curve_params = {
            'Private Equity': {'depth': -0.15, 'recovery_time': 3, 'peak_return': 0.25},
            'Real Estate': {'depth': -0.05, 'recovery_time': 2, 'peak_return': 0.15},
            'Hedge Fund': {'depth': -0.02, 'recovery_time': 1, 'peak_return': 0.12}
        }
    
    def simulate_j_curve(self, asset_type: str, n_periods: int) -> pd.Series:
        """Simulate J-curve effect for alternative investments"""
        params = self.j_curve_params[asset_type]
        
        # Create J-curve pattern
        returns = np.zeros(n_periods)
        
        # Initial decline (negative returns)
        decline_periods = min(params['recovery_time'], n_periods // 3)
        for i in range(decline_periods):
            returns[i] = params['depth'] * (1 - i / decline_periods)
        
        # Recovery and growth phase
        for i in range(decline_periods, n_periods):
            time_factor = (i - decline_periods) / (n_periods - decline_periods)
            returns[i] = params['peak_return'] * time_factor
        
        return pd.Series(returns)
    
    def simulate_private_equity(self, vintage_year: int, commitment: float, 
                               n_periods: int = 10) -> Dict:
        """Simulate private equity investment with capital calls and distributions"""
        # Capital call schedule (typically 3-5 years)
        call_periods = min(5, n_periods // 2)
        capital_calls = []
        
        for i in range(call_periods):
            if i == 0:
                call = commitment * 0.3  # Initial call
            else:
                call = commitment * 0.2  # Subsequent calls
            capital_calls.append(call)
        
        # Add zero calls for remaining periods
        capital_calls.extend([0] * (n_periods - call_periods))
        
        # Simulate returns with J-curve
        returns = self.simulate_j_curve('Private Equity', n_periods)
        
        # Calculate NAV progression
        nav = [0]
        for i in range(n_periods):
            if i < len(capital_calls):
                nav.append(nav[-1] * (1 + returns[i]) + capital_calls[i])
            else:
                nav.append(nav[-1] * (1 + returns[i]))
        
        # Simulate distributions (typically start after year 3)
        distributions = [0] * n_periods
        for i in range(3, n_periods):
            if nav[i] > nav[i-1]:
                distributions[i] = nav[i] * 0.1  # 10% distribution rate
        
        return {
            'capital_calls': capital_calls,
            'distributions': distributions,
            'nav': nav[1:],  # Remove initial 0
            'returns': returns,
            'total_irr': self._calculate_irr(capital_calls, distributions + [nav[-1]])
        }
    
    def simulate_real_estate(self, vintage_year: int, initial_investment: float,
                           n_periods: int = 10) -> Dict:
        """Simulate real estate investment with rental income and appreciation"""
        # Base returns with J-curve
        base_returns = self.simulate_j_curve('Real Estate', n_periods)
        
        # Add rental income component
        rental_yield = 0.05  # 5% rental yield
        rental_income = [initial_investment * rental_yield] * n_periods
        
        # Property appreciation
        appreciation_returns = base_returns + rental_yield
        
        # Calculate NAV
        nav = [initial_investment]
        for i in range(n_periods):
            nav.append(nav[-1] * (1 + appreciation_returns[i]))
        
        # Simulate distributions (rental income)
        distributions = rental_income
        
        return {
            'nav': nav[1:],
            'rental_income': rental_income,
            'appreciation_returns': appreciation_returns,
            'total_irr': self._calculate_irr([initial_investment] + [0] * (n_periods-1), 
                                           distributions + [nav[-1]])
        }
    
    def simulate_hedge_fund(self, vintage_year: int, initial_investment: float,
                          n_periods: int = 10) -> Dict:
        """Simulate hedge fund investment with fees and lock-up"""
        # Generate returns with some correlation to market
        market_returns = np.random.normal(0.08, 0.15, n_periods)
        alpha = np.random.normal(0.02, 0.05, n_periods)  # Skill component
        beta = 0.3  # Low beta for hedge fund
        
        gross_returns = alpha + beta * market_returns
        
        # Apply fees
        management_fee = 0.02  # 2% management fee
        performance_fee = 0.20  # 20% performance fee
        hurdle_rate = 0.08  # 8% hurdle rate
        
        net_returns = []
        nav = [initial_investment]
        
        for i in range(n_periods):
            # Apply management fee
            gross_return = gross_returns[i]
            after_mgmt_fee = gross_return - management_fee
            
            # Apply performance fee if above hurdle
            if after_mgmt_fee > hurdle_rate:
                excess_return = after_mgmt_fee - hurdle_rate
                performance_fee_amount = excess_return * performance_fee
                net_return = after_mgmt_fee - performance_fee_amount
            else:
                net_return = after_mgmt_fee
            
            net_returns.append(net_return)
            nav.append(nav[-1] * (1 + net_return))
        
        return {
            'nav': nav[1:],
            'gross_returns': gross_returns,
            'net_returns': net_returns,
            'total_irr': self._calculate_irr([initial_investment] + [0] * (n_periods-1), 
                                           [0] * n_periods + [nav[-1]])
        }
    
    def _calculate_irr(self, cash_flows_in: List[float], 
                      cash_flows_out: List[float]) -> float:
        """Calculate Internal Rate of Return"""
        try:
            from scipy.optimize import newton
            
            def npv(rate):
                total = 0
                for i, (cf_in, cf_out) in enumerate(zip(cash_flows_in, cash_flows_out)):
                    if rate != -1:
                        total += (cf_out - cf_in) / ((1 + rate) ** i)
                    else:
                        total += (cf_out - cf_in)
                return total
            
            # Find rate where NPV = 0
            irr = newton(npv, 0.1)  # Start with 10% guess
            return irr
        except:
            return 0.0  # Return 0 if IRR calculation fails
    
    def calculate_liquidity_adjusted_returns(self, returns: pd.Series, 
                                           liquidity_score: float) -> pd.Series:
        """Adjust returns for liquidity constraints"""
        # Higher liquidity score = lower liquidity premium
        liquidity_premium = (1 - liquidity_score) * 0.02  # 0-2% premium
        
        # Apply liquidity premium to returns
        adjusted_returns = returns - liquidity_premium
        return adjusted_returns
    
    def simulate_portfolio_alternatives(self, portfolio_weights: Dict[str, float],
                                      alternative_investments: List[AlternativeInvestment],
                                      n_periods: int = 10) -> Dict:
        """Simulate a portfolio of alternative investments"""
        portfolio_nav = [0] * n_periods
        portfolio_returns = []
        
        for investment in alternative_investments:
            if investment.asset_type == 'Private Equity':
                sim_result = self.simulate_private_equity(
                    investment.vintage_year, 
                    investment.initial_commitment, 
                    n_periods
                )
            elif investment.asset_type == 'Real Estate':
                sim_result = self.simulate_real_estate(
                    investment.vintage_year,
                    investment.initial_commitment,
                    n_periods
                )
            elif investment.asset_type == 'Hedge Fund':
                sim_result = self.simulate_hedge_fund(
                    investment.vintage_year,
                    investment.initial_commitment,
                    n_periods
                )
            else:
                continue
            
            # Add to portfolio (assuming equal weight for simplicity)
            weight = portfolio_weights.get(investment.asset_id, 1.0 / len(alternative_investments))
            
            for i in range(n_periods):
                portfolio_nav[i] += sim_result['nav'][i] * weight
            
            if 'returns' in sim_result:
                portfolio_returns.append(sim_result['returns'] * weight)
        
        # Calculate portfolio returns
        if portfolio_returns:
            portfolio_returns = pd.concat(portfolio_returns, axis=1).sum(axis=1)
        else:
            portfolio_returns = pd.Series([0] * n_periods)
        
        return {
            'portfolio_nav': portfolio_nav,
            'portfolio_returns': portfolio_returns,
            'total_portfolio_value': portfolio_nav[-1] if portfolio_nav else 0
        } 