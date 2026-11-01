# O2 certified computation on the box K (n = 6 strip, 1.87 ≤ H ≤ 2)

Goal (part A): a certified computation proving

    Ψ(r; H) ≥ F6(H)   for all r ∈ K \ Π and all H ∈ [1.87, 2],

with Ψ, K, Π as in `LEMMAS.md` §6. Part B: a replay of the swarm's corner certificate with directed rounding. Everything below is fixed by design. Do not change the mathematics; if something looks wrong, stop and say so in the report. Model the code organisation on `../o1dp` (C kernel with directed rounding, Python driver, `certificate.json`, `verify` and `report` modes, loud gates).

## Definitions (from LEMMAS.md)

- h(t) = (cos t + sin t)/2; G(r, t) = (|cos t + r sin t| + |sin t − r cos t|)/2.
- φ_{x,y}(t) = G(x, t) + G(y, t) + (x − y) h(t);  A(x, y) = min_{t ∈ [0, π/2]} φ_{x,y}(t).
- ψ_x(t) = (1 + x) h(t) + G(x, t);  m1(x) = min_t ψ_x(t) = 1 + x (x ≥ 0), 1/√(1 + x²) (x < 0).
- Ψ(r; H) = m1(r1) + m1(r5) + A(r1, r2) + A(r3, r2) + A(r3, r4) + A(r5, r4) + H σ, σ = −r1 + r2 − r3 + r4 − r5.
- Split, with x = r1, y = r2, z = r3, w = r4, u = r5:
  B1(x; y, H) = m1(x) + A(x, y) − H x,  B2(z; y, w, H) = A(z, y) + A(z, w) − H z,  B3(u; w, H) = m1(u) + A(u, w) − H u,
  Ψ = B1 + B2 + B3 + H (y + w).
- L(θ, H) = 2 + (4 − (3H − 2) cos θ)/sin θ + (4 − 2H sin θ)/cos θ; F6(H) = min_θ L(θ, H) ≤ L(θ0, H) for every θ0.
- K = [0, 6.14] × [−6.14, 0.38] × [−0.38, 6.14] × [−6.14, 0.38] × [0, 6.14]  (coordinates x, y, z, w, u).
- Π = Π_j (I_j + [−0.15, 0.15]), I_1 = I_3 = I_5 = [0.890900, 1], I_2 = I_4 = [−1/0.890900, −1]. Store the exclusion intervals J_j = I_j ± 0.15 as binary64 numbers rounded INWARD (so that the excluded set is a subset of Π): J_odd = [0.740900 rounded up, 1.15 rounded down], J_even = [−1/0.890900 − 0.15 rounded up, −0.85 rounded down].
- Reference implementations for gates: `A`, `m1`, `Psi` by dense sampling plus local refinement, and the hull κ of `../runs/openmath-2026-10-27/m4check.py` through the dual of LEMMAS.md Lemma 1 (see `../o1dp/README.md` for how `m4check` must be imported: exec only its first 29 lines).

## Certified lower bounds (C kernel, every operation outward-rounded)

Interval arithmetic in binary64 with fesetround or explicit nextafter padding (as in `../o1dp/src/kernel.c`): every arithmetic operation that feeds a lower bound rounds down, every one that feeds an upper bound rounds up; sqrt, and libm cos/sin where used, padded by at least 2 ulps outward. Intervals must always satisfy lo ≤ hi; assert it.

### Candidate evaluation on a box

For an interval pair (X, Y) (x-interval X, y-interval Y) a lower bound of A over X × Y:

1. E_lb = 1 + max(X.lo, 0) + max(−Y.hi, 0), rounded down.
2. Kink candidates. For a parameter interval Q (either X or Y) the sign change tan t = q exists for q > 0 and tan t = −1/q for q < 0. For the "positive kink" of Q (if Q.hi > 0): the direction (cos t, sin t) = (1, q)/√(1 + q²) with q ranging over Q⁺ = Q ∩ [0, ∞); evaluate φ at that direction in interval arithmetic with x ∈ X, y ∈ Y and q ∈ Q⁺ treated as an independent interval (this is a valid enclosure of the candidate values because the true candidate value is φ(t_k(q)) at q = x or q = y, a point of the enclosure). For the "negative kink" (if Q.lo < 0): (cos t, sin t) = (−q, 1)/√(1 + q²), q ∈ Q⁻ = Q ∩ (−∞, 0]. Each kink candidate's lower bound is the lower end of the interval evaluation of
   φ = [|c + x s| + |s − x c| + x (c + s) + |c + y s| + |s − y c| − y (c + s)]/2,
   with c, s intervals; |·| of an interval containing 0 is [0, max(|lo|, |hi|)].
3. A_lb(X, Y) = min(E_lb, kink candidates present). Including a kink whose sign condition may hold on the box is required; including one that cannot hold is allowed (Lemma 3(c)).
4. The same for m1 over X: candidates 1 + max(X.lo, 0) and, if X.lo < 0, the negative kink value of ψ, i.e. the interval evaluation of [(1 + x)(c + s) + |c + x s| + |s − x c|]/2 at (c, s) = (−q, 1)/√(1 + q²), q ∈ X⁻; the known closed form 1/√(1 + q²) may be used instead for that candidate (it is the same number). m1_lb(X) = min of the present candidates.

### Centred (mean-value) form

Plain interval bounds lose O(width) and cannot close near H = 2 where B1, B3 are nearly flat over wide x-ranges. Also implement for each of A and m1 a centred form:
   f(p) ≥ f(p0) − Σ_i D_i · hw_i,
where p0 is the box midpoint (f(p0) evaluated as an interval, lower end taken), hw_i the half-widths, and D_i an upper bound of |∂f/∂p_i| over the box. For f = A = min of candidates: a valid D_i is the max over the candidates present on the box of an upper bound of |∂ candidate / ∂p_i| over the box, where each candidate's derivative is enclosed by interval AD through its formula, enclosing the derivative of |v| as the hull of ±1 when v's interval contains 0. (Justification: a minimum of locally Lipschitz functions is locally Lipschitz with the hull of their gradients as a Clarke subdifferential; the mean-value inequality then holds. Write this argument in a comment.) Use lb = max(plain, centred).
A simpler alternative that is also valid and may be used instead of AD: the integrand's slope in x is one of {0, sin t} for x < 0 (Lemma 8) and one of {sin t, cos t + sin t} for x > 0, so |∂A/∂x| ≤ √2 globally, and by the symmetry A(x, y) = A(−y, −x) also |∂A/∂y| ≤ √2; |m1'| ≤ 1. Then D_x = D_y = √2 (rounded up) is a valid Lipschitz bound. Use the AD bound where it is sharper, otherwise the constant √2. Whatever is used, gate G2 must test the centred form on boxes that contain kinks.

### Lower bound of B1, B2, B3 on an outer box

Outer boxes are rectangles Y × W in the (y, w) plane. For a given outer box and a given H endpoint (a single binary64 number H_e):
- B1_lb(Y, H_e) = certified lower bound of min_{x ∈ [0, 6.14], y ∈ Y} [m1(x) + A(x, y) − H_e x], computed by a 1-D best-first branch-and-bound over x (y stays the interval Y), each x-box bounded by max(plain, centred). Stop refining when the lower bound of the whole x-range is within tol_inner of its best upper bound (upper bound: evaluate at box midpoints with upward rounding), or return what you have; the lower bound is valid at any stage. Record the number of x-boxes used.
- B3_lb(W, H_e) likewise over u ∈ [0, 6.14].
- B2_lb(Y, W, H_e) over z ∈ [−0.38, 6.14] with both y ∈ Y and w ∈ W as intervals.
- Exclusion Π. The excluded set is a product, so a point is excluded only if ALL FIVE coordinates lie in their J's. If the outer box Y × W lies inside J_2 × J_4, the inner problem is the minimum over (x, z, u) ∈ [0, 6.14]³ \ J_odd³, which is the union of the three sets {x ∉ J_odd}, {z ∉ J_odd}, {u ∉ J_odd}; certify each separately: for {x ∉ J_odd}, B1 over the two pieces [0, J_odd.lo] and [J_odd.hi, 6.14] (take the smaller of the two lower bounds) plus B2 and B3 over their full ranges; similarly for z and u. If the outer box is not inside J_2 × J_4, no exclusion applies to the inner ranges. An outer box that straddles the boundary of J_2 × J_4 is split until it is inside or outside, unless it is certified without exclusion first.
- Full inner ranges must be exactly [0, 6.14], [−0.38, 6.14] as binary64 numbers rounded OUTWARD (6.14 rounded up, −0.38 rounded down); the excluded pieces use the inward-rounded J.

### H handling (exact, no curvature constants)

For fixed r, Ψ(r; H) is affine in H and L(θ0, H) is affine in H, so Ψ − L(θ0, ·) is affine in H and its minimum over an H-cell [Ha, Hb] is at an endpoint. For a box (outer box with inner ranges) the certified statement is: for both endpoints H_e ∈ {Ha, Hb},
    B1_lb(Y, H_e) + B2_lb(Y, W, H_e) + B3_lb(W, H_e) + H_e · (Y.lo + W.lo) (rounded down)  >  L_ub(θ0, H_e),
where L_ub is L(θ0, H_e) evaluated with every operation rounded up. If that holds at both endpoints then Ψ(r; H) > L(θ0, H) ≥ F6(H) for every r in the box and every H in the cell. (Justification: at each H_e the left side lower-bounds min over the box of Ψ(·; H_e); a function affine in H that is positive at both endpoints is positive in between. Write this in a comment.)
Choose θ0 per H-cell as the binary64 nearest to the minimiser of L(·, H_mid) (any θ0 is valid; this one makes the loss L(θ0, H) − F6(H) small). H-cells: start with 8 equal cells of [1.87, 2]; store endpoints as binary64 with the first lower endpoint ≤ 1.87 and the last upper endpoint ≥ 2 (round outward). Split an H-cell in two when it fails to close with a reasonable box budget. The multiplication H_e · (Y.lo + W.lo): both Y.lo + W.lo and H_e may be negative; use proper interval multiplication rounded down.
Discard rule (Corollary 10.1): if the lower bound of −σ over the box ≥ 5, the box is certified without evaluation; for an outer box Y × W with inner ranges, min(−σ) = min x + min z + min u − Y.hi − W.hi. Record such discards separately.

### Outer branch-and-bound

Best-first over outer rectangles Y × W ⊂ [−6.14, 0.38]², splitting the longer side; a rectangle is certified when the H-cell test above passes for all its (inner-range) pieces. Give each H-cell its own run and its own record. Report per H-cell: number of outer boxes, inner boxes, discards, minimum certified margin (left minus right at the worse endpoint), wall time. The certificate (`certificate.json`) stores per H-cell: Ha, Hb, θ0, L_ub at both endpoints, the list of certified outer rectangles with their margins (or a hash of the list plus the count, with the full list in a separate file), tolerances, and kernel build hash. `verify` mode replays every outer rectangle with the stored H-cell data and checks the inequality again (same kernel, from the stored list, no search).

### Gates (must be run and logged before the main run; all random, zero violations required)

- G1 (candidates): 200 000 random (x, y) ∈ [−8, 8]²: A_lb([x,x],[y,y]) ≤ A_ref(x, y) ≤ A_lb + 1e-9 and the same for m1; A_ref by dense sampling (20 001 points) plus refinement. Also 2 000 random triples (t1, t2, dy) with |dy| ≤ 0.9: inf_r [G(r,t1)+G(r,t2) − r dy] (sampled over r plus the kink r-values) vs hull κ from m4check, agreement to 1e-9.
- G2 (box soundness): 100 000 random boxes X × Y of widths 1e-8..2 inside [−8, 8]²: A_lb(X, Y) ≤ A at 20 random points of the box; same for the centred form; same for m1. Half of the boxes must straddle a sign change (contain 0 in x or y, or contain xy = −1).
- G3 (Ψ soundness): 20 000 random outer boxes and H endpoints: the certified Ψ lower bound ≤ Ψ_ref at 10 random (x, y, z, w, u) points of the box with H = H_e, where Ψ_ref uses A_ref, m1 closed form.
- G4 (identity): Ψ_ref(r*(H); H) = F6(H) to 1e-8 at H ∈ {1.87, 1.9, 1.95, 1.99, 2} with r* = (T, −1/T, T, −1/T, T), T = tan(π/2 − θ*(H)); and L(θ0, H) ≥ F6(H) for the θ0 of each H-cell at 50 random H in the cell.
- G5 (exclusion geometry): for 10 000 random H ∈ [1.87, 2], the product of the J_j (as stored) lies inside the sup-ball of radius 0.32 around r*(H); and J_j ⊂ I_j ± 0.15.

## Part B: corner replay

The corner certificate (swarm member m1; files in `../runs/openmath-2026-10-27/handoff-routeA/` once unpacked, `proofs/m1-corner/{PROOF.md, run_corner.py, iv.py, a7.py, sym_check.py}`) proves Ψ ≥ F6 on |r − r*(H)|_∞ ≤ 0.32 via a convex surrogate and nine 1-D/2-D interval scans A1–A9 over 52 H-cells, all with margins ≥ 0.02. Do the following, in order of priority:
1. Read PROOF.md and iv.py and report whether iv.py is outward-rounded in every operation that feeds a scan margin, and whether run_corner.py's final assembly of the scan margins is directed. List every operation that is not.
2. If the non-directed operations are few, add to this project a Python replay `src/corner_replay.py` that re-implements the nine scans with an interval class that rounds outward everywhere (nextafter padding on every operation; abs/sqrt/min/max handled correctly), reproduces the 52 H-cells, and reports the nine minimum margins; a margin loss of order 1e-12 against m1's numbers is expected and must be reported.
3. If porting is not feasible within the budget, instead write a precise list of the non-directed operations and a bound on the total rounding error of the assembly (operation count × ulp × magnitude), to be subtracted from the reported margins, and say so plainly.

## Deliverables

- `src/kernel.c`, `src/driver.py` (modes: gates, run, verify, report), `src/corner_replay.py` (or the part-B note), `certificate.json` (+ box lists), `gates.log`, `run.log`, `verification.log`, `README.md` (implementer's report: what was built, what was run, every number, every deviation from this spec, what remains open). Keep `../o1dp/README.md` as the model for the report.
- Do not touch anything outside `o2cert/`. Do not run git commands. Do not modify `LEMMAS.md` or `SPEC.md`; put disagreements in `README.md` under "Issues with the spec".
- Budget: the main run may take hours; run it in chunks per H-cell, checkpointing `certificate.json` after every cell so that a partial run is still a certificate for the cells it covers. Use all cores (one process per H-cell is fine).
