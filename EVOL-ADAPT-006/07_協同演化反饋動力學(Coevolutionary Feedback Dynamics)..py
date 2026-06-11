import numpy as np

# =========================
# 參數設定
# =========================
np.random.seed(42)

dA = 3   # species A dimension
dB = 3   # species B dimension
dE = 3   # environment dimension

eta = 0.05
sigma_A = 0.1
sigma_B = 0.1

T = 500  # time steps

# =========================
# 初始化狀態
# =========================
xA = np.random.randn(dA)
xB = np.random.randn(dB)
e  = np.random.randn(dE)

# =========================
# 適應度函數（可調）
# =========================
def fitness_A(xA, xB, e):
    return -np.sum((xA - e)**2) + 0.5 * np.sum(xA * xB)

def fitness_B(xB, xA, e):
    return -np.sum((xB - e)**2) + 0.5 * np.sum(xB * xA)

# =========================
# 梯度近似（數值）
# =========================
def numerical_grad(f, x, x_opponent, e, eps=1e-5):
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x_pos = x.copy()
        x_neg = x.copy()
        x_pos[i] += eps
        x_neg[i] -= eps
        
        f_pos = f(x_pos, x_opponent, e)
        f_neg = f(x_neg, x_opponent, e)
        
        grad[i] = (f_pos - f_neg) / (2 * eps)
    return grad

# =========================
# 記錄
# =========================
history_A = []
history_B = []
history_E = []
V_history = []

# =========================
# Lyapunov function
# =========================
def V(xA, xB, e):
    return np.sum((xA - xB)**2)

# =========================
# 主迭代
# =========================
for t in range(T):
    
    # ---- gradients ----
    grad_A = numerical_grad(fitness_A, xA, xB, e)
    grad_B = numerical_grad(fitness_B, xB, xA, e)
    
    # ---- stochastic noise ----
    noise_A = sigma_A * np.random.randn(dA)
    noise_B = sigma_B * np.random.randn(dB)
    
    # ---- environment update ----
    g_e = -0.1 * (e - 0.5 * (xA + xB))
    
    # =========================
    # Euler update (core dynamics)
    # =========================
    xA = xA + eta * grad_A + noise_A
    xB = xB + eta * grad_B + noise_B
    e  = e  + eta * g_e
    
    # =========================
    # record
    # =========================
    history_A.append(xA.copy())
    history_B.append(xB.copy())
    history_E.append(e.copy())
    V_history.append(V(xA, xB, e))

# =========================
# 結果分析
# =========================
history_A = np.array(history_A)
history_B = np.array(history_B)
V_history = np.array(V_history)

print("Final state A:", xA)
print("Final state B:", xB)
print("Final environment:", e)
print("Final Lyapunov V:", V_history[-1])
