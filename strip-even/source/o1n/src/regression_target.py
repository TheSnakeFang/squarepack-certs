"""Check n=6 point targets against the same three saved o1dp slices."""
import json
import driver as d

d.CHAIN=6
rows=json.loads((d.ROOT/'../o1dp/certificate.json').read_text())['slices']
for i in (0,len(rows)//2,len(rows)-1):
    r=rows[i]
    point,_=d.target(r['Ha'])
    upper,_=d.target(r['Ha'],r['Hb'])
    delta=point-r['F6_ub']
    ok=abs(delta)<=1e-12
    d.log('regression-n6.log',f'target_slice={i} old_F6_ub={r["F6_ub"]:.17g} new_point_F6_ub={point:.17g} delta={delta:.17g} new_interval_F6_ub={upper:.17g} PASS={ok}')
    if not ok:
        raise RuntimeError('n=6 point-target regression failed')
