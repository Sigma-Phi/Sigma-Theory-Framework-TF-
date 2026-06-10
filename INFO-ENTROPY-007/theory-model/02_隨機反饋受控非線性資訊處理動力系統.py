import numpy as np
import matplotlib.pyplot as plt


# =========================
# DIPLM-F Core Simulation
# =========================

class DIPLMF:
    def __init__(self, n=10, lam=0.1, sigma=0.01):
        self.n = n
        self.lam = lam
        self.sigma = sigma

        # state s_t ∈ R^n
        self.s = np.random.uniform(-0.1, 0.1, n)

        # weight W_t ∈ R^{n×n}
        self.W = np.random.randn(n, n) * 0.1

    # noise η_t
    def noise(self):
        return np.random.normal(0, self.sigma, self.n)

    # control U_t = λ(1 - s_t)
    def control(self):
        return self.lam * (1 - self.s)

    # one step update
    def step(self, O):
        eta = self.noise()
        U = self.control()

        # state update: tanh(W s + O + noise)
        s_next = np.tanh(self.W @ self.s + O + eta)

        # weight update: W + U s^T
        self.W = self.W + np.outer(U, self.s)

        self.s = s_next

        return self.s, self.W


# =========================
# Metrics (可驗證部分)
# =========================

def spectral_radius(W):
    return max(abs(np.linalg.eigvals(W)))


def error_norm(s):
    # target fixed point assumed = zero vector (for test stability)
    return np.linalg.norm(s)


# =========================
# Run Simulation
# =========================

def run_sim(T=200):
    model = DIPLMF(n=10, lam=0.05, sigma=0.02)

    errors = []
    spectra = []

    for t in range(T):
        O = np.random.normal(0, 0.1, model.n)

        s, W = model.step(O)

        errors.append(error_norm(s))
        spectra.append(spectral_radius(W))

    return errors, spectra


# =========================
# Plot results
# =========================

if __name__ == "__main__":
    errors, spectra = run_sim(300)

    plt.figure(figsize=(12, 5))

    # error convergence
    plt.subplot(1, 2, 1)
    plt.plot(errors)
    plt.title("State Error ||s_t||")
    plt.xlabel("t")
    plt.ylabel("Error")

    # spectral radius
    plt.subplot(1, 2, 2)
    plt.plot(spectra)
    plt.title("Spectral Radius of W_t")
    plt.xlabel("t")
    plt.ylabel("ρ(W)")

    plt.tight_layout()
    plt.show()
