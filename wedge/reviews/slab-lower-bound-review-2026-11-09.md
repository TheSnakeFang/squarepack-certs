# Referee report: `docs/slab-lower-bound.md` (draft v0.1, 2026-11-09)

Referee: Claude Opus 5.5 (adversarial read), 2026-11-09. The note was not edited.

**Overall verdict: sound with fixes.** I could not break Theorem S or Corollaries 1–3, and I rederived every step
listed below. The catch is in Section 6 (and the matching sentence in Section 0). Bui's and Ryu's wall
trapezoids have width ≍ h^{3/4}, not O(√h). So Corollary 3 does not apply to them, and the claim that "the
wall filler of all three papers is optimal" is false for two of the three papers. Conjecture B is Bui's
published Conjecture 1, and the note does not credit it.

## Findings, most severe first

1. **FATAL (for the stated conclusion; Theorem S itself is unaffected).** The claim in §0, lines 27–30, and §6,
   lines 270–278, that the wall trapezoids of Bui, McClenagan and Ryu have width O(√h), so that Corollary 3 makes
   their wall fillers optimal and "the three papers stop at 3/5 because both pieces of the frame are already
   optimal as regions", is wrong for Bui and for Ryu.
   * Bui (arXiv:2508.04603v2, §4): "a right trapezoid with height x, base Θ(x^β), slope of right edge Θ(x^{−γ})",
     specialised to γ = 1/2, **β = 3/4**. The base is x^{3/4} and the lean is √x.
   * Ryu (k2-minus-c-upper v1.1, construction E38, lines 1683–1702): D_ℓ = ⌊c_D m^{3/4}⌋ and D_r = ⌊c_R m^{3/4}⌋. The
     wall Z_L has χ = ξ₀ − g₀ tan α ≈ D_ℓ (width ≍ m^{3/4}), ζ = tan α ≍ m^{−1/2} and L = g₀ ≈ m. Z_LR and Z_UR have
     χ ≈ D_r. My reading of hypothesis (W2) of Lemma W also suggests that this width is forced: with tan α₀ = a_w√ζ,
     (W2) needs N₀ ≳ m^{3/4}.
   * McClenagan (arXiv:2602.01484, §4): "T has a width on the order of √h". Only this paper fits Corollary 3.

   For a wall of height m and width m^{3/4}, Corollary 1 gives only c·m/√(m^{3/4}) = c·m^{5/8}, against the
   O(m^{3/4}) cost of the construction. So the note does not exclude that better wall packings would improve the
   frames of Bui or Ryu: max(b/√m, m^{5/8}) would give b^{5/9} per end. The sentence "b/√m for the slab and m^{3/4}
   for a wall … give … k^{3/8} for his frame" has no support. The note itself hedged this point (lines 274–275), and
   the hedge was right. Fix: restrict the optimality claim to McClenagan's frame. For Bui and Ryu, say that the
   walls are the thick case of §7, and that Conjecture B (= Bui's Conjecture 1) is what would be needed.

2. **GAP (overclaim), §6 lines 263–266.** The note says Ryu's open problem ("a direct argument that some end cost of
   order b^β with β > 0 is unavoidable in this frame", line 2396) "has this answer". In his frame the lifts are free:
   Lemma 6.1 and Prop 6.3 only need y₀, y₁ ≥ 0 with y₀ + y₁ = L_b − h − (R−1)d, so a lift can be of order k. Theorem S
   gives b/√y, which says nothing once y ≳ b². This is a partial answer, conditional on y ≤ b^λ with λ < 2, and it
   should be stated that way. The specific statement for Ryu's own choice y ≍ b^{4/5} (end cost Θ(b^{3/5}) is
   optimal for Reg(y)) is correct.

3. **MINOR (novelty or credit).** Conjecture B (§7) is Bui's Conjecture 1 (arXiv:2508.04603v2, §6.3): "a right
   trapezoid with height x and difference between two bases Θ(x^{1−γ}) cannot be packed in o(x^{1−γ/2})". This is
   √(LR) with R = x^{1−γ}. Bui also discusses why the naive proof fails (his Fig. 16). It should be credited. In
   return, Corollary 1 proves Bui's conjecture in the range γ ≥ 1/2 when the base is O(x^{1−γ}), which includes
   his main case γ = 1/2 with base O(√x). That is worth saying. Bui's Proposition 3 (an Ω(√x) lower bound for a thin
   parallelogram, using the fundamental lemma along paths, via Bui arXiv:2504.09489 Prop. 21) is a related earlier
   lower bound for a thin region and should be cited.

4. **MINOR, §6 line 264.** "His Theorem 1.2 uses columns of m ≍ b^{4/5}": in v1.1 that is Theorem 1.1
   (`thm:main38`). Theorem 1.2 (`thm:main`) is the k^{2/5} bound, with m ≍ b^{2/3}.

5. **MINOR, Lemma 3.1(a).** "G is affine in x on such an interval" is false when the current gap segment ends on the
   ceiling, because g is only concave there. Fix: G is then concave, so G = δ at no more than two points or on an
   interval where it is constant. The conclusion is unchanged.

6. **NIT, flow §3 steps 3–6.** The steps do not say what happens when q lies on two squares (for example in the
   relative interior of the bottom side of Z′ and at a vertex of a steep Z″). Fix: call x exceptional whenever q is
   a vertex of any square. E stays finite.

7. **NIT, §6 line 257.** "E is its uncovered area": in fact E(y) = A₀(y) − |C| = area(Reg(y)) + ½tan θ − |C|. I
   checked this by integrating. So E is greater than or equal to the uncovered area, which is the harmless direction.

8. **NIT, Corollary 2, general form (line 246).** The form W ≥ c·L·min(f, √((1−f)/M)) is stated without proof and is
   not checked by the script. I checked it by hand (finding 9). It is correct with a small absolute c. Note that
   for a square of side n + f with 1/n ≤ f ≤ 1/2, it gives min(nf, √n) ≥ √(n‖x‖). That is stronger than Roth–Vaughan
   for x just above an integer. If it is right, it deserves a sentence. If the author does not believe it, that
   tension is a reason to re-check the gap-death step at small δ. I found no error there.

9. **Script.** `tools/slab_constants.py` reproduces its output (1317 ≤ 1350, 20.17 ≤ 21, margins −0.142, −0.092,
   −0.147). It recomputes the note's own counting formulas, which are the areas of √2-neighbourhoods, and evaluates
   the corollary inequalities on a grid of M. It does not test any geometric lemma, so it tests "the arithmetic
   behind the constants", which is what the note says it tests and no more. I redid the corollaries in closed form,
   in the scratch script `(local scratch path removed)`.
   For M ≥ 13 (Cor 1) and M ≥ 125.5 (Cor 2), τ√M is constant, so the right side is constant apart from a term
   that decreases. For 1 ≤ M ≤ 13 I bounded the decreasing terms at M = 1 and the lateral term at M = 13. I get
   0.692, 0.734 and 0.853 against 0.826, 0.826 and 1. So the claims hold for all M, not only on the grid.

## Per-lemma verdicts (all rederived by me unless marked "read")

* **Lemma 2.1: correct.** Interior minimum: p, q ≥ φ, p + q ≥ 2, the weighted-harmonic minimisation, and the
  maximisation of 1/p + 1/q. I also sampled it at random (minimum ratio 1.000). It is identical to Ryu's Lemma 3.1
  (read).
* **Lemma 2.2: correct**, including touching squares and the floor case. The ordering on a chord is constant on each
  I_r without needing strict separation: the two closed conditions r_Z ≤ l_{Z′} and l_Z ≥ r_{Z′} partition the
  connected I_r. R ⊂ Ω holds by convexity of Ω₋ (floor case: B(c₁, ½) ⊂ Ω plus the vertical segments down to the
  floor). |T| ≤ m′ holds because τ⁺ − τ⁻ ≥ 1. The tan-difference bound needs ψ, ψ′ ∈ (−π/2, π/2), which holds. It is
  a faithful adaptation of Ryu's Prop 3.3 (read, lines 354–417).
* **Corollary 2.3: correct.** The neighbourhood area is 16.06, so at most 16 squares, 14 others; (2 − π/4)/60 =
  0.0202 > 1/50; √(1.814² + ¼) = 1.88 < 1.9. In the floor case ℓ ≤ 1.11, which is covered.
* **Flow (§3): correct with NIT 6.** The q = p argument is right: two closed half-discs whose boundary lines differ
  overlap, so a touching square at a relative-interior point of a top side is flat and is entered through its bottom
  side. The bottom side lies strictly below the top side (sin φ < cos φ), so no square is revisited.
* **Lemma 3.1(a): correct with fix 5.** (b) and (c): correct. (d): correct. I checked every case of the
  lowest-common-point argument, including zero-length gaps, where c is the upper end of one crossing and the lower
  end of the next. In that case c is reached "as the upper end of a crossing", and the two ways of reaching c really
  do exclude each other.
* **Consequences paragraph: correct.** Each itinerary interval maps x to the entry or arrival point by a
  translation, and images from different intervals are disjoint by (d). Bottom sides and the ceiling are graphs, so
  the measures are preserved. ∫G ≤ W holds by Fubini on finitely many intervals.
* **Lemma 4.1: correct.**
* **Lemma 4.2: correct.** Consecutive centres are at most √2 + δ apart, and the first centre is at height at most
  √2/2 + δ. Σ_{S′} μ(S, S′) ≤ 1 because each x has one successor of S and all such x cross S (measure ≤ cos φ_S).
  S ⊂ B(p, 2.607) (area 21.35, so at most 21). Floor box 2.414 × 1.814 = 4.38, so at most 4, each with μ ≤ √2.
  21 + 4√2 = 26.66 < 27. Reversed ordered pairs, if any occur, are counted under their own first element, which is
  harmless.
* **Lemma 4.3: correct.** The final gap has positive length: a steep lateral side cannot be parallel to a flat top
  side. The slope bound is cot a(Z′) − tan a(Z) ≥ cot τ − tan τ. The one-sided integral bound holds. The swept
  segments are disjoint up to null sets. There is no pair (Z′, Z′), because the top side of Z′ meets σ only at a
  vertex. The box neighbourhood has area 10.58, giving at most 10 squares including Z′, so at most 9 + floor = 10
  pairs. sτ·τ = 0.9915 at τ = 0.08, and 20/0.99 < 21.
* **Section 5: correct.** N cos τ ≤ Σ cos φ ≤ g(x′) ≤ M gives N ≤ M/cos τ. (1 − cos τ)/(τ² cos τ) is increasing and
  equals 0.5013 at 0.08. Arrival puts g(x′) in [N − δ′, N + δ], hence x′ ∈ A, and the measure is preserved.
* **Corollary 1: correct.** At most ζL + 1 + δ + δ′ integers, each giving length ≤ (δ + δ′)/ζ, and 1/ζ ≤ L, so
  |A| ≤ 0.1736L. τ ≤ 0.08 exactly when M ≤ 12.97. **Corollary 2: correct**, including the general form (finding 8).
  **Corollary 3: correct** as a statement about the trapezoid. Its application to Bui and Ryu is wrong (finding 1).
* **Remark 6.1: plausible, not checked in detail.** It needs the slab squares to lie above y = 0, which holds when
  the lower part is a perfect grid.
* **§6, Ryu's end region: accurate (read and checked).** Reg(y), σ, w and tan(θ/2) = b/(b² − 1) match lines 630–637
  and 1677. Rise = bσ + σ tan θ > 1.6 (b sin θ ≈ 2b²/(b² + 1) ≥ 1.6). M = y + bσ. Columns of m = ⌊ḡ⌋ + 1 squares and
  y ∈ [c_y b^{4/5}, c_y b^{4/5} + 2] (line 1800). Ryu's wall regions: overclaimed (finding 1). Erdős–Graham frame:
  accurate for McClenagan's version, false for Bui's (base x^{3/4}). The open-problem answer is overclaimed
  (finding 2).
* **§7 (outline only): nothing plainly false.** I checked these sentences: "for thickness O(R) and L ≥ R² this
  follows from Corollary 1" (L/√R ≥ √(LR) ⇔ L ≥ R²), and the lattice hole area (det = 1 + εℓ). Ryu's "O(δW) for
  merges" and "100-page paper" I could not verify; the evand repo lists Ryu [Q] at 108 pp.

## Novelty (about 20 minutes of searching)

* **Explicit Roth–Vaughan constant.** I found nothing better than RV's own c₀ = 10⁻¹⁰⁰. The evand repo
  (`literature/waste-bounds-2026-10-12.md`, which has read RV in full) records that c₀ is explicit, that the
  hypothesis is α(α − [α]) > 1/6, and that an effective constant is open (WISHLIST A13). The same file describes
  RV's argument as horizontal chains with the projection deficit Σ(1 − cos θᵢ) ≥ [α] + 1 − α, which forces tilt. The
  idea behind Theorem S is therefore RV's own. What is new is the injective flow and the measure bookkeeping.
  Web search (https://arxiv.org/abs/2504.09489, https://en.wikipedia.org/wiki/Square_packing,
  https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS7/html_1) found no improved explicit constant.
  Corollary 2 (5·10⁻⁴) appears to be new.
* **Lower bounds for trapezoids or thin rectangles.** Bui's Conjecture 1 (= Conjecture B) and Bui's Proposition 3
  (thin parallelogram, Ω(√x)) in https://arxiv.org/abs/2508.04603. I found no proved trapezoid bound of the form of
  Corollary 1 or 3.
* **evand/square-packing.** `tasks/k2c-exponent/README.md` models Ryu's frame and its walls, with no lower bound.
  `tasks/k2c-lower/README.md` is about c*(k) covers and lists Ryu's [T] and [Q] lower bounds, which are for the
  integer square, a different setting. Neither contains Theorem S.

## What I verified versus only read

Derived myself: every lemma above, the corollary arithmetic in closed form, E = W_Reg + ½tan θ, and the Ryu wall
geometry from his E1–E6.

Read only: Ryu's text, including my reading of (W2) as forcing width ≳ m^{3/4}; Bui's and McClenagan's statements
(extracted from the arXiv PDFs; I did not check their proofs); RV's content (second-hand, through the evand
literature note).
