from data.synthetic_market_data import SyntheticMarketDataGenerator
from data.synthetic_client_data import SyntheticClientDataGenerator
from models.client import Client
from models.portfolio import Portfolio
from analytics.risk_analytics import RiskAnalytics
from analytics.portfolio_optimization import PortfolioOptimizer
from analytics.esg_analytics import ESGAnalytics
from simulation.behavioral_simulation import BehavioralSimulator
from simulation.alternative_investments import AlternativeInvestmentSimulator
from models.behavioral import BehavioralProfile
import pandas as pd
import numpy as np

class SimulationEngine:
    def __init__(self, n_clients=100, n_periods=252):
        self.n_clients = n_clients
        self.n_periods = n_periods
        self.market_data_gen = SyntheticMarketDataGenerator()
        self.client_data_gen = SyntheticClientDataGenerator(n_clients=n_clients)
        self.risk_analytics = RiskAnalytics()
        self.portfolio_optimizer = PortfolioOptimizer()
        self.esg_analytics = ESGAnalytics()
        self.behavioral_simulator = BehavioralSimulator()
        self.alternative_simulator = AlternativeInvestmentSimulator()
        self.clients = []
        self.market_data = {}
        self.portfolio_history = []
        self.risk_metrics = []
        self.esg_scores = []
        self.behavioral_impacts = []

    def setup(self):
        # Generate synthetic clients
        demographics = self.client_data_gen.generate_demographics()
        risk = self.client_data_gen.generate_risk_tolerance()
        goals = self.client_data_gen.generate_goal_hierarchies()
        behaviors = self.client_data_gen.generate_behavioral_patterns()
        
        for i, row in demographics.iterrows():
            client_goals = goals[goals['client_id'] == i].to_dict('records')
            client_biases = behaviors[behaviors['client_id'] == i]['bias'].tolist()
            
            # Create a new behavioral profile for each client
            behavioral_profile = BehavioralProfile()
            for bias in client_biases:
                behavioral_profile.update_bias(bias, np.random.uniform(0.3, 0.8))
            
            client = Client(
                client_id=i,
                name=row['name'],
                age=row['age'],
                income=row['income'],
                wealth=row['wealth'],
                family_size=row['family_size'],
                sex=row['sex'],
                address=row['address'],
                risk_tolerance=int(risk.iloc[i]['risk_tolerance']),
                goals=client_goals,
                behavioral_profile=behavioral_profile
            )
            self.clients.append(client)

    def generate_market_data(self):
        self.market_data['equities'] = self.market_data_gen.generate_equity_returns()
        self.market_data['bonds'] = self.market_data_gen.generate_fixed_income()
        self.market_data['alternatives'] = self.market_data_gen.generate_alternatives()
        self.market_data['macro'] = self.market_data_gen.generate_macroeconomic()

    def initial_allocation(self, risk_tolerance):
        # Simple rule: higher risk_tolerance = more equities, less bonds
        eq = min(0.2 + 0.06 * risk_tolerance, 0.9)
        bonds = max(0.7 - 0.05 * risk_tolerance, 0.05)
        alts = 1.0 - eq - bonds
        return {'equities': eq, 'bonds': bonds, 'alternatives': alts}

    def assign_initial_portfolios(self):
        eq_names = self.market_data['equities'].columns.tolist()
        bond_names = self.market_data['bonds'].columns.tolist()
        alt_names = self.market_data['alternatives'].columns.tolist()
        
        for client in self.clients:
            alloc = self.initial_allocation(client.risk_tolerance)
            wealth = client.wealth
            eq_amt = alloc['equities'] * wealth / len(eq_names)
            bond_amt = alloc['bonds'] * wealth / len(bond_names)
            alt_amt = alloc['alternatives'] * wealth / len(alt_names)
            holdings = {name: eq_amt for name in eq_names}
            holdings.update({name: bond_amt for name in bond_names})
            holdings.update({name: alt_amt for name in alt_names})
            client.portfolio = Portfolio(holdings=holdings)

    def optimize_portfolios(self):
        """Apply portfolio optimization to each client"""
        all_returns = pd.concat([
            self.market_data['equities'],
            self.market_data['bonds'],
            self.market_data['alternatives']
        ], axis=1)
        
        for client in self.clients:
            # Optimize based on risk tolerance
            if client.risk_tolerance >= 7:
                # High risk tolerance: maximize Sharpe ratio
                result = self.portfolio_optimizer.optimize_sharpe_ratio(all_returns)
            elif client.risk_tolerance >= 4:
                # Medium risk tolerance: risk parity
                result = self.portfolio_optimizer.risk_parity_optimization(all_returns)
            else:
                # Low risk tolerance: minimum variance
                result = self.portfolio_optimizer.minimum_variance_optimization(all_returns)
            
            if result['success']:
                # Update portfolio with optimized weights
                optimized_weights = result['weights']
                total_value = client.portfolio.total_value({col: 1 for col in all_returns.columns})
                
                new_holdings = {}
                for i, asset in enumerate(all_returns.columns):
                    new_holdings[asset] = optimized_weights[i] * total_value
                
                client.portfolio.holdings = new_holdings

    def calculate_risk_metrics(self):
        """Calculate risk metrics for all portfolios"""
        all_returns = pd.concat([
            self.market_data['equities'],
            self.market_data['bonds'],
            self.market_data['alternatives']
        ], axis=1)
        
        for client in self.clients:
            # Calculate portfolio returns
            portfolio_returns = pd.Series(0.0, index=all_returns.index)
            for asset, amount in client.portfolio.holdings.items():
                if asset in all_returns.columns:
                    portfolio_returns += all_returns[asset] * amount / client.portfolio.total_value({col: 1 for col in all_returns.columns})
            
            # Calculate risk metrics
            var_95 = self.risk_analytics.historical_var(portfolio_returns, 0.95)
            cvar_95 = self.risk_analytics.conditional_var(portfolio_returns, 0.95)
            volatility = portfolio_returns.std() * np.sqrt(252)
            
            # Update client's risk profile
            client.portfolio.update_risk_profile(
                var=var_95,
                cvar=cvar_95,
                volatility=volatility
            )
            
            self.risk_metrics.append({
                'client_id': client.client_id,
                'var_95': var_95,
                'cvar_95': cvar_95,
                'volatility': volatility
            })

    def calculate_esg_scores(self):
        """Calculate ESG scores for all portfolios"""
        all_assets = list(self.market_data['equities'].columns) + \
                    list(self.market_data['bonds'].columns) + \
                    list(self.market_data['alternatives'].columns)
        
        # Generate ESG scores for all assets
        asset_esg_scores = {}
        for asset in all_assets:
            asset_esg_scores[asset] = self.esg_analytics.calculate_asset_esg_score({})
        
        for client in self.clients:
            # Calculate portfolio ESG score
            portfolio_weights = client.portfolio.allocation({col: 1 for col in all_assets})
            portfolio_esg = self.esg_analytics.calculate_portfolio_esg_score(portfolio_weights, asset_esg_scores)
            
            # Update client's ESG profile
            client.portfolio.update_esg_profile(
                environmental=portfolio_esg.environmental,
                social=portfolio_esg.social,
                governance=portfolio_esg.governance
            )
            
            self.esg_scores.append({
                'client_id': client.client_id,
                'esg_score': portfolio_esg.overall,
                'environmental': portfolio_esg.environmental,
                'social': portfolio_esg.social,
                'governance': portfolio_esg.governance
            })

    def simulate_behavioral_effects(self):
        """Simulate behavioral effects on portfolio performance"""
        market_returns = self.market_data['equities'].mean(axis=1)  # Use equity market as proxy
        
        for client in self.clients:
            # Calculate portfolio returns
            all_returns = pd.concat([
                self.market_data['equities'],
                self.market_data['bonds'],
                self.market_data['alternatives']
            ], axis=1)
            
            portfolio_returns = pd.Series(0.0, index=all_returns.index)
            for asset, amount in client.portfolio.holdings.items():
                if asset in all_returns.columns:
                    portfolio_returns += all_returns[asset] * amount / client.portfolio.total_value({col: 1 for col in all_returns.columns})
            
            # Simulate behavioral effects
            behavioral_result = self.behavioral_simulator.simulate_behavioral_trading(
                client.behavioral_profile,
                portfolio_returns,
                market_returns,
                all_returns
            )
            
            self.behavioral_impacts.append({
                'client_id': client.client_id,
                'behavioral_impact': behavioral_result['behavioral_impact'].sum(),
                'trading_decisions': behavioral_result['trading_decisions']
            })

    def simulate(self):
        eq = self.market_data['equities']
        bonds = self.market_data['bonds']
        alts = self.market_data['alternatives']
        asset_prices = pd.concat([
            (1 + eq).cumprod(),
            (1 + bonds).cumprod(),
            (1 + alts).cumprod()
        ], axis=1)
        
        for client in self.clients:
            values = []
            for t in range(self.n_periods):
                prices = asset_prices.iloc[t].to_dict()
                values.append(client.portfolio.total_value(prices))
            self.portfolio_history.append(pd.Series(values, name=f'Client_{client.client_id}'))

    def run(self):
        print("Setting up simulation...")
        self.setup()
        
        print("Generating market data...")
        self.generate_market_data()
        
        print("Assigning initial portfolios...")
        self.assign_initial_portfolios()
        
        print("Optimizing portfolios...")
        self.optimize_portfolios()
        
        print("Calculating risk metrics...")
        self.calculate_risk_metrics()
        
        print("Calculating ESG scores...")
        self.calculate_esg_scores()
        
        print("Simulating behavioral effects...")
        self.simulate_behavioral_effects()
        
        print("Running simulation...")
        self.simulate()
        
        print(f"Simulation complete! Initialized {len(self.clients)} clients.")
        self.print_summary()

    def print_summary(self):
        """Print comprehensive simulation summary"""
        print("\n" + "="*60)
        print("SIMULATION SUMMARY")
        print("="*60)
        
        # Portfolio performance
        final_values = [hist.iloc[-1] for hist in self.portfolio_history]
        avg_final_value = np.mean(final_values)
        print(f"Average final portfolio value: ${avg_final_value:,.2f}")
        
        # Risk metrics
        avg_var = np.mean([rm['var_95'] for rm in self.risk_metrics])
        avg_vol = np.mean([rm['volatility'] for rm in self.risk_metrics])
        print(f"Average VaR (95%): {avg_var:.2%}")
        print(f"Average volatility: {avg_vol:.2%}")
        
        # ESG scores
        avg_esg = np.mean([esg['esg_score'] for esg in self.esg_scores])
        print(f"Average ESG score: {avg_esg:.1f}")
        
        # Behavioral impact
        avg_behavioral_impact = np.mean([bi['behavioral_impact'] for bi in self.behavioral_impacts])
        print(f"Average behavioral impact: {avg_behavioral_impact:.2%}")
        
        print("="*60) 