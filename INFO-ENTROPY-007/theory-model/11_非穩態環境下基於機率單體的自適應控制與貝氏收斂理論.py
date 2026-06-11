# bayesian_simplex_convergence.py

import numpy as np
import matplotlib.pyplot as plt


class BayesianSimplexSystem:

    def __init__(self, mus, sigma, true_index=0):
        self.mus = np.array(mus)
        self.n = len(mus)
        self.sigma = sigma
        self.true_index = true_index

    def likelihood(self, obs):
        """
        S_t = phi(O_t)
        """
        coef = 1.0 / (np.sqrt(2 * np.pi) * self.sigma)

        return coef * np.exp(
            -0.5 * ((obs - self.mus) / self.sigma) ** 2
        )

    def control_operator(self, signal):
        """
        U_t = G(S_t)
        """
        return signal / np.sum(signal)

    def state_update(self, state, control):
        """
        X_{t+1}
        = (X_t ⊙ U_t) / sum(X_t ⊙ U_t)
        """
        posterior = state * control
        posterior /= np.sum(posterior)

        return posterior

    def sample_observation(self):
        """
        O_t ~ N(mu_true, sigma^2)
        """
        return np.random.normal(
            self.mus[self.true_index],
            self.sigma
        )

    def tvd(self, state):
        """
        Total Variation Distance
        """
        target = np.zeros(self.n)
        target[self.true_index] = 1.0

        return 0.5 * np.sum(np.abs(state - target))

    def lyapunov(self, state):
        """
        V(X_t) = -log(X_t(i*))
        """
        eps = 1e-15
        return -np.log(
            max(state[self.true_index], eps)
        )

    def run(self, T=1000):

        state = np.ones(self.n) / self.n

        states = [state.copy()]
        tvds = [self.tvd(state)]
        lyaps = [self.lyapunov(state)]

        for _ in range(T):

            obs = self.sample_observation()

            signal = self.likelihood(obs)

            control = self.control_operator(signal)

            state = self.state_update(
                state,
                control
            )

            states.append(state.copy())
            tvds.append(self.tvd(state))
            lyaps.append(self.lyapunov(state))

        return (
            np.array(states),
            np.array(tvds),
            np.array(lyaps)
        )


def monte_carlo(
        M=100,
        T=1000,
        sigma=1.0,
        threshold=0.01):

    convergence_times = []

    for _ in range(M):

        system = BayesianSimplexSystem(
            mus=[0.0, 2.0, 4.0],
            sigma=sigma,
            true_index=0
        )

        _, tvd_series, _ = system.run(T)

        hit = np.where(
            tvd_series < threshold
        )[0]

        if len(hit) > 0:
            convergence_times.append(hit[0])

    convergence_times = np.array(convergence_times)

    if len(convergence_times) == 0:
        return None

    mean = np.mean(convergence_times)

    ci_low = np.percentile(
        convergence_times,
        2.5
    )

    ci_high = np.percentile(
        convergence_times,
        97.5
    )

    return {
        "mean": mean,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "samples": len(convergence_times)
    }


if __name__ == "__main__":

    system = BayesianSimplexSystem(
        mus=[0.0, 2.0, 4.0],
        sigma=1.0,
        true_index=0
    )

    states, tvd, lyap = system.run(T=1000)

    print("Final Posterior:")
    print(states[-1])

    print("\nFinal TVD:")
    print(tvd[-1])

    print("\nFinal Lyapunov:")
    print(lyap[-1])

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(tvd)
    plt.title("TVD Convergence")
    plt.xlabel("Time")
    plt.ylabel("TVD")

    plt.subplot(1, 2, 2)
    plt.plot(lyap)
    plt.title("Lyapunov Function")
    plt.xlabel("Time")
    plt.ylabel("-log P(theta*)")

    plt.tight_layout()
    plt.show()

    print("\nMonte Carlo Test")

    result = monte_carlo(
        M=100,
        T=1000,
        sigma=1.0
    )

    print(result)
