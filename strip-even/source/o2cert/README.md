# O2 certified computation report

**All H-cells certified.**

## Gates

Results below are copied from gates.partial.json and gates.log.

- G1: `{"pairs": 200000, "dense_points": 20001, "dual_triples": 2000, "violations": 0, "max_A_gap": 4.8276862090536084e-14, "min_A_gap": 4.440892098500626e-16, "max_m_gap": 1.3145040611561853e-13, "dual_max_error": 6.661338147750939e-16, "elapsed_seconds": 6.732704000023659, "passed": true}`
- G2: `{"boxes": 100000, "samples_per_box": 20, "straddling_boxes": 50000, "violations": 0, "max_excess_plain_centered_A_m": [-8.451905841866392e-12, -6.490757264998592e-09, -1.63202784619898e-14, -1.580957587066223e-13], "elapsed_seconds": 17.943258000013884, "passed": true}`
- G3: `{"boxes": 20000, "samples_per_box": 10, "violations": 0, "max_excess": -0.3795986259682538, "elapsed_seconds": 26.45163820902235, "passed": true}`
- G4: `{"identity_H": [1.87, 1.9, 1.95, 1.99, 2], "identity_errors": [0.0, 8.881784197001252e-16, 8.881784197001252e-16, 1.7763568394002505e-15, 2.6645352591003757e-15], "H_samples_per_cell": 50, "violations": 0, "max_minimum_minus_trial": -8.871126055964851e-12, "elapsed_seconds": 26.467200209008297, "passed": true}`
- G5: `{"H_samples": 10000, "max_sup_distance": 0.2724264214723131, "inward_inclusion": true, "J_odd": [0.7409, 1.15], "J_even": [-1.2724604332697271, -0.8500000000000001], "violations": 0, "elapsed_seconds": 26.774183959001675, "passed": true}`

## Per-H-cell results

| Cell | Ha | Hb | Outer boxes | Inner boxes | Discards | Minimum margin | Seconds | Complete |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| H0 | 1.8699999999999999 | 1.88625 | 45627 | 224586736 | 0 | 4.5093924772032773e-07 | 549.220121 | True |
| H1 | 1.88625 | 1.9025000000000001 | 40809 | 190213118 | 0 | 6.417922575607803e-07 | 496.360372 | True |
| H2 | 1.9025000000000001 | 1.91875 | 39463 | 177153318 | 0 | 1.8995141015665237e-07 | 497.912742 | True |
| H3 | 1.91875 | 1.9350000000000001 | 40599 | 180314888 | 0 | 8.738316531697874e-06 | 525.624014 | True |
| H4 | 1.9350000000000001 | 1.9512499999999999 | 42623 | 189550772 | 0 | 1.0355866179700966e-05 | 567.693651 | True |
| H5 | 1.9512499999999999 | 1.9675 | 46373 | 206659326 | 0 | 3.158408188319583e-06 | 621.976588 | True |
| H6 | 1.9675 | 1.9837499999999999 | 52771 | 236708646 | 7 | 4.5183895380773715e-07 | 706.391573 | True |
| H7 | 1.9837499999999999 | 2 | 63973 | 284832286 | 3693 | 9.376187737331064e-08 | 831.177205 | True |

Final resumed invocation wall time: 532.736663 seconds. No H-cells are missing.

## Implementation and assumptions

C kernel reuses o1dp nextafter arithmetic and eight-ulp libm padding. Every interval operation is outward rounded and asserts ordered endpoints. The eight-ulp libm accuracy premise is retained; this is not a proof of the platform libm. Python uses the requested venv, numpy and scipy. Sources and shared library are hashed. No network or git commands were used. One temporary port-generation helper was initially written to /private/tmp/build_corner_o2.py, contrary to the requested write boundary, then moved into the project and archived at initial-pass/staging/build_corner_port.py. All deliverables and computation outputs are inside o2cert; no sibling project files were changed.

Candidate bounds, global-Lipschitz centred forms, best-first inner B&B, affine H endpoint tests, product exclusion, per-cell checkpoints and deterministic saved-rectangle replay are implemented. Full and excluded inner intervals use directed decimal endpoints. Adjacent cells share endpoints. Partition verification checks exact coverage and disjoint interiors of certified plus pending rectangles; pending regions are not certified.

## Deviations and open work

The simpler constant Lipschitz option is used instead of interval AD. Inner searches stop at a fixed box budget, which the spec permits; this can leave conservative lower bounds. Outer selection uses largest area first rather than smallest bound. Initial outer partition aligns with exclusion boundaries. The discard shortcut uses the full inner-range lower bound of -sigma; excluded-piece-specific discard optimizations are not needed for soundness. The driver supports adaptive H-cell splitting and resumable per-cell partitions. Full H-cells may remain open at the configured time/box limit; the same driver resumes their queues.

## Issues with the spec

None identified in LEMMAS.md or SPEC.md during implementation. See the separate corner audit for issues in the supplied swarm proof and arithmetic.

## Reproduce

```sh
clang -O2 -shared -fPIC src/kernel.c -o src/kernel.dylib
../.venv/bin/python src/driver.py gates --workers 8
../.venv/bin/python src/driver.py run --workers 8 --seconds 600 --max-boxes 200000 --inner-budget 2047 --split-depth 1
../.venv/bin/python src/corner_replay.py
../.venv/bin/python src/driver.py verify
../.venv/bin/python src/driver.py report
```

## Part B: directed corner replay

The source `iv.py` encloses add, subtract, multiply, divide, negation,
absolute value, square root, acos and tan. Negation and abs endpoints are exact.
Its constructor does not validate ordered endpoints. One-ulp padding of libm
functions is an accuracy assumption, not a universal guarantee. The port checks
interval ordering and uses the same eight-ulp libm premise as part A.

The original final assembly is **not fully directed**. The following scalar
operations feed a bound without directed rounding:

- `1/math.sqrt(2)` as the lower bracket for rho in `a_prime_negative_ok` and
  `T_enclosure`; rounded upward this can omit the H=2 endpoint.
- H-cell endpoints, `Tlo-RC`, `Thi+RC`, `1/Thi-RC`, `1/Tlo+RC`.
- Reciprocal endpoints `1/XI.hi`, `1/XI.lo` in Dmax and M2g domains.
- `Dmax=max(Lp,Lq)/XI.lo` and subtractions assembling A4 and A8.
- Every add, multiply and subtract in the scalar A5 and A6 expressions.
- `Dmax+lmax` and the final subtraction assembling A9.
- A7's Taylor penalty `min(M2,M2g)*dd/4` before wrapping it with C: padding
  the already-rounded result once does not enclose arbitrary accumulated error.
- Interpolated final subdivision endpoints: roundoff can move the last endpoint
  away from its parent boundary. Internal shared endpoints themselves are valid
  partition boundaries and need not be rounded outward.

The port fixes these operations, preserves the nine scan formulas and counts,
uses outward H-cell envelopes covering the original decimal cells, enforces exact
parent endpoints in subdivisions, and uses an outward enclosure of radius 0.32.
Binary midpoints used solely as shared split boundaries are retained: their value
need not equal the exact midpoint to partition the parent. Comparisons, counts,
min/max selecting already valid bounds, formatting and timing require no directed
padding. `corner_certificate.json` contains full precision per-cell results;
`corner-comparison.json` compares a local copy of the unchanged arithmetic with
the port. The only change to that baseline is JSON recording.

A typographical identity in the supplied PROOF.md section 5 is false as printed:
`lam(x)+1/(2Rx) = (H Rx-2)/(2xRx) = H/2-1/Rx`.
The last expression needs division by x. The next displayed factorization
`B_X-A(u)=(1/x-u)[A[1/x,u]+H/2-1/Rx]` is correct because W=x(1/x-u),
and A7 implements that correct factorization. No lemma or scan was changed.
This typo is in the swarm proof, not in LEMMAS.md or SPEC.md.

The replay retains the supplied analytic surrogate proof and monotonicity/root
identity as mathematical premises. Numerical scans do not formally verify those
symbolic premises or establish an unconditional libm error bound.

### Measured corner margins

| Scan | Directed minimum | Directed minus original |
|---|---:|---:|
| A1 | 0.022013814839154766 | -1.8630930131990908e-15 |
| A2 | 0.08422427910981195 | -4.4686476741162551e-15 |
| A3 | 0.19087499701716851 | -2.7755575615628914e-15 |
| A4 | 0.020814288051128945 | -1.0522832605275312e-14 |
| A5 | 0.067590661701055973 | -6.2311267257086911e-15 |
| A6 | 0.10772626391944538 | -3.3445468616832841e-15 |
| A7 | 0.020002508942806068 | -1.9845236565174673e-14 |
| A8 | 0.11487827092322604 | -1.1948775302528247e-14 |
| A9 | 0.14197397587675528 | -1.2878587085651816e-14 |

The directed replay used 52 H-cells and 414652 interval boxes, with 0 open scans, in 5.984429 seconds. These numbers are from corner_certificate.json.

### Gate repair history

The initial run used the closed-form m1 reference. After adding the required dense m1 grid and kink refinement, G1 recorded 5,299 violations caused by cancellation in that trigonometric reference at negative x. The gate and its zero-violation threshold were preserved. The C lower bound received an additional downward guard of `64*2^-52*(1+max(|lo|,|hi|))`; the complete gate suite was rerun. Both the failed and passing records remain in gates.log. The final gate results above correspond to the source hashes in gates.json.

Total logged main wall time across completed invocations: 836.266076 seconds.

Corner replay was performed while part A was running, rather than waiting until after its final verification. Part-A verification makes no outer or H splits, but recomputes the deterministic inner branch-and-bound bounds. Thus it is not a replay of stored inner subdivision traces; those are not included in the certificate. An end-to-end timer was not started before the document reads; the reported total is the logged main-search wall time.

### Saved-rectangle scope

A cell marked incomplete has certificates only for its saved accepted rectangles. Its pending rectangles are explicitly uncertified. Verification rechecks every accepted rectangle and the full partition made of accepted plus pending rectangles. A successful partial replay must not be described as a proof of the entire domain. The corner proof does not fill these pending regions automatically.

## Remaining scope

No H-cells remain open. Part A covers the full box outside the fixed exclusion, and part B replays the corner certificate. The resulting O2 implication relies on the supplied analytic lemmas and the documented binary64/libm assumptions; the random gates and numerical replay are not an independent formal verification of those premises.

## Search and replay details

The first pass allowed 300 seconds per H-cell; the resumed pass allowed a further 600 seconds per attempted cell, each below the requested two-hour ceiling. Checkpoints were saved during each search and after each completion. The endpoint bounds use the exact affine-in-H argument. For nonnegative endpoint variables, the kernel evaluates m1(x)-Hx as 1+(1-H)x to retain cancellation. The source and initial certificates before this change are preserved in initial-pass/. Current verification reevaluates every accepted rectangle with the current kernel and checks positive margins; historical stored margins can be more conservative. Inner box counts include counts charged to memoized inner-bound requests.

No adaptive H-cell split was required in the completed pass.

## Final replay

The replay checked 186155 accepted outer rectangles in 498.276885 seconds. Complete-domain coverage: True. Every saved partition and numerical bound passed. The smallest recomputed positive margin was 9.376187737331064e-08. See verification.log and verification.json.

## Referee findings and post-review changes (2026-10-31, added by the project owner)

Blind Codex review (`../docs/o2cert-review-codex-2026-10-31.md`): verdict "O2 is certified on [1.87, 2] under the stated premises", no MAJOR findings. The referee recompiled the kernel, reran gates (PASS), the corner replay (PASS) and the full verify (PASS, 186,155 rectangles = 182,455 numerical + 3,700 analytic discards, minimum recomputed margin 9.376e-8), and checked every lemma with 60-digit arithmetic.

Changes made after the review:
- `LEMMAS.md`: Lemma 1 now assumes nonempty interior and proves the top/bottom case by compactness; Lemma 5's intermediate sum corrected; Corollary 10.1 states H ≤ 2; §7 range corrected; §8 added. Text only.
- `src/refresh_provenance.py`: rewrote `source_hashes` in `certificate.json` and `cells/*.json` to the post-edit hashes and appended a `provenance_refresh` block recording the old hashes and the reason. `certificate.sha256` updated. `driver.py verify` was rerun afterwards (`verify-after-refresh-console.log`, `verification.log`).
- `src/corner_impl/run_corner.py`: the monotonicity precondition (sup a' < 0) is now asserted, not just printed (referee MINOR 19); `corner_replay.py` rerun, same nine margins, 0 open.
- Not changed, on purpose: `src/kernel.c` (referee MINOR 13: the unused upper endpoint of `mone` is not a general enclosure when the box spans both signs; the lower endpoint, which is all the certificate uses, is sound). Any kernel edit would require a full rerun; the kernel stays as audited.
- Known exposition errors in the swarm's `PROOF.md` (not part of this project): the dropped 1/x factor in §5 T2 and the false sharp-q remark at lines 186–190; neither affects the nine scans.
- The referee's MINOR 4 (hard-coded path to `m4check.py`) applies to packets that move the project; in this repository the path exists.

Distribution note: `certificate.json` (32 MB) is committed as `certificate.json.gz`; `gunzip -k certificate.json.gz` before `driver.py verify`. `cells/`, `initial-pass/` and `certificate.before-parallel-verify.json` are provenance copies kept out of git (the certs bundle carries them).
