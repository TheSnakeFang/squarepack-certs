# Adversarial judgment of slab.md

Only `slab.md` was read. Prior-check assertions received no weight. No external sources were consulted. VERIFIED below means independently re-derived; GAP includes missing details that are repaired here, as well as external claims that cannot be checked from this note. I found errors in Section 7, but no unrepairable error in Theorem S or its fundamental lemma.

## Verdict table

| Item | Verdict | Finding |
|---|---|---|
| §1 orientation metric modulo π/2 | VERIFIED | Quotient distance, including the ±π/4 seam, is the appropriate metric. |
| §1 centre separation and neighbourhood counting | VERIFIED | Each square contains its radius-1/2 open disc; each meeting square lies wholly in the radius-√2 neighbourhood. Counting uses whole disjoint square areas. |
| Lemma 2.1, positive φ | VERIFIED | Convex supporting slopes and the constrained reciprocal bound give the stated constant. |
| Lemma 2.1, φ=0 | GAP | The proof divides by φ and assumes strict slopes. The conclusion is simply nonnegativity in this case. |
| Lemma 2.2, R contained in Ω, square and floor cases | VERIFIED | Erosion convexity and downward closure prove both versions. |
| Lemma 2.2, strip confinement and definition of m′ | VERIFIED | Connectedness prevents an intermediate square from crossing either protected centre line. Boundary-only contacts can be counted without weakening the estimate. |
| Lemma 2.2, partition into at most m′+1 intervals | VERIFIED | A unit square has projection length at least 1, so at most one projection endpoint is in the open width-1 strip. |
| Lemma 2.2, convex gaps, side slopes, mod π/2 | VERIFIED | Gap slopes jump upward by at least 2; tangent expansion and quotient distance give the required lower bound. |
| Lemma 2.2, summation, intervening squares and distant endpoints | VERIFIED | The whole intervening chain is required; its metric variation dominates endpoint distance. No distance restriction is needed here. |
| Corollary 2.3, 14-square count | GAP | Its written subtraction of S₁ and S₂ does not apply when S₂ is a wall. A shorter floor rectangle repairs it. |
| Corollary 2.3, θ/50 and radius 1.9 | VERIFIED | With the repaired count, both inequalities hold strictly. |
| §3 flow, termination, touching sides | VERIFIED | Every completed square crossing raises height by at least cos τ; zero gaps do not create a loop. |
| Lemma 3.1(a), null exceptional set and finite partition | GAP | The induction needs a finite branching bound, ceiling-level-set argument and endpoint convention; supplied below. |
| Lemma 3.1(b), height identity and signs | VERIFIED | Vertical increment is cos φ, horizontal increment −sin φ. |
| Lemma 3.1(c), translations | VERIFIED | Every fixed-prefix horizontal map is x↦x−constant. |
| Lemma 3.1(d), exact injectivity | VERIFIED | Reversing from a first intersection gives a common lower point, including zero-gap contacts. |
| §3 measure conservation | GAP | Pointwise disjointness alone is not an area calculation. Piecewise translations and a Jacobian-1 parametrization supply it. |
| Lemma 4.1, W/δ | VERIFIED | Follows from the repaired swept-area calculation. |
| Lemma 4.2, consecutive distances and accumulated tilt | VERIFIED | Endpoint-to-centre distances are at most √2/2; quotient-metric triangle inequality applies through every transition. |
| Lemma 4.2, multiplicity and 1350W/τ | VERIFIED | Square-source contribution ≤21, floor-source contribution ≤4√2; total <27. |
| Lemma 4.3, affine-gap estimate | VERIFIED | For a measurable subset of one half-line, integral of distance from its endpoint is at least half its measure squared. |
| Lemma 4.3, disjointness and ≤10n pairs | VERIFIED | Complete vertical gaps determine their two boundary objects almost everywhere; the stated neighbourhood area is <10.6. |
| Lemma 4.3, Cauchy–Schwarz and constant 21 | VERIFIED | τ(cot τ−tan τ)≥0.991452…>0.99. |
| n≤area(Ω)≤LM | VERIFIED | Disjoint interiors of unit-area squares. |
| §5 Theorem S | VERIFIED | The repaired flow details suffice; (sec τ−1)/τ²≤0.501337…<0.502. |
| Corollary 1, 4e−5 and 1.5e−4 | VERIFIED | Uniform bounds below, including the capped-τ branch. |
| Corollary 2(a), 5e−4 | VERIFIED | Substitution gives RHS/L≤0.853106<1. |
| Corollary 2(b), 5e−5 | VERIFIED | Two analytic branches give RHS/L<0.877; no grid needed. |
| Corollary 2(b), square and near-integer consequences | VERIFIED | For f≤1/2, replace √(1−f) by 1/√2. The floor-grid upper bound is ≤2xf. |
| Corollary 3 and h^(3/4) consequence | VERIFIED | Rotation gives exactly the claimed affine subgraph; w+r≤2C√h. |
| Remark 6.1, floor replaced by a row | GAP | Starting coverage, allocation of waste outside the slab and new constants are not specified. |
| §0/§6 literature attribution and frame-specific hypotheses | GAP | The referenced constructions, parameters and optimality assertions cannot be verified from the permitted source. Conditional exponent calculations are checked below. |
| §7 Conjecture B, literal all-scale formulation | WRONG | Small-area triangles disprove any universal positive constant as stated. An asymptotic formulation could avoid this counterexample. |
| §7 “Deficits” proposed drop argument | WRONG | It omits ΔN. A drop in G need not represent a change in D. |
| §7 lattice example, exact loss “measure ε per level” | GAP | No definition of a level, finite truncation, or derivation of the exact loss is supplied. Hole area alone does not establish that horizontal measure. |
| §7 suggested continuation and sideways proof | GAP | These are proposals, with no injectivity substitute or charging/multiplicity argument. |

## Fundamental lemma: detailed adversarial checks

For Lemma 2.1 with φ>0, an interior minimum must be a breakpoint. Its one-sided slopes are −p,q, with p,q≥φ and p+q≥2. Supporting lines give integral ≥(pa²+qb²)/2. Minimizing over a+b=λ gives λ²/[2(1/p+1/q)]. To maximize the reciprocal sum, either p or q is at least 2−φ and the other is at least φ, or both are between φ and 2−φ and one reduces to p+q=2. On that segment the convex function 1/p+1/(2−p) has its maximum at an endpoint. This proves the constant. Endpoint minima give the stronger φλ²/2. For φ=0, use integral ≥0 directly. This is the only repair needed in Lemma 2.1.

For Lemma 2.2, the erosion Ω₋ is convex because Ω is convex. Radius-1/2 discs at all points of the centre segment are contained in Ω, and their union contains R. In the floor version, the two points (x₁±1/2,y₁) belong to Ω, and downward closure fills the rectangle below their joining segment. The floor is therefore a legitimate terminal boundary in this version. An arbitrary wall in an arbitrary non-downward-closed region is not covered by this proof; a rotated subgraph has the same proof after rotation.

For |t|<1/2, each protected centre-line point is strictly inside its endpoint square: the open disc of radius 1/2 is inside the square. An intermediate square cannot meet that line, even at its boundary, since that would put points of its interior inside the endpoint square. Its intersection with the open strip is connected. If it meets the interior of R, it must consequently stay between the protected lines throughout that strip. In the wall version the other bound is the supporting half-plane of the floor. Squares meeting R only on its boundary need not enter the chain, and counting them in m′ only makes the estimate weaker.

Projection length is |cos α|+|sin α|≥1. Thus at most one endpoint of an intermediate square's projection is strictly inside (−1/2,1/2). Removing these values fixes the list of squares with positive-length chords. The order cannot change without overlapping interiors. An internal chord vertex changes l upward, or r downward, by tan γ+cot γ≥2. Simultaneous changes add; they never cancel in l_next−r_previous. Degenerate axis alignment has no finite-slope internal corner to consider.

For each gap, bounding-side slopes are finite between these vertices. With principal side directions ψ,ψ′ relative to the t-axis,

    |tan ψ′−tan ψ| ≥ |ψ′−ψ| ≥ dist(orientation₁,orientation₂ mod π/2).

Rotating coordinates adds the same angle to both orientation classes, so the last distance is the original θ. A side crossing the ±π/4 convention seam therefore causes no problem. For the floor, the bounding line s=ℓ has slope 0 and its physical orientation is the floor orientation. Treat zero adjacent angle by the φ=0 repair above.

For each fixed partition interval the entire chain, including all squares crossed by the centre segment or other strip chords, is used. If b_i=min(φ_i,θ), then Σb_i≥θ: either one φ_i≥θ, or truncation changes nothing. Since φ_i≤π/4<1,

    Σφ_i(2−φ_i) ≥ Σb_i(2−b_i) ≥ (2−θ)Σb_i ≥ θ(2−θ).

Finally Σλ_r²≥1/q≥1/(m′+1). This proves the exact stated fundamental inequality, including arbitrarily far endpoints. Touching vertices live on finitely many t-levels and do not affect the integral. Zero-width gaps, when present, have zero adjacent angle on their open interval and do not invalidate the estimate.

For Corollary 2.3, the square-square rectangle fits inside a 1×1.82 rectangle. Its radius-√2 neighbourhood has area

    1.82+2√2(2.82)+2π = 16.079350… <16.1.

There are at most 16 meeting squares in total, hence at most 14 others. The written proof fails to justify the same subtraction for a wall. Repair: for a floor pair the centre height is ≤√2/2+0.4, so the neighbourhood area is at most

    (√2/2+0.4)+2√2(1+√2/2+0.4)+2π =13.350091… .

There are at most 13 squares total, hence at most 12 others. Thus the claimed 14 works in both cases. Now (2−π/4)/60>1/50 and √(1.82²+1/4)<1.9.

## Flow: omitted details and verification

There are finitely many possible square prefixes: no square can be visited twice, since its crossing exits its upper side and subsequent motion increases height. At each fixed prefix the horizontal coordinate is x minus a constant, and any fixed vertex can be met for at most one x. This gives finitely many vertex exceptions over all prefixes. Endpoint starting abscissas can be discarded separately without changing any measure assertion. If “open intervals” in Lemma 3.1(a) means open in ℝ, its statement also needs this endpoint qualification.

Before arrival, gap lengths accumulated between straight square sides are affine on a fixed prefix. The final total gap length to the ceiling is a concave function of x, because it is g(x−constant) minus an affine function. For a concave function on an interval, the level δ has at most two separated components, with the only non-singleton possibility a flat interval. Consequently the death/arrival partition has finitely many additional endpoints. Concavity gives continuity in the interior of [0,L]; any allowed discontinuity at a domain endpoint affects only the finitely many paths whose translated abscissa is that endpoint. This supplies the missing finite-partition details without assuming g is piecewise linear.

The signs in (3.1) are correct: each crossing contributes (−sin φ,cos φ), and each gap contributes (0,length). In particular g(x′)=Σcos φ+G=N−D+G.

Injectivity survives both positive and zero gaps. A crossing's interior belongs to exactly one square interior. A positive gap's interior belongs to waste. At a nonvertex boundary point a path arriving vertically from waste cannot coincide with an exit whose immediately lower vertical neighbourhood is inside a flat square. Two exits at such a point must be from the same top side and hence have the same normal predecessor. Shared top/bottom contacts propagate this predecessor argument downward. Vertex contacts are excluded. There is no crossing or merger of distinct nonexceptional paths.

For the area claim, partition by fixed prefix and gap index. Parametrize a vertical gap by (x,v)↦(x−c,v), between its two height graphs (or truncated graph for gap death). Its Jacobian is 1, so its swept area is exactly the integral of its length over starting x. Injectivity makes these swept sets disjoint, apart from boundaries of area zero. Summing gives ∫G dx≤W. Likewise every fixed-prefix arrival map is a translation; disjointness of images permits adding their measures. Entry abscissas on any square's bottom side occupy disjoint subsets of an interval of length cos φ. These are the precise measure statements needed by §4.

## Death bounds

Gap death uses exactly δ of gap length and gives δ|X_gap|≤W.

For tilt death, consecutive centres have separation ≤√2+δ even when the eventual steep square is hit laterally. The first centre has height ≤√2/2+δ. The sum of metric angles from the floor to the terminal square is ≥τ. For a fixed waste point p, each square-source S with p∈R(S,S′) lies wholly in B(p,1.9+√2/2), of area <21.4. Thus at most 21 square sources contribute. For each source, the outgoing path sets are disjoint subsets of its crossing set, of total measure ≤1. A floor-source terminal square lies in a box of width 1+√2 and height √2+δ, area <4.4; at most four such squares contribute, each by at most its horizontal extent √2. The weighted multiplicity is <27, proving 1350W/τ. This argument counts whole squares, not merely separated centres.

For lateral death, a zero final gap would require the relative interiors of two nonparallel boundary sides to meet without interior overlap. That is impossible. A vertex alternative is exceptional. Hence every nonexceptional lateral death has positive final gap and belongs to a stated I(Z,Z′).

The affine function γ on that pair has slope magnitude ≥s=cot τ−tan τ>0. A measurable set of length a on one side of its zero satisfies integral γ≥sa²/2, by placing its mass as close to the zero as possible. The complete vertical gaps for distinct pairs cannot overlap on positive area: almost every vertical waste component has unique bounding objects. Thus Σ|I|²≤2W/s.

The relevant box has width ≤0.08 and height ≤1.4. Its enlarged area is ≤0.112+2√2(1.48)+2π=10.581258…<10.6. It contains points of Z′ and each predecessor square, so there are at most nine square predecessors; adding the floor gives ten pairs per Z′. Cauchy–Schwarz gives (Σ|I|)²≤10nΣ|I|²≤20nW/s. The function τcot τ−τtan τ is decreasing on (0,0.08] (differentiate, or use its convergent sine/cosine expansions), and its endpoint value is 0.9914520675…>0.99. Thus 20/s<21τ. Also n≤area Ω≤LM.

At arrival Σcos φ≤g≤M and cos φ≥cos τ, so N≤M/cos τ. The function (sec τ−1)/τ² is increasing here, for example from the positive even-power series for sec τ; at 0.08 it is 0.501336813… . This verifies the 0.502 deficit coefficient and completes Theorem S using the repaired details above.

## Uniform arithmetic for the corollaries

Put w₀=W/L. Dividing the theorem by L gives

    1−|A|/L ≤ w₀/δ+1350w₀/τ+√(21τMw₀).

The right side increases with w₀. All strict numerical margins below exclude the proposed threshold and every smaller value.

For Corollary 1, write R=ζL≥1 and s=δ+δ′. The number of integer windows meeting the height range is at most R+s+1. Thus |A|/L≤s(1+(1+s)/R)≤s(2+s). With δ=δ′=1/24 this is 25/144, leaving 119/144=0.826388889… . Also M≥1. Set b=√((1/24)/0.502) and M₀=(1/24)/(0.502·0.08²)=12.968957… .

For W=κL/√M and M≥M₀, τ=b/√M, and the right side is at most

    24κ/√M₀+1350κ/b+√(21κb).

For κ=4e−5 this is <0.203259. For κ=1.5e−4 it is <0.734007. The latter applies to every M≥13. For 1≤M≤M₀, τ=0.08 and the first two terms are at most 24κ+1350κ/0.08; the last is at most √(21κb). For κ=4e−5 their sum is <0.691517. Both constants are therefore proved uniformly.

For Corollary 2(a), M=m+1/2≥125.5, δ=δ′=0.4 and τ=√(0.4/(0.502M))<0.08. A is empty. Writing b=√(0.4/0.502), the RHS at κ=0.0005 is at most

    2.5κ/√125.5+1350κ/b+√(21κb)=0.853105372…<1.

For Corollary 2(b), set q=min(f,√((1−f)/M)), κ=5e−5 and w₀=κq. The proposed δ and δ′ leave A empty. Since q≤f≤1, q/δ≤2.5. Write a=√((1−f)/(1.004M)), τ=min(0.08,a). If τ=a, then q/τ≤√1.004 and τMq≤(1−f)/√1.004≤1/√1.004. Thus the RHS is at most

    2.5κ+1350κ√1.004+√(21κ/√1.004)<0.100132.

If τ=0.08, then M≤(1−f)/(1.004·0.08²). Hence again τMq≤1/√1.004, while q/τ≤1/0.08. The RHS is at most

    2.5κ+1350κ/0.08+√(21κ/√1.004)<0.876247.

These bounds prove the stated 5e−5 without the grid's unproved 9e−5 assertion. For square side x≥1 and f≤1/2, q≥(1/√2)min(f,1/√x), giving c=5e−5/√2 in the square formulation. If f≤x^(−1/2), the axis grid leaves x²−⌊x⌋²=2xf−f²≤2xf, proving the stated constant-factor optimality.

For Corollary 3, rotating puts L=h, g(0)=w and g(h)=w+r, so Corollary 1 applies since r≥1. If w,r≤C√h, then M≤2C√h, and the explicit consequence is W≥(4e−5/√(2C))h^(3/4).

## Concrete packing attacks

Coordinates below specify centres unless square intervals are given. They are local configurations embeddable in a sufficiently large rectangle; contact is allowed.

* **Nearly touching, different tilts.** Let 0<a≤0.08, c=cos a, s=sin a. Take an axis square at (2,2) and a square of tilt a at (2+(1+c+s)/2,2). Their horizontal supporting lines separate their interiors; the second square touches the first at its leftmost vertex. There are no other squares. In the centre rectangle the uncovered area is exactly (c+s−1)/2+(c+s−1)²/(8sc): the second term is the triangular tip cut off by |t|≤1/2. This exceeds a(2−a)/4 in the small-angle regime and agrees with the gap proof. It does not supply a zero-waste transition between different tilts.
* **Intervening squares and vertices.** Axis squares at (1,1),(2,1),(3,1) give a centre segment through the middle square, touching along full sides. The endpoint rectangle has zero waste and θ=0, consistent with the lemma. Adding any number of intervening axis squares only enlarges m′. Vertical grid lines meet vertices, but correspond to finitely many starting x in a finite packing. Ignoring the middle square in the chain would be unjustified; the written lemma does not ignore it.
* **Tilted columns on axis layers.** Above axis squares with top height H, take the tilted block P+[0,K]u+[0,J]n, tiled by its unit parameter cells, with P=(X,H). Since sin a,cos a>0, every block point has y≥H. Its bottom touches the layer at a vertex and rises along the layer, creating real triangular waste. A vertical flow changes orientation only at entry to the block, then has deficit J(1−cos a). This checks the sign and accumulation of D; it does not evade the first-transition charge. For a single square resting on the floor, centre (2,(c+s)/2) and tilt a gives the corresponding wall test.
* **Brick offsets.** Axis rows [i+o_j,i+o_j+1]×[j,j+1], with o_j alternating 0 and 1/2, restricted to a containing rectangle, tile across every internal horizontal seam away from vertices. They produce zero-gap bottom-to-top transitions despite shifted row boundaries. All tilts are zero; no lateral charge is warranted or produced. The vertex starting values are finite.
* **Far endpoints.** Two differently tilted squares at (2,2) and (K,2), K≥4, with or without intermediate axis squares, leave the whole ordered chain in the strip. The partition bound depends on the number of intermediate squares, not K. Neither strip confinement nor the telescoping metric estimate assumes that the endpoint squares are consecutive.

These attacks test the specified degeneracies; they are not a claim to have exhaustively optimized packings.

## Errors and unproved claims outside the theorem

**WRONG: Section 7 deficit-drop identification.** The height identity on two paths gives exactly

    ΔG = Δg − ΔN + ΔD.

The proposed argument omits −ΔN. For a concrete example take L=4 and g(x)=1+x/2. Pack [k,k+1]×[0,1] for k=0,1,2,3 and also [k,k+1]×[1,2] for k=2,3. All squares are axis aligned. For the untruncated vertical paths, N=1 on (0,2), N=2 on (2,4), D=0 throughout, and G=x/2 on the first interval, G=x/2−1 on the second. G drops by 1 at x=2 with no change in D or adjacent tilts whatsoever. With the note's δ≤0.4, paths near the left side of this jump die in gaps; they do not provide the missing sideways tilt charge. Handling such dead bands is additional work, not the stated identification of a gap drop with ΔD. This defeats the outline's inference, not Theorem S.

**WRONG: literal universal Conjecture B.** Set L=ε, R=1, w=0 and g(x)=x/ε on [0,ε]. This is the right triangle allowed by the stated zero-width convention, of area ε/2. The empty packing has W=ε/2, so W/√(LR)=√ε/2→0. No uniform positive c exists with only R≥1 imposed. If positive bases are desired, set w=ε instead; the ratio still tends to zero. Restricting to a specified large-scale regime could repair the formulation, but would be a different quantified statement. No purported disproof of an asymptotic literature conjecture is intended.

**GAP: Remark 6.1.** A row must cover the starting set up to null sets, and the replacement centre rectangles may extend below y=0. The waste charged there must be included in the budget. Neither a precise region/waste definition nor replacement multiplicity constants are given, so this is not a proved extension.

**GAP: external constructions and numerical/grid assertion.** From this source alone I cannot certify the cited McClenagan, Bui or Ryu constructions, their allowed lifts, exact wall widths, or the descriptions of their open problems. The note's claimed 9e−5 grid minimum is also not established by reading its assertion. The smaller 5e−5 actually stated in the corollary is proved above. Attribution and comparative novelty remain unverified.

Conditional on the supplied construction hypotheses, the exponent algebra is sound: minimizing max(xh^(−1/2),h^(3/4)) gives h=x^(4/5) and x^(3/5); width m^(3/4) gives m^(5/8); a cost b/√y bounded above by a constant times b^(3/5−ε) forces y+O(1)≳b^(4/5+2ε). These calculations do not establish those construction hypotheses, independent-region restrictions, or the asserted improvements to complete frames. The literal phrase “for every h” in the strip discussion also needs its hypothesis h≥1, since Corollary 2(b) assumes that.

The Section 7 lattice and continuation suggestions have not been promoted to lemmas: the exact lateral-loss claim and an injectivity/multiplicity replacement require additional derivations. They are GAP, not VERIFIED.

FATAL: no
