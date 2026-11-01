#!/usr/bin/env python3
"""Re-prove only the last slice, then replay the 76 pre-lemma grids."""
import concurrent.futures as cf
import datetime,hashlib,json,math,time
import numpy as np
import driver as d
ROOT=d.ROOT
START=datetime.datetime(2026,10,30,19,14,44,tzinfo=datetime.timezone.utc).timestamp()
DEADLINE=START+7200
BACKUP=ROOT/'certificate.before-lemma.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def replay(row):
    start=time.monotonic();ub,theta=d.target(row['Ha'])
    value,u,_=d.solve(row['edges'],row['Ha'],row['Hb'],ub)
    assert value>=row['D'],('regressed',row['Ha'],value,row['D'])
    assert not row['proved'] or value>ub,('lost proof',row['Ha'],value,ub)
    return dict(Ha=row['Ha'],Hb=row['Hb'],cells=row['cells'],old_D=row['D'],D=value,
                unconstrained=u,F6_ub=ub,theta=theta,margin=math.nextafter(value-ub,-math.inf),
                seconds=time.monotonic()-start,proved=value>ub,previously_proved=row['proved'])
def final_job(row):
    start=time.monotonic();edges=np.array(row['edges']);ub,theta=d.target(row['Ha']);history=[]
    assert row['Ha']==1.9999990234375 and row['Hb']==2 and len(edges)==801
    for rnd in range(1,20):
        if time.time()>=DEADLINE:raise TimeoutError('two-hour deadline')
        value,u,binding=d.solve(edges,row['Ha'],row['Hb'],ub)
        margin=math.nextafter(value-ub,-math.inf)
        history.append(dict(cells=len(edges)-1,D=value,unconstrained=u,margin=margin,binding_cells=int(binding.sum())))
        d.log('run.log',f"# LEMMA FINAL round={rnd} cells={len(edges)-1} D={value:.17g} F6_ub={ub:.17g} margin={margin:.17g} binding={int(binding.sum())} seconds={time.monotonic()-start:.3f}")
        if value>ub:break
        mids=(edges[:-1]+edges[1:])*.5
        refined=np.unique(np.r_[edges,mids[binding.astype(bool)]])
        if len(refined)==len(edges):raise RuntimeError('no binding refinement progress')
        if len(refined)>12801:raise RuntimeError('final slice exceeds 12800 cells')
        edges=refined
    else:raise RuntimeError('final slice round limit')
    result=dict(row)
    result.update(D=value,F6_ub=ub,theta=theta,margin=margin,proved=True,reason='proved',
                  cells=len(edges)-1,edges=edges.tolist(),rounds=len(history),seconds=time.monotonic()-start,
                  history=history,pre_lemma_history=row['history'],pre_lemma_D=row['D'])
    d.log('run.log',f"{row['Ha']:.17g} {row['Hb']:.17g} {result['cells']} {len(history)} {value:.17g} {ub:.17g} {margin:.17g} {result['seconds']:.3f} PROVED near_upright_pair_lemma 0")
    return result

def main():
    gates=(ROOT/'lemma-gates-console.log').read_text()
    assert gates.count('PASS=True')==4 and 'PASS=False' not in gates
    cert=json.loads(BACKUP.read_text());old=cert['slices']
    assert len(old)==76 and sum(r['proved'] for r in old)==75
    hashes={p.name:sha(p) for p in (ROOT/'certificate.before-ratio.json',BACKUP)}
    d.log('run.log','# LEMMA UPDATE: only final slice re-proved from saved 800 cells; then all 76 pre-lemma grids replayed; <=6 workers; two-hour watchdog')
    pool=cf.ProcessPoolExecutor(max_workers=6)
    try:
        final=pool.submit(final_job,old[-1]).result(timeout=max(1,DEADLINE-time.time()))
        (ROOT/'lemma-final-result.json').write_text(json.dumps(final,indent=2)+'\n')
        pending={pool.submit(replay,row):i for i,row in enumerate(old)};results=[]
        while pending:
            if time.time()>=DEADLINE:raise TimeoutError('two-hour deadline')
            done,_=cf.wait(pending,timeout=10,return_when=cf.FIRST_COMPLETED)
            for f in done:
                i=pending.pop(f);r=f.result();r['index']=i;results.append(r)
                d.log('run.log',f"# LEMMA REPLAY {i+1}/76 [{r['Ha']:.17g},{r['Hb']:.17g}] cells={r['cells']} D={r['D']:.17g} margin={r['margin']:.17g} old_D={r['old_D']:.17g} seconds={r['seconds']:.3f} monotonicity=PASS status={'PROVED' if r['proved'] else 'UNPROVED'}")
    except BaseException:
        for p in pool._processes.values():p.terminate()
        pool.shutdown(wait=False,cancel_futures=True);raise
    else:pool.shutdown()
    results.sort(key=lambda r:r['index']);rows=[]
    for row,rr in zip(old,results):
        updated=dict(row);updated['pre_lemma_D']=row['D'];updated['pre_lemma_margin']=row['margin']
        for key in ('D','F6_ub','theta','margin','proved'):updated[key]=rr[key]
        updated['lemma_replay_seconds']=rr['seconds'];updated['lemma_replay_unconstrained']=rr['unconstrained']
        rows.append(updated)
    if final['edges']==old[-1]['edges']:assert final['D']==results[-1]['D']
    rows[-1]=final
    assert rows[0]['Ha']==d.DOMAIN_LO and rows[-1]['Hb']==2
    assert all(a['Hb']==b['Ha'] for a,b in zip(rows,rows[1:])) and all(r['proved'] for r in rows)
    for r in rows:
        e=r['edges'];assert len(e)==r['cells']+1 and e[0]==0 and e[-1]==d.TOP
        assert all(a<b for a,b in zip(e,e[1:]))
    assert hashes=={p.name:sha(p) for p in (ROOT/'certificate.before-ratio.json',BACKUP)}
    previous_hashes=cert['source_sha256'];cert['slices']=rows
    cert['source_sha256']={p.name:sha(p) for p in (ROOT/'src/kernel.c',ROOT/'src/driver.py',ROOT/'SPEC.md',ROOT/'src/replay_lemma.py')}
    cert['lemma_update']=dict(start_epoch=START,wall_seconds=time.time()-START,hard_stop_seconds=7200,workers=6,
        previous_certificate_sha256=sha(BACKUP),preserved_backup_sha256=hashes,previous_source_sha256=previous_hashes,
        saved_grid_replay=results,final_slice=final,gates='lemma-gates-console.log',
        gate3='historical only; not rerun for lemma kernel',coverage='76 contiguous closed slices covering [DOMAIN_LO,2]',
        premise='SPEC.md Certified bounds: Near-upright pair lemma (addendum 2)')
    tmp=ROOT/'certificate.json.tmp';tmp.write_text(json.dumps(cert,indent=2)+'\n');tmp.replace(ROOT/'certificate.json')
    msg=f"Lemma replay PASS: 76/76 nondecreasing bounds; all 75 prior proofs retained; final slice PROVED; coverage PASS including H=2; wall_seconds={time.time()-START:.3f}"
    d.log('run.log','# '+msg);(ROOT/'verification.log').write_text(msg+'\n')
if __name__=='__main__':main()
