# Slab lower bound: a region of thickness M over a floor of length L wastes ≥ c·L/√M (draft v0.3, 2026-11-09)

Status: written 2026-11-09 in one session, day 2 of the exponent probe (`docs/k2c-exponent-probe.md`). v0.2 applies
the blind referee report `docs/slab-lower-bound-review-2026-11-09.md` (verdict: sound with fixes; the proofs stood,
the claims about Bui's and Ryu's walls did not). v0.3 applies a second blind judge (Codex,
`docs/slab-lower-bound-judge-codex-2026-11-09.md`: no fatal error; gaps in Lemma 2.1, Corollary 2.3, Lemma 3.1(a),
the measure statements of Section 3, Remark 6.1 and Corollary 2(b), and two errors in the outline of Section 7, all
repaired or marked here). See Section 9. Both judges are AI models; no person has read this note. Constants are
checked by `tools/slab_constants.py`, the flow itself numerically by `tools/slab_flow_check.py`.

## 0. What is claimed

Let g be a concave function on [0, L] with 0 ≤ g ≤ M, and Ω = {(x, y) : 0 ≤ x ≤ L, 0 ≤ y ≤ g(x)}. A packing is a
finite set of closed unit squares in Ω with pairwise disjoint interiors; its waste W is the area of Ω minus the number
of squares. For 0 < δ, δ′ put

    A(δ, δ′) = { x ∈ [0, L] : N − δ′ ≤ g(x) ≤ N + δ for some integer N }.

**Theorem S.** Let 0 < δ ≤ 2/5, δ′ > 0 and 0 < τ ≤ 0.08 with 0.502·M·τ² ≤ δ′. Every packing of Ω satisfies

    L − |A(δ, δ′)| ≤ W/δ + 1350·W/τ + √(21·τ·M·L·W).

**Corollary 1 (sloped ceiling).** Let g(x) = w + ζx with w ≥ 0, ζ > 0, rise ζL ≥ 1 and M = w + ζL. Then
W ≥ 4·10⁻⁵·L/√M, and W ≥ 1.5·10⁻⁴·L/√M if M ≥ 13.

**Corollary 2 (rectangles).** (a) Every packing of an L × (m + ½) rectangle with integer m ≥ 125 has
W ≥ 5·10⁻⁴·L/√(m + ½). In particular a square of side n + ½, n ≥ 125, has waste ≥ 5·10⁻⁴·√(n + ½).
(b) Every packing of an L × M rectangle, M ≥ 1 with fractional part f ∈ (0, 1), has
W ≥ 5·10⁻⁵·L·min(f, √((1 − f)/M)). For a square of side x with f = x − ⌊x⌋ ≤ ½ this is W(x) ≥ c·min(xf, √x).

**Corollary 3 (wall trapezoid).** A right trapezoid of height h whose parallel sides have lengths w and w + r, r ≥ 1,
has waste ≥ 4·10⁻⁵·h/√(w + r). If w, r ≤ C√h this is ≥ c(C)·h^{3/4}.

How this sits in the literature (details in Section 6):

* Corollary 3 matches McClenagan's O(h^{3/4}) packing of his wall trapezoid, which has width ≍ √h
  (arXiv:2602.01484, §4). So his filler is optimal up to a constant, and his x^{3/5} cannot be improved by packing
  that trapezoid better.
* It does **not** settle the walls of Bui (arXiv:2508.04603, §4) or Ryu (k2-minus-c-upper v1.1, construction E38).
  Their walls have height m, lean √m and width ≍ m^{3/4}; there Corollary 1 gives m^{5/8} against their O(m^{3/4}).
* Bui's Conjecture 2 predicts the exponent max(1 − max(β, 1−γ)/2, 1 − γ/2, β − ½, 3/5) for a trapezoid of height x,
  width x^β and slope x^{−γ}. Corollary 1 proves the first term as a lower bound. His Conjecture 1 (difference of the
  bases x^{1−γ} forces waste x^{1−γ/2}) follows when β ≤ γ and γ ≥ ½, and is open otherwise.
* Corollary 2(b) is stronger than Roth–Vaughan's √(x·‖x‖) just above an integer. For x − ⌊x⌋ ≤ x^{−1/2} the trivial
  packing is optimal up to a constant. For Bui's Question 1 (x − ⌊x⌋ ≍ x^{−2/5}) the lower bound moves from x^{3/10}
  to x^{1/2}; the question itself (is o(x^{3/5}) possible) stays open.
* Ryu's end region Reg(y) costs ≥ c·b/√(y + 2) at lift y, so his end cost O(b^{3/5}) is optimal for the region he
  uses (y ≍ b^{4/5}). This is a partial answer to the open problem in his §12, since lifts are free in his frame.

What is not claimed: nothing here is a new bound for W(x) at generic x or for c*(k) over all packings. Theorem S is
weak for thick regions (M large), and that is where any improvement of 3/5 has to come from (Section 7).

Credits. Forcing tilt through the projection deficit Σ(1 − cos θ_i) along a chain of squares is Roth and Vaughan's
argument (JCTA 24, 1978; known to me only through evand/square-packing `literature/waste-bounds-2026-10-12.md`, as
Elsevier returned 403). The fundamental lemma (Lemma 2.2) is theirs; the proof given here is the one in Ryu's
k2-minus-c v1.2, Proposition 3.3, rewritten for packings whose squares may touch. Following a path upwards through
the squares along their normals, and the height identity (3.1), are Ryu's "master flow" (k2-minus-c-quarter, §3–4);
the flow below is a simpler variant (vertical moves in gaps). Bui's Proposition 3 is an earlier lower bound of this
kind for a thin region (a parallelogram, Ω(√x)), by the fundamental lemma along paths. New here, as far as the
referee and I could find: the injective flow with exact conservation of measure, the Cauchy–Schwarz bound for
lateral entries (Lemma 4.3), the sloped ceiling as the obstruction, and the corollaries. No explicit Roth–Vaughan
constant better than their 10⁻¹⁰⁰ turned up in the search; evand's wishlist lists an effective constant as open.

## 1. Conventions

A unit square Z has an orientation φ_Z ∈ (−π/4, π/4]: its sides make the angles φ_Z + jπ/2 with the x-axis. Its
inclination is a(Z) = |φ_Z|. For two squares θ(Z, Z′) ∈ [0, π/4] is the distance of φ_Z and φ_Z′ in ℝ/(π/2)ℤ; the
floor has orientation 0, so θ(Z, floor) = a(Z). θ is a metric.

If a(Z) < π/4 write u_Z = (cos φ_Z, sin φ_Z), n_Z = (−sin φ_Z, cos φ_Z) and Z = {P + s·u_Z + t·n_Z : 0 ≤ s, t ≤ 1}.
The bottom side is t = 0, the top side t = 1, the lateral sides s = 0 and s = 1. For x in the projection of the top
side, top_Z(x) is the height of the top side above x; its slope is tan φ_Z.

Waste also denotes the set of points of Ω in no square. Squares of a packing have centres at pairwise distance ≥ 1.
A unit square that meets a set X lies in the √2-neighbourhood of X, so at most area(N_√2(X)) squares of a packing
meet X; for an a × b rectangle that area is ab + 2√2(a + b) + 2π.

## 2. The fundamental lemma

**Lemma 2.1 (convex gaps; Ryu).** Let I be an interval of length λ, 0 ≤ φ ≤ 1, and γ ≥ 0 a continuous, convex,
piecewise linear function on I such that |γ′| ≥ φ off the break points and the slope of γ increases by at least 2 at
every break point. Then ∫_I γ ≥ φ(2 − φ)λ²/4.

Proof. If φ = 0 the claim is ∫_I γ ≥ 0, true as γ ≥ 0; let φ > 0. Let y* be a minimum point of γ on the closure of
I, at distances a and b = λ − a from the two ends. If y* is
an end point, γ(y) ≥ φ|y − y*| and ∫γ ≥ φλ²/2. Otherwise y* is a break point with slopes −p < 0 < q, p, q ≥ φ,
p + q ≥ 2, and by convexity ∫γ ≥ (pa² + qb²)/2 ≥ λ²/(2(1/p + 1/q)) (Cauchy–Schwarz). Under the constraints,
1/p + 1/q ≤ 1/φ + 1/(2 − φ) = 2/(φ(2 − φ)): if say p ≤ q and q ≥ 2 − φ this is clear; if q < 2 − φ then q ≥ 1,
p ≥ 2 − q, and 1/(2 − q) + 1/q is convex and symmetric about 1, so it is at most its value at q = 2 − φ. ∎

**Lemma 2.2 (fundamental lemma).** Let S₁ be a square of a packing of Ω, with centre c₁. Let S₂ be either another
square of the packing, with centre c₂, or the floor, in which case c₂ is the foot of the perpendicular from c₁. Let
ℓ = |c₁ − c₂|, u = (c₂ − c₁)/ℓ, n ⊥ u a unit vector, and

    R = R(S₁, S₂) = { c₁ + s·u + t·n : 0 ≤ s ≤ ℓ, |t| ≤ ½ }.

Then R ⊂ Ω. If at most m′ squares other than S₁, S₂ meet R, the waste inside R has area at least
θ(2 − θ)/(4(m′ + 1)), where θ = θ(S₁, S₂).

Proof. *R ⊂ Ω.* Centres of squares lie in Ω₋ = {p : B(p, ½) ⊂ Ω}, which is convex. In the first case the segment
c₁c₂ lies in Ω₋ and R within ½ of it. In the floor case R = [x₁ − ½, x₁ + ½] × [0, y₁] for c₁ = (x₁, y₁); it lies in Ω
because (x₁ ± ½, y₁) ∈ Ω and Ω contains the vertical segment from each of its points down to the floor.

*Coordinates.* Use (s, t) as in the definition of R, Σ = {|t| < ½}, and for |t| < ½ let ℓ_t be the chord of R at
height t. For a square Z let [τ⁻(Z), τ⁺(Z)] be its t-projection (of length ≥ 1), and for t in it let l_Z(t), r_Z(t) be
the least and largest s on Z at height t. l_Z is convex, r_Z concave, each piecewise linear with at most one break
point (at a vertex), where the slope changes by tan γ + cot γ ≥ 2 for some γ ∈ (0, π/2); off the break point the
slope is tan ψ, ψ ∈ (−π/2, π/2) being the angle from the t-axis to the side in question.

*Squares in the strip.* The points c₁ + t·n, |t| < ½, are interior points of S₁, and c₂ + t·n are interior points of
S₂ in the first case. Let Z ≠ S₁, S₂ meet some chord ℓ_t. Z ∩ Σ is convex and misses the open segment
Σ ∩ {s = 0}, and misses Σ ∩ {s = ℓ} in the first case; in the floor case Z ⊂ {s ≤ ℓ}. So Z ∩ Σ ⊂ R. Hence for
|t| < ½ such a Z meets ℓ_t exactly when τ⁻(Z) ≤ t ≤ τ⁺(Z), and its chord at height t then lies in ℓ_t. At most one of
τ^±(Z) lies in (−½, ½). Let T be the set of these values over all such Z; |T| ≤ m′. T cuts (−½, ½) into q ≤ m′ + 1
open intervals I_r of lengths λ_r, Σλ_r = 1.

*Gaps.* Fix r. For t ∈ I_r the chord ℓ_t meets the same squares, each in a segment of positive length, and (their
interiors being disjoint, by continuity in t) in the same order Z₀ = S₁, Z₁, …, Z_K, followed by Z_{K+1} = S₂ or the
floor. Put γ_i(t) = l_{Z_i}(t) − r_{Z_{i−1}}(t) ≥ 0 for 1 ≤ i ≤ K + 1 (with l ≡ ℓ for the floor). The sets
{(s, t) : t ∈ I_r, r_{Z_{i−1}}(t) < s < l_{Z_i}(t)} are pairwise disjoint parts of the waste in R. Each γ_i is convex
and piecewise linear, its slope increases by ≥ 2 at break points, and off them γ_i′ = tan ψ′ − tan ψ, where ψ, ψ′ are
the directions of the two sides bounding the gap; so |γ_i′| ≥ |ψ′ − ψ| ≥ φ_i := θ(Z_{i−1}, Z_i), because the direction
of a side is congruent to the orientation of its square modulo π/2 (and the floor line s = ℓ has ψ′ = 0, orientation
0). By Lemma 2.1, ∫_{I_r} γ_i ≥ φ_i(2 − φ_i)λ_r²/4.

*Summation.* Σ_i φ_i ≥ θ by the triangle inequality. With φ_i′ = min(φ_i, θ) also Σφ_i′ ≥ θ, and since x(2 − x) is
increasing on [0, 1], Σ_i φ_i(2 − φ_i) ≥ (2 − θ)Σφ_i′ ≥ θ(2 − θ). Hence the waste in R is at least
(θ(2 − θ)/4)·Σ_r λ_r² ≥ θ(2 − θ)/(4q). ∎

**Corollary 2.3.** In Lemma 2.2 suppose ℓ ≤ √2 + 2/5. Then at most 14 other squares meet R, and the waste in R has
area ≥ θ(S₁, S₂)/50. Every point of R is within 1.9 of c₁.

Proof. R lies in a 1 × 1.82 rectangle. If S₂ is a square, area(N_√2(R)) ≤ 1.82 + 2√2·2.82 + 2π < 16.1, so at most
16 squares meet R, two of which are S₁, S₂. If S₂ is the floor, R = [x₁ − ½, x₁ + ½] × [0, ℓ] and every square lies
in y ≥ 0; the part of N_√2(R) below y = 0 is a 1 × √2 rectangle and two quarter discs of radius √2, of area √2 + π,
so the rest has area < 16.08 − √2 − π < 11.53: at most 11 squares, one of which is S₁. The same holds for any line
with the whole packing on one side of it (a side wall). Either way at most 14 others. Then
(2 − π/4)/(4·15) > 1/50 and √(1.82² + ¼) < 1.9. ∎

## 3. The flow

Fix a packing, δ ∈ (0, 2/5] and τ ∈ (0, 0.08]. A square is *steep* if a(Z) ≥ τ and *flat* otherwise. A flat square
has a bottom side, a top side and two lateral sides; a vertical ray going up can enter it only through the bottom
side or, if φ_Z ≠ 0, through the one lateral side whose outward normal points downwards.

For x ∈ [0, L] the *path* of x is built as follows. It starts at p = (x, 0) with gap count G = 0 and N = 0.

1. The current point p is on the floor or on the top side of a flat square. Let q be the first point of the closed
   upward vertical ray from p that lies on the ceiling or in a square other than the one just left (q = p is
   possible). The open segment (p, q), if non-empty, is a *gap segment*; it lies in the waste. Add its length to G.
   If G would exceed δ, stop at the point where G = δ: **gap death**.
2. If q is on the ceiling (and in no square): **arrival** at q.
3. If q is in a steep square: **tilt death**.
4. If q is in a flat square Z′, in the relative interior of a lateral side: **lateral death**.
5. If q is in a flat square Z′, in the relative interior of its bottom side: move along the segment from q to
   p′ = q + n_Z′, a point of the relative interior of the top side, increase N by one, and go to step 1 with p = p′.
6. If q is a vertex of any square, x is *exceptional*; this takes precedence over 3–5.

In step 1 the case q = p occurs when another square touches the current point. If p is in the relative interior of
the top side of Z and of a side of Z′ ≠ Z, the two squares lie on opposite sides of the common line, so that side is
parallel to the top side of Z with outward normal −n_Z: Z′ is flat and it is its bottom side. So steps 2–6 cover all
cases. Heights strictly increase along a path, each square is visited at most once (proof of Lemma 3.1(a)), and the
construction ends.

**Lemma 3.1.**
(a) The set E of exceptional x is finite. There is a finite set E′ ⊇ E ∪ {0, L} such that on each open interval
    of [0, L] ∖ E′ the itinerary (the sequence of squares and sides met, and the kind of ending) is constant. The
    points of E′ ∖ E are non-exceptional and have their paths, but are not assigned to any interval; being finitely
    many they do not affect any measure below.
(b) (Height identity.) If the path of x arrives after passing Z₁, …, Z_N, at the ceiling point of abscissa x′, then

        g(x′) = N − D + G,   D = Σ_j (1 − cos φ_{Z_j}),   x′ = x − Σ_j sin φ_{Z_j},        (3.1)

    where G ≤ δ is the total length of its gap segments.
(c) (Translation.) On an interval of constant itinerary, the abscissa of the path at each of its stages is x minus a
    constant.
(d) (Injectivity.) Paths of distinct non-exceptional x are disjoint.

Proof. (b) and (c): a gap segment is vertical, and crossing Z from q to q + n_Z adds cos φ_Z to the height and
−sin φ_Z to the abscissa. (a): No square is crossed twice: for a flat Z every point of the top side is higher than
every point of the bottom side, by cos φ_Z − |sin φ_Z| > 0, so a path that has left Z through its top side never
again reaches its bottom side. Hence a path crosses distinct squares, and there are finitely many possible prefixes
(sequences of squares crossed so far). Induct on the number of steps. On an open interval where a prefix is fixed,
the horizontal coordinate of the current point is x minus a constant (by (c)), so the vertical ray from it passes
through a given vertex for at most one x; over all prefixes and vertices that is finitely many x. Away from them the
first object hit is locally constant, since it can change only where the ray passes a vertex. On a fixed prefix
each gap segment that ends on a square has affine length in x (both ends lie on straight sides), and the final gap
to the ceiling has length g(x − constant) minus an affine function, which is concave. So the total G at a given
stage is affine or concave, the set where it exceeds δ is an interval, and the set where it equals δ is at most two
points or a closed interval; this adds finitely many end points. A concave g is continuous on (0, L); a jump at 0 or
L affects only the finitely many x whose translated abscissa is that end. Collect all these points with 0 and L in
E′.

(d): A non-exceptional path consists of gap segments, whose interiors are in the waste, and crossings [q, q + n_Z]
from the relative interior of the bottom side of a flat square Z to the relative interior of its top side, whose
interiors are in the interior of Z. It meets the floor only at its starting point. Suppose two such paths meet and let c be a common point of least height; we show that c is the starting
point of both, so x₁ = x₂.

* c interior to a square Z: both paths cross Z along the segment through c parallel to n_Z and share its lower end.
* c in the waste and not on the floor: on each path c lies on a gap segment, which starts at a point of the floor or
  of a top side and runs through waste; so both contain the vertical waste segment below c, and its lower end.
* c on the boundary of a square, not on the floor. A path reaches c either along a gap segment of positive length
  ending at c, and then the points just below c are waste, or as the upper end of a crossing of a square Z, and then
  c is in the relative interior of the top side of Z and the points just below c are interior to Z. The two cases
  exclude each other, and in the second Z is determined by c. So both paths share the gap segment below c, or both
  cross the same Z along the same segment. Either way they share a lower point.
* c on the floor: it is the starting point of both.

The first three cases contradict the choice of c. ∎

Consequences used below. Let X be a set of non-exceptional starting points with a common itinerary up to some stage.
By (c) and (d) the abscissas of their paths at that stage form a translate of X, and the gap segments, entry points
and arrival points of different x are different. In particular: the arrival abscissas of a set X of arriving paths
form a set of measure |X|; the set of x whose path crosses a given flat square Z has measure ≤ cos φ_Z ≤ 1; and gap
segments of different paths sweep disjoint parts of the waste, so ∫ G(x) dx ≤ W over any set of x.

The last point is an area statement and needs a parametrisation, not only disjointness. Fix an interval J of
constant itinerary and the index of a gap on it. There are a constant c and functions β ≤ α on J (β affine, α affine
or concave, or truncated at the level where G reaches δ) such that the gap segment of x ∈ J is
{(x − c, v) : β(x) < v < α(x)}. The map (x, v) ↦ (x − c, v) has Jacobian 1, so the set swept has area
∫_J (α − β) dx, the integral of that gap's length. By (d) the swept sets for different (J, gap index) are disjoint
apart from boundaries of area zero, and they lie in the waste; summing gives ∫ G dx ≤ W. In the same way the arrival
map is a translation on each J and the images are disjoint, which gives the measure of the arrival abscissas; and
the entry abscissas into a flat square Z fill disjoint translates in the projection of its bottom side, of length
cos φ_Z.

## 4. Three ways to die

**Lemma 4.1 (gap deaths).** The set of x with a gap death has measure ≤ W/δ.

Proof. Each such path has gap segments of total length δ, and ∫G ≤ W. ∎

**Lemma 4.2 (tilt deaths).** The set T of x with a tilt death has measure ≤ 1350·W/τ.

Proof. Let x ∈ T, with squares Z₁, …, Z_j passed and steep square Z* reached; put Z₀ = floor. Consecutive members of
the chain Z₀, Z₁, …, Z_j, Z* are joined by a gap segment of length ≤ δ (possibly 0), so two consecutive squares have
centres at distance ≤ √2 + δ, and the first square has its centre at height ≤ √2/2 + δ. By the triangle inequality
the sum of θ over consecutive pairs is ≥ θ(floor, Z*) = a(Z*) ≥ τ, and by Corollary 2.3 each θ(S, S′) is at most 50
times the waste in R(S, S′). For a pair (S, S′) let μ(S, S′) be the measure of the set of x ∈ T whose chain contains
it consecutively. Then

    τ·|T| ≤ Σ_{(S,S′)} μ(S, S′)·θ(S, S′) ≤ 50 ∫_waste Σ_{(S,S′) : p ∈ R(S,S′)} μ(S, S′) dp.

Fix p. If S is a square and p ∈ R(S, S′), then S ⊂ B(p, 1.9 + √2/2), a disc of area < 21.4, so there are at most 21
such S, and Σ_{S′} μ(S, S′) ≤ 1 for each (paths crossing S). If S is the floor and p ∈ R(S′, floor), then S′ lies in a
box of width 1 + √2 and height √2 + δ around p, of area < 4.4; there are at most 4 such S′, each with
μ ≤ √2 (its horizontal extent). The inner sum is ≤ 21 + 4√2 < 27, and 50·27 = 1350. ∎

**Lemma 4.3 (lateral deaths).** The set of x with a lateral death has measure ≤ √(21·τ·n·W), where n is the number
of squares; n ≤ area(Ω) ≤ LM.

Proof. For a flat square Z′ with φ_Z′ ≠ 0, with entering lateral side σ, and Z a flat square or the floor, let
I(Z, Z′) be the set of ξ such that the vertical segment from (ξ, top_Z(ξ)) up to the point of σ above ξ has length in
(0, δ] and its interior lies in the waste. A lateral death of x ends with such a segment for some pair, and by Lemma
3.1 different x give different ξ for the same pair. So the measure in question is ≤ Σ |I(Z, Z′)|.

On I(Z, Z′) the length of the segment is γ(ξ) = σ(ξ) − top_Z(ξ), the restriction of an affine function whose slope
has absolute value ≥ cot a(Z′) − tan a(Z) ≥ s := cot τ − tan τ: the lateral side has slope ∓cot a(Z′), the top side
of Z slope tan φ_Z, the floor slope 0. Since γ > 0 on I(Z, Z′), this set lies on one side of the zero ξ₀ of that
affine function, where γ(ξ) ≥ s|ξ − ξ₀|; hence ∫_{I(Z,Z′)} γ ≥ s·|I(Z, Z′)|²/2. The segments for different pairs sweep
disjoint parts of the waste (a vertical waste segment determines the objects at its two ends). So

    Σ |I(Z, Z′)|² ≤ 2W/s.

For fixed Z′ the top side of Z meets the set of points at most δ below σ, which lies in a box of width
sin τ ≤ 0.08 and height 1 + δ ≤ 1.4; area(N_√2) of that box is < 10.6, so at most 10 squares meet it, one of which is
Z′. With the floor that makes at most 10 pairs per Z′, at most 10n pairs in all. By Cauchy–Schwarz
Σ|I| ≤ √(10n·2W/s), and s·τ ≥ 0.99 for τ ≤ 0.08 (τ cot τ − τ tan τ is decreasing). 20/0.99 < 21. ∎

## 5. Proof of Theorem S

Let x be non-exceptional. Its path ends by a gap death, a tilt death, a lateral death or an arrival. If it arrives,
all squares it passed are flat. By (3.1) the height reached is N − D + G ≤ M with every cos φ ≥ cos τ, so
N ≤ M/cos τ and

    D ≤ N(1 − cos τ) ≤ M(1 − cos τ)/cos τ ≤ 0.502·M·τ² ≤ δ′     (τ ≤ 0.08),

while 0 ≤ G ≤ δ. So g(x′) ∈ [N − δ′, N + δ]: the arrival abscissa x′ lies in A(δ, δ′). The arrival abscissas of the
arriving x form a set of the same measure (Lemma 3.1), so the set of arriving x has measure ≤ |A(δ, δ′)|. Adding
Lemmas 4.1–4.3 with n ≤ LM gives the theorem. ∎

## 6. Corollaries and what they say about the frames

All numerical claims are checked on a grid by `tools/slab_constants.py`; the right side of Theorem S is increasing
in W, so excluding W = κL/√M excludes every smaller waste. The referee redid Corollaries 1, 2(a) and 3 in closed
form for all M.

**Corollary 1.** g = w + ζx takes each value once, so for each integer N the set {g ∈ [N − δ′, N + δ]} has length
≤ (δ + δ′)/ζ, and at most ζL + 1 + δ + δ′ integers matter: |A| ≤ (δ + δ′)(2 + δ + δ′)·L when ζL ≥ 1. Take
δ = δ′ = 1/24 (|A| ≤ 0.174·L) and τ = min(0.08, √(δ′/(0.502·M))).

**Corollary 2.** (a) g ≡ m + ½, δ = δ′ = 2/5: A is empty, and τ = √(δ′/(0.502·M)) ≤ 0.08 for M ≥ 125.
(b) g ≡ M with fractional part f: take δ = min(f, 4/5)/2 and δ′ = (1 − f)/2. Then δ < f and δ′ < 1 − f, so no
integer N has N − δ′ ≤ M ≤ N + δ and A is empty. With τ = min(0.08, √(δ′/(0.502·M))) the theorem reads
L ≤ W/δ + 1350·W/τ + √(21·τ·M·L·W). Put q = min(f, √((1 − f)/M)), κ = 5·10⁻⁵ and suppose W ≤ κqL; it
suffices to show that the right side divided by L is < 1 at W = κqL (it is increasing in W, and the left side is
L). Here q/δ ≤ 2.5 (δ = f/2 ≥ q/2 if f ≤ 4/5, δ = 2/5 and q < 1 otherwise), and τ = min(0.08, a) with
a = √((1 − f)/(1.004·M)).
If τ = a: q/τ ≤ √1.004 and τMq ≤ (1 − f)/√1.004, so the right side over L is
≤ 2.5κ + 1350κ√1.004 + √(21κ/√1.004) < 0.101.
If τ = 0.08 ≤ a: q/τ ≤ 12.5 and M ≤ (1 − f)/(1.004·0.08²), so again τMq ≤ 0.08·√(M(1 − f)) ≤ (1 − f)/√1.004 and
the right side over L is ≤ 2.5κ + 1350·12.5κ + √(21κ/√1.004) < 0.877.
(The script also finds the least W/L allowed on a grid of (f, M) to be ≥ 9·10⁻⁵·q; the proof does not use it.)
For a square of side x with f ≤ ½, q ≥ min(f, 1/√x)/√2.

**Corollary 3.** Rotate the trapezoid so that the side of length h is the floor; then g is affine, L = h, the rise
is r and M = w + r.

**Remark 6.1 (a slab on a grid; not proved).** Theorem S might also hold when the floor is not a wall but the top
edge of a row of axis-parallel squares of the packing lying below the line y = 0 (the region being convex): paths
would start on those top sides and the floor case of Lemma 2.2 would be replaced by the square case. This is a
conjecture, not a result. Missing: (i) the top sides of the row must cover the starting set [0, L] up to a null
set, which needs a hypothesis on the row; (ii) the rectangles R(S, S′) with S in the row reach below y = 0, so
waste there is charged, and the region and the waste W in the theorem must be redefined to include it; (iii) the
multiplicity counts of Corollary 2.3 and Lemma 4.2 (21 squares, 4 floor pairs, 1350) must be redone.

**McClenagan's frame.** For a side x with fractional part ½: an N × N grid plus strips of width h, each packed on
its own, costs ≥ c·x/√h by Corollary 2(b), because the strip is an x × h rectangle and h has the fractional part of
x. McClenagan fills the strip with stacks spanning it, which leaves end trapezoids of height h and width ≍ √h,
packed on their own; by Corollary 3 these cost ≥ c·h^{3/4}. So his frame costs ≥ c·max(x/√h, h^{3/4}) ≥ c·x^{3/5}
for every h ≥ 1 (Corollary 2(b) assumes M ≥ 1) and every filling of the strip and of the trapezoids. Both pieces of that frame are optimal as regions.

**Bui's and Ryu's walls.** These are wider. Bui's right trapezoid has height x, base x^β with β = 3/4 and slope
x^{−1/2}. Ryu's E38 sets D_ℓ = ⌊c_D·m^{3/4}⌋, D_r = ⌊c_R·m^{3/4}⌋, so his walls Z_L, Z_LR, Z_UR have length ≈ m, slope
≍ m^{−1/2} and width ≍ m^{3/4} (the referee reads his hypothesis (W2) as forcing that width). For such a wall
Corollary 1 gives only c·m/√(m^{3/4}) = c·m^{5/8}, against the O(m^{3/4}) of their fillers. So this note leaves open
that a better wall filler improves those frames: walls at m^{5/8} would give x^{5/9} for Bui's frame, b^{5/9} for
Ryu's end and k^{5/14} for c*(k). Whether that is possible is Bui's Conjecture 1 at β = 3/4, γ = ½; he conjectures
it is not.

**Ryu's end region.** In k2-minus-c-upper the band end is Reg(y) = {0 ≤ x′ ≤ w, 0 ≤ y′ ≤ y + (x′ − σ)tan θ} with
σ = sin θ, w = b cos θ + σ, tan θ ≈ 2/b and a lift y; any family of squares in Reg(y) may be used. His end cost E is
the uncovered area of Reg(y) plus ½tan θ. For y ≥ 1 this is the setting of Corollary 1 with L = w, rise
w·tan θ ≥ b sin θ > 1.6 and M = y + b sin θ, about y + 2 for the tilts he uses. So

    E ≥ 4·10⁻⁵·w/√(y + b sin θ)   for every packing of Reg(y), every lift y ≥ 1.

His Theorem 1.1 (the k^{3/8} bound) uses columns of m ≍ b^{4/5} squares spanning Reg(y), with y ≍ b^{4/5}; for that
region his end cost O(b^{3/5}) is optimal up to a constant, whatever is put into it, and an end cost b^{3/5 − ε} needs
a lift y ≥ b^{4/5 + 2ε}. His §12 asks for "a direct argument that some end cost of order b^β with β > 0 is unavoidable
in this frame". This is a partial answer only: lifts are free in his frame (they may be of order k), and for
y ≳ b² the bound says nothing.

## 7. What is still open: thick regions

*Note (v0.3).* This section is an outline kept for the record. It is superseded by `docs/wedge-lower-bound.md`, which
states the theorem with 0 < ζ ≤ 1 and treats the case where N changes between neighbouring paths (the ΔN term
missing below) as the "skip" alternative of its Lemma 6.3. Two statements below are wrong as written; they are
corrected in place.

Theorem S only sees that the thickness is not an integer; it gives L/√M, which decays with M. Every lower bound in
Section 6 is escaped by a region that is thick compared with its rise: a wall of height h, lean √h and width ≫ √h
(Bui, Ryu), or an end region with a large lift.

The statement that would close this door was conjectured by Bui (arXiv:2508.04603, §6.3):

**Conjecture B (Bui's Conjecture 1).** A right trapezoid of height L whose bases differ by R ≥ 1, with slope
0 < ζ = R/L ≤ 1, wastes ≥ c·√(LR), whatever its width. (Bui: height x, difference x^{1−γ}, waste not o(x^{1−γ/2}).)
Without ζ ≤ 1 this is false: the triangle with L = ε, R = 1 and width 0 has area ε/2, so the empty packing has
W/√(LR) = √ε/2 → 0.

By Corollary 1 it holds when the width is O(R) and L ≥ R². In general it says that each unit of rise costs
√(L/R), the price the layers construction pays (`k2c-exponent-probe.md`, finding 5), and it would make h^{3/4}
unavoidable for a wall of height h and lean √h however much room is left beside it. Bui notes that the obvious
proof, a constant waste in each of the √(LR) sub-trapezoids of unit rise, fails when the trapezoid is wide (his
Fig. 16), and that even the conjecture would not bound W(x), since a packing need not contain such trapezoids.

Why the present proof does not give it, and a route that might (an outline, not a proof):

* Deficits. In a thick region D is not small, so arrival heights are not quantized. But D is constant on each
  itinerary interval, and by (3.1) the gap count G then grows at rate ζ along the interval. G ≤ δ, so G has to drop
  by about 1 per unit of rise at the boundaries between itineraries, and a drop is a change of D between neighbouring
  paths, |ΔD| ≤ τ·Σ_j θ(Z_j, Z_j′) over laterally adjacent squares. Lemma 2.2 applied sideways charges that to the
  waste: drops of total size R cost ≥ c·R/τ, unless a fraction of the paths meets a steep square, which costs
  ≥ c·Lτ. Choosing τ = √(R/L) would give √(LR).
  *Wrong as written:* by (3.1) for two paths ΔG = Δg − ΔN + ΔD, and the outline drops ΔN. Example: L = 4,
  g = 1 + x/2, axis-parallel squares [k, k+1] × [0, 1] for k = 0, …, 3 and [k, k+1] × [1, 2] for k = 2, 3. Then
  for the untruncated vertical paths D ≡ 0, N = 1 and G = x/2 on (0, 2), N = 2 and G = x/2 − 1 on (2, 4): G drops by 1 at x = 2 with no tilt anywhere.
* Lateral deaths. Lemma 4.3 needs the number of squares, which is what limits it to thin regions, and it is sharp for
  the vertical flow: in the lattice packing with basis u − ℓ·n, n + ε·u (tilt a, ε ≤ ℓ·tan a), every square has a
  hole of area εℓ and loses paths of measure ε per level. The cure is Ryu's rule of continuing straight along n_Z
  through gaps; then a lateral hit forces θ(Z, Z′) > 0 and is charged through Lemma 2.2. That costs injectivity and
  exact conservation of measure, which is much of the work in his 108-page paper.
* Bad intervals between good ones need the sideways lemma for squares that are far apart (a chain along a horizontal
  line inside the tube of dead paths).

None of this is done, and I would not bet on having found every case.

## 8. Checks done

* `python3 -I tools/slab_constants.py` recomputes the counts behind 1350 and 21 and verifies the corollaries on
  grids. It checks the arithmetic behind the constants, not the geometry.
* `python3 -I tools/slab_flow_check.py` (written by Codex from the definitions in Sections 3–5) runs the flow by
  exact ray casting on 22 explicit packings and 200 parameter settings: rows, brick rows, Erdős–Graham stacks, the
  lattice with holes of Section 7, rows parallel to a sloped ceiling, staircases, randomly perturbed packings, and
  hand-built overhang, vertex-contact and wall-hugging cases. No check failed: the height identity and the
  translation property hold to 10⁻¹⁴, arrival images do not overlap, measures agree with a backward trace from the
  ceiling to within the grid tolerance, and Lemmas 4.1–4.3, the inclusion of arrivals in A and Theorem S hold in
  every row. Results: `runs/k2c-exponent-2026-11-09/flow-check.md` (not in git). The constants 1350 and 21 are far
  from tight on these examples, so this tests the flow, not the constants.

## 9. Referee reports

* `docs/slab-lower-bound-review-2026-11-09.md`: blind adversarial read by Claude Opus 5.5 of v0.1. Verdict "sound
  with fixes". Every lemma, Section 5 and Corollaries 1–3 were rederived and found correct. Applied in v0.2:
  1. (Fatal for a conclusion, not for the theorem.) v0.1 said the wall trapezoids of Bui, McClenagan and Ryu all
     have width O(√h), so that all three fillers are optimal. That is true of McClenagan's only; Bui's and Ryu's
     walls have width ≍ h^{3/4}. Sections 0 and 6 now say so.
  2. The answer to Ryu's open problem is partial (free lifts). Stated as such.
  3. Conjecture B is Bui's Conjecture 1; credited, with his Proposition 3, Conjecture 2 and Question 1.
  4. Ryu's k^{3/8} theorem is his Theorem 1.1, not 1.2.
  5. Lemma 3.1(a): G is concave, not affine, when a gap ends on the ceiling.
  6. Flow step 6: any vertex makes x exceptional.
  7. Ryu's E is the uncovered area plus ½tan θ.
  8. Corollary 2(b) is now stated, argued and checked by the script.
* `docs/slab-lower-bound-judge-codex-2026-11-09.md`: a second, blind judge (Codex, fresh session, told to assume
  there is an error) read v0.2 alone. It re-derived Theorem S, the fundamental lemma (Lemmas 2.1, 2.2) and all
  corollary constants, and found no fatal error. Gaps it marked, repaired in v0.3: Lemma 2.1 at φ = 0; the count
  in Corollary 2.3 when S₂ is the floor or a wall; the finiteness details of Lemma 3.1(a); the Jacobian-1
  parametrisation behind the measure statements of Section 3; Corollary 2(b) resting on a grid (now proved in
  closed form) and the missing h ≥ 1; Remark 6.1 (now marked not proved). Errors it found, both in the outline of
  Section 7: Conjecture B needs ζ ≤ 1, and the deficit argument omits ΔN. It could not check the cited
  constructions of Bui, McClenagan and Ryu from this note alone.
* Both readers are AI models. No person has read this note.
