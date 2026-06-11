import numpy as np

# =========================
# 1. Entropy
# =========================
def entropy(y):
    """Shannon entropy"""
    values, counts = np.unique(y, return_counts=True)
    p = counts / len(y)
    return -np.sum(p * np.log2(p + 1e-12))


# =========================
# 2. Information Gain
# =========================
def info_gain(y, x):
    """binary split IG approximation"""
    parent_entropy = entropy(y)

    left_y = y[x == 0]
    right_y = y[x == 1]

    if len(left_y) == 0 or len(right_y) == 0:
        return 0

    child_entropy = (
        len(left_y) / len(y) * entropy(left_y)
        + len(right_y) / len(y) * entropy(right_y)
    )

    return parent_entropy - child_entropy


# =========================
# 3. Simplex projection
# =========================
def project_simplex(p):
    """Euclidean projection onto probability simplex"""
    p = np.clip(p, 0, None)
    return p / (np.sum(p) + 1e-12)


# =========================
# 4. IG-DPS system step
# =========================
def ig_dps_step(X, Y, features, noise_scale=0.01):
    """
    X: current belief distribution (state)
    Y: labels
    features: matrix (N, d)
    """

    n_features = features.shape[1]

    # --- compute IG for each feature ---
    igs = np.array([
        info_gain(Y, features[:, i])
        for i in range(n_features)
    ])

    # --- signal (argmax IG) ---
    s_t = np.argmax(igs)

    # --- control (one-hot) ---
    u = np.zeros(n_features)
    u[s_t] = 1

    # --- stochastic transition ---
    noise = np.random.normal(0, noise_scale, size=X.shape)

    # simplified "transition operator"
    X_next = X + u * 0.1 + noise

    # --- projection to simplex ---
    X_next = project_simplex(X_next)

    return X_next, igs, s_t


# =========================
# 5. Simulation
# =========================
def run_igdps(X0, Y, features, T=20):
    X = X0
    history_entropy = []
    history_ig = []

    for t in range(T):
        H = entropy(Y)
        history_entropy.append(H)

        X, igs, s_t = ig_dps_step(X, Y, features)

        history_ig.append(np.max(igs))

        print(f"t={t}, selected_feature={s_t}, IG={np.max(igs):.4f}, entropy={H:.4f}")

    return X, history_entropy, history_ig


# =========================
# 6. Synthetic dataset
# =========================
np.random.seed(42)

N = 200
d = 5

features = np.random.randint(0, 2, size=(N, d))

# label depends on feature 0 + noise (structured signal)
Y = (features[:, 0] ^ features[:, 1]).astype(int)

# initial state (uniform simplex)
X0 = np.ones(d) / d


# =========================
# 7. Run system
# =========================
final_X, H_hist, IG_hist = run_igdps(X0, Y, features, T=15)
