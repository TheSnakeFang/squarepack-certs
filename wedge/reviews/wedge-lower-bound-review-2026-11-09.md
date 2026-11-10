# Referee report: `docs/wedge-lower-bound.md` (draft v0.1, 2026-11-09)

Referee: Claude Opus 5.5 (adversarial read), 2026-11-09. The note was not edited.

**Overall verdict: sound with fixes.** I went looking for the hole and did not find one. I rederived every lemma,
the arithmetic, and the reduction to Bui's Conjecture 1. What I found is a set of small gaps and misstatements, all
fixable in a sentence or two. Nothing below is FATAL. That is a weaker statement than "the proof is right": it is one
reader's afternoon against the author's afternoon. The existing numerical audit does not test the main line (finding
8), so a second blind referee and a non-vacuous numerical test are still needed before anyone calls this proved.

## Findings, most severe first

1. **GAP (easily fixed), §1 and Cor. 4.5: the wall case of the fundamental lemma is not in [S].** [S, Lemma 2.2]
   covers square–square and square–floor only. The note uses R(Z, wall) and "θ/50 of waste" for the side walls
   without proof. The fix: for the right wall, reflect the floor case. From every point of Ω the horizontal segment
   to the right wall lies in Ω, because g is increasing. Every square lies on the left of the wall (so Z ⊂ {s ≤ ℓ}),
   and the rest of the proof of Lemma 2.2 is unchanged. Cor. 2.3 then holds with ℓ ≤ √2/2 + δ. For the left wall the
   note's exception is right: R ⊂ Ω iff y_c + ½ ≤ w. The count "at most two" is right, but the stated reason ("box of
   side 0.72") is not the right box. A flat square whose probes reach x = 0 has its top-left vertex at x ≤ δ·sin τ, so
   x_c ∈ [0.5, 0.55]. The exception needs y_c > w − ½, and the ceiling above the top-right vertex bounds y_c above,
   giving y_c ≤ w − ½ + 1.1ζ. Centres at least 1 apart in a 0.05 × 1.1 box: at most two. The bound
   2·δ·tan τ < 0.01 is right.

2. **MINOR, Lemma 3.1(a): stated too strongly.** The itinerary is not constant on each component of the complement of
   the exceptional set. It changes where an emitter point enters or leaves the conflicted set, where G + r* = δ, and
   where a probe switches between a square and the ceiling or a wall (that switch is usually at a vertex, but a
   conflict or gap threshold is not). These points are finitely many by the argument given. Fix: exclude them too.
   Then the J_k are the arriving cells of the refined partition, and nothing downstream changes (Lemma 6.1 only needs
   G̃ affine on each J_k, and boundaries with Δ_k = 0 are allowed). The numerical audit hit the same ambiguity (its
   "Ambiguities", item 1).

3. **MINOR, flow step 4: the ceiling case for the emitting square.** If a flat square has its top side on the ceiling
   (possible when |φ_Z − ζ′| = 0 and ζ′ < τ), then r* = 0, q = e lies in Z, and "on the ceiling and in no square" is
   false. Steps 5–7 do not apply either, so the flow is undefined there. Fix: "in no square other than the emitting
   one" (likewise for walls). This is a set of positive measure in that edge case, so it should be fixed, but it is
   just an arrival with γ_N = 0, and (3.1) holds.

4. **MINOR, Cor. 4.5: the distance for conflicts.** For a conflict the two probes meet at a point within δ of Z₁ and
   within δ of Z₂. So the squares are within 2δ, not δ, and the centres within √2 + 2δ. That is still ≤ √2 + 2/5, so
   Cor. 2.3 applies and the constants do not change.

5. **MINOR, §8, second clause of the first bullet ("first two terms of his Conjecture 2").** Bui's Conjecture 2 is
   for all β, γ ≥ 0. Theorem B and [S] both need rise ≥ 1, and Theorem B also needs ζ ≤ 1. So the two exponents are
   lower bounds only for γ ≤ 1 (with the implied constants such that R ≥ 1, and ζ ≤ 1 when γ = 0). For γ > 1 the
   rise tends to 0, neither result applies, and the R ≥ 1 hypothesis really is needed: Bui's Fig. 16 sub-trapezoids
   have rise x^{−γ/2} < 1. State the range.

6. **MINOR, §8, "Frames" bullet on Ryu.** The bound max(b/√m, m^{3/4}) needs two things the sentence leaves out.
   (i) The b/√m term is [S] applied to Reg(y), so it needs the lift to be O(m), that is, thickness ≍ m. That is the
   free-lift caveat of the [S] review, finding 2. (ii) The m^{3/4} term needs the wall region (Ryu's Z_L, a right
   trapezoid with L = g₀ ≈ m and rise g₀·tan α ≍ √m; I checked this against his lines 1759–1777) to be packed on its
   own. "For that kind of end" covers (ii), but (i) should be said. The conclusion b^{3/5} → k^{3/8} is correct under
   both.

7. **NIT, §8, Ryu's end region.** For lifts y < σ·tan θ we get g(0) < 0, so Reg(y) is not of the form in §0. It is a
   right trapezoid (a triangle) over a floor shortened by less than σ, with rise ≥ 1.6 − o(1). Theorem B applies after
   a translation. The claim "≥ c·√b for every lift y" stands, and so does the answer to Ryu's open problem (his
   lines 2398–2399). E(y) is at least the uncovered area, as the [S] review checked.

8. **NIT (about the evidence, not the proof).** `runs/k2c-exponent-2026-11-09/wedge-flow-check.md` (27 packings,
   162 rows, 0 failures) checks the flow lemmas well: identities, ordering, densities, conflicts, laterals. It does
   not test the main line. The hypothesis of Prop. 7.1 held in 0 rows. Every layers row with δ = 1/32 has arriving
   measure 0. Lemma 6.3 is exercised on only three rows, at δ = 1/8. The ratios drop/(τΘ) ≈ 4–10 in its layers table
   are skip boundaries (for example N = 75 → 76, Δ = 47), not failures. A useful next test is a genuinely low-waste,
   flat layers wedge (W ≈ c√(LR), all tilts < τ, most paths arriving), so that Lemmas 6.1, 6.3 and 5.1 are actually
   used.

9. **NIT.** Lemma 4.3 counts two lateral sides, but for a given ordered pair only one is reachable (the probe
   direction has a fixed sign of s-component). Harmless overcount. Lemma 5.1's constant is √2·50·210 + 0.4 = 14849.6
   ≤ 14851. In Prop. 7.1 the last line gives 0.4696·R ≤ 21216·τW, which implies the stated 0.47·R ≤ 21300·τW.

## Per-lemma verdicts

* **Flow (§2): correct with fix 3.** The entry-side argument is right: n·ν ≤ 0 means bottom side or one lateral side.
  The r* = 0 argument (two half-discs at a common relative-interior point force a common line, hence parallel
  squares and the bottom side) is right. Heights increase, and no square is revisited.
* **Lemma 3.1: (a) correct with fix 2; (b) correct.** The hit point satisfies Δs′·u_i = Δs·u_{i−1} + c·n_{i−1}. Dotting
  with u_{i−1} gives Δs′ = Δs·sec θ. The floor gives sec φ₁. Zero-length probes force θ = 0, so the factor is 1.
  Every factor is ≥ 1 and positive. **(c) correct**: the height adds cos φ_i per crossing and γ_i·cos φ_i per gap.
  **(d) correct**: cos φ + ζ·sin φ = cos(φ − ζ′)/cos ζ′. N = 0 gives κ′ = 1. ζκ′ ≥ ζ·cos ζ′ = sin ζ′. The ceiling is
  a line, so γ_N is affine. (This is unlike [S], where it was concave.)
* **Lemma 3.2: correct.** I checked every case asked about. Probes of the same square after different histories
  are parallel and start at distinct points of a segment they are perpendicular to, so they are disjoint. A
  zero-length probe meeting another probe is a measure-zero conflict. Probes ending on the ceiling or a wall at the
  same point are a conflict. A gap death partway along a probe is fine, because conflicts are defined with the whole
  geometric probe (length min(r*, δ)), whether or not any path travels it. That is conservative and is exactly what
  the second case needs. Floor probes stay below δ, and square tops are at height ≥ cos τ. "Probe end vs crossing
  end" is impossible because n·n_Z > 0. The ordering follows from disjoint graphs over height.
* **Lemma 3.3: correct.** Slope ≥ 1 plus injectivity of entry points.
* **Lemma 4.1: correct.** Pieces sweep κ_j·dx × length, are disjoint, and lie in the waste.
* **Lemma 4.2: correct.** The [S] proof transfers: consecutive centres are ≤ √2 + δ apart, the first centre is at
  height ≤ √2/2 + δ, Σ_{S′} μ(S, S′) ≤ 1 by Lemma 3.3, and the counts 21 and 4 are unchanged.
* **Lemma 4.3: correct** (with an overcount, NIT 9). θ = 0 gives no relative-interior lateral end. The floor is the
  case θ = a(Z₂).
* **Lemma 4.4: correct.** The case split on t⁰ < 1, t⁰ ≥ 1 with s⁰ ∉ (0, 1), and t⁰ ≥ 1 with 0 < s⁰ < 1 is complete,
  because t⁰ ∈ [1 − δ, 1 + δ] is forced. In the third case the interior point e − r′·n_{Z₁} gives the δ·tan θ
  bound. 4·tan(0.16)·sec(0.16) = 4.09 ≤ 4.3. Three-square situations reduce to pairs by the union bound.
  Square–floor conflicts are impossible. I tried to build a large crossing set: tilting Z₁ towards Z₂, or raising
  Z₁'s corner above Z₂'s top, is capped by the requirement that the crossing below e avoids (0, 1)². A Monte Carlo
  over 40,490 random non-overlapping pairs (scratch `l44.py`) gave a maximum of 0.99·δθ for the B₂-meeting superset
  of conflicts (claim ≤ 4.3·δθ) and 1.04·δθ for lateral ends (claim ≤ 2.02·δθ).
* **Corollary 4.5: correct with fixes 1 and 4.** 50·(6.32·420 + 8.08 + 8.08) = 133,528 ≤ 134,000. 32 + 4172.8 ≤ 4250.
  The 420 counts ordered pairs among the 21 squares in B(p, 2.61); R is symmetric in c₁ and c₂.
* **Lemma 5.1: correct.** The tubes are disjoint by Lemma 3.2 and x_k^+ < x_{k+1}^−. For y ∈ Y_i, λ_k(y) lies on the
  crossing of Z_i and ρ_k(y) on that of Z_i′, so C starts in Z_i and ends in Z_i′. C is in Ω by convexity. A pair is
  consecutive on at most one C at a height, because its gap on the line is one interval and the C's are disjoint.
  Bad heights: #bad ≤ (5/2)·(line waste), and θ_i < 2τ. If (k, y) is not bad, every gap is < 2/5, so centres are
  ≤ √2 + 2/5 apart. 210 = C(21, 2). This is in effect the general fact "∫ (tilt variation along horizontal lines) dy
  ≲ W", which is true by Cor. 2.3.
* **(6.1): correct.** Φ = −P + G̃. Φ(a_{k+1}^+) − Φ(b_k^−) = ζΔ_k ≥ 0 by Lemma 3.2. drop_k ≤ δ because G̃ ∈ [0, δ].
* **Lemma 6.1: correct** (telescoping).
* **Lemma 6.2: correct.** |h_i − h_i′| ≤ Σ_{l<i} sin τ·θ_l + δ < ¼ + δ, and cos 0.08 − 0.2813 = 0.7155.
* **Lemma 6.3: correct.** The pairing by index is legitimate because it only bounds a difference of two sums term by
  term. What makes it useful is Lemma 6.2, and both paths are arriving, so all their levels exist. Non-aligned
  levels form a suffix, so Θ_k ≥ 1/(4τ) in that case. All three cases N′ = N, N′ < N and N′ > N check, with
  1 − cos τ ≤ 0.51τ². N′ = 0 or N = 0 is consistent (the case cannot have drop > 0).
* **Proposition 7.1: correct.** The image of 𝒢 has measure ≥ cos ζ′·|𝒢| ≥ 0.53L, so ΣΔ_k ≤ 0.47L. There are at most
  0.94R skips, each with drop ≤ δ. Every non-skip boundary with drop > 0 has drop ≤ τΘ_k by Lemma 6.3. The bound
  0.53R − 1/32 ≥ 0.499R uses R ≥ 1. The constant is 14851/0.7 = 21216.
* **Theorem B: correct.** τ = 10800W/L ≤ 0.0756, 1350W/τ = L/8, 4250W ≤ 0.03L, and 0.01 ≤ 0.01L. Then
  W² ≥ 0.47LR/(21300·10800) gives W ≥ 4.5·10⁻⁵·√(LR). The other branch uses R ≤ L. W = 0 gives a contradiction.
* **Hidden assumptions (2h).** ζ ≤ 1 is used for sin ζ′ ≥ ζ/√2 and for R ≤ L. R ≥ 1 is used essentially (−δ and the
  skip term), which is consistent with Bui's Fig. 16. w = 0 is fine: the box argument of finding 1 does not use w.
  Very small or very large width: nothing depends on w. Non-integer L: not used. Squares flush with a wall have
  a(Z) = 0 and lose no measure.

## Attempts to refute the theorem

* **Layers (probe §2).** These are consistent and tight up to constants. Adjacent paths that differ by one swap of a
  tilted square for an upright one have ΔD = q ≈ α²/2 and Θ_k ≈ α (or 2α after an index shift), so drop ≤ q ≤ τα
  holds when α < τ. About R/q boundaries are needed, so ΣΘ_k ≈ 2R/α, which is the layer-end triangle cost in
  W ≈ Lα + 2R/α. The proof picks τ ≍ W/L ≍ α (times 10⁴), the scale at which layers are optimal.
* **Bui Fig. 16** (o(1) waste in a sub-trapezoid of length x^{γ/2}). Its rise is x^{−γ/2} < 1, and it is not a
  packing of the sub-trapezoid: squares cross its floor and ceiling. It is excluded on both counts. Gluing such
  pieces to reach rise ≥ 1 would give o(√(LR)) inside a larger packing. The theorem does not contradict that, because
  the proof uses the floor and ceiling as genuine boundaries and the walls for ΣΔ_k ≤ 0.47L.
* **Thick regions, an integer distance L between the walls.** Axis rows fill everything up to ⌊w⌋. What is left is
  thin, and [S] gives L/√R there, which is ≥ √(LR) when L ≥ R². A tilted lattice aligned with the ceiling moves the
  problem to the floor. A lattice with holes (the [S] §7 example) has Θ_k = 0, so it gets only skips, and most of
  its paths die. That matches its waste of about L/2.
* **Bui §4, McClenagan, Ryu E38.** All have waste ≳ √(LR) for their trapezoids (h^{3/4} at rise √h). The §6.4
  sentence "Θ(x^{1−γ})" in Bui is a typo for x^{1−γ/2} (his §4 says x^{1−γ/2}). I found no construction below
  c·√(LR).

## Section 8

* **Bui's Conjecture 1** ("a right trapezoid with height x and difference between two bases Θ(x^{1−γ}) cannot be
  packed in o(x^{1−γ/2})", 0 < γ < 1, arXiv:2508.04603v2 §6.3). Theorem B implies it: L = x, R ≍ x^{1−γ}, so
  R ≥ 1 and ζ ≤ 1 for large x, uniformly in the width. Correct.
* **Conjecture 2 terms:** correct only for γ ≤ 1 (finding 5).
* **Walls:** correct. Bui's and Ryu's walls are right trapezoids with L ≍ m and R ≍ √m.
* **Frames:** correct for Bui and McClenagan, given [S, Cor. 2(b)] (refereed earlier). Ryu: finding 6.
* **Ryu's end region:** correct (finding 7). "Not claimed: W(x) or c*(k)": correct, and it matches Bui's own remark.

## What I verified versus only read

Derived myself: every statement in §§1–7, including all the case analyses, the constants, and the arithmetic of
Theorem B. The wall extension of Lemma 2.2 and the two-square bound at the left wall. A Monte Carlo of Lemmas 4.3
and 4.4. The tightness check against layers. The geometry of Ryu's Reg(y) and Z_L (paper.tex lines 620–640 and
1759–1777).

Taken as given: [S, Lemma 2.2 and Cor. 2.3] for square–square and square–floor (refereed earlier).

Read only: Bui's statements of Conjectures 1 and 2, Fig. 16 and §4 (from the extracted text of the arXiv PDF, not
the figure). Ryu's open-problem sentence. The output of the existing wedge flow audit (I did not rerun
`tools/wedge_flow_check.py`).

Scratch: `(local scratch path removed)`.
