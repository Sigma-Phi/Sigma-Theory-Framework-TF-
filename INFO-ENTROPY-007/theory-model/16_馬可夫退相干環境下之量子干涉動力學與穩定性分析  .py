import numpy as np

# =========================
# 基本設定
# =========================
N = 8                     # 系統維度 (2^n)
T = 200                   # 時間步數
M = 50                   # Monte Carlo 次數
gamma = 0.05             # decoherence rate
eta = np.pi / (4 * np.sqrt(N))

np.random.seed(42)

# 目標態 X*
X_star = np.zeros(N)
X_star[0] = 1.0


# =========================
# 工具函數
# =========================
def normalize(x):
    x = np.clip(x, 1e-12, None)
    return x / np.sum(x)


def kl_div(x, y):
    x = np.clip(x, 1e-12, 1)
    y = np.clip(y, 1e-12, 1)
    return np.sum(x * np.log(x / y))


def fidelity(x, x_star):
    return np.dot(np.sqrt(x), np.sqrt(x_star))**2


# =========================
# 馬可夫退相干（噪聲通道）
# =========================
def decoherence(x, gamma):
    noise = np.random.normal(0, gamma, size=len(x))
    x_noisy = x * (1 - gamma) + noise
    return normalize(x_noisy)


# =========================
# 控制 G（Lipschitz correction）
# 將機率往 target state 拉回
# =========================
def control_g(x):
    grad = X_star - x
    u = eta * grad
    x_new = x + u
    return normalize(x_new)


# =========================
# 單次 trajectory
# =========================
def run_once():
    x = np.ones(N) / N
    kl_trace = []
    fid_trace = []
    lyap_trace = []

    for t in range(T):

        # decoherence step
        x = decoherence(x, gamma)

        # control step (interference-like correction)
        x = control_g(x)

        # metrics
        kl = kl_div(x, X_star)
        fid = fidelity(x, X_star)
        V = 1 - x[0]

        kl_trace.append(kl)
        fid_trace.append(fid)
        lyap_trace.append(V)

    return np.array(kl_trace), np.array(fid_trace), np.array(lyap_trace)


# =========================
# Monte Carlo simulation
# =========================
kl_avg = np.zeros(T)
fid_avg = np.zeros(T)
lyap_avg = np.zeros(T)

for _ in range(M):
    kl, fid, lyap = run_once()
    kl_avg += kl
    fid_avg += fid
    lyap_avg += lyap

kl_avg /= M
fid_avg /= M
lyap_avg /= M


# =========================
# 結果輸出
# =========================
print("Final KL Divergence:", kl_avg[-1])
print("Final Fidelity:", fid_avg[-1])
print("Final Lyapunov V:", lyap_avg[-1])


# =========================
# 簡單視覺化（可選）
# =========================
try:
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12,4))

    plt.subplot(1,3,1)
    plt.plot(kl_avg)
    plt.title("KL Divergence")

    plt.subplot(1,3,2)
    plt.plot(fid_avg)
    plt.title("Fidelity")

    plt.subplot(1,3,3)
    plt.plot(lyap_avg)
    plt.title("Lyapunov V = 1 - p0")

    plt.tight_layout()
    plt.show()

except:
    pass
