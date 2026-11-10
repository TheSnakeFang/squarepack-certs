# Adversarial audit of Theorem B, Sections 5–8

Verdict: I find no unrepairable error in Sections 5–7, conditional on taking the literal statements of Sections 1–4 and [S, Lemma 2.2/Corollary 2.3] as given. The stipulated existence of a real error is not corroborated by this audit. Several Section 8 conclusions require additional results or geometric hypotheses; those are GAP, not verified consequences of Theorem B alone. No prior-check assertion was used. Only the two authorized source files were opened; no web search was performed.

## Verdict table

| Item | Precise claim audited | Verdict |
| --- | --- | --- |
| §5 tube construction | Ordered choices of arriving paths give tubes with disjoint interiors at common heights. | VERIFIED |
| Lemma 5.1, horizontal chains | At almost every height, endpoint orientation distance is bounded by the sum over consecutive squares on the intervening segment; uncovered length below 2/5 makes every such pair eligible for [S]. | VERIFIED |
| Lemma 5.1, multiplicity and constant | Summing over tubes and levels gives Σ θ_i\|Y_i\| ≤ 14851 W, independently of width and square count. | VERIFIED |
| Identity (6.1) | drop_k = P_k − P_{k+1} − ζΔ_k ≤ P_k − P_{k+1}, with Δ_k ≥ 0 and drop_k ≤ δ. | VERIFIED |
| Lemma 6.1 | Positive drops total at least sin(ζ′) times arriving floor measure minus δ. | VERIFIED |
| Lemma 6.2 | Every aligned pair of equal-index crossings has overlap length at least 0.7. | VERIFIED |
| Lemma 6.3, first unaligned level | If any common level is unaligned, τΘ_k ≥ 1/4 ≥ drop_k. | VERIFIED |
| Lemma 6.3, N′ = N | Every positive drop is at most τΘ_k. | VERIFIED |
| Lemma 6.3, N′ < N | A positive drop forces τΘ_k > 1/2, and hence is paid for. | VERIFIED |
| Lemma 6.3, N′ > N | Either drop_k ≤ τΘ_k or Δ_k ≥ 1/(2ζ). | VERIFIED |
| Proposition 7.1, arrivals and skips | Its hypothesis leaves at least 3L/4 arriving floor measure and at most 0.94R skips. | VERIFIED |
| Proposition 7.1, final constants | The drop and sideways bounds imply 0.47R ≤ 21300τW. | VERIFIED |
| Theorem B, positive small W | τ = 10800W/L is admissible and satisfies the proposition's hypothesis, giving W ≥ 4.52009…·10⁻⁵√(LR). | VERIFIED |
| Theorem B, large W, zero W, failed hypothesis | W > 7·10⁻⁶L is already sufficient; W = 0 is impossible; no unhandled failure of the proposition's hypothesis remains. | VERIFIED |
| §8, Bui Conjecture 1 | For x ≥ 1 and 0 < γ < 1, R = x^(1−γ) gives W ≥ 7·10⁻⁶x^(1−γ/2), uniformly in width. | VERIFIED |
| §8, combined two-term exponent | Combining Theorem B with the stated sloped-slab bound gives max(1 − max(β,1−γ)/2, 1−γ/2). | GAP |
| §8, walls and optimality | The wall lower bound is m^(3/4); optimality additionally requires the claimed matching fillers and their geometric identification. | GAP |
| §8, Bui/McClenagan frames | The stated strip and wall costs imply x^(3/5), provided the cited strip bound and frame decomposition hold. | GAP |
| §8, Ryu frames | The stated costs imply b^(3/5), and the stated identity then gives k^(3/8); applicability to his frame needs the external geometric and cost facts. | GAP |
| §8, Ryu end region | The translated region has waste at least c√b at every lift, provided tan θ ≤ 1, b sin θ ≥ 1, and sin θ ≍ 1/b; answering the cited open problem needs its external specification. | GAP |
| §8, scope limitation | A bound for independently packed trapezoids does not establish a bound for arbitrary square packings or arbitrary c*(k) constructions. | VERIFIED |

## Re-derivation of Sections 5–7

### Lemma 5.1

At a generic height, a square has a single horizontal chord. Disjoint tube interiors give disjoint horizontal segments C. On each path, crossing-height interiors are disjoint, so there is at most one relevant equal-index pair for a tube at that height. Convexity of Ω puts the entire segment C inside Ω. The squares on C form a finite ordered chain; the orientation metric triangle inequality bounds the endpoint angle by its successive angles. If the endpoints belong to the same square, the angle is zero and no chain charge is needed.

Let ℓ_w(y) be the length of uncovered Ω at height y. Each bad segment contains at least 2/5 uncovered length, so there are at most (5/2)ℓ_w(y) bad segments. Since both endpoint squares are flat, θ_i < 2τ. Integrating gives at most 5τW ≤ 0.4W.

For a nonbad segment, each full gap between consecutive square chords has length less than 2/5. Choosing the chord endpoints, each at distance at most √2/2 from its square centre, gives centre distance at most √2 + gap < √2 + 2/5. This is precisely the hypothesis of [S, Corollary 2.3]; a small horizontal gap does not require the squares to be flat.

The multiplicity assertion is valid almost everywhere: a segment spanning two consecutive chords must contain their intervening gap. Two disjoint segment interiors cannot both span that gap. If the gap has length zero, both spanning segments must contain the contact point in their interiors. The exceptions where an endpoint lies on a square boundary, or horizontal square sides cause degenerate chords, occur at finitely many heights for the fixed chosen paths and packing, and do not affect the integral. The same square cannot occur twice in the chain, by convexity. Thus a pair is charged at most once at a generic height, even for brick offsets and very wide tubes.

A square's vertical projection has length at most √2. Hence a fixed unordered pair is charged on a height set of measure at most √2. The rectangle R for that pair can be treated symmetrically in its endpoints. If p belongs to R, each whole square is contained in B(p,1.9 + √2/2) ⊂ B(p,2.61). This disk has area 21.400843… < 22; the disjoint square interiors therefore allow at most 21 squares and 210 unordered pairs. Tonelli's theorem, or simply finite summation followed by integration, now gives

    good contribution ≤ √2 · 50 · 210 W = 14849.2424049… W,
    total contribution ≤ 14849.6424049… W < 14851 W.

No bound on the number of squares, maximum ceiling height, tube width, or separation of the two arriving intervals is used.

### Identity (6.1) and Lemma 6.1

At consecutive interval ends, subtract Φ_left = −P_k + G̃_left from Φ_right = −P_{k+1} + G̃_right. Since the ceiling is affine,

    ζΔ_k = P_k − P_{k+1} − drop_k.

This establishes the sign in (6.1). Ordered arrival abscissas give Δ_k ≥ 0, and 0 ≤ G̃ ≤ δ gives drop_k ≤ δ, including negative drops without any absolute-value claim.

On J_k, integrate G̃′ ≥ sin ζ′. The exact telescoping identity is

    Σ_k [G̃(b_k−) − G̃(a_k+)]
      = Σ_{k<K} drop_k + G̃(b_K−) − G̃(a_1+).

The last difference is at most δ. Replacing signed drops by positive parts proves Lemma 6.1. For no arriving intervals the lemma is simply 0 ≥ −δ; for one interval it bounds its growth by δ. Thus the formula's empty-set notational convention is harmless.

### Lemma 6.2

For the two actual chosen paths, write the bottom-entry height as the sum of preceding cosines plus its accumulated vertical gap. Each accumulated gap lies in [0,δ], so their difference has absolute value at most δ, not 2δ. For common flat orientations,

    |cos φ − cos φ′| ≤ sin τ |φ − φ′| ≤ τθ.

Consequently an aligned level has |h_i − h_i′| < 1/4 + δ. Both crossing intervals have length at least cos τ, and the overlap of intervals of lengths at least c with starting points separated by d ≤ c is at least c−d. Thus

    |Y_i| ≥ cos(0.08) − 1/4 − 1/32
          = 0.7155517063… > 0.7.

This is uniform in the chosen points. The proof does not require them to be interval endpoints. Only the orientations and square counts, which are constant on the itinerary intervals, enter the later endpoint-drop estimate.

### Lemma 6.3

The aligned levels form an initial segment. If i₀ is the first unaligned level, all levels below it are aligned and their angle sum is at least 1/(4τ). Therefore τΘ_k ≥ 1/4 and every positive drop, at most δ = 1/32, is paid for. No assumption about later levels is needed.

Otherwise all common levels are aligned. Put A = τΘ_k. The elementary bound 1−cos t ≤ t²/2 ≤ 0.51τ² is valid for |t| < τ; it does not depend on square count.

* For N′ = N, D_k − D_{k+1} is a sum of matched cosine differences, bounded above by A. Identity (6.1) gives drop_k ≤ A.
* For N′ = N−j with j ≥ 1, positivity of drop_k and Δ_k ≥ 0 imply D_k − D_{k+1} > j. But D_k − D_{k+1} ≤ A + 0.51jτ². Hence A > j(1−0.51τ²) ≥ 0.996736 > 1/2 > δ ≥ drop_k. The written weak inequality is valid.
* For N′ = N+j with j ≥ 1, the extra j deficits have a minus sign, giving D_k − D_{k+1} ≥ −A−0.51jτ². If A ≥ 1/4 the drop is paid for. If A < 1/4, identity (6.1) gives

      ζΔ_k ≥ j(1−0.51τ²) − A − drop_k
            > 1−0.51(0.08)²−1/4−1/32
            = 0.715486 > 1/2.

  This proves the claimed skip alternative, including N = 0. It is essential to keep −ζΔ_k in (6.1); discarding it would lose precisely this case.

### Proposition 7.1

The hypothesis and the literal Corollary 4.5 give |𝒢| ≥ 3L/4. On each arriving interval the arrival map has derivative at least cos ζ′; distinct interval images are disjoint and ordered by Lemma 3.2. Thus their total measure is at least

    (3/4) cos ζ′ L ≥ 3L/(4√2) = 0.5303300859… L ≥ 0.53L.

The open gaps of lengths Δ_k are disjoint and miss these images. Hence ΣΔ_k ≤ 0.47L. Each skip consumes at least 1/(2ζ), so their count is at most 0.94ζL = 0.94R, without any rounding problem for an integer count. This is an arrival-image estimate; it does not incorrectly assume that the arrival map preserves floor measure.

For positive drops on nonskips, Lemma 6.3 forces payment. On skips, simply use drop_k ≤ δ, whether or not payment also holds. Therefore

    (3/4)sin ζ′ L − δ ≤ τΣΘ_k + 0.94Rδ.

Here sin ζ′ = ζ/√(1+ζ²) ≥ ζ/√2. Since R ≥ 1,

    (3/4)sin ζ′ L − δ
      ≥ [3/(4√2) − 1/32] R
      = 0.4990800859… R ≥ 0.499R.

The skip penalty is 0.94/32 = 0.029375 ≤ 0.0294. Lemmas 5.1 and 6.2 give ΣΘ_k ≤ (14851/0.7)W = 21215.7142857…W ≤ 21216W. Thus

    0.4696R ≤ 21216τW.

The final rounding is in the correct direction: 0.47·21216 = 9971.52 < 0.4696·21300 = 10002.48. Hence 0.47R ≤ 21300τW. All quantifiers permit choosing the path representatives before this argument; the bounds hold for every such choice.

### Theorem B and the failed-hypothesis issue

R = ζL ≤ L and R ≥ 1 imply L ≥ 1 and √(LR) ≤ L. If W > 7·10⁻⁶L, the asserted bound follows immediately. Otherwise, for W > 0, choose τ = 10800W/L. Then

    0 < τ ≤ 0.0756 < 0.08,
    1350W/τ = L/8,
    4250W ≤ 0.02975L,
    0.01 ≤ 0.01L.

The hypothesis sum is therefore at most 0.16475L < L/4. This proves that the proposition's hypothesis cannot fail in the only positive-W branch where it is needed. Applying it gives

    W² ≥ [0.47/(21300·10800)] LR,
    W ≥ 4.5200917415…·10⁻⁵√(LR) ≥ 7·10⁻⁶√(LR).

For W = 0, τ = 0.08 gives hypothesis 0.01 ≤ L/4 because L ≥ 1, and conclusion 0.47R ≤ 0 is impossible. Equality W = 7·10⁻⁶L is included in the small-W branch. The theorem is uniform for R close to 1, ζ approaching 0, ζ = 1, and arbitrary w ≥ 0. There is no regime L < 1 in its hypotheses. Large W needs no arrival argument at all.

### Numeric input checks

The slab rectangle distance cutoff is √2+2/5 = 1.81421356… < 1.82. Its √2-neighbourhood area is bounded by

    1.82 + 2√2(1+1.82) + 2π = 16.0793498… < 16.1 < 17.

Thus at most 16 unit squares meet it, leaving at most 14 besides the specified pair. The resulting coefficient (2−π/4)/(4·15) = 0.02024336… exceeds 1/50, and √(1.82²+1/4) = 1.8874321… < 1.9. These check the numerical use of [S]; they are not a substitute for its stipulated fundamental lemma.

The accepted death coefficient also rounds safely: 1/δ + 134000δ = 32+4187.5 = 4219.5 ≤ 4250. The number 1350 is used as the literal Lemma 4.2 input, not as a newly proved death estimate. The choice 10800 is exactly 8·1350. No claim that the entirety of Sections 1–4 was independently verified is intended.

## Counterexample attempts and regime tests

**Staircase of tilted columns on upright layers.** An added upright layer changes the column height relative to a tilted layer by 1−cos α, not by 1. This is represented by the matched cosine differences in D: a matched upright/tilted change costs at most τ|α|, which dominates 1−cos α for |α| < τ. If the common prefix angle sum becomes large, the first-unaligned-level argument already pays the whole drop. If a column instead adds an entire crossing, N changes; a positive unpaid drop with N′ > N then forces a missing arrival-height span of at least 1/2. The staircase therefore does not evade the skip count. If |α| ≥ τ, these paths need not arrive, and the accepted tilt-death estimate is the relevant alternative. This tests Lemmas 6.2–6.3 rather than silently assuming equal counts.

**Brick-offset rows.** With all orientations zero, every θ and D vanishes. Equal-count adjacent arrivals cannot have a positive drop. A downward jump in N cannot have a positive drop either. An upward jump can reset the gap only across a skip. Brick offsets do not duplicate a horizontal consecutive-pair charge: two disjoint tubes spanning the same gap would overlap. Thus they do not violate either Lemma 5.1 or the drop estimates.

**Two distinct tilts side by side.** The cosine difference satisfies the explicit τθ bound even with opposite signs of tilt. A long common prefix of mismatched tilts may destroy height alignment, but then τΘ ≥ 1/4. Before that happens each matched pair overlaps vertically by more than 0.7155. Horizontal intervening squares may have any orientations; the chain metric handles them. Small waste cannot make the angle sum free, by the fundamental-lemma integration in Lemma 5.1.

**One tilted block in an upright grid.** The angle changes at entry and exit of the block are charged by the same horizontal chain argument. If these lie in different tubes at the same height, their horizontal transition gaps are distinct. Reusing a pair over many heights costs at most √2 in the integral; its potentially large vertical position or the grid's thickness is irrelevant. If the block kills paths, the accepted death bound applies instead. I obtain no small-W violation.

**Almost no arrivals.** If |𝒢| < 3L/4, Corollary 4.5 implies its numerical upper bound for deaths exceeds L/4, so Proposition 7.1's hypothesis is unavailable. This is not a counterexample to the proposition. In the theorem's small-W branch the chosen τ forces that same bound below L/4, excluding this configuration. In the other branch the theorem is already true. This is also the resolution for an empty packing or a very narrow region that cannot admit unit squares.

These tests are consistency checks, not constructions claimed to optimize waste. The preceding inequalities, rather than the examples alone, establish the verified rows. No upper bound on w, no small-deficit assumption D ≪ 1, and no stronger density or measure-preservation statement than Sections 1–4 is used in Sections 5–7.

## Section 8: gaps and conditional derivations

The following are the errors/verification limits found in this audit. None supplies a counterexample to Theorem B.

**G1 — Combined slab exponent needs more than [S, Section 2].** Theorem B directly proves the Bui Conjecture 1 exponent: L=x, ζ=x^(−γ), R=x^(1−γ) satisfy the hypotheses for x≥1 and 0<γ<1. But the additional exponent 1−max(β,1−γ)/2 uses [S, Corollary 1], not its fundamental lemma alone. Conditional on that separately stated slab bound, M=x^β+x^(1−γ) ≍ x^max(β,1−γ), and taking the maximum of the two lower bounds gives exactly the printed exponent. I have not re-proved the slab bound from its full flow argument here. For γ>1 and x>1, R<1 really does put the geometry outside both stated sloped-region bounds; this does not assert that every possible lower-bound method fails.

**G2 — Wall lower bounds do not by themselves prove filler optimality.** For a right trapezoid with L ≍ m and R ≍ √m, eventually 1≤R≤L and Theorem B gives W≥c m^(3/4), independently of width. That lower bound is verified. The names, exact shapes, and matching O(m^(3/4)) upper bounds for the cited Bui/Ryu/McClenagan fillers are external inputs, not consequences of Theorem B. They are asserted in the notes, but were not independently established within the permitted proof inputs. Optimality is conditional on those facts.

**G3 — The frame conclusion additionally needs the strip theorem and decomposition.** Given an independently packed x×h strip with the stated fixed fractional part, the cited rectangle corollary yields c x/√h for h≥1. Given an independently packed right end trapezoid with height comparable to h and rise comparable to √h, Theorem B gives c h^(3/4) for sufficiently large h. Their maximum is at least c x^(3/5): split at h=x^(4/5). Bounded h≥1 is covered by the linear strip bound; if 0<h<1 and the fractional part is bounded away from zero, the strip contains no unit square and its area xh is already linear in x. However, the rectangle corollary and the assertion that the actual frames contain these independently packed pieces require additional results. The lower bound is not established for a packing whose squares cross the proposed artificial piece boundaries.

**G4 — Ryu's k exponent is conditional on external frame facts.** Given costs c b/√m and c m^(3/4), splitting at m=b^(4/5) gives a lower bound c b^(3/5). Given also a lower cost comparison c*(k) ≥ c₁k/b+c₂b^(3/5), splitting at b=k^(5/8) gives c*(k)≥c k^(3/8). Both optimizations are correct. The cited end-region geometry, thickness O(m), separately packed walls, slab estimate, and comparison to c*(k) are additional inputs; the note explicitly leaves its source identity unrederived. Therefore closing the stated exponent window is conditional, not proved from Theorem B alone.

**G5 — The Ryu end-region claim needs quantitative angle hypotheses.** Write σ=sin θ, t=tan θ, w=b cos θ+σ, so Reg(y) has ceiling y+(x−σ)t. If y≥σt, its floor length is w and rise wt; Theorem B applies when 0<t≤1 and wt≥1. If 0≤y<σt, the nonempty region starts at x₀=σ−y/t; translation gives a triangle of floor length L′=w−x₀=b cos θ+y/t and rise R′=b sin θ+y. Thus b sin θ≥1 and 0<t≤1 suffice in both cases, and L′R′≥b²sin θ cos θ. For the intended asymptotic regime sin θ≍1/b, cos θ≍1, this gives c√b uniformly in y. This repairs the abbreviated triangle argument. The approximation tan θ≈2/b without a quantified range is not itself a universal hypothesis for arbitrary b and θ, and the cited external open problem was not available for verification. For example, if one omits the needed angle/rise conditions altogether, θ=0, y=0 gives an empty region with zero waste, not c√b. That is a counterexample to an unrestricted extension, not to the stipulated Ryu-angle regime or Theorem B.

FATAL: no
