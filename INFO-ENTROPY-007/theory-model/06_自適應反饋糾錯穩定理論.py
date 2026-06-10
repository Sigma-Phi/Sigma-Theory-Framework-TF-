import numpy as np

# =========================
# 1. 系統參數
# =========================
n = 50                     # bit length
T = 200                    # time steps
noise_prob = 0.08         # Bernoulli noise strength
alpha = 1.2                # correction strength
beta = 0.8                 # noise sensitivity
lambda_r = 0.5             # redundancy weight

# =========================
# 2. 初始化狀態
# =========================
X = np.random.randint(0, 2, n)
X_hat = X.copy()

def hamming(x, y):
    return np.sum(x != y)

# =========================
# 3. 噪聲模型 (A2)
# =========================
def channel_noise(x, p):
    noise = np.random.binomial(1, p, size=len(x))
    return np.bitwise_xor(x, noise)

# =========================
# 4. 控制函數 G(S_t)
# =========================
def controller(snr_est):
    # bounded nonlinear adaptive redundancy
    return np.clip(1.0 / (snr_est + 1e-3), 0, 1)

# =========================
# 5. 觀測 φ(X, O)
# =========================
def observe(x, x_hat):
    dist = hamming(x, x_hat)
    snr_est = 1.0 / (dist + 1e-3)
    return dist, snr_est

# =========================
# 6. Lyapunov function
# =========================
def V(dist, redundancy):
    return dist + lambda_r * redundancy

# =========================
# 7. 模擬主循環
# =========================
history_V = []
history_dist = []
history_snr = []

for t in range(T):

    # --- channel ---
    X_noisy = channel_noise(X, noise_prob)

    # --- observation ---
    dist, snr = observe(X_noisy, X_hat)

    # --- control ---
    R_t = controller(snr)

    # --- decoding (simplified correction rule) ---
    correction_strength = alpha * R_t - beta * noise_prob

    if correction_strength > 0:
        flip_prob = min(0.5, correction_strength * 0.1)
        correction_noise = np.random.binomial(1, flip_prob, size=n)
        X_hat = np.bitwise_xor(X_noisy, correction_noise)
    else:
        X_hat = X_noisy

    # --- update Lyapunov ---
    V_t = V(dist, R_t)

    history_V.append(V_t)
    history_dist.append(dist)
    history_snr.append(snr)

# =========================
# 8. 結果輸出
# =========================
print("Final Hamming Distance:", history_dist[-1])
print("Final Lyapunov Value:", history_V[-1])
print("Average Dist:", np.mean(history_dist))
print("System Stability (trend):", history_V[-1] - history_V[0])
