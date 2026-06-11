import numpy as np

# =========================
# System Parameters
# =========================
n = 30              # total nodes
f = 8               # byzantine nodes (must be < n/3 ideally)
T = 50             # time steps

np.random.seed(42)

# =========================
# Initialization
# =========================
X = np.random.randint(0, 2, size=n)  # binary states

byzantine_idx = np.random.choice(n, f, replace=False)
honest_idx = np.array([i for i in range(n) if i not in byzantine_idx])

# =========================
# Lyapunov function
# =========================
def lyapunov(X):
    # disagreement = average pairwise mismatch
    n = len(X)
    diff = 0
    for i in range(n):
        for j in range(n):
            diff += abs(X[i] - X[j])
    return diff / (n * n)

# =========================
# Honest update rule (majority rule)
# =========================
def honest_update(X):
    new_X = X.copy()
    majority = 1 if np.sum(X) >= len(X) / 2 else 0
    for i in honest_idx:
        # local noisy observation of majority
        noise = np.random.rand() < 0.05
        if noise:
            new_X[i] = 1 - majority
        else:
            new_X[i] = majority
    return new_X

# =========================
# Byzantine behavior
# =========================
def byzantine_update(X):
    for i in byzantine_idx:
        # adversarial flipping strategy
        if np.random.rand() < 0.5:
            X[i] = 1 - X[i]
        else:
            X[i] = np.random.randint(0, 2)
    return X

# =========================
# Simulation loop
# =========================
print("Initial state:", X)
print("Byzantine nodes:", byzantine_idx)

for t in range(T):
    X = honest_update(X)
    X = byzantine_update(X)

    V = lyapunov(X)

    print(f"t={t:02d}, V(X)={V:.4f}, state_sum={np.sum(X)}")

# =========================
# Final result
# =========================
print("\nFinal state:", X)
print("Final disagreement:", lyapunov(X))
