# From packings to chain functions: the reduction for n = 6, 1.87 ≤ H < 2

Status 2026-10-31 (revised after the blind referee pass recorded in `strip-n6-reduction-review-codex-2026-10-31.md`): this is the bridge between the geometry (a packing of six unit squares in an L × H rectangle) and the two certified inequalities O1 (`o1dp/`) and O2 (`o2cert/`). It replaces the swarm's Step 1–2 (`runs/openmath-2026-10-27/proof-F6.md` §1–2), which used separating lines and Rédei's theorem; the argument below only sorts centres by x. Everything here is elementary; the two certified computations carry the weight.

## 1. Setting

A packing is six closed unit squares S_1, …, S_6 with pairwise disjoint interiors, all contained in R = [0, L] × [0, H]. Square S_i has centre (X_i, Y_i) and tilt θ_i; rotating a square by π/2 gives the same square, so we may take θ_i ∈ [0, π/2) (this is a reduction modulo π/2 of the angle of one edge, not a reflection). Its axis-parallel half-extents are both h(θ_i) = (cos θ_i + sin θ_i)/2 ∈ [1/2, 1/√2] (the largest |x| and the largest |y| among its four centred vertices). Containment in R gives

    h(θ_i) ≤ X_i ≤ L − h(θ_i),   h(θ_i) ≤ Y_i ≤ H − h(θ_i).      (1)

Since 2h(θ_i) ≤ √2 < 1.87 ≤ H, each interval in (1) has positive length for every tilt; no feasibility constraint on the tilts is needed.

For two tilts let Δ(θ, θ') = S(θ) + S(θ') be the Minkowski sum of the two centred squares, a centrally symmetric convex polygon with at most eight sides. For a height dy such that the line y = dy meets Δ let

    κ(θ, θ', dy) = max{ x : (x, dy) ∈ Δ(θ, θ') }.

(`o1dp/SPEC.md` gives κ in closed form as a min over the eight facet normals with positive x-component; `o2cert/LEMMAS.md` Lemma 1 gives it as a support-function infimum. Both are this number.) Each centred unit square contains the closed disk of radius 1/2, so Δ contains the closed unit disk; in particular for |dy| < 1 the point (0, dy) lies in the interior of Δ and κ(θ, θ', dy) > 0.

## 2. The pair constraint

**Lemma 2.1.** Let S, S' be unit squares with tilts θ, θ', centres c, c', and disjoint interiors. If c'_x ≥ c_x and |c'_y − c_y| < 1, then c'_x − c_x ≥ κ(θ, θ', c'_y − c_y).

*Proof.* Two convex bodies have intersecting interiors iff the difference of their centres lies in the interior of S(θ) + (−S(θ')), and −S(θ') = S(θ') by central symmetry; so disjoint interiors means c' − c ∉ int Δ. Put dy = c'_y − c_y and dx = c'_x − c_x ≥ 0. Since |dy| < 1, (0, dy) is an interior point of Δ (§1), and (κ, dy) ∈ Δ. Every point of the half-open segment from an interior point to a point of a convex set is interior; hence if 0 ≤ dx < κ then (dx, dy) ∈ int Δ, a contradiction. ∎

In a packing with H < 2, (1) gives |Y_j − Y_i| ≤ H − h(θ_i) − h(θ_j) ≤ H − 1 < 1 for every pair, so the hypothesis of Lemma 2.1 holds for every pair. (The weaker bound |dy| < h(θ_i) + h(θ_j), which only says that the line y = dy meets Δ, would not suffice: a horizontal section of Δ need not contain x = 0.) In particular two squares of a packing never have the same centre x-coordinate.

## 3. The chain bound

Relabel the squares so that X_1 < X_2 < … < X_6. By (1) and Lemma 2.1 applied to consecutive pairs,

    L ≥ (X_6 + h(θ_6)) − (X_1 − h(θ_1)) = h(θ_1) + h(θ_6) + Σ_{i=1}^{5} (X_{i+1} − X_i)
      ≥ h(θ_1) + h(θ_6) + Σ_{i=1}^{5} κ(θ_i, θ_{i+1}, Y_{i+1} − Y_i) =: Φ_θ(Y).      (2)

## 4. Vertex reduction

**Lemma 4.1.** For fixed θ, θ', the function dy ↦ κ(θ, θ', dy) is concave on the interval of heights at which the line y = dy meets Δ.

*Proof.* If (x, y) and (x', y') lie in Δ and 0 ≤ λ ≤ 1, then (λx + (1−λ)x', λy + (1−λ)y') ∈ Δ by convexity, so κ(λy + (1−λ)y') ≥ λx + (1−λ)x'; take x = κ(y), x' = κ(y'). ∎

Fix the tilts θ of the packing. On the box B_θ = Π_i [h(θ_i), H − h(θ_i)] every difference Y_{i+1} − Y_i has absolute value at most H − 1 < 1, so Φ_θ is a sum of concave functions of linear maps and is concave on B_θ. Every point of a box is a convex combination of its vertices, so a concave function on a box is bounded below by its smallest vertex value. A vertex of B_θ is a choice, for each square, of Y_i = h(θ_i) (square on the floor, role F) or Y_i = H − h(θ_i) (square on the ceiling, role C). Writing σ ∈ {F, C}^6 for the role pattern and Φ^σ(θ, H) for Φ_θ at that vertex, we get: for the packing's own tilt vector θ there is a role pattern σ with

    L ≥ Φ^σ(θ, H).      (3)

(No claim is made that the vertex configuration is itself a packing; only a lower bound is being derived.)

At a vertex the displacements are dy_i = Y_{i+1} − Y_i with Y_i = h(θ_i) or H − h(θ_i), i.e. (F→F) h(θ_{i+1}) − h(θ_i), (F→C) H − h(θ_i) − h(θ_{i+1}), (C→F) h(θ_i) + h(θ_{i+1}) − H, (C→C) h(θ_i) − h(θ_{i+1}), where square i is the left one in centre-x order; this is the table in `o1dp/SPEC.md`. For the Morandi pattern FCFCFC it is dy_i = s_i (H − h(θ_i) − h(θ_{i+1})), s = (+, −, +, −, +), the chain function Φ_M of `o2cert/LEMMAS.md` Lemma 2.

## 5. The two certified inequalities

Let L(θ, H) = 2 + (4 − (3H − 2) cos θ)/sin θ + (4 − 2H sin θ)/cos θ for θ ∈ (0, π/2) and F6(H) = min_θ L(θ, H) (the minimum exists since L → +∞ at both ends). Since ∂L/∂H = −3 cot θ − 2 tan θ < 0, F6 is strictly decreasing in H. (The swarm's closed form F6(H) = b(a^{-1}(H)) and the uniqueness of the minimiser are in `proof-F6.md` §3.2; they are not needed for the lower bound.)

- **O1** (`o1dp/`, certified, independently refereed): for every H ∈ [1.87, 2) and every σ other than FCFCFC and CFCFCF, Φ^σ(θ, H) > F6(H) for all θ ∈ [0, π/2]^6.
- **O2** (`o2cert/`, certified, independently refereed): for every H ∈ [1.87, 2], Φ_M(θ, H) ≥ F6(H) for all θ ∈ [0, π/2]^6.

Both are stated on the closed tilt cube; since S(π/2) = S(0) and h(π/2) = h(0), the chain functions take the same values on the closed and the half-open cube.

**Lemma 5.1 (mirror pattern).** Φ^{CFCFCF}(θ, H) = Φ^{FCFCFC}(π/2 − θ, H), where π/2 − θ is taken coordinatewise.

*Proof.* Reflect the strip in the line y = H/2. Centre x-coordinates are unchanged, so the chain's index order is unchanged; a square of tilt θ_i becomes a square of tilt −θ_i, which is the same square as tilt π/2 − θ_i; h(π/2 − θ) = h(θ); floors become ceilings; and Δ(θ, θ') is reflected in the x-axis, so κ(π/2 − θ, π/2 − θ', −dy) = κ(θ, θ', dy). The displacements of the reflected configuration are the negatives of the originals, so the two chain values agree. ∎

## 6. The theorem

**Theorem.** For every H with 1.87 ≤ H < 2, every packing of six unit squares in a rectangle of width L and height H has L ≥ F6(H).

*Proof.* By (3), L ≥ Φ^σ(θ, H) for the packing's tilts θ and some role pattern σ. If σ is neither FCFCFC nor CFCFCF, O1 gives Φ^σ(θ, H) > F6(H). If σ = FCFCFC, O2 gives Φ^σ(θ, H) ≥ F6(H); if σ = CFCFCF, Lemma 5.1 and O2 give the same. ∎

The hypothesis H < 2 enters only through |dy| ≤ H − 1 < 1 in §2 (for H = 2 two upright squares stacked at vertical distance 1 have dx = 0 while the closed-section κ is 1, so the pair constraint fails there); H ≥ 1.87 enters only through the ranges of O1 and O2 and the remark after (1). The bound is attained by the Morandi configuration, a genuine packing of width L(θ*(H), H) = F6(H) (`proof-F6.md` §3.1), so F6(H) is the exact minimum width for these H; that sharpness statement rests on the construction, not on the reduction above.

## 7. Premises of the certified computations

- O1 (`o1dp/SPEC.md`, `o1dp/README.md`): κ is evaluated by the eight-normal closed form with three certified lower bounds per gap (plain interval, correlated ratio, near-upright pair lemma, the last proved in SPEC.md), combined by a min-plus dynamic program over tilt cells and H-slices; each slice certifies D > F6_ub, where F6_ub is an outward enclosure of L(θ0, Ha) at the slice's left endpoint, and F6 decreasing gives F6(H) ≤ F6(Ha) ≤ F6_ub on the slice. Interval arithmetic is outward-rounded with libm results padded as stated in SPEC.md. The closed form of κ was gated against the brute-force hull of `runs/openmath-2026-10-27/m4check.py`.
- O2 (`o2cert/LEMMAS.md`, `o2cert/SPEC.md`, `o2cert/README.md`): the dual function Ψ(r; H) of Lemma 2 there; the reduction of Ψ ≥ F6 to the box K (Lemmas 5–11); the swarm's corner certificate (member m1 of swarm smvuml416, a convex surrogate with nine interval scans, replayed with directed rounding in `o2cert/src/corner_impl`, whose analytic identities are a premise); and the box computation of `o2cert/certificate.json`, where every outer rectangle certifies Ψ > L(θ0, H) ≥ F6(H) at both endpoints of its H-cell with an affine-in-H argument. The kernel uses outward rounding with an 8-ulp libm premise for cos, sin and sqrt. Both referee reports are in `docs/`.
