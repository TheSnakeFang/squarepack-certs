# Referee report: o1n, 2026-11-01

Scope: the SPEC-chain O1 claim for n=8 on [1.855,2) and n=10 on [1.850,2). I read both specifications in full, the reduction, the previous referee report, the current sources, certificates, summary and logs. All builds, scripts and new logs are in this scratch directory; the source repository was not modified. Findings below distinguish mathematical certification under the stated arithmetic premises from numerical diagnostics. No MAJOR or MINOR defect affecting this certificate was found.

1. **NOTE — The interval-in-H target has the correct quantifiers and rounding.** `src/kernel.c:132` constructs signed interval displacements separately: F→C uses `sub(H,add(a.h,b.h))`, C→F uses `sub(add(a.h,b.h),H)`. Thus a negative displacement is not replaced by its absolute value or by an incorrectly ordered pair of endpoints. Lines 133–135 enclose `cos(t−u)` and `sin(t−u)` through dot products, then form `(1+cos(t−u)+|sin(t−u)|)/2`; the fixed tilts are in [0,π/2], where cos(t−u) is nonnegative. Zero tilts receive exact sine, cosine and half-extent values at lines 130–131.

   The interval primitives at lines 12–15 round addition/subtraction endpoints outward, take all four products before outward padding, and divide by multiplying by `[dn(1/nx.u),up(1/nx.l)]`. Every retained denominator has `nx.l>0` (line 139). Consequently the upper endpoint remains valid even when the numerator interval straddles zero. Unary negation and absolute-value endpoint selection need no rounding; multiplication by one half is nevertheless padded. Transcendentals receive eight nextafter steps in both directions. The final `z=up(z+gap_upper(...))` (line 146) is upward rounded, beginning with the exact endpoint cost 1.

   For each retained facet j, let U_j bound its ratio T_j(H) above for all H in the slice. Choose j* minimizing U_j: for every H, κ(H)≤T_j*(H)≤U_j*=min_j U_j. This proves the direction of the minimum operation. Skipping a facet with uncertified positive denominator can only enlarge this upper bound; it does not require that the active facet be retained. Summing the bounds gives Φ_M(θ₀,H)≤F_n_ub throughout the slice, and F_n(H)≤Φ_M(θ₀,H) holds without monotonicity or a certified optimizer. No correction is needed.

   Independently, at 80 decimal digits I evaluated the exact fixed-tilt facet ratios at both H endpoints, took the maximum for each affine-in-H ratio, then the minimum over ratios per gap and summed. All 295 stored targets exceed this independent whole-slice bound. The excess ranges were 6.192332300706403e−14 to 6.782034313648952e−14 for n=8 and 8.35474620944973e−14 to 9.194605623858225e−14 for n=10 (`spots.py`, `spot-results.json`). This is a numerical cross-check of the interval proof, not a replacement for its arithmetic premises.

2. **NOTE — The n-parameterization, flag, backward pass and endpoint accounting are correct.** `src/kernel.c:157–171` initializes the left endpoint at position 0, makes exactly `chain−1` transitions, and adds the right endpoint at `chain−1`. `ff=f||(r==s)` excludes exactly the two alternating sequences: every other binary role sequence contains an equal consecutive pair. The certified D selects only final flag 1. There is no sixth-square constant left in the executable recurrence. The comment at line 175 still says “i=1,6”; changing that comment to “i=1,n” would improve clarity but has no executable effect.

   In the backward pass, `j=chain−2−p` visits the n−1 edges in reverse. W(j,r,f,c) means the suffix cost conditional on the prefix's existing flag f; it transitions to f∨[r=s] and accepts only final flag 1. Thus V_i+W_i is a valid lower bound for complete flagged paths through the state. V carries only the left endpoint cost, W only the right endpoint cost; no shared vertex cost must be subtracted in the binding test at line 178. Binding controls refinement, not removal of cells or states from the certified forward solve.

   My independent exhaustive enumeration of every role/cell path on a two-cell grid matched the C flagged and unrestricted values bit for bit: 4,096 paths for n=6, 65,536 for n=8, and 1,048,576 for n=10. Flagged D values were respectively 2.6398561312726936, 3.0330075016124054 and 3.426158871952117. The binding masks also matched at the tested threshold (both cells binding). Separately, the three saved n=6 grids reproduced D=5.965757725467423, 5.6649197271183045 and 5.47863817463249 exactly (`structural.py`, `structural.stdout`). No algorithmic fix is needed.

3. **NOTE — The three gap bounds are unchanged, and their hypotheses survive the lowered H range.** A direct source diff shows `kernel.c:1–124` is byte-identical to the current o1dp kernel, including interval primitives, support lower bound, plain ratio bound, correlated derivative bound and near-upright lemma. Changes begin with the target function and then replace the fixed chain length by a parameter.

   Independently differentiating N gives N′=(−sinδ+sign(sinδ)cosδ)/2−dy′n_y−dy n_y′. Lines 51–60 enclose this expression, including both generalized derivatives at δ=0 and the correct owner/role signs for dy′. The face/derivative argument at lines 73–78 also handles a negative affine lower numerator by falling back on N≥0. In the upper endpoint cell, the c=0 branch is interpreted at the physical π/2 endpoint; its enclosing binary64 TOP is not a new physical tilt. The lower-bound intervals cover the intersection with the physical tilt domain.

   For the lemma, N≥m(1−3W/4−W²/4), nx≤m and W≤1 yield the stated bound. H≤2 supplies the nonnegative 2−H term, and H>√2 supplies the displacement sign. Both hold even at the stored predecessor of 1.850. Lines 95–111 apply the lemma only to C→F sine normals near zero or F→C cosine normals near π/2, with upward-rounded penalties and downward-rounded subtraction. No extension of the lemma is being assumed. No correction is needed.

4. **NOTE — The geometric reduction is n-independent, with the stated endpoint limitation.** In `docs/strip-n6-reduction.md`, the key pairwise inequality is `|Y_j−Y_i|≤H−h_i−h_j≤H−1<1`. The Minkowski sum contains the unit disk, so the horizontal section contains an interior point at x=0. Sorting centers by x and applying the pair constraint to consecutive pairs then produces n−1 gaps. Concavity of κ in dy and minimization of the resulting concave function over the n-dimensional height box reduce to its vertices, giving the four correct role displacements. These arguments use only finiteness of n and √2<H<2, not n=6 or H≥1.87. The reflected-pattern identity is likewise independent of n.

   This validates the reduction to the SPEC chain for the requested ranges. It does not transfer the separate n=6 O2 theorem to n=8 or 10, and O1 alone does not prove global Morandi optimality. At H=2, two upright squares can have vertical separation 1 and horizontal advance 0 although closed-section κ=1; the packing reduction therefore still requires H<2. No correction is needed to the claim under review.

5. **NOTE — Fresh random and boundary tests found no unsound gap or chain bound.** With seed 934107, `independent.py` tested 12,000 boxes with 64 independent reference-hull samples each, including both same-corner regions, widths down to 1e−8, H near 2 and H near 1.850. There were zero violations in 768,000 samples; largest G−κ was −6.085252302057143e−10. Seed 841177 added 2,000 boxes/128,000 samples near H=1.855, alternating the two corner regions: zero violations, maximum −2.5809985260139e−9. Thus both lowered cutoffs were explicitly exercised.

   Fresh gate-4 checks used 6,000 chains per n, split between [H₀,H₀+0.001] and [1.999,2], with ordinary tilts and tilts near each endpoint. The same downward-rounded path costs and global DP bounds were compared with the independent vertex-sum hull reference. For n=8, maximum path-bound minus reference was −0.03331610059826495 and maximum global-DP minus reference was −0.12901388439728834. For n=10 the corresponding values were −0.0560960307003846 and −0.2015881685037222. Zero violations occurred (`random-results.json`).

   To avoid relying on the ill-conditioned binary64 hull at exact endpoint configurations, `highprec_gaps.py` additionally checked 2,000 saved-grid cell pairs at endpoints/midpoints, with H at slice ends including exactly 2, using independent 80-digit facet evaluation and the physical π/2 endpoint. Zero violations; maximum lower-bound minus reference was −8.8817841970012523e−16. Random tests do not prove the interval code, but they support the analytic audit. No fix is indicated.

6. **NOTE — Independent optimization checks passed on 20 randomly selected slices per n.** Seed 772619 selected the slices listed in `spot-results.json`. The search objective was independently implemented: at each tilt vector it minimizes over all non-alternating role patterns via a discrete recurrence, using independently computed point facet costs. Each slice received 12 random tilt starts plus three structured starts, bounded L-BFGS-B searches, and a Powell polish of the winning fixed pattern. Winning values were re-evaluated with the vertex-sum hull reference. The smallest observed best-found-nonalt minus D was 0.028721407568450097 for n=8 and 0.025612277279048357 for n=10. These are best-found values, not certified global minima.

   At both ends of each of those 40 slices, I separately minimized the equal-middle-tilt alternating chain using a 257-point scan followed by bounded local minimization around the best grid point. All 80 endpoint comparisons satisfied F_n_ub≥the independently minimized value. Per-slice slack against the larger endpoint minimum ranged from 1.3325331060798362e−8 to 1.5054245228185437e−7 for n=8, and 9.526459621156391e−9 to 1.2297867790778128e−7 for n=10. This check does not assume monotonicity. No fix is indicated.

7. **NOTE — Coverage, provenance and reported numbers agree.** Each source hash recorded in both certificates matches the current `src/kernel.c`, `src/driver.py` and `SPEC.md`. I compiled the copied source in scratch with `clang -O2 -std=c11 -D_DARWIN_C_SOURCE -shared -fPIC`; its entire disassembled text section (538 lines) and constant section match the supplied library. The gap code was inspected directly rather than accepted from the README.

   Independent metadata checks found 145/145 proved slices for n=8 and 150/150 for n=10, strictly increasing tilt partitions covering [0,π/2], positive-width contiguous H slices, and no unproved leaves. Domains are [1.8549999999999998,2] and [1.8499999999999999,2], respectively. Exact decimal comparisons confirm that each stored lower endpoint is below the requested decimal cutoff. All D, target and downward-rounded margin values agree with the corresponding run-log entries. Source hashes and log agreement are reproducibility checks, not substitutes for the bound argument.

   | n | slice | D | F_n_ub | downward-rounded margin |
   |---|---|---:|---:|---:|
   | 8 | first: [1.8549999999999998,1.8559999999999999] | 7.981932888148611 | 7.979514322795648 | 0.002418565352963142 |
   | 8 | smallest margin: [1.877,1.878] | 7.826915458698205 | 7.826790024226110 | 0.00012543447209534261 |
   | 8 | last: [1.999,2] | 7.102114555571072 | 6.977562236560565 | 0.12455231901050733 |
   | 10 | first: [1.8499999999999999,1.851] | 9.974387722720952 | 9.972560862216680 | 0.001826860504271721 |
   | 10 | smallest margin: [1.865,1.866] | 9.838511383991513 | 9.838241027141821 | 0.00027035684969156643 |
   | 10 | last: [1.999,2] | 8.746002000369241 | 8.636416613983820 | 0.10958538638542058 |

   Additional exhaustive checks on asymmetric three-cell grids reproduced backward binding masks [0,0,0], [1,0,1] and [1,1,1] as the threshold varied, for n=6 and n=8 (`binding.py`). The n=6 point-target regression differed from the old targets by only 2.3092638912203256e−14, 2.5757174171303632e−14 and 2.4868995751603507e−14. No provenance or coverage repair is needed.

   I ran the supplied parallel verification mode against the scratch copies using the freshly compiled kernel. Every saved D, F_n_ub and downward-rounded margin matched exactly, and both commands exited successfully. Final output:

   ```text
   replay PASS n=8 proved=145 unproved=0 coverage=[1.8549999999999998,2] workers=6 seconds=89.989
   replay PASS n=10 proved=150 unproved=0 coverage=[1.8499999999999999,2] workers=6 seconds=124.996
   ```

   Full per-slice readback is in `replay8.stdout`, `replay10.stdout` and `audit/verify-n8.log`, `audit/verify-n10.log`.

8. **NOTE — The small margins are numerically real under the stated premises; errors beyond the libm premise are not covered.** The smallest margins are 1.2543447209534261e−4 and 2.7035684969156643e−4, in the interior slices identified above. The first-slice margins are larger, about 2.42e−3 and 1.83e−3. They are not one-ulp comparisons or decimal-printing artifacts: the replay compares stored binary64 values, uses downward-rounded subtraction, and reproduces them exactly.

   As a sensitivity check, I rebuilt the kernel changing only the transcendental padding loop from 8 to 64 nextafter steps and reran the first and smallest-margin grids for each n. All four still proved. The resulting margins were:

   | n | slice | margin with 64-step padding |
   |---|---|---:|
   | 8 | first | 0.0024185653524613215 |
   | 8 | [1.877,1.878] | 0.0001254344715952982 |
   | 10 | first | 0.0018268605036126928 |
   | 10 | [1.865,1.866] | 0.0002703568490360908 |

   Widening the padding reduced these margins by only about 5.0e−13 to 6.6e−13 (`sensitivity.py`, `sensitivity-results.json`). This is strong numerical evidence that the narrow margins are not rounding artifacts. It is not a verification of every libm call, nor a replacement for the mathematical interval audit.

   The unchanged eight-step computation is **not guaranteed sound if sin/cos errors exceed its stated eight-ulp enclosure assumption**. An oversized error can put a true transcendental value outside a cell/target interval; a large observed final margin does not repair an invalid enclosure. To remove that condition, use independently certified transcendental enclosures or a proved library error bound and sufficient padding, then replay. A 64-step implementation could accommodate a correspondingly justified wider error bound, but the four sensitivity runs alone do not certify the other slices under that new premise. The present report does not claim an unconditional libm guarantee.

**Verdict:** Yes. Under the stated IEEE-754, compiler/no-reassociation, functioning-nextafter and eight-ulp transcendental-enclosure premises, o1n certifies the SPEC-chain claim for n=8 on [1.855,2) and n=10 on [1.850,2): every non-alternating role pattern and every tilt vector in the closed physical tilt cube has Φ strictly greater than F_n(H). Both complete certificates replayed exactly; their H coverage has no gaps; the target bounds apply throughout each slice; and the gap bounds and n-dependent DP implement the required inequalities. The geometric reduction is n-independent on these ranges, but this O1 result does not supply an n=8 or n=10 O2 theorem, unrestricted Morandi optimality, a physical packing statement at H=2, or a proof of the libm accuracy premise.
