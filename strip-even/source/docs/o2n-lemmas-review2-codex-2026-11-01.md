# Second referee report: o2n/LEMMAS.md

2026-11-01. Reviewed the revised document, the first-pass report and §14 responses, the accepted n=6 analytic reduction and its referee report, and the supplied numerical scripts. Source files were read only. New computations are in `audit.py`, `audit.json`, `audit_extra.py`, and `audit_extra.json` in this directory. Numerical tests below are diagnostics, not interval certificates.

1. **NOTE — The revised Lemma 16 is valid, including negative c_Y.**

   Quotes: “c_x ≥ 0 and c_Y ∈ R (not necessarily ≥ 0)”; “(N3) c_Y ≥ 1 − min(q(x_−), q(x_+))”; “(L) ℓ''(u) = 2c_Y/u³ − D''(u) > 0 for every u ∈ J.”

   I re-derived all three candidate comparisons. Write `L0=c_x x+c_Y Y`. The zero-deficit candidate is bounded below by `c_x x_−+min(c_Y Y_−,c_Y Y_+)`; this is precisely what N2' must bound, and it works for either sign of c_Y. For the x-kink, subtracting its ridge value gives

   `L0−dX−ℓ(x)=(Y−1/x)(c_Y−ψ(x))` below the ridge, and `(Y−1/x)(c_Y−1+q(x))` above it.

   The first product is nonnegative by N1. Differentiation gives `q'(x)=(1−x)/(1+x²)^(3/2)`, so q increases to 1 and decreases thereafter; its minimum on any positive interval is at an endpoint. N3 therefore makes the second product nonnegative throughout the entire x interval, including intervals crossing 1. For the y-kink, the analogous two products, based at `ℓ(1/Y)`, have coefficients `c_x−ψ(Y)` and `c_x−1+q(Y)`. N1' handles the first and `c_x≥0`, `q(Y)≥1` handle the second. Finally J contains x, 1/Y and T; L and exact Tan give `ℓ(u)≥ℓ(T)` throughout J. Taking the minimum of these three candidate lower bounds proves the assertion. No derivative of a selected active branch, nor any unproved smoothness across a switching curve, is needed.

   For c_Y≥0, L follows from D''<0 and N3 from q≥1; N2' reduces exactly to N2. For negative c_Y neither automatic inference is made in the revised proof. At `T=.9999, H=2, c_x=0`, I obtain `c_Y=−0.0000121314276658536921`. On the quarter-radius box, the sampled N1/N1'/N2'/N3 margins are `.199974, .200038, .171570, .399975`; the minimum sampled ℓ'' is `.0405163`. A 202×202 candidate grid, including the exact center, has minimum `g−g(T,1/T)=0` to floating precision. These numbers illustrate the repair; the proof is the preceding algebra.

2. **MINOR — The normal-slope remark needs the curvature hypothesis; Tan alone is insufficient.**

   Quote: “For T < 1, given (Tan), (T, 1/T) is a strict local minimiser of g iff c_Y lies in the open interval I(T)”.

   The displayed interval correctly expresses the two strict transverse inequalities, but does not by itself ensure a minimum along the ridge. Even retaining c_x≥0, take `T=1/2`, `c_x=0`, `c_Y=−T²D'(T)=−.03262379212492639`. Tan holds and

   `I(T)=(−.11803398874989485, .10557280900008412)`,

   so c_Y is strictly inside I(T). Nevertheless `ℓ''(T)=−.06452035960037013` and `ℓ(.501)−ℓ(.5)=−3.19104283217e−8`; the ridge supplies a descending direction. This counterexample violates L, as it should. Fix the remark to say “under (Tan) and (L) on a neighbourhood of T”, retaining the coefficient assumptions. With ridge strict convexity, the transverse conditions give the stated sufficiency; at an interval endpoint the corresponding affine transverse segment is flat, and outside its closure there is a descent direction. This does not affect Lemma 16 or the theorem, which explicitly require L.

3. **MINOR — The fixed-box containment claim is not implied by the stated bracket-width condition.**

   Quote (§10, step 2): “It is nonempty and contains (T, 1/T) for every T ∈ [T_lo, T_hi], because T_hi − T_lo ≤ 1/4.”

   The x-factor assertion follows before rounding, but the Y-factor additionally requires `1/T_lo−1/T_hi≤1/4`. Example: `T_lo=.76`, `T_hi=1.01`, difference exactly .25, gives `I_x=[.76,1.01]` and `I_Y=[1.0657894736842105,1.2400990099009901]`. This excludes `(T,1/T)=(1,1)`, including the true H=2 point. The derivative bracket signs themselves are valid for these endpoints on the relevant H ranges. Inward rounding also requires checking the final stored endpoints, rather than relying on non-strict symbolic equalities.

   Fix step 2 by requiring a directed check of

   `x_−≤T_lo≤T_hi≤x_+` and `Y_−≤1/T_hi≤1/T_lo≤Y_+`

   after rounding, and reject/subdivide the cell if it fails. This supplies the exact hypothesis already present in Lemma 17'. The actual fine brackets used by `rect_check.py` have comfortable containment margins, `.23979` or larger, so this is a specification defect rather than a failure of those sampled brackets. A complete strict C certificate would also fail if the true minimizer were left in its complement; it must not be used as a substitute for this simple local precondition.

4. **NOTE — The exact interval-parameter argument preserves zero loss.**

   Quotes: “(Tan) is never checked: it holds exactly at the true (T_n(H), H)”; “Internal coordinates are split by the pair coefficients … which sum to the block coefficient exactly at the true point”.

   This is correct. Over a parameter rectangle define `γ=T²(c_x−D'(T))`. Tan is then an identity, and at the actual root the two γ values around an internal even coordinate sum to k by T-eq. Away from the root they need not sum to k; the proof never sums them there to represent the block. Interval checks of the individual inequalities over the larger rectangle are conservative. The actual block remains the exact H-dependent function of §8/§11. No interval midpoint, residual tolerance, rounded multiplier or approximate value at r* may replace these identities.

   The L implementation condition is also correctly oriented: `c_Y>sup_{u∈J} u³D''(u)/2` is equivalent to the required strict curvature bound for positive u. Enclose that supremum from above and c_Y from below. I reran the supplied rectangle diagnostic with bytecode writes disabled: 28/30/31 cells for n=6/8/10, minimum sampled L margins `.047999, .048003, .048003`, and minimum sampled c_Y `−.00099077, −.00053679, −.00043174`. It remains a finite sampling diagnostic, not a verification of all real parameters. This correctly repairs the implementer's negative-γ issue and strengthens first-pass finding 14.

5. **NOTE — Lemma 21' fixes the first-pass MAJOR origin defect exactly.**

   Quotes: “z … ∈ D_L (so x_1 ≥ 0)”; “B1_L = (k/2)x_1 + Σ_i [(k/2)s_i⁺ + (1 − k/2)s_i⁻]”.

   Summing the four pair lower bounds yields exactly the stated B1_L: the internal coordinates have coefficient k on both signs, x1 has k, and x5 has k/2 on both signs. Each internal coordinate occurs in two quadratic remainders and each outer coordinate in one, so the total remainder is at most `8||z||∞²`. Since `0<k≤1`, each hinge term is at least `(k/2)|s_i|`. Since x1≥0, successively solving the four edge-sum equations gives `||z||∞≤x1+Σ|s_i|`. Hence the claimed lower bound, nonnegative ball of radius k/16, and sphere margin k²/128 follow exactly.

   The direction `(0,1,−1,1,−1)` has norm 1 and B1_L=k/2, proving sharpness. It is a direction in the endpoint-restricted tangent cone; sufficiently small positive multiples lie in D_L whenever k>0. Independent linear programs on every feasible signed cube face returned minima `.07,.075,.076532` for k `.14,.15,.153064`. Without x1≥0 they returned the corresponding negatives. The old unrestricted C0 obligation has correctly been removed. First-pass finding 1 is resolved.

6. **NOTE — General-n separation, deficit cap and H=2 equality are exact.**

   Quotes: “w_n = (1 + r_{n−1}) h(t_n) + G(r_{n−1}, t_n)”; “An interior coordinate lies in two pairs and an end coordinate in one”; “min_{F_n} Ψ_n(·; 2) = n − (n − 2)d0”.

   Substitution of `−r_i dy_i` gives `−Hs_i r_i+s_i r_i(h_i+h_{i+1})`. Because n is even, the two end coefficients are both 1+r; the interior signs and `Hσ=−HΣρ` are correct. There are n−2 pairs, m odd coordinates and m−1 even coordinates. Adding the endpoints to the pair E values gives exactly `n+kΣρ−Σd`, including on the orthant boundary. The support slices are feasible, and H*>√2 guarantees the prescribed displacement sign. Joint infima commute without an attainment or minimax assumption. Lemmas 3–4 are n-independent and the finite candidate formula remains valid on all clipped slivers, including zero coordinates.

   Direct kink evaluation gives the two printed dX branches. For fixed positive x the first increases in Y, the second decreases, and their common apex is `D(x)=1/(1+w+√(w(w+2)))`. Thus the upper cap d0 is attained only when x=Y=1; axes have d=0. Summing caps gives the H=2 lower bound, while all ρ=1 simultaneously attain it. Clipping at H=2 proves the same value globally. The revised x>0 and “upper bound” qualifications resolve first-pass finding 5. First-pass finding 4 remains accepted.

7. **NOTE — The tangent-chain computation and the Morandi stationarity calculation agree independently.**

   Quotes: “4 + (2n − 4)√2 − (n − 1)H”; “(2 − H)(m − (m − 1)/T²) = (n − 2)D'(T)”.

   I executed only the stipulated first 29 lines of `m4check.py`, dropping the specified import/path lines. At uniform π/4 interior tilts, the two end gaps each give `3/2+√2−H`, the n−3 middle gaps each give `2√2−H`, and the exterior half-widths sum to 1. This proves the formula on the stated range. At H=2 the values are `5.3137084989847604`, `6.9705627484771406`, `8.6274169979695208`.

   The multiplier recurrence gives `μ_{p+2}=μ_p−2β`; matching the last endpoint yields `β=−k/[2(m−1)]`, exactly T-eq. Substitution produces both closed forms in Lemma 18 and all its pair coefficients; the central multiplier is zero for either parity of m. The revised qualification restricting the closed form to compatible T is correct.

   At 75-digit precision I solved independently for n=6,8,10 at their respective H_lo and at 1.87,1.90,1.99,2. The largest pair tangency residual was `2.81e−77`. At H=1.90, respectively:

   | n | T_n | F_n |
   |---|---:|---:|
   | 6 | .902823126950174 | 5.808611109888402 |
   | 8 | .932136812661801 | 7.667053634318344 |
   | 10 | .947840532578338 | 9.524740641319533 |

   The independent hull-chain evaluation at `φ=atan(T_n)` differed from f_n by at most `2.67e−15`; separately minimizing the hull-chain function over φ gave the same maximum width discrepancy. The π/4 formula discrepancy was at most `4.45e−15`. These numerical minimizations support, but do not replace, the analytic minimization statement. First-pass findings 6 and 10 are resolved/confirmed.

8. **NOTE — Lemma 6.3(d),(e) supplies the formerly missing global minimization and existence arguments.**

   Quotes: “if T < √((m − 1)/m) … both terms … are negative”; “F_n(√2) − n ≥ … > 0”.

   These signs are correct for H<2. Above 1 both terms in f' are positive. Between √((m−1)/m) and 1, strict convexity yields the unique zero. At H=2 the unique maximum of D gives the unique minimizer T=1. The D'' formula is correct; its displayed sufficient concavity inequality reduces to `(x−1)²(x²+x+1)≤x²+1`, and the subsequent estimate proves it on [1/2,3/2]. Strictness follows from the preceding strict bound on P, with x=1 handled directly. My independent 2,001-point check gave maximum D'' `−.0205802738900`.

   Thus the envelope derivative is `−(mT+(m−1)/T)<0`. The arithmetic-geometric-mean lower bound at √2 and the negative value at 2 prove a unique H* for every even n≥6, without relying on the decimal table or O2. First-pass findings 10(iii) and 15 are resolved.

9. **NOTE — Clipping and the box reduction retain all boundaries and wrong-sign coordinates.**

   Quotes: “c(H) := √(4/H² − 1)”; “There are n − 3 interior coordinates”; “R_n(H) := (n − 1) + (n − 3)c(H)”.

   The odd interior upper derivative bound is `2/√(1+r²)−H`; the even lower bound is its negative. These give the precise threshold c, with non-strict monotonicity sufficient at equality. The end derivative is at most `1+2/(3√3)−H`, which at 1.8469 is `−.4619998205402495`. There are m−2 odd and m−1 even interior coordinates. After clipping, either Σρ≥n−1 and Corollary 10.1 applies, or every positive coordinate is less than `(n−1)+(n−3)c`. No equality boundary or orthant face is dropped. In 3,000 fresh random tests the largest increase under clipping was zero. First-pass finding 7 remains accepted.

10. **NOTE — Telescoping, the block converse and the equal even-star values remain exact.**

   Quotes: “For every two admissible splits”; “B_j(T, 1/T, T) = 2(f_n(T; H) − n)/(n − 2) for every j and T”.

   Each coordinate's coefficients sum to k independently for each sign. Summing linear terms gives `−Σ(N_j−k)ρ_j`; the only N_j=1 terms are the two nonnegative endpoints, which supply exactly m1−1=ρ. Thus Σg=Ψ−n on the entire clipped domain, for arbitrary admissible real splits. The converse follows termwise from `inf B_P≤B_P(z*)`: equality in the finite sum forces equality in every term. It is a conditional necessity, not a proof that the blocks are tight.

   For the even-star scheme, `β_j+α_j=km/(m−1)` gives the common value directly. Restricting a block to its common-ridge curve and differentiating proves the forced odd split in 19(e). Combining the first two stars gives precisely B_L, with x3,Y2,Y4 internal and x5 split k/2 on both signs. The reflected block supplies the other half. There are no omitted end terms. Fresh random independent splits and mixed signs gave maximum telescoping residual `1.60e−14`; independent deficit evaluation gave error at most `1.78e−15` and no ridge-sign mismatch in 3,000 tests. First-pass findings 8 and 12 are resolved/confirmed.

11. **NOTE — The revised tail caps and origin handling cover the required slivers.**

   Quotes: “g_p(x, Y) ≥ g_p(x⁺, Y⁺) − c̃_x x⁻ − c̃_Y Y⁻”; “with positive parts”; “For H < 2”.

   The slope bounds cost at most x⁻+Y⁻ in A. Combining them with the signed linear terms leaves exactly the two tilde penalties. The chosen nonnegative reversed coefficients justify replacing each negative part by c. For triples the resulting threshold divided by k is at most `2(n−1)/(n−2)+c(2m−3)/(m−1)`. I obtain `3.090244132498368` for n=6 at H_lo, `3.012695145308703` for n=8 at H_lo, and `2.9416442561635685` for n=10 at 1.86. Multiplying by the appropriate coefficient ratios gives bounds strictly below every printed coordinate cap, including 6.181 for n=6 and 11.767 for n=10. The c caps `.3935,.4077,.3953,.4155` are all outward.

   For L the four wrong-sign penalties total `(7/2)kc`, and the sum of positive parts yields `Θ_L/k≤4.5+3.5c=5.954153348377832` at H_lo. The caps 5.955 and 11.909 therefore suffice. The revised positive-parts notation repairs the prior ambiguity. Division by k is explicitly restricted to H<2; the endpoint uses Theorem 10.

   Lemma 21's quadrant formulas and linear estimate are valid on the stated height range. Its coefficients obey `c_l,c_r≥k/(m−1)` and `1−c̃≥k/(m−1)` there; the reversed split is essential to the positive Y-direction estimate. The four square remainders give the claimed ball and sphere margins. Fresh pair-origin tests had minimum margin `4.56e−6`. First-pass findings 3, 12's tail issue, and 13 are resolved.

12. **NOTE — The certified assembly is sufficient on the rational ranges, with explicit implementation preconditions.**

   Quotes: “Check B_P(z; H_e) > U(H_e) … on a cover of (caps ∩ D_P(H_a)) minus N_cell minus N_0”; “Use the same T̂ at both endpoints.”

   Use a positive rational trial T̂ (preferably within [1/2,3/2]) so Lemma 6.3 supplies U≥rhs. Each fixed block and U are affine in H; endpoint inequalities therefore interpolate pointwise on the same enlarged spatial domain. Minimized envelopes need not be affine, and the proof does not assume that. Use c(H_a) rounded up, exact outward caps, and the minimum origin radius on the cell rounded down. Intersect the endpoint-coordinate restrictions with every domain. Exclusion of a product neighbourhood is a union of coordinate-outside pieces; if using the separable minimizations, retain those restrictions on the appropriate inner or outer variable. Verify that all pieces and all H-cells cover their closed boundaries with no unresolved boxes. At H_b=2 the origin radius is zero and no origin neighbourhood is excluded.

   With the containment check in finding 3, the four pieces exhaust D_P: tail, local ridge box, origin box, certified complement. Their lower bounds sum to exactly F_n, because ΣB_P(z*)=F_n−n; there is no numerical equality tolerance. The switch of scheme at 1.86 is covered by the two closed ranges. The low-H five-variable obligation includes its wrong-sign slivers and both chain ends by reflection. This completes the logical implication conditional on genuine outward certificates. The supplied grids and logs do not yet provide those certificates. First-pass finding 14 is otherwise resolved.

13. **MINOR — The sentence about minimizers at H* states a conditional necessity as an unconditional fact.**

   Quote (§10): “At H*(n) itself both z* and 0 are minimisers of every block (Lemma 14(c))”.

   Lemma 14(c) says this only if equality in the sum of block infima is achieved. It does not establish block tightness at H*. The document itself correctly reports that the n=10 even-star end block fails there. Replace the sentence by “Any scheme achieving equality in Lemma 14(c) at H* must have both z* and 0 as minimizers of every block.” This is outside the rational-range theorem, but matters when describing the remaining root-boundary problem.

14. **NOTE — The revised range claim and H* data are correct; the exact-root interval remains open.**

   Quotes: “This document reduces O2_n on the smaller range [H_lo(n), 2]”; “the sliver [H*(n), H_lo(n)) … is not covered.”

   Independent 75-digit calculations give:

   | n | H*, approximately | T_n(H*) | F_n(H_lo)−n |
   |---|---:|---:|---:|
   | 6 | 1.8610971451879037034 | .887997081883048750 | −4.202470790613e−6 |
   | 8 | 1.8520484460607287756 | .919182637645472960 | −3.844615399649e−6 |
   | 10 | 1.8469355214063834396 | .936728261385061855 | −4.285242604809e−6 |

   Thus 1.861098 and 1.852049 are correct upward rational starts, not the actual roots. H0's trial upper bound below n proves the necessary strict negativity throughout the certified range without using these decimal approximations. Nothing in C or the origin lemmas fills the omitted interval or proves the complement at exactly H*. First-pass finding 2 is resolved by narrowing the theorem, not by proving the formerly asserted larger range.

15. **NOTE — The first-pass dispositions are substantially correct, with the three qualifications above.**

   Quote (§14): “Disposition”.

   All 15 first-pass findings were addressed: 1 by the exact endpoint-restricted origin proof; 2 by the explicit rational-range theorem; 3 by outward c and tail caps; 4–9 by retained correct arguments and notation/affinity repairs; 10 by the compatible-T qualification, central multiplier parity and global minimizer proof; 11 by separate coefficient ranges and conditional H0 checks; 12 by positive-parts tail notation; 13 by excluding H=2 before division; 14 by explicit cell mechanics; 15 by the analytic existence proof. The residual issues are the normal-slope remark, automatic-containment sentence, and unconditional H* minimizer sentence in findings 2, 3 and 13 of this report. None is a counterexample to the zero-loss theorem under its full local hypotheses. The section heading “Numerical sanity checks (not proofs)” correctly labels the supplied evidence; in particular neither the sampled positive margins nor the five-variable grid establishes C.

**Verdict. Yes, conditional on genuine §11 certificates and enforcement of Lemma 17's stated containment hypothesis, the revised reduction proves Ψ_n(r;H)≥F_n(H) for all r on n=6: [1.861098,2], n=8: [1.852049,2], and n=10: [1.846936,2], using five-variable blocks below 1.86.** The revised negative-c_Y lemma and five-variable origin proof are sound and introduce no loss at r*. Make the three minor corrections above, particularly the explicit post-rounding containment check. What remains is the outward-rounded, exhaustive parameter/domain computation, with coverage and strict complement inequalities verified; it has not been performed by this report or by the supplied grid diagnostics. The interval down to each exact H*, including H* itself, remains outside this theorem.
