from dataclasses import dataclass

@dataclass
class FeeModel:
    management_fee_rate: float = 0.01  # 1% annual
    transaction_fee_rate: float = 0.001  # 0.1% per transaction

    def management_fee(self, portfolio_value):
        return self.management_fee_rate * portfolio_value

    def transaction_fee(self, transaction_amount):
        return self.transaction_fee_rate * transaction_amount 