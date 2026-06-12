import numpy as np
from scipy.linalg import sqrtm, eigvalsh

# ==============================
# Basic Quantum Utilities
# ==============================

def random_density_matrix(n):
    """Generate a random valid density matrix."""
    A = np.random.randn(n, n) + 1j * np.random.randn(n, n)
    rho = A @ A.conj().T
    rho = rho / np.trace(rho)
    return rho


def von_neumann_entropy(rho):
    """S(ρ) = -Tr(ρ log ρ)"""
    vals = eigvalsh(rho)
    vals = np.clip(vals, 1e-12, 1.0)
    return -np.sum(vals * np.log(vals))


def trace_distance(rho, sigma):
    """D(ρ,σ) = 1/2 Tr|ρ-σ|"""
    diff = rho - sigma
    eigs = eigvalsh(diff.conj().T @ diff)
    return 0.5 * np.sum(np.sqrt(np.clip(eigs, 0, None)))


# ==============================
# Holographic Evolution Model
# ==============================

def random_kraus_ops(n, noise_level=0.05):
    """Generate simple CPTP-like Kraus operators."""
    K1 = np.eye(n) + noise_level * (np.random.randn(n, n))
    K2 = noise_level * (np.random.randn(n, n))

    # Normalize roughly to preserve trace
    Ks = [K1, K2]
    norm = sum([K.conj().T @ K for K in Ks])
    norm_inv = np.linalg.inv(norm + 1e-8 * np.eye(n))

    Ks = [K @ sqrtm(norm_inv) for K in Ks]
    return Ks


def apply_channel(rho, Ks):
    """Apply quantum channel: ρ -> Σ K ρ K†"""
    new_rho = sum(K @ rho @ K.conj().T for K in Ks)
    new_rho = (new_rho + new_rho.conj().T) / 2  # enforce Hermitian
    new_rho = new_rho / np.trace(new_rho)
    return new_rho


# ==============================
# Simulation Engine
# ==============================

def simulate(
    dim=4,
    steps=200,
    noise=0.05,
    tol=1e-6
):
    rho = random_density_matrix(dim)
    history_entropy = []
    history_dist = []

    for t in range(steps):
        Ks = random_kraus_ops(dim, noise_level=noise)
        rho_next = apply_channel(rho, Ks)

        # Observables
        S = von_neumann_entropy(rho)
        D = trace_distance(rho, rho_next)

        history_entropy.append(S)
        history_dist.append(D)

        print(f"t={t:03d} | S(ρ)={S:.6f} | TraceDist={D:.6e}")

        # Convergence check
        if D < tol:
            print("\n✅ Convergence achieved.")
            break

        rho = rho_next

    return rho, history_entropy, history_dist


# ==============================
# Run Simulation
# ==============================

if __name__ == "__main__":
    final_rho, entropy_hist, dist_hist = simulate(
        dim=6,
        steps=300,
        noise=0.03,
        tol=1e-7
    )

    print("\nFinal density matrix:")
    print(final_rho)

    print("\nFinal entropy:", entropy_hist[-1])
