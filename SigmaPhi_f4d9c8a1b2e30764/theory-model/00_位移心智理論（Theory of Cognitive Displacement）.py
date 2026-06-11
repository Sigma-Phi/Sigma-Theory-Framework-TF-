import numpy as np
import matplotlib.pyplot as plt

# =========================
# 🧠 位移心智理論模擬
# =========================

np.random.seed(42)

T = 500  # 時間步數
N = 1    # 單軌跡（可改多粒子）

# 狀態初始化
pi = np.zeros((T, 3))
E = np.zeros(T)

pi[0] = np.array([0.6, 0.2, 0.2])  # 初始：偏運作層
E[0] = 0.2

# 參數
alpha = 0.05
k = 8.0
gamma0 = 0.1
delta = 0.05
E_max = 1.0

tau = 0.5  # 修正閾值

# sigmoid
def beta(s):
    return 1 / (1 + np.exp(-k * (s - 0.5)))

# 對象化程度（簡化）
def phi(state):
    return np.clip(state[2] + 0.3 * np.abs(state[1] - state[0]), 0, 1)

# 控制策略
def control(s):
    return 1 if s > tau else 0


# transition matrix generator
def transition_matrix(s, u):
    b = beta(s)
    g = gamma0 * (1 - u)

    P = np.array([
        [1 - alpha, alpha, 0],
        [0, 1 - b, b],
        [g, 0, 1 - g]
    ])

    # normalize rows
    P = P / P.sum(axis=1, keepdims=True)
    return P


# =========================
# simulation loop
# =========================

for t in range(T - 1):

    s = phi(pi[t])
    u = control(s)

    P = transition_matrix(s, u)

    pi[t + 1] = pi[t] @ P

    # noise
    noise = np.random.normal(0, 0.01)

    # energy dynamics
    if pi[t, 2] > 0.4 and u == 1:
        dE = 0.05 + noise
    elif u == 0:
        dE = -0.03 + noise
    else:
        dE = noise

    E[t + 1] = np.clip(E[t] + dE, 0, E_max)


# =========================
# visualization
# =========================

plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(pi[:, 0], label="Operational (π1)")
plt.plot(pi[:, 1], label="Reflective (π2)")
plt.plot(pi[:, 2], label="Recursive (π3)")
plt.title("Mind State Evolution")
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(E, color="red", label="Energy E_t")
plt.title("Recursive Overload Energy")
plt.legend()

plt.tight_layout()
plt.show()
