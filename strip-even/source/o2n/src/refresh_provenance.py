"""Rebind active bundle metadata after the documented lemma wording fixes.

Only top-level JSON records are active metadata. Development archives retain
their historical source pins. Validate every record before writing any record.
This does not replace an unmodified replay and bundle audit.
"""
import hashlib
import json

import driver as d

OLD = '5c7419ef27595f6d6c8b083c02475a718bde3341f0bdfda10f8faa9c0a568b3a'
NEW = '93987270271bf9cbc2090ca24d9d3a7f0b46a41420ba1de948408e97a3811db5'
KEY = 'provenance_refresh_2026_11_01'
NOTE = {
    'old_hash': OLD, 'new_hash': NEW, 'date': '2026-11-01',
    'reason': 'Three wording-only corrections from the second lemma referee '
              'pass, recorded in LEMMAS.md section 14: the normal-slope remark '
              'assumes (L), stored-box containment is explicitly checked after '
              'rounding, and the minimiser statement at H* is conditional. '
              'No mathematical obligation or computation changed.',
}


def main():
    current = d.hashes()
    if current['LEMMAS.md'] != NEW:
        raise ValueError('LEMMAS.md is not the reviewed final document')
    pending = []
    for path in sorted(d.R.glob('*.json')):
        record = json.loads(path.read_text())
        pins = [record[k] for k in ('hashes', 'core_hashes') if k in record]
        if not pins:
            continue
        for pin in pins:
            if set(pin) != set(current):
                raise ValueError(f'{path.name}: unexpected pinned files')
            for name, digest in pin.items():
                allowed = (OLD, NEW) if name == 'LEMMAS.md' else (current[name],)
                if digest not in allowed:
                    raise ValueError(f'{path.name}: pinned hash differs: {name}')
        for key, name in (('continue_source_sha256', 'continue_partitions.py'),
                          ('resume_source_sha256', 'resume_range.py'),
                          ('source_sha256', 'continue_partitions.py')):
            if key in record:
                actual = hashlib.sha256((d.R/'src'/name).read_bytes()).hexdigest()
                if record[key] != actual:
                    raise ValueError(f'{path.name}: pinned hash differs: {name}')
        if KEY in record and record[KEY] != NOTE:
            raise ValueError(f'{path.name}: conflicting refresh record')
        changed = any(pin['LEMMAS.md'] == OLD for pin in pins)
        if changed:
            for pin in pins:
                pin['LEMMAS.md'] = current['LEMMAS.md']
            record[KEY] = NOTE.copy()
            pending.append((path, record))
    for path, record in pending:
        d.write(path.name, record)
        print(f'Refreshed {path.name}')
    print(f'Validated all active pins; refreshed {len(pending)} records. '
          'Run driver.py verify and audit_bundle.py to regenerate evidence.')


if __name__ == '__main__':
    main()
