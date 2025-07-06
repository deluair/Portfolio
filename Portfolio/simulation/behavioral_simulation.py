import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from models.behavioral import BehavioralProfile

class BehavioralSimulator:
    def __init__(self):
        self.bias_effects = {
            'Loss Aversion': self._loss_aversion_effect,
            'Recency Bias': self._recency_bias_effect,
            'Herding': self._herding_effect,
            'Anchoring': self._anchoring_effect,
            'Confirmation': self._confirmation_bias_effect
        }
    
    def _loss_aversion_effect(self, returns: pd.Series, bias_strength: float) -> pd.Series:
        """Loss aversion: investors feel losses more acutely than gains"""
        # Amplify negative returns based on bias strength
        adjusted_returns = returns.copy()
        negative_mask = returns < 0
        adjusted_returns[negative_mask] = returns[negative_mask] * (1 + bias_strength)
        return adjusted_returns
    
    def _recency_bias_effect(self, returns: pd.Series, bias_strength: float, 
                           lookback_period: int = 20) -> pd.Series:
        """Recency bias: overweight recent performance"""
        # Calculate recent performance and adjust current returns
        recent_performance = returns.rolling(window=lookback_period).mean()
        # Amplify returns based on recent performance
        adjusted_returns = returns + (recent_performance * bias_strength)
        return adjusted_returns
    
    def _herding_effect(self, returns: pd.Series, bias_strength: float, 
                       market_returns: pd.Series) -> pd.Series:
        """Herding: follow market sentiment"""
        # Adjust returns based on market performance
        market_sentiment = market_returns.rolling(window=10).mean()
        adjusted_returns = returns + (market_sentiment * bias_strength)
        return adjusted_returns
    
    def _anchoring_effect(self, returns: pd.Series, bias_strength: float, 
                         anchor_price: float, current_price: float) -> pd.Series:
        """Anchoring: over-rely on initial information"""
        # Adjust returns based on deviation from anchor
        price_ratio = current_price / anchor_price
        anchor_adjustment = (price_ratio - 1) * bias_strength
        adjusted_returns = returns + anchor_adjustment
        return adjusted_returns
    
    def _confirmation_bias_effect(self, returns: pd.Series, bias_strength: float, 
                                 beliefs: pd.Series) -> pd.Series:
        """Confirmation bias: seek information confirming existing beliefs"""
        # Amplify returns that align with beliefs
        belief_alignment = returns * beliefs
        adjusted_returns = returns + (belief_alignment * bias_strength)
        return adjusted_returns
    
    def simulate_behavioral_trading(self, client_behavior: BehavioralProfile,
                                  portfolio_returns: pd.Series,
                                  market_returns: pd.Series,
                                  asset_prices: pd.DataFrame) -> Dict:
        """Simulate trading decisions influenced by behavioral biases"""
        trading_decisions = []
        adjusted_returns = portfolio_returns.copy()
        
        for bias, strength in client_behavior.biases.items():
            if bias in self.bias_effects:
                if bias == 'Loss Aversion':
                    adjusted_returns = self.bias_effects[bias](adjusted_returns, strength)
                elif bias == 'Recency Bias':
                    adjusted_returns = self.bias_effects[bias](adjusted_returns, strength)
                elif bias == 'Herding':
                    adjusted_returns = self.bias_effects[bias](adjusted_returns, strength, market_returns)
                elif bias == 'Anchoring':
                    # Use first price as anchor
                    anchor_price = asset_prices.iloc[0].mean()
                    current_price = asset_prices.iloc[-1].mean()
                    adjusted_returns = self.bias_effects[bias](adjusted_returns, strength, anchor_price, current_price)
                elif bias == 'Confirmation':
                    # Assume positive beliefs for simplicity
                    beliefs = pd.Series(1, index=adjusted_returns.index)
                    adjusted_returns = self.bias_effects[bias](adjusted_returns, strength, beliefs)
                
                # Record trading decision based on bias
                decision = self._generate_trading_decision(bias, strength, adjusted_returns)
                trading_decisions.append(decision)
        
        return {
            'adjusted_returns': adjusted_returns,
            'trading_decisions': trading_decisions,
            'behavioral_impact': adjusted_returns - portfolio_returns
        }
    
    def _generate_trading_decision(self, bias: str, strength: float, 
                                 returns: pd.Series) -> Dict:
        """Generate trading decision based on bias and recent performance"""
        recent_return = returns.tail(5).mean()
        
        if bias == 'Loss Aversion':
            if recent_return < -0.02:  # Significant loss
                action = 'sell' if strength > 0.5 else 'hold'
            else:
                action = 'buy' if recent_return > 0.02 else 'hold'
        
        elif bias == 'Recency Bias':
            if recent_return > 0.01:
                action = 'buy'
            elif recent_return < -0.01:
                action = 'sell'
            else:
                action = 'hold'
        
        elif bias == 'Herding':
            # Follow market trend
            action = 'buy' if recent_return > 0 else 'sell'
        
        else:
            action = 'hold'
        
        return {
            'bias': bias,
            'strength': strength,
            'recent_performance': recent_return,
            'action': action,
            'confidence': strength
        }
    
    def calculate_behavioral_penalty(self, behavioral_impact: pd.Series) -> float:
        """Calculate performance penalty due to behavioral biases"""
        # Simple penalty based on cumulative behavioral impact
        cumulative_impact = behavioral_impact.sum()
        return abs(cumulative_impact) * 0.1  # 10% penalty on behavioral impact
    
    def simulate_market_sentiment(self, returns: pd.Series, 
                                sentiment_periods: List[int] = [20, 60, 252]) -> Dict:
        """Simulate market sentiment using multiple timeframes"""
        sentiment = {}
        
        for period in sentiment_periods:
            # Calculate sentiment based on rolling performance
            rolling_return = returns.rolling(window=period).mean()
            rolling_vol = returns.rolling(window=period).std()
            
            # Sentiment score: positive if return > volatility
            sentiment[f'{period}d'] = (rolling_return > rolling_vol).astype(int)
        
        return sentiment
    
    def simulate_herd_behavior(self, individual_decisions: List[Dict], 
                              market_returns: pd.Series) -> pd.Series:
        """Simulate how individual decisions aggregate into market behavior"""
        # Aggregate individual decisions
        buy_signals = []
        sell_signals = []
        
        for decision in individual_decisions:
            if decision['action'] == 'buy':
                buy_signals.append(decision['confidence'])
            elif decision['action'] == 'sell':
                sell_signals.append(decision['confidence'])
        
        # Calculate net sentiment
        net_buying = sum(buy_signals) - sum(sell_signals)
        
        # Adjust market returns based on herd behavior
        herd_adjustment = net_buying * 0.001  # Small adjustment factor
        adjusted_market_returns = market_returns + herd_adjustment
        
        return adjusted_market_returns 