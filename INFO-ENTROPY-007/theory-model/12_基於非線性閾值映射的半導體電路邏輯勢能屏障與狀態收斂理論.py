import numpy as np

# =========================
# 参数（对应 A5）
# =========================
n = 8
T = 300
dt = 0.1

V_max = 1.0
theta = 0.5
L = 6.0
eta_t = dt

noise_scale = 0.03


# =========================
# A3: σ (Lipschitz sigmoid)
# =========================
def sigma(x):
    return 1.0 / (1.0 + np.exp(-L * (x - theta)))


# =========================
# φ: 信号传导函数 (S = φ(X) = WX)
# =========================
def phi(X, W):
    return W @ X


# =========================
# G: 控制函数 U = G(X,t)
# =========================
def G(X, t):
    return -0.3 * (X - 0.5)


# =========================
# F: 状态转移函数
# X_{t+1} = F(X_t, U_t, ξ_t)
# =========================
def F(X, U, noise, W):
    return sigma(phi(X, W) + U + noise)


# =========================
# Lyapunov 函数 V(X)
# =========================
def V(X, X_star):
    return np.linalg.norm(X - X_star) ** 2


# =========================
# A1: state space initialization
# =========================
X = np.random.uniform(0, 1, n)

# O: observation space（直接等于 X）
O = X.copy()

# S: signal space（将由 φ 生成）
# U: control space

# W: topology matrix
W = np.random.randn(n, n) * 0.2

# 理想吸引子（理论 X*）
X_star = np.ones(n) * 0.5


trajectory = []
lyapunov = []


# =========================
# 主循环（动态系统）
# =========================
for t in range(T):

    # A2: sub-Gaussian noise
    xi_t = np.random.normal(0, noise_scale, n)

    # U = G(X,t)
    U_t = G(X, t)

    # S = φ(X)
    S_t = phi(X, W)

    # F 更新
    X_next = F(X, U_t, xi_t, W)

    # A1 bound
    X_next = np.clip(X_next, 0, V_max)

    # 更新 observation
    O = X_next.copy()

    # record
    trajectory.append(X_next.copy())
    lyapunov.append(V(X_next, X_star))

    X = X_next


trajectory = np.array(trajectory)


# =========================
# 收敛性（对应 Proposition）
# =========================
def estimate_lambda(Vt):
    Vt = np.maximum(Vt, 1e-12)
    t = np.arange(len(Vt))
    return -np.polyfit(t, np.log(Vt), 1)[0]


lambda_est = estimate_lambda(lyapunov)


# =========================
# 输出（对应 Theorem conclusion）
# =========================
print("Final X_t:", X)
print("Final O_t:", O)
print("Final V:", lyapunov[-1])
print("Estimated λ:", lambda_est)

if lambda_est > 0:
    print("✔ System satisfies exponential decay behavior")
else:
    print("✘ No exponential convergence detected")
