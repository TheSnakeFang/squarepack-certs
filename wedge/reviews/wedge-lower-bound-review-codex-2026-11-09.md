Verdict: sound with fixes.

Independent adversarial report on `wedge-lower-bound.md`, draft v0.2, 2026-11-09. This verdict concerns Theorem B and its stated constant, using only [S, Lemma 2.2 and Corollary 2.3] as granted results. I found no fatal geometric error. Two local repairs complete the main proof. The frame consequences need an additional qualification. This is a mathematical referee assessment, not a formal verification.

## Numbered findings, most severe first

1. **GAP — Section 8, lines 311–314: the rectangle-strip lower bound needs a fractional-part hypothesis.** The cited [S, Corollary 2(b)] gives
   `c L min(f, sqrt((1-f)/M))`, not uniformly `c L/sqrt(M)`. A rectangle of integer dimensions has zero waste, so the asserted strip bound cannot hold uniformly in its dimensions. More generally, an integer-length rectangle of height `m+f` has an axis-aligned packing wasting `Lf`; this is smaller than `L/sqrt(m+f)` when `f sqrt(m+f)` tends to zero. If these are strips obtained by subtracting an integer core from an outer square, an integer or nearly integer outer side creates precisely this issue. **Fix:** state the frame conclusion for outer sides with fractional part bounded away from both 0 and 1, for example half-integer sides, and spell out the resulting strip dimensions. Otherwise retain the fractional-part factor and reoptimize. This affects the unqualified frame discussion, not Theorem B or the width-independent wall bound. The claimed conversion from `b^{3/5}` to `k^{3/8}` also needs the external construction's parameter relation; that relation is not supplied in this note and was not independently verified here.

2. **MINOR — Lemma 3.1(a), lines 86–89: a finite E cannot contain every point where `G+r*=delta`.** This equality can hold on a whole interval. Concrete example: take `L=4`, `zeta=1/4`, `w=3`, and the single square `[1,2] x [delta,1+delta]`, with `delta=1/32`. For every starting `x` in `(1,2)`, the first probe has `G+r*=delta`; the floor is unconflicted. Thus the literal description of E makes E infinite. **Fix:** put in E the boundaries of the equality sets on each affine itinerary cell, rather than all equality points. A cell on which equality holds identically has a fixed decision under the stated strict `>` rule and needs no further subdivision. The finite-partition conclusion and every later use survive.

3. **MINOR — Proposition 7.1, lines 295–296: the last numerical implication needs an explicit rescaling.** The displayed estimates give `0.4696 R <= 21216 tau W`; rounding `0.4696` up to `0.47` alone would be invalid. **Fix:** add
   `0.4696*21300 = 10002.48 > 9971.52 = 0.47*21216`.
   This proves exactly `0.47 R <= 21300 tau W`. The stated proposition and theorem constants are valid; neither needs weakening.

There is no FATAL finding. Nothing found kills the flow/sideways approach. Findings 2–3 repair the write-up; finding 1 restricts a downstream claim.

## Per-lemma verdicts

| Item | Verdict | Reason / required fix |
|---|---|---|
| Section 0, Theorem B and quantitative formulation | correct | Follows after the local repairs below. The scale comparison with [S] is algebraically right. |
| Section 1, orientations and wall cases | correct | Wall rectangles and the exceptional-left-wall count checked below. |
| Section 2, flow definition and termination | correct | Including zero-length contacts and boundary precedence; details below. |
| Lemma 3.1(a) | correct with fixable gap | Replace equality points by boundaries of equality cells, finding 2. |
| Lemma 3.1(b) | correct | Transverse coordinate derivative is the product of secants. |
| Lemma 3.1(c) | correct | Direct vector summation, including the incoming gap in each entry height. |
| Lemma 3.1(d) | correct | The ceiling projection formula and lower bounds have the stated signs. |
| Lemma 3.2 | correct | Degenerate cases admit the predecessor argument detailed below. |
| Lemma 3.3 | correct | Expansion on cells plus globally disjoint crossing coordinates. |
| Lemma 4.1 | correct | Gap-sweep Jacobian is kappa, not merely its horizontal projection. |
| Lemma 4.2 | correct | Hypotheses, chain weights, and 1350 independently reconstructed. |
| Lemma 4.3 | correct | One-sided strips of width `delta sin(theta)` give the claimed bounds. |
| Lemma 4.4 | correct | Three cases are exhaustive; disjoint square interiors give the decisive restriction. |
| Corollary 4.5 | correct | Ordered-pair, floor, wall, and exceptional-wall counts are sufficient. |
| Lemma 5.1 | correct | Tubes do not overlap, and a gap between successive chords cannot be charged twice at one height. |
| Equation (6.1) | correct | Follows from `zeta Delta = P_left-P_right-drop`. |
| Lemma 6.1 | correct | Telescoping has the stated endpoint signs. |
| Lemma 6.2 | correct | Prefix comparison gives overlap greater than 0.7155. |
| Lemma 6.3 | correct | Index pairing is legitimate; all three count comparisons work, including zero counts. |
| Proposition 7.1 | correct with fixable gap | Supply finding 3's numerical rescaling. |
| Proof of Theorem B | correct | All parameter restrictions and final constants checked. |
| Section 8 | correct with fixable gap | Basic trapezoid substitutions work; qualify the frame strip bound as in finding 1. External construction identifications remain conditional on their source hypotheses. |

## Independent geometric and measure derivations

### Flow, finite partition, and density

A nonzero probe before its first hit is in the waste, and its direction has positive vertical component. A flat-to-flat incoming direction has positive scalar product with the target's upward normal, since the orientation difference is less than 0.16. It cannot first enter through the target's top side. A first contact can instead be a vertex, a lateral side, or the bottom side, exactly as the rules specify.

For a zero-length contact at an interior point of an emitter's top edge, a second square touching there along a side must have the same supporting line and occupy the opposite half-plane. Its side is its bottom side and its orientation equals the emitter's. A contact with a second square's vertex is covered by step 3 unless conflict death already stops the path. For the floor emitter, an interior-side zero contact similarly forces a horizontal bottom edge. Thus zero gaps introduce no missing transition. Top edges cannot have an interior point on a vertical wall, since such a nonparallel supporting contact would put some of the square beyond the wall. Contacts with the ceiling that belong to another square are processed as square contacts, as specified.

Each positive-length piece increases height. A square crossing increases height by at least `cos(tau)`, so the finite packing allows only finitely many crossings. Zero-length terminal events do not create a loop. Coincident boundary events are settled by the stated priority rules.

For a fixed itinerary, let the emitter displacement be `ds u_old`. The next bottom-hit displacement satisfies

`ds_new u_new = ds u_old + dr n_old`.

Taking the dot product with `u_old` gives `ds_new cos(phi_new-phi_old)=ds`. The first transition from the floor gives `ds_1 cos(phi_1)=dx`. Consequently

`ds_j/dx = product sec(theta_{i-1,i}) >= 1`.

This calculation applies to completed crossings. It does not claim that a terminal lateral hit has the same coordinate map. All gap lengths, including a final gap truncated at the remaining budget, are affine on a fixed event cell.

The first-hit functions on each emitter are piecewise affine: there are finitely many target edges, vertices, and walls. After subdivision, its capped probe region is a finite union of polygons or lower-dimensional pieces. Whether another emitter's capped probe region meets a given probe is therefore a finite union of parameter intervals and points. Pulling their boundaries back through the nonconstant affine emitter coordinate preserves finiteness. The finite number of possible square sequences completes the finite-partition argument after finding 2's repair. Identically zero gaps and identically saturated gap budgets are retained as cells.

The height after crossing `Z_j` and its following gap is

`gamma_0 + sum_{i<=j}(1+gamma_i) cos(phi_i)`.

In particular, the formula for `h_i` includes `gamma_{i-1}`; no incoming gap is lost. At arrival this gives (3.1), with `0<=Gtilde<=G<=delta`.

For the ceiling, dotting `(dx', zeta dx')=ds u_N+dr n_N` with `u_N` gives

`dx'/dx = kappa_N/(cos(phi_N)+zeta sin(phi_N))`

`= kappa_N cos(zeta')/cos(phi_N-zeta') >= cos(zeta')`.

The denominator is positive in the stated angle ranges. Since the itinerary fixes N and D, differentiating (3.1) gives `Gtilde'=zeta kappa' >= sin(zeta') >= zeta/sqrt(2)`. For N=0, `x'=x` and `Gtilde'=zeta`, which also satisfies the inequality.

### Disjointness, including the endpoint cases

Different probes from one emitter cannot intersect: their initial displacement is a nonzero vector along `u`, perpendicular to their common direction `n`. If two probes from different emitters meet anywhere, including their endpoints, both are conflicted. Neither can then contribute a positive-length travelled probe piece: step 1 stops the corresponding path first. A path that would die midway along a probe is subject to the same test on the entire capped probe, so truncation cannot evade it.

A conflict-death point itself is still part of its path. For a square emitter it is the endpoint of the preceding square crossing; for the floor it is a starting point. Thus it is covered by the predecessor argument, rather than by an assertion that the conflicted probe was travelled.

At a common point of least height:

- Inside a square, both paths are its normal crossing and have a lower common point.
- Outside all squares and above the floor, both paths arrived along positive-length non-conflicted probes. They must have the same emitter and the same probe, and hence a lower common point. This includes ceiling and wall endpoints in no square.
- On a square boundary, an incoming path either has a positive-length waste probe or ends a crossing of a flat square at an interior point of its top side. Zero-length transitions preserve this preceding crossing and create no extra kind of incoming piece. Two top-side crossings through the same point would have overlapping square interiors unless they cross the same square. A probe approaching such a top-side interior point would enter that square immediately before contact, since its direction has positive dot product with the square's upward normal. That is impossible for a waste probe. Two incoming probes reduce to the preceding case.
- On the floor, both paths must have started there.

Vertex hits do not appear on non-exceptional paths as visited probe endpoints. A crossing through an interior top-side point that happens also to be another square's vertex still has the same predecessor analysis; it does not open a coalescence case.

Thus distinct non-exceptional paths, including their terminal points, are disjoint. Their graphs over height preserve their initial left-to-right order. If the left starting path had arrival abscissa at least that of the right starting path, then at the right path's arrival height it would lie strictly to the left of that ceiling point. The increasing ceiling there is lower than that height, a contradiction. This proves the stated order on arrivals, not its reverse.

For each crossed flat square, the affine maps into its bottom coordinate have slopes at least one. Their images from different itinerary cells are disjoint by path disjointness. Summing image lengths inside `(0,1)` proves total starting measure at most one. Direct floor hits on any square occupy a subset of its horizontal projection, of length at most `sqrt(2)`. This establishes both density assertions.

### Wall extension and local counting

For the right wall, `[x_c,L] x [y_c-1/2,y_c+1/2]` is inside the trapezoid: the square's inscribed half-unit disc places its left vertical edge inside, and the ceiling only increases to the right. All packing squares lie to the left of the wall, so the floor proof of [S, Lemma 2.2] applies after rotation. The same strip proof works at the left wall whenever `y_c+1/2<=w`. The rectangle width is the perpendicular centre-to-wall distance; for wall-death squares this is at most `sqrt(2)/2+delta`, so the short-distance hypothesis is more than satisfied.

For an excluded left-wall square, a probe can move left only if `phi>0`. Its top-left vertex has abscissa `a` with `0<=a<=delta sin(tau)`. Therefore

`x_c=a+(cos(phi)+sin(phi))/2 in [0.5,0.55]`.

Using the top-right vertex below the ceiling gives

`w-1/2 < y_c <= w-1/2+1.1 zeta`.

The occupied centre rectangle has width at most 0.05 and height at most 1.1. Since square centres have distance at least one, any two centres in it differ vertically by at least `sqrt(1-0.05^2)`. Three would require vertical span exceeding 1.99. Hence there are at most two. Their total possible starting measure for wall death is bounded by `2 delta tan(tau)`, even slightly smaller than the allowance in the note.

For any short square pair, each point of its fundamental rectangle is within 1.9 of either centre, since that rectangle is symmetric in its two endpoints. Each whole square is then inside `B(p,1.9+sqrt(2)/2)`, hence inside `B(p,2.61)`. The latter disc has area 21.40085, so at most 21 disjoint unit-square interiors can lie inside it. This justifies 21, 420 ordered distinct pairs, and 210 unordered pairs.

For a floor pair occurring in the flow, its centre height is at most `sqrt(2)/2+delta`. If p belongs to its rectangle, the entire square lies in a box of width `1+sqrt(2)` and height `sqrt(2)+delta`. At the chosen delta its area is 3.48966, so the bound four is safe. Rotating gives the same box bound for each wall. Only charged pairs are counted; there is no claim of a uniform count for arbitrary distant floor/wall pairs.

### Death bounds and the conflict geometry

In a gap after `Z_j`, use coordinates `(x,r)` with point `e_j(x)+r n_j`. Its area Jacobian is `kappa_j>=1`. The different travelled pieces are disjoint, apart from area-zero endpoints. Integrating the total gap length delta over gap-death starting points gives `delta |B_gap|<=W`. This also covers a final zero-length piece when the budget was previously exhausted.

For tilt deaths, consecutive square centres have distance at most `sqrt(2)+delta`; the first centre lies within `sqrt(2)/2+delta` of the floor. Thus every use of [S, Corollary 2.3] meets its distance hypothesis. The orientation metric gives a chain sum at least tau. Let mu be the starting measure assigned to a directed consecutive pair. For each crossed square S, the outgoing mu weights sum to at most one, by the density lemma. Floor-pair weights are at most `sqrt(2)`. At a waste point the weighted rectangle multiplicity is at most `21+4 sqrt(2)<27`. Hence `tau |B_tilt|<=50*27 W=1350 W`.

For a lateral death, in the target frame the probe changes the target's lateral coordinate by at most `delta sin(theta)`. Only the one-sided strip leading into that side can contribute. The emitter top line has lateral-coordinate derivative `cos(theta)` with respect to its own arclength. Each lateral side therefore takes at most `delta tan(theta)` emitter length. The wall calculation is the same with theta equal to the emitter inclination. When theta=0, a ray parallel to a lateral side could only first reach its vertex from below; a positive-measure lateral-interior death is impossible. The zero-length relative-side case was already excluded by the supporting-line argument.

For conflicts, work in `Z_2=[0,1]^2`. A meeting point is in its full cap `[0,1] x [1,1+delta]`, even if its actual probe is shortened by another obstacle. If `e=(s0,t0)` emits from `Z_1`, then `1-delta<=t0<=1+delta`. Its backward unit normal segment is inside `Z_1`, apart from its endpoints. Since square interiors are disjoint:

- If `t0<1`, its lateral coordinate is outside `(0,1)` and within `delta sin(theta)` of an endpoint to reach the cap.
- If `t0>=1` and `s0` is outside `(0,1)`, the same bound holds.
- If `t0>=1` and `s0` is inside `(0,1)`, follow the backward normal just below height one. The required normal length is `(t0-1)/cos(theta)+eta<1`. That point cannot be inside `Z_2`, so `s0` must be within `delta tan(theta)` of a lateral edge.

These cases include equality at height one and all endpoint meetings. If theta=0, the third case is impossible and the others have zero emitter length. In fact open top-side parameters exclude the remaining parallel-side endpoint possibility. The emitter-coordinate measure is bounded by

`4 delta tan(theta)/cos(theta) <= 4.086685 delta theta < 4.3 delta theta`.

Thus two nonoverlapping flat squares cannot have a much larger positive-measure conflict set. The restriction comes from the backward segment inside the emitting square, not just the intersection of two infinite ray families. Floor probes lie below delta while square top emitters are above 0.9, so floor–square conflict is impossible.

For Corollary 4.5 the conversion from emitter arclength to starting measure uses the same injective maps with derivative at least one, including when the terminal event is a conflict death before travel. The short-pair distance is at most `sqrt(2)+2 delta`, and the coefficients are valid because

`2 tan(0.16)/0.16 = 2.017244 < 2.02`,

`tan(0.08)/0.08 = 1.002139 < 1.01`.

The full charged coefficient before delta is

`50*(6.32*420+2.02*4+1.01*8)=133528 < 134000`.

The two excluded left-wall squares cost less than 0.0051, hence less than 0.01. Finally `1/delta+134000 delta=4219.5<4250`. All death categories are included.

### The sideways lemma

The chosen starting points satisfy `x_k^+<x_{k+1}^-`. Path order therefore places a strictly positive separation between the right boundary of one tube and the left boundary of the next at every common height. The tubes have disjoint interiors even when their ceiling endpoints have different heights: each tube is defined only over heights reached by both boundary paths.

If `y in Y_i`, the segment between the paths starts in the i-th square of the left path and ends in the i-th square of the right path. Convexity of the trapezoid puts the whole horizontal segment in the region. For almost every height, square chords are interior, nonoverlapping intervals in a fixed left-to-right order. Discard the finitely many vertex and horizontal-edge heights; they do not affect the integral. A square cannot appear twice along such a segment. If both endpoints are in the same square, the angle to charge is zero.

On a bad segment, the uncovered length is at least 2/5. Disjoint segments give at most `(5/2)*line_waste(y)` bad segments, and their endpoint tilt distance is less than `2 tau`. Integrated contribution is at most `5 tau W<=0.4 W`.

On a good segment, every gap between consecutive square chords is less than 2/5. Choosing the two facing chord endpoints gives centre distance at most `sqrt(2)+2/5`. Thus [S, Corollary 2.3] applies even when intermediate squares are steep. The triangle inequality is in the orientation metric and does not require intermediate flatness.

A specific consecutive square pair has a single intervening chord gap at that height. Any segment that charges that pair must contain the entire gap and reach both squares. Two ordered, disjoint tube segments cannot both do this. For a zero gap, their positive separation still prevents double charging. This proves the required one-charge-per-pair-per-height assertion.

A fixed pair can share heights over length at most sqrt(2). The 210-pair rectangle multiplicity proved above gives a good contribution at most `sqrt(2)*50*210 W=14849.242405 W`. Together with the bad contribution this is `14849.642405 W<14851 W`. The tubes may contain other paths or squares; neither fact spoils the argument.

## Boundary algebra, skips, and theorem arithmetic

Since `Phi=-P+Gtilde`, subtracting the left arrival limit from the right one gives

`zeta Delta=P_left-P_right-drop`.

Order makes Delta nonnegative, so (6.1) has the correct sign. The Gtilde increase across each arriving interval is at least `sin(zeta')` times that interval's starting length. The exact telescoping identity is

`sum_k [Gtilde(b_k^-)-Gtilde(a_k^+)]`

`=sum_{k<K} drop_k+Gtilde(b_K^-)-Gtilde(a_1^+)`.

The last difference is at most delta. Discarding negative drops gives Lemma 6.1. If there are no arrivals, its inequality is trivial; the proposition's positive-measure hypothesis ensures there are arrivals when this indexing is needed.

Index pairing of two square lists is legitimate. It does not assert that paired squares are adjacent or at equal heights. It pairs their cosine sums and entry-height prefixes; the horizontal chain in Lemma 5.1 handles intervening squares. On `[-tau,tau]`,

`|cos(phi)-cos(psi)|<=sin(tau)|phi-psi|<=tau theta`.

The partial gap sums of either path are in `[0,delta]`, so an aligned level has entry-height offset less than `1/4+delta`. Both crossings have vertical length at least `cos(tau)`. Therefore their common height interval has length at least

`cos(0.08)-1/4-1/32=0.715551706>0.7`.

This also holds for paths chosen arbitrarily close to their interval endpoints.

At the first non-aligned level, all preceding levels are aligned and their angles sum to at least `1/(4 tau)`. Consequently `tau Theta>=1/4`, which pays any drop, since a drop is at most delta. If every common level is aligned, the three integer-count possibilities are exhaustive:

- `N'=N`: `P_left-P_right=sum(cos(phi_i')-cos(phi_i))<=tau Theta`.
- `N'=N-j`: `P_left-P_right<=tau Theta-j(1-0.51 tau^2)`. A positive drop implies this is positive, so `tau Theta>j(1-0.51 tau^2)>1/2`. This pays the drop.
- `N'=N+j`: `zeta Delta>=j(1-0.51 tau^2)-tau Theta-drop`. If `tau Theta>=1/4`, it pays the drop directly. Otherwise the right side is at least `1-0.51*(0.08)^2-1/4-1/32=0.715486>1/2`, proving the skip alternative.

The estimate `1-cos(phi)<=0.51 tau^2` is safe (even 0.5 suffices). Empty common lists are covered by the same formulas. No assumption of small total deficit or bounded width is hidden here.

Under Proposition 7.1's hypothesis, the death estimate leaves at least `3L/4` arriving starting measure. Their ordered affine images have total measure at least

`(3/(4 sqrt(2))) L=0.530330085 L>=0.53 L`.

The boundary gaps are disjoint and miss that image, so their total length is at most `0.47 L`. Each skip consumes at least `1/(2 zeta)` of that length: at most `0.94 R` skips. Each skip's positive drop is at most delta, regardless of whether its paired angles also pay it. Non-skips' positive drops are paid by Lemma 6.3. Negative drops cause no problem. Thus

`sin(zeta')*(3L/4)-delta <= tau sum Theta+0.94 R delta`.

For `R>=1`, the left side is at least `(3/(4 sqrt(2))-1/32)R=0.499080085 R`, hence at least `0.499 R`. The skip term is `0.029375 R<=0.0294 R`. Lemmas 5.1–6.2 give `sum Theta<=14851 W/0.7<=21216 W`. Finding 3's rescaling now gives the stated proposition.

For Theorem B, `R<=L` implies `sqrt(LR)<=L`. If `0<W<=7e-6 L`, choose `tau=10800 W/L<=0.0756`. Then the left side of the proposition's hypothesis is at most

`(4250*7e-6+1/8+0.01)L=0.16475 L<L/4`,

using `L>=R>=1`. The proposition yields

`W>=sqrt(0.47/(21300*10800))*sqrt(LR)`

`=4.520091741e-5 sqrt(LR)>4.5e-5 sqrt(LR)`.

This proves the weaker advertised `7e-6` bound as well. If W=0, tau=0.08 meets the hypothesis because `0.01<=L/4`, and gives a contradiction. The branch with `W>7e-6 L` was already sufficient. No restriction on w occurs in this argument.

## Consequences and attempts to falsify the theorem

The Bui substitution is right: `L=x`, `R=Theta(x^{1-gamma})` gives `sqrt(LR)=Theta(x^{1-gamma/2})`. His published conjectural statement is in [arXiv:2508.04603, Section 6.3](https://arxiv.org/html/2508.04603v1#S6.SS3). The theorem proves a uniform quantitative version in its stated slope range. Combining with a slab bound `L/sqrt(M)` and `M=Theta(x^{max(beta,1-gamma)})` gives the displayed first two exponents, conditionally on that slab bound. Rise below one is outside the stated theorem.

For a wall of length comparable to m and rise comparable to sqrt(m), direct substitution gives `m^{3/4}` at every width. Balancing valid strip cost `x/sqrt(h)` against valid wall cost `h^{3/4}` gives `h~x^{4/5}` and cost `x^{3/5}`. The algebra is correct once finding 1's strip hypothesis and the separate-region packing premise are imposed. The same balance with b and m gives `b^{3/5}`.

For the Reg(y) formula read in [S], namely `0<=t<=y+(x-sigma)tan(theta)` on `0<=x<=b cos(theta)+sigma`, with `sigma=sin(theta)` and `tan(theta)~2/b`: if `y>=sigma tan(theta)`, it is directly a trapezoid of length comparable to b and rise comparable to two. If `0<=y<sigma tan(theta)`, translate its nonempty part from `x=sigma-y/tan(theta)`; its length is `b cos(theta)+y/tan(theta)` and its rise is `b sin(theta)+y`. These are still comparable to b and two. Thus Theorem B does imply `c sqrt(b)` uniformly in the lift for this supplied formula, provided the source tilt guarantees rise at least one. The identification with Ryu's source and the numerical parameter relations were not checked against his original paper.

I tried the following counterexample mechanisms: very thin triangles, integer and noninteger lengths, arbitrarily thick integer-height grid backgrounds, parallel touching squares, almost-parallel competing emitters, zero budget after an earlier gap, and different path lengths N. None defeats the derived estimates. For integer L,R with `1<=R<=L` and integer baseline w, the elementary axis-aligned column packing has

`n=Lw+((R-1)(L-1)+gcd(L,R)-1)/2`,

so `W=(L+R-gcd(L,R))/2>=L/2>=sqrt(LR)/2`. This family is far above the proposed constant even at unbounded width. It is not an optimality proof for arbitrary packings.

A standard-library Python check tested 150,000 nonoverlapping flat-square pairs. Separation was certified by a separating axis; their entire untruncated normal caps were intersected by polygon clipping. The cap-intersection projection bounds the actual conflicted emitter set from above. The largest observed ratio to `delta*theta` was 0.94510, below 4.3. Only 19 sampled pairs had positive cap-overlap measure, so this is limited corroboration, not evidence replacing the analytic proof. A separate axis-grid sweep over lengths from 1 to 100, rises from 1 to L, and widths up to 10000.5 had minimum `W/sqrt(LR)=0.5`.

The scratch script is `(local scratch path removed)`. It was executed with `python3 -I`. Numerical values above are corroborative floating-point evaluations; the proof uses the explicit inequalities and comfortable margins shown above.

## What was derived, assumed, and only read

**Derived independently:** the flow transition factors, height and ceiling identities, disjointness including endpoint and zero-gap cases, global density, gap Jacobian, all charging weights and local multiplicity bounds, both wall extensions and the two-square exception, the three-case conflict estimate, the sideways chain integral, all Section 6 identities and alternatives, the skip accounting, and the theorem's numerical implications. The equality-plateau configuration is explicit. The strip counterexamples are explicit rectangle packings. The main lower bound follows from these derivations and the granted fundamental lemma/corollary.

**Assumed as authorized:** [S, Lemma 2.2 and Corollary 2.3], including their constants. Their conclusions were not independently reproved; each use's geometry, containment where a wall extension was needed, and short-distance hypotheses were checked. No other result of [S] is needed for Theorem B.

**Only read / conditional:** other [S] results and descriptions of external frame constructions. Their appearances in Section 8 were checked by substitution and algebra, with the limitations stated above. Original Ryu/McClenagan constructions and the b-to-k conversion were not independently audited. Bui's original conjectural scale was checked in the linked primary source; this does not supply any step of the proof.

**Independence and actions:** no file whose name contains `review` in `docs/` was read; no content under `runs/` was read; Section 9 of the wedge note was not read. No earlier referee conclusions were used. No existing file was edited and no git action was taken. The only new repository file is this report; the numerical script was created in the authorized scratch directory.
