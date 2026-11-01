# O1 certified min-plus DP (n = 6 strip, 1.87 ≤ H < 2)

Goal: a certified computation proving, for every H in [1.87, 2),

    min over role patterns σ ∈ {F, C}^6 \ {FCFCFC, CFCFCF} and tilts θ ∈ [0, π/2)^6 of Φ^σ(θ, H)  >  F6(H).

Everything below is fixed by design. Do not change the mathematics; if something in it looks wrong, stop and say so in the report.

## Definitions

- S(t): unit square centred at the origin, rotated by t. Edge normals u_t = (cos t, sin t), v_t = (−sin t, cos t).
- h(t) = (cos t + sin t)/2 for t ∈ [0, π/2]: half-extent of S(t) in x and in y.
- Support function of S(t): h_S(t)(n) = (|n·u_t| + |n·v_t|)/2.
- Δ = S(t1) + S(t2) (Minkowski sum). Its facet normals lie among the 8 unit vectors ±u_{t1}, ±v_{t1}, ±u_{t2}, ±v_{t2}, and h_Δ(n) = h_S(t1)(n) + h_S(t2)(n).
- κ(t1, t2, dy) = max{x : (x, dy) ∈ Δ} = min over those 8 normals n with n_x > 0 of (h_Δ(n) − dy·n_y)/n_x.
  This is valid whenever the line y = dy meets Δ, and in fact (0, dy) ∈ Δ for every dy used here: Δ contains the vertical segment x = 0, |y| ≤ b1 + b2 with b_i = 1/(2 max(cos t_i, sin t_i)) ≥ 1/2, and every |dy| below is ≤ 1. Hence every numerator h_Δ(n) − dy·n_y is ≥ 0 and κ ≥ 0.
- Roles: F (floor) has centre height y = h(t); C (ceiling) has y = H − h(t). For consecutive squares (r, t) → (r', t'), dy = y' − y:
  F→F: h(t') − h(t);  F→C: H − h(t') − h(t);  C→F: h(t') + h(t) − H;  C→C: h(t) − h(t').
- Chain: Φ^σ(θ, H) = h(θ1) + h(θ6) + Σ_{i=1..5} κ(θ_i, θ_{i+1}, dy_i(σ_i, σ_{i+1}, θ_i, θ_{i+1}, H)).
  (By the vertex reduction already proved, every packing of 6 unit squares in L × H has L ≥ min over σ, θ of Φ^σ.)
- F6(H) = min_θ L(θ, H) with L(θ, H) = 2 + (4 − (3H − 2)cos θ)/sin θ + (4 − 2H sin θ)/cos θ. F6 is decreasing in H. Reference: F6(1.87) = 5.956225297, F6(1.90) = 5.808611110, F6(1.93) = 5.660765767, F6(1.96) = 5.512539066, F6(1.99) = 5.363615071, F6(2−) = 8√2 − 6.
- Important check of conventions: the unconstrained minimum (all 64 patterns) of Φ is at most F6(H), attained by the Morandi pattern at equal tilts; that it equals F6(H) is the content of O2 (open), so treat equality below as an expectation used for sanity checks, not a premise. Independently checked: at H = 1.87 with σ = FCFCFC and θ = (0, φ, φ, φ, φ, 0), φ = π/2 − arcsin(0.746653759), Φ = F6(1.87) to 1e−14. The reference point implementation of κ is `kappa()` in `../runs/openmath-2026-10-27/m4check.py` (brute-force hull of the 16 vertex sums).

## Certified bounds (all in interval arithmetic with outward rounding)

Cells: a list of tilt intervals covering [0, π/2] (non-uniform allowed). H-slices: intervals [Ha, Hb] covering [1.87, 2] (include 2 itself; it only makes bounds more conservative. The statement being certified is for H < 2: at H = 2 exactly upright squares stack with |dy| = 1, where the closed-section κ no longer equals the packing constraint; see README "Scope at H = 2").

- Per cell: enclosures of cos t, sin t, h(t). Use correct handling of extrema inside the cell (cos/sin are monotone on [0, π/2], so this is just endpoint evaluation, but pad libm results outward by a few ulps).
- Gap lower bound G(r, r', cell c, cell c', slice): for each of the 8 signed normals n, as functions of the cell intervals:
  if n_x.hi ≤ 0, skip; otherwise term_lb = max(0, num.lo) / n_x.hi when n_x.lo ≤ 0 or num.lo ≤ 0, else num.lo / n_x.hi (num = h_Δ(n) − dy·n_y as an interval). G = max(0, min over non-skipped terms of term_lb).
  Justification: at any point of the box, κ is the min over normals with n_x > 0, each such term is ≥ its term_lb, and num ≥ 0 holds pointwise. Write this argument in a comment.
  Optional tightening (only if it passes the same gates): mean-value / centred form per term using derivative enclosures.
- Correlated ratio bound (addendum, needed near H = 2). The plain term bound takes num.lo and n_x.hi at different corners; for near-upright squares near H = 2 both vanish together at t_k = 0 or π/2, so it collapses to 0 although the true ratio stays near 1. For each eligible normal owned by square k (u_k with n_x = cos t_k, or −v_k with n_x = sin t_k), also compute:
  - e = the end of cell k where n_x is smallest (left end a_k for −v_k, right end b_k for u_k); x = |t_k − e| ∈ [0, w_k].
  - c = upper bound of n_x(e) (0 if e is 0 or π/2 exactly). Since |d n_x/dt| ≤ 1, n_x(t) ≤ c + x.
  - A = lower bound of N on the face t_k = e (the other tilt over its cell, H over the slice), and a = max(A, 0). This is valid because N(e) ≥ A and N(e) ≥ 0 pointwise (interiority).
  - B = lower bound over the whole box of the one-sided derivative of N in the direction away from e (∂N/∂t_k for −v_k, −∂N/∂t_k for u_k), where N = h_Δ(n) − dy·n_y. Use generalized derivatives for |sin δ| in h_Δ (enclose both one-sided derivatives at δ = 0). The derivative involves d h_Δ/dt_k, d dy/dt_k (through h(t_k) for the role) and d n_y/dt_k.
  - Mean value: N(t) ≥ a + x·B, so term ≥ (a + xB)/(c + x) ≥ min(a/c, B) if c > 0, and ≥ B if c = 0 (then a/x ≥ 0).
  Use term_lb = max(plain term_lb, ratio bound, 0). Comment the argument in code. Gate 2 must be rerun with the new bound, with at least half the boxes concentrated near t = 0, t = π/2 and H ∈ [1.999, 2].
- Near-upright pair lemma (addendum 2, needed for the slice closed at H = 2). The ratio bound is 1-D in the owner tilt and fails when BOTH tilts sit at the same corner: for C→F at t = t' = 0, H = 2 the face value a and the derivative bound B are both 0. The following 2-D lemma is proved below; implement it as a third candidate, term_lb = max(plain, ratio, lemma, 0), and nothing else changes.

  **Lemma.** Let 0 < W ≤ 1 and H ∈ [1.87, 2].
  (a) C→F edge with both tilts t, t' ∈ [0, W]. For each −v normal (owner tilt t_k, n = (sin t_k, −cos t_k)) and every point with sin t_k > 0: N/n_x ≥ 1 − 3W/4 − W²/4.
  (b) F→C edge with both tilts t, t' ∈ [π/2 − W, π/2]. For each u normal (n = (cos t_k, sin t_k)) and every point with cos t_k > 0: the same bound.
  The bound does not depend on H or on where inside [0, W] the cells sit.

  **Proof of (a).** Write t = t_k (owner), t1 = the other tilt, δ = t − t1, m = max(t, t1). Since n is a facet normal of S(t), h_S(t)(n) = 1/2; and n·u_{t1} = sin δ, n·v_{t1} = −cos δ, so h_S(t1)(n) = (|sin δ| + cos δ)/2. With n_y = −cos t and dy = h(t) + h(t1) − H,
      N = 1/2 + (|sin δ| + cos δ)/2 + dy·cos t.
  dy ≤ √2 − H < 0 and 0 < cos t ≤ 1 give dy·cos t ≥ dy. For x ∈ [0, 1]: sin x ≥ x − x³/6 and cos x ≥ 1 − x²/2, hence cos x + sin x ≥ 1 + x − x²/2 − x³/6; also |sin δ| ≥ |δ| − |δ|³/6 and cos δ ≥ 1 − δ²/2. Therefore
      N ≥ (2 − H) + (|δ| + t + t1)/2 − [ δ²/4 + |δ|³/12 + (t² + t1²)/4 + (t³ + t1³)/12 ].
  Now (|δ| + t + t1)/2 = m, and 0 ≤ t, t1 ≤ m gives |δ| ≤ m, so the bracket is ≤ 3m²/4 + m³/4 ≤ m(3W/4 + W²/4). With 2 − H ≥ 0: N ≥ m(1 − 3W/4 − W²/4). Finally n_x = sin t ≤ t ≤ m, and sin t > 0 forces m > 0, so N/n_x ≥ N/m ≥ 1 − 3W/4 − W²/4. ∎

  **Proof of (b).** Put s = π/2 − t, s1 = π/2 − t1 ∈ [0, W]. Then n = (sin s, cos s), n_x = sin s ≤ s, n_y = cos s ∈ (0, 1]; dy = H − h(t) − h(t1) ≥ 1.87 − √2 > 0, so −dy·n_y ≥ −dy; h_S(t)(n) = 1/2; n·u_{t1} = cos(t − t1), n·v_{t1} = sin(t − t1), so h_S(t1)(n) = (cos δ + |sin δ|)/2 with |δ| = |s − s1|. Since h(π/2 − x) = h(x), −dy = (cos s + sin s)/2 + (cos s1 + sin s1)/2 − H. This is (a) with (s, s1) in place of (t, t1). ∎

  **Implementation.** In g(): for the C→F gap (the call with dy = h(b) + h(a) − H) and sine normals only, if a.b ≤ 1 and b.b ≤ 1, set W = max(a.b, b.b) and lemma = 1 − 3W/4 − W²/4 computed with every operation rounded down (round 3W/4 and W²/4 up, the subtractions down). For the F→C gap (dy = H − h(b) − h(a)) and cosine normals only, if a.a ≥ π/2 − 1 and b.a ≥ π/2 − 1, set W = up(nextafter(M_PI_2, +∞) − min(a.a, b.a)) and the same formula. Everywhere else lemma = 0. The lemma uses only H ≤ 2 and H > √2 (for the sign of dy); both hold on every slice, including the first one, whose stored lower endpoint is the binary64 predecessor of 1.87.

  **Gates for the lemma.** (i) Pointwise lemma gate: 200 000 random triples (t, t1, H) with t, t1 ∈ [0, W] for random W ∈ (0, 1] and H ∈ [1.87, 2] (a quarter of them with H = 2 exactly, a quarter with W ≤ 1e−3): compute the exact term (sup − dy·n_y)/n_x for the two −v normals of the C→F edge and check ≥ 1 − 3W/4 − W²/4; mirror for F→C at π/2 with the two u normals. Zero violations. (ii) Gate 2 rerun with at least half the boxes having both cells inside [0, 0.3] or inside [π/2 − 0.3, π/2], half of those with H = 2 in the slice, widths 1e−8..0.3. Zero violations. (iii) Gate 4 rerun.
- Target: F6_ub(slice) = certified upper bound of L(θ0, Ha) for one float θ0 near the minimiser at Ha (F6 is decreasing, so F6(H) ≤ F6(Ha) ≤ L(θ0, Ha) for all H in the slice).

## DP

State (position i, role r, cell c, flag f), f = 1 once the pattern has two equal consecutive roles (i.e. it has left the Morandi orbit; FCFCFC and CFCFCF are exactly the patterns that never set f).
V_1(r, c, 0) = h_lb(c); V_{i+1}(r', c', f ∨ [r = r']) = min over (r, c, f) of V_i(r, c, f) + G(r, r', c, c', slice).
Certified value: D = min over (r, c) of V_6(r, c, 1) + h_lb(c). The slice is proved when D > F6_ub(slice). Accumulate in a way that only rounds down (e.g. nextafter toward −∞ after each add).
Memory: do not store full N×N tables if N is large; recompute G on the fly per pass (precompute per-cell trig enclosures).

Note on slice width: the proof criterion D > F6_ub(Ha) is sound (for every H in the slice, F6(H) ≤ F6(Ha)), but D can only approach the non-Morandi minimum over the slice, which sits near Hb, while the target is taken at Ha. Since |F6'| ≈ 5 on this range, a slice of width w costs about 5w of margin. The non-Morandi margin is only ≈ 0.044 near H = 1.87, so slices there must be narrow (start at width 0.002 near 1.87; wider is fine where the margin is larger).

## Refinement

Forward values V and backward values W (same recursion from the right end). A cell c at position i is "binding" if min over states of V_i + W_i − (overlap of the shared term) < F6_ub. Bisect every binding cell, recompute, repeat. If a slice stalls (no progress over several rounds), bisect the H-slice. Start from ~200 uniform cells and H-slices of width 0.01; adapt.

## Gates (must pass before the full run, results logged to o1dp/gates.log)

1. Point κ: compare the closed form with the brute-force hull (m4check.kappa) at 100 000 random (t1, t2, dy) with |dy| ≤ 1: max error ≤ 1e−11.
2. Box soundness: 50 000 random cell pairs of widths 1e−4..0.3, each with random role pair and H-slice; sample 64 interior points; G must be ≤ every sampled exact κ. Zero violations.
3. DP sanity: (a) unconstrained DP (no flag) is a lower bound for min over H in the slice of the unconstrained minimum, which is expected to be F6(Hb) (equality is O2, open; it is at most F6(Hb)) (F6 is decreasing, so the slice minimum sits at its right end); it must stay ≤ F6(Hb) and increase toward it as cells refine (log the sequence at H-slice [1.87, 1.875], and also at a point slice [1.87, 1.87] where the limit is F6(1.87)); (b) flagged DP value ≤ the best sampled non-Morandi Φ found by random/local search on that slice; (c) at H ≈ 1.87 the flagged minimum should approach 6 (the all-upright row) from below.
4. End-to-end: random full chains (σ, θ, H) evaluated exactly vs the DP bound at their cells: never exceeded.

## Implementation

- C (clang, -O2) for the kernels and DP; a small Python driver for slicing, logging and gates. No new heavy dependencies; numpy/scipy are in ../.venv.
- Parallelise over H-slices with processes, at most 6 workers; keep memory under ~2 GB total (the machine has 16 GB shared with other services).
- Outputs: o1dp/src/, o1dp/gates.log, o1dp/run.log (one line per slice: Ha, Hb, cells, rounds, D, F6_ub, margin, seconds), o1dp/certificate.json (final cell lists per slice), o1dp/README.md (how to rerun, what is proved, every assumption).
- Hard stop: 8 hours of wall time for the full run. If not all slices close, report which and why.
