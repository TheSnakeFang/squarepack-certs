# Codex (gpt-6.1-sol) blind referee report on the O1 certificate, 2026-10-30

Packet: PACKET.md (scratch copy of o1dp at squarepack abb610a plus runs/openmath-2026-10-27/{proof-F6.md,m4check.py,CHECK-2026-10-28.md}). Run time 27 min. Verdict: certified under premises, 0 MAJOR, 5 MINOR.

---

1. **NOTE — The near-upright pair lemma is correct.** SPEC.md:47–51 gives
   `N = 1/2 + (|sin δ| + cos δ)/2 + dy·cos t` and
   `N ≥ m(1 − 3W/4 − W²/4)`.
   Here the normal really is −v_owner, its y-component is negative, and C→F gives `dy=h(t)+h(t1)−H<0`. Thus `dy cos t ≥ dy`. The stated sine and cosine inequalities hold on [0,1]; each of the three squared terms is at most m² and each of the three cubed terms at most m³. The coefficient `1−3W/4−W²/4` is nonnegative for W≤1, justifying division using `sin t≤m`. The reflected proof at SPEC.md:53 correctly uses **F→C and u_owner**, positive dy, and `−dy cos s≥−dy`. H≤2 supplies `2−H≥0`; the lower height bound supplies the sign of dy. No mathematical correction is needed.

2. **NOTE — The kernel's gap bounds are sound on the physical tilt domain, conditional on its arithmetic assumptions.** kernel.c:81–85 says: “ineligible normals included by the box only decrease the minimum.” This is the correct direction: only u and −v can have positive x-component on [0,π/2]; normals that vanish at a particular point may remain in the box minimum without invalidating a lower bound. The vertical segment in SPEC.md:16 proves every relevant numerator nonnegative, so kernel.c:38–39 may clip its lower bound to zero. The support bound in kernel.c:30–34 uses the concavity of `cos x+sin x` between its difference endpoints, with outward subtraction and padded trigonometry.

   For the correlated bound, independent differentiation gives
   `N' = (−sin δ + sign(sin δ)cos δ)/2 − dy' n_y − dy n_y'`.
   kernel.c:51–60 encloses precisely this expression. Its owner-dependent coefficients for dy' are `(2r−1)h'` for the first square and `(1−2s)h'` for the second. The interval sign [−1,1] includes both generalized derivatives at δ=0. kernel.c:73–78 correctly handles a negative affine numerator bound using N≥0. The endpoint branch with c=0 returns B alone, so its face-value calculation does not affect that branch. At the upper endpoint the argument is applied from the physical π/2, rather than treating the enclosing binary64 TOP as a real tilt. The last cell's intervals enclose its intersection with the physical domain.

   The lemma tests at kernel.c:95–111 select exactly the two proved role/normal/corner combinations. The upper threshold and width are enclosed upward; positive penalties are rounded upward and subtractions downward. No unsupported role symmetry or absolute-value displacement substitution was found. No correction is needed to these bounds.

3. **NOTE — Arithmetic certification is explicitly conditional.** README.md, “Bound and arithmetic assumptions,” states: “System libm sin/cos/sqrt errors are assumed at most eight ulps” and calls this “an unverified libm accuracy assumption.” kernel.c:7–25 pads those evaluations and rounds interval arithmetic outward with nextafter; the target and DP likewise round in the required directions. This audit does **not** establish a worst-case error theorem for the system libm. Random gates cannot establish it. For an unconditional arithmetic certificate, replace the assumption with a proved library guarantee or independently certified transcendental enclosures. Under the stated assumption, I found no arithmetic gap in the operations used here.

4. **NOTE — The DP and target have the correct quantifiers and rounding direction.** SPEC.md:63–64 gives
   `f' = f ∨ [r=r']` and `D = min V_6(r,c,1)+h_lb(c)`.
   kernel.c:134–149 implements these statements with downward-rounded additions. Exactly the two alternating binary role sequences never set the flag; the other 62 do. The shared cell at a vertex preserves the actual tilt's membership, while independently minimizing edges only relaxes the objective. The backward pass is for refinement and does not enter the certified forward value. Exhaustive enumeration of all 64 role sequences and all 3^6 cell sequences on an independent three-cell grid reproduced both flagged and unrestricted C results exactly.

   kernel.c:125 evaluates
   `2 + (4−(3Ha−2)cos θ0)/sin θ0 + (4−2Ha sin θ0)/cos θ0`
   with outward interval arithmetic. All saved trial angles have positive sine and cosine. A globally optimal numerical angle is unnecessary: `F6(H)≤F6(Ha)≤L(θ0,Ha)≤F6_ub`. Independent 90-decimal evaluation at each saved binary64 trial angle and height confirmed all 76 upper bounds. Together with `D>F6_ub`, this proves the required strict inequality on each slice.

5. **NOTE — Coverage and the printed table check out.** certificate.json starts at binary64 `1.8699999999999999`, below the exact decimal 1.87, and ends at 2. All 76 slices have positive width and share identical adjacent boundaries. Each saved tilt partition strictly increases from 0 to `nextafter(pi/2,+∞)`, enclosing [0,π/2]. All 76 stored proof flags are true, all D exceed their targets, and each stored margin equals the downward-rounded difference. Every README table row agrees with certificate.json at the displayed precision. The minimum margin is `0.009532428361397114`; the last slice has `D=5.47863817463249`, `F6_ub=5.313713381796298`, and margin `0.1649247928361923`. No coverage or table correction is needed.

6. **MINOR — The recorded SPEC hash is stale, and verify does not enforce all certificate invariants.** certificate.json:20 records
   `e0171e70a3e87fcd918603ceddaab3df1e62d028cde7ab5ae6bc830d3f8f3360`
   for SPEC.md; the supplied file hashes to
   `a7ecd0983ba4933995b637117fd104b9ac680f873d7af66fb58b448a70c7d9a2`.
   The kernel.c, driver.py, and replay_lemma.py hashes match, as do both preserved-backup hashes. The actual supplied SPEC was reviewed directly, so this discrepancy does not invalidate the reviewed mathematical bounds, but the bundled hash-verification claim is not current. Record the document revision and refresh its hash.

   driver.py:262 says `if 'edges' not in r:continue`, and :266 only checks `r['proved']==(d>ub)`. Consequently a successful invocation is not, by itself, a check that every slice has a grid and proves. It also does not check source hashes, positive slice widths, stored margins, or the README. Strengthen verify to enforce those conditions explicitly. The independent audit checked them for this actual packet; all passed except the SPEC hash.

7. **MINOR — The supplied gates are not self-contained at their reference path.** driver.py:23 reads
   `ROOT/'../runs/openmath-2026-10-27/m4check.py'`.
   That path is absent from this packet; the reference is supplied at `context/m4check.py`. Thus the documented `src/driver.py gates` command cannot run unmodified here, although verify does not use that reference. Point ref() at the packaged context file, retaining its AST extraction of only verts, kappa, and h. My independent diagnostic used those supplied function definitions without executing their unrelated top-level imports/search.

8. **MINOR — The report generator drops the H=2 qualification, and the qualification needs one wording correction.** report.py:122 performs
   `(root/'README.md').write_text(text)`
   but its template contains none of README.md:192–208 (“Scope at H = 2”). Running the advertised report command would erase that addition. Include the scope note in the generator. I compared all table rows directly and did not run this destructive regeneration.

   README.md:196 says “no bound of the form ‘non-Morandi > F6’ can hold there.” This should refer to a **packing lower bound**: the stated inequality for the closed-section chain can hold at H=2 and is precisely what the last slice bounds. The physical packing interpretation fails there. For H in the requested range with H<2, cross-role displacements satisfy `|dy|≤H−1<1`, and same-role displacements satisfy `|dy|≤(sqrt(2)−1)/2<1`. Because each square's central vertical radius is at least 1/2, `(0,dy)` lies strictly inside the Minkowski sum. Its horizontal section therefore has an interior interval containing zero; on the right-separated branch, non-overlap requires advance at least its right endpoint κ. At H=2, upright squares instead give a boundary section with closed κ=1 but permitted packing advance 0. This establishes the requested scope distinction without assuming continuity across the degenerate endpoint.

9. **MINOR — The contextual FI-O1 formula is not the chain being certified.** context/proof-F6.md:215–216 writes the displacement as
   `(σ_{i+1}−σ_i)(H−h_i−h_{i+1})`.
   It incorrectly sets dy=0 for same-role pairs with unequal tilts. SPEC.md:17–19 and kernel.c:118–120 correctly use the four actual role displacements. Replace the contextual formula by
   `dy=(σ_{i+1}−σ_i)H+(1−2σ_{i+1})h_{i+1}−(1−2σ_i)h_i`.
   The present result is for the packet's explicitly designated **SPEC chain**. It must not be silently identified with that erroneous printed contextual formula. Also correct SPEC.md:55 (“H≥1.87, both true on every slice”): the first slice begins slightly below 1.87. This is harmless because the lemma's proof only needs H>sqrt(2) and H≤2, which also hold on the enlarged first slice.

10. **MINOR — One diagnostic assertion presupposes the unresolved alternating-pattern result.** SPEC.md:22 says the unconstrained minimum “must equal F6(H),” repeated in gate 3 at :77. Equality for unrestricted alternating tilts is part of O2, explicitly left open in context/proof-F6.md. The known construction proves only that the unrestricted minimum is **at most** F6, which suffices for a useful one-sided sanity check. Label equality/convergence as an expectation rather than an established premise. The flagged DP certificate uses neither O2 nor this equality; gate 3's historical status is correctly disclosed in README.md.

11. **NOTE — Independent executions and their limits.** From the packet root I compiled the supplied source to a scratch artifact with
   `clang -O2 -std=c11 -D_DARWIN_C_SOURCE -shared -fPIC o1dp/src/kernel.c -o audit-kernel.dylib`.
   Compilation succeeded. `otool -t` showed identical complete text sections for the rebuilt and supplied libraries (473 output lines after removing the filename header). The rebuilt and supplied constant sections also match. The audit found exact agreement on 12,000 gap calls and all 76 saved-angle target calls. These comparisons connect the inspected C source to the executable used for replay.

   `.venv/bin/python audit_packet.py` passed independent coverage/table/margin/hash checks subject to finding 6, exhaustive small-grid DP enumeration, the re-executed 200,000-triple/800,000-term long-double lemma gate (zero violations, minimum slack `1.2431738462548303e-05`), 7,776 deterministic endpoint/corner evaluations using independent 90-decimal support calculations (zero violations without tolerance; largest lower-minus-reference `−8.573419617979812e-16`), and all 76 high-precision target checks. An initial binary64 hull endpoint diagnostic failed at H=2 and t=t'=binary64 π/2: the hull rounded away tiny tilted edges and reported approximately zero against a gap bound near one. Exact-endpoint, high-precision reevaluation confirmed closed κ=1. That failure is a reference-conditioning issue, not evidence for accepting sampled tests as proofs. I did not rerun the complete original random gates or historical gate 3; the supplied logs remain historical evidence.

   From `o1dp/`, I ran the unmodified documented command `../.venv/bin/python src/driver.py verify`. It exited successfully with the exact output `certificate replay PASS: 76 slices; 76 proved`. Thus every saved D and recomputed target matched exactly, all 76 saved-grid proofs replayed, and the command's coverage assertions passed. A separate timed replay of the first 200-cell grid also reproduced D exactly (1.484021 seconds). These executions used the supplied library, whose executable text and constant sections match the fresh build described above.

**Verdict:** Yes: O1 for the chain explicitly defined in SPEC.md is certified on [1.87,2) under the stated vertex-reduction, F6, IEEE-754/compiler, and eight-ulp libm premises. The lemma is valid, the reviewed bounds and DP are sound under those premises, coverage is complete, and all 76 slices replayed exactly with positive margins. The five MINOR findings require documentation, provenance, and checker repairs; they do not invalidate this SPEC-chain result. The literal contextual FI-O1 formula must be corrected before identifying it with this result. I have not re-proved the external vertex reduction or the supplied identification of F6, established the system libm error guarantee, or resolved O2; no physical packing lower bound at H=2 is certified.
