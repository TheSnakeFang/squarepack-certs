#!/usr/bin/env python3
"""Exact rational witness for the rectangular gamma requirement in SPEC.md.

No floating point enters the enclosure arithmetic or sign assertions. Decimal
strings are for display only. This is a spec diagnostic, not a gate/certificate.
"""
from fractions import Fraction as Q
from math import isqrt
from decimal import Decimal, localcontext
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def add(a, b):
    return a[0] + b[0], a[1] + b[1]

def neg(a):
    return -a[1], -a[0]

def mul(a, b):
    p = [x*y for x in a for y in b]
    return min(p), max(p)

def div(a, b):
    assert b[0] > 0
    return mul(a, (1/b[1], 1/b[0]))

def pt(x):
    return x, x

def sqrt_bounds(x):
    scale = 10**80
    floor = isqrt((x.numerator * scale**2)//x.denominator)
    lo, hi = Q(floor, scale), Q(floor+1, scale)
    assert lo*lo <= x <= hi*hi
    return lo, hi

def dp(t):
    w = t + 1/t
    p = sqrt_bounds(w*(w+2))
    return div(pt(1/t**2 - 1), mul(p, add(p, pt(w+1))))

def derivative(n, t, h):
    m = n//2
    return add(pt((2-h)*(m-(m-1)/t**2)), neg(mul(pt(Q(n-2)), dp(t))))

def gamma(n, j, side, t, h):
    m = n//2
    cx = (2-h) * (Q(m-j, m-1) if side == 'left' else Q(j, m-1))
    return mul(pt(t*t), add(pt(cx), neg(dp(t))))

def decimal(q):
    with localcontext() as c:
        c.prec = 28
        return str(Decimal(q.numerator)/Decimal(q.denominator))

def encode(a):
    return {'exact': [str(v) for v in a], 'decimal': [decimal(v) for v in a]}

def main():
    start = time.monotonic()
    n = 8
    ha, hb = Q(199999,100000), Q(2)
    tl, th = Q(9999,10000), Q(1000001,1000000)
    signs = {}
    for name, h in [('Ha', ha), ('Hb', hb)]:
        lo, hi = derivative(n, tl, h), derivative(n, th, h)
        assert lo[1] < 0 < hi[0]
        signs[name] = {'lower_T_derivative': encode(lo), 'upper_T_derivative': encode(hi)}
    witnesses = []
    for h in [hb, Q(1999999,1000000)]:
        for j in [1, 2]:
            for side in ['left', 'right']:
                g = gamma(n,j,side,tl,h)
                assert g[1] < 0
                witnesses.append({'n': n, 'j': j, 'side': side, 'T': str(tl), 'H': str(h), 'gamma': encode(g)})
    data = {'kind': 'specification_diagnostic_not_certificate',
            'cell': [str(ha), str(hb)], 'T_bracket': [str(tl), str(th)],
            'T_sign_checks': signs, 'negative_gamma_witnesses': witnesses,
            'exact_arithmetic': 'fractions.Fraction; sqrt enclosed using integer isqrt at scale 10^80',
            'seconds': time.monotonic()-start}
    (ROOT/'local-spec-issue.json').write_text(json.dumps(data, indent=2)+'\n')
    print('EXACT RATIONAL DIAGNOSTIC: PASS')
    print(f'n={n} H=[{ha},{hb}], T=[{tl},{th}]')
    for name, row in signs.items():
        print(name, 'dT_f(T_lo).upper='+row['lower_T_derivative']['decimal'][1],
              'dT_f(T_hi).lower='+row['upper_T_derivative']['decimal'][0])
    for row in witnesses:
        print(f"j={row['j']} {row['side']} T={row['T']} H={row['H']} gamma.upper={row['gamma']['decimal'][1]} < 0")
    print('No G1-G6 gate or H-cell certificate is asserted by this diagnostic.')
    print(f"diagnostic_seconds={data['seconds']:.6f}")

if __name__ == '__main__':
    main()
