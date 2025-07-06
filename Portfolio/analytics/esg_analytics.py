import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from models.esg import ESGProfile

class ESGAnalytics:
    def __init__(self):
        self.esg_weights = {
            'environmental': 0.4,
            'social': 0.3,
            'governance': 0.3
        }
    
    def calculate_asset_esg_score(self, asset_data: Dict) -> ESGProfile:
        """Calculate ESG score for an individual asset"""
        # This would typically use external ESG data providers
        # For simulation, generate synthetic ESG scores
        
        # Environmental factors (0-100 scale)
        carbon_footprint = np.random.uniform(0, 100)
        energy_efficiency = np.random.uniform(0, 100)
        waste_management = np.random.uniform(0, 100)
        environmental_score = (carbon_footprint + energy_efficiency + waste_management) / 3
        
        # Social factors
        labor_practices = np.random.uniform(0, 100)
        community_impact = np.random.uniform(0, 100)
        human_rights = np.random.uniform(0, 100)
        social_score = (labor_practices + community_impact + human_rights) / 3
        
        # Governance factors
        board_independence = np.random.uniform(0, 100)
        executive_compensation = np.random.uniform(0, 100)
        transparency = np.random.uniform(0, 100)
        governance_score = (board_independence + executive_compensation + transparency) / 3
        
        # Create ESG profile
        esg_profile = ESGProfile(
            environmental=environmental_score,
            social=social_score,
            governance=governance_score
        )
        esg_profile.update()  # Calculate overall score
        
        return esg_profile
    
    def calculate_portfolio_esg_score(self, portfolio_weights: Dict[str, float], 
                                    asset_esg_scores: Dict[str, ESGProfile]) -> ESGProfile:
        """Calculate weighted ESG score for a portfolio"""
        env_score = 0
        soc_score = 0
        gov_score = 0
        total_weight = 0
        
        for asset, weight in portfolio_weights.items():
            if asset in asset_esg_scores:
                esg_profile = asset_esg_scores[asset]
                env_score += esg_profile.environmental * weight
                soc_score += esg_profile.social * weight
                gov_score += esg_profile.governance * weight
                total_weight += weight
        
        if total_weight > 0:
            env_score /= total_weight
            soc_score /= total_weight
            gov_score /= total_weight
        
        portfolio_esg = ESGProfile(
            environmental=env_score,
            social=soc_score,
            governance=gov_score
        )
        portfolio_esg.update()
        
        return portfolio_esg
    
    def esg_screening(self, assets: List[str], asset_esg_scores: Dict[str, ESGProfile],
                     screening_criteria: Dict) -> List[str]:
        """Apply ESG screening criteria to filter assets"""
        screened_assets = []
        
        for asset in assets:
            if asset in asset_esg_scores:
                esg_profile = asset_esg_scores[asset]
                
                # Check if asset meets all screening criteria
                passes_screening = True
                
                if 'min_overall_score' in screening_criteria:
                    if esg_profile.overall < screening_criteria['min_overall_score']:
                        passes_screening = False
                
                if 'min_environmental_score' in screening_criteria:
                    if esg_profile.environmental < screening_criteria['min_environmental_score']:
                        passes_screening = False
                
                if 'min_social_score' in screening_criteria:
                    if esg_profile.social < screening_criteria['min_social_score']:
                        passes_screening = False
                
                if 'min_governance_score' in screening_criteria:
                    if esg_profile.governance < screening_criteria['min_governance_score']:
                        passes_screening = False
                
                if passes_screening:
                    screened_assets.append(asset)
        
        return screened_assets
    
    def calculate_esg_impact(self, portfolio_weights: Dict[str, float],
                           asset_esg_scores: Dict[str, ESGProfile],
                           impact_metrics: Dict[str, float]) -> Dict[str, float]:
        """Calculate ESG impact metrics for a portfolio"""
        impact_results = {}
        
        # Carbon footprint impact
        if 'carbon_footprint' in impact_metrics:
            total_carbon = 0
            for asset, weight in portfolio_weights.items():
                if asset in asset_esg_scores:
                    # Assume carbon footprint is inversely related to environmental score
                    carbon_intensity = 100 - asset_esg_scores[asset].environmental
                    total_carbon += carbon_intensity * weight
            impact_results['carbon_footprint'] = total_carbon
        
        # Social impact
        if 'social_impact' in impact_metrics:
            total_social_impact = 0
            for asset, weight in portfolio_weights.items():
                if asset in asset_esg_scores:
                    total_social_impact += asset_esg_scores[asset].social * weight
            impact_results['social_impact'] = total_social_impact
        
        # Governance quality
        if 'governance_quality' in impact_metrics:
            total_governance = 0
            for asset, weight in portfolio_weights.items():
                if asset in asset_esg_scores:
                    total_governance += asset_esg_scores[asset].governance * weight
            impact_results['governance_quality'] = total_governance
        
        return impact_results
    
    def esg_optimization(self, returns: pd.DataFrame, 
                        asset_esg_scores: Dict[str, ESGProfile],
                        target_esg_score: float = 70.0,
                        esg_constraint_weight: float = 0.3) -> Dict:
        """Optimize portfolio considering both returns and ESG scores"""
        from scipy.optimize import minimize
        
        mean_returns = returns.mean()
        cov_matrix = returns.cov()
        
        def objective(weights):
            # Combine return optimization with ESG constraint
            portfolio_return = np.sum(mean_returns * weights)
            portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            
            # Calculate portfolio ESG score
            portfolio_weights = {returns.columns[i]: weights[i] for i in range(len(weights))}
            portfolio_esg = self.calculate_portfolio_esg_score(portfolio_weights, asset_esg_scores)
            
            # Penalty for ESG deviation from target
            esg_penalty = abs(portfolio_esg.overall - target_esg_score) * esg_constraint_weight
            
            # Maximize Sharpe ratio while considering ESG
            sharpe = (portfolio_return - 0.02) / portfolio_vol  # Assuming 2% risk-free rate
            return -(sharpe - esg_penalty)
        
        # Constraints
        n_assets = len(returns.columns)
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # weights sum to 1
        ]
        
        bounds = tuple((0, 1) for _ in range(n_assets))
        initial_weights = np.array([1/n_assets] * n_assets)
        
        result = minimize(objective, initial_weights,
                        method='SLSQP', bounds=bounds, constraints=constraints)
        
        if result.success:
            optimal_weights = result.x
            portfolio_weights = {returns.columns[i]: optimal_weights[i] for i in range(len(optimal_weights))}
            portfolio_esg = self.calculate_portfolio_esg_score(portfolio_weights, asset_esg_scores)
            
            return {
                'weights': optimal_weights,
                'esg_score': portfolio_esg.overall,
                'success': True
            }
        else:
            return {'success': False, 'message': result.message}
    
    def generate_esg_report(self, portfolio_weights: Dict[str, float],
                          asset_esg_scores: Dict[str, ESGProfile]) -> Dict:
        """Generate comprehensive ESG report for a portfolio"""
        portfolio_esg = self.calculate_portfolio_esg_score(portfolio_weights, asset_esg_scores)
        
        # Calculate ESG distribution
        esg_distribution = {
            'high_esg': 0,  # >80
            'medium_esg': 0,  # 60-80
            'low_esg': 0   # <60
        }
        
        for asset, weight in portfolio_weights.items():
            if asset in asset_esg_scores:
                score = asset_esg_scores[asset].overall
                if score > 80:
                    esg_distribution['high_esg'] += weight
                elif score > 60:
                    esg_distribution['medium_esg'] += weight
                else:
                    esg_distribution['low_esg'] += weight
        
        return {
            'portfolio_esg_score': portfolio_esg.overall,
            'environmental_score': portfolio_esg.environmental,
            'social_score': portfolio_esg.social,
            'governance_score': portfolio_esg.governance,
            'esg_distribution': esg_distribution,
            'esg_rating': self._get_esg_rating(portfolio_esg.overall)
        }
    
    def _get_esg_rating(self, score: float) -> str:
        """Convert ESG score to rating"""
        if score >= 80:
            return 'AAA'
        elif score >= 70:
            return 'AA'
        elif score >= 60:
            return 'A'
        elif score >= 50:
            return 'BBB'
        elif score >= 40:
            return 'BB'
        else:
            return 'B' 