"""Reproduce the SPEC target-monotonicity obstruction without changing its math."""
from pathlib import Path

reference = Path(__file__).resolve().parent.parent / 'runs/openmath-2026-10-27/m4check.py'
lines = reference.read_text().splitlines()[:29]
namespace = {}
exec('\n'.join(line for line in lines if not line.startswith(
    ('from targets', 'sys.path', 'import numpy', 'from scipy'))), namespace)
kappa, h = namespace['kappa'], namespace['h']
t, H = 0.2, 1.9
dy = H - 2 * h(t)
print(f't={t!r} H={H!r} alternating displacement magnitude={dy!r}')
print(f'kappa(t,t,+dy)={kappa(t,t,dy)!r}')
print(f'kappa(t,t,-dy)={kappa(t,t,-dy)!r}')
for magnitude in (0.1, 0.2, 0.3):
    print(f'kappa(t,t,{-magnitude!r})={kappa(t,t,-magnitude)!r}')
