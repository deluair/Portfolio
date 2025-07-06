from dataclasses import dataclass

@dataclass
class ESGProfile:
    environmental: float = 0.0
    social: float = 0.0
    governance: float = 0.0
    overall: float = 0.0

    def update(self, environmental=None, social=None, governance=None):
        if environmental is not None:
            self.environmental = environmental
        if social is not None:
            self.social = social
        if governance is not None:
            self.governance = governance
        self.overall = (self.environmental + self.social + self.governance) / 3 