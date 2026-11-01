"""Exact counterexample to the unrestricted C0 obligation; not a certificate."""
from fractions import Fraction as Q
from time import perf_counter


def b1(z, k):
    x1, y2, x3, y4, x5 = map(Q, z)
    minus = lambda x: max(-x, Q(0))
    return (k*y2 + k*y4 + minus(x1+y2) + k*x1
            + minus(x3+y2) + minus(x3+y4) + k*x3
            + minus(x5+y4) + k/2*max(x5, Q(0)) - k/2*minus(x5))


if __name__ == '__main__':
    start = perf_counter()
    z = (-1, 1, -1, 1, -1)
    assert max(map(abs, z)) == 1
    assert all(z[i]+z[j] == 0 for i, j in ((0, 1), (2, 1), (2, 3), (4, 3)))
    print('C0 unrestricted-domain counterexample:', z)
    for h in (Q('1.846936'), Q('1.86')):
        k = 2-h
        value = b1(z, k)
        assert value == -k/2 < 0
        print(f'H={h} k={k} B1_L={value} decimal={float(value):.6f}')
    # B1 at a fixed point is affine in k. These exact coefficients prove
    # B1_L(z;k)=-k/2 for every k, not merely the two displayed endpoints.
    assert b1(z, Q(0)) == 0 and b1(z, Q(1)) == Q(-1, 2)
    print('Exact affine identity: B1_L(z;k) = -k/2 for all k.')
    print('This point is in the stated C0 domain but violates the separate x1>=0 block constraint.')
    print(f'Diagnostic wall_seconds={perf_counter()-start:.6f}')
