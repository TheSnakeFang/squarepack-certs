# Referee report: the general-even-n O2 reduction

Reviewed 2026-11-01 against `PACKET.md`. The inputs under `squarepack` and `o2n-draft` were read only. This review concerns the analytic reduction and specification, not an executed interval certificate. Independent calculations are in `audit.py`, `audit.json`, `audit.log`, `audit_extra.py`, `audit_extra.json`, `audit_blocks.py`, and `audit_blocks.json` in this directory. All three Python programs enforce a 900-second alarm; the runs completed successfully. No git commands were used.

1. **MAJOR — The five-variable origin obligation omits an essential domain restriction and is false literally as displayed.**

   Quote (§11, C0): “certify κ0^L := min_{|z|_∞ = 1} B1_L > 0”.

   With the coordinate order printed there, take `z=(-1,1,-1,1,-1)`. All four hinge terms vanish, and the displayed `B1_L` equals `−k/2`, which is negative throughout the proposed low-H interval. The intended restriction `x1≥0` is suggested by the preceding domain paragraph, but it must be present in this minimization. The author's `origin5.py` does enforce it with `z[:,0]=abs(z[:,0])`; that script therefore did not test the unrestricted displayed claim. The correct homogeneous domain is the tangent cone `x1≥0`, with the other four coordinates unrestricted, not the original clipped box with a fixed lower bound `−c`.

   There is a short exact repair, eliminating this computational obligation entirely. Let

   `s1=x1+Y2`, `s2=Y2+x3`, `s3=x3+Y4`, `s4=Y4+x5`.

   The displayed first-order expression is exactly

   `B1_L = (k/2)x1 + Σ_i [(k/2)s_i^+ + (1−k/2)s_i^-]`.

   For `x1≥0` and `0<k≤1`, this is at least `(k/2)(x1+Σ|s_i|)`, which is at least `(k/2)|z|_∞`: recursively recover each coordinate from the preceding coordinate and its edge sum. Equality occurs at `(0,1,−1,1,−1)`. Thus **the corrected constant is exactly `κ0^L=k/2`**, and the stated quadratic remainder gives `B_L≥0` on `|z|_∞≤k/16`. Independent floating LPs over every hinge sector and every cube face returned `−k/2` without the restriction and `+k/2` with it, at `k=.14,.15,.153064`. The identity and bound were also checked with exact rational arithmetic on all restricted cube grid points; the proof above, not those tests, establishes the result.

2. **MAJOR — The obligations do not cover the full interval used to define O2_n, including exactly H*(n).**

   Quotes (§0): “O2_n: Ψ_n(r; H) ≥ F_n(H) … H ∈ [H*(n), 2]”; (§11): “H_lo = 1.861098, 1.852049, 1.846936”.

   The upward-rounded starting points are correct for the stated *rational* certificate ranges. They leave nonempty intervals `[H*(n),H_lo)` outside the obligations. Certifying the listed cells cannot establish the broader §0 assertion on those intervals, and continuity at `H_lo` does not fill them. In particular the origin lemmas alone do not prove the complement inequality at exactly H*: Lemma 14(c) imposes necessary equality there, but does not prove block optimality away from the two excluded neighborhoods.

   Independent 70-digit computations give:

   | n | H*(n), approximately | T_n(H*) | F_n(H_lo)−n |
   |---|---:|---:|---:|
   | 6 | 1.8610971451879037034 | 0.88799708188304875 | −4.2024707906e−6 |
   | 8 | 1.8520484460607287756 | 0.91918263764547296 | −3.8446153996e−6 |
   | 10 | 1.8469355214063834396 | 0.93672826138506185 | −4.2852426048e−6 |

   At `1.861097` and `1.852048`, respectively, the gaps have the opposite sign: `+7.1378016059e−7` and `+3.0958843759e−6`. Thus using those downward-rounded numbers would actually make the desired inequality false at `r=0`. Fix the final theorem's range to `[H_lo,2]`, or add a root-constrained boundary certificate and all missing cells down to the exact H*. Do not claim the exact-root range from the present obligations.

3. **MINOR — Some numerical domain bounds are rounded inward; several tighter tail bounds have not been proved by the displayed tail estimate.**

   Quotes (§11): “c ≤ 0.4076” for n=8; “c ≤ c(1.86) = 0.3952” for the n=10 triple scheme; and the n=6 tail “Y_2, x_1 ≤ 3.061, x_3 ≤ 6.121”.

   At the actual starting heights, `c(1.852049)=0.407617087185222…` and `c(1.86)=0.395225289236325…`. The quoted caps exclude real wrong-sign slivers if used as machine bounds. Use the exact expression with outward rounding, or safe caps `.4077` and `.3953`. By contrast `.3935` for n=6 and `.4155` for the low-H n=10 scheme are safe.

   Lemma 20(c)'s *proved* uniform upper bound for `Θ/k` at the rational lower heights is approximately `3.09024413250` for n=6, `3.01269514531` for n=8, and `2.94164425617` for n=10 starting at 1.86. The first two do not imply the tighter printed tables. Independent 400-height numerical scans of the actual quotient found maxima `3.06064520140` and `2.99867340142`, consistent with those tables, but a scan is not their proof. Either certify the actual Θ bounds on every H-cell as §10 suggests, or use the larger analytic boxes. For example n=6 can safely use `3.091,3.091,6.182`; n=8 can use `3.013` for Y/end-x, `9.039` for its weakest x, and `4.520` for the middle-block x's. The n=10 printed positive-coordinate caps already exceed the analytic bounds at 1.86.

   This is a specification correction, not a counterexample to the reduction: using exact `c(H)` and the exact tail condition avoids it. It becomes a proof-coverage failure if an implementation silently uses the inward caps.

4. **NOTE — Lemmas 1–5 faithfully generalize the accepted n=6 reduction, including both ends.**

   Quotes: “s_i = (−1)^{i+1}”; “w_n = (1 + r_{n−1}) h(t_n) + G(r_{n−1}, t_n)”; “An interior coordinate lies in two pairs and an end coordinate in one”.

   Substitution gives `−r_i dy_i=−s_iHr_i+s_ir_i(h_i+h_{i+1})`. Since n is even, `s_{n−1}=+1`, so both end coefficients really are `1+r`; the alternating interior coefficients and `Hσ=−HΣρ` are correct. There are `n−2` A terms, m odd coordinates and `m−1` even coordinates. Each interior ρ occurs twice and each endpoint once. Adding the two exact m1 terms gives `n+kΣρ−Σd` with no missing endpoint contribution.

   The slice bounds in Lemma 1 are valid, including the boundary slice at H=2. Infima over `(t,r)` commute as infima, without a minimax theorem or r-attainment assumption. Lemmas 3–4 are genuinely n-independent: the integrand is nonnegative by the two support inequalities, its second derivative on a sign sector is its negative, and its minimum is among the endpoints and listed kinks. The formulas for E, m1 and the reflection symmetry follow. Fixing this finite candidate set gives a well-defined continuous A on all the clipped slivers, including zero coordinates; invalid-sign kink candidates must not displace a valid candidate in a numerical implementation.

5. **NOTE — The deficit cap, Corollary 6.1, and the H=2 equality are exact in both directions.**

   Quote (Proposition 6.4): “Lower bound: Corollary 6.1 at H = 2. Upper bound: at r = (1, −1, 1, …, 1) …”.

   Direct kink evaluation gives, with `R=√(1+x²)`,

   `dX=(1−1/R)(x+Y)+1−R` when `xY≤1`,

   `dX=1+x+Y−(x+Y)(1+x)/R` when `xY≥1`.

   The first branch increases in Y and the second decreases; their common maximum for fixed positive x is `D(x)=1/[1+x+1/x+√((x+1/x)(x+1/x+2))]`. This is at most `d0`, with equality only at `(x,Y)=(1,1)`. Symmetry gives the other kink. The axes have zero deficit. Thus the lower bound sums exactly `n−2` caps; the all-ones ρ vector attains every cap simultaneously. Lemma 9 at H=2 extends the lower bound from the orthant to every r, proving the asserted global minimum. This does not rely on a numerical optimizer or on the future obligations.

   Minor endpoint notation repair: the statement `sup_Y dX(x,Y)=dX(x,1/x)=D(x)` needs `x>0`; handle x=0 separately or define its limiting value. Also “with equality iff” in the deficit cap should explicitly mean equality in the upper bound, since equality at the lower bound is common.

6. **NOTE — The chain computation and Lemma 7 are correct on the intended H range.**

   Quote: “4 + (2n − 4)√2 − (n − 1)H”.

   Independently using only the specified filtered first 29 lines of `m4check.py`, I evaluated its hull κ on the alternating chain. At `(0,π/4,…,π/4,0)`, each end gap contributes `3/2+√2−H`, each of the `n−3` middle gaps contributes `2√2−H`, and the two exterior half-widths sum to 1. This gives precisely the quoted expression, not a numerical fit. Its equality to `f_n(1;H)` establishes the tangent bound by minimization in T. At H=2 it gives `5.3137084989847604`, `6.9705627484771406`, and `8.6274169979695208` for n=6,8,10.

   Across the 15 independent height tests listed in finding 10, hull evaluations of this formula differed by at most `4.45e−15`. The phrase “For every H” should be restricted to the domain where F_n has been defined and Lemma 6.3 applies (here H≤2, and in use H≥H*); the proof does not define F_n for arbitrary H>2.

7. **NOTE — Lemmas 8–11 preserve all signs and boundaries on the lowered H range.**

   Quotes: “c(H) := √(4/H² − 1)”; “There are n − 3 interior coordinates”; “R_n(H) := (n − 1) + (n − 3)c(H)”.

   The one-coordinate derivative bounds integrate even when the minimizing kink changes. A wrong-sign odd interior coordinate has upper slope `2/√(1+r²)−H`; an even one has lower slope `H−2/√(1+r²)`. The chosen c sets these to zero exactly, so non-strict monotonicity suffices at the threshold. Endpoint upper slope is at most `1+2/(3√3)−H`, already negative at H=1.8469 (approximately `−.4620`). Both endpoint clips are therefore justified independently of other coordinates. There are exactly `m−2` odd and `m−1` even interior coordinates, hence `n−3` possible negative ρ values.

   After clipping, if `Σρ≥n−1`, Corollary 10.1 and the tangent bound apply. Otherwise the total positive mass is less than `(n−1)+(n−3)c`, so every nonnegative coordinate has the required upper bound; negative ones already lie in `[−c,0]`. No point with ρ=0, `|ρ|=c`, or `Σρ=n−1` is omitted. In 1,500 independent random clipping tests down to H=1.8469, the largest computed increase in Ψ was zero. That is a diagnostic; the slope proof supplies the result.

8. **NOTE — Lemmas 13–14 give an exact decomposition, including independent wrong-sign splits, and the converse is valid.**

   Quotes: “For every two admissible splits … Σ … = Ψ_n(r; H) − n”; “with equality iff every block attains its infimum at z*_P”.

   For each coordinate, both splits have total coefficient k, so their combined linear contribution is `−(N_j−k)(ρ_j^+−ρ_j^−)=−(N_j−k)ρ_j`. Endpoint nonnegativity supplies the two exact m1 identities. This proves telescoping on the full clipped domain, not just its orthant; the wrong-sign split disappears identically on the orthant. Its coefficients need not equal the right-sign coefficients.

   Since each individual infimum is at most its value at the restricted r*, equality in the finite sum forces equality term by term; no simultaneous minimization assumption is being smuggled in. Conversely exact attained block bounds sum to `F_n−n`. At H*, every block has `B_P(0)=0`; equality in the decomposition bound forces its r* value also to be zero. The converse is necessary, not a proof of the block inequalities. Independent random admissible splits and mixed signs gave maximum telescoping residual `1.78e−14` over 1,500 tests.

9. **NOTE — Lemmas 15–17's local argument is valid; the kink pieces are piecewise affine transversely, not one affine function through the ridge.**

   Quotes: “sign(dX − dY) = sign((Y − x)(1 − xY))”; “the two kink candidates are affine in the transversal variable on each side of the ridge”.

   Below `xY=1`, subtraction gives `(R_x−R_Y)(x+Y−R_xR_Y)/(R_xR_Y)`. Squaring shows `(x+Y)²−R_x²R_Y²=−(1−xY)²`, so its sign off the hyperbola is `sign(Y−x)`. Above it, subtraction is `(x+Y)(q(Y)−q(x))`; using `q(u)²=1+2/(u+1/u)` gives `sign(x−Y)`. This proves the printed dichotomy and the two coincidence curves, including their intersection at (1,1). Direct candidate comparisons had maximum deficit error `1.78e−15` and zero nondegenerate sign mismatches in 1,500 independent tests.

   Differentiating D gives exactly the stated D′ and D″. The sufficient concavity inequality reduces to `(x−1)²(x²+x+1)≤x²+1`; the displayed estimate proves it on `[1/2,3/2]`, and the strict earlier inequality (or direct evaluation at 1) gives `D″<0`. The largest sampled D″ on a 2,001-point high-precision grid was `−0.02058027389`; the proof does not depend on this sampling.

   For the x-kink, subtracting its ridge value leaves `(Y−1/x)(cY−ψ(x))` below the ridge and `(Y−1/x)(cY−1+q(x))` above. The Y-kink has the symmetric formula, based at `ℓ(1/Y)`. N1/N1′ and coefficient nonnegativity make all four corrections nonnegative. N2 handles the zero-deficit candidate. On J, `ℓ″=2cY/u³−D″>0`, and exact Tan gives `ℓ′(T)=0`. This proves the minimum without a transverse Hessian or an approximation near the kink. “Affine across the ridge” without the qualification “on each side” would be false: the slopes generally change there.

   The normal-slope interval is also correct for T<1 under Tan: decreasing Y requires `cY<ψ(T)`, and increasing x requires `cX>1−q(T)`, equivalent to the printed lower endpoint for cY. At either endpoint there is an actual flat one-sided segment, so strict local minimality fails there; outside the closed interval there is a descending direction. These remarks do not replace the stronger uniform hypotheses used on the boxes.

10. **NOTE — The scalar equation and stationary multipliers check; they agree with independently minimized hull-chain widths.**

   Quote (Lemma 18): “μ_{2i+1} = k(i/(m − 1) − 1/2) … μ_{2i} = (k T²/2)(m − 2i)/(m − 1)”.

   Each successive tangency equation determines the next a with nonzero coefficient. The two-step recurrence is `μ_{p+2}=μ_p−2β`, where `β=k(1−T^−2)/2−D′`. Matching the final endpoint gives `β=−k/[2(m−1)]`, exactly `(2−H)(m−(m−1)/T²)=(n−2)D′(T)`. Substitution yields all the printed multipliers and the pair coefficients. The antisymmetry is correct; the central multiplier is zero also when m is odd (a harmless unstated additional case). In (b), make explicit that the closed form solves the *full* system when T satisfies the compatibility equation; for arbitrary T the first n−3 equations have the recurrence solution containing β, not necessarily the printed closed form.

   Independent 70-digit solutions and direct substitution gave maximum tangency residual `2.13e−72` across n=6,8,10 at H_lo, 1.87, 1.90, 1.99, and 2. Representative values:

   | n | H | T_n | F_n |
   |---|---:|---:|---:|
   | 6 | 1.87 | .890925497167584 | 5.956225297106004 |
   | 6 | 1.90 | .902823126950174 | 5.808611109888402 |
   | 6 | 1.99 | .981485294032906 | 5.363615071240595 |
   | 8 | 1.87 | .923393081789953 | 7.875390301927249 |
   | 8 | 1.90 | .932136812661801 | 7.667053634318344 |
   | 8 | 1.99 | .987543712373674 | 7.040500079982711 |
   | 10 | 1.87 | .940935092137247 | 9.793463370422488 |
   | 10 | 1.90 | .947840532578338 | 9.524740641319533 |
   | 10 | 1.99 | .990614526105992 | 8.717369850741646 |

   Evaluating the independent hull chain at `φ=atan(T_n)` and separately minimizing its uniform interior tilt gave width differences at most `2.67e−15` and `1.78e−15`, respectively. A 101-point scan of the whole `[0,π/2]` interval at each height found no smaller competing branch. These are numerical checks, not a proof of the construction's global geometric optimality.

   Lemma 6.3 itself proves the stated interval minimizer. There is also a direct noncircular extension to all T>0: below `sqrt((m−1)/m)` both terms in f′ are negative, and above 1 both are positive. Thus the unique stationary point is the global Morandi-family minimizer for H<2; at H=2 use the unique maximum of D. The text need not defer this fact to O2_n.

11. **MINOR — Lemma 19(d)'s box proof is sound once its scalar enclosures are certified, but its status and a numerical remark should be made precise.**

   Quotes: “What is proved here … every proof complete”; “using T_n(H*(n)) ≥ 0.887 … ≥ 0.919 … ≥ 0.936”; “every coefficient used below is in [0, 0.127]”.

   The last sentence is false for the pair's x coefficients: the end coefficient is k, reaching `.138902`, `.147951`, or `.153064` on the rational ranges. It may have intended only certain Y coefficients. Delete or qualify it; the actual local proof uses the safe `.154` cap instead.

   The quarter-radius proof has ample slack: J lies within `[.637,4/3]`, γ≤k, `ψ(.637)=.15658170168`, `ψ(.669)=.16884587798`, `ψ(.686)=.17538105187`, and `ψ(.75)=.2`. N2 has margin because `(cX+γ)/4≤.077<D(.887)`. The displayed rounded ψ values should be marked approximations rather than exact equalities. The γ nonnegativity follows from the exact scalar equation and the smallest cX, as claimed.

   The decimal enclosures for the true H* and its T are not proved by a decimal table. For the rational certificate ranges, §11(T) can supply precisely the missing rigorous scalar checks, so this is not an additional obstruction conditional on those obligations. For reference, the lower-T derivative tests at the respective H_lo are `−.00146533377012`, `−.00037780371555`, and `−.00193960761177`; at T=1 they are k>0. The sampled minimum N1/N1′/N2 slacks on 101 heights were, respectively, `(.06013,.10894,.11179)`, `(.05327,.08556,.10524)`, and `(.04876,.07274,.10132)` for n=6,8,10. None of these sampled figures substitutes for outward interval checks. Either include actual certified scalar brackets in the analytic proof or describe this part as conditional on T.

12. **NOTE — Equal block values and the five-variable block formula are exact; the latter tail notation needs clarification.**

   Quotes (Lemma 19): “B_j(T, 1/T, T) = 2(f_n(T; H) − n)/(n − 2) for every j and T”; (§11): “B_L … on the orthant B_L = …”.

   Since `β_j+α_j=km/(m−1)`, substitution proves the common block value for every positive T, not just at its stationary value. The forced odd split in 19(e) follows by differentiating the common-ridge curve at the interior minimizing point. Grouping the first four pairs sums two such blocks: x3 and both Y coordinates have total coefficient k on either sign, x1 has k, and the shared x5 has k/2 on either sign. This is exactly the printed five-variable formula, including its wrong-sign terms. Its value at r* is `(F_10−10)/2`; the reflected block completes Ψ−10. Locally the four stationary pair coefficients supply Lemma 17 without any new local theorem. Thus the five-variable block is specified sufficiently once finding 1 is repaired.

   I independently reproduced why the larger block is needed: for n=10 at H* the end triple has `B_1−rhs≈−.002598615852` at `(x1,Y2,x3)≈(0,.667459686,1.498217827)`. At H=1.848 this restricted minimum remains negative, approximately `−.001325213479`. These are failures of the smaller block obligation, not counterexamples to Ψ≥F. They support the stated decision to group four pairs near the lower endpoint; they do not certify the grouped block.

   The printed tail uses `k(x1+Y2+x3+Y4)^+`, whereas the direct application of Lemma 20 gives `k(x1^++Y2^++x3^++Y4^+)`. This is not a false tail implication: the printed expression is smaller, so proving its complement merely asks the program to check a larger set. That larger set is still bounded because the three potentially negative coordinates in the sum are bounded below by −c. Nevertheless, use the sum of positive parts consistently with Theorem 22, or explicitly retain the larger domain and add the `3c` allowance when converting its cutoff to individual coordinate bounds. Do not silently treat the two cutoffs as equal.

13. **NOTE — Lemmas 20–21 supply the correct sliver and origin bounds for triple blocks; H=2 must be separated before division by k.**

   Quotes: “g_p(x,Y) ≥ g_p(x^+,Y^+) − c̃_x x^- − c̃_Y Y^-”; “B_j(z) ≥ κ0 |z|_∞ − 4|z|²_∞”; “Θ_j(H)/k ≤ … uniformly in H ∈ [H*(n),2]”.

   The slope comparison costs at most one unit per wrong-sign displacement in A. Combining it with the exact linear terms leaves exactly the two tilde-coefficient penalties, proving 20(a). For the stated nonnegative reversed coefficients these penalties total at most `c(β̃+α̃+k)`, proving 20(b). Dividing the tangent bound proves 20(c) for H<2. At H=2 its printed ratios are 0/0; state H<2 for these ratios, use their explicit uniform bounds, and handle H=2 by Theorem 10 as the assembly already intends.

   I checked all four quadrants of 21(a). The two mixed-sign kink formulas give the stated bounds using `1/√(1+s²)≥1−s²/2`; when both x,Y are negative, the candidates `(1−uv)/R_u` and `(1−uv)/R_v` give the quadratic loss. Subtracting the pair linear part proves 21(b). In 21(c), the reversed split makes both `k−β̃−α̃` and `β+α−k` equal `k/(m−1)`, which is the needed positive linear growth in the two signs of Y. Also `c_l,c_r≥κ0` and `1−c̃≥κ0` on the stated heights. The quadratic loss is at most four times the squared infinity norm. The sphere value `κ0²/16` at radius `κ0/8` and the nonnegative ball at radius `κ0/4` follow exactly. Independent random pair-origin tests had minimum gap `.0001500`; no test was used to justify the lemma. The corrected five-variable origin bound is in finding 1.

14. **NOTE — The exact-parameter argument and endpoint interpolation are sufficient for zero loss, subject to explicit coverage and the corrections above.**

   Quotes (Lemma 17′): “At the true point (T_n(H), H) … (Tan) exactly”; (§10): “B_P(z; H) − U(H) is affine in H for fixed z”.

   This is the right separation of roles. Interval arithmetic encloses T and checks inequalities; it must not replace Tan by a small residual or choose independently rounded coefficients as the actual split. The closed forms and scalar equation prove Tan exactly at the same true parameter. Also each internal-coordinate split must still sum exactly to its prescribed block coefficient. With that convention Lemma 17′ proves the local bound against the true attained value, not an approximation.

   A fixed rational trial T̂ in `[1/2,3/2]` provides `U≥rhs` and is affine in H; the same T̂ must be used at both endpoints of a cell (with the appropriate factor 1/(m−1), or 1/2 for the five-variable block). Endpoint positivity on the *same enlarged cell domain* then interpolates pointwise, including sign-changing coordinates. For a cell touching 2 choose `T_lo<1<T_hi` for strict root bracketing and use the separate H=2 theorem wherever k is divided out.

   The implementation must verify that the fixed inward N_cell is nonempty and contains every `(T,1/T,…)` in the root bracket; all Lemma 16 inequalities must be checked uniformly there. It must cover the union “at least one coordinate outside N_cell” and the complement of N0, not require every coordinate to be outside. Use the largest c, a certified upper tail cutoff, and the smallest origin radius on each cell, with all spatial/H cell boundaries covered and no pending boxes. Then the tail, local-ridge, local-origin, and certified-complement regions exhaust D_P. The endpoint signs for T are affine in H, as claimed. These requirements are compatible with the stated strategy, but a float grid and the supplied logs do not constitute such a certificate.

15. **MINOR — Complete the general-n existence statement for H* rather than leaving it implicit.**

   Quote (§0): “H*(n) is the unique root of F_n(H) = n”.

   Strict decrease follows from the proved envelope derivative. Existence above √2 can also be proved without data: by the global T-minimization observation in finding 10 and `D≤d0`,

   `F_n(√2)−n ≥ 2(2−√2)√(m(m−1)) − 2(m−1)d0 > 0`,

   whereas `F_n(2)−n=−(n−2)d0<0`. This proves a unique H* in `(√2,2)` for every even n≥6 and supplies the lower-height fact used in Lemma 1. Add this argument. It does not certify the ten printed decimal digits; those require a numerical bracket with directed error control if they are used as proof inputs.

**Verdict.** **No, not literally as written.** The displayed five-variable origin obligation is false without its endpoint-domain restriction, and the listed certificate ranges do not establish the broader claim starting at exactly H*(n). The underlying zero-loss reduction is otherwise sound: after restricting C0 to `x1≥0` (or replacing it by the exact `κ0^L=k/2` proof above), using outward domain/tail bounds and rigorous parameter/coverage checks, certified §11 complement inequalities do imply `Ψ_n(r;H)≥F_n(H)` for all r on **n=6: [1.861098,2], n=8: [1.852049,2], n=10: [1.846936,2]**, with the specified change of block scheme at 1.86. No positive error budget is needed at r*. The complement certificates themselves remain unperformed here; coverage down to the exact H* is an additional obligation, not a consequence of these upward-rounded ranges.
