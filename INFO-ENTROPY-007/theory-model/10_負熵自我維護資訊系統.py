"""
NSMIS.py
Negentropic Self-Maintenance Information System
Author: Theory Prototype
"""
import numpy as np
class NSMIS:
    def __init__(
        self,
        n=20,
        alpha=0.15,
        eta=0.05,
        sigma=0.02,
        beta=1.0,
        control_gain=1.0,
        seed=None,
    ):
        if seed is not None:
            np.random.seed(seed)
        self.n = n
        self.alpha = alpha
        self.eta = eta
        self.sigma = sigma
        self.beta = beta
        self.K = control_gain
        # state
        self.X = np.random.rand(n)
        # fully-connected coupling matrix
        W = np.ones((n, n))
        np.fill_diagonal(W, 0)
        W /= (n - 1)
        self.W = W
        self.history = {
            "entropy": [],
            "negentropy_flow": [],
            "lyapunov": [],
            "state_norm": [],
        }
    # --------------------------------------------------
    # Softmax probability mapping
    # --------------------------------------------------
    def softmax(self, x):
        z = x - np.max(x)
        e = np.exp(z)
        return e / np.sum(e)
    # --------------------------------------------------
    # Shannon entropy
    # --------------------------------------------------
    def entropy(self, x):
        p = self.softmax(x)
        return -np.sum(p * np.log(p + 1e-12))
    # --------------------------------------------------
    # Numerical entropy gradient
    # --------------------------------------------------
    def entropy_gradient(self, x, eps=1e-6):
        grad = np.zeros_like(x)
        for i in range(len(x)):
            xp = x.copy()
            xm = x.copy()
            xp[i] += eps
            xm[i] -= eps
            grad[i] = (
                self.entropy(xp)
                - self.entropy(xm)
            ) / (2 * eps)
        return grad
    # --------------------------------------------------
    # Neighborhood coupling
    # --------------------------------------------------
    def coupling(self, x):
        return self.W @ x - x
    # --------------------------------------------------
    # Observable variables
    # --------------------------------------------------
    def observe(self):
        H = self.entropy(self.X)
        logic_entropy = H
        info_potential = 1.0 / (H + 1e-8)
        return {
            "S_L": logic_entropy,
            "Phi": info_potential,
        }
    # --------------------------------------------------
    # Feedback signal
    # --------------------------------------------------
    def feedback_signal(
        self,
        target_entropy=1.0,
        target_phi=1.0,
        negentropy_flow=0.0,
    ):
        obs = self.observe()
        return np.array(
            [
                obs["S_L"] - target_entropy,
                target_phi - obs["Phi"],
                negentropy_flow,
            ]
        )
    # --------------------------------------------------
    # Control law
    # --------------------------------------------------
    def control(self, signal):
        return self.K * np.tanh(signal)
    # --------------------------------------------------
    # Lyapunov function
    # --------------------------------------------------
    def lyapunov(self, x, x_star):
        H = self.entropy(x)
        return H + self.beta * np.linalg.norm(
            x - x_star
        ) ** 2
    # --------------------------------------------------
    # One simulation step
    # --------------------------------------------------
    def step(self):
        H_before = self.entropy(self.X)
        grad_H = self.entropy_gradient(self.X)
        coupling_term = self.coupling(self.X)
        signal = self.feedback_signal()
        u_small = self.control(signal)
        U = np.mean(u_small) * np.ones(self.n)
        noise = np.random.normal(
            0,
            self.sigma,
            self.n,
        )
        self.X = (
            self.X
            + self.eta
            * (
                -grad_H
                + self.alpha * coupling_term
                + U
            )
            + noise
        )
        H_after = self.entropy(self.X)
        negentropy_flow = (
            H_before - H_after
        )
        x_star = np.mean(self.X) * np.ones(self.n)
        V = self.lyapunov(
            self.X,
            x_star,
        )
        self.history["entropy"].append(
            H_after
        )
        self.history[
            "negentropy_flow"
        ].append(
            negentropy_flow
        )
        self.history[
            "lyapunov"
        ].append(V)
        self.history[
            "state_norm"
        ].append(
            np.linalg.norm(self.X)
        )
    # --------------------------------------------------
    # Run simulation
    # --------------------------------------------------
    def run(self, steps=1000):
        for _ in range(steps):
            self.step()
        return self.history
# ======================================================
# Example
# ======================================================
if __name__ == "__main__":
    model = NSMIS(
        n=30,
        alpha=0.10,
        eta=0.03,
        sigma=0.01,
        seed=42,
    )
    result = model.run(
        steps=500
    )
    print(
        "Final Entropy:",
        result["entropy"][-1],
    )
    print(
        "Final Negentropy Flow:",
        result["negentropy_flow"][-1],
    )
    print(
        "Final Lyapunov:",
        result["lyapunov"][-1],
    )
    print(
        "State Norm:",
        result["state_norm"][-1],
    )
