import numpy as np

# -----------------------------
# PARAMETERS
# -----------------------------
n = 5  # number of phenotypes
p = 5  # number of candidate mates
T = 50  # number of generations
alpha = 2.0  # selection strength
noise_std = 0.01  # stochastic noise level

# -----------------------------
# INITIAL STATES
# -----------------------------
# Random initial population distribution on simplex
X = np.random.dirichlet(np.ones(n))
# Random fitness matrix (phenotype x candidate)
W_base = np.random.rand(n, p)

# -----------------------------
# FUNCTIONS
# -----------------------------
def softmax(x):
    ex = np.exp(x - np.max(x))
    return ex / ex.sum(axis=0)

def fitness(X, U):
    # Weighted fitness: W * U
    return X @ W_base @ U

def evolve(X, U):
    # Population update with stochastic noise
    W_effective = W_base @ U
    X_next = X * W_effective
    X_next = X_next / X_next.sum()  # normalize to simplex
    X_next += np.random.normal(0, noise_std, size=X.shape)
    X_next = np.clip(X_next, 0, None)
    X_next /= X_next.sum()  # renormalize
    return X_next

def signal(X):
    # Observable signal proportional to phenotype frequency
    return X

def choose_mate(S):
    # Softmax selection over candidate mates
    return softmax(alpha * S)

# -----------------------------
# SIMULATION
# -----------------------------
history_X = [X.copy()]
history_fitness = []

for t in range(T):
    S = signal(X)
    U = choose_mate(S)
    X = evolve(X, U)
    history_X.append(X.copy())
    history_fitness.append(fitness(X, U))

# -----------------------------
# RESULTS
# -----------------------------
history_X = np.array(history_X)
history_fitness = np.array(history_fitness)

print("Final phenotype distribution:", history_X[-1])
print("Mean fitness over time:", history_fitness)
