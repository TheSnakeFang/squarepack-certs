#!/usr/bin/env python3
"""Independent saved-partition audit plus parallel numerical replay. No search."""
import json, math, time, multiprocessing as mp, hashlib
import driver as d

def check_cell(row):
    t0=time.monotonic()
    assert row['source_hashes']==d.hashes()
    assert row['L_upper']==[d.LIB.target(row['theta'],h) for h in (row['Ha'],row['Hb'])]
    rectangles=row['rectangles'];pending=row['pending']
    assert row['proved']==(len(pending)==0)
    allrect=rectangles+pending
    ys=sorted(set([-d.TOP,d.YTOP]+[r[i] for r in allrect for i in (0,1)]))
    for r in allrect:
        assert all(math.isfinite(v) for v in r[:4])
        assert -d.TOP<=r[0]<r[1]<=d.YTOP and -d.TOP<=r[2]<r[3]<=d.YTOP
    for l,u in zip(ys,ys[1:]):
        active=sorted((r[2],r[3]) for r in allrect if r[0]<=l and r[1]>=u)
        end=-d.TOP
        for x,y in active:assert x==end and y>x;end=y
        assert end==d.YTOP
    minimum=None;discards=0
    for r in rectangles:
        if len(r)>5 and r[5]=='sigma':
            assert r[4] is None and d.DN(d.DN(d.LOW-r[1])-r[3])>=5;discards+=1
        else:
            assert math.isfinite(r[4]) and r[4]>0
            v,_=d.rect_test(tuple(r[:4]),row['Ha'],row['Hb'],row['theta'],row['budget_inner'],row['tol_inner'])
            assert v>0
            minimum=v if minimum is None else min(minimum,v)
    assert row['discards']==discards
    return {'id':row['id'],'rectangles':len(rectangles),'pending':len(pending),'discards':discards,'minimum_replayed_margin':minimum,'seconds':time.monotonic()-t0,'partition':'PASS','replay':'PASS','full_cell':row['proved']}

def main():
    t0=time.monotonic();c=json.loads((d.ROOT/'certificate.json').read_text())
    assert c['source_hashes']==d.hashes()
    g=json.loads((d.ROOT/'gates.json').read_text());assert g['passed'] and g['source_hashes']==d.hashes()
    assert c['domain']==[d.H0,2.] and c['J_odd']==list(d.J) and c['J_even']==list(d.JE)
    end=d.H0
    for row in c['cells']:
        assert row['Ha']==end and row['Hb']>end;end=row['Hb']
    assert end==2. and c['complete']==all(r['proved'] for r in c['cells'])
    results=[]
    with mp.Pool(min(8,len(c['cells']))) as pool:
        for r in pool.imap_unordered(check_cell,c['cells']):
            results.append(r);d.log('verification.log',json.dumps(r))
    obj={'complete_domain':c['complete'],'rows':results,'certified_rectangles':sum(r['rectangles'] for r in results),'seconds':time.monotonic()-t0,'source_hashes':d.hashes(),'verifier_sha256':hashlib.sha256((d.ROOT/'src/verify_parallel.py').read_bytes()).hexdigest()}
    d.save('verification.json',obj);d.log('verification.log','REPLAY PASS '+json.dumps({k:v for k,v in obj.items() if k not in ('rows','source_hashes')}))

if __name__=='__main__':main()
