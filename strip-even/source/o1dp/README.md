# O1 interval DP results

**76/76 slices prove, including the final interval closed at H=2.**
The saved intervals cover [1.87, 2] without gaps; the stored lower endpoint
is the binary64 predecessor of 1.87. Margins are D minus F6_ub, rounded down.
Under the premises below, this certifies the requested non-Morandi inequality
throughout [1.87, 2), with the stronger computation also including H=2.

Only the previously unproved interval [1.9999990234375, 2]
was re-proved, starting from its saved 800-cell grid:
**800 cells, D=5.4786381746324899,
F6_ub=5.3137133817962976, margin=0.1649247928361923, PROVED**.
It required 1 round(s) and no H-splitting.
All 76 pre-lemma saved grids were separately replayed with the new kernel.
All 75 prior proofs survived and every D was at least its pre-lemma value.

Smallest positive current margin: 0.0095324283613971144.
Largest current grid: 3204 cells.
The update used at most six workers and finished in 1088.769
seconds from task start, within its two-hour hard stop.

## Gates

The new pointwise lemma gate and gates 1, 2 and 4 passed with zero violations.
The lemma gate used 200,000 triples and both normals in both mirrored cases
(800,000 terms), with exactly 50,000 H=2 triples and at least 50,000 W<=1e-3 triples.
Gate 2 used 25,000 boxes with both cells wholly in the same corner region
[0,0.3] or [pi/2-0.3,pi/2], widths 1e-8 through 0.3; exactly 12,500
of those slices included H=2. The other 25,000 boxes used the original general
distribution. All boxes had 64 interior samples. Gate 3 remains historical
from the plain kernel and was not rerun or relabeled.

```
lemma_gate triples=200000 terms=800000 H2=50000 W_le_1e-3=50000 violations=0 min_term_minus_lemma=1.2431738462548303e-05 PASS=True
gate1 samples=100000 max_abs_error=6.106226635438361e-15 PASS=True
gate2 boxes=50000 interior_samples=3200000 violations=0 max_G_minus_reference=-9.6082741762870683e-10 PASS=True
gate4 chains=20000 violations=0 max_path_bound_minus_reference=-0.0093334531982867119 max_global_DP_minus_reference=-0.4433688928379107 PASS=True seconds=42.153
```

## Bound and arithmetic assumptions

The original plain term bound, support bound, target and DP recursion are
unchanged. Each eligible normal now also receives exactly the SPEC's
correlated ratio lower bound. The new premise is the **Near-upright pair
lemma (addendum 2)**, proved in [SPEC.md](SPEC.md#certified-bounds-all-in-interval-arithmetic-with-outward-rounding).
Its candidate is nonzero only for C->F sine normals with both cells inside
[0,1], or F->C cosine normals with both inside [pi/2-1,pi/2]. It supplies
1-3W/4-W^2/4 with upward-rounded penalties and downward-rounded subtractions;
the upper-corner width and eligibility threshold use an upward enclosure
of pi/2. Each term is `max(plain, ratio, lemma, 0)`.
For its smallest-n_x face, N(e)>=a=max(A,0) follows from the face interval
and pointwise interiority. An outward interval encloses the one-sided
N derivative throughout the box, including both derivatives of |sin(delta)|
at delta=0. Thus N>=a+x B and n_x<=c+x. If a+x B is negative, nonnegativity
already supplies the lower bound; otherwise division gives min(a/c,B),
or B when c=0. The physical endpoint faces have exact sin/cos values.

- IEEE-754 binary64, ordinary round-to-nearest arithmetic, functioning
  nextafter, and no fast-math or reassociation. DP sums and margins round down.
- System libm sin/cos/sqrt errors are assumed at most eight ulps; results are
  padded outward. This remains an unverified libm accuracy assumption.
- Adjacent floats bracket pi/4; the float above binary64 pi/2 encloses the
  physical tilt endpoint. The extra width is only an enclosure device.
- The facet support is (1+cos(delta)+|sin(delta)|)/2. The other four signed
  normals have nonpositive x component on the physical domain.
- Numerator clipping uses the SPEC's vertical-segment/interiority argument
  and |dy|<=1. The supplied vertex reduction and F6 monotonicity are premises.
- The target evaluates L at one trial angle with outward arithmetic at Ha.
  The numerical minimizer need not find a global minimum for that upper bound.
- Gates compare against the unmodified hull reference definitions parsed
  from ../runs/openmath-2026-10-27/m4check.py. Random tests are sampled evidence;
  replay is reproducibility evidence, not an independent formal verification.

## Artifacts and replay

`certificate.before-ratio.json` and `certificate.before-lemma.json` are
untouched. `certificate.json` contains the current grids, bounds and source
hashes, with all 76 pre-lemma-grid replay outcomes under
`lemma_update.saved_grid_replay`. Prior update provenance and historical
refinement records remain preserved; `pre_lemma_D` records the preceding bound.
`lemma_update.final_slice` records the new final-slice proof and its refinement.
`run.log` appends that result and the 76 replay outcomes. `gates.log` appends
the new gate run. Console records are `lemma-gates-console.log` and
`lemma-replay-console.log`; `verification.log` records coverage and replay.

From this directory:

```sh
clang -O2 -std=c11 -D_DARWIN_C_SOURCE -shared -fPIC src/kernel.c -o src/kernel.dylib
../.venv/bin/python src/driver.py gates
../.venv/bin/python src/driver.py verify
../.venv/bin/python src/report.py
```

`verify` replays all current grids and checks exact saved values and coverage.
The one-time lemma migration is `src/replay_lemma.py`; it reads
`certificate.before-lemma.json`. Its two-hour watchdog terminates native
worker calls as well as Python processes. At most six workers run; no full
NxN matrix is stored and worker memory remains O(N). No git commits were made,
and all writes stayed inside o1dp.

## Endpoint outcome

The joint lemma resolves the shared-corner collapse of the one-dimensional
ratio bound. The final slice [1.9999990234375, 2] now proves with margin
0.1649247928361923. Its saved 800-cell grid was the starting partition;
1 solve round(s) yielded the 800-cell certificate above.
The kernel's support, plain bound, ratio bound, target and DP recursion
are unchanged. The only additional mathematical premise is SPEC addendum 2.

## Current per-slice bounds

| Ha | Hb | Cells | D | Margin |
|---|---|---:|---:|---:|
| 1.8699999999999999 | 1.8720000000000001 | 200 | 5.96575772546742 | 0.00953242836139711 |
| 1.8720000000000001 | 1.8740000000000001 | 200 | 5.95873060595564 | 0.0123409068058873 |
| 1.8740000000000001 | 1.8760000000000001 | 200 | 5.95079222631243 | 0.0142388004376999 |
| 1.8760000000000001 | 1.8780000000000001 | 200 | 5.94285384666922 | 0.0161373876439317 |
| 1.8780000000000001 | 1.8800000000000001 | 200 | 5.93491546702602 | 0.0180366873419988 |
| 1.8800000000000001 | 1.8820000000000001 | 200 | 5.92697708738281 | 0.0199367191412687 |
| 1.8820000000000001 | 1.8840000000000001 | 200 | 5.9190387077396 | 0.0218375033749316 |
| 1.8840000000000001 | 1.8860000000000001 | 200 | 5.91110032809639 | 0.0237390611336323 |
| 1.8860000000000001 | 1.8880000000000001 | 200 | 5.90316194845319 | 0.0256414143009991 |
| 1.8880000000000001 | 1.8900000000000001 | 200 | 5.89522356880998 | 0.02754458559121 |
| 1.8900000000000001 | 1.8920000000000001 | 200 | 5.88728518916677 | 0.0294485985886839 |
| 1.8920000000000001 | 1.8940000000000001 | 200 | 5.87934680952356 | 0.0313534777900974 |
| 1.8940000000000001 | 1.8960000000000001 | 200 | 5.87140842988036 | 0.0332592486488368 |
| 1.8960000000000001 | 1.8980000000000001 | 200 | 5.86347005023715 | 0.0351659376220947 |
| 1.8980000000000001 | 1.9000000000000001 | 200 | 5.85553167059394 | 0.0370735722207556 |
| 1.9000000000000001 | 1.9020000000000001 | 200 | 5.84759322603557 | 0.0389821161471504 |
| 1.9020000000000001 | 1.9040000000000001 | 200 | 5.83965293257312 | 0.0408898151925596 |
| 1.9040000000000001 | 1.9060000000000001 | 200 | 5.83171263911066 | 0.0427985492635887 |
| 1.9060000000000001 | 1.9080000000000001 | 200 | 5.8237723456482 | 0.044708350648329 |
| 1.9080000000000001 | 1.9100000000000001 | 200 | 5.81583205218575 | 0.0466192529877185 |
| 1.9100000000000001 | 1.9120000000000001 | 200 | 5.80789175872329 | 0.0485312913470475 |
| 1.9120000000000001 | 1.9140000000000001 | 200 | 5.79995146526083 | 0.0504445022920992 |
| 1.9140000000000001 | 1.9160000000000001 | 200 | 5.79201117179838 | 0.0523589239701891 |
| 1.9160000000000001 | 1.9180000000000001 | 200 | 5.78407087833592 | 0.0542745961965583 |
| 1.9180000000000001 | 1.9200000000000002 | 200 | 5.77613058487346 | 0.0561915605464849 |
| 1.9200000000000002 | 1.9220000000000002 | 200 | 5.768190291411 | 0.0581098604535795 |
| 1.9220000000000002 | 1.9240000000000002 | 200 | 5.76024920815995 | 0.0600287515261586 |
| 1.9240000000000002 | 1.9260000000000002 | 200 | 5.75230508473981 | 0.0619460308561681 |
| 1.9260000000000002 | 1.9280000000000002 | 200 | 5.74436096131967 | 0.0638647882806058 |
| 1.9280000000000002 | 1.9300000000000002 | 200 | 5.73641683789954 | 0.0657850757913252 |
| 1.9300000000000002 | 1.9320000000000002 | 200 | 5.7284727144794 | 0.0677069478417191 |
| 1.9320000000000002 | 1.9340000000000002 | 200 | 5.72052859105926 | 0.0696304614942402 |
| 1.9340000000000002 | 1.9360000000000002 | 200 | 5.71258446763912 | 0.0715556765787122 |
| 1.9360000000000002 | 1.9380000000000002 | 200 | 5.70464034421899 | 0.0734826558623585 |
| 1.9380000000000002 | 1.9400000000000002 | 200 | 5.69669622079885 | 0.0754114652325697 |
| 1.9400000000000002 | 1.9420000000000002 | 200 | 5.68875209737871 | 0.0773421738935864 |
| 1.9420000000000002 | 1.9440000000000002 | 200 | 5.68080797395858 | 0.0792748545783093 |
| 1.9440000000000002 | 1.9460000000000002 | 200 | 5.67286385053844 | 0.0812095837766646 |
| 1.9460000000000002 | 1.9480000000000002 | 200 | 5.6649197271183 | 0.083146441982044 |
| 1.9480000000000002 | 1.9500000000000002 | 200 | 5.65697560369817 | 0.0850855139575453 |
| 1.9500000000000002 | 1.9520000000000002 | 200 | 5.64903148027803 | 0.0870268890239076 |
| 1.9520000000000002 | 1.9540000000000002 | 200 | 5.64108735685789 | 0.0889706613712588 |
| 1.9540000000000002 | 1.9560000000000002 | 200 | 5.63314323343776 | 0.0909169303970287 |
| 1.9560000000000002 | 1.9580000000000002 | 200 | 5.62519911001762 | 0.0928658010726799 |
| 1.9580000000000002 | 1.9600000000000002 | 200 | 5.61725498659748 | 0.0948173843421811 |
| 1.9600000000000002 | 1.9620000000000002 | 200 | 5.60931086317735 | 0.0967717975555429 |
| 1.9620000000000002 | 1.9640000000000002 | 200 | 5.60136673975721 | 0.0987291649411155 |
| 1.9640000000000002 | 1.9660000000000002 | 200 | 5.59342261633707 | 0.100689618120843 |
| 1.9660000000000002 | 1.9680000000000002 | 200 | 5.58547849291694 | 0.102653296673154 |
| 1.9680000000000002 | 1.9700000000000002 | 200 | 5.5775343694968 | 0.104620348748832 |
| 1.9700000000000002 | 1.9720000000000002 | 200 | 5.56959024607666 | 0.106590931745888 |
| 1.9720000000000002 | 1.9740000000000002 | 200 | 5.56164612265653 | 0.108565213050281 |
| 1.9740000000000002 | 1.9760000000000002 | 200 | 5.55370199923639 | 0.11054337085026 |
| 1.9760000000000002 | 1.9780000000000002 | 200 | 5.54575724681725 | 0.112524966034265 |
| 1.9780000000000002 | 1.9800000000000002 | 200 | 5.53780737265578 | 0.11450570843519 |
| 1.9800000000000002 | 1.9820000000000002 | 200 | 5.52985749849432 | 0.116490936154328 |
| 1.9820000000000002 | 1.9840000000000002 | 200 | 5.52190762433286 | 0.118480880545222 |
| 1.9840000000000002 | 1.9860000000000002 | 200 | 5.51395775017139 | 0.120475789301166 |
| 1.9860000000000002 | 1.9880000000000002 | 200 | 5.50600787600993 | 0.122475927951744 |
| 1.9880000000000002 | 1.9900000000000002 | 200 | 5.49805800184846 | 0.124481581531683 |
| 1.9900000000000002 | 1.992 | 270 | 5.5038241183355 | 0.140209047094884 |
| 1.992 | 1.9940000000000002 | 400 | 5.49585231279584 | 0.142204741833154 |
| 1.9940000000000002 | 1.996 | 404 | 5.48795447983212 | 0.144280916027677 |
| 1.996 | 1.9980000000000002 | 804 | 5.48664691381702 | 0.15295424819001 |
| 1.9980000000000002 | 1.9990000000000001 | 1604 | 5.48597145601607 | 0.162266995179899 |
| 1.9990000000000001 | 1.9995000000000001 | 3204 | 5.48562825156204 | 0.166920772402397 |
| 1.9995000000000001 | 1.9997500000000001 | 500 | 5.45977883777086 | 0.143570595048592 |
| 1.9997500000000001 | 1.9998750000000001 | 518 | 5.45928065237383 | 0.144322217619243 |
| 1.9998750000000001 | 1.9999375000000001 | 536 | 5.45903155965819 | 0.144698076751607 |
| 1.9999375000000001 | 1.9999687500000001 | 554 | 5.45890701329609 | 0.144886018333443 |
| 1.9999687500000001 | 1.9999843749999999 | 572 | 5.45884474011397 | 0.144979992135044 |
| 1.9999843749999999 | 1.9999921875 | 590 | 5.45881360352264 | 0.145026979789362 |
| 1.9999921875 | 1.9999960937500001 | 608 | 5.45879803522691 | 0.145050473805005 |
| 1.9999960937500001 | 1.999998046875 | 626 | 5.45879025107902 | 0.145062220859965 |
| 1.999998046875 | 1.9999990234375 | 644 | 5.45878635900508 | 0.145068094399229 |
| 1.9999990234375 | 2 | 800 | 5.47863817463249 | 0.164924792836192 |

## Scope at H = 2 (added 2026-10-30 after an independent check)

The inequality O1 is only meaningful for H < 2. At H = 2 exactly two upright
squares stack (F at y = 1/2, C at y = 3/2) and six squares fit in length 3, so
no packing lower bound of the form "non-Morandi > F6" can hold there (the
inequality for the closed-section chain itself is what the last slice bounds). The chain function Phi
uses the closed-section kappa = max{x : (x, dy) in Delta}; for every H < 2 all
displacements satisfy |dy| < 1, the line meets the interior of Delta, and the
closed section equals the packing constraint, so the vertex reduction applies.
At |dy| = 1 (H = 2, both squares upright, F->C or C->F) the closed section is 1
while the packing constraint is 0: Phi_closed is no longer a packing bound.
Including H = 2 in the last slice is therefore only a conservative device, and
the certified statement is: for every H in [1.87, 2), every pattern other than
FCFCFC/CFCFCF has Phi > F6(H). A Nelder-Mead search over the 62 patterns at
H = 2 with tilts kept in [1e-7, pi/2 - 1e-7] found nothing below 5.6116
(certified D on the last slice 5.4786); evaluating exactly at tilt pi/2 with
dy = 1 gives the open-section value 0 in floating point and produces spurious
chain values near 4.8, which is this degenerate case, not a counterexample.

## Relation to the printed FI-O1 formula (referee finding, 2026-10-30)

The chain certified here is the SPEC chain with the four actual role
displacements (F->F: h(t')-h(t); F->C: H-h(t')-h(t); C->F: h(t')+h(t)-H;
C->C: h(t)-h(t')). The formula printed for FI-O1 in proof-F6.md section 5,
dy = (sigma_{i+1}-sigma_i)(H-h_i-h_{i+1}), sets dy = 0 for same-role pairs
with unequal tilts and is a misprint of the same chain; the corrected form is
dy = (sigma_{i+1}-sigma_i) H + (1-2 sigma_{i+1}) h_{i+1} - (1-2 sigma_i) h_i,
which is the SPEC chain. The vertex reduction (proof-F6.md section 2) is
stated for the true displacements, so the SPEC chain is the one it produces.
Blind referee report: squarepack docs/o1dp-review-codex-2026-10-30.md.
