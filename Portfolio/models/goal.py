from dataclasses import dataclass
from typing import Optional

@dataclass
class Goal:
    goal_id: str
    client_id: int
    goal_type: str  # e.g., 'Retirement', 'Education'
    target_amount: float
    current_amount: float = 0.0
    priority: int = 1
    time_horizon_years: int = 10
    probability_of_success: Optional[float] = None
    notes: Optional[str] = None 