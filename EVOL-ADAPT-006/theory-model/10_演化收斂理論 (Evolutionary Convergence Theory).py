import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# 參數設定
# ---------------------------
N = 50          # 群體大小
d = 5           # 基因長度
T = 100         # 世代數
p_c_min, p_c_max = 0.5, 1.0  # 交配機率上下界
p_m_min, p_m_max = 0.01, 0.2  # 突變機率上下界
theta_m = 0.1   # 突變控制參數
epsilon = 1e-6  # 防止除零
X_bounds = (-5.12, 5.12)  # Rastrigin 解空間

# ---------------------------
# 適應度函數 (Rastrigin)
# ---------------------------
def fitness(x):
    A = 10
    return -(A * len(x) + np.sum(x**2 - A * np.cos(2 * np.pi * x)))  # 越大越好

# ---------------------------
# 初始化群體
# ---------------------------
X = np.random.uniform(X_bounds[0], X_bounds[1], size=(N, d))
best_history = []

# ---------------------------
# 演化過程
# ---------------------------
for t in range(T):
    # 計算適應度
    f_values = np.array([fitness(x) for x in X])
    
    # 精英保留
    elite_idx = np.argmax(f_values)
    elite = X[elite_idx].copy()
    
    # 選擇 (輪盤賭)
    prob = (f_values - f_values.min()) + 1e-6  # 避免負值
    prob /= prob.sum()
    selected_idx = np.random.choice(N, size=N, p=prob)
    X_new = X[selected_idx].copy()
    
    # 交配 (單點重組)
    for i in range(0, N, 2):
        if i+1 < N and np.random.rand() < np.random.uniform(p_c_min, p_c_max):
            point = np.random.randint(1, d)
            X_new[i, point:], X_new[i+1, point:] = X_new[i+1, point:].copy(), X_new[i, point:].copy()
    
    # 計算群體多樣性
    div = np.mean(np.linalg.norm(X_new - X_new.mean(axis=0), axis=1))
    p_m = min(p_m_max, max(p_m_min, theta_m / (div + epsilon)))
    
    # 突變
    mutation = np.random.uniform(-1, 1, size=(N, d)) * p_m
    X_new += mutation
    X_new = np.clip(X_new, X_bounds[0], X_bounds[1])
    
    # 精英回補
    X_new[np.argmin([fitness(x) for x in X_new])] = elite
    
    X = X_new
    best_history.append(fitness(elite))

# ---------------------------
# 繪圖
# ---------------------------
plt.plot(best_history)
plt.xlabel("Generation")
plt.ylabel("Best Fitness")
plt.title("Evolutionary Convergence Simulation")
plt.grid(True)
plt.show()
