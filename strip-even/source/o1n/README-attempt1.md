# Implementation stopped: fixed-math obstruction

No inequality has been certified for n=8 or n=10. The n=6 regression,
gates 1/2/lemma/5/3/4, and full runs were not started. There are no
certificate files. Slices proved: 0 for each n; slices tested: 0.
Lowest proved H, minimum margin, maximum cells, and solver wall time:
not applicable. Exact proved H range: empty for each n.

Both SPEC files and ../o1dp/README.md were read fully before work.
The instruction to stop if the fixed mathematics looks wrong applies to
`SPEC.md`, "Target F_n: no closed form, certified by the chain itself":
its assertion that kappa is even in dy because Delta is centrally symmetric
is false. Central symmetry maps the right boundary at dy to the *left*
boundary at -dy, not the right boundary there.

The prescribed hull reference, executing only its first 29 lines and
filtering the four specified import/path prefixes, gives at t=t'=0.2,
H=1.9, d=H-2h(t)=0.7212640913636972:

```
kappa(t,t,+d) = 0.8741313753697272
kappa(t,t,-d) = 1.166546314512658
```

These are actual alternating-role displacements within the specified
height and tilt domain. This is not a rounding-scale discrepancy.
Also, at this tilt kappa(t,t,-0.1)=1.0406098484920598 and
kappa(t,t,-0.2)=1.0608808520429271: it can increase with |dy|.
Analytically, here Delta=2S(t), and its right boundary is
min((1-dy*sin(t))/cos(t), (1+dy*cos(t))/sin(t)); it is not even.

This invalidates the stated per-gap argument for monotonicity of F_n,
which is used to bound every H in a slice by the target evaluated at Ha.
It does not establish that F_n itself is nonmonotone: the full alternating
chain or its minimum may still be nonincreasing by a different argument.
That would require a mathematical correction or replacement proof, which
was explicitly outside the authorization for this task. No replacement
premise, bound, or mathematics was silently introduced.

Reproduce locally (no network):

```
../.venv/bin/python math-check.py
```

`math-check.txt` saves the diagnostic output. No writes were made outside
o1n, no git commands were used, and ../o1dp was not modified. No workers
or long-running computations were launched. The diagnostic uses ordinary
binary64 and the reference's system-libm sin/cos; no certified interval
claim is made from it. In any resumed certification, the inherited
assumption of at most eight ulps of libm error and outward padding must
still be documented and checked as stipulated; it cannot fix the
mathematical obstruction above.
