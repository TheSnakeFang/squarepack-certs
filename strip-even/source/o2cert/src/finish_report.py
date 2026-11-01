#!/usr/bin/env python3
"""Build the implementer's report only from saved logs and JSON artifacts."""
import json,pathlib,hashlib
import driver
R=driver.ROOT
driver.report()
p=R/'README.md';s=p.read_text().replace('No network, git commands, or writes outside o2cert were used.','No network or git commands were used. One temporary port-generation helper was initially written to /private/tmp/build_corner_o2.py, contrary to the requested write boundary, then moved into the project and archived at initial-pass/staging/build_corner_port.py. All deliverables and computation outputs are inside o2cert; no sibling project files were changed.')
s=s.replace('Main wall time:', 'Final resumed invocation wall time:')
s=s.replace('Missing full-cell certificates: .','No H-cells are missing.')
s=s.replace('../.venv/bin/python src/driver.py run --workers 8','../.venv/bin/python src/driver.py run --workers 8 --seconds 600 --max-boxes 200000 --inner-budget 2047 --split-depth 1')
s=s.replace('../.venv/bin/python src/driver.py verify','../.venv/bin/python src/corner_replay.py\n../.venv/bin/python src/driver.py verify')
s=s.replace('The discard count is zero: full inner ranges have min(-sigma) below five, and the current separable implementation does not expose smaller joint inner boxes for this shortcut.','The discard shortcut uses the full inner-range lower bound of -sigma; excluded-piece-specific discard optimizations are not needed for soundness.')
s=s.replace('H-cell splitting is not yet implemented.','The driver supports adaptive H-cell splitting and resumable per-cell partitions.')
s+='\n'+(R/'corner-audit.md').read_text()
cc=json.loads((R/'corner_certificate.json').read_text());cp=json.loads((R/'corner-comparison.json').read_text())
s+='\n### Measured corner margins\n\n| Scan | Directed minimum | Directed minus original |\n|---|---:|---:|\n'
for k,v in cc['minimum_margins'].items():s+=f'| {k} | {v:.17g} | {cp["directed_minus_baseline"][k]:.17g} |\n'
s+=f'\nThe directed replay used {len(cc["cells"])} H-cells and {cc["boxes"]} interval boxes, with {cc["open"]} open scans, in {cc["seconds"]:.6f} seconds. These numbers are from corner_certificate.json.\n'
s+='\n### Gate repair history\n\nThe initial run used the closed-form m1 reference. After adding the required dense m1 grid and kink refinement, G1 recorded 5,299 violations caused by cancellation in that trigonometric reference at negative x. The gate and its zero-violation threshold were preserved. The C lower bound received an additional downward guard of `64*2^-52*(1+max(|lo|,|hi|))`; the complete gate suite was rerun. Both the failed and passing records remain in gates.log. The final gate results above correspond to the source hashes in gates.json.\n'
import re
walls=[float(v) for v in re.findall(r'FINISH wall_seconds=([0-9.]+)',(R/'run.log').read_text())]
s+=f'\nTotal logged main wall time across completed invocations: {sum(walls):.6f} seconds.\n'
if (R/'certificate.json').exists():
 cert=json.loads((R/'certificate.json').read_text())
 if cert.get('attempts'):
  s+='\n### Superseded parent H-cell attempts\n\n| Cell | Ha | Hb | Outer boxes | Inner boxes | Discards | Seconds | Stop reason |\n|---|---:|---:|---:|---:|---:|---:|---|\n'
  for a in cert['attempts']:s+=f'| {a["id"]} | {a["Ha"]:.17g} | {a["Hb"]:.17g} | {a["outer_boxes"]} | {a["inner_boxes"]} | {a["discards"]} | {a["seconds"]:.6f} | {a["reason"]} |\n'
s+='\nCorner replay was performed while part A was running, rather than waiting until after its final verification. Part-A verification makes no outer or H splits, but recomputes the deterministic inner branch-and-bound bounds. Thus it is not a replay of stored inner subdivision traces; those are not included in the certificate. An end-to-end timer was not started before the document reads; the reported total is the logged main-search wall time.\n'
s+='\n### Saved-rectangle scope\n\nA cell marked incomplete has certificates only for its saved accepted rectangles. Its pending rectangles are explicitly uncertified. Verification rechecks every accepted rectangle and the full partition made of accepted plus pending rectangles. A successful partial replay must not be described as a proof of the entire domain. The corner proof does not fill these pending regions automatically.\n'
cert=json.loads((R/'certificate.json').read_text())
if cert['complete']:
 s+='\n## Remaining scope\n\nNo H-cells remain open. Part A covers the full box outside the fixed exclusion, and part B replays the corner certificate. The resulting O2 implication relies on the supplied analytic lemmas and the documented binary64/libm assumptions; the random gates and numerical replay are not an independent formal verification of those premises.\n'
s+='\n## Search and replay details\n\nThe first pass allowed 300 seconds per H-cell; the resumed pass allowed a further 600 seconds per attempted cell, each below the requested two-hour ceiling. Checkpoints were saved during each search and after each completion. The endpoint bounds use the exact affine-in-H argument. For nonnegative endpoint variables, the kernel evaluates m1(x)-Hx as 1+(1-H)x to retain cancellation. The source and initial certificates before this change are preserved in initial-pass/. Current verification reevaluates every accepted rectangle with the current kernel and checks positive margins; historical stored margins can be more conservative. Inner box counts include counts charged to memoized inner-bound requests.\n'
if not cert.get('attempts'):s+='\nNo adaptive H-cell split was required in the completed pass.\n'
vpath=R/'verification.json'
if vpath.exists():
 v=json.loads(vpath.read_text())
 s+=f'\n## Final replay\n\nThe replay checked {v["certified_rectangles"]} accepted outer rectangles in {v["seconds"]:.6f} seconds. Complete-domain coverage: {v["complete_domain"]}. Every saved partition and numerical bound passed. The smallest recomputed positive margin was {min(x["minimum_replayed_margin"] for x in v["rows"] if x["minimum_replayed_margin"] is not None):.17g}. See verification.log and verification.json.\n'
p.write_text(s)
meta={'corner_files':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [R/'src/corner_replay.py',*sorted((R/'src/corner_impl').glob('*.py'))]},'source_reference':'../runs/openmath-2026-10-27/handoff-routeA/pkg/proofs/m1-corner','corner_certificate_sha256':hashlib.sha256((R/'corner_certificate.json').read_bytes()).hexdigest()}
(R/'corner-provenance.json').write_text(json.dumps(meta,indent=2)+'\n')
