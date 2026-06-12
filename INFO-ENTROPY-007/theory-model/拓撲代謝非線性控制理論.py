import numpy as np
import networkx as nx

# -----------------------------
# 1. 系統參數
# -----------------------------
N = 200                  # 節點數 (可調大到 10^3~10^4)
T = 500                  # 時間步數
Mx = 10.0                # 最大負載
eta0 = 0.05              # 初始步長
sigma0 = 0.3             # noise scale
pc = 0.2                 # failure threshold (conceptual)

np.random.seed(42)

# -----------------------------
# 2. 建立 Scale-Free Network
# -----------------------------
G = nx.barabasi_albert_graph(N, 3)
A = nx.to_numpy_array(G)

# row-normalized adjacency = W
W = A / (A.sum(axis=1, keepdims=True) + 1e-12)

# node load x_t
x = np.random.rand(N) * 2

# -----------------------------
# 3. 熵函數
# -----------------------------
def entropy(x):
    p = x / (np.sum(x) + 1e-12)
    p = np.clip(p, 1e-12, 1)
    return -np.sum(p * np.log(p))

# -----------------------------
# 4. KL to uniform (Lyapunov term)
# -----------------------------
def kl_to_uniform(W):
    U = np.ones_like(W) / W.shape[0]
    Wp = W / (W.sum(axis=1, keepdims=True) + 1e-12)
    return np.sum(Wp * np.log((Wp + 1e-12) / (U + 1e-12)))

# -----------------------------
# 5. 控制更新 G (topology rewiring)
# -----------------------------
def control_update(W, grad, eta):
    noise = np.random.randn(*W.shape) * sigma0
    dW = -eta * grad + 0.01 * noise
    W_new = W + dW

    # projection to simplex (row-wise)
    W_new = np.maximum(W_new, 1e-6)
    W_new = W_new / W_new.sum(axis=1, keepdims=True)
    return W_new

# -----------------------------
# 6. 梯度（簡化 entropy gradient）
# -----------------------------
def entropy_grad(x):
    p = x / (np.sum(x) + 1e-12)
    return -(np.log(p + 1e-12) + 1)

# -----------------------------
# 7. dynamics function F (Euler-Maruyama)
# -----------------------------
def step(x, W, eta):
    noise = np.random.randn(N) * sigma0

    # nonlinear metabolic accumulation
    flow = W @ x

    dx = np.tanh(flow) - 0.1 * x + noise

    x_new = x + eta * dx
    x_new = np.clip(x_new, 0, Mx)

    return x_new

# -----------------------------
# 8. simulation logs
# -----------------------------
x_hist = []
V_hist = []

# -----------------------------
# 9. main loop
# -----------------------------
for t in range(T):

    eta = eta0 / (1 + 0.01 * t)   # Robbins-Monro

    # entropy gradient
    grad = np.outer(entropy_grad(x), entropy_grad(x))

    # update topology
    W = control_update(W, grad, eta)

    # update state
    x = step(x, W, eta)

    # Lyapunov function
    H = entropy(x)
    V = H + kl_to_uniform(W)

    x_hist.append(x.mean())
    V_hist.append(V)

# -----------------------------
# 10. results
# -----------------------------
print("Final mean load:", np.mean(x))
print("Final Lyapunov V:", V_hist[-1])
print("Stability trend (V decrease):", V_hist[0] - V_hist[-1])
