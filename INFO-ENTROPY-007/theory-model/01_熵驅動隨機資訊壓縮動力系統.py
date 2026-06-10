import numpy as np

np.random.seed(42)

# ---------------------------
# 基本設定
# ---------------------------
n = 5                 # state dimension
T = 2000              # time steps
eta0 = 0.1            # learning rate scale
alpha = 0.05          # control strength
eps = 1e-12

# ---------------------------
# 初始化 probability simplex
# ---------------------------
X = np.random.rand(n)
X = X / np.sum(X)

def entropy(p):
    p = np.clip(p, eps, 1.0)
    return -np.sum(p * np.log(p))

def sample_observation(p, N=50):
    return np.random.multinomial(N, p)

def empirical_distribution(obs):
    return obs / np.sum(obs)

# ---------------------------
# log-signal mapping
# ---------------------------
def signal(p):
    return -np.log(p + eps)

# ---------------------------
# control law（簡化版）
# ---------------------------
def control(s, x):
    return alpha * np.linalg.norm(s - (-np.log(x + eps)))

# ---------------------------
# simulation
# ---------------------------
entropy_trace = []
dist_trace = []

for t in range(T):
    
    # 1. observation
    O = sample_observation(X)
    P_hat = empirical_distribution(O)
    
    # 2. learning rate (decay)
    eta = eta0 / (1 + 0.001 * t)
    
    # 3. entropy signal
    S = signal(X)
    
    # 4. control (not strongly coupled, but included)
    U = control(S, X)
    
    # 5. stochastic approximation update
    X_new = (1 - eta) * X + eta * P_hat
    
    # optional weak control perturbation
    X_new = X_new + U * (P_hat - X)
    
    # 6. project back to simplex
    X_new = np.clip(X_new, eps, None)
    X = X_new / np.sum(X_new)
    
    # 7. logging
    entropy_trace.append(entropy(X))
    dist_trace.append(np.linalg.norm(P_hat - X))

# ---------------------------
# results
# ---------------------------
print("Final distribution:", X)
print("Final entropy:", entropy(X))
