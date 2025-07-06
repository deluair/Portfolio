import numpy as np
import random

def set_global_seed(seed):
    np.random.seed(seed)
    random.seed(seed)

# Add more utility functions as needed

def log(message):
    print(f"[LOG] {message}") 