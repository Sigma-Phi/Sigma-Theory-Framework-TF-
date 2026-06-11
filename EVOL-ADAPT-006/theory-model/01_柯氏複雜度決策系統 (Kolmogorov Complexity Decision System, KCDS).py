import zlib
import random
import math
import numpy as np

# =========================
# 1. Compression Proxy K(x)
# =========================
def compression_length(x: str) -> float:
    """
    MDL / Kolmogorov complexity proxy using zlib compression
    """
    if len(x) == 0:
        return 0
    compressed = zlib.compress(x.encode("utf-8"))
    return len(compressed)


def compression_ratio(x: str) -> float:
    if len(x) == 0:
        return 0
    return compression_length(x) / len(x)


# =========================
# 2. Noise Model η_t
# =========================
def noise_flip(x: str, p: float = 0.02) -> str:
    """
    sub-Gaussian-like noise approximation via bit flips
    """
    x_list = list(x)
    for i in range(len(x_list)):
        if random.random() < p:
            x_list[i] = '1' if x_list[i] == '0' else '0'
    return "".join(x_list)


# =========================
# 3. Algorithm Space A
# =========================
def identity(x): return x

def invert(x): 
    return "".join('1' if c == '0' else '0' for c in x)

def shuffle(x):
    x_list = list(x)
    random.shuffle(x_list)
    return "".join(x_list)

ALGORITHMS = [identity, invert, shuffle]


# =========================
# 4. Control Law G(S_t)
# =========================
def control_policy(x: str):
    """
    MDL minimization: choose algorithm that minimizes compression length
    """
    best_a = None
    best_score = float("inf")

    for a in ALGORITHMS:
        x_new = a(x)
        score = compression_length(x_new)

        if score < best_score:
            best_score = score
            best_a = a

    return best_a


# =========================
# 5. Dynamics F
# =========================
def transition(x: str, theta=None):
    """
    x_{t+1} = U_t(x_t) + η_t
    """
    U_t = control_policy(x)
    x_new = U_t(x)
    x_new = noise_flip(x_new, p=0.03)
    return x_new


# =========================
# 6. Lyapunov Function V(x)
# =========================
def V(x: str):
    return compression_length(x)


# =========================
# 7. Simulation Engine
# =========================
def run_kcds(x0: str, T: int = 50):
    x = x0

    history = []
    V_history = []

    for t in range(T):
        v = V(x)
        cr = compression_ratio(x)

        history.append(x)
        V_history.append(v)

        print(f"t={t:02d} | V(x)={v:4.0f} | CR={cr:.3f} | x={x[:40]}")

        x = transition(x)

    return history, V_history


# =========================
# 8. Generate Initial State
# =========================
def generate_initial_state(n=60):
    """
    mixture of structure + randomness
    """
    base = "01" * (n // 2)
    noise = "".join(random.choice("01") for _ in range(n // 3))
    return (base + noise)[:n]


# =========================
# 9. Run Experiment
# =========================
if __name__ == "__main__":
    x0 = generate_initial_state(80)
    run_kcds(x0, T=40)
