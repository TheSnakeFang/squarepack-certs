"""Refresh the stored source hashes in certificate.json and cells/*.json after
text-only edits to hashed files (LEMMAS.md), recording the old hashes.  The
computation itself is unchanged; `driver.py verify` replays it against the
refreshed hashes."""
import json, sys, pathlib, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import driver
ROOT = driver.ROOT
new = driver.hashes()
cert_path = ROOT/'certificate.json'
cert = json.loads(cert_path.read_text())
old = cert['source_hashes']
changed = sorted(k for k in new if new[k] != old.get(k))
note = {'date': datetime.date.today().isoformat(), 'changed_files': changed, 'old_source_hashes': old,
        'reason': 'text-only edits to LEMMAS.md after the blind referee pass (Lemma 1 hypothesis, Lemma 5 intermediate sum, Corollary 10.1 H<=2, section 7 range, new section 8); no kernel, driver or certificate data changed'}
assert set(changed) <= {'LEMMAS.md'}, changed
cert['source_hashes'] = new
for c in cert['cells']:
    assert c['source_hashes'] == old; c['source_hashes'] = new
cert.setdefault('provenance_refresh', []).append(note)
cert_path.write_text(json.dumps(cert))
for p in sorted((ROOT/'cells').glob('H*.json')):
    c = json.loads(p.read_text()); assert c['source_hashes'] == old; c['source_hashes'] = new
    c.setdefault('provenance_refresh', []).append(note); p.write_text(json.dumps(c))
print('refreshed; changed files:', changed)

# gates.json carries the same hashes and is checked by verify_parallel.py.
for name in ('gates.json', 'gates.partial.json'):
    p = ROOT/name
    if not p.exists(): continue
    g = json.loads(p.read_text())
    if g.get('source_hashes') == new: continue
    assert g['source_hashes'] == old, name
    g['source_hashes'] = new; g.setdefault('provenance_refresh', []).append(note); p.write_text(json.dumps(g))
    print('refreshed', name)
