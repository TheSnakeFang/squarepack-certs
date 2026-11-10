# Checks on the last step of the wedge proof (Proposition 7.5)

2026-11-10. Follow-up to `notes/wedge-lower-bound.md` and `note/` (note v0.1,
doi:10.5281/zenodo.24099178). Floating point experiments and exact arithmetic on
constants. Not a certificate, and not a human read of the proof.

## Why

Proposition 7.5 says: with delta = 1/32, 0 < tau <= 0.08, R >= 1, zeta <= 1, if
`4250 W + 1350 W/tau + 0.01 <= L/4` then `0.47 R <= 21300 tau W`. Its hypothesis needs
W below about L/84500 at tau = 0.08. No packing we can build meets that (a staircase
would need on the order of 1e18 squares), so the published simulators never ran this
step. The note's "Checks" section says so, with the looser figure L/34000.

The hypothesis is used in one place only: Corollary 6.5, to get |G| >= 3L/4 for the set
G of arriving floor points. Every other line of the proof is an inequality that holds
for every packing. So the test is to build a packing at the proposition's parameters in
which at least 3/4 of the floor paths arrive, and check each line with measured values.

## Results

| Check | Tool | Outcome |
|---|---|---|
| Numerical constants of Sections 5 to 7 and the proof of Theorem 1.5, exact rationals | `tools/wedge_constants.py` | 70 claims, 70 PASS |
| Lemma 7.4 near its bound: two sheared stacks, tilts 0.07999 and 0.0799, tau = 0.08 | `tools/wedge_prop75_check.py` (case C2) | largest drop/(tau Theta) = 0.996985, no violation |
| Every proof line on a packing with majority arrival | `tools/wedge_prop75_a2.py` | all lines PASS, see below |

The first attempt at the third row (cases A and B of `wedge_prop75_check.py`, tilt 0.07)
had no arriving paths at all and passed vacuously. A path's gaps add up to about
`sin(alpha) + (1 - cos(alpha))/2` whatever its entry point, and that has to stay below
delta = 1/32, so the tilt must be about 0.03 or less. That was a specification error.

### Majority-arrival run

One tilt alpha = 0.03, L = 320, R = 1 (zeta = 1/320), delta = 1/32, tau = 0.08,
715,290 squares, W = 2316.68. Independent overlap validation: 1,079,898 comparisons,
PASS. Full floor, 320 windows with exact carry-over across window cuts (the windowed
aggregation reproduces the published small run with all differences zero).
279,466 arriving itinerary pieces, 279,465 boundaries. Measured |G|/L = 0.785672.

| Line | Statement | lhs | rhs | lhs/rhs |
|---|---|---:|---:|---:|
| P1 (Cor 6.5) | L - \|G\| <= W/delta + 1350W/tau + 134000 delta W + 0.01 | 68.585 | 4.89e7 | 1.4e-6 |
| P2 | cos(zeta') \|G\| <= \|X'\| | 251.4138 | 251.6178 | 0.99919 |
| P3 | sum Delta <= L - \|X'\|, every Delta >= 0 | 66.1331 | 68.3822 | 0.96711 |
| P4 | #{Delta >= 1/(2 zeta)} <= 2 zeta sum Delta | 0 | 0.4133 | 0 |
| P5 (Lemma 7.2) | sin(zeta') \|G\| - delta <= sum of positive drops | 0.754418 | 0.784160 | 0.96207 |
| P6 (Lemma 7.4) | positive drops <= tau sum Theta + delta skips | 0.784160 | 5.2848 | 0.14838 |
| P6 per boundary | drop <= tau Theta unless skip | 0.0021367 | 0.0144 | 0.14838 |
| P7 (Lemma 7.3) | 0.7 sum Theta <= sum theta_i \|Y_i\| | 46.242 | 64.167 | 0.72065 |
| P7 (Lemma 7.1) | sum theta_i \|Y_i\| <= 14851 W | 64.167 | 3.44e7 | 1.9e-6 |
| P8 | 0.53 L <= \|X'\| | 169.6 | 251.618 | 0.67404 |
| P8 | sum Delta <= 0.47 L | 66.133 | 150.4 | 0.43971 |
| P8 | skips <= 0.94 R | 0 | 0.94 | 0 |
| P8 | 0.499 R <= sin(zeta')(3L/4) - delta | 0.499 | 0.718746 | 0.69426 |
| P8 | 0.4696 R <= 21216 tau W | 0.4696 | 3.93e6 | 1.2e-7 |
| P8 | 0.47 R <= 21300 tau W | 0.47 | 3.95e6 | 1.2e-7 |

The staircase audit's checks 1 to 8 also pass (about 630 million comparisons, 0
failures). The P-lines were recomputed separately from the 279,465 stored boundary
records and agree.

## What this does and does not show

- The chain from "3/4 of the paths arrive" to the conclusion has now been run on a
  real packing, and P2, P3 and P5 hold with only a few percent to spare, so they are
  real tests of the geometry (arrival abscissas, order, the height bookkeeping of
  Lemma 7.2).
- The lines that carry W (P1, both ends of the conclusion, Lemma 7.1's upper bound)
  are slack by a factor of about a million here, because this packing wastes far more
  than the theorem's bound. They are not tested in any sharp sense.
- No skips occur (no Delta reaches 1/(2 zeta) = 160), so the skip branch of Lemma 7.4
  is exercised only by the near-tight sheared stacks, not here.
- The literal hypothesis is still not met: (4250W + 1350W/tau + 0.01)/(L/4) = 611,749.
  Corollary 6.5 itself, which turns small waste into |G| >= 3L/4, holds trivially.
- Three premise groups in the constants audit are geometry, not arithmetic: the
  local-rectangle constants from Corollary 2.3, the wall counts, and the
  packing-dependent measure statements.

## Reproduce

```
python3 -I tools/wedge_constants.py
python3 -I tools/wedge_prop75_check.py
python3 -I tools/wedge_prop75_a2.py --selftest
python3 -I tools/wedge_prop75_a2.py --run --alpha 0.03 --L 320 --width 1
```

The last command took 97 minutes and 4.3 GB on a 16 GB Mac mini. It is resumable and
writes a 407 MB checkpoint under `runs/k2c-exponent-2026-11-09/work/` (not tracked).
Reports land in `runs/k2c-exponent-2026-11-09/` (not tracked). The reports of the runs
described here are in `reports/`. Run the commands from the `wedge/` folder.
