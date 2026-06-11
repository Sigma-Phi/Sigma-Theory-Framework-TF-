import numpy as np
import random
from scipy.special import logsumexp

# ----------------------------
# 1. 系統初始化
# ----------------------------

# 模擬樹拓撲: 用列表表示簡單葉節點排列 (最小例子: 3葉)
def random_tree_topology(M):
    return list(np.random.permutation(M))

# 分支長度向量初始化
def random_branch_lengths(M, t_max=1.0):
    return np.random.uniform(0.1, t_max, size=2*M-3)

# 模擬觀測矩陣 O: L位點，每位點有4種碱基
def simulate_observation(M, L):
    bases = ['A','C','G','T']
    return np.random.choice(bases, size=(M,L))

# ----------------------------
# 2. 信號映射函數 phi
# ----------------------------
def compute_marginal_likelihood(tree, lengths, obs):
    # 簡化: 假設每個位點獨立, 用隨機數代替真實似然
    L = obs.shape[1]
    return np.random.rand(L)

def phi(X, O):
    tau, t = X
    marginal_likelihood = compute_marginal_likelihood(tau, t, O)
    bootstrap_support = np.random.rand(len(tau))  # 隨機支持度
    return np.concatenate([marginal_likelihood, bootstrap_support])

# ----------------------------
# 3. 控制策略 G
# ----------------------------
def G(S, step_scale=0.1):
    # 根據信號 S 調整步長 (簡單線性映射)
    return np.clip(step_scale * (1 - np.mean(S)), 0.01, 0.2)

# ----------------------------
# 4. 狀態轉移函數 F (Metropolis-Hastings)
# ----------------------------
def propose_tree(tau):
    # 隨機交換兩個葉節點
    tau_new = tau.copy()
    i, j = np.random.choice(len(tau), 2, replace=False)
    tau_new[i], tau_new[j] = tau_new[j], tau_new[i]
    return tau_new

def propose_lengths(t, step_size):
    return t + np.random.normal(0, step_size, size=len(t))

def log_posterior(X, O):
    # 簡化: 使用隨機函數模擬 log posterior
    return np.random.randn()

def F(X, U, O):
    tau, t = X
    step_size = U
    tau_new = propose_tree(tau)
    t_new = propose_lengths(t, step_size)
    X_new = (tau_new, t_new)
    
    # Metropolis-Hastings acceptance
    log_acc_ratio = log_posterior(X_new, O) - log_posterior(X, O)
    if np.log(random.random()) < log_acc_ratio:
        return X_new
    else:
        return X

# ----------------------------
# 5. 主迴圈
# ----------------------------
def TMECT_simulation(M=3, L=5, iterations=1000):
    O = simulate_observation(M, L)
    X = (random_tree_topology(M), random_branch_lengths(M))
    
    trajectory = [X]
    
    for t in range(iterations):
        S = phi(X, O)
        U = G(S)
        X = F(X, U, O)
        trajectory.append(X)
        
        if t % 100 == 0:
            print(f"Iteration {t}: Tau={X[0]}, t={np.round(X[1],2)}, Step={np.round(U,3)}")
            
    return trajectory

# ----------------------------
# 6. 運行模擬
# ----------------------------
trajectory = TMECT_simulation(M=3, L=5, iterations=500)
