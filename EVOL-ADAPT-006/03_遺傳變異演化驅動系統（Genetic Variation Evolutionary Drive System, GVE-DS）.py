import numpy as np

# =========================
# Genetic Variation Evolutionary Drive System (GVE-DS)
# =========================

class GVEDS:
    def __init__(self, n=10, m=5, k=5, seed=42):
        np.random.seed(seed)

        # state space X_t ∈ R^n
        self.n = n
        self.X = np.random.randn(n)

        # observation space O_t ∈ R^m
        self.m = m

        # signal space S_t ∈ R^k
        self.k = k

        # parameters
        self.sigma = 0.1          # noise level
        self.lam = 0.05           # gradient strength
        self.alpha = 0.2          # selection strength

        # optimal genotype (unknown in real system, here for Lyapunov)
        self.X_star = np.ones(n)

        # history
        self.history = []

    # -------------------------
    # φ: genotype → phenotype
    # nonlinear + Lipschitz
    # -------------------------
    def phi(self, X, O):
        return np.tanh(X[:self.k] + 0.1 * np.mean(O))

    # -------------------------
    # G: mutation generator (stochastic policy)
    # -------------------------
    def G(self, S):
        noise = np.random.randn(self.n) * self.sigma
        policy = np.tanh(np.pad(S, (0, self.n - len(S))))
        return policy + noise

    # -------------------------
    # environment observation
    # -------------------------
    def observe(self):
        return np.random.randn(self.m)

    # -------------------------
    # fitness / risk function R
    # -------------------------
    def R(self, X, O):
        return np.sum((X - np.mean(O))**2)

    # gradient approximation
    def grad_R(self, X, O):
        return 2 * (X - np.mean(O))

    # -------------------------
    # F: transition dynamics
    # -------------------------
    def F(self, X, O, U):
        noise = np.random.randn(self.n) * self.sigma
        grad = self.grad_R(X, O)

        return (
            X
            + U
            + noise
            - self.lam * grad
        )

    # -------------------------
    # Lyapunov function
    # -------------------------
    def V(self, X):
        return np.linalg.norm(X - self.X_star) ** 2

    # -------------------------
    # one step
    # -------------------------
    def step(self):
        O = self.observe()
        S = self.phi(self.X, O)
        U = self.G(S)

        X_next = self.F(self.X, O, U)

        self.history.append({
            "V": self.V(self.X),
            "fitness": self.R(self.X, O)
        })

        self.X = X_next

    # -------------------------
    # run simulation
    # -------------------------
    def run(self, T=200):
        for _ in range(T):
            self.step()

        return self.history


# =========================
# Run simulation
# =========================

if __name__ == "__main__":
    system = GVEDS(n=20)
    history = system.run(T=300)

    V_vals = [h["V"] for h in history]
    F_vals = [h["fitness"] for h in history]

    print("Final Lyapunov V:", V_vals[-1])
    print("Final Fitness:", F_vals[-1])

    # simple trend check
    print("Lyapunov trend (first → last):", V_vals[0], "→", V_vals[-1])
