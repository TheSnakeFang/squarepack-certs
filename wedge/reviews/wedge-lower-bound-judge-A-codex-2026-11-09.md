# Adversarial audit of wedge.md, Sections 1–4

I read only wedge.md and slab.md. I gave no evidential weight to claims of previous checking. No web search, other source, or pre-existing review was used. Computations below were independently evaluated with Python. VERIFIED means the claim was re-derived, including the degeneracies discussed below; it does not mean a computer search proved it. GAP means the written argument omits a necessary justification, even when I supply a repair here.

I found an invalid inference in the cited proof of [S, Corollary 2.3], and several omissions that can be repaired. I did not find a counterexample to a scoped lemma or an unrepairable obstruction to Theorem B. The instruction to assume there is an error is not evidence of an additional error.

## Verdict table

| Item | Verdict |
|---|---|
| [S] Lemma 2.1, auxiliary inequality | VERIFIED |
| [S] Lemma 2.2, square/floor fundamental lemma | VERIFIED |
| [S] Corollary 2.3 | GAP |
| Section 1, orientation and flat-angle conventions | VERIFIED |
| Section 1, right-wall fundamental lemma | VERIFIED |
| Section 1, left-wall criterion and two-square exception | VERIFIED |
| Section 2, emitters and probes | VERIFIED |
| Flow step 1, conflict death | VERIFIED |
| Flow step 2, gap budget and gap death | VERIFIED |
| Flow step 3, vertex exception | VERIFIED |
| Flow step 4, arrival and wall death | VERIFIED |
| Flow step 5, tilt death | VERIFIED |
| Flow step 6, lateral death | VERIFIED |
| Flow step 7, bottom entry and crossing | VERIFIED |
| Section 2, termination justification after step 7 | GAP |
| Lemma 3.1(a), finite itinerary partition | GAP |
| Lemma 3.1(b), affine coordinates and expansion | VERIFIED |
| Lemma 3.1(c), height and gap identities | VERIFIED |
| Lemma 3.1(d), arrival derivative | VERIFIED |
| Lemma 3.2, disjointness and order | VERIFIED |
| Lemma 3.3, density bounds | VERIFIED |
| Lemma 4.1, gap-death bound | VERIFIED |
| Lemma 4.2, tilt-death bound | GAP |
| Lemma 4.3, lateral and wall bounds | VERIFIED |
| Lemma 4.4, conflict bound | VERIFIED |
| Corollary 4.5, total death bound | VERIFIED |

## Errors and gaps

E1. [S, Corollary 2.3]: the area argument counts S2 as a unit-area square even when S2 is the floor. That inference is invalid. Restricting the neighbourhood to the packing half-plane repairs the claimed bound.

E2. Termination after step 7: increasing height alone does not imply that a square cannot be crossed twice. The missing argument is that every top-side point of a flat square is higher than every bottom-side point of that square, since cos(phi) > |sin(phi)|. This repairs termination.

E3. Lemma 3.1(a): the claim that conflicts create only finitely many cuts needs a finite polygonal description of the truncated probe regions. The argument in the note does not give that description. The finite subdivision construction below repairs it.

E4. Lemma 4.2: “exactly as there” omits the incidence and weight argument needed after changing the gap direction. The perpendicular expansion, disjointness, and rectangle-incidence calculation below repair it without importing any result from [S] outside Section 2.

No scoped claim is marked WRONG: I found no counterexample to its assertion. E1 is an error in the supplied proof of a cited assertion, not a counterexample to that assertion.

## Fundamental lemma and conventions

**[S, Lemma 2.1].** A nonnegative convex piecewise affine gap function on an interval of length lambda, with nonzero slopes of magnitude at least phi and slope jumps at least 2, has integral at least phi(2-phi)lambda²/4. For phi=0 the conclusion is immediate. At an endpoint minimum the lower bound phi lambda²/2 is stronger. At an interior minimum the adjacent slopes are -p and q, with p,q >= phi and p+q >= 2. Integrating the supporting V gives (pa²+qb²)/2, whose minimum over a+b=lambda is lambda²/[2(1/p+1/q)]. The maximum reciprocal sum under the constraints is 1/phi+1/(2-phi); this follows by reducing the larger slope until either the smaller is phi or their sum is 2, and then maximizing on the remaining closed interval at an endpoint. This proves the stated constant. Flat zero intervals can occur only in the trivial phi=0 case. Trying an asymmetric V, or a minimum at an interval endpoint, does not defeat the bound.

**[S, Lemma 2.2].** The width-one rectangle joining two square centres, or a square centre to the floor, is in the region and contains waste at least theta(2-theta)/[4(m'+1)]. For two squares, the segment of centres is in the convex erosion by the radius-1/2 disc. Its radius-1/2 neighbourhood contains the rectangle. For the floor, downward closure gives containment.

For |t|<1/2 the endpoint centre lines are strictly inside their respective squares. Any other square meeting a chord cannot cross either of these barrier lines inside the open strip. Its intersection with the strip is convex and connected, and consequently lies between the barriers. Each square has projection length at least 1, so it contributes at most one entry/exit height in this open strip. Removing these at most m' heights leaves at most m'+1 intervals of constant square order. On each interval, each intervening gap is nonnegative and convex; its slope jumps are at least 2, and away from jumps its slope magnitude is at least the orientation distance of its two bounding objects. The latter follows from |tan b-tan a| >= |b-a| and reduction modulo pi/2. Lemma 2.1 applies. Summing the angular distances uses the metric triangle inequality and the increasing function t(2-t) on [0,pi/4]. Finally sum lambda_r² >= 1/(m'+1). This re-derives the lemma, including contacts: boundary-only chords at the finitely many removed heights have no area. Axis-parallel sides cause no interior infinite-slope difficulty; horizontal projection edges occur at projection endpoints. Diamonds with inclination pi/4 cause no change to this argument.

**[S, Corollary 2.3], repair of E1.** For a 1 by 1.82 rectangle the radius-sqrt(2) neighbourhood has area

    1.82 + 2 sqrt(2)(1+1.82) + 2 pi = 16.079349799 < 16.1.

Thus at most 16 unit squares meet it. With two square endpoints, subtracting both leaves at most 14 others. With a floor endpoint there is only one endpoint square, so that subtraction is invalid. However, all packing squares are above the floor. The part of the neighbourhood strictly below the floor has area sqrt(2)+pi. Hence the relevant neighbourhood has area at most 11.523543583, allowing at most 11 squares total and at most 10 others. In particular 14 remains a valid bound. Then

    (2-pi/4)/60 = 0.0202433639434 > 1/50,
    sqrt(1.82²+1/4) = 1.88743211798 < 1.9.

These establish the corollary. A square touching R only at a boundary point is still entirely in the closed neighbourhood, so the count remains valid.

**Section 1.** The orientation distance is a metric modulo pi/2. For two flat squares, the representative difference has magnitude below 2tau <= 0.16 < pi/4, so no wraparound occurs. All crossing and probe directions have positive vertical component, including at the allowed limiting tilts. A square of inclination pi/4 is steep and need not be assigned a flat-square crossing frame.

The right-wall rectangle is contained in the region: the centre's vertical segment of length 1 lies in its inscribed disc, and every horizontal segment from there to the right wall stays under an increasing ceiling. The fundamental-lemma strip proof works with all squares to the left of the wall. Its numerical short-distance corollary also works: the half-plane restriction just used for the floor applies after rotation. For the left-wall rectangle the exact additional condition is y_c+1/2 <= w; necessity follows at x=0 and sufficiency follows from increasing g. Bottom and right containment already follow from the inscribed disc and x_c <= L.

For a left-wall exception that can emit within delta, phi must be positive. Write its top-left vertex as (a,b), c=cos(phi), s=sin(phi). Then

    0 <= a <= delta s,
    x_c = a+(c+s)/2 in [0.5,0.540855535] subset [0.5,0.55],
    y_c <= w+zeta(a+c)-(c+s)/2 <= w-1/2+1.1 zeta.

Here a+c <= sqrt(1+delta²) < 1.1 and c+s >= 1. Failure of rectangle containment gives y_c>w-1/2. Three centres in a box of width 0.05 and height at most 1.1 would, when ordered vertically, have consecutive vertical separations at least sqrt(1-0.05²); two such separations exceed 1.1. Thus at most two exceptions occur. Equal tilts and coincident wall contacts do not increase that number. The minimum centre distance 1 follows from the disjoint open radius-1/2 inscribed discs.

## Flow: each numbered step

The claimed construction assigns a single upward path to every floor point until a death, arrival, or vertex exception. The first-hit parameter exists: the relevant boundary and square sets are closed, there are finitely many, and the positive vertical component forces a boundary hit in finite distance. Before this hit the ray stays in the region and outside other squares; it also immediately leaves its emitting square. Truncation at delta produces a segment with waste interior. It need not have positive length.

The following configurations supply concrete degeneracy tests. Define Z(phi,c) to be the unit square with centre c and side vectors (cos phi,sin phi), (-sin phi,cos phi), each centred parameter ranging over [-1/2,1/2]. All the configurations below fit, for example, in L=8, w=5, zeta=0.1 unless a different ceiling is specified; they are local tests, not all necessarily reached from the floor before the gap budget expires.

* Axis contacts: [1,2]x[0,1], [1,2]x[1,2], and [2,3]x[0,1] have edge contacts and vertex contacts. The first two give zero-length probes on a positive-length interval.
* Budget equality: a square [1,2]x[delta,1+delta] gives G+r*=delta on the whole initial interval (1,2).
* A vertex hit: [1,2]x[0.02,1.02] is first hit at a vertex by floor x=1 or x=2, but through its bottom side for x in (1,2).
* Equal-tilt contacts: Z(phi,(2,2)) and Z(phi,(2,2)+n_phi), for phi=0.079 or -0.079, share a top/bottom edge. Replacing n_phi by (1+epsilon)n_phi gives a prescribed gap epsilon, including epsilon=delta. Translating instead by u_phi gives a lateral edge contact.
* Actual conflicts: take alpha=0.079, Z(-alpha,(2,2)) and Z(alpha,(2+cos alpha+sin alpha,2)). Their horizontal projections meet at a single line, and their inner upper vertices coincide. Probes from open top-side intervals near these vertices converge and cross above them. These give positive-measure conflicts, not merely vertex exceptions. The estimates below allow them.

**Step 1.** Stop at any emitter point whose full truncated probe meets a probe of another emitting object. This removes the entire interacting emitter set, including endpoint-only interactions and singleton probes. It may remove a path before the part it would actually travel meets anything; that is conservative and is exactly what Lemma 4.4 estimates. The converging two-square configuration above tests a genuine positive-measure instance. No assertion of injectivity is needed to define this stop.

**Step 2.** If the next gap would exceed the remaining budget, travel precisely delta-G and stop; otherwise add the actual first-hit distance and process that hit. On the equality example above, the algorithm continues through the square, as required by its strict inequality. If G=delta and the next r*=0, it can still cross a touching square; if r*>0 it stops at the emitter. These cases preserve the budget and cause no missing positive-length segment.

**Step 3.** A first hit at any square vertex is discarded before applying square-side rules. The vertex example shows that genuine grazing hits are covered. For a fixed prior itinerary, the emitter moves with a nonzero component perpendicular to the probe direction; the set of rays through any fixed vertex therefore contains at most one parameter. Finitely many itineraries, justified below, imply finitely many such starting points. This is a zero-measure exception, unlike conflicts.

**Step 4.** A boundary hit outside every other square stops at the ceiling or wall. It can coincide with the current emitter and thus have zero distance. For example, a square with phi=arctan zeta<tau can have its whole top side on the ceiling, giving a positive-length set of immediate arrivals. This does not contradict the height identity: the preceding gap contribution varies along that interval. If a hit is on another square as well, the square/vertex rules take precedence. A relative-interior bottom hit of a flat square on the ceiling cannot direct the path out of the region: the square's inward bottom normal has positive scalar product cos phi+zeta sin phi with the ceiling's outward normal (-zeta,1), so such an interior bottom contact is incompatible with containment.

**Step 5.** Stop whenever a nonvertex hit belongs to a square with inclination at least tau. Equality a=tau is included; inclination pi/4 is included. No top/bottom convention is needed for this terminal square. A tilted square touching a flat one at a single vertex is instead handled by step 3.

**Step 6.** Stop at a relative-interior lateral hit of a flat square. This is a closed-case distinction after excluding vertices and steep squares. Equal-tilt lateral neighbours do not give a positive interval of such hits: their normals are parallel to the lateral sides, and a top-side interior point cannot lie on the neighbour's lateral supporting line without overlapping the neighbour or being its own top vertex.

**Step 7.** Every remaining square hit is in the open bottom side, and normal translation by one unit crosses its interior and reaches its open top side. For positive gap length, the first-hit condition gives n dot nu <= 0. The top-side outward normal of a flat target has strictly positive dot product with n, since the angular difference is below 0.16; a top entry is impossible. For zero gap, two nonvertex square-side contacts require a common supporting line and opposite interior half-planes. The other side is consequently the parallel bottom side. An axis-parallel square touching the floor gives the same bottom-entry case. These arguments cover the edge-contact examples above.

**Termination, repair of E2.** A flat square's highest bottom point is strictly below its lowest top point by cos phi-|sin phi|>0. Once crossed, an upward path can never enter its bottom side again. A first later lateral hit would stop, rather than cross. Thus every successful step 7 uses a new square, and finiteness of the packing bounds the number of iterations. This, rather than height increase alone, supplies the missing termination argument.

## Structure lemmas

**Lemma 3.1(a), repair of E3.** The claim is a finite partition into intervals of fixed crossed squares, hit sides, and stopping event, with all vertex events removed. For each emitter, compare the finitely many candidate line-intersection distances to all target sides and region boundaries. Subdivide its unit parameter interval at the linear inequalities deciding side membership, nonnegative distance, nearest target, and truncation at delta. On every resulting interval, the end of the probe is affine in its parameter. The union of these probes is a polygon, possibly degenerate: it is described by the emitter parameter and distance inequalities 0<=r<=a+bs, followed by an invertible affine map. Therefore every emitter's probe region is a finite union of polygons. Its intersections with another emitter's moving probe are governed by projections of finite systems of linear inequalities, hence give finitely many intervals and endpoints. This remains true with open emitter endpoints; isolated boundary points are added to the partition.

Now induct on the at most n square crossings. Current emitter coordinates and accumulated gaps are affine on each partial-itinerary interval. Pulling back the finite subdivisions just described, and the affine budget equality, makes only finitely many cuts at each stage. Vertex hits are isolated because of the perpendicular nonzero derivative in 3.1(b). This proves (a). In particular a whole interval of budget equality, or of zero-length contacts, is kept as an interval; it is not incorrectly declared a finite exceptional set. This construction supplies the polygonal step absent from the note's proof.

**Lemma 3.1(b).** On a fixed itinerary the parameter of each crossed square has derivative the product of the secants of successive flat-angle differences, with the floor's angle zero. Taking the scalar product of the hit displacement with the preceding u gives ds_new cos(phi_new-phi_old)=ds_old. Thus the derivative is positive and at least 1; line-intersection distances, and the final budget truncation, are affine. Equal tilts give factor 1, not an artificial expansion. Near the permitted maximum difference 0.16 all denominators remain positive. The proof does not assert measure preservation: it asserts expansion of transverse emitter measure.

**Lemma 3.1(c).** The height after each completed crossing and gap is gamma_0+sum(1+gamma_i)cos phi_i. Hence h_i and the crossing-height interval have the stated values, and arrival gives N-D+Gtilde, with 0<=Gtilde<=sum gamma_i<=delta. Each term is actual displacement in its own previous square's normal direction. No vertical-gap substitution is being made. Zero gaps and boundary arrivals preserve the identity.

**Lemma 3.1(d).** On an arriving interval, the terminal abscissa has derivative

    kappa' = kappa_N/(cos phi_N+zeta sin phi_N)
           = kappa_N cos zeta'/cos(phi_N-zeta') >= cos zeta'.

The denominator is positive, including negative flat tilts and zeta=1. Since N and all phi_i are fixed, N,D are constant and Gtilde'=zeta kappa'>=sin zeta'>=zeta/sqrt(2). With no squares, x'=x and Gtilde=g(x), so the separate N=0 convention is correct. No endpoint equality causes a derivative claim outside an itinerary interval.

**Lemma 3.2.** Distinct nonexceptional paths are disjoint and retain left-to-right order at every common height; arriving abscissas are strictly increasing. The paths are finite compact polygonal arcs, so a first common height exists if they meet. Inside a square, the same normal crossing forces a lower common entry. Outside squares, two distinct-emitter probes would have been killed at their emitters; same-emitter probes are distinct parallel segments unless their emitter points agree. At a nonvertex square boundary, an incoming positive-length probe cannot meet the interior of a top crossing from below: it would enter that square's interior before the claimed first hit, since the relevant normal dot product is positive. Two top crossings in distinct squares would force overlapping interiors near their shared relative-interior top point. Zero-length contacts simply concatenate crossings and do not create a new type of incoming positive-length arc. The same first-common-height argument therefore applies at them. These exhaust the axis contacts and converging-probe tests.

Order follows for disjoint graphs over height. For arriving paths, suppose the left path ended at abscissa at least that of the right path. At the right path's terminal height, order puts the left path strictly to its left, where the increasing ceiling has smaller height, a contradiction. This establishes global arrival injectivity, not just an intervalwise derivative.

**Lemma 3.3.** A given flat square is crossed by floor parameters of total measure at most 1; a square first reached from the floor is reached by measure at most sqrt(2). On each itinerary interval the first map expands by kappa>=1 into the open bottom parameter interval (0,1). Disjointness prevents images of distinct intervals from overlapping. Summing their lengths proves the first assertion. The second is bounded by the square's horizontal projection, cos a+sin a<=sqrt(2), since the initial probe is vertical. Vertices add only finitely many parameters. Merely proving a local derivative would not suffice for the first assertion; Lemma 3.2 supplies exactly the necessary global multiplicity bound.

## Death estimates and constants

**Lemma 4.1.** Gap deaths have total starting measure at most W/delta. In an itinerary gap the map (x,r) -> e(x)+r n has absolute Jacobian kappa>=1. Integrating over the actual, possibly x-dependent travelled r-interval therefore gives area at least the integral of gap length in x. Disjointness permits summation over stages and itineraries; within a path, heights increase. Every gap-death path contributes exactly delta of length. Thus W>=delta times its starting measure. The endpoints, including zero-length pieces, have zero area. This verifies the area statement despite the changing gap directions.

**Lemma 4.2, repair of E4.** Let T be the tilt-death parameters. Every path's chain from floor to its terminal steep square has angular variation at least tau by the metric triangle inequality. Consecutive square centres are at distance at most sqrt(2)+delta; a first square's centre height is at most sqrt(2)/2+delta. Both are within the fundamental-lemma threshold.

Weight an ordered pair by the measure mu of paths in T using it consecutively. For a fixed outgoing square S, the sets for distinct successors are disjoint, and 3.3 gives sum mu(S,S')<=1. A first floor-to-square pair has mu<=sqrt(2). A waste point p in a square-pair rectangle has each endpoint square entirely within B(p,1.9+sqrt(2)/2). That disc has area 21.353423389<22, so at most 21 endpoint squares S occur. For floor pairs through p, square centres are horizontally within 1/2 of p, and their heights are at most sqrt(2)/2+delta. The entire squares therefore lie in a box of width 1+sqrt(2), height sqrt(2)+delta, and area 3.489657736<4, in particular allowing at most four. Thus

    tau |T| <= 50 W (21+4 sqrt(2))
            = 1332.842712475 W < 1350 W.

This uses no direction-specific property of a vertical gap after a square. It explicitly supplies the argument omitted by the reference to [S] outside its permitted Section 2.

**Lemma 4.3.** For an ordered flat pair (or floor-to-flat pair), the measure of emitter points that hit open lateral sides within delta is at most 2delta tan theta. For a given wall the corresponding measure is at most delta tan a. In the target frame an incoming probe changes its s-coordinate by at most delta sin theta. For each target side, only the one-sided strip of that width can reach it, and its preimage along the emitter line has length at most delta sin theta/cos theta. Sum over the two sides. The wall calculation uses x=0 or x=L and divides by the horizontal component cos phi of the emitter tangent. At theta=0 the only possible parallel contacts would involve an emitter endpoint or overlapping square interiors, as in step 6; there is no open-side hit. These arguments bound arbitrary subsets of emitters, regardless of whether their probes also conflict.

The factors used later are valid uniformly, since tan t/t and sec t increase for t>=0:

    2 tan(0.16)/0.16 = 2.01724325919 < 2.02,
    tan(0.08)/0.08 = 1.00213880885 < 1.01.

**Lemma 4.4.** Floor probes cannot meet square probes; for each ordered pair of flat squares the conflicted emitter set has arclength at most 4.3delta theta. All floor probes are below delta. Every top point of a flat square is at height at least cos phi (in particular above cos tau-sin tau>0.9), because its bottom side is above the floor. Square probes go upwards. Thus no floor/square conflict occurs.

For the pairwise estimate, let e=(s0,t0) emit from Z1 and let its probe meet a Z2 probe. Then its probe meets [0,1]x[1,1+delta], so 1-delta<=t0<=1+delta. If t0<1, disjointness puts s0 outside (0,1), and reaching that slab puts it within delta sin theta of an endpoint. The same conclusion holds when t0>=1 and s0 is outside (0,1). If t0>=1 and 0<s0<1, move backwards inside Z1 to just below t=1. The travel length is (t0-1)/cos theta+eta<1. If the s-coordinate there were in (0,1), the square interiors would overlap. Letting eta decrease to zero forces s0 within delta tan theta of an endpoint. Thus

    s0 in [-delta sin theta, delta tan theta]
          union [1-delta tan theta,1+delta sin theta].

The combined length is <=4delta tan theta; divide by cos theta for emitter arclength. Uniformly on theta<=0.16,

    4 tan theta/(theta cos theta) <= 4.08668458249 < 4.3.

At theta=0 the exterior strips have zero width, and an interior top emitter would force overlapping interiors by the backwards test. Thus the set is empty, not a hidden positive-measure exception. Endpoint-only probe meetings satisfy the same inequalities. The explicit converging pair above demonstrates why removing just vertex events would not have sufficed, and why the positive conflict bound is needed.

**Corollary 4.5.** Every nonexceptional nonarrival has one of the four charged death types (counting lateral and wall together). For each emitter, the total measure of its preimage in starting x is at most its emitter arclength: intervalwise kappa>=1 plus Lemma 3.2 prevents multiplicity. A square pair responsible for a lateral death or conflict has centre distance at most sqrt(2)+2delta, since the emitter points are within sqrt(2)/2 of the centres and the two probes have total length at most 2delta. Thus the angle is chargeable by 50 times rectangle waste.

For a fixed waste point, there are at most 21 squares in the radius-(1.9+sqrt(2)/2) disc, hence at most 21*20=420 ordered distinct pairs. The coarser radius 2.61 still has area 21.400843316<22 and gives the same integer count. For floor incidences the box above gives at most four squares. For each wall the rotated box has width sqrt(2)+delta and height 1+sqrt(2), again giving at most four. A wall-hit square has centre distance at most sqrt(2)/2+delta from that wall, so this box argument applies. The left wall uses its chargeable rectangles only; the two unchargeable squares were counted separately in Section 1.

The constants are consequently

    50*(6.32*420 + 2.02*4 + 1.01*8) = 133528 <= 134000,
    1/delta + 134000delta = 4219.5 <= 4250,
    2*1.01*delta*tan(0.08) = 0.005060800985 < 0.01.

The last displayed exceptional contribution in the note has a harmless extra factor 1.01: the direct wall estimate would give 2delta tan tau. Both bounds are below 0.01. Overcounting two lateral sides, ordered square pairs, or a point subject to more than one possible death only enlarges these upper bounds. This re-derives the stated total measure bound.

## Uses in Sections 5–7

I checked these sections only for stronger demands on Sections 1–4, not as a separate audit of their lemmas.

* Section 5 uses ordered disjoint graphs to obtain disjoint tube interiors, the height intervals from 3.1(c), and the fundamental lemma for arbitrary squares in a horizontal chain, including steep squares. [S, Lemma 2.2] and its repaired corollary do cover arbitrary orientations. Horizontal lines through vertices and endpoints of crossing-height intervals should be excluded when stating the linewise square-order argument; there are finitely many relevant heights, so this requires only an almost-everywhere formulation, not a stronger flow theorem.
* Section 6 uses constant N,D on each arriving interval, finite one-sided affine limits, monotonicity of arrival abscissas, and gap partial sums in [0,delta]. These are exactly the assertions established above, once the partition gap E3 is repaired. No conservation of starting measure is needed.
* Section 7 uses that arrival-image measure is at least cos(zeta') times starting measure, and that the intervening image gaps are disjoint. This needs both the local derivative in 3.1(d) and the global order in 3.2; neither alone suffices. Both are available. It does not assume the map is measure preserving.

I found no later use of a substantively stronger flow assertion. The later proof inherits E1, E3 and E4 until those missing arguments are inserted; E2 supplies the finite iteration bound needed for E3. All four repairs above are compatible with the constants and definitions in wedge.md. This audit does not independently certify Sections 5–7 or Theorem B in their entirety.

FATAL: no
