import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. 系統參數
# =========================
np.random.seed(42)

T = 300                # 時間步數
n = 3                  # 狀態維度 X_t ∈ R^n

lam = 0.2              # Lyapunov / entropy weight
noise_scale = 0.05     # 噪聲

# =========================
# 2. 初始狀態
# =========================
X = np.zeros((T, n))
X[0] = np.random.randn(n)

# entropy proxy
def entropy(x):
    return np.sum(x**2)

# control rule U_t（可自行替換成更複雜認知模型）
def control_policy(x, t):
    """
    U_t = 1 -> pseudo-displacement (looping / rumination)
    U_t = 0 -> convergence mode
    """
    # 模擬：早期容易反芻，後期逐步收斂
    if t < 120:
        return 1 if np.linalg.norm(x) < 2 else 0
    else:
        return 0

# =========================
# 3. 動力系統 F(X_t, U_t)
# =========================
def dynamics(x, u):
    if u == 1:
        # pseudo-displacement：limit cycle + positive feedback
        A = np.array([[0.8, -0.3, 0.1],
                      [0.3,  0.9, -0.2],
                      [-0.1, 0.2, 0.85]])
        x_next = A @ x + 0.1 * np.tanh(x)
    else:
        # convergence：contractive mapping (吸引子)
        A = np.eye(3) * 0.6
        attractor = np.array([0.1, -0.2, 0.05])
        x_next = A @ x + (1 - 0.6) * attractor

    # noise
    x_next += noise_scale * np.random.randn(3)
    return x_next

# =========================
# 4. Lyapunov function V(X)
# =========================
def V(x, u):
    cycle_penalty = 1.0 if u == 1 else 0.0
    return entropy(x) + lam * cycle_penalty

# =========================
# 5. 模擬主迴圈
# =========================
U = np.zeros(T)
V_trace = np.zeros(T)

for t in range(T - 1):
    U[t] = control_policy(X[t], t)
    X[t + 1] = dynamics(X[t], U[t])
    V_trace[t] = V(X[t], U[t])

U[-1] = control_policy(X[-1], T-1)
V_trace[-1] = V(X[-1], U[-1])

# =========================
# 6. 視覺化
# =========================
fig, axs = plt.subplots(3, 1, figsize=(10, 8))

# state trajectory
axs[0].plot(X)
axs[0].set_title("State Trajectory X_t")
axs[0].legend(["x1", "x2", "x3"])

# control signal
axs[1].plot(U, color="red")
axs[1].set_title("Control Signal U_t (0=converge, 1=pseudo-displacement)")

# Lyapunov function
axs[2].plot(V_trace, color="green")
axs[2].set_title("Lyapunov / Entropy V(X)")

plt.tight_layout()
plt.show()
