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
