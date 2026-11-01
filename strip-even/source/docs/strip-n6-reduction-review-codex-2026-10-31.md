# Blind referee report on docs/strip-n6-reduction.md, Codex, 2026-10-31

Blind review (Codex CLI 0.163.0, `codex exec -s workspace-write` in a scratch directory holding the document, o1dp/SPEC.md, o2cert/LEMMAS.md, proof-F6.md and m4check.py). Verdict on the first version: not as written, one MAJOR (Lemma 2.1 used the vertical extent of the Minkowski sum to place (0, dy) in its interior, which is false; the repair is |dy| < 1 via the unit disk contained in the sum). The repaired document is the current docs/strip-n6-reduction.md. Report reproduced verbatim below.

---

# Referee report: packing-to-chain reduction

Reviewed `reduction.md` against the supplied O1 definitions, O2 lemmas, and `proof-F6.md` §1–3. O1 and O2 are accepted as the black boxes specified in the packet; their implementations and certificates were not re-audited. Line references below refer to `reduction.md`. **There is one major mathematical error, with a short repair that suffices for the stated theorem.**

1. **MAJOR — Lemma 2.1 is false as stated; vertical projection is confused with vertical section.**

   Exact sentences (lines 19, 21): “If c'_x ≥ c_x and |c'_y − c_y| < h(θ) + h(θ'), then c'_x − c_x ≥ κ(θ, θ', c'_y − c_y).” “The vertical extent of Δ is ±(h(θ) + h(θ')), so |dy| below that bound puts (0, dy) in the interior of Δ.”

   The second sentence is false: central symmetry does not imply symmetry about the y-axis. A horizontal section can lie wholly to the right of that axis. Consequently the lemma itself, not merely its proof, is false.

   Counterexample: take θ = θ' = π/8, c = (0,0), c' = (0,6/5). Here Δ = 2S(π/8), whose inequalities are

       |x cos θ + y sin θ| ≤ 1,
       |−x sin θ + y cos θ| ≤ 1.

   We have 6/5 < 2h(π/8) = 1.3065629648763766, but (6/5)cos(π/8) = 1.1086554390135441 > 1. Thus the two squares are strictly separated, even as closed sets. At y = 6/5 the section has endpoints

       x_min = ((6/5)cos θ − 1)/sin θ = 0.2839303450949611,
       κ = (1 − (6/5)sin θ)/cos θ = 0.5853359254446799.

   The claimed conclusion is 0 ≥ κ. Taking c'_x = 0.1 instead also gives a counterexample, so the problem is not confined to ties in x-order. These counterexamples need a taller strip and do not refute the intended theorem.

   **Fix:** replace the lemma's height hypothesis by `|dy| < 1` (or explicitly assume `(0,dy) ∈ int Δ`). Every centred unit square contains the closed disk of radius 1/2; therefore Δ contains the closed unit disk, and `|dy| < 1` puts `(0,dy)` in its interior. The last sentence of §2 already supplies precisely the needed bound:

       |Y_j − Y_i| ≤ H − h_i − h_j ≤ H − 1 < 1.

   Use this bound before applying the repaired lemma. Alternatively, use O1's vertical-section bound `|dy| < b_i+b_j`, with `b_i = 1/(2 max(cos θ_i,sin θ_i)) ≥ 1/2`.

   The other steps of the lemma are correct. For full-dimensional convex bodies, intersection of their interiors is equivalent to the centre difference belonging to `int(S + (−S'))`; central symmetry gives `−S' = S'`. Once `(0,dy)` is interior, κ is positive, and every point with `0 < dx < κ` is interior by the segment argument; `dx = 0` is the interior point itself. No stronger ordering assumption than `dx ≥ 0` is needed.

2. **MINOR — Δ need not be an octagon with eight distinct sides.**

   Exact sentence fragment (line 11): “the Minkowski sum of the two centred squares (a centrally symmetric octagon)”.

   Coincident orientations modulo π/2 give a square. **Fix:** say “a centrally symmetric convex polygon with at most eight sides.” The facet formula remains valid with duplicate normals; only normals with positive x-component enter its right-boundary minimum, exactly as in O1. The definition of κ itself is sound: compactness gives the maximum whenever the horizontal line meets Δ. For all heights used in this reduction, the unit-disk argument in finding 1 proves the stronger interior intersection.

3. **NOTE — The setting and containment inequalities are correct; the omitted feasibility constraint is redundant on this height range.**

   Exact sentences (line 7): “since a square has 90° symmetry we may take θ_i ∈ [0, π/2).” “Its axis-parallel half-extents are both h(θ_i) = (cos θ_i + sin θ_i)/2 ∈ [1/2, 1/√2].”

   Neither statement needs correction. Reducing an arbitrary angle modulo π/2 preserves the actual square; it does not reflect that square or incorrectly fold its tilt into [0,π/4]. Taking the largest absolute coordinate among its four centred vertices gives the stated h, and containment gives both inequalities (1). Closed squares with pairwise disjoint interiors allow boundary contact, consistently with the weak inequalities throughout.

   The old reduction explicitly imposed `h(θ_i) ≤ H/2`. Here it is automatic because `2h(θ_i) ≤ √2 < 1.87 ≤ H`. Thus every box factor is nonempty, indeed has positive length, for every tilt in the closed cube. No constraint was lost. This observation is worth adding where B_θ is introduced.

4. **MINOR — Lemma 4.1 is true, but its proof only writes the midpoint case.**

   Exact sentence (line 36): “The right boundary of a convex set, as a function of height, is concave: if (x, y) and (x', y') are in Δ then so is their midpoint, so κ((y + y')/2) ≥ (x + x')/2; take x = κ(y), x' = κ(y').”

   Midpoint concavity alone is not the definition of concavity without a regularity argument. **Fix:** replace the midpoint by an arbitrary convex combination. For `0 ≤ λ ≤ 1`, convexity directly gives

       κ(λy + (1−λ)y') ≥ λκ(y) + (1−λ)κ(y').

   The lemma's whole stated open interval is valid: it is the interior of the vertical projection of Δ, whether or not `(0,y)` lies inside Δ. Thus finding 1 does not invalidate Lemma 4.1. Concavity in fact holds on the closed projection interval as well.

5. **NOTE — The chain bound, box minimisation, and theorem assembly work after finding 1 is repaired.**

   Exact sentences (lines 27, 38, 59): “Relabel the squares so that X_1 ≤ X_2 ≤ … ≤ X_6.” “A concave function on a box attains its minimum at a vertex.” “By (3), L ≥ Φ^σ(θ, H) for some role pattern σ and tilt vector θ.”

   The telescoping identity in (2) is correct. By (1), `X_6+h_6 ≤ L` and `X_1−h_1 ≥ 0`, so their difference is at most L; the end squares need not furnish the union's outermost edges. Every consecutive pair satisfies the repaired lemma. In fact equal centre x-coordinates cannot occur in such a packing: they would put the centre difference inside Δ by `|dy| < 1`, contradicting disjoint interiors.

   Each difference of coordinates maps the whole box B_θ into the domain of Lemma 4.1. Therefore the sum defining Φ_θ is concave. Every point in a box is a convex combination of its finitely many vertices; concavity bounds its value below by at least the smallest vertex value. This proves the claimed vertex minimum without requiring that any such vertex placement be an actual packing. Only a lower bound is being obtained.

   The minimum over tilts in (3) also exists for fixed H < 2. The section stays uniformly in the interior range `|dy| ≤ H−1 < 1`; the polygonal section endpoint varies continuously with the tilts there. Compactness of the closed tilt cube and finiteness of the role set then give attainment. Moreover `S(0)=S(π/2)` and `h(0)=h(π/2)`, so replacing every π/2 endpoint by 0 preserves Φ exactly: the closed and half-open cubes have the same attainable values and the same minimum. The parenthetical sentence at line 42 is therefore valid but weaker than what is available.

   **Suggested clarification:** prove the vertex bound for the packing's own tilt vector first, then write “Choose a minimizing vertex for those tilts.” This makes the existential claim at line 59 immediate, without leaving attainment of the global minimum implicit. O1 covers 62 patterns, O2 covers FCFCFC, and the reflection lemma covers CFCFCF. No case is omitted.

6. **NOTE — The role table and mirror identity use the correct signs and index order.**

   Exact sentences (lines 42, 51): “At a vertex the displacements are dy_i = Y_{i+1} − Y_i … exactly the table in `o1dp/SPEC.md`.” “Φ^{CFCFCF}(θ, H) = Φ^{FCFCFC}(π/2 − θ, H), where π/2 − θ is taken coordinatewise.”

   Both are correct. In O1, `(r,t)` is square i on the left in centre-x order, and `(r',t')` is square i+1. Direct subtraction gives FF: `h_{i+1}−h_i`; FC: `H−h_i−h_{i+1}`; CF: `h_i+h_{i+1}−H`; CC: `h_i−h_{i+1}`. For FCFCFC this is exactly O2's sign vector `(+,-,+,-,+)`, including its indexing in Lemma 2.

   Reflection in y = H/2 preserves every centre x-coordinate and therefore the chain's index order. It swaps roles, negates dy, preserves h, and sends S(θ) to S(−θ) = S(π/2−θ). Reflecting Δ gives the stated κ identity, including θ = 0 or π/2. Add the sentence about preserving x-order to make this fully explicit. Boundary contact and dy = 0 cause no exception.

   **Computed:** `verify_review.py` loads only the first 29 lines of `m4check.py`, removing the four prohibited classes of import/path lines. Its own role-based chain and its separate O2 sign-based chain use the resulting hull κ. With seed 20261031, 5,000 random tilt vectors and heights in [1.87,2) gave maximum absolute discrepancies:

   | Check | Maximum discrepancy |
   | --- | ---: |
   | CFCFCF versus reflected FCFCFC | 3.55 × 10⁻¹⁵ |
   | Role-based FCFCFC versus O2 sign formula | 1.78 × 10⁻¹⁵ |
   | Pairwise κ reflection | 9.99 × 10⁻¹⁶ |
   | Independently written eight-normal formula versus hull κ | 8.88 × 10⁻¹⁶ |
   | Four displacement-table entries versus centre subtraction | 2.22 × 10⁻¹⁶ |

   Also tested 5,000 convex-combination inequalities across the full vertical projection interval: maximum apparent violation 1.55 × 10⁻¹⁵. For 100 random tilt/height boxes, enumerating all 64 vertices gave no vertex minimum greater than the sampled interior value. These are diagnostics, not substitutes for the analytic proofs.

7. **NOTE — The numerical reference needs care at the H = 2 boundary; the mathematical reflection identity remains correct.**

   Exact sentence (line 53): “The displacements of the reflected configuration are the negatives of the originals, so the chain values agree.”

   No mathematical correction is needed. In additional tests on all `3^6` vectors with coordinates in `{0,π/4,π/2}`, the binary64 reference agreed within 1.78 × 10⁻¹⁵ at H = 1.87, 1.99, and the predecessor float of 2. At H = 2 it showed a spurious discrepancy of about 3 for the all-upright endpoint vector and its reflection. Ordinary floating-point `cos(π/2)` is not zero; the exact straddling comparisons in `m4check.py` can then discard points on the intended top/bottom section.

   I repeated all 2,916 endpoint cases using a separately written section computation with 70-digit arithmetic and canonical coordinate pairs `(1,0)`, `(1/√2,1/√2)`, `(0,1)`, preserving the endpoint symmetries exactly. Maximum discrepancy was 1.45 × 10⁻⁷⁰, including H = 2. Results are in `endpoint-results.json`; the original binary64 diagnostics are retained in `verification-results.json`. This is a limitation of this reference test at a degenerate boundary, not a finding against the accepted O1/O2 certificates.

8. **NOTE — F6, the black-box interfaces, and the height restrictions are consistent.**

   Exact sentences (lines 46, 48–49): “Since each coefficient of H in L is negative, L(θ, ·) is decreasing for every θ, hence F6 is decreasing in H.” O1: “for every H ∈ [1.87, 2) … Φ^σ(θ, H) > F6(H) for all θ ∈ [0, π/2]^6.” O2: “for every H ∈ [1.87, 2], Φ_M(θ, H) ≥ F6(H) for all θ ∈ [0, π/2]^6.”

   Direct differentiation gives `∂L/∂H = −3cot θ − 2tan θ < 0`, matching `proof-F6.md` and O2. For H < 2, L tends to +∞ at both ends, so its minimum is attained in the open interval. Pointwise comparison at a minimizer gives strict decrease of F6; alternatively `3cot θ+2tan θ ≥ 2√6` gives a uniform strict comparison. No use of the uniqueness or closed-form parametrisation is necessary.

   O1's opening goal uses the half-open cube, whereas its cell coverage uses the closed cube. The two statements are equivalent by endpoint periodicity, as explained in finding 5, without any appeal to preservation of strict inequalities under limits. The excluded patterns are exactly the two alternating patterns. O2's Objects section writes H < 2, but its stated scope, Theorem 10 and the reduction through Theorem 11 include H = 2, consistent with the packet's accepted black box. The conventions for L match the swarm's formula; its optimal spiral tilt and the chain's mirror tilt are related by π/2−θ, not by identifying the two angles.

   H < 2 is used in the geometry to get the strict interior bound `|dy| < 1`, subsequently needed for the pair constraint. It also makes the compact-parameter continuity argument above straightforward. It cannot be replaced by H ≤ 2: two upright squares at vertical separation 1 may have dx = 0 while the closed-section κ equals 1. The geometry before the certificates works for `√2 ≤ H < 2` with feasible boxes; the specific number 1.87 has no further geometric role. Its other appearances are the certified ranges and the automatic feasibility/sign facts `H > √2`.

9. **MINOR — §7 states implementation premises more specifically than the supplied files substantiate, and describes the certificate target imprecisely.**

   Exact sentences (lines 65–67): “both certificates evaluate κ through closed forms that were gated against a brute-force hull computation … and target L(θ0, H) ≥ F6(H) for a trial θ0”; “O2 rests on … a convex surrogate with nine interval scans, replayed with directed rounding in `o2cert/src/corner_impl`”; “Both computations assume IEEE-754 binary64 arithmetic with a libm whose cos, sin and sqrt are within 8 ulps (O2) resp. the padding stated in `o1dp/SPEC.md` (O1).”

   The substantive analytic dependencies match the supplied documents: O1 uses its gap lower bounds, min-plus DP and monotonicity of F6; O2 uses its dual Ψ, corner certificate and remaining box computation. But `L(θ0,H) ≥ F6(H)` is just the automatic upper-target inequality, not the inequality that certifies the chain bound. O1 explicitly requires `D > F6_ub(slice)`, where `F6_ub` encloses `L(θ0,Ha)` at the slice's left endpoint. O2's supplied lemmas formulate the required `Ψ ≥ F6` inequality, not an implementation of a common trial-angle target.

   O1 specifies a hull gate and outward rounding, with “a few ulps” of libm padding. The supplied O2 lemmas specify the corner radius, corner-region coverage and box reduction, but do not establish the nine scans, the named source path, the hull gate, or the 8-ulp machine contract. O1's exact quantitative machine assumptions likewise cannot be recovered from “a few ulps.” These details may be true in the unprovided implementation records; they are not verified by this packet. **Fix:** cite the precise certificate README/SPEC and machine contract for those assertions, or limit §7 to the analytic premises actually supplied. Acceptance of the black boxes does not turn undocumented provenance into checked evidence. This does not require re-running either black box for the geometric repair.

10. **NOTE — The old proof contributes no missing hypothesis, but sharpness is a separately cited result.**

    Exact sentences (lines 3, 61): “It replaces the swarm's Step 1–2 … which used separating lines and Rédei's theorem; the argument below only sorts centres by x.” “The bound is attained by the Morandi configuration … so F6(H) is the exact minimum width for these H.”

    Centre ordering and the repaired pair lemma genuinely remove the need for separating-line selection, common horizontal transversals and Rédei's theorem. The swarm's §2 contains the same mistaken implication from vertical projection to `(0,dy) ∈ int Δ`; it cannot repair finding 1 by citation. Its explicit tilt-feasibility condition is redundant here, and its warning against independent folding into [0,π/4] is respected. The new displacement table retains the height differences for equal roles.

    The new document does not need the swarm's stronger “no loss”/equivalence language or assert that every minimizing chain is realizable. Sharpness is instead imported from the Morandi construction in §3.1, with the optimizing branch discussed in §3.2. Given that separately established construction, line 61 is justified; it does not follow from O1/O2 and the lower-bound reduction alone. No additional premise from the replaced §1–2 is needed.

**Verdict:** **No, not as written:** Lemma 2.1 and its key interior assertion are false, so the displayed proof has a genuine gap despite the intended lower bound being recoverable. Replace its height hypothesis by `|dy| < 1`, prove interiority using the unit disk contained in Δ, and invoke the already established `|Y_j−Y_i| ≤ H−1 < 1`. With that local repair, the chain bound, vertex reduction, correct role table, reflection identity and accepted O1/O2 inequalities prove `L ≥ F6(H)` for every stated packing and every `H ∈ [1.87,2)`. The remaining changes are exposition and certificate-provenance corrections; no new packing classification or certified computation is needed.
