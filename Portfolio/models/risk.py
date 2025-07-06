from dataclasses import dataclass, field
from typing import Dict

@dataclass
class RiskProfile:
    var: float = 0.0  # Value at Risk
    cvar: float = 0.0  # Conditional Value at Risk
    volatility: float = 0.0
    exposures: Dict[str, float] = field(default_factory=dict)  # e.g., {'equity': 0.6, 'bond': 0.3}

    def update(self, var=None, cvar=None, volatility=None, exposures=None):
        if var is not None:
            self.var = var
        if cvar is not None:
            self.cvar = cvar
        if volatility is not None:
            self.volatility = volatility
        if exposures is not None:
            self.exposures = exposures 