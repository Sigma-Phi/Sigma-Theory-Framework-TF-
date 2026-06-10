import numpy as np

# =========================
# 熵驅動雜訊反演系統模擬
# Noise-Adaptive Feedback System
# =========================

np.random.seed(42)

# -------------------------
# Hyperparameters
# -------------------------
n = 5                  # state dimension
T = 200                # time steps
eta = 0.05             # control gain
alpha = 0.01           # learning rate for W_t
sigma2 = 0.5           # noise variance

# -------------------------
# Initialization
# -------------------------
X = np.random.randn(n) * 2        # true latent state X_t
X_star = X.copy()

W = np.eye(n) * 0.1               # adaptive matrix W_t
SNR_list = []
error_list = []
loss_list = []

# -------------------------
# Storage
# -------------------------
X_hist = []
O_hist = []
S_hist = []

# -------------------------
# Simulation loop
# -------------------------
for t in range(T):

    # -------------------------
    # Observation noise
    # O_t = X_t + N_t
    # -------------------------
    noise = np.random.multivariate_normal(
        mean=np.zeros(n),
        cov=sigma2 * np.eye(n)
    )

    O = X + noise

    # -------------------------
    # Signal extraction
    # S_t = O_t - X_t
    # -------------------------
    S = O - X

    # -------------------------
    # Control law
    # U_t = -eta * W_t * S_t
    # -------------------------
    U = -eta * W @ S

    # -------------------------
    # State update
    # X_{t+1} = X_t + U_t
    # -------------------------
    X = X + U

    # -------------------------
    # Adaptive matrix update
    # W_{t+1} = W_t + alpha (S S^T - sigma^2 I)
    # -------------------------
    W = W + alpha * (np.outer(S, S) - sigma2 * np.eye(n))

    # -------------------------
    # Metrics
    # -------------------------
    signal_power = np.linalg.norm(X) ** 2
    noise_power = np.linalg.norm(S) ** 2 + 1e-8

    snr = 10 * np.log10(signal_power / noise_power)

    error = np.linalg.norm(X - X_star) ** 2
    loss = np.linalg.norm(S) ** 2

    # -------------------------
    # Store
    # -------------------------
    X_hist.append(X.copy())
    O_hist.append(O.copy())
    S_hist.append(S.copy())

    SNR_list.append(snr)
    error_list.append(error)
    loss_list.append(loss)

# =========================
# Results
# =========================
print("Final State X_T:", X)
print("Final Error:", error_list[-1])
print("Final Loss (||S||^2):", loss_list[-1])
print("Final SNR (dB):", SNR_list[-1])

# =========================
# Simple convergence check
# =========================
print("\n--- Convergence Summary ---")
print("Initial Loss:", loss_list[0])
print("Final Loss:", loss_list[-1])
print("Loss Reduction Ratio:", loss_list[0] / (loss_list[-1] + 1e-8))

# =========================
# Optional: spectral stability check
# =========================
eigvals = np.linalg.eigvals(np.eye(n) - eta * W)
spectral_radius = np.max(np.abs(eigvals))

print("\nSpectral Radius of (I - eta W_T):", spectral_radius)
