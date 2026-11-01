"""Adversarial metadata checks; no production evidence is modified."""
import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
import runpy
import sys
import tempfile
import types

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R/'src'))
import driver
current = driver.hashes()
base = {p.name: json.loads(p.read_text()) for p in R.glob('*.json')}
readme_before = (R/'README.md').read_bytes()
checks = []

def report_case(label, change, expected):
    data = copy.deepcopy(base)
    change(data)
    def read(name):
        if name not in data:
            raise FileNotFoundError(name)
        return data[name]
    fake = types.SimpleNamespace(read=read, hashes=lambda: current)
    sys.modules['driver'] = fake
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            try:
                runpy.run_path(str(R/'src/make_report.py'), run_name='__main__')
            except SystemExit as exc:
                assert exc.code == 1, (label, exc.code)
            else:
                raise AssertionError(f'{label}: did not fail closed')
    finally:
        sys.modules['driver'] = driver
    assert expected in output.getvalue(), (label, output.getvalue())
    assert (R/'README.md').read_bytes() == readme_before
    checks.append({'case': label, 'result': 'PASS', 'status': output.getvalue().strip()})

for filename, prefix in [('verification.json', 'Replay'), ('bundle-audit.json', 'Bundle audit')]:
    report_case(filename+' missing', lambda d, f=filename: d.pop(f), prefix+': MISSING')
    report_case(filename+' stale', lambda d, f=filename: d[f]['hashes'].update({'LEMMAS.md': 'bad'}), prefix+': STALE')
    report_case(filename+' malformed', lambda d, f=filename: d.update({f: []}), prefix+': INVALID')
for field, value in [('replay', 'FAIL'), ('partition', 'FAIL'), ('complete', False), ('pending_boxes', 1)]:
    report_case('cell '+field, lambda d, f=field, v=value: d['verification.json']['cells'][0].update({f: v}), 'Replay: FAIL')
report_case('empty replay', lambda d: d['verification.json'].update(cells=[]), 'Replay: INCOMPLETE')
report_case('missing replay cell', lambda d: d['verification.json']['cells'].pop(), 'Replay: INCOMPLETE')
report_case('duplicate replay cell', lambda d: d['verification.json']['cells'].append(d['verification.json']['cells'][0]), 'Replay: INCOMPLETE')
report_case('audit failed', lambda d: d['bundle-audit.json'].update(passed=False), 'Bundle audit: FAIL')
report_case('audit guard failed', lambda d: d['bundle-audit.json']['rows'][0].update(no_search_guard='FAIL'), 'Bundle audit: FAIL')
report_case('missing audit row', lambda d: d['bundle-audit.json']['rows'].pop(), 'Bundle audit: INCOMPLETE')

with tempfile.TemporaryDirectory(dir=R/'fix-evidence') as folder:
    root = Path(folder)
    old = '5c7419ef27595f6d6c8b083c02475a718bde3341f0bdfda10f8faa9c0a568b3a'
    good = {'hashes': current | {'LEMMAS.md': old}, 'cells': [{'keep': 123}]}
    def write(name, value):
        (root/name).write_text(json.dumps(value))
    fake = types.SimpleNamespace(R=root, hashes=lambda: current, write=write)
    sys.modules['driver'] = fake
    try:
        module = runpy.run_path(str(R/'src/refresh_provenance.py'))
        for pin in current:
            if pin == 'LEMMAS.md':
                continue
            write('a.json', good)
            bad = copy.deepcopy(good)
            bad['hashes'][pin] = 'bad'
            write('z.json', bad)
            before = {p.name: p.read_bytes() for p in root.glob('*.json')}
            try:
                module['main']()
            except ValueError:
                pass
            else:
                raise AssertionError('refresh accepted '+pin)
            assert before == {p.name: p.read_bytes() for p in root.glob('*.json')}
            checks.append({'case': 'refresh rejects '+pin+' before writes', 'result': 'PASS'})
        (root/'z.json').unlink()
        with contextlib.redirect_stdout(io.StringIO()):
            module['main']()
        updated = json.loads((root/'a.json').read_text())
        note = updated.pop(module['KEY'])
        assert note == module['NOTE']
        assert updated == {'hashes': current, 'cells': good['cells']}
        before = (root/'a.json').read_bytes()
        with contextlib.redirect_stdout(io.StringIO()):
            module['main']()
        assert before == (root/'a.json').read_bytes()
        checks.append({'case': 'refresh only lemma pin plus record; idempotent', 'result': 'PASS'})
    finally:
        sys.modules['driver'] = driver
(R/'fix-evidence/metadata-tests.json').write_text(json.dumps(checks, indent=2)+'\n')
print(f'{len(checks)} metadata checks PASS; rejected reports left README unchanged.')
