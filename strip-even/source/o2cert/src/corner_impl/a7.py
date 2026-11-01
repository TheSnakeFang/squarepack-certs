"""Condition (A7):  B_X >= A(u) for W=1-xu > 0, i.e.
      K(x,u;H) := (A(1/x)-A(u))/(1/x-u) + H/2 - 1/Rx  >= 0   on {W >= 0}.
Two regimes (divided difference off the belt, midpoint-Taylor near it)."""
from iv import I, C, add, sub, mul, div, neg, ab, sq, sqrt_i, A_f, d1A_f, d2A_f
from iv import grid
D0 = 0.10

def cond7(xI, uI, HI, M2g):
    zI = div(C(1.0), xI)                       # zeta = 1/x
    den = sub(zI, uI)                          # zeta - u = W/x
    if den.hi < 0.0:                           # W < 0 throughout: (A7) not required here
        return I(1.0, 1.0)
    tail = sub(mul(HI, C(0.5)), div(C(1.0), sqrt_i(add(C(1.0), sq(xI)))))   # H/2 - 1/Rx
    if den.lo >= D0:                           # regime (a): plain divided difference
        return add(div(sub(A_f(zI, HI), A_f(uI, HI)), den), tail)
    # regime (b): midpoint Taylor; M2 = sup|A''| on hull(zeta,u), 4 sound sub-scans
    mI = mul(add(zI, uI), C(0.5))
    hull = I(min(zI.lo, uI.lo), max(zI.hi, uI.hi))
    M2 = 0.0
    for k in range(4):
        w = I(grid(hull,k,4), grid(hull,k+1,4))
        M2 = max(M2, ab(d2A_f(w, HI)).hi)
    dd = ab(den).hi
    return add(sub(d1A_f(mI, HI), div(mul(I(min(M2,M2g)), I(dd)), I(4.0))), tail)

def scan7(xI, uI, HI, M2, budget=200000, TAU=0.02):
    stack = [(xI, uI, 0)]; n = 0; m = None; ok = True
    while stack:
        a, b, d = stack.pop(); n += 1
        v = cond7(a, b, HI, M2)
        if v.lo > TAU or (d >= 34 and v.lo > 0.0):
            m = v.lo if m is None else min(m, v.lo); continue
        if n > budget or d >= 40 or (a.hi - a.lo) < 1e-10 or (b.hi - b.lo) < 1e-10:
            ok = False; m = v.lo if m is None else min(m, v.lo); continue
        am = 0.5 * (a.lo + a.hi); bm = 0.5 * (b.lo + b.hi)
        stack += [(I(am, a.hi), I(bm, b.hi), d + 1), (I(a.lo, am), I(bm, b.hi), d + 1),
                  (I(am, a.hi), I(b.lo, bm), d + 1), (I(a.lo, am), I(b.lo, bm), d + 1)]
    return ok, (m if m is not None else 9e9), n
