"""Constants for docs/slab-lower-bound.md (Theorem S and its corollaries).

Theorem S:  L - |A| <= W/delta + C1*W/tau + sqrt(C2*tau*M*L*W)
for 0 < delta <= 2/5, 0 < tau <= 0.08 and 0.502*M*tau^2 <= delta'.

With W = kappa*L/sqrt(M) and |A| <= a*L this reads
    1 - a <= kappa/(delta*sqrt(M)) + C1*kappa/(tau*sqrt(M)) + sqrt(C2*tau*sqrt(M)*kappa).
The script checks, on a grid of M, that the stated kappa makes the right side
smaller than the left side, i.e. that W = kappa*L/sqrt(M) is impossible.  The
right side is increasing in kappa, so every smaller waste is impossible too.

Run:  python3 -I tools/slab_constants.py
"""
import math

C1 = 1350.0
C2 = 21.0
TAU0 = 0.08


def geometry_constants():
    """Recompute the counts behind C1 and C2 for delta <= 2/5."""
    d = 0.4
    r2 = math.sqrt(2.0)
    rho = r2 + d  # largest distance of the centres of consecutive squares

    def nbhd(a, b):  # area of the sqrt(2)-neighbourhood of an a x b rectangle
        return a * b + 2 * r2 * (a + b) + 2 * math.pi

    m_prime = math.floor(nbhd(1.0, rho)) - 2
    c_fl = (2 - math.pi / 4) / (4 * (m_prime + 1))
    reach = math.hypot(rho, 0.5) + r2 / 2
    k_sq = math.floor(math.pi * reach**2)
    k_floor = math.floor((1 + r2) * (r2 / 2 + d + r2 / 2)) * r2
    k_tot = k_sq + k_floor
    pairs = math.floor(nbhd(math.sin(TAU0), 1 + d)) - 1 + 1
    s_tau = (1 / math.tan(TAU0) - math.tan(TAU0)) * TAU0  # s_tau * tau at tau0
    return m_prime, c_fl, k_tot, k_tot / c_fl, pairs, 2 * pairs / s_tau


def tau_for(M, dprime):
    return min(TAU0, math.sqrt(dprime / (0.502 * M)))


def rhs(kappa, M, delta, dprime):
    tau = tau_for(M, dprime)
    assert 0.502 * M * tau * tau <= dprime * (1 + 1e-12)
    sM = math.sqrt(M)
    return kappa / (delta * sM) + C1 * kappa / (tau * sM) + math.sqrt(C2 * tau * sM * kappa)


def worst(kappa, delta, dprime, a, Ms):
    return max(rhs(kappa, M, delta, dprime) - (1 - a) for M in Ms)


def main():
    mp, cfl, k, c1, pairs, c2 = geometry_constants()
    print(f"m' <= {mp}, c_FL >= {cfl:.5f}, K <= {k:.2f}, K/c_FL = {c1:.0f} (C1 = {C1:.0f})")
    print(f"pairs per square <= {pairs}, 2*pairs/(s_tau*tau) = {c2:.2f} (C2 = {C2:.0f})")
    assert c1 <= C1 and c2 <= C2

    grid = [1 + 0.01 * i for i in range(0, 1200)] + [13 * 1.01**i for i in range(0, 4000)]

    # Corollary 1: sloped ceiling, rise >= 1, delta = delta' = 1/24.
    d = 1 / 24
    a = 2 * d * (2 + 2 * d)
    print(f"Cor 1: |A|/L <= {a:.4f}")
    w = worst(4e-5, d, d, a, grid)
    print(f"  kappa = 4e-5, all M >= 1:  max(rhs - lhs) = {w:.4f}")
    assert w < 0
    w = worst(1.5e-4, d, d, a, [M for M in grid if M >= 13])
    print(f"  kappa = 1.5e-4, M >= 13:   max(rhs - lhs) = {w:.4f}")
    assert w < 0

    # Corollary 2(a): flat ceiling at height m + 1/2, delta = delta' = 2/5, A empty.
    d = 0.4
    w = worst(5e-4, d, d, 0.0, [M for M in grid if M >= 125])
    print(f"Cor 2: kappa = 5e-4, M >= 125: max(rhs - lhs) = {w:.4f}")
    assert w < 0

    # Corollary 2(b): height M with fractional part f, delta = min(f, 0.8)/2, delta' = (1 - f)/2.
    worst_ratio = float("inf")
    for i in range(1, 400):
        f = i / 400
        d, dp = min(f, 0.8) / 2, (1 - f) / 2
        for j in range(0, 150):
            M = 1.1**j
            tau = tau_for(M, dp)
            lo, hi = 0.0, 10.0  # least W/L allowed by Theorem S, by bisection
            for _ in range(200):
                mid = (lo + hi) / 2
                if mid / d + C1 * mid / tau + math.sqrt(C2 * tau * M * mid) < 1:
                    lo = mid
                else:
                    hi = mid
            worst_ratio = min(worst_ratio, lo / min(f, math.sqrt((1 - f) / M)))
    print(f"Cor 2(b): least (W/L)/min(f, sqrt((1-f)/M)) on the grid = {worst_ratio:.2e} (claimed 5e-5)")
    assert worst_ratio > 5e-5
    print("ok")


if __name__ == "__main__":
    main()
