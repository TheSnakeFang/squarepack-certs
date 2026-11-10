# Wedge lower bound: a trapezoid of length L and rise R wastes ≥ c·√(LR) at any width (draft v0.4, 2026-11-09)

Status: a claimed proof of Bui's Conjecture 1 (arXiv:2508.04603, §6.3), written in one session on 2026-11-09 after
the slab note (`docs/slab-lower-bound.md`, cited as [S]). **Refereed twice, blind, by AI referees of two model
families, then judged by three further blind AI judges (Codex; scopes Sections 1–4, Sections 5–8, and [S]), none
of whom found a fatal error; the gaps they found are repaired in v0.4. Not read by a person. Treat as
unverified**; Section 9 says what has and has not been checked. The proof of Theorem B uses Lemma 2.2 and
Corollary 2.3 of [S] (the fundamental lemma) and nothing else from [S]; Section 8 also uses [S, Corollaries 1, 2(b)].

## 0. Statement

Let w ≥ 0, 0 < ζ ≤ 1, L > 0, g(x) = w + ζx and Ω = {(x, y) : 0 ≤ x ≤ L, 0 ≤ y ≤ g(x)}. Put R = ζL (the rise). A
packing is a finite set of closed unit squares in Ω with pairwise disjoint interiors, and W = area(Ω) − number of
squares.

**Theorem B.** If R ≥ 1, every packing of Ω has W ≥ 7·10⁻⁶·√(LR).

In Bui's notation (height x = L, difference of the bases x^{1−γ} = R, 0 < γ < 1) this is his Conjecture 1: the
waste is ≥ c·x^{1−γ/2}, for every width. Theorem S of [S] gave L/√M for thickness M, which is larger for thin
regions (M < L/R) and smaller for thick ones. Consequences are in Section 8.

**Proposition 7.1** is the quantitative form: for 0 < τ ≤ 0.08, if 4250·W + 1350·W/τ + 0.01 ≤ L/4, then
0.47·R ≤ 21300·τ·W.

## 1. Conventions

As in [S, §1]: orientation φ_Z ∈ (−π/4, π/4], inclination a(Z) = |φ_Z|, θ(·,·) the distance of orientations in
ℝ/(π/2)ℤ, the floor and the two side walls have orientation 0. For a(Z) < π/4, u_Z = (cos φ_Z, sin φ_Z),
n_Z = (−sin φ_Z, cos φ_Z), Z = {P_Z + s·u_Z + t·n_Z : 0 ≤ s, t ≤ 1}, bottom side t = 0, top side t = 1, lateral
sides s = 0, 1. ζ′ = arctan ζ ≤ π/4.

Fix δ = 1/32 and τ ∈ (0, 0.08]. A square is *flat* if a(Z) < τ, *steep* otherwise. Two flat squares have
θ(Z, Z′) = |φ_Z − φ_Z′| < 2τ ≤ 0.16.

[S, Cor. 2.3]: if two squares have centres at distance ≤ √2 + 2/5, or one square has its centre within that
distance of the floor, the waste in the rectangle R(S₁, S₂) is ≥ θ(S₁, S₂)/50, and R(S₁, S₂) lies within 1.9 of the
centre of S₁.

*Side walls.* [S, Lemma 2.2] treats the floor; the same proof gives the right wall, because the horizontal segment
from any point of Ω to the right wall lies in Ω (g is increasing) and every square lies to the left of the wall. So
for a square S with centre (x_c, y_c), R(S, right wall) = [x_c, L] × [y_c − ½, y_c + ½] ⊂ Ω carries waste
≥ a(S)/50 when L − x_c ≤ √2 + 2/5. For the left wall, R(S, left wall) = [0, x_c] × [y_c − ½, y_c + ½] lies in Ω
exactly when y_c + ½ ≤ w, and then the same holds. The squares for which it fails and which can emit towards the
left wall within length δ are at most two: such a flat square has its top left vertex at x ≤ δ·sin τ, so
x_c ∈ [0.5, 0.55], and w − ½ < y_c ≤ w − ½ + 1.1·ζ because its top right vertex is under the ceiling; centres are at
distance ≥ 1.

## 2. The flow

*Emitters.* The floor F emits from the points e = (x, 0), 0 < x < L, in the direction n_F = (0, 1). A flat square Z
emits from the points e_Z(s) = P_Z + s·u_Z + n_Z of its top side, 0 < s < 1, in the direction n_Z.

*Probes.* For an emitter point e with direction n let r*(e) ≥ 0 be the least r such that e + r·n lies on the
ceiling, on a side wall, or in a square other than the emitting one. The *probe* of e is the segment
σ(e) = {e + r·n : 0 ≤ r ≤ min(r*(e), δ)}. Its points other than the two ends lie in the waste. An emitter point is
*conflicted* if its probe meets the probe of a point of a different emitter.

*Paths.* The path of x ∈ (0, L) starts at e = (x, 0) with G = 0, N = 0 and repeats:

1. If e is conflicted: **conflict death**.
2. If G + r*(e) > δ: travel δ − G along the probe and stop: **gap death**. Otherwise travel to q = e + r*(e)·n
   and add r*(e) to G.
3. If q is a vertex of a square: x is *exceptional*.
4. If q is on the ceiling and in no square other than the emitting one: **arrival**. If q is on a side wall and in
   no square other than the emitting one: **wall death**.
5. If q is in a steep square: **tilt death**.
6. If q is in the relative interior of a lateral side of a flat square: **lateral death**.
7. Otherwise q is in the relative interior of the bottom side of a flat square Z′. Cross Z′ along the segment from
   q to q + n_Z′, put N := N + 1, and continue from the emitter point e := q + n_Z′ of Z′.

Step 7 covers all remaining cases: a ray with direction n, entering a flat square Z′ with |angle(n, n_Z′)| < 0.16,
enters through a side whose outward normal ν has n·ν ≤ 0, that is the bottom side or a lateral side; and if
r* = 0 for an emitter point e of Z in the relative interior of a side of Z′, the two squares lie on opposite sides
of a common line, so that side is the bottom side of Z′ and Z′ is parallel to Z. All directions have a positive
y-component, so heights strictly increase.

*Termination.* Height increase alone does not stop a path from returning to a square. For a flat Z, a top-side
point P_Z + s·u_Z + n_Z is higher than a bottom-side point P_Z + s′·u_Z by cos φ_Z + (s − s′)·sin φ_Z
≥ cos φ_Z − |sin φ_Z| > 0, so every top-side point is higher than every bottom-side point. A path that has crossed
Z is at a point of its top side and then rises, so it never again reaches the bottom side of Z; a later hit of Z
in a lateral side stops it (step 6), a vertex makes x exceptional, and the top side cannot be entered (its outward
normal n_Z has positive product with every direction of travel, these being within 0.16 of n_Z). So each completed
step 7 uses a new square, there are at most n of them (n the number of squares), and the construction ends.

The only difference from the flow of [S] is that a path keeps the direction of the square it has just left while
it is in a gap, instead of moving vertically. This is Ryu's rule (k2-minus-c-quarter, §3). It is what makes
lateral deaths cheap (Lemma 4.3): in [S] they cost the tilt of the square that is hit, here they cost the tilt
*difference* of two neighbouring squares, which the fundamental lemma charges to the waste. The price is that
probes of different squares can cross; conflicted points are simply removed (Lemma 4.4).

Notation for a path that has crossed Z₁, …, Z_j: φ_i = φ_{Z_i}; γ₀ is the length travelled from the floor to Z₁ and
γ_i the length travelled after leaving Z_i; θ_{0,1} = a(Z₁) and θ_{i−1,i} = θ(Z_{i−1}, Z_i).

## 3. Structure of the flow

**Lemma 3.1.**
(a) There is a finite set E ⊂ (0, L), containing the exceptional x, such that on each interval of (0, L) ∖ E the
    itinerary (squares, sides, kind of ending) is constant. Besides the exceptional points, E contains the points
    where an emitter point on the path enters or leaves the conflicted set, and the end points of the sets where
    G + r* = δ (that equality can hold on a whole interval, on which the path then continues). Below, "interval
    of constant itinerary" and the arriving intervals J_k refer to this partition.
(b) On such an interval, the lateral coordinate s_j of the path in Z_j is an affine function of x with slope
    κ_j = Π_{i ≤ j} sec θ_{i−1,i} ≥ 1, and each γ_i is affine in x.
(c) After crossing Z₁, …, Z_j and travelling γ_j, the path is at height γ₀ + Σ_{i ≤ j} (1 + γ_i)·cos φ_i. In
    particular the bottom entry into Z_i is at height h_i = γ₀ + Σ_{l < i} (1 + γ_l)·cos φ_l, the crossing of Z_i
    occupies the heights H_i = [h_i, h_i + cos φ_i], and an arriving path that crossed N squares ends at the
    ceiling point of abscissa x′ with

        g(x′) = N − D + G̃,   D = Σ_i (1 − cos φ_i),   G̃ = γ₀ + Σ_i γ_i·cos φ_i ∈ [0, δ].        (3.1)

(d) On an interval of arriving x, x′ is affine in x with slope κ′ = κ_N·cos ζ′/cos(φ_N − ζ′) ≥ cos ζ′ (κ′ = 1 if
    N = 0). Hence N and D are constant there and G̃ is affine with slope ζκ′ ≥ sin ζ′ ≥ ζ/√2.

Proof. (a) *Probe regions are polygons.* Fix an emitter (the floor, with parameter x ∈ (0, L), or a flat square,
with parameter s ∈ (0, 1)); its points lie on a line and its direction n is fixed and transverse to it. For each
side of a square, the ceiling and each wall, the distance along n from e(s) to that line is affine in s, and
whether the hit point lies in the side segment is a linear inequality in s. Cutting the parameter interval at the
finitely many points where these inequalities switch or two candidate distances cross, or a distance crosses δ,
r*(e(s)) and min(r*, δ) become affine on each piece. On a piece I with min(r*, δ) = α + βs the union of the probes
is the image of the polygon {(s, r) : s ∈ I, 0 ≤ r ≤ α + βs} under the invertible affine map (s, r) ↦ e(s) + r·n.
So the probe region of every emitter is a finite union of convex polygons (possibly degenerate). For a piece I of
one emitter and a convex polygon Q of another, the set of s ∈ I whose probe meets Q is the projection to the s-axis
of the convex polygon {(s, r) : s ∈ I, 0 ≤ r ≤ α + βs, e(s) + r·n ∈ Q}, an interval. Hence the conflicted set of
each emitter is a finite union of intervals, and each emitter's parameter interval splits into finitely many
intervals on which conflict status, the object hit, the side hit and the formula for min(r*, δ) are fixed.
*Induction.* By the termination argument a path makes at most n crossings. Suppose the itinerary up to the k-th
emitter is constant on an interval of x. There the emitter parameter is affine and strictly increasing in x
((b), slope κ ≥ 1) and G is affine, so pulling back the finitely many cut points of that emitter, and the set where
the affine function G + r* equals δ (one point or a whole subinterval, whose end points are cut), gives finitely
many cuts. A vertex v is met by the probe of at most one point of each emitter line (n is transverse to it), so by
at most one x per interval. After at most n + 1 stages, E is finite. (b) A displacement Δs·u_{Z_{i−1}} of the emitter
point moves the hit point on the line of the bottom side of Z_i by Δs′·u_{Z_i} = Δs·u_{Z_{i−1}} + c·n_{Z_{i−1}}; taking
the product with u_{Z_{i−1}} gives Δs′·cos θ_{i−1,i} = Δs. For the floor, Δs′·cos φ₁ = Δx. The distance between two
lines along a fixed direction is affine. (c) Crossing Z_i adds cos φ_i to the height and travelling γ_i along
n_{Z_i} adds γ_i·cos φ_i; G̃ ≤ Σγ ≤ δ. (d) A displacement Δs·u_{Z_N} moves the ceiling point by
(Δx′, ζΔx′) = Δs·u_{Z_N} + c·n_{Z_N}, so Δx′·(cos φ_N + ζ sin φ_N) = Δs, and
cos φ_N + ζ sin φ_N = cos(φ_N − ζ′)/cos ζ′. Then differentiate (3.1). ∎

**Lemma 3.2 (disjoint and ordered).** The paths of two distinct non-exceptional points do not meet. If x₁ < x₂,
then at every height reached by both paths the first is to the left of the second. In particular x ↦ x′ is
increasing on the set of arriving x.

Proof. Every probe piece travelled by a path belongs to a non-conflicted probe (steps 1, 2). Let c be a common
point of two paths of least height.

* c interior to a square Z: both paths cross Z along the segment through c parallel to n_Z; its lower end is common.
* c in no square and not on the floor: c lies on a travelled probe of each path, beyond its emitter point. The two
  probes meet, so they belong to the same emitter, are parallel, hence equal; the emitter point is common and lower.
* c on the boundary of a square, not on the floor. A path reaches c at the end of a probe of positive length, and
  then the points of the path just before c are in the waste; or as the upper end of a crossing of a flat square Z,
  with c in the relative interior of the top side of Z, and then the points just before c are interior to Z. If
  both paths come by probes, the probes are equal as before. If both come by crossings, the two squares have c in
  the relative interior of their top sides and lie below lines through c whose normals differ by less than 0.16,
  so they overlap unless they are the same square; then the crossings are equal. One probe and one crossing is
  impossible: the probe has direction n with n·n_Z > 0, so its points just before c would be interior to Z.
  In all cases there is a lower common point.
* c on the floor: it is the starting point of both.

So the two paths start at the same point. Each path is a graph over the heights it reaches, because every piece
has a direction with positive y-component; two disjoint graphs keep their order. On the ceiling, which is
increasing, the order of the end points is the order of their abscissas: if x₁′ ≥ x₂′, the first path would at
height g(x₂′) be at an abscissa < x₂′, where the ceiling is lower than g(x₂′). ∎

**Lemma 3.3 (density).** For a flat square Z the set of x whose path crosses Z has measure ≤ 1. For any square S
the set of x whose path reaches S directly from the floor has measure ≤ √2.

Proof. By Lemma 3.1(b) the map x ↦ s is affine with slope ≥ 1 on each interval of constant itinerary, and by
Lemma 3.2 the images of different intervals in (0, 1) are disjoint. The second statement is the horizontal extent
of S. ∎

## 4. Deaths

Let B be the set of non-exceptional x that do not arrive.

**Lemma 4.1 (gap deaths).** Their measure is ≤ W/δ.

Proof. Such a path has travelled probe pieces of total length δ. Travelled pieces of different paths are disjoint
(Lemma 3.2) and lie in the waste. A family of paths of x-measure dx in a gap after Z_j has width κ_j·dx ≥ dx
perpendicular to its direction, so the area swept is ≥ δ times the measure. ∎

**Lemma 4.2 (tilt deaths).** Their measure is ≤ 1350·W/τ.

Proof. Let T be the set of such x. The chain floor, Z₁, …, Z_j, Z* of x ∈ T has consecutive members joined by a
probe of length ≤ δ; the probe runs from a point of the top side of one square to a point of the next, each within
√2/2 of the centre, so consecutive centres are within √2 + δ, and Z₁ has its centre at height ≤ √2/2 + δ. So
[S, Cor. 2.3] applies to every consecutive pair (it holds for squares of any inclination, Z* included), and by the
triangle inequality Σθ ≥ θ(floor, Z*) = a(Z*) ≥ τ along the chain. For an ordered pair (S, S′) let μ(S, S′) be
the measure of the x ∈ T whose chain contains S, S′ consecutively. Integrating over T,

    τ·|T| ≤ Σ_{(S,S′)} μ(S, S′)·θ(S, S′) ≤ 50 ∫_waste Σ_{(S,S′) : p ∈ R(S,S′)} μ(S, S′) dp.

Fix p. If S is a square, it is a flat square crossed by the paths concerned; each such path has one successor of S,
so the sets for different S′ are disjoint and Σ_{S′} μ(S, S′) ≤ 1 by Lemma 3.3. If p ∈ R(S, S′) then p is within
1.9 of the centre of S, so S ⊂ B(p, 1.9 + √2/2), a disc of area 21.35… < 22; the squares have disjoint interiors,
so there are at most 21 such S. If S is the floor, R(S′, floor) = [x₁ − ½, x₁ + ½] × [0, y₁] with (x₁, y₁) the
centre of S′ and y₁ ≤ √2/2 + δ, so S′ lies in the box [p_x − ½ − √2/2, p_x + ½ + √2/2] × [0, √2 + δ], of area
(1 + √2)(√2 + δ) < 3.49 < 4: at most 4 such S′ (in fact 3), each with μ(floor, S′) ≤ √2 by Lemma 3.3. The inner sum
is ≤ 21 + 4√2, and τ·|T| ≤ 50·W·(21 + 4√2) < 1333·W ≤ 1350·W. ∎

**Lemma 4.3 (lateral and wall deaths).** Let Z₁ be a flat square or the floor and Z₂ a flat square. The emitter
points of Z₁ whose probe ends in the relative interior of a lateral side of Z₂ form a set of measure
≤ 2δ·tan θ(Z₁, Z₂). The emitter points of a flat square Z whose probe ends on a given side wall form a set of
measure ≤ δ·tan a(Z).

Proof. Use the frame (s, t) of Z₂, in which the lateral side is {s = 0, 0 < t < 1} (or s = 1). In it the direction
of the probes of Z₁ is (∓sin θ, cos θ), θ = θ(Z₁, Z₂), and the emitter points of Z₁ lie on a line that makes the
angle θ with the s-axis. A probe of length ≤ δ changes s by at most δ·sin θ, so an emitter point whose probe ends
on {s = 0} has |s| ≤ δ·sin θ; if θ = 0 no probe ends in the relative interior of the side. The emitter line meets
the strip |s| ≤ δ sin θ, on the side from which the lateral side can be reached, in a segment of length
≤ δ·sin θ/cos θ. There are two lateral sides. The wall is the same computation with the wall as the line s = 0
and θ = a(Z). ∎

**Lemma 4.4 (conflicts).** Floor points are never conflicted with points of squares. For two distinct flat squares
Z₁, Z₂, the set of s with e_{Z₁}(s) conflicted with some point of Z₂ has measure ≤ 4.3·δ·θ(Z₁, Z₂).

Proof. Probes from the floor stay below height δ, and every point of the top side of a flat square in Ω has height
≥ cos τ − sin τ > 0.9. For the squares, use the frame (s, t) of Z₂ = [0, 1]². All probes of Z₂ lie in
B₂ = [0, 1] × [1, 1 + δ]. Let θ = θ(Z₁, Z₂); if θ = 0 put ε = 0 below. In the frame, n_{Z₁} = (−ε sin θ, cos θ)
with ε = ±1. Let e = (s⁰, t⁰) be an emitter point of Z₁ whose probe contains a point c = e + r·n_{Z₁} of B₂,
0 ≤ r ≤ δ. Then 1 − δ ≤ t⁰ ≤ 1 + δ. The segment from e to e − n_{Z₁} is the crossing of Z₁ below e; its points other
than the ends are interior to Z₁, so none of them is in (0, 1)².

* t⁰ < 1. Then e ∉ (0,1) × (0, 1), and t⁰ > 0, so s⁰ ∉ (0, 1): say s⁰ ≤ 0 (the case s⁰ ≥ 1 is symmetric). The probe
  reaches s ≥ 0 within length δ, so |s⁰| ≤ δ·sin θ.
* t⁰ ≥ 1 and s⁰ ∉ (0, 1): as before, s⁰ is within δ·sin θ of 0 or of 1.
* t⁰ ≥ 1 and 0 < s⁰ < 1. For small η > 0 the point e − r′·n_{Z₁} with r′ = (t⁰ − 1)/cos θ + η < 1 is interior to Z₁
  and has 0 < t < 1, so its s-coordinate s⁰ + ε·r′·sin θ is not in (0, 1). Hence s⁰ is within r′·sin θ of 0 or of 1;
  letting η → 0, within δ·tan θ.

So s⁰ lies in [−δ sin θ, δ tan θ] ∪ [1 − δ tan θ, 1 + δ sin θ], two intervals of total length ≤ 4δ·tan θ. The top
side of Z₁ makes the angle θ with the s-axis, so the set of such e has length ≤ 4δ·tan θ/cos θ ≤ 4.3·δ·θ for
θ ≤ 0.16. (For θ = 0 the set is empty.) ∎

**Corollary 4.5.** The measure of the set B of non-arriving x is at most W/δ + 1350·W/τ + 134000·δ·W + 0.01. With δ = 1/32 this is
≤ 4250·W + 1350·W/τ + 0.01.

Proof. Gap and tilt deaths are Lemmas 4.1, 4.2. A lateral or conflict death happens at an emitter point of some
Z₁ because of some flat Z₂ at distance ≤ 2δ from Z₁ (δ for a lateral death; for a conflict the two probes meet at a
point within δ of each square), so that the centres are within √2 + 2δ < √2 + 2/5; by Lemma 3.3 (and
Lemma 3.1(b) for the floor) the measure of the x concerned is at most the measure of the emitter points, which is
≤ (2.02 + 4.3)·δ·θ(Z₁, Z₂) for an ordered pair of flat squares, ≤ 2.02·δ·a(Z₂) for the floor and Z₂, and
≤ 1.01·δ·a(Z) for Z and a wall. By [S, Cor. 2.3] each θ is at most 50 times the waste in the corresponding
rectangle. A point p of the waste lies in R(Z₁, Z₂) only if both squares lie in B(p, 2.61), which holds for at most
21 squares, hence for at most 420 ordered pairs; in R(Z₂, floor) for at most 4 squares; and in R(Z, wall) for at
most 4 squares per wall. The two exceptional squares at the left wall (Section 1) add ≤ 2·1.01·δ·tan τ < 0.01.
In total 50·δ·W·(6.32·420 + 2.02·4 + 1.01·8) + 0.01 ≤ 134000·δ·W + 0.01. ∎

## 5. The sideways lemma

Let J₁, …, J_K be the intervals of arriving x, from left to right (Lemma 3.1(a)); J_k = (a_k, b_k). For 1 ≤ k < K
choose arriving points x_k^− ∈ J_k and x_k^+ ∈ J_{k+1} with x_k^− < x_k^+, and such that x_{k}^+ < x_{k+1}^−. Let λ_k and ρ_k
be their paths. The *tube* T_k is the set of points (x, y) with λ_k(y) ≤ x ≤ ρ_k(y), over the heights y reached by
both paths. By Lemma 3.2 tubes with different k have disjoint interiors.

Write Z_i and Z_i′ for the i-th squares of λ_k and ρ_k, N and N′ for their numbers, H_i and H_i′ for the height
intervals of the crossings (Lemma 3.1(c)), θ_i = θ(Z_i, Z_i′) for i ≤ min(N, N′), and Y_i = H_i ∩ H_i′. All of these
depend on k; N, N′, the squares and θ_i depend only on the two intervals, not on the chosen points.

**Lemma 5.1.** Σ_k Σ_{i ≤ min(N, N′)} θ_i·|Y_i| ≤ 14851·W.

Proof. Fix a height y. For each k there is at most one i with y ∈ Y_i (the H_i of one path are disjoint up to end
points). For such k and i, the horizontal segment C from λ_k(y) to ρ_k(y) lies in T_k and in Ω, starts in Z_i and
ends in Z_i′. Let Y₀ = Z_i, Y₁, …, Y_r = Z_i′ be the squares met by C in order. By the triangle inequality
θ_i ≤ Σ_j θ(Y_{j−1}, Y_j).

Call (k, y) *bad* if the uncovered part of C has length ≥ 2/5. The segments C for different k are disjoint apart
from end points, so the number of bad k at height y is at most 5/2 times the line waste at height y; as
θ_i < 2τ, the bad pairs contribute at most 2τ·(5/2)·W ≤ 0.4·W to the sum.

If (k, y) is not bad, consecutive squares Y_{j−1}, Y_j on C are separated by a gap < 2/5 on the line of height y, so
their centres are within √2 + 2/5. A pair of squares is consecutive on at most one of the segments C at a given
height. Hence the not-bad part of the sum is at most

    ∫ Σ_{(Y, Y′)} θ(Y, Y′) dy ≤ √2 · Σ_{{Y, Y′}} θ(Y, Y′),

the sum on the left over the pairs that are consecutive on the line of height y with a gap < 2/5, and the sum on
the right over the unordered pairs that are so at some height; a pair meets a common horizontal line on a set of
heights of measure ≤ √2. By [S, Cor. 2.3], θ(Y, Y′) is at most 50 times the waste in R(Y, Y′), and a point p of the
waste lies in R(Y, Y′) only if both squares lie in B(p, 2.61): at most 21 squares, at most 210 unordered pairs.
So the right side is ≤ √2·50·210·W < 14850·W. ∎

## 6. Boundaries between arriving intervals

On J_k let N_k, D_k be the constants of Lemma 3.1(d), P_k = D_k − N_k, and let G̃ be the function of (3.1). Write
G̃(b_k^−), G̃(a_{k+1}^+) for its limits at the ends, Φ = g(x′) for the arrival height, and for 1 ≤ k < K

    drop_k = G̃(b_k^−) − G̃(a_{k+1}^+),     Δ_k = x′(a_{k+1}^+) − x′(b_k^−) ≥ 0.

Since Φ = −P + G̃ and Φ is increasing along the arriving points (Lemma 3.2),

    drop_k = (P_k − P_{k+1}) − ζ·Δ_k ≤ P_k − P_{k+1},    and drop_k ≤ δ.        (6.1)

**Lemma 6.1 (drops add up).** Let 𝒢 be the set of arriving x. Then Σ_k max(drop_k, 0) ≥ sin ζ′·|𝒢| − δ.

Proof. By Lemma 3.1(d), G̃(b_k^−) − G̃(a_k^+) ≥ sin ζ′·|J_k|. Summing over k,
sin ζ′·|𝒢| ≤ Σ_{k<K} drop_k + G̃(b_K^−) − G̃(a_1^+) ≤ Σ_k max(drop_k, 0) + δ. ∎

For a boundary k call the level i ≤ min(N, N′) *aligned* if τ·Σ_{l < i} θ_l < ¼, and put Θ_k = Σ_{aligned i} θ_i.

**Lemma 6.2 (aligned levels face each other).** For an aligned level, |Y_i| ≥ 0.7.

Proof. By Lemma 3.1(c), h_i − h_i′ = Σ_{l<i} (cos φ_l − cos φ_l′) + (G̃-parts), where the two partial sums of gaps lie
in [0, δ]. As |cos φ_l − cos φ_l′| ≤ sin τ·|φ_l − φ_l′| ≤ τ·θ_l, the offset is ≤ ¼ + δ, and both intervals have
length ≥ cos τ. So |Y_i| ≥ cos 0.08 − ¼ − 1/32 > 0.7. ∎

**Lemma 6.3 (a drop is paid for, or it is a skip).** Let drop_k > 0. Then either drop_k ≤ τ·Θ_k, or N′ > N and
Δ_k ≥ 1/(2ζ).

Proof. If some level i ≤ min(N, N′) is not aligned, then τ·Θ_k ≥ ¼ ≥ δ ≥ drop_k (the levels before the first
non-aligned one are aligned and their sum is ≥ 1/(4τ)). So assume all levels are aligned; then Θ_k is the sum of
θ_i over all i ≤ min(N, N′).

* N′ = N. By (6.1), drop_k ≤ D_k − D_{k+1} = Σ_i (cos φ_i′ − cos φ_i) ≤ τ·Θ_k.
* N′ = N − j, j ≥ 1. By (6.1), 0 < P_k − P_{k+1} = D_k − D_{k+1} − j, and
  D_k − D_{k+1} = Σ_{i ≤ N′} (cos φ_i′ − cos φ_i) + Σ_{i > N′} (1 − cos φ_i) ≤ τΘ_k + 0.51·j·τ². So
  τΘ_k ≥ j·(1 − 0.51τ²) > ½ ≥ drop_k.
* N′ = N + j, j ≥ 1. Then ζ·Δ_k = (P_k − P_{k+1}) − drop_k = j + D_k − D_{k+1} − drop_k, and
  D_k − D_{k+1} = Σ_{i ≤ N} (cos φ_i′ − cos φ_i) − Σ_{i > N} (1 − cos φ_i′) ≥ −τΘ_k − 0.51·j·τ². If τΘ_k < ¼, then
  ζ·Δ_k ≥ j·(1 − 0.51τ²) − ¼ − δ ≥ ½. If τΘ_k ≥ ¼, then drop_k ≤ δ ≤ τΘ_k. ∎

## 7. Proof of Theorem B

**Proposition 7.1.** Let R ≥ 1, ζ ≤ 1, δ = 1/32 and 0 < τ ≤ 0.08. If 4250·W + 1350·W/τ + 0.01 ≤ L/4, then
0.47·R ≤ 21300·τ·W.

Proof. By Corollary 4.5, |𝒢| ≥ 3L/4. The arrival abscissas of 𝒢 form a set of measure ≥ cos ζ′·|𝒢| ≥ 0.53·L
(Lemma 3.1(d), Lemma 3.2), and the Δ_k are the lengths of disjoint intervals of [0, L] that miss it, so
Σ_k Δ_k ≤ 0.47·L. Call k a *skip* if Δ_k ≥ 1/(2ζ); there are at most 0.94·ζL = 0.94·R skips, and each has
drop_k ≤ δ. By Lemmas 6.1 and 6.3,

    sin ζ′·(3L/4) − δ ≤ Σ_k max(drop_k, 0) ≤ τ·Σ_k Θ_k + 0.94·R·δ.

The left side is ≥ (ζ/√2)(3L/4) − 1/32 ≥ 0.499·R for R ≥ 1. By Lemmas 5.1 and 6.2,
0.7·Σ_k Θ_k ≤ Σ_k Σ_i θ_i·|Y_i| ≤ 14851·W. So 0.4696·R ≤ 0.499·R − 0.0294·R ≤ τ·21216·W, and
0.47·21216 < 0.4696·21300. ∎

Proof of Theorem B. Since ζ ≤ 1, √(LR) ≤ L. If W > 7·10⁻⁶·L we are done. Otherwise, if W > 0, take
τ = 10800·W/L ≤ 0.0756. Then 1350·W/τ = L/8, 4250·W ≤ 0.03·L and 0.01 ≤ 0.01·L (L ≥ R ≥ 1), so the hypothesis of
Proposition 7.1 holds and 0.47·R ≤ 21300·10800·W²/L, that is W ≥ 4.5·10⁻⁵·√(LR). If W = 0, the proposition with
τ = 0.08 gives 0.47·R ≤ 0, which is false. ∎

## 8. Consequences (if the proof stands)

Only the first bullet and the lower bounds in the others follow from Theorem B (with [S] where cited). Everything
about the frames of Bui, McClenagan and Ryu depends on their wall shapes, their matching upper bounds and their
decomposition into separately packed pieces, as described in those papers; this note cites those facts and does not
re-derive them. No bound here applies to a packing whose squares cross the boundaries between the pieces.

* **Bui's Conjecture 1** holds: a right trapezoid of height x ≥ 1 whose bases differ by x^{1−γ}, 0 < γ < 1, wastes
  ≥ 7·10⁻⁶·x^{1−γ/2}, whatever its width. Combined with [S, Corollary 1] (not only Section 2 of [S]), the lower
  bound for his trapezoid (height x, width x^β, slope x^{−γ}, 0 < γ < 1) is x to the power
  max(1 − max(β, 1−γ)/2, 1 − γ/2), which are the first two terms of his Conjecture 2 in that range. For γ > 1 the
  rise is below 1 and neither result applies.
* **Walls.** A right trapezoid of height m and lean ≍ √m wastes ≥ c·m^{3/4} at any width (Theorem B, for m large
  enough that 1 ≤ R ≤ L). Given that the wall fillers of Bui and of Ryu (width ≍ m^{3/4}) are such trapezoids
  packed on their own with waste O(m^{3/4}), as those papers state, they are optimal up to a constant, as
  McClenagan's is by [S].
* **Frames.** Take an outer side x whose fractional part is bounded away from 0 and 1, say x = n + ½. Given that
  Bui's and McClenagan's frames consist of a grid, x × h strips with h ≥ 1 and end trapezoids of height ≍ h and rise
  ≍ √h, each packed on its own: the strip has the fractional part of x and costs ≥ c·x/√h ([S, Cor. 2(b)]; near an
  integer that bound carries the factor min(f, √(1 − f)) and is not uniform), and each end trapezoid costs
  ≥ c·h^{3/4}; so for such x those frames cannot beat x^{3/5}, whatever is put into the strips and trapezoids. Given
  that Ryu's frame has an end region of thickness O(m) (lift O(m)) and wall regions of height ≍ m and lean ≍ √m,
  each packed on its own, the end costs ≥ c·b/√m ([S, Corollary 1]) and each wall ≥ c·m^{3/4}; together
  ≥ c·b^{3/5}, which gives k^{3/8} through his identity c*(k) ≈ 4k/b + (end costs), which I take from his paper and
  have not rederived. Under those hypotheses the window [5/14, 3/8] left open in [S] closes at 3/8 for ends of that
  kind. For larger lifts only the next bullet applies.
* **Ryu's end region.** Reg(y) = {0 ≤ x′ ≤ w, 0 ≤ y′ ≤ y + (x′ − σ)·t} with σ = sin θ, t = tan θ, w = b cos θ + σ,
  as cited from his paper. Assume 0 < t ≤ 1 and b·sin θ ≥ 1. If y ≥ σt, Reg(y) is a right trapezoid with floor
  length L = w, slope t ≤ 1 and rise R = wt ≥ b sin θ ≥ 1. If 0 ≤ y < σt, the ceiling meets the floor at
  x₀ = σ − y/t ∈ (0, σ] and Reg(y) is, after translating by x₀, the triangle of floor length
  L′ = w − x₀ = b cos θ + y/t and rise R′ = L′t = b sin θ + y ≥ 1. In both cases Theorem B applies and
  LR ≥ b² sin θ cos θ, so every packing of Reg(y) wastes ≥ 7·10⁻⁶·b·√(sin θ cos θ), which is ≥ c·√b uniformly in
  y ≥ 0 when sin θ ≍ 1/b (his tilts, tan θ ≈ 2/b). Given his description of the frame and of the open problem of
  his §12, this answers it with β = ½, the value his cube-root lower bound suggests.
* Not claimed: a bound for W(x) or c*(k) over all packings. A packing need not contain such trapezoids (Bui makes
  the same remark after his conjecture).

## 9. Checks and referee reports

* `docs/wedge-lower-bound-review-2026-11-09.md`: blind adversarial read of v0.1 by Claude Opus 5.5, told to assume
  there is a hole. Verdict "sound with fixes"; no fatal error; every lemma, the arithmetic and the reduction to
  Bui's conjecture rederived. Its own caveat: "one reader's afternoon against the author's afternoon". Applied in
  v0.2: the wall case of the fundamental lemma is now argued (Section 1) and the left-wall count corrected; Lemma
  3.1(a) uses the finer partition; step 4 allows the emitting square; conflicts are within 2δ; the ranges in
  Section 8 are stated.
* `tools/wedge_flow_check.py` (Codex, from the definitions here): the flow by exact geometry on 31 packings and 186
  parameter rows. All checks of Lemmas 3.1–4.4, (6.1), 6.1–6.3 and 5.1 passed. **But the main line was hardly
  exercised**: the test packings waste far too much for Proposition 7.1 to apply, and in most rows no path arrives.
  Results: `runs/k2c-exponent-2026-11-09/wedge-flow-check.md` (not in git).
* `docs/wedge-lower-bound-review-codex-2026-11-09.md`: second referee (Codex), blind to the first report and to the
  simulator. Verdict "sound with fixes", no fatal finding, every lemma rederived. Applied in v0.3: Lemma 3.1(a)
  cuts at the ends of the sets where G + r* = δ; the last rounding in Proposition 7.1 is shown; the frame
  consequence is stated for sides away from integers.
* `tools/wedge_staircase_check.py` (Codex): staircase packings (tilted columns on axis layers, 199,030 squares in
  the largest) built so that most paths arrive: 79% for the clean staircase, 74% with squares removed, 63% with two
  tilts, 99.9% in a window of a small-angle staircase, 16% with brick-offset layers. Here Sections 5–6 are a real
  comparison. No failure in 23 million comparisons. Lemma 6.1: the lower bound is 0.69, 0.66, 0.58 of the actual
  sum of positive drops. Lemma 6.3: drop/(τΘ) ≤ 0.36 at every paid boundary, against α/(2τ) = 0.44 predicted for a
  layer end; no skips. Lemma 5.1: the sum is 0.05·W, against the constant 14851. Floating point with tolerance
  2·10⁻⁷, not a certificate. Results: `runs/k2c-exponent-2026-11-09/wedge-staircase-check.md` (not in git).
* Three further blind judges (Codex, fresh sessions, each told to assume there is an error and to build
  counterexamples), one per scope: `docs/wedge-lower-bound-judge-A-codex-2026-11-09.md` (Sections 1–4, with the
  fundamental lemma of [S]), `docs/wedge-lower-bound-judge-B-codex-2026-11-09.md` (Sections 5–8) and
  `docs/slab-lower-bound-judge-codex-2026-11-09.md` ([S]). None found a fatal error. Judge B marked every step of
  Sections 5–7 verified, including Theorem B with constant 4.52·10⁻⁵ in the small-W branch. Applied in v0.4: the
  count of [S, Cor. 2.3] when S₂ is the floor or a wall (repaired in [S] v0.3); termination of the flow (Section
  2); the polygonal probe regions and the induction in Lemma 3.1(a); Lemma 4.2 written out instead of cited
  (50·(21 + 4√2) < 1333); Section 8 made conditional on the cited papers, the use of [S, Corollary 1] stated, and
  the two cases and hypotheses for Ryu's end region written out.
* Proposition 7.1 itself has never had its hypothesis satisfied by a test packing; that would need a waste below
  about L/34000.
* Still missing: a human reader. Everything above is AI-written and AI-checked.
