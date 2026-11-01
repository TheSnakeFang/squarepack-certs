# O2n: stopped on a local-parameter specification conflict

The corrected (C0) domain is accepted: the old point with x1 = -1 is
excluded. It is not the reason for this stop. After reading all of LEMMAS.md,
SPEC.md, ../o2cert/SPEC.md, and the reference kernel/driver, a different
mandatory condition was found impossible. No mathematics or input spec was
changed.

## Issues with the spec

SPEC.md, per-H-cell check 2, requires both

    gamma = T^2 (c_x - D'(T)) >= 0

throughout the entire independent parameter rectangle
`[T_lo,T_hi] x [H_a,H_b]`. Here `c_x` is beta or alpha, each a
nonnegative constant multiple of `k = 2-H`.

Every nondegenerate final H-cell `[H_a,2]` has this conflict:

1. The strict derivative bracket at H=2 requires `T_lo < 1 < T_hi`.
   Indeed, `partial_T f_n(T;2) = -(n-2)D'(T)` and D' is positive
   for `T < 1`, zero at 1, and negative for `T > 1`.
2. At the point `(T,H) = (T_lo,2)` of the parameter rectangle,
   `c_x = 0`, so `gamma = -T_lo^2 D'(T_lo) < 0`.
3. By continuity the violation also holds for H strictly below 2.
   Exempting the single endpoint using Theorem 10 does not remove it.

This holds for every positive-width final cell and cannot be repaired by
further finite bisection or tighter outward rounding. It affects n=8 first
in the requested order, and also n=6 and n=10 even-star.

This is a conflict in the requested rectangular verification, not a
counterexample to the local lemma at the true stationary point. At
`T=T_n(H)`, the stationary relation makes the coefficients nonnegative.
The problem is the explicit requirement to check the displayed gamma
formula at *all independent* T and H in the rectangle.

### Exact reproducible witness

`check_local_spec_issue.py` uses fractions.Fraction throughout, enclosing
square roots between rational bounds using integer isqrt at scale 10^80.
No binary64 or libm premise enters its sign checks. Full rational endpoints
are in `local-spec-issue.json`; decimal displays are in
`local-spec-issue.log`.

For n=8, choose

    H-cell = [199999/100000, 2] = [1.99999, 2]
    T-bracket = [9999/10000, 1000001/1000000] = [0.9999, 1.000001].

The bracket width is 0.000101, less than 0.001, and T_lo >= 0.919.
Exact rational enclosures verify the required strict endpoint signs:

| H | Upper bound of derivative at T_lo | Lower bound of derivative at T_hi |
|---|---:|---:|
| 1.99999 | -6.280912679238936e-5 | +1.072798096938569e-5 |
| 2 | -7.280312589226935e-5 | +7.279209694756889e-7 |

Nevertheless, for both sides of blocks j=1 and j=2 at `(T_lo,2)`,

    gamma < -1.213142766585369e-5.

At the strictly interior H=1.999999, all four gammas are also negative;
their upper bounds range from -1.179816099585369e-5 to
-1.113162765585369e-5. These are exact rational sign conclusions; the
numbers printed here are abbreviated decimal displays.

A possible author-side repair is to specify a nonnegative off-stationary
extension using the explicit stationary coefficients of Lemma 18, while
retaining their agreement at T_n(H). That changes the required rectangular
calculation and has not been implemented or assumed valid here. The
specification needs to resolve this requirement before implementation resumes.

## Gates and runs

Per the explicit instruction to stop and report when something in the fixed
mathematics looks wrong, no kernel was copied/built and no certification
search was started. G1-G6 each have **0 trials, not run**; none passed or
failed. The separate diagnostic passed 4 exact derivative sign checks and
8 exact negative-gamma checks. It is not a gate or a certificate.

| Run | Requested H range | Certified cells | Outer / inner boxes | Min margin | Exact certified H range | Search wall time |
|---|---|---:|---:|---|---|---:|
| n=8 | [1.852049, 2] | 0 | 0 / 0 | N/A | empty | 0 s |
| n=6 | [1.861098, 2] | 0 | 0 / 0 | N/A | empty | 0 s |
| n=10 even-star | [1.86, 2] | 0 | 0 / 0 | N/A | empty | 0 s |
| n=10 five-block | [1.846936, 1.86] | 0 | 0 / 0 | N/A | empty | 0 s |

No H-cell certificates or checkpoints exist. Search wall times exclude
reading and diagnostic work. The measured diagnostic wall time is recorded
in `local-spec-issue.json`. No workers were started.

## Reproduce

```sh
../.venv/bin/python check_local_spec_issue.py > local-spec-issue.log
```

This rewrites only the diagnostic JSON and log inside o2n.
`README-attempt1.md`, `check_spec_issue.py`, and `spec-issue.log` are
historical artifacts concerning the old unrestricted (C0) domain. They
remain unchanged and must not be treated as findings against the corrected
SPEC.md. The current issue is recorded in the distinct `local-spec-issue.*`
files.

## Deviations, assumptions, and uncertainty

The required stop prevented all implementation and run deliverables beyond
this diagnostic/report: no new C kernel, driver modes, random gates, H0,
C0 enumeration, searches, certificate replay, or full-range results. In
particular kappa0^L on the corrected domain remains uncomputed; the five-block
stage was not reached in the requested order. No substitute theorem or
coefficient formula was used to continue.

The diagnostic relies only on the displayed D' formula and exact rational
arithmetic, with integer-verified rational square-root bounds. The final
cell obstruction is proved above independently of the witness's particular
width. It does not establish a defect in O2_n itself, and no claim is made
about whether other obligations would close after this issue is resolved.

All writes were inside o2n. No network, git commands, external-file edits,
or changes to SPEC.md / LEMMAS.md were made. The existing refereed kernel
was read but not executed; its binary64 and libm assumptions therefore do
not apply to any result reported here.
