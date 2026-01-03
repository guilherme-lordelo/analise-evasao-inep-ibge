import numpy as np

def inv_logit(x):
    return 1 / (1 + np.exp(-x))

def logit(p):
    if np.any((p <= 0) | (p >= 1)):
        raise ValueError("logit requer valores estritamente entre 0 e 1")
    return np.log(p / (1 - p))
