# O1 certified min-plus DP for even n ∈ {8, 10} (strip, H_0(n) ≤ H < 2)

This is `../o1dp/SPEC.md` with the chain length n as a parameter. Everything in that file stays fixed (definitions of h, κ, roles, the displacement table, the three certified gap bounds, the DP with the Morandi flag, the refinement, gates 1–4 and the lemma gate). Read it fully first. Only the following changes.

## Parameters

- n ∈ {8, 10} (run both; keep n = 6 runnable as a regression and check it reproduces `../o1dp` slice values up to rounding, on three slices).
- Chain: Φ^σ(θ, H) = h(θ_1) + h(θ_n) + Σ_{i=1}^{n−1} κ(θ_i, θ_{i+1}, dy_i), σ ∈ {F, C}^n. The excluded patterns are the two alternating ones FCFC… and CFCF…; the flag f is set once two consecutive roles are equal, exactly as before.
- H range: [H_0(n), 2] with H_0(8) = 1.855 and H_0(10) = 1.850, stored as the binary64 predecessor as before. Reference: the heights where the Morandi width equals n are H*(8) = 1.852048 and H*(10) = 1.846936; at those heights the all-floor row ties the target, so the margin vanishes there and slices just above need to be narrow (start at width 0.001 near H_0). If a slice near H_0 does not close after refinement and H-bisection down to width 1e-4, stop there and report the lowest proved H; do not spend more than a quarter of the wall budget on the bottom 0.005 of the range.
- Everywhere the old spec says 1.87, read H_0(n); everywhere it says 6, read n; "five gaps" means n − 1 gaps. The near-upright pair lemma uses only H ≤ 2 and H > √2 and is unchanged.

## Target F_n: no closed form, certified by the chain itself

The reference width is F_n(H) = min_θ Φ_M(θ, H) for the alternating pattern σ_M = FCFC… at tilts θ = (0, φ, φ, …, φ, 0), all n − 2 middle tilts equal; numerically the minimum over φ equals Friedman's Morandi curve (reference values F_8(1.9) = 7.6670536343, F_8(1.95) = 7.3194018689, F_10(1.9) = 9.5247406413, F_10(1.95) = 9.0765365203, and F_n(2) = n − (n − 2)(3 − 2√2)). The DP needs only an upper bound per slice:

- Do not assume F_n is monotone in H (the first version of this spec claimed κ is even in dy by central symmetry; that is false, κ is the right boundary of Δ, and Codex's `math-check.py` records the counterexample). Instead bound F_n over the whole slice at once: F_n_ub(slice) := the upper end of an interval evaluation of Φ_M((0, φ0, …, φ0, 0), H) with H = [Ha, Hb] as an interval and φ0 a float near the numerical minimiser at the slice midpoint. Since F_n(H) ≤ Φ_M(θ0, H) for every H and every θ0, this bounds F_n(H) for every H in the slice. Upper-bound κ by: for each of the 8 normals with n_x > 0, compute an upper bound of (h_Δ(n) − dy·n_y)/n_x over the H-interval with every operation rounded up (dy = ±(H − h(θ_i) − h(θ_{i+1})) is an interval); take the minimum of these per-term upper bounds (valid because the term attaining the true κ at any given H contributes an upper bound of itself). Add h(0) + h(0) = 1 and the n − 1 gaps with upward rounding. The slice width costs about (n − 1)·w of margin (|∂Φ_M/∂H| ≈ n − 1 near the optimum), so keep slices narrow where the margin is small, exactly as the old spec says for n = 6. Gate 5: at 1000 random (n, slice, φ0) check F_n_ub ≥ the double-precision chain value at 50 sampled H in the slice, and that for a point slice F_n_ub − Φ_M ≤ 1e−12.
- Log F_n_ub per slice alongside D and the margin.

## Gates

Gates 1, 2, the lemma gate and gate 5 as above. Gate 3 (DP sanity) on the slices [H_0, H_0 + 0.005] and [1.9, 1.91] for each n: the unconstrained DP (no flag) must stay ≤ F_n_ub of the slice's right end and increase toward F_n(Hb) as cells refine; the flagged DP must stay ≤ the best non-alternating Φ found by random starts plus L-BFGS-B over θ ∈ [0, π/2]^n for ≥ 300 random non-alternating patterns (log the best pattern and value: expected near FFCFCFCF ≈ 7.995 at H = 1.862 for n = 8 and ≈ 10.000 at H = 1.857 for n = 10). Gate 4 with n-chains.

## Outputs and budget

- `o1n/src/` (reuse `../o1dp/src` by copying, not by import; the C kernel takes n at runtime), `o1n/gates-n8.log`, `o1n/gates-n10.log`, `o1n/run-n8.log`, `o1n/run-n10.log`, `o1n/certificate-n8.json`, `o1n/certificate-n10.json`, `o1n/README.md` (how to rerun, what is proved for each n with the exact proved H range, every assumption), and a `verify` mode that replays a certificate from its cell lists.
- At most 6 worker processes, memory under 2 GB, hard stop 6 hours wall time per n. Run n = 8 first, then n = 10. If not all slices close, report which and why.
