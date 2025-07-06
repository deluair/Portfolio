import pandas as pd
from typing import Dict, List
from .asset import Asset
from .risk import RiskProfile
from .esg import ESGProfile
from .fee import FeeModel

class Portfolio:
    def __init__(self, holdings=None, assets=None):
        # holdings: dict of {asset: amount}
        self.holdings = holdings if holdings is not None else {}
        self.assets: List[Asset] = assets if assets is not None else []
        self.risk_profile = RiskProfile()
        self.esg_profile = ESGProfile()
        self.fee_model = FeeModel()

    def update_holding(self, asset, amount):
        self.holdings[asset] = self.holdings.get(asset, 0) + amount

    def add_asset(self, asset: Asset, amount: float):
        self.assets.append(asset)
        self.update_holding(asset.asset_id, amount)

    def remove_asset(self, asset_id: str):
        self.assets = [a for a in self.assets if a.asset_id != asset_id]
        if asset_id in self.holdings:
            del self.holdings[asset_id]

    def total_value(self, prices):
        # prices: dict or pd.Series of {asset: price}
        return sum(self.holdings.get(asset, 0) * price for asset, price in prices.items())

    def allocation(self, prices):
        # Return allocation as % of total value
        total = self.total_value(prices)
        if total == 0:
            return {asset: 0 for asset in self.holdings}
        return {asset: (self.holdings[asset] * prices.get(asset, 0)) / total for asset in self.holdings}

    def rebalance(self, target_alloc, prices):
        # target_alloc: dict of {asset: target %}
        total = self.total_value(prices)
        for asset, target_pct in target_alloc.items():
            self.holdings[asset] = (target_pct * total) / prices.get(asset, 1)

    def update_risk_profile(self, **kwargs):
        self.risk_profile.update(**kwargs)

    def update_esg_profile(self, **kwargs):
        self.esg_profile.update(**kwargs)

    def calculate_fees(self):
        return self.fee_model.management_fee(self.total_value({a.asset_id: 1 for a in self.assets})) 