import numpy as np
from scipy.stats import entropy

# =========================
# 📌 ISCS SIMULATION MODEL
# =========================

class ISCS:
    def __init__(self, n=32, m=8, seed=42):
        np.random.seed(seed)
        
        # state: x_t ∈ {0,1}^n
        self.n = n
        self.x = np.random.randint(0, 2, n)
        
        # key: k_t
        self.k = np.random.randint(0, 256, n)
        
        # entropy state: e_t
        self.e = np.random.randn(m)
        
        # entropy injection strength
        self.sigma = 0.5

    # -------------------------
    # σ (nonlinear permutation)
    # -------------------------
    def sigma(self, x):
        # simple nonlinear mixing (proxy for S-box)
        x = np.roll(x, 1)
        x = np.bitwise_xor(x, np.random.randint(0, 2, len(x)))
        return x

    # -------------------------
    # entropy injection η_t
    # -------------------------
    def entropy_noise(self):
        return (np.random.randn(self.n) * self.sigma > 0).astype(int)

    # -------------------------
    # key update G_k
    # -------------------------
    def key_update(self, x):
        noise = np.random.randint(0, 3, self.n)
        self.k = (self.k + x + noise) % 256

    # -------------------------
    # cipher dynamic F
    # -------------------------
    def step(self):
        eta = self.entropy_noise()

        # x_{t+1} = σ(x ⊕ k ⊕ η)
        mixed = np.bitwise_xor(self.x, (self.k % 2))
        mixed = np.bitwise_xor(mixed, eta)

        self.x = self.sigma(mixed)

        # update key
        self.key_update(self.x)

        # update entropy state
        self.e = 0.9 * self.e + np.random.randn(len(self.e)) * 0.1

    # -------------------------
    # observation O_t
    # -------------------------
    def observe(self):
        # statistical signature
        p1 = np.mean(self.x)
        hist = np.bincount(self.x, minlength=2) / len(self.x)

        return {
            "bias": p1,
            "entropy": entropy(hist + 1e-9, base=2)
        }

# =========================
# 📊 KL divergence to uniform
# =========================

def kl_to_uniform(x):
    hist = np.bincount(x, minlength=2) / len(x)
    uniform = np.array([0.5, 0.5])
    return entropy(hist + 1e-12, uniform)

# =========================
# 🚀 RUN SIMULATION
# =========================

system = ISCS(n=64)

T = 200
kl_trace = []
entropy_trace = []

for t in range(T):
    system.step()
    
    obs = system.observe()
    
    kl = kl_to_uniform(system.x)
    kl_trace.append(kl)
    entropy_trace.append(obs["entropy"])

# =========================
# 📈 RESULTS
# =========================

print("Final KL divergence:", kl_trace[-1])
print("Final entropy:", entropy_trace[-1])

# simple trend check
print("KL trend (first -> last):", kl_trace[0], "->", kl_trace[-1])
