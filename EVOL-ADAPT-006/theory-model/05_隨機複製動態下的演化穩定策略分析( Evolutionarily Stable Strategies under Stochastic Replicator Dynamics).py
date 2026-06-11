import numpy as np

# =========================
# 1. 系統參數設定
# =========================

np.random.seed(42)

n = 5  # strategies number

T = 500  # time steps

mu_max = 0.05

# payoff matrix A_t (fixed or time-varying)
A = np.array([
    [3, 0, 1, 2, 1],
    [2, 3, 0, 1, 0],
    [1, 2, 3, 0, 1],
    [0, 1, 2, 3, 2],
    [1, 0, 1, 2, 3]
], dtype=float)

V = 1.0
C = 0.5

# =========================
# 2. 初始化 state (Δ^n)
# =========================

x = np.random.dirichlet(np.ones(n))

history = []
entropy_history = []

# =========================
# 3. 工具函數
# =========================

def fitness(x):
    """fitness function f_i = (A x)_i + V - C*(1 - x_i)"""
    Ax = A @ x
    return Ax + V - C * (1 - x)

def mean_fitness(f, x):
    return np.sum(x * f)

def entropy(x):
    x_safe = np.clip(x, 1e-12, 1)
    return -np.sum(x_safe * np.log(x_safe))

def mutation_rate(f):
    # bounded control policy (proxy for gradient norm)
    return min(mu_max, np.linalg.norm(f) / (10 + np.linalg.norm(f)))

# =========================
# 4. 主迭代 dynamics
# =========================

for t in range(T):

    f = fitness(x)
    f_bar = mean_fitness(f, x)

    mu = mutation_rate(f)

    # replicator-mutator update
    x_next = (1 - mu) * x * (f / (f_bar + 1e-12)) + mu * (1.0 / n)

    # normalization (numerical stability)
    x_next = np.clip(x_next, 0, 1)
    x_next = x_next / np.sum(x_next)

    # record
    history.append(x.copy())
    entropy_history.append(entropy(x))

    # update
    x = x_next

# =========================
# 5. 結果分析
# =========================

history = np.array(history)

print("Final state (ESS approximation):")
print(x)

print("\nFinal entropy:")
print(entropy(x))

print("\nStrategy convergence (last 10 steps):")
print(history[-10:])
