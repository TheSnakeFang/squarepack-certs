Implemented both n values. All gates passed, all slices proved, and both certificates replayed exactly.

| n | Proved / unproved | Exact proved H range | Minimum margin | Max cells | Run wall |
|---|---:|---|---:|---:|---:|
| 8 | 145 / 0 | [1.8549999999999998, 2) | 0.00012543447209534261 | 464 | 114.7 s |
| 10 | 150 / 0 | [1.8499999999999999, 2) | 0.0002703568496915664 | 464 | 202.8 s |

Elapsed through gates and replay: **605.4 s** for n=8; **767.7 s** for n=10. No H-bisections were needed.

Gate results, for each n:

- **1:** 100,000 points; maximum error `6.11e-15`.
- **2:** 50,000 boxes, 3.2 million samples; zero violations.
- **Lemma:** 800,000 terms; zero violations.
- **5:** 50,000 samples; zero violations; maximum point excess `2.66e-13`.
- **3:** Both slices passed all four refinement levels; 300 optimization starts per slice.
- **4:** 20,000 chains; zero violations.

The three n=6 DP regressions match exactly; point targets differ by at most `2.58e-14`.

[Rerun instructions and assumptions]( /Volumes/Kevin_SSD/GitHub/squarepack/o1n/README.md) and [numerical summary](/Volumes/Kevin_SSD/GitHub/squarepack/o1n/summary.json) are saved. Remaining qualifications: the supplied mathematical premises and the unverified **eight-ulp libm assumption**. H=2 is included computationally; the packing claim excludes it.

