"""
===============================================================================
NODE-002
理論名稱：遺傳漂變固定化定理
英文名稱：Genetic Drift Fixation Theorem (GDFT)
STATUS: VERIFIED
TYPE: STOCHASTIC DYNAMICAL SYSTEM
AUTHOR: System_Trinity
===============================================================================
理論核心：
有限族群中的無偏隨機抽樣將使基因頻率形成有界馬丁格爾，
並最終收斂至吸收固定態。
X_t ∈ Δ^(m−1)
X_t → X∞ ∈ {e₁,...,eₘ}
===============================================================================
"""
import numpy as np
import matplotlib.pyplot as plt
class GeneticDriftSystem:
    """
    Genetic Drift Simulator
    State Space:
        X_t ∈ Δ^(m−1)
    Dynamics:
        K_(t+1) ~ Multinomial(Ne, X_t)
        X_(t+1) = K_(t+1) / Ne
    """
    def __init__(
        self,
        population_size: int,
        initial_frequency,
        max_generations: int = 10000,
        random_seed=None,
    ):
        self.Ne = population_size
        self.X0 = np.array(initial_frequency, dtype=float)
        self.max_generations = max_generations
        if random_seed is not None:
            np.random.seed(random_seed)
        if not np.isclose(self.X0.sum(), 1.0):
            raise ValueError("Allele frequencies must sum to 1.")
        self.num_alleles = len(self.X0)
    def shannon_entropy(self, x):
        x = np.clip(x, 1e-12, 1.0)
        return -np.sum(x * np.log(x))
    def is_fixated(self, x):
        return np.any(np.isclose(x, 1.0))
    def run(self):
        X = self.X0.copy()
        trajectory = [X.copy()]
        entropy_history = [self.shannon_entropy(X)]
        fixation_generation = None
        for t in range(self.max_generations):
            counts = np.random.multinomial(self.Ne, X)
            X = counts / self.Ne
            trajectory.append(X.copy())
            entropy_history.append(self.shannon_entropy(X))
            if self.is_fixated(X):
                fixation_generation = t + 1
                break
        return {
            "trajectory": np.array(trajectory),
            "entropy": np.array(entropy_history),
            "fixation_generation": fixation_generation,
            "final_state": X,
        }
def monte_carlo_fixation_probability(
    population_size,
    initial_frequency,
    runs=1000,
):
    m = len(initial_frequency)
    fixation_counter = np.zeros(m)
    for _ in range(runs):
        model = GeneticDriftSystem(
            population_size=population_size,
            initial_frequency=initial_frequency,
        )
        result = model.run()
        winner = np.argmax(result["final_state"])
        fixation_counter[winner] += 1
    fixation_probability = fixation_counter / runs
    return fixation_probability
def plot_trajectory(result):
    traj = result["trajectory"]
    generations = np.arange(len(traj))
    plt.figure(figsize=(10, 5))
    for i in range(traj.shape[1]):
        plt.plot(
            generations,
            traj[:, i],
            label=f"Allele {i+1}",
        )
    plt.xlabel("Generation")
    plt.ylabel("Frequency")
    plt.title("Genetic Drift Trajectory")
    plt.legend()
    plt.grid(True)
    plt.show()
def plot_entropy(result):
    entropy = result["entropy"]
    plt.figure(figsize=(10, 4))
    plt.plot(entropy)
    plt.xlabel("Generation")
    plt.ylabel("Shannon Entropy")
    plt.title("Diversity Decay")
    plt.grid(True)
    plt.show()
if __name__ == "__main__":
    # ----------------------------------------------------
    # Example Configuration
    # ----------------------------------------------------
    Ne = 100
    X0 = [0.5, 0.3, 0.2]
    model = GeneticDriftSystem(
        population_size=Ne,
        initial_frequency=X0,
        random_seed=42,
    )
    result = model.run()
    print("=" * 70)
    print("GENETIC DRIFT FIXATION THEOREM")
    print("=" * 70)
    print("Initial State:")
    print(X0)
    print("\nFinal State:")
    print(result["final_state"])
    print("\nFixation Generation:")
    print(result["fixation_generation"])
    print("\nFinal Entropy:")
    print(result["entropy"][-1])
    # ----------------------------------------------------
    # Monte Carlo Verification
    # ----------------------------------------------------
    probs = monte_carlo_fixation_probability(
        population_size=Ne,
        initial_frequency=X0,
        runs=5000,
    )
    print("\nEstimated Fixation Probability:")
    print(probs)
    print("\nTheoretical Probability:")
    print(np.array(X0))
    print("\nAbsolute Error:")
    print(np.abs(probs - np.array(X0)))
    # ----------------------------------------------------
    # Visualization
    # ----------------------------------------------------
    plot_trajectory(result)
    plot_entropy(result)
