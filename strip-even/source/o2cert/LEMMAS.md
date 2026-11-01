# O2 via the r-space dual: the analytic part

Status 2026-10-31: the lemmas below are the analytic half of a proof of O2 (the Morandi-pattern inequality) for 1.87 ≤ H ≤ 2. They reduce O2 to (i) the corner certificate of the Open Math swarm (member m1, convex surrogate, radius 0.32) and (ii) one bounded certified computation on the box K defined in Lemma 9, which `SPEC.md` specifies. Lemmas 5–9 follow the blind referee's finding 14 (`docs/o2-routeA-review-codex-2026-10-31.md`); Lemmas 1–4 are the swarm's dual backbone, written out with proofs.

## 0. Objects

- h(t) = (cos t + sin t)/2 on [0, π/2]. S(t) = unit square centred at the origin rotated by t; edge normals e1 = (cos t, sin t), e2 = (−sin t, cos t); vertices ±(e1 + e2)/2 = ±(b, h), ±(e1 − e2)/2 = ±(h, −b) with b(t) = (cos t − sin t)/2. Support function h_{S(t)}(v) = (|v·e1| + |v·e2|)/2; in particular h_{S(t)}((0,1)) = h(t), h_{S(t)}((1,0)) = h(t).
- G(r, t) = h_{S(t)}((1, r)) = (|cos t + r sin t| + |sin t − r cos t|)/2.
- Chain function of the Morandi pattern FCFCFC: Φ_M(t; H) = h(t1) + h(t6) + Σ_{i=1}^{5} κ(t_i, t_{i+1}, dy_i), κ(t1, t2, dy) = max{x : (x, dy) ∈ S(t1) + S(t2)}, dy_i = s_i (H − h(t_i) − h(t_{i+1})), s = (+1, −1, +1, −1, +1).
- L(θ, H) = 2 + (4 − (3H − 2) cos θ)/sin θ + (4 − 2H sin θ)/cos θ, F6(H) = min_θ L(θ, H). F6(2) = 8√2 − 6. Morandi tilt θ*(H), m(H) = π/2 − θ*(H), T(H) = tan m(H) ∈ [0.8909, 1] for H ∈ [1.87, 2].
- O2: Φ_M(t; H) ≥ F6(H) for all t ∈ [0, π/2]^6, H ∈ [1.87, 2).

## 1. Support-function form of κ

**Lemma 1.** Let K ⊂ R² be compact convex with nonempty interior and y0 with K ∩ {y = y0} ≠ ∅. Then max{x : (x, y0) ∈ K} = inf_{r ∈ R} [h_K((1, r)) − r y0].

*Proof.* For (x, y0) ∈ K and any r, x + r y0 ≤ h_K((1, r)), so the max is ≤ the inf. Conversely let x* be the max and p = (x*, y0). Since K has interior, the line y = y0 either meets the interior of K or is its top or bottom. In the first case p has a supporting line with outward normal (n1, n2), n1 > 0 (n1 = 0 would make the line horizontal, but K has points above and below it), and r = n2/n1 gives equality. In the second case, say the top, h_K((1, r)) − r y0 = max_{q ∈ K} [q1 + r(q2 − y0)] ≥ x* for every r, and any maximising points q_r have q_{r,2} → y0 as r → +∞ (otherwise the value would tend to −∞), so by compactness their limit points lie on the top face and the value tends to at most x*. ∎

For κ: K = S(t1) + S(t2), h_K((1, r)) = G(r, t1) + G(r, t2), and |dy_i| = H − h(t_i) − h(t_{i+1}) ∈ [0, H − 1] ⊂ [0, 1] while the half-height of K is h(t_i) + h(t_{i+1}) ≥ 1, so the line meets K (its interior when |dy| < 1). Hence κ(t1, t2, dy) = inf_r [G(r, t1) + G(r, t2) − r dy]. Note dy_i has the sign s_i automatically because h(t_i) + h(t_{i+1}) ≤ √2 < 1.87 ≤ H; no constraint on t is dropped.

## 2. Separation

**Lemma 2.** Φ_M(t; H) = inf_{r ∈ R^5} Q(t, r; H) with Q = Σ_{j=1}^{6} w_j(t_j; r) + H σ(r), σ = −r1 + r2 − r3 + r4 − r5, and
w_1 = (1 + r1) h(t) + G(r1, t), w_2 = (r1 − r2) h(t) + G(r1, t) + G(r2, t), w_3 = (r3 − r2) h(t) + G(r2, t) + G(r3, t), w_4 = (r3 − r4) h(t) + G(r3, t) + G(r4, t), w_5 = (r5 − r4) h(t) + G(r4, t) + G(r5, t), w_6 = (1 + r5) h(t) + G(r5, t).
Consequently inf_t Φ_M(t; H) = inf_r Ψ(r; H), where
Ψ(r; H) = m1(r1) + m1(r5) + A(r1, r2) + A(r3, r2) + A(r3, r4) + A(r5, r4) + H σ(r),
m1(x) = min_{t ∈ [0, π/2]} [(1 + x) h(t) + G(x, t)], A(x, y) = min_{t ∈ [0, π/2]} [G(x, t) + G(y, t) + (x − y) h(t)].

*Proof.* Substitute Lemma 1 into each κ: −r_i dy_i = −s_i H r_i + s_i r_i (h(t_i) + h(t_{i+1})); the H parts sum to H σ(r), and collecting the coefficient of h(t_j) gives 1 + r1, r1 − r2, r3 − r2, r3 − r4, r5 − r4, 1 + r5. Infima over independent variables commute, and inf over t ∈ [0, π/2)^6 equals the min over the closed cube by continuity. ∎

So O2 follows from (R): Ψ(r; H) ≥ F6(H) for all r ∈ R^5 and H ∈ [1.87, 2]. Equality holds at r*(H) = (T, −1/T, T, −1/T, T) (polynomial identity, swarm m8; verified numerically to 1e-8).

## 3. The inner minima

**Lemma 3.** (a) The integrand φ_{x,y}(t) = [G(x, t) + x h(t)] + [G(y, t) − y h(t)] is ≥ 0, and between consecutive sign changes of the four absolute-value arguments it is of the form α cos t + β sin t, hence concave there. Its minimum over [0, π/2] is attained at an endpoint or at a sign change; the sign changes are tan t = x (x > 0), tan t = −1/x (x < 0), tan t = y (y > 0), tan t = −1/y (y < 0). At t = 0 and t = π/2 the value is E(x, y) = 1 + x⁺ + y⁻. Hence
A(x, y) = min over the candidate set {E} ∪ {φ(t_k) : t_k a sign change of x or y in (0, π/2)}.
At tan t = q > 0 one has (cos t, sin t) = (1, q)/√(1 + q²); at tan t = −1/q with q < 0, (cos t, sin t) = (−q, 1)/√(1 + q²).
(b) Likewise m1(x) = min over {1 + x⁺} ∪ {value at the sign change of x}, which gives m1(x) = 1 + x for x ≥ 0 and 1/√(1 + x²) for x < 0.
(c) Including extra candidate points can only lower a candidate minimum, so a kernel that includes a candidate whenever its defining sign condition may hold on a box produces a valid lower bound of A (and of m1).

*Proof.* Support inequalities with the vertices (b, h) and (−b, −h) of S(t): G(x, t) + x h ≥ (1, x)·(−b, −h) + x h = −b and G(y, t) − y h ≥ (1, y)·(b, h) − y h = b; so φ ≥ 0. On a sign-constant piece φ = α cos t + β sin t, φ'' = −φ ≤ 0. The rest is inspection; the values at 0 and π/2 are E because G(x, 0) = G(x, π/2) = (1 + |x|)/2 and h = 1/2 there. For m1 use (1 + x) h + G(x, t) ≥ h − b = sin t ≥ 0 and the same concavity. ∎

(The swarm's closed forms E, Kx±, Ky± in `proofs/m4-ushell/D2.md` are these candidate values written out.)

**Lemma 4.** A(x, y) ≥ 0 for all x, y, and A(x, y) ≥ x⁺ + y⁻ − 1. Also A(x, y) = A(−y, −x).

*Proof.* A ≥ 0 is Lemma 3(a). From the reverse triangle inequality G(r, t) ≥ (|r| − 1) h(t); hence φ ≥ 2(x⁺ + y⁻ − 1) h(t), which is ≥ x⁺ + y⁻ − 1 when x⁺ + y⁻ ≥ 1 (h ≥ 1/2); when x⁺ + y⁻ < 1 the right side is negative and A ≥ 0 suffices. The symmetry is t ↦ π/2 − t, under which G(r, t) ↦ G(−r, t) and h ↦ h. ∎

(Lemma 4 is only needed if the dichotomy of swarm member m2 is used. The reduction below does not use it.)

## 4. The flat orthant and the global deficit cap

Let F = {r : r1, r3, r5 ≥ 0, r2, r4 ≤ 0} and, for x ≥ 0 ≥ y, the pair deficit d(x, y) = E(x, y) − A(x, y) = (1 + x − y) − A(x, y) ≥ 0.

**Lemma 5 (E-identity).** On F, Ψ(r; H) = 6 + (2 − H)(−σ(r)) − [d(r1, r2) + d(r3, r2) + d(r3, r4) + d(r5, r4)], and −σ(r) = Σ |r_j| ≥ 0.

*Proof.* m1(r1) + m1(r5) = 2 + r1 + r5 and the four E's sum to 4 + r1 + 2r3 + r5 − 2r2 − 2r4; the total is 6 + 2(r1 + r3 + r5) − 2(r2 + r4) = 6 − 2σ. ∎

**Lemma 6 (global deficit cap).** For all x ≥ 0 and Y = −y ≥ 0: 0 ≤ d(x, −Y) ≤ d0 := 3 − 2√2 = 0.17157…, with equality iff x = Y = 1.

*Proof.* With R = √(1 + x²), the x-kink candidate (tan t = x) evaluates to Kx = [1 + 2x + 2x² + 2Y + xY + |1 − xY|]/(2R), so
dX := E − Kx = x²(x + Y − R)/(R(R + 1)) for xY ≤ 1 and dX = (1 + x + Y) − (x + Y)(1 + x)/R for xY ≥ 1.
For fixed x the first is affine in Y with slope x²/(R(R+1)) ≥ 0, the second affine with slope 1 − (1 + x)/R ≤ 0, and they agree at Y = 1/x. Hence sup_Y dX = dX(x, 1/x) = D(x) := 1 + w − √(w(w + 2)) with w = x + 1/x ≥ 2, using ((x + 1/x)(1 + x)/R)² = w²(1 + 2x/(1 + x²)) = w(w + 2). D(x) = 1/(1 + w + √(w(w + 2))) is decreasing in w, so D ≤ D|_{w=2} = 1/(3 + 2√2) = 3 − 2√2, with equality iff x = 1 (and then Y = 1/x = 1). By the symmetry A(x, y) = A(−y, −x) the y-kink candidate satisfies E − Ky ≤ D(Y) ≤ d0 as well. Since d = max(0, E − Kx, E − Ky) (Lemma 3: for x > 0 > y the only candidates are E and the two kinks; x = 0 or Y = 0 by continuity), d ≤ d0. ∎

**Corollary 6.1.** On F, Ψ(r; H) ≥ 6 − 4 d0 + (2 − H)(−σ) = F6(2) + (2 − H)(−σ(r)), because 6 − 4(3 − 2√2) = 8√2 − 6.

**Lemma 7 (tangent bound).** F6(H) ≤ L(π/4, H) = 4 + 8√2 − 5H = F6(2) + 5(2 − H) for every H.

*Proof.* F6 is a minimum over θ; evaluate L at θ = π/4. ∎

## 5. Clipping, the H = 2 endpoint, and the reduction to a box

**Lemma 8 (slopes).** (a) For x < 0 the map x ↦ G(x, t) + x h(t) is nondecreasing with slope in {0, sin t}, the value sin t occurring only when tan t < 1/|x|; hence its slope is ≤ 1/√(1 + x²). Therefore x ↦ A(x, y) (x < 0) is nondecreasing with slope ≤ 1/√(1 + x²), and m1'(x) = |x|/(1 + x²)^{3/2} ≤ 2/(3√3) < 0.385 for x < 0.
(b) For y > 0 the map y ↦ G(y, t) − y h(t) is nonincreasing with slope in {−cos t, 0}, the value −cos t occurring only when tan t > y; hence slope ≥ −1/√(1 + y²). Therefore y ↦ A(x, y) (y > 0) is nonincreasing with slope ≥ −1/√(1 + y²).
(A minimum over t of functions with slopes in an interval I has one-sided slopes in I.)

*Proof.* Differentiate: ∂_x [G + xh] = (sin t · sgn(cos t + x sin t) − cos t · sgn(sin t − x cos t))/2 + (cos t + sin t)/2. For x < 0, sin t − x cos t > 0 always, and cos t + x sin t > 0 iff tan t < 1/|x|; this gives sin t or 0, and sin t < 1/√(1 + x²) when tan t < 1/|x|. (b) is the same computation. ∎

**Lemma 9 (clipping).** Fix H ∈ [1.87, 2] and define P(r) by: r1 ↦ max(r1, 0), r5 ↦ max(r5, 0), r3 ↦ max(r3, −0.38), r2 ↦ min(r2, 0.38), r4 ↦ min(r4, 0.38). Then Ψ(P(r); H) ≤ Ψ(r; H). At H = 2 the same holds for the full clipping P0 (r3 ↦ max(r3, 0), r2 ↦ min(r2, 0), r4 ↦ min(r4, 0)), and P0(r) ∈ F.

*Proof.* Ψ depends on r3 through A(r3, r2) + A(r3, r4) − H r3, whose slope for r3 < 0 is ≤ 2/√(1 + r3²) − H by Lemma 8(a); for |r3| ≥ 0.38 and H ≥ 1.87 this is ≤ 2/√1.1444 − 1.87 < 0, so raising r3 to −0.38 does not increase Ψ. Ψ depends on r1 < 0 through m1(r1) + A(r1, r2) − H r1, slope ≤ 0.385 + 1 − 1.87 < 0, so raising r1 to 0 does not increase Ψ; same for r5. Ψ depends on r2 through A(r1, r2) + A(r3, r2) + H r2, slope ≥ −2/√(1 + r2²) + H > 0 for r2 ≥ 0.38, so lowering r2 to 0.38 does not increase Ψ; same for r4. At H = 2 the thresholds can be taken to be 0 (slopes ≤ 2 − 2 = 0, resp. ≥ 0). ∎

**Theorem 10 (H = 2).** Ψ(r; 2) ≥ F6(2) for all r ∈ R^5.

*Proof.* Ψ(r; 2) ≥ Ψ(P0(r); 2) ≥ F6(2) by Lemma 9 and Corollary 6.1 at H = 2. ∎

**Corollary 10.1.** For all r and H: Ψ(r; H) = Ψ(r; 2) + (2 − H)(−σ(r)) ≥ F6(2) + (2 − H)(−σ(r)). In particular, for H ≤ 2, if −σ(r) ≥ 5 then Ψ(r; H) ≥ F6(2) + 5(2 − H) ≥ F6(H) by Lemma 7.

**Theorem 11 (reduction to K).** Let K = [0, 6.14] × [−6.14, 0.38] × [−0.38, 6.14] × [−6.14, 0.38] × [0, 6.14]. If Ψ(r; H) ≥ F6(H) for all r ∈ K and all H ∈ [1.87, 2], then (R) holds, hence O2.

*Proof.* Given r and H, let q = P(r) (Lemma 9), so Ψ(r; H) ≥ Ψ(q; H), with q1, q5 ≥ 0, q2, q4 ≤ 0.38, q3 ≥ −0.38. If −σ(q) ≥ 5, Corollary 10.1 gives Ψ(q; H) ≥ F6(H). Otherwise −σ(q) = q1 + q3 + q5 − q2 − q4 < 5; the wrong-sign parts contribute at least −1.14 (three coordinates of magnitude ≤ 0.38), so every right-sign coordinate has magnitude < 5 + 1.14 = 6.14 and q ∈ K. ∎

## 6. What the computation must certify

By Theorem 11 and the swarm's corner certificate (member m1: Ψ(r; H) ≥ F6(H) whenever |r − r*(H)|_∞ ≤ 0.32, H ∈ [1.87, 2]), it suffices to certify

    Ψ(r; H) ≥ F6(H)   for all r ∈ K \ Π   and all H ∈ [1.87, 2],

where Π = Π_j (I_j + [−0.15, 0.15]) with I_1 = I_3 = I_5 = [0.890900, 1] ⊇ {T(H)}, I_2 = I_4 = [−1/0.890900, −1] ⊇ {−1/T(H)}; Π lies inside every corner ball since 0.15 + width(I_j) ≤ 0.2725 < 0.32. Boxes with min(−σ) ≥ 5 may be discarded by Corollary 10.1. `SPEC.md` specifies the kernel. The corner certificate itself is replayed separately (see `SPEC.md`, part B).

## 7. Numerical sanity checks performed (not proofs)

- max d over 20 000 log-uniform pairs 0.171266 < d0; d(1, −1) = d0 to 1e-16.
- F6'(H) = −(3T + 2/T) to 1e-6 at five H; F6(2) + 5(2 − H) − F6(H) ∈ [0, 0.0075] on [1.87, 2] (zero exactly at H = 2).

## 8. Referee record

Blind Codex review 2026-10-31 (`../docs/o2cert-review-codex-2026-10-31.md`): no MAJOR findings; verdict "O2 is certified on [1.87, 2] under the stated premises". Text repairs applied here afterwards: the intermediate sum in Lemma 5, the interior hypothesis and top/bottom limit in Lemma 1, the H ≤ 2 restriction in Corollary 10.1, and the sanity range in §7. The stored source hashes in `certificate.json` and `cells/*.json` were refreshed after these text-only edits (see `README.md`, provenance refresh).
- min over 3000 random r ∈ [−8, 8]^5 of Ψ(r; 2) − F6(2): +0.379; of Ψ(r; H) − [F6(2) + (2 − H)(−σ)]: +0.379.
- max Ψ(P(r); H) − Ψ(r; H) over 3000 random (r, H): 0 (never positive).
- min Ψ − F6 over 4000 samples of K \ F with −σ < 5 outside the ball: +0.52.
