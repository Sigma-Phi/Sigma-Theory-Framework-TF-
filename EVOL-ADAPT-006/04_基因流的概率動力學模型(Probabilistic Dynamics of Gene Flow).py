import numpy as np

# =========================================================
# Gene Flow Probabilistic Dynamical System (Simulation)
# =========================================================

class GeneFlowSystem:
    def __init__(self, n=5, sigma=0.01, seed=42):
        np.random.seed(seed)
        self.n = n
        self.sigma = sigma  # noise scale

        # initial state X_0 (must be in simplex Δ^n)
        self.X = self._normalize(np.random.rand(n))

        # external distribution O (can be static or time-varying)
        self.O = self._normalize(np.random.rand(n))

        # weight matrix W for control function
        self.W = np.random.randn(n, n) * 0.5

    def _normalize(self, x):
        x = np.clip(x, 1e-12, None)
        return x / np.sum(x)

    def softmax(self, x):
        e = np.exp(x - np.max(x))
        return e / np.sum(e)

    # signal function φ(X,O)
    def signal(self):
        return self.O - self.X

    # control function G(S)
    def control(self, S):
        return self.softmax(self.W @ S)

    # stochastic noise ε_t
    def noise(self):
        eps = np.random.normal(0, self.sigma, self.n)
        return self._normalize(self.X + eps) - self.X

    # main update rule
    def step(self):
        S = self.signal()
        U = self.control(S)

        eps = self.noise()

        self.X = (1 - U) * self.X + U * self.O + eps
        self.X = self._normalize(self.X)

        return self.X, U

    # KL divergence
    def kl_divergence(self, p, q):
        p = np.clip(p, 1e-12, 1)
        q = np.clip(q, 1e-12, 1)
        return np.sum(p * np.log(p / q))


# =========================================================
# Simulation
# =========================================================

def run_simulation(T=200):
    model = GeneFlowSystem(n=6, sigma=0.02)

    history = []
    kl_history = []

    O_star = model.O.copy()

    for t in range(T):
        X, U = model.step()

        kl = model.kl_divergence(X, O_star)

        history.append(X.copy())
        kl_history.append(kl)

        if t % 20 == 0:
            print(f"t={t}, KL={kl:.6f}, X={X}")

    return np.array(history), np.array(kl_history)


# =========================================================
# Run
# =========================================================

if __name__ == "__main__":
    history, kl = run_simulation(T=200)

    print("\nFinal state:", history[-1])
    print("Final KL divergence:", kl[-1])
