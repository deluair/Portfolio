from dataclasses import dataclass, field
from typing import List, Dict, Optional
from .portfolio import Portfolio
from .risk import RiskProfile
from .behavioral import BehavioralProfile
from .esg import ESGProfile
from .fee import FeeModel
from .goal import Goal

@dataclass
class Client:
    client_id: int
    name: str
    age: int
    income: float
    wealth: float
    family_size: int
    sex: str
    address: str
    risk_tolerance: int
    goals: List[Goal] = field(default_factory=list)
    behavioral_profile: BehavioralProfile = field(default_factory=BehavioralProfile)
    risk_profile: RiskProfile = field(default_factory=RiskProfile)
    esg_profile: ESGProfile = field(default_factory=ESGProfile)
    fee_model: FeeModel = field(default_factory=FeeModel)
    portfolio: Portfolio = field(default_factory=Portfolio) 