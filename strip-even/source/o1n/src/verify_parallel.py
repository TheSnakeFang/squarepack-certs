"""Replay the certificate with at most six independent cell-grid solves.
The serial equivalent remains: driver.py verify --n N.
"""
import argparse
import json
import math
import multiprocessing as mp
import os
import time


def replay(item):
    import driver as d
    i,r=item
    upper=d.LIB.target(d.CHAIN,r['phi'],r['Ha'],r['Hb'])
    lower,_,_=d.solve(r['edges'],r['Ha'],r['Hb'],upper)
    assert upper==r['F_n_ub'],f'target mismatch: slice {i}'
    assert lower==r['D'],f'D mismatch: slice {i}'
    assert math.nextafter(lower-upper,-math.inf)==r['margin']>0,f'margin mismatch: slice {i}'
    return i,lower,upper


def main():
    p=argparse.ArgumentParser();p.add_argument('--n',type=int,choices=[6,8,10],required=True);a=p.parse_args()
    os.environ['O1N_N']=str(a.n)
    import driver as d
    start=time.monotonic()
    cert=json.loads((d.ROOT/f'certificate-n{a.n}.json').read_text())
    assert cert['n']==a.n and cert['domain']==[d.DOMAIN_LO,2.]
    assert cert['source_sha256']==d.source_hashes(),'source mismatch'
    rows=cert['slices'];assert rows
    end=d.DOMAIN_LO
    for r in rows:
        assert math.isfinite(r['Ha']) and math.isfinite(r['Hb']) and r['Ha']==end<r['Hb'],'coverage gap/overlap'
        end=r['Hb']
        if not r['proved']:continue
        edges=r['edges']
        assert edges[0]==0 and edges[-1]==d.TOP and len(edges)==r['cells']+1
        assert all(math.isfinite(x) for x in edges) and all(x<y for x,y in zip(edges,edges[1:]))
        assert math.isfinite(r['D']) and math.isfinite(r['F_n_ub'])
    assert end==2.
    items=[(i,r) for i,r in enumerate(rows) if r['proved']]
    logfile=f'verify-n{a.n}.log'
    with mp.get_context('spawn').Pool(6) as pool:
        for i,lower,upper in pool.imap_unordered(replay,items):
            d.log(logfile,f'slice={i} D={lower:.17g} F_n_ub={upper:.17g} PASS=True')
    d.log(logfile,f'replay PASS n={a.n} proved={len(items)} unproved={len(rows)-len(items)} coverage=[{d.DOMAIN_LO!r},2] workers=6 seconds={time.monotonic()-start:.3f}')


if __name__=='__main__':
    main()
