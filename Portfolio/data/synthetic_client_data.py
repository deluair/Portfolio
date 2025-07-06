import pandas as pd
from faker import Faker
import numpy as np

class SyntheticClientDataGenerator:
    def __init__(self, n_clients=100, seed=42):
        self.n_clients = n_clients
        self.fake = Faker()
        Faker.seed(seed)
        np.random.seed(seed)

    def generate_demographics(self):
        data = []
        for _ in range(self.n_clients):
            profile = self.fake.simple_profile()
            age = np.random.randint(25, 80)
            income = np.random.normal(150000, 100000)
            wealth = np.random.lognormal(6, 1.2)
            family_size = np.random.randint(1, 6)
            data.append({
                'name': profile['name'],
                'age': age,
                'income': max(25000, income),
                'wealth': wealth,
                'family_size': family_size,
                'sex': profile['sex'],
                'address': profile['address']
            })
        return pd.DataFrame(data)

    def generate_risk_tolerance(self):
        # Simulate risk tolerance scores (1-10)
        return pd.DataFrame({
            'client_id': range(self.n_clients),
            'risk_tolerance': np.random.randint(1, 11, self.n_clients)
        })

    def generate_goal_hierarchies(self):
        # Simulate multiple goals per client
        goals = ['Retirement', 'Education', 'Major Purchase', 'Philanthropy']
        data = []
        for client_id in range(self.n_clients):
            n_goals = np.random.randint(1, 4)
            selected_goals = np.random.choice(goals, n_goals, replace=False)
            for goal in selected_goals:
                priority = np.random.randint(1, 4)
                data.append({'client_id': client_id, 'goal': goal, 'priority': priority})
        return pd.DataFrame(data)

    def generate_behavioral_patterns(self):
        # Simulate behavioral bias profiles
        biases = ['Loss Aversion', 'Recency Bias', 'Herding', 'Anchoring', 'Confirmation']
        data = []
        for client_id in range(self.n_clients):
            bias_profile = np.random.choice(biases, np.random.randint(1, 4), replace=False)
            for bias in bias_profile:
                data.append({'client_id': client_id, 'bias': bias})
        return pd.DataFrame(data) 