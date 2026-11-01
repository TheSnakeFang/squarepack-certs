# O2n implementation stopped: specification issue

No certification run was started. The required document/source review found a
false obligation in (C0). Per the instruction to stop if the fixed mathematics
looks wrong, the mathematics and implementation requirements have not been
changed.

## Issues with the spec

`LEMMAS.md` §11 defines

    κ0^L = min_{|z|∞ = 1} B1_L(z) > 0.

`SPEC.md`, per-H-cell check 6, likewise requires minimisation on the faces of the
entire cube. At the exact rational vertex

    (x1, Y2, x3, Y4, x5) = (-1, 1, -1, 1, -1),

all four pair sums are zero. Substitution in the stated formula gives

    B1_L = k + k - k - k - k/2 = -k/2.

Thus the stated minimum is at most -k/2, strictly negative throughout the
requested five-block range. At H=1.846936 the value is exactly
`-19133/250000 = -0.076532`; at H=1.86 it is exactly `-7/100 = -0.07`.
This disproves the positive lower bound as written; it does not claim that
this vertex is a global minimiser.

The separate block domain requires x1 >= 0. The counterexample has x1=-1,
so it does not disprove the intended bound on that restricted domain or O2n.
Restricting (C0) to the appropriate domain may be the intended correction,
but doing so would change the fixed mathematics. No such change was made.
`SPEC.md` also asks to consider k=0: at that endpoint the same vertex gives
zero, so a uniformly strictly positive minimum over the full stated k interval
is impossible as well.

## Verification and status

`check_spec_issue.py` uses only exact `fractions.Fraction` arithmetic. It checks
unit sup-norm, the four vanishing pair sums, both rational endpoints, and the
affine identity B1_L=-k/2 for every k. Reproduce with:

```sh
../.venv/bin/python check_spec_issue.py
```

Its output is saved in `spec-issue.log`. This is a diagnostic counterexample,
not an H-cell certificate or a replacement for any requested gate.

G1–G6: **not run**, 0 gate trials. No gate has passed or failed. `gates.log`
records the stop, rather than implying a successful gate result.

| Requested run | Requested H range | Certified cells | Outer / inner boxes | Minimum margin | Exact certified H range | Run wall time |
|---|---|---:|---:|---|---|---:|
| n=8 | [1.852049, 2] | 0 | 0 / 0 | N/A | empty | 0 s |
| n=6 | [1.861098, 2] | 0 | 0 / 0 | N/A | empty | 0 s |
| n=10 even-star | [1.86, 2] | 0 | 0 / 0 | N/A | empty | 0 s |
| n=10 five-block | [1.846936, 1.86] | 0 | 0 / 0 | N/A | empty | 0 s |

Run wall times exclude document review and the separately timed diagnostic.
No certificates exist and no H-cell checkpoints were produced.

## Deviations, assumptions, and remaining work

The only departure from the requested implementation/run sequence is the
explicitly required stop on a specification issue: no kernel was copied or
built, no driver modes were implemented, and no gates, searches, certificate
replays, or numerical reports were run. The exact diagnostic and this report
are the only new implementation work. No binary64 or libm assumption enters
the counterexample. No worker processes were started. No network or git
commands were used, and no files outside o2n were written. `SPEC.md` and
`LEMMAS.md` remain unchanged.

The intended domain of (C0), and its intended treatment of k=0, require a
specification correction before implementation resumes. The positivity of
the restricted-domain minimum and all requested certificates remain unchecked.
