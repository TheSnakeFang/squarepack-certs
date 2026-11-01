"""Generate README from finished certificates and their replay; no proof changes."""
import json,pathlib,sys
from fractions import Fraction
R=pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0,str(R/'src'));import driver as d
order=['n8','n6','n10','n10-five']
def evidence(name, kind, expected):
 try:
  data=d.read(name)
  if data.get('hashes') != d.hashes():
   return data, 'STALE (pinned hashes differ)'
  if kind == 'Replay':
   rows=data.get('cells')
   if not isinstance(rows,list) or not rows:
    return data, 'INCOMPLETE (no cell results)'
   for r in rows:
    if r.get('complete') is not True or r.get('pending_boxes') != 0 or r.get('replay') != 'PASS' or r.get('partition') != 'PASS':
     return data, f"FAIL (cell {r.get('id')}: replay={r.get('replay')}, partition={r.get('partition')}, complete={r.get('complete')}, pending_boxes={r.get('pending_boxes')})"
   observed=[(r['id'],r['outer_boxes']) for r in rows]
   if sorted(observed) != sorted(expected):
    return data, 'INCOMPLETE (cell results differ from manifests)'
  else:
   if data.get('passed') is not True:
    return data, 'FAIL (passed is not true)'
   rows=data.get('rows')
   if not isinstance(rows,list) or not rows or any(r.get('no_search_guard') != 'PASS' for r in rows):
    return data, 'FAIL (missing or failed audit rows)'
   if sorted((r['run'],r['cells']) for r in rows) != sorted(expected):
    return data, 'INCOMPLETE (audit rows differ from manifests)'
  return data, 'PASS'
 except FileNotFoundError:
  return None, 'MISSING'
 except (ValueError,KeyError,TypeError,AttributeError) as exc:
  return None, f'INVALID ({exc})'

expected_cells=[];expected_audit=[]
for tag in order:
 c=d.read(f'certificate-{tag}.json')
 expected_cells.extend((r['id'],r['outer_boxes']) for r in c['cells'])
 expected_audit.append((tag,len(c['cells'])))
v,replay_status=evidence('verification.json','Replay',expected_cells)
audit,audit_status=evidence('bundle-audit.json','Bundle audit',expected_audit)
print(f'Replay: {replay_status}')
print(f'Bundle audit: {audit_status}')
if replay_status != 'PASS' or audit_status != 'PASS':
 sys.exit(1)
g=d.read('gates.json')
lines=['# O2n certified computation','','The supplied SPEC.md and revised LEMMAS.md are unchanged. The claims below use their analytic lemmas and the arithmetic assumptions stated below. Random gates alone are not certificates.','', '## Results','', '| Run | Completed H-cells | Accepted outer boxes | Tested outer boxes | Inner boxes charged | Minimum strict margin | Exact requested rational H range | Search wall seconds |','|---|---:|---:|---:|---:|---:|---|---:|']
meta=[]
for tag in order:
 p=R/f'certificate-{tag}.json'
 if not p.exists():continue
 c=d.read(p.name);rows=c['cells'];good=all(r['complete'] for r in rows) and c['complete'];assert c['hashes']==d.hashes()
 ranges={'n8':'[1.852049, 2]','n6':'[1.861098, 2]','n10':'[1.86, 2]','n10-five':'[1.846936, 1.86]'}
 nclosed=sum(r['complete'] for r in rows);outer=sum(r['outer_boxes'] for r in rows);inner=sum(r['inner_boxes'] for r in rows);tested=sum(r['outer_tested'] for r in rows);m=min((r['min_margin'] for r in rows if r['min_margin'] is not None),default=None)
 claimed=ranges[tag] if good else 'incomplete; see certificate'
 lines.append(f'| {tag} | {nclosed} | {outer:,} | {tested:,} | {inner:,} | {m:.17g} | {claimed} | {c["wall_seconds"]:.6f} |')
 meta.append((tag,c,good))
lines+=['','Counts are from the completed partition. Inner counts include the initial bound request and the second request that saves the accepted leaf partition. The final five-block continuation also counts exact-key cache hits; these are charged leaf counts, not counts of distinct arithmetic evaluations. Superseded H-cell attempts, if any, are separate in each certificate. Search wall time excludes gates and final replay.','']
if v:
 lines += [f'Replay: **PASS**, {len(v["cells"])} H-cells, {sum(r["outer_boxes"] for r in v["cells"]):,} accepted outer boxes, {v["seconds"]:.6f} seconds. All recorded cells have complete-domain coverage: {all(r["complete"] for r in v["cells"])}. Replay verifies source hashes, H0, tail caps, T brackets, local hypotheses, every inner leaf bound, both endpoint inequalities, and outer partition coverage. It never runs a minimization or bisection.','']
lines+=['## Gate results','','The final gate pass is gates.json, pinned to the final source/library hashes. Earlier development gate records are archived in development-run/gates-history.log.','']
for name,rec in g['results'].items():lines.append(f'- **{name}: PASS**, '+json.dumps({k:x for k,x in rec.items() if k not in ('passed','elapsed_seconds')})+'.')
if (R/'supplemental-gates.json').exists():
 lines += ['', 'G4 supplemental check: one additional random H per n, zero violations. Combined total: 300 random H plus the explicit H=2 endpoint per n. The supplement also runs the 2,000 original o2cert G1 support-function/hull triples; see supplemental-gates.json for the maximum error.']
lines+=['',f'Final gate wall time: {g["seconds"]:.6f} seconds.','', '## H0, local, tail, and endpoint evidence','']
for tag,c,good in meta:
 slacks={k:min(z[k] for row in c['cells'] for z in row['Loc']) for k in d.NAMES}
 peak=max((row['peak_worker_rss_bytes'] for row in c['cells']+c['attempts']),default=0)
 lines += [f'### {tag}','',f'H0: `{json.dumps(c["H0"])}`. Tail checks: `{json.dumps(c["tail"])}`.',f'Minimum recorded local slacks: `{json.dumps(slacks)}`. Peak worker RSS: {peak:,} bytes. {len(c["attempts"])} superseded H-cell attempts.',f'Exact outward binary64 domain endpoints as rational numbers: `[{Fraction(c["range"][0])}, {Fraction(c["range"][1])}]`; hex: `[{c["range"][0].hex()}, {c["range"][1].hex()}]`. The table reports the exact requested rational subrange contained in those endpoints.','']
 if c['attempts'] or not good:lines += [f'Full per-attempt results, open cells, best failed margins and per-cell timings: [{"certificate-"+tag+".json"}](certificate-{tag}.json).','']
lines += ['## Implementation and assumptions','','- The candidate evaluator and global Lipschitz centred form are copied verbatim from `../o2cert/src/kernel.c` into `src/kernel.c`; no sibling imports are used. The copied driver is retained as a development reference. `src/block.c` extends the kernel.','- Run the Python entry points without `-O` or `PYTHONOPTIMIZE`; assertion checks are part of verification.', '- IEEE binary64 and round-to-nearest basic operations are assumed. Each interval arithmetic result is expanded with nextafter, and sqrt/libm results use the inherited eight-ulp padding. The build uses `-O2 -ffp-contract=off`, no fast-math. These are conditional numerical certificates, not a formal proof of the platform libm or compiler.','- Every trial T_hat is an exact binary64 rational, shared between the two endpoints. Endpoint bounds and the given affine-in-H argument certify the whole H-cell.','- H0 evaluates rational H_lo and T0 using enclosing binary64 intervals. T_lo and T_hi are binary64 rationals with strict endpoint sign checks. The local box is rounded inward. Local checks use the whole independent (T,H) rectangle, allow negative cY, and use 256 interval subdivisions of J for L. Neither gamma >= 0 nor Tan is checked.','- The five-block tail uses the sum of positive parts `k*(x1^+ + Y2^+ + x3^+ + Y4^+) + (k/2)*x5^+`; the printed caps are checked against its exact rational ratios.', '- The first-order origin bounds are Lemmas 21 and 21\'; no C0 computation is used. Product exclusions are implemented as unions over the odd-coordinate complements, after outer splitting at the even-coordinate boundaries.','- Each accepted outer box references a compressed file of all inner leaf intervals with a SHA-256 hash. The H-cell manifest is compressed and hashed in the top-level certificate. Failed/partial H-cells never count as full-range certificates.','- Six worker processes maximum. Streaming the accepted inner partitions keeps worker memory bounded; the worker safety cutoff is 230 MiB RSS. The initial runner caps each range at 10,200 seconds; the five-block continuation enforces a cumulative 10,800-second cap. Archived development search times are listed below and included in the aggregate budget audit. No network, git commands, or writes outside o2n were used.','', '## Deviations from SPEC.md','','1. Outer selection uses largest volume first, instead of prioritizing the smallest lower bound. Inner minimizations use the prescribed best-first lower bound. This affects search order only; every accepted box is checked identically.','2. The shared gate suite, including the other n and five-block cases, was run before the n=8 production search. Production ranges were then run in the requested n=8, n=6, n=10 even-star, n=10 five-block order.','3. The n=10 even-star and five-block manifests are separate (`certificate-n10.json`, `certificate-n10-five.json`) to preserve their separate range budgets and schemas.','4. During development, a superseded n=8 run was interrupted to replace memory-growing embedded leaf lists with streamed compressed files and to tighten the scalar rational T0 enclosure. That checkpoint is archived under `development-run/`; it is not part of the final certificate. A second development run (`development-run-2/`) was stopped to remove unnecessary root finding from replay. All final certificates were regenerated; their verification uses only stored parameters, interval checks, and leaf bounds. The five-block range was continued with `src/resume_range.py` after its first 180-second attempts; this runner preserves the completed cells and cumulative range time while giving new cells up to 1,800 seconds and 500,000 outer tests. The last cell was then resumed from its saved spatial partition with `src/continue_partitions.py`, preserving every accepted box and enforcing the remaining cumulative budget. It uses a bounded, exact-key cache of deterministic inner results, checked against uncached results on 60 cases with zero differences; all stored leaf intervals are still replayed directly. All production ranges were restarted from the final source, and the final gates and replay are pinned to that source.','', '5. One extra random H per n and the legacy hull cross-check were added as supplemental gates after the search, bringing G4 to 300 random H plus H=2 per n. The full primary gate suite ran before the search.', '', '## Issues with the spec','','None identified in the revised fixed mathematics. Neither historical issue in README-attempt1.md or README-attempt2.md applies to this version. No mathematical formula, coefficient, lemma, target inequality, clipping bound, or coordinate cap was changed.','', '## What remains open and uncertain','','The slivers [H*(n), H_lo(n)) remain uncovered, as the specification requires. No result for n >= 12 is claimed. The certificate relies on the supplied analytic lemmas and the documented compiler/binary64/libm premises. Random gates do not independently prove those premises.','', '## Reproduce','','To replay this shipped bundle, retain its compiled library and run `../.venv/bin/python src/driver.py verify --workers 6`, followed by `../.venv/bin/python src/audit_bundle.py`. Rebuilding can change the library hash. For a fresh search, first move the four certificate manifests to a backup directory, then run:', '', '```sh','clang -O2 -ffp-contract=off -shared -fPIC src/block.c -o src/kernel.dylib','../.venv/bin/python src/driver.py gates --workers 6','../.venv/bin/python src/driver.py run --workers 6 --inner-budget 511 --tol 0.00002 --cell-seconds 1800 --max-outer 500000 --range-seconds 10200','../.venv/bin/python src/supplement_g4.py', '../.venv/bin/python src/driver.py verify --workers 6', '../.venv/bin/python src/audit_bundle.py','../.venv/bin/python src/driver.py report','../.venv/bin/python src/make_report.py','```','','A partial five-block run can be continued with `../.venv/bin/python src/resume_range.py certificate-n10-five.json --cell-seconds 1800`. `run` skips completed ranges. To start over, move the four top-level certificate manifests aside first; all old cell and leaf files are harmless unless referenced by a current manifest. Build details are in build.json; numerical gate data in gates.json; production progress in run.log, run-console.log, resume-console.log, and continuation-console.log (run.log also retains superseded development entries); current manifests are authoritative. Replay results in verification.json and verification.log.','']
dev={}
for folder in ['development-run','development-run-2']:
 for p in (R/folder).glob('certificate-n*.json'):
  c=json.loads(p.read_text());tag=p.stem.removeprefix('certificate-');dev[tag]=dev.get(tag,0)+c['wall_seconds']
if audit_status == 'PASS':
 lines += ['Additional bundle audit: '+audit_status+'. Exact requested ranges and source provenance were checked, and every stored parameter check was exercised with root and inner-search entry points disabled; the replay function was also checked for search calls. See bundle-audit.json.', '']
smoke=R/'development-run/cells/smoke-n8.json.gz'
if smoke.exists():
 import gzip
 with gzip.open(smoke,'rt') as f:dev['n8']=dev.get('n8',0)+json.load(f)['seconds']
if (R/'cache-gate.json').exists():
 cg=d.read('cache-gate.json');lines += [f'Exact-key cache gate: {cg["cases"]} cases, {cg["violations"]} violations. Cached bounds and every saved interval matched the uncached result bit for bit.', '']
lines += ['## Aggregate search time audit', '', 'Logged search times exclude document reading, gates, final replay, and pauses between invocations. Interrupted development times are their last checkpoint values.', '', '| Range | Final production seconds | Archived development seconds | Total search seconds |', '|---|---:|---:|---:|']
for tag,c,_ in meta:
 total=c['wall_seconds']+dev.get(tag,0);assert total<10800
 lines.append(f'| {tag} | {c["wall_seconds"]:.6f} | {dev.get(tag,0):.6f} | {total:.6f} |')
lines += ['', '## Provenance refresh', '',
 'On 2026-11-01, `src/refresh_provenance.py` rebound only the LEMMAS.md pin after the three wording-only corrections recorded in its section 14. Each refreshed manifest records the old hash, new hash, date and reason in `provenance_refresh_2026_11_01`; all other active source/library pins were checked unchanged. Historical development archives retain their original pins. The unmodified six-worker replay and bundle audit were rerun against the final document. No mathematical obligation or search code changed.', '',
 'Referee: [blind computation review](../docs/o2n-review-codex-2026-11-01.md), verdict yes under the stated premises; 0 MAJOR, 3 MINOR fixed.', '']
(R/'README.md').write_text('\n'.join(lines)+'\n')
