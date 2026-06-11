import numpy as np
import matplotlib.pyplot as plt


class KinSelectionDynamics:
    def __init__(
        self,
        theta=0.05,
        beta=5.0,
        B_max=5.0,
        C_max=3.0,
        seed=42
    ):
        self.theta = theta
        self.beta = beta
        self.B_max = B_max
        self.C_max = C_max
        np.random.seed(seed)

    # sigmoid control (G function)
    def control_policy(self, o, B, C):
        signal = o * B - C
        return 1 / (1 + np.exp(-self.beta * signal))

    # environment generator (phi)
    def environment(self):
        B = np.random.uniform(0, self.B_max)
        C = np.random.uniform(0, self.C_max)
        r = np.random.uniform(0, 1)  # kin recognition signal
        return r, B, C

    # state transition F
    def step(self, x):
        o, B, C = self.environment()

        u = self.control_policy(o, B, C)

        fitness_signal = o * B - C

        # replicator-like nonlinear update
        dx = self.theta * x * (1 - x) * u * fitness_signal

        x_next = x + dx

        # projection to simplex [0,1]
        x_next = np.clip(x_next, 0.0, 1.0)

        return x_next, o, B, C, u, dx


def simulate(T=500, x0=0.1):
    model = KinSelectionDynamics()

    x = np.zeros(T)
    u_series = np.zeros(T)
    signal_series = np.zeros(T)

    x[0] = x0

    for t in range(T - 1):
        x[t + 1], o, B, C, u, dx = model.step(x[t])

        u_series[t] = u
        signal_series[t] = o * B - C

    return x, u_series, signal_series


if __name__ == "__main__":
    T = 600
    x, u, s = simulate(T=T, x0=0.05)

    plt.figure(figsize=(12, 5))

    plt.plot(x, label="Altruism frequency x(t)")
    plt.plot(u, label="Control u(t)", alpha=0.6)
    plt.plot(s, label="Hamilton signal (oB - C)", alpha=0.4)

    plt.axhline(0.5, linestyle="--", alpha=0.3)

    plt.title("Inclusive Fitness Kin Selection Dynamics Simulation")
    plt.legend()
    plt.xlabel("Time step")
    plt.ylabel("Value")
    plt.tight_layout()
    plt.show()
