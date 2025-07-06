from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Asset:
    asset_id: str
    name: str
    asset_type: str  # e.g., 'Equity', 'Bond', 'Alternative', 'ESG'
    sector: Optional[str] = None
    region: Optional[str] = None
    esg_score: Optional[float] = None
    currency: str = 'USD'
    other_attributes: dict = field(default_factory=dict)

@dataclass
class Equity(Asset):
    ticker: Optional[str] = None
    style: Optional[str] = None  # e.g., 'Growth', 'Value'

@dataclass
class Bond(Asset):
    maturity: Optional[str] = None
    coupon: Optional[float] = None
    rating: Optional[str] = None

@dataclass
class Alternative(Asset):
    subtype: Optional[str] = None  # e.g., 'Private Equity', 'Real Estate' 