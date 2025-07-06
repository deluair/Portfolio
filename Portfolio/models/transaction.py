from dataclasses import dataclass
from typing import Optional

@dataclass
class Transaction:
    transaction_id: str
    client_id: int
    asset_id: str
    date: str  # ISO format
    transaction_type: str  # 'buy' or 'sell'
    amount: float
    price: float
    fees: float = 0.0
    taxes: float = 0.0
    notes: Optional[str] = None 