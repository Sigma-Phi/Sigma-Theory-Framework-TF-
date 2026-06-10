# celct_simulation.py
# Closed-Loop Entropy Limit Control Theory (CELCT) - Numerical Simulation

import numpy as np

# -----------------------------
# True distribution P*
# -----------------------------
P_star = np.array([0.2, 0.5, 0.3])
n = len(P_star)

# -----------------------------
# Initialization
# -----------------------------
T = 5000
eta_0 = 0.1

p = np.ones(n) / n          # initial belief (uniform)
m = 0.0                     # memory (entropy accumulation)

# tracking
p_history = np.zeros((T, n))
U_history = np.zeros(T)
H_history = np.zeros(T)
KL_history = np.zeros(T)

# -----------------------------
# Utility functions
# -----------------------------
def entropy(p):
    p = np.clip(p, 1e-12, 1.0)
    return -np.sum(p * np.log(p))

def kl_divergence(p, q):
    p = np.clip(p, 1e-12, 1.0)
    q = np.clip(q, 1e-12, 1.0)
    return np.sum(p * np.log(p / q))

def sample_from_distribution(dist):
    return np.random.choice(len(dist), p=dist)

# -----------------------------
# Simulation loop
# -----------------------------
for t in range(T):

    # step size (Robbins-Monro)
    eta_t = eta_0 / (1 + 0.001 * t)

    # observation
    O_t = sample_from_distribution(P_star)

    # probability update (stochastic approximation)
    p = (1 - eta_t) * p
    p[O_t] += eta_t

    # entropy
    H_t = entropy(p)

    # control (code length)
    U_t = -np.log(max(p[O_t], 1e-12))

    # memory update
    m += H_t

    # metrics
    KL_t = kl_divergence(P_star, p)

    # store
    p_history[t] = p
    U_history[t] = U_t
    H_history[t] = H_t
    KL_history[t] = KL_t

# -----------------------------
# Results
# -----------------------------
print("Final estimated distribution p_T:", p)
print("True distribution P*:", P_star)
print("Final entropy H(p_T):", entropy(p))
print("True entropy H(P*):", entropy(P_star))
print("Final KL divergence:", kl_divergence(P_star, p))
print("Average code length:", np.mean(U_history))

# Theoretical expectations:
# p_t → P*
# E[U_t] → H(P*)
# KL → 0
