# O1 even-n certified interval DP

The statements below concern the fixed SPEC chain, conditional on the arithmetic and mathematical premises listed below. No monotonicity of F_n is assumed. On each proved slice, D is a lower bound for every non-alternating chain and F_n(H) is at most the stored F_n_ub throughout the slice. The strict positive margin D - F_n_ub therefore proves Phi > F_n(H).

## Results

| n | proved / unproved slices | exact proved H range (H < 2) | minimum positive margin | maximum cells | run wall seconds | gates + run wall seconds |
|---|---|---|---:|---:|---:|---:|
| 8 | 145 / 0 | [1.8549999999999998, 2.0) | 0.00012543447209534261 | 464 | 114.687 | 186.997 |
| 10 | 150 / 0 | [1.8499999999999999, 2.0) | 0.00027035684969156643 | 464 | 202.777 | 601.593 |

## Regression and gates

The n=6 regression reuses three exact saved grids from `../o1dp/certificate.json` (first, middle, last). D matches bit for bit; the old target is used only as the binding threshold during this regression. The new n=6 point-target upper bounds also match the old values within 2.58e-14. New certification uses the interval-in-H chain target. Logged witness roles use 0=F and 1=C.

```text
regression-n6.log
slice=0 Ha=1.8699999999999999 Hb=1.8720000000000001 cells=200 D=5.965757725467423 reference_D=5.965757725467423 error=0 PASS=True seconds=1.454
slice=38 Ha=1.9460000000000002 Hb=1.9480000000000002 cells=200 D=5.6649197271183045 reference_D=5.6649197271183045 error=0 PASS=True seconds=1.413
slice=75 Ha=1.9999990234375 Hb=2 cells=800 D=5.4786381746324899 reference_D=5.4786381746324899 error=0 PASS=True seconds=22.695
target_slice=0 old_F6_ub=5.9562252971060259 new_point_F6_ub=5.956225297106049 delta=2.3092638912203256e-14 new_interval_F6_ub=5.9562253800304523 PASS=True
target_slice=38 old_F6_ub=5.5817732851362605 new_point_F6_ub=5.5817732851362862 delta=2.5757174171303632e-14 new_interval_F6_ub=5.5817735654634335 PASS=True
target_slice=75 old_F6_ub=5.3137133817962976 new_point_F6_ub=5.3137133817963225 delta=2.4868995751603507e-14 new_interval_F6_ub=5.3137133817965667 PASS=True
gates-n8.log
gate1 samples=100000 max_abs_error=6.106226635438361e-15 PASS=True
gate2 boxes=50000 interior_samples=3200000 violations=0 max_G_minus_reference=-9.6082741762870683e-10 PASS=True
lemma_gate triples=200000 terms=800000 H2=50000 W_le_1e-3=50000 violations=0 min_term_minus_lemma=1.2431738462548303e-05 PASS=True
gate5 cases=1000 samples=50000 violations=0 max_chain_minus_upper=-3.1974423109204508e-14 max_point_excess=2.6645352591003757e-13 PASS=True
gate3 search slice=[1.8549999999999998,1.8599999999999999] random_nonalt_patterns=300 method=L-BFGS-B best=8 witness={"roles": [0, 0, 0, 0, 0, 0, 0, 0], "tilts": [0, 0, 0, 0, 0, 0, 0, 0], "H": 1.8599999999999999}
gate3 slice=[1.8549999999999998,1.8599999999999999] cells=50 unconstrained=7.7195739039811642 right_end_target=7.9448090536561997 deficit=0.22523514967503555 flagged=7.7874486964681093 sampled_nonalt=8 PASS=True
gate3 slice=[1.8549999999999998,1.8599999999999999] cells=100 unconstrained=7.8325157189163521 right_end_target=7.9448090536561997 deficit=0.11229333473984759 flagged=7.8853056552873051 sampled_nonalt=8 PASS=True
gate3 slice=[1.8549999999999998,1.8599999999999999] cells=200 unconstrained=7.8887751494312814 right_end_target=7.9448090536561997 deficit=0.056033904224918274 flagged=7.9338224235957986 sampled_nonalt=8 PASS=True
gate3 slice=[1.8549999999999998,1.8599999999999999] cells=400 unconstrained=7.9167843244864597 right_end_target=7.9448090536561997 deficit=0.02802472916973997 flagged=7.9580010308428575 sampled_nonalt=8 PASS=True
gate3 search slice=[1.8999999999999999,1.9099999999999999] random_nonalt_patterns=300 method=L-BFGS-B best=7.8556865959549196 witness={"roles": [1, 0, 1, 0, 1, 0, 1, 1], "tilts": [0.0, 0.7853518465554464, 1.5707963267948966, 0.785437985675022, 0.785435563478214, 0.7854355643272023, 1.5707963267948966, 1.5707963267948966], "H": 1.9096704813670795}
gate3 slice=[1.8999999999999999,1.9099999999999999] cells=50 unconstrained=7.3830840784489826 right_end_target=7.5975743878796109 deficit=0.2144903094306283 flagged=7.4984403214032103 sampled_nonalt=7.8556865959549196 PASS=True
gate3 slice=[1.8999999999999999,1.9099999999999999] cells=100 unconstrained=7.4912992423078499 right_end_target=7.5975743878796109 deficit=0.10627514557176099 flagged=7.5911770507689234 sampled_nonalt=7.8556865959549196 PASS=True
gate3 slice=[1.8999999999999999,1.9099999999999999] cells=200 unconstrained=7.5446083449058525 right_end_target=7.5975743878796109 deficit=0.052966042973758398 flagged=7.6368586322135945 sampled_nonalt=7.8556865959549196 PASS=True
gate3 slice=[1.8999999999999999,1.9099999999999999] cells=400 unconstrained=7.5711281599984481 right_end_target=7.5975743878796109 deficit=0.026446227881162798 flagged=7.6595451647306119 sampled_nonalt=7.8556865959549196 PASS=True
gate3 PASS=True seconds=22.636
gate4 chains=20000 violations=0 max_path_bound_minus_reference=-0.017689042454431814 max_global_DP_minus_reference=-0.7598354225824524 PASS=True seconds=64.838
gates-n10.log
gate1 samples=100000 max_abs_error=6.106226635438361e-15 PASS=True
gate2 boxes=50000 interior_samples=3200000 violations=0 max_G_minus_reference=-9.6082741762870683e-10 PASS=True
lemma_gate triples=200000 terms=800000 H2=50000 W_le_1e-3=50000 violations=0 min_term_minus_lemma=1.2431738462548303e-05 PASS=True
gate5 cases=1000 samples=50000 violations=0 max_chain_minus_upper=-3.1974423109204508e-14 max_point_excess=2.6645352591003757e-13 PASS=True
gate3 search slice=[1.8499999999999999,1.855] random_nonalt_patterns=300 method=L-BFGS-B best=10 witness={"roles": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "tilts": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "H": 1.855}
gate3 slice=[1.8499999999999999,1.855] cells=50 unconstrained=9.640508851866878 right_end_target=9.9277896275149065 deficit=0.28728077564802845 flagged=9.6973900259375085 sampled_nonalt=10 PASS=True
gate3 slice=[1.8499999999999999,1.855] cells=100 unconstrained=9.7837045172842565 right_end_target=9.9277896275149065 deficit=0.14408511023064996 flagged=9.827736058458914 sampled_nonalt=10 PASS=True
gate3 slice=[1.8499999999999999,1.855] cells=200 unconstrained=9.8555424313185682 right_end_target=9.9277896275149065 deficit=0.072247196196338237 flagged=9.8931537994692729 sampled_nonalt=10 PASS=True
gate3 slice=[1.8499999999999999,1.855] cells=400 unconstrained=9.8916031723259827 right_end_target=9.9277896275149065 deficit=0.036186455188923716 flagged=9.9260070703667544 sampled_nonalt=10 PASS=True
gate3 search slice=[1.8999999999999999,1.9099999999999999] random_nonalt_patterns=300 method=L-BFGS-B best=9.6043703368634219 witness={"roles": [0, 1, 1, 0, 1, 0, 1, 0, 1, 0], "tilts": [0.0, 1.5707963267948966, 1.5707963267948966, 0.8192647808316703, 0.8192645573791115, 0.8192645453743906, 0.8192645420366378, 0.8192645481755205, 0.8192645484468685, 1.5707963267948966], "H": 1.90902209722172}
gate3 slice=[1.8999999999999999,1.9099999999999999] cells=50 unconstrained=9.1634769032883643 right_end_target=9.4351398219296261 deficit=0.2716629186412618 flagged=9.274017427841633 sampled_nonalt=9.6043703368634219 PASS=True
gate3 slice=[1.8999999999999999,1.9099999999999999] cells=100 unconstrained=9.2998500174168317 right_end_target=9.4351398219296261 deficit=0.13528980451279438 flagged=9.3970240130752725 sampled_nonalt=9.6043703368634219 PASS=True
gate3 slice=[1.8999999999999999,1.9099999999999999] cells=200 unconstrained=9.3674251538012339 right_end_target=9.4351398219296261 deficit=0.067714668128392219 flagged=9.4580602999874017 sampled_nonalt=9.6043703368634219 PASS=True
gate3 slice=[1.8999999999999999,1.9099999999999999] cells=400 unconstrained=9.4012820196756657 right_end_target=9.4351398219296261 deficit=0.033857802253960401 flagged=9.4885286384905534 sampled_nonalt=9.6043703368634219 PASS=True
gate3 PASS=True seconds=34.313
gate4 chains=20000 violations=0 max_path_bound_minus_reference=-0.031057071749245324 max_global_DP_minus_reference=-1.1089914527364879 PASS=True seconds=88.484
```

## Rerun

Run from this directory. No network, git commands, or writes to o1dp are needed. Python requires the existing NumPy/SciPy environment. Each `gates` invocation starts the per-n six-hour budget. The full run retains that deadline and has six worker processes at most. The bottom 0.005 is capped at 5,400 seconds and stops after a refined leaf fails; the controller can terminate native calls.

```sh
clang -O2 -std=c11 -D_DARWIN_C_SOURCE -shared -fPIC src/kernel.c -o src/kernel.dylib
../.venv/bin/python src/driver.py regression
../.venv/bin/python src/regression_target.py
../.venv/bin/python src/driver.py gates --n 8
../.venv/bin/python src/driver.py run --n 8
../.venv/bin/python src/driver.py verify --n 8
../.venv/bin/python src/driver.py gates --n 10
../.venv/bin/python src/driver.py run --n 10
../.venv/bin/python src/driver.py verify --n 10
../.venv/bin/python src/report.py
```

The reference loader executes exactly the first 29 lines of `../runs/openmath-2026-10-27/m4check.py`, dropping lines beginning `from targets`, `sys.path`, `import numpy`, or `from scipy`. The C kernel and Python driver were copied from o1dp, then parameterized. The three gap lower-bound candidates are unchanged. The backward pass conditions on the flag already set in the prefix and accepts only terminal flag 1; adding V and W shares no vertex cost.

Initial slices have width 0.001. Each starts with 200 uniform tilt cells, augmented by geometric endpoint cells when 1.99 < Hb < 2. Binding cells are bisected, with at most seven rounds and 6,400 cells per attempt. Stalled attempts split H until another bisection would be narrower than 1e-4. Saved leaf grids, bounds, targets, margins, histories, source hashes, and failed parent attempts are in each certificate. Verification checks the entire leaf coverage, skips explicitly unproved leaves, and exactly replays every claimed proof from its saved grid and trial tilt.

## Premises and limitations

- The SPEC vertex reduction, role displacement table, facet representation, interiority/nonnegative-numerator argument, correlated derivative argument, and near-upright pair lemma are assumed. The certified statement excludes exactly the two alternating role patterns. This does not establish O2 or unconstrained global optimality.
- IEEE-754 binary64 round-to-nearest, functioning nextafter, no fast-math or reassociation, and conventional libm behavior are assumed. Every bound operation is outward padded; all DP additions and reported margins round downward. System sin/cos/sqrt error is assumed at most eight ulps, padded by eight nextafter steps. This accuracy assumption has not been formally verified.
- Adjacent binary64 values enclose pi/4; nextafter(binary64 pi/2, +infinity) encloses the physical upper tilt endpoint. Lower H endpoints are the binary64 predecessors of the specified H0 values. The extended endpoints only enclose the physical domain.
- F_n is bounded for the entire H slice by evaluating the fixed Morandi chain (0, phi, ..., phi, 0) with interval H, upper-bounding every eligible facet ratio and taking their minimum, then summing upward from 1. The scalar optimizer merely chooses phi; neither global minimizer certification nor monotonicity is required for this upper bound.
- H=2 is included conservatively in interval calculations. At H=2 the closed-section kappa differs from the physical packing constraint for exactly upright touching layers. The packing statement is therefore only for H<2; the chain bound itself includes 2.
- Random gates, local-search witnesses, and replay are numerical evidence and reproducibility checks, not an independent formal proof of the interval code. Local search does not certify the non-alternating minimum.
- Worker storage is O(n times number of cells), with no full cell-pair matrix. Certificates record per-worker peak RSS. Source hashes guard replay against changed code.

## Replay results

n=8: replay PASS n=8 proved=145 unproved=0 coverage=[1.8549999999999998,2]
n=10: replay PASS n=10 proved=150 unproved=0 coverage=[1.8499999999999999,2] workers=6 seconds=159.085

The serial `driver.py verify` and the six-worker `verify_parallel.py --n N` replay the same saved grids; n=8 used the serial mode and n=10 the parallel mode. Runtime/compiler versions and source plus binary hashes are recorded in `environment.json`.

## Failures

The prior monotonicity claim and its correct rejection are retained in `README-attempt1.md` and `math-check.py`. They are superseded only in the target definition by the current SPEC. Consult the current gate logs and unproved-leaf list above for this attempt; no failed slice is called proved.

Both current runs proved every leaf. No gate failed and no H-slice splitting was needed. Coarse tilt grids were refined in place, using at most three rounds. Peak measured worker RSS stayed below 75 MiB; six simultaneous workers remain well below 2 GB.

## n = 6: extension to [1.862, 1.87]

All 16 slices are proved; none are unproved. The exact closed interval is
[1.8619999999999999, 1.8700000000000001], with the lower endpoint stored as
`nextafter(1.862, -infinity)` and the upper endpoint as binary64 `1.87`.
There are no gaps or overlaps in the saved leaf coverage. This extends the
n = 6 computation down to the requested lower endpoint; it does not establish
optimality or O2. The chain statement and arithmetic premises above apply.

Minimum positive margin: `0.00020493122752718304`. Maximum cells: 310; maximum refinement rounds: 4. The initial H width was 0.0005; all slices closed without H-bisection. The fallback bisects H only while both children remain at least 1e-4 wide.

Gates 3 and 4 passed (`gates-n6.log`). Gate 3 used 300 random non-alternating patterns with L-BFGS-B on each of [nextafter(1.862, -infinity), 1.867], [1.867, 1.87], and the lower-endpoint point slice, at 50, 100, 200, and 400 cells. Gate 4 checked 20,000 full chains over the requested range, with zero violations. Gates 1, 2, the lemma gate, and gate 5 were not rerun for this extension.

The full run took 18.144 seconds; gates through run took 46.750 seconds; gates through successful replay took 82.129 seconds. At most six workers were used, with maximum measured per-worker RSS 77856768 bytes. The two-hour budget covers gates, run, and replay; the bottom 0.005 has a 30-minute allowance. Neither limit was reached.

The range runner imports the existing DP and refinement functions. `src/driver.py`, `src/kernel.c`, and `SPEC.md` are unchanged (their hashes match the n = 8 certificate). The dynamic library was rebuilt from the existing source. `environment-n6.json` records compiler/runtime versions and source/binary hashes; `certificate-n6.json` records the grids, bounds, trial tilts, histories, and source hashes. Replay recomputed every claimed D and target exactly and checked contiguous coverage: PASS, 16 proved / 0 unproved.

Rerun from this directory (start with gates to reset the two-hour budget):

```sh
clang -O2 -std=c11 -D_DARWIN_C_SOURCE -shared -fPIC src/kernel.c -o src/kernel.dylib
../.venv/bin/python src/run_n6.py gates
../.venv/bin/python src/run_n6.py run
../.venv/bin/python src/run_n6.py verify
```

The results are in `gates-n6.log`, `run-n6.log`, `certificate-n6.json`,
`verify-n6.log`, and the `6` entry in `summary.json`. Existing n = 8 and n = 10
results are retained.
