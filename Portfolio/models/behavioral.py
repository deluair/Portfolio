from dataclasses import dataclass, field
from typing import Dict

@dataclass
class BehavioralProfile:
    biases: Dict[str, float] = field(default_factory=dict)  # e.g., {'Loss Aversion': 0.8, 'Herding': 0.3}

    def update_bias(self, bias, strength):
        self.biases[bias] = strength 