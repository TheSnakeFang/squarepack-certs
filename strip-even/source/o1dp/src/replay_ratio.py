#!/usr/bin/env python3
"""Replay exactly the 76 original saved grids under the correlated kernel."""
import concurrent.futures as cf
import hashlib,json,math,time
import driver as d
START=1793344206.0
ROOT=d.ROOT
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def replay(row):
    start=time.monotonic();ub,theta=d.target(row['Ha'])
    value,u,_=d.solve(row['edges'],row['Ha'],row['Hb'],ub)
    assert value>=row['D'],('regressed',row['Ha'],value,row['D'])
    assert not row['proved'] or value>ub,('lost proof',row['Ha'],value,ub)
    return dict(Ha=row['Ha'],Hb=row['Hb'],cells=row['cells'],old_D=row['D'],D=value,
                unconstrained=u,F6_ub=ub,theta=theta,margin=math.nextafter(value-ub,-math.inf),
                seconds=time.monotonic()-start,proved=value>ub,previously_proved=row['proved'])
def main():
    gates=(ROOT/'ratio-gates-console.log').read_text()
    assert gates.count('PASS=True')==3 and 'violations=0' in gates
    backup=ROOT/'certificate.before-ratio.json';cert=json.loads(backup.read_text());old=cert['slices']
    assert len(old)==76 and sum(r['proved'] for r in old)==75
    results=[];pool=cf.ProcessPoolExecutor(max_workers=6)
    d.log('run.log','# Ratio replay: exactly 76 original grids; refinement halted after explicit endpoint path shows bound <=4 versus target >5.31')
    try:
        pending={pool.submit(replay,row):i for i,row in enumerate(old)}
        while pending:
            if time.time()>=START+7200:raise TimeoutError('two-hour deadline')
            done,_=cf.wait(pending,timeout=10,return_when=cf.FIRST_COMPLETED)
            for f in done:
                i=pending.pop(f);r=f.result();r['index']=i;results.append(r)
                status='PROVED' if r['proved'] else 'UNPROVED'
                d.log('run.log',f"# REPLAY {i+1}/76 [{r['Ha']:.17g},{r['Hb']:.17g}] cells={r['cells']} D={r['D']:.17g} margin={r['margin']:.17g} old_D={r['old_D']:.17g} seconds={r['seconds']:.3f} monotonicity=PASS status={status}")
    except BaseException:
        for p in pool._processes.values():p.terminate()
        pool.shutdown(wait=False,cancel_futures=True)
        raise
    else:pool.shutdown()
    results.sort(key=lambda r:r['index']);rows=[]
    for row,rr in zip(old,results):
        updated=dict(row)
        updated['pre_ratio_D']=row['D'];updated['pre_ratio_margin']=row['margin']
        for key in ('D','F6_ub','theta','margin','proved'):updated[key]=rr[key]
        updated['replay_seconds']=rr['seconds'];updated['replay_unconstrained']=rr['unconstrained']
        if not rr['proved']:updated['reason']='correlated_ratio_endpoint_stall'
        rows.append(updated)
    assert rows[0]['Ha']==d.DOMAIN_LO and rows[-1]['Hb']==2.
    assert all(a['Hb']==b['Ha'] for a,b in zip(rows,rows[1:]))
    cert['slices']=rows;previous_hashes=cert['source_sha256']
    cert['source_sha256']={p.name:sha(p) for p in (ROOT/'src/kernel.c',ROOT/'src/driver.py',ROOT/'SPEC.md')}
    cert['ratio_update']={'start_epoch':START,'wall_seconds':time.time()-START,
        'hard_stop_seconds':7200,'workers':6,'previous_certificate_sha256':sha(backup),
        'previous_source_sha256':previous_hashes,'saved_grid_replay':results,
        'final_slice':results[-1], 'gates':'ratio-gates-console.log',
        'refinement_stop':'CCFCFC all-first-cell bound remains below 4; requested derivative/face bound cannot close endpoint',
        'endpoint_diagnostic':'ratio-endpoint-diagnostic.json',
        'gate3':'historical only; not rerun for ratio kernel'}
    tmp=ROOT/'certificate.json.tmp';tmp.write_text(json.dumps(cert,indent=2)+'\n');tmp.replace(ROOT/'certificate.json')
    r=results[-1]
    d.log('run.log',f"{r['Ha']:.17g} {r['Hb']:.17g} {r['cells']} 1 {r['D']:.17g} {r['F6_ub']:.17g} {r['margin']:.17g} {r['seconds']:.3f} {'PROVED' if r['proved'] else 'UNPROVED'} correlated_ratio_endpoint_stall 0")
    msg=f"Original-grid replay PASS: 76/76 nondecreasing bounds, all 75 prior proofs retained; final slice {'PROVED' if r['proved'] else 'UNPROVED'}; coverage PASS; seconds={time.time()-START:.3f}"
    d.log('run.log','# '+msg);(ROOT/'verification.log').write_text(msg+'\n')
if __name__=='__main__':main()
