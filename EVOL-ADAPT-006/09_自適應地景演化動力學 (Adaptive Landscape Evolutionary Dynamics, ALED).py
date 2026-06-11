import numpy as np

# =========================
# ALED: Adaptive Landscape Evolutionary Dynamics
# =========================

class ALED:
    def __init__(self, n=10, seed=42):
        np.random.seed(seed)
        self.n = n

        # state: simplex
        self.x = np.ones(n) / n

        # fitness landscape baseline
        self.f = np.random.uniform(0.5, 1.5, n)

        # noise level
        self.sigma = 0.05

        # control parameters
        self.gamma = 2.0
        self.mu_max = 0.2

    # -------------------------
    # entropy signal S_t
    # -------------------------
    def entropy(self, x):
        x = np.clip(x, 1e-12, 1)
        return -np.sum(x * np.log(x))

    # -------------------------
    # fitness observation
    # -------------------------
    def observe(self):
        noise = np.random.uniform(-self.sigma, self.sigma, self.n)
        return self.f + noise

    # -------------------------
    # adaptive mutation control U_t
    # -------------------------
    def control(self, S_t, S_target=None):
        if S_target is None:
            S_target = np.log(self.n)  # max entropy baseline

        u = self.gamma * (S_target - S_t)
        return np.clip(u, 0.0, self.mu_max)

    # -------------------------
    # replicator-mutator update
    # -------------------------
    def step(self):
        O = self.observe()

        # fitness-normalized selection
        fitness = self.x * O
        denom = np.sum(fitness) + 1e-12
        x_new = fitness / denom

        # signal
        S = self.entropy(self.x)

        # control
        U = self.control(S)

        # mutation / exploration (uniform noise)
        mutation = np.random.dirichlet(np.ones(self.n))

        # combine dynamics
        self.x = (1 - U) * x_new + U * mutation

        # renormalize (numerical safety)
        self.x = np.clip(self.x, 1e-12, 1)
        self.x = self.x / np.sum(self.x)

        return S, U, O


# =========================
# simulation
# =========================

def run_simulation(T=500, n=10):
    model = ALED(n=n)

    history_x = []
    history_S = []
    history_U = []

    for t in range(T):
        S, U, O = model.step()

        history_x.append(model.x.copy())
        history_S.append(S)
        history_U.append(U)

    return np.array(history_x), np.array(history_S), np.array(history_U)


# =========================
# evaluation metrics
# =========================

def convergence_metric(X):
    diffs = np.linalg.norm(X[1:] - X[:-1], axis=1)
    return diffs


def diversity_bounds(X):
    ent = [-np.sum(x*np.log(x+1e-12)) for x in X]
    return np.array(ent)


# =========================
# run
# =========================

if __name__ == "__main__":
    X, S, U = run_simulation()

    print("Final state:", X[-1])
    print("Final entropy:", S[-1])
    print("Average mutation:", np.mean(U))

    # simple diagnostics
    conv = convergence_metric(X)
    print("Convergence (last 10 steps):", conv[-10:])
