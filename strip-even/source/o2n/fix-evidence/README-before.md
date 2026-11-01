# O2n certified computation

The supplied SPEC.md and revised LEMMAS.md are unchanged. The claims below use their analytic lemmas and the arithmetic assumptions stated below. Random gates alone are not certificates.

## Results

| Run | Completed H-cells | Accepted outer boxes | Tested outer boxes | Inner boxes charged | Minimum strict margin | Exact requested rational H range | Search wall seconds |
|---|---:|---:|---:|---:|---:|---|---:|
| n8 | 30 | 14,016 | 27,848 | 118,628,654 | 1.4573977746429317e-06 | [1.852049, 2] | 73.069441 |
| n6 | 28 | 6,565 | 13,044 | 47,255,346 | 1.1125800777611603e-06 | [1.861098, 2] | 29.145306 |
| n10 | 28 | 12,500 | 24,832 | 107,606,480 | 6.5592756344767791e-06 | [1.86, 2] | 64.746643 |
| n10-five | 6 | 152,026 | 303,982 | 2,018,388,334 | 4.0450333985141251e-08 | [1.846936, 1.86] | 2678.156017 |

Counts are from the completed partition. Inner counts include the initial bound request and the second request that saves the accepted leaf partition. The final five-block continuation also counts exact-key cache hits; these are charged leaf counts, not counts of distinct arithmetic evaluations. Superseded H-cell attempts, if any, are separate in each certificate. Search wall time excludes gates and final replay.

Replay: **PASS**, 92 H-cells, 185,107 accepted outer boxes, 579.334272 seconds. All recorded cells have complete-domain coverage: True. Replay verifies source hashes, H0, tail caps, T brackets, local hypotheses, every inner leaf bound, both endpoint inequalities, and outer partition coverage. It never runs a minimization or bisection.

## Gate results

The final gate pass is gates.json, pinned to the final source/library hashes. Earlier development gate records are archived in development-run/gates-history.log.

- **G1_points_D: PASS**, {"points": 200000, "dense_points_per_reference": 20001, "D_points": 1000, "violations": 0, "A_gap_min": 4.440892098500626e-16, "A_gap_max": 4.7961634663806775e-14, "m_gap_min": 1.4654943925052066e-14, "m_gap_max": 1.3145040611561853e-13, "D_Dp_Dpp_max_error": [4.996003610813204e-16, 5.551115123125783e-17, 1.6653345369377348e-16]}.
- **G1_boxes_centered: PASS**, {"boxes": 100000, "points_per_box": 20, "straddling_boxes": 50000, "violations": 0, "max_excess_plain_centered_A_m": [-1.0384582083133864e-11, -5.4082782696696086e-09, -1.63202784619898e-14, -3.4017233474514796e-13]}.
- **G2_n8: PASS**, {"boxes": 20000, "points_per_box": 20, "violations": 0, "max_excess": -0.013360399904308873}.
- **G2_n6: PASS**, {"boxes": 20000, "points_per_box": 20, "violations": 0, "max_excess": -0.011415257854847712}.
- **G2_n10: PASS**, {"boxes": 20000, "points_per_box": 20, "violations": 0, "max_excess": -0.013743933172652323}.
- **G2_n10_five: PASS**, {"boxes": 20000, "points_per_box": 20, "violations": 0, "max_excess": -0.1752931614303962}.
- **G3: PASS**, {"family_points_per_n": 200, "telescoping_per_n": 500, "five_identity_points": 500, "violations": 0, "max_errors": [8.881784197001252e-15, 2.525757381022231e-15, 1.865174681370263e-14, 6.217248937900877e-15]}.
- **G4: PASS**, {"H_per_n": 300, "violations": 0, "max_root_error": 1.4432899320127035e-15, "min_upper_trial_gap": 2.573025495901921e-14}.
- **G5: PASS**, {"local_points_per_n": 2000, "negative_cY_instances": 2000, "negative_attempts": 2113, "violations": 0, "min_block_gap": 0.0034681600019381698, "min_negative_pair_gap": 0.00010096469599185642}.
- **G6: PASS**, {"origin_points_per_n": 2000, "five_origin_points": 2000, "cone_points": 2000, "violations": 0, "min_triple_values": [8.358040888270787e-09, 8.4767536717046e-09, 1.7244923465484447e-08], "min_five": 2.066992468087751e-08, "min_cone_slack": 0.0011114032292265982}.

G4 supplemental check: one additional random H per n, zero violations. Combined total: 300 random H plus the explicit H=2 endpoint per n. The supplement also runs the 2,000 original o2cert G1 support-function/hull triples; see supplemental-gates.json for the maximum error.

Final gate wall time: {g["seconds"]:.6f} seconds.

## H0, local, tail, and endpoint evidence

### n8

H0: `{"H": 1.852049, "T_hat": 0.919182758067, "f_upper": 7.999996155384644, "f_minus_n_upper": -3.8446153558524534e-06, "T0": 0.919, "derivative_upper": -0.00037780371554765874}`. Tail checks: `{"c_cap": 0.4077, "cap_slack": 8.291281477629252e-05, "theta_over_k_upper": 3.0126951453087076}`.
Minimum recorded local slacks: `{"containment": 0.2427353338308946, "J": 0.17079299999999994, "N1": 0.05325956868252487, "N1'": 0.08578436802338828, "N2'": 0.09275030551856073, "N3": 0.39922906337401054, "L": 0.047676352307445574, "min_cY": -0.0005441529668763348}`. Peak worker RSS: 85,884,928 bytes. 0 superseded H-cell attempts.
Exact outward binary64 domain endpoints as rational numbers: `[8340887186271899/4503599627370496, 2]`; hex: `[0x1.da1fe21d96e9bp+0, 0x1.0000000000000p+1]`. The table reports the exact requested rational subrange contained in those endpoints.

### n6

H0: `{"H": 1.8610980000000001, "T_hat": 0.88799735207, "f_upper": 5.9999957975292375, "f_minus_n_upper": -4.202470762493248e-06, "T0": 0.887, "derivative_upper": -0.0014653337701180794}`. Tail checks: `{"c_cap": 0.3935, "cap_slack": 3.911667753431213e-06, "theta_over_k_upper": 3.0902441324983716}`.
Minimum recorded local slacks: `{"containment": 0.23978432724144236, "J": 0.14011399999999993, "N1": 0.060165204682976266, "N1'": 0.1091791425431514, "N2'": 0.09798579885629263, "N3": 0.3988608999303184, "L": 0.04765587814014168, "min_cY": -0.001014753474676962}`. Peak worker RSS: 85,262,336 bytes. 0 superseded H-cell attempts.
Exact outward binary64 domain endpoints as rational numbers: `[8381640259299975/4503599627370496, 2]`; hex: `[0x1.dc70eb24a6a87p+0, 0x1.0000000000000p+1]`. The table reports the exact requested rational subrange contained in those endpoints.

### n10

H0: `{"H": 1.8469360000000001, "T_hat": 0.936728340798, "f_upper": 9.99999571475745, "f_minus_n_upper": -4.2852425501394e-06, "T0": 0.936, "derivative_upper": -0.0019396076117671327}`. Tail checks: `{"c_cap": 0.39530000000000004, "cap_slack": 7.47107636737132e-05, "theta_over_k_upper": 2.9416442561635727}`.
Minimum recorded local slacks: `{"containment": 0.24405880075241024, "J": 0.17627067437010255, "N1": 0.060249710659904025, "N1'": 0.08503136298606571, "N2'": 0.09520015020469666, "N3": 0.3993984328620283, "L": 0.047672539378529506, "min_cY": -0.000665480132779412}`. Peak worker RSS: 85,835,776 bytes. 0 superseded H-cell attempts.
Exact outward binary64 domain endpoints as rational numbers: `[4188347653454561/2251799813685248, 2]`; hex: `[0x1.dc28f5c28f5c2p+0, 0x1.0000000000000p+1]`. The table reports the exact requested rational subrange contained in those endpoints.

### n10-five

H0: `{"H": 1.8469360000000001, "T_hat": 0.936728340798, "f_upper": 9.99999571475745, "f_minus_n_upper": -4.2852425501394e-06, "T0": 0.936, "derivative_upper": -0.0019396076117671327}`. Tail checks: `{"c_cap": 0.41550000000000004, "cap_slack": 2.7614749189663886e-05, "theta_over_k_upper": 5.9541533483778375}`.
Minimum recorded local slacks: `{"containment": 0.24835734203955304, "J": 0.187648, "N1": 0.04874168365454067, "N1'": 0.07295369159433827, "N2'": 0.09411198424212883, "N3": 0.4144824209301151, "L": 0.07031577128376092, "min_cY": 0.023561302095486104}`. Peak worker RSS: 147,537,920 bytes. 4 superseded H-cell attempts.
Exact outward binary64 domain endpoints as rational numbers: `[4158930140688577/2251799813685248, 8376695306909123/4503599627370496]`; hex: `[0x1.d8d0cc35ce182p+0, 0x1.dc28f5c28f5c3p+0]`. The table reports the exact requested rational subrange contained in those endpoints.

Full per-attempt results, open cells, best failed margins and per-cell timings: [certificate-n10-five.json](certificate-n10-five.json).

## Implementation and assumptions

- The candidate evaluator and global Lipschitz centred form are copied verbatim from `../o2cert/src/kernel.c` into `src/kernel.c`; no sibling imports are used. The copied driver is retained as a development reference. `src/block.c` extends the kernel.
- Run the Python entry points without `-O` or `PYTHONOPTIMIZE`; assertion checks are part of verification.
- IEEE binary64 and round-to-nearest basic operations are assumed. Each interval arithmetic result is expanded with nextafter, and sqrt/libm results use the inherited eight-ulp padding. The build uses `-O2 -ffp-contract=off`, no fast-math. These are conditional numerical certificates, not a formal proof of the platform libm or compiler.
- Every trial T_hat is an exact binary64 rational, shared between the two endpoints. Endpoint bounds and the given affine-in-H argument certify the whole H-cell.
- H0 evaluates rational H_lo and T0 using enclosing binary64 intervals. T_lo and T_hi are binary64 rationals with strict endpoint sign checks. The local box is rounded inward. Local checks use the whole independent (T,H) rectangle, allow negative cY, and use 256 interval subdivisions of J for L. Neither gamma >= 0 nor Tan is checked.
- The five-block tail uses the sum of positive parts `k*(x1^+ + Y2^+ + x3^+ + Y4^+) + (k/2)*x5^+`; the printed caps are checked against its exact rational ratios.
- The first-order origin bounds are Lemmas 21 and 21'; no C0 computation is used. Product exclusions are implemented as unions over the odd-coordinate complements, after outer splitting at the even-coordinate boundaries.
- Each accepted outer box references a compressed file of all inner leaf intervals with a SHA-256 hash. The H-cell manifest is compressed and hashed in the top-level certificate. Failed/partial H-cells never count as full-range certificates.
- Six worker processes maximum. Streaming the accepted inner partitions keeps worker memory bounded; the worker safety cutoff is 230 MiB RSS. The initial runner caps each range at 10,200 seconds; the five-block continuation enforces a cumulative 10,800-second cap. Archived development search times are listed below and included in the aggregate budget audit. No network, git commands, or writes outside o2n were used.

## Deviations from SPEC.md

1. Outer selection uses largest volume first, instead of prioritizing the smallest lower bound. Inner minimizations use the prescribed best-first lower bound. This affects search order only; every accepted box is checked identically.
2. The shared gate suite, including the other n and five-block cases, was run before the n=8 production search. Production ranges were then run in the requested n=8, n=6, n=10 even-star, n=10 five-block order.
3. The n=10 even-star and five-block manifests are separate (`certificate-n10.json`, `certificate-n10-five.json`) to preserve their separate range budgets and schemas.
4. During development, a superseded n=8 run was interrupted to replace memory-growing embedded leaf lists with streamed compressed files and to tighten the scalar rational T0 enclosure. That checkpoint is archived under `development-run/`; it is not part of the final certificate. A second development run (`development-run-2/`) was stopped to remove unnecessary root finding from replay. All final certificates were regenerated; their verification uses only stored parameters, interval checks, and leaf bounds. The five-block range was continued with `src/resume_range.py` after its first 180-second attempts; this runner preserves the completed cells and cumulative range time while giving new cells up to 1,800 seconds and 500,000 outer tests. The last cell was then resumed from its saved spatial partition with `src/continue_partitions.py`, preserving every accepted box and enforcing the remaining cumulative budget. It uses a bounded, exact-key cache of deterministic inner results, checked against uncached results on 60 cases with zero differences; all stored leaf intervals are still replayed directly. All production ranges were restarted from the final source, and the final gates and replay are pinned to that source.

5. One extra random H per n and the legacy hull cross-check were added as supplemental gates after the search, bringing G4 to 300 random H plus H=2 per n. The full primary gate suite ran before the search.

## Issues with the spec

None identified in the revised fixed mathematics. Neither historical issue in README-attempt1.md or README-attempt2.md applies to this version. No mathematical formula, coefficient, lemma, target inequality, clipping bound, or coordinate cap was changed.

## What remains open and uncertain

The slivers [H*(n), H_lo(n)) remain uncovered, as the specification requires. No result for n >= 12 is claimed. The certificate relies on the supplied analytic lemmas and the documented compiler/binary64/libm premises. Random gates do not independently prove those premises.

## Reproduce

To replay this shipped bundle, retain its compiled library and run `../.venv/bin/python src/driver.py verify --workers 6`, followed by `../.venv/bin/python src/audit_bundle.py`. Rebuilding can change the library hash. For a fresh search, first move the four certificate manifests to a backup directory, then run:

```sh
clang -O2 -ffp-contract=off -shared -fPIC src/block.c -o src/kernel.dylib
../.venv/bin/python src/driver.py gates --workers 6
../.venv/bin/python src/driver.py run --workers 6 --inner-budget 511 --tol 0.00002 --cell-seconds 1800 --max-outer 500000 --range-seconds 10200
../.venv/bin/python src/supplement_g4.py
../.venv/bin/python src/driver.py verify --workers 6
../.venv/bin/python src/audit_bundle.py
../.venv/bin/python src/driver.py report
../.venv/bin/python src/make_report.py
```

A partial five-block run can be continued with `../.venv/bin/python src/resume_range.py certificate-n10-five.json --cell-seconds 1800`. `run` skips completed ranges. To start over, move the four top-level certificate manifests aside first; all old cell and leaf files are harmless unless referenced by a current manifest. Build details are in build.json; numerical gate data in gates.json; production progress in run.log, run-console.log, resume-console.log, and continuation-console.log (run.log also retains superseded development entries); current manifests are authoritative. Replay results in verification.json and verification.log.

Additional bundle audit: PASS. Exact requested ranges and source provenance were checked, and every stored parameter check was exercised with root and inner-search entry points disabled; the replay function was also checked for search calls. See bundle-audit.json.

Exact-key cache gate: 60 cases, 0 violations. Cached bounds and every saved interval matched the uncached result bit for bit.

## Aggregate search time audit

Logged search times exclude document reading, gates, final replay, and pauses between invocations. Interrupted development times are their last checkpoint values.

| Range | Final production seconds | Archived development seconds | Total search seconds |
|---|---:|---:|---:|
| n8 | 73.069441 | 101.570377 | 174.639818 |
| n6 | 29.145306 | 30.348134 | 59.493440 |
| n10 | 64.746643 | 54.931804 | 119.678448 |
| n10-five | 2678.156017 | 0.000000 | 2678.156017 |
