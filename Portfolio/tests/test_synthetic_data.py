import pytest
from data.synthetic_market_data import SyntheticMarketDataGenerator
from data.synthetic_client_data import SyntheticClientDataGenerator

def test_market_data_shapes():
    gen = SyntheticMarketDataGenerator(seed=123)
    equities = gen.generate_equity_returns(n_assets=5, n_periods=100)
    bonds = gen.generate_fixed_income(n_bonds=3, n_periods=100)
    alts = gen.generate_alternatives(n_assets=2, n_periods=100)
    macro = gen.generate_macroeconomic(n_periods=100)
    assert equities.shape == (100, 5)
    assert bonds.shape == (100, 3)
    assert alts.shape == (100, 2)
    assert macro.shape == (100, 3)
    assert not equities.isnull().any().any()
    assert not bonds.isnull().any().any()
    assert not alts.isnull().any().any()
    assert not macro.isnull().any().any()

def test_client_data_shapes():
    gen = SyntheticClientDataGenerator(n_clients=10, seed=123)
    demo = gen.generate_demographics()
    risk = gen.generate_risk_tolerance()
    goals = gen.generate_goal_hierarchies()
    behaviors = gen.generate_behavioral_patterns()
    assert demo.shape[0] == 10
    assert risk.shape[0] == 10
    assert goals['client_id'].max() < 10
    assert behaviors['client_id'].max() < 10 