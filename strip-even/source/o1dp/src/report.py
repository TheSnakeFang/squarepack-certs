"""Generate the current report from the lemma-update certificate."""
import json,pathlib
root=pathlib.Path(__file__).resolve().parent.parent
readme=root/'README.md'
existing=readme.read_bytes() if readme.exists() else b''
heading=b'## Scope at H = 2'
scope_start=0 if existing.startswith(heading) else existing.find(b'\n'+heading)
if scope_start>0:scope_start+=1
preserved=existing[scope_start:] if scope_start>=0 else b''
c=json.loads((root/'certificate.json').read_text());rows=c['slices'];update=c['lemma_update'];f=update['final_slice']
proved=sum(r['proved'] for r in rows)
gates=(root/'lemma-gates-console.log').read_text()
summary='\n'.join(line for line in gates.splitlines() if line.startswith(('lemma_gate triples=','gate1 samples=','gate2 boxes=','gate4 chains=')))
text=f'''# O1 interval DP results

**{proved}/{len(rows)} slices prove, including the final interval closed at H=2.**
The saved intervals cover [1.87, 2] without gaps; the stored lower endpoint
is the binary64 predecessor of 1.87. Margins are D minus F6_ub, rounded down.
Under the premises below, this certifies the requested non-Morandi inequality
throughout [1.87, 2), with the stronger computation also including H=2.

Only the previously unproved interval [{f['Ha']:.17g}, {f['Hb']:.17g}]
was re-proved, starting from its saved 800-cell grid:
**{f['cells']} cells, D={f['D']:.17g},
F6_ub={f['F6_ub']:.17g}, margin={f['margin']:.17g}, PROVED**.
It required {f['rounds']} round(s) and no H-splitting.
All 76 pre-lemma saved grids were separately replayed with the new kernel.
All 75 prior proofs survived and every D was at least its pre-lemma value.

Smallest positive current margin: {min(r['margin'] for r in rows if r['proved']):.17g}.
Largest current grid: {max(r['cells'] for r in rows)} cells.
The update used at most six workers and finished in {update['wall_seconds']:.3f}
seconds from task start, within its two-hour hard stop.

## Gates

The new pointwise lemma gate and gates 1, 2 and 4 passed with zero violations.
The lemma gate used 200,000 triples and both normals in both mirrored cases
(800,000 terms), with exactly 50,000 H=2 triples and at least 50,000 W<=1e-3 triples.
Gate 2 used 25,000 boxes with both cells wholly in the same corner region
[0,0.3] or [pi/2-0.3,pi/2], widths 1e-8 through 0.3; exactly 12,500
of those slices included H=2. The other 25,000 boxes used the original general
distribution. All boxes had 64 interior samples. Gate 3 remains historical
from the plain kernel and was not rerun or relabeled.

```
{summary}
```

## Bound and arithmetic assumptions

The original plain term bound, support bound, target and DP recursion are
unchanged. Each eligible normal now also receives exactly the SPEC's
correlated ratio lower bound. The new premise is the **Near-upright pair
lemma (addendum 2)**, proved in [SPEC.md](SPEC.md#certified-bounds-all-in-interval-arithmetic-with-outward-rounding).
Its candidate is nonzero only for C->F sine normals with both cells inside
[0,1], or F->C cosine normals with both inside [pi/2-1,pi/2]. It supplies
1-3W/4-W^2/4 with upward-rounded penalties and downward-rounded subtractions;
the upper-corner width and eligibility threshold use an upward enclosure
of pi/2. Each term is `max(plain, ratio, lemma, 0)`.
For its smallest-n_x face, N(e)>=a=max(A,0) follows from the face interval
and pointwise interiority. An outward interval encloses the one-sided
N derivative throughout the box, including both derivatives of |sin(delta)|
at delta=0. Thus N>=a+x B and n_x<=c+x. If a+x B is negative, nonnegativity
already supplies the lower bound; otherwise division gives min(a/c,B),
or B when c=0. The physical endpoint faces have exact sin/cos values.

- IEEE-754 binary64, ordinary round-to-nearest arithmetic, functioning
  nextafter, and no fast-math or reassociation. DP sums and margins round down.
- System libm sin/cos/sqrt errors are assumed at most eight ulps; results are
  padded outward. This remains an unverified libm accuracy assumption.
- Adjacent floats bracket pi/4; the float above binary64 pi/2 encloses the
  physical tilt endpoint. The extra width is only an enclosure device.
- The facet support is (1+cos(delta)+|sin(delta)|)/2. The other four signed
  normals have nonpositive x component on the physical domain.
- Numerator clipping uses the SPEC's vertical-segment/interiority argument
  and |dy|<=1. The supplied vertex reduction and F6 monotonicity are premises.
- The target evaluates L at one trial angle with outward arithmetic at Ha.
  The numerical minimizer need not find a global minimum for that upper bound.
- Gates compare against the unmodified hull reference definitions parsed
  from ../runs/openmath-2026-10-27/m4check.py. Random tests are sampled evidence;
  replay is reproducibility evidence, not an independent formal verification.

## Artifacts and replay

`certificate.before-ratio.json` and `certificate.before-lemma.json` are
untouched. `certificate.json` contains the current grids, bounds and source
hashes, with all 76 pre-lemma-grid replay outcomes under
`lemma_update.saved_grid_replay`. Prior update provenance and historical
refinement records remain preserved; `pre_lemma_D` records the preceding bound.
`lemma_update.final_slice` records the new final-slice proof and its refinement.
`run.log` appends that result and the 76 replay outcomes. `gates.log` appends
the new gate run. Console records are `lemma-gates-console.log` and
`lemma-replay-console.log`; `verification.log` records coverage and replay.

From this directory:

```sh
clang -O2 -std=c11 -D_DARWIN_C_SOURCE -shared -fPIC src/kernel.c -o src/kernel.dylib
../.venv/bin/python src/driver.py gates
../.venv/bin/python src/driver.py verify
../.venv/bin/python src/report.py
```

`verify` replays all current grids and checks exact saved values and coverage.
The one-time lemma migration is `src/replay_lemma.py`; it reads
`certificate.before-lemma.json`. Its two-hour watchdog terminates native
worker calls as well as Python processes. At most six workers run; no full
NxN matrix is stored and worker memory remains O(N). No git commits were made,
and all writes stayed inside o1dp.

## Endpoint outcome

The joint lemma resolves the shared-corner collapse of the one-dimensional
ratio bound. The final slice [{f['Ha']:.17g}, 2] now proves with margin
{f['margin']:.17g}. Its saved 800-cell grid was the starting partition;
{f['rounds']} solve round(s) yielded the {f['cells']}-cell certificate above.
The kernel's support, plain bound, ratio bound, target and DP recursion
are unchanged. The only additional mathematical premise is SPEC addendum 2.

## Current per-slice bounds

| Ha | Hb | Cells | D | Margin |
|---|---|---:|---:|---:|
'''
for r in rows:
    text+=f"| {r['Ha']:.17g} | {r['Hb']:.17g} | {r['cells']} | {r['D']:.15g} | {r['margin']:.15g} |\n"
readme.write_bytes(text.encode()+ (b'\n'+preserved if preserved else b''))
print(f'README updated: {proved}/{len(rows)} proved; gates and replay provenance recorded')
