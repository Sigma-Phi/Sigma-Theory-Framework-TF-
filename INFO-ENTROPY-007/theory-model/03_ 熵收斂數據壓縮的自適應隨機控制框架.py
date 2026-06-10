import numpy as np

# =========================
# 1. Utility Functions
# =========================

def entropy(p):
    """Shannon entropy"""
    p = np.clip(p, 1e-12, 1.0)
    return -np.sum(p * np.log2(p))


def kl_div(p, q):
    """KL divergence P || Q"""
    p = np.clip(p, 1e-12, 1.0)
    q = np.clip(q, 1e-12, 1.0)
    return np.sum(p * np.log2(p / q))


def normalize(p):
    return p / np.sum(p)


# =========================
# 2. Stochastic Source
# =========================

def generate_source(T, k=4, regime="stationary"):
    """
    Generates symbolic stream probabilities
    """
    if regime == "stationary":
        base = np.random.dirichlet(np.ones(k))
        return np.random.choice(k, size=T, p=base)

    elif regime == "nonstationary":
        stream = []
        for t in range(T):
            base = np.random.dirichlet(np.ones(k) + (t % 5))
            stream.append(np.random.choice(k, p=base))
        return np.array(stream)


# =========================
# 3. Model Components (φ, F, G simplified)
# =========================

class CompressionSystem:
    def __init__(self, k=4, lr=0.05):
        self.k = k
        self.lr = lr

        # state X_t: probability estimate
        self.p_hat = np.ones(k) / k

        # entropy estimate
        self.H = entropy(self.p_hat)

        # Lyapunov energy
        self.V = []

    def phi(self, x_t, obs):
        """
        Observation update (Bayesian-like)
        """
        counts = np.bincount(obs, minlength=self.k)
        empirical = counts / np.sum(counts)
        return empirical

    def G(self, z_t):
        """
        Control law (adaptive learning rate modulation)
        """
        return self.lr * (1 + 0.1 * (entropy(z_t) - self.H))

    def F(self, x_t, z_t, u_t):
        """
        State update (nonlinear stochastic update)
        """
        new_p = (1 - u_t) * x_t + u_t * z_t
        return normalize(new_p)

    def step(self, obs_window):
        z_t = self.phi(None, obs_window)
        u_t = self.G(z_t)

        self.p_hat = self.F(self.p_hat, z_t, u_t)
        self.H = entropy(self.p_hat)

        return self.p_hat, self.H


# =========================
# 4. Simulation Loop
# =========================

def run_simulation(T=500, window=20, k=4):
    system = CompressionSystem(k=k)

    stream = generate_source(T, k=k, regime="nonstationary")

    entropies = []
    kl_vals = []

    for t in range(window, T):
        obs_window = stream[t-window:t]

        p_prev = system.p_hat.copy()

        p_hat, H = system.step(obs_window)

        # metrics
        entropies.append(H)
        kl_vals.append(kl_div(p_hat, p_prev))

        # Lyapunov-like function
        V = np.linalg.norm(p_hat - p_prev)**2 + abs(H - entropy(p_hat))
        system.V.append(V)

    return entropies, kl_vals, system.V


# =========================
# 5. Run
# =========================

if __name__ == "__main__":
    ent, kl, V = run_simulation()

    print("Final entropy:", ent[-1])
    print("Final KL:", kl[-1])
    print("Final Lyapunov energy:", V[-1])
