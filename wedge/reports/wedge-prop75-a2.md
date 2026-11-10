# Proposition 7.5 case A2

Floating point experiment, not a certificate. Comparison tolerance 2e-7; geometry epsilon unchanged.

Parameters: `{'alpha': 0.03, 'L': 320.0, 'R': 1.0, 'zeta': 0.003125, 'delta': 0.03125, 'tau': 0.08, 'm': 2243, 'squares': 715290, 'w': 2242.020883682307, 'W': 2316.6827783383196, 'window_width': 1.0}`.

|G|/L = 0.78567192913; |G| = 251.415017321. Majority target PASS.
|X-prime| = 251.61783042; sum Delta = 66.1331308393; positive drops = 0.784159647691; sum Theta = 66.06; sum theta_i |Y_i| = 64.1669833181; skips = 0.
Literal hypothesis ratio (4250W+1350W/tau+0.01)/(L/4) = 611749.04628. The literal small-waste hypothesis is not met.

| Line | lhs <= rhs | lhs | rhs | lhs/rhs | Result |
|---|---|---:|---:|---:|---|
| P1 | L-\|G\| <= death bound | 68.5849826785 | 48869264.8777 | 1.40343798603e-06 | PASS |
| P2 | cos(zeta-prime)\|G\| <= \|X-prime\| | 251.413789718 | 251.61783042 | 0.999189084887 | PASS |
| P3 | sum Delta <= L-\|X-prime\| | 66.1331308393 | 68.3821695804 | 0.967110743123 | PASS |
| P3 | -min Delta <= 0 | -0 | 0 | 0 | PASS |
| P4 | skip count <= 2 zeta sum Delta | 0 | 0.413332067746 | 0 | PASS |
| P5 | sin(zeta-prime)\|G\|-delta <= positive drops | 0.754418092869 | 0.784159647691 | 0.96207206669 | PASS |
| P6 | positive drops <= tau sum Theta + delta skips | 0.784159647691 | 5.2848 | 0.148380193705 | PASS |
| P7 | 0.7 sum Theta <= sum theta Y | 46.242 | 64.1669833181 | 0.720650989166 | PASS |
| P7 | sum theta Y <= 14851 W | 64.1669833181 | 34405055.9411 | 1.86504516743e-06 | PASS |
| P8 | 0.53 L <= \|X-prime\| | 169.6 | 251.61783042 | 0.674038082743 | PASS |
| P8 | sum Delta <= 0.47 L | 66.1331308393 | 150.4 | 0.439714965687 | PASS |
| P8 | skips <= 0.94 R | 0 | 0.94 | 0 | PASS |
| P8 | 0.499 R <= sin(zeta-prime)(3L/4)-delta | 0.499 | 0.718746337917 | 0.694264406892 | PASS |
| P8 | 0.4696 R <= tau 21216 W | 0.4696 | 3932059.34602 | 1.19428512816e-07 | PASS |
| P8 | 0.47 R <= 21300 tau W | 0.47 | 3947627.45429 | 1.19058853816e-07 | PASS |
| P6-boundary | drop <= tau Theta or skip | 0.00213667485518 | 0.0144 | 0.148380198276 | PASS |

| Audit check | Comparisons | Failures | Result |
|---|---:|---:|---|
| 1 | 1397332 | 0 | PASS |
| 2 | 839617 | 0 | PASS |
| 3 | 558930 | 0 | PASS |
| 4 | 1 | 0 | PASS |
| 5 | 317 | 0 | PASS |
| 6 | 626839995 | 0 | PASS |
| 7 | 1 | 0 | PASS |
| 8 | 1 | 0 | PASS |

Largest non-skip positive drop/(tau Theta): 0.148380198276. Witness: `{'k': 239259, 'N': 2243, 'Np': 2243, 'D': 0.08999325020249138, 'Dp': 0.08729345269641664, 'drop': 0.0021366748551792103, 'Delta': 0.18019926659059138, 'resid': 5.726357148877481e-11, 'Theta': 0.18, 'angles': '1-2043:0; 2044-2049:0.03; 2050-2243:0', 'aligned': '1-2243:1', 'minY': 0.9700045027987017, 'maxY': 1.0, 'cost': 0.17480329531671712, 'skip': False, 'coordinates': [300.12296282806676, 300.12386296312957]}`.
P-line failures (with witnesses): `[]`.
Audit failure witnesses: `[]`.
Ending measures by kind: `{'gap': 68.5839395908443, 'lateral': 0.0010430876677587353, 'arrival': 251.41501732148794}`; gap emitters: `{'layer': 67.58393959084428, 'floor': 1.0000000000000142}`.
Native paths: 280076; arrivals: 279466; boundaries: 279465. Independent validation: 1079898 comparisons, PASS. Total measured run seconds: 5471.307450; peak RSS GB: 4.302520.

Windows own whole native affine pieces by their left endpoint. Full-floor flow states are pruned against each window, never clipped; artificial cuts therefore introduce no boundaries and preserve the original audit interior representatives exactly. Both the last complete path and the last arriving path (including complete entry chains and affine limits) are checkpointed. Across empty-arrival windows the latter is retained. Cross-window ordering and arrival boundaries use the same audit calculations as interior boundaries. Global checks are evaluated once on the totals. Every native Delta, drop, Theta and tube cost is stored in the JSON-lines checkpoint.
Checkpoint: `runs/k2c-exponent-2026-11-09/work/wedge-prop75-a2.jsonl`. No formal or interval-arithmetic certificate is claimed.
