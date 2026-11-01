#!/usr/bin/env python3
"""Bounded n=6 range runner; uses driver.py and kernel.c unchanged.

Run gates, run, verify in order. The budget starts at gates and covers replay.
"""
from driver import *
import driver as base
import signal
os.environ['O1N_N']='6'
CHAIN=base.CHAIN=6
H0=base.H0=1.862
DOMAIN_LO=base.DOMAIN_LO=math.nextafter(H0,-math.inf)
DOMAIN_HI=1.87
GATE_LOG=base.GATE_LOG='gates-n6.log'
HARD_STOP=7200

def budget_start():
    return json.loads((ROOT/'budget-n6.json').read_text())['start_epoch']

def enforce_budget():
    remaining=HARD_STOP-(time.time()-budget_start())
    if remaining<=0:raise TimeoutError('Two-hour budget exhausted')
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('Two-hour budget exhausted')))
    signal.setitimer(signal.ITIMER_REAL,remaining)

def source_hashes():
    paths=['src/kernel.c','src/driver.py','src/run_n6.py','SPEC.md']
    return {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}

def gate3():
    rng=np.random.default_rng(20261101);start=time.monotonic()
    for ha,hb in [(DOMAIN_LO,H0+.005),(H0+.005,DOMAIN_HI),(DOMAIN_LO,DOMAIN_LO)]:
        best=float(CHAIN);witness={'roles':[0]*CHAIN,'tilts':[0]*CHAIN,'H':hb}
        for trial in range(300):
            roles=rng.integers(0,2,CHAIN).tolist()
            while all(a!=b for a,b in zip(roles,roles[1:])):roles=rng.integers(0,2,CHAIN).tolist()
            H=float(rng.uniform(ha,hb));x=rng.uniform(0,math.pi/2,CHAIN)
            opt=minimize(lambda t:chain_value(t,roles,H),x,method='L-BFGS-B',bounds=[(0,math.pi/2)]*CHAIN,options={'maxiter':200,'ftol':1e-12})
            value=chain_value(opt.x,roles,H,True)
            if value<best:best=value;witness={'roles':roles,'tilts':opt.x.tolist(),'H':H}
        log(GATE_LOG,f'gate3 search slice=[{ha:.17g},{hb:.17g}] random_nonalt_patterns=300 method=L-BFGS-B best={best:.17g} witness={json.dumps(witness)}')
        limit,_=target(hb);ub,_=target(ha,hb);prev=-math.inf
        for cells in (50,100,200,400):
            d,u,_=solve(np.linspace(0,TOP,cells+1),ha,hb,ub)
            ok=u<=limit and u>=prev and d<=best
            log(GATE_LOG,f'gate3 slice=[{ha:.17g},{hb:.17g}] cells={cells} unconstrained={u:.17g} right_end_target={limit:.17g} deficit={limit-u:.17g} flagged={d:.17g} sampled_nonalt={best:.17g} PASS={ok}')
            if not ok:raise RuntimeError('Gate 3 failed')
            prev=u
    log(GATE_LOG,f'gate3 PASS=True seconds={time.monotonic()-start:.3f}')

def gate4(rng=None,start=None):
    if rng is None:rng=random.Random(20261030)
    if start is None:start=time.monotonic()
    kappa,h=ref()
    edges=np.linspace(0,TOP,201);ub,_=target(DOMAIN_LO,DOMAIN_HI);dv,uv,_=solve(edges,DOMAIN_LO,DOMAIN_HI,ub)
    worst=-math.inf;v=0;dpworst=-math.inf
    for j in range(20000):
        ts=[rng.random()*math.pi/2 for _ in range(CHAIN)];roles=[rng.randrange(2) for _ in range(CHAIN)];H=rng.uniform(DOMAIN_LO,DOMAIN_HI)
        ys=[H-h(t) if r else h(t) for r,t in zip(roles,ts)]
        exact=h(ts[0])+h(ts[-1])+sum(kappa(ts[i],ts[i+1],ys[i+1]-ys[i]) for i in range(CHAIN-1))
        ix=np.minimum(199,np.searchsorted(edges,ts,side='right')-1)
        # Fixed-path DP bound: same downward endpoint and edge terms as C DP.
        def hl(k):
            return LIB.h_lower(edges[k],edges[k+1])
        lower=hl(ix[0])
        for i in range(CHAIN-1):
            aa,bb=ix[i],ix[i+1]
            lower=math.nextafter(lower+LIB.gap(edges[aa],edges[aa+1],edges[bb],edges[bb+1],DOMAIN_LO,DOMAIN_HI,roles[i],roles[i+1]),-math.inf)
        lower=math.nextafter(lower+hl(ix[-1]),-math.inf)
        err=lower-exact;worst=max(worst,err);v+=err>0
        global_d=dv if any(roles[i]==roles[i+1] for i in range(CHAIN-1)) else uv
        dpworst=max(dpworst,global_d-exact);v+=global_d>exact
    log(GATE_LOG,f'gate4 chains=20000 violations={v} max_path_bound_minus_reference={worst:.17g} max_global_DP_minus_reference={dpworst:.17g} PASS={v==0} seconds={time.monotonic()-start:.3f}')
    if v:raise RuntimeError('Gate 4 failed')

def full_run():
    start=time.monotonic()
    budget=ROOT/f'budget-n{CHAIN}.json'
    start_epoch=json.loads(budget.read_text())['start_epoch'] if budget.exists() else time.time()
    deadline=start+max(0,HARD_STOP-(time.time()-start_epoch));bottom_deadline=min(deadline,start+max(0,HARD_STOP/4-(time.time()-start_epoch)))
    boundaries=[H0+i*.0005 for i in range(round((DOMAIN_HI-H0)/.0005)+1)];boundaries[0]=DOMAIN_LO;boundaries[-1]=DOMAIN_HI
    # Descending scheduling leaves broad high-H coverage even if the bottom stalls.
    queue=[(a,b,0, min(deadline,bottom_deadline) if a<H0+.005 else deadline) for a,b in reversed(list(zip(boundaries[:-1],boundaries[1:])))]
    leaves=[];attempts=[];pending={};timed_out=False;bottom_stopped=False
    name=f'run-n{CHAIN}.log';certpath=ROOT/f'certificate-n{CHAIN}.json'
    (ROOT/name).write_text('# Ha Hb cells rounds D F_n_ub margin seconds status reason depth\n')
    def save():
        obj={'format':1,'n':CHAIN,'domain':[DOMAIN_LO,DOMAIN_HI],'workers':6,'hard_stop_seconds':HARD_STOP,'bottom_budget_seconds':HARD_STOP/4,'wall_seconds':time.monotonic()-start,'total_wall_seconds':time.time()-start_epoch,'timed_out':timed_out,'source_sha256':source_hashes(),'slices':sorted(leaves,key=lambda r:r['Ha']),'superseded_attempts':attempts}
        p=certpath.with_suffix('.json.tmp');p.write_text(json.dumps(obj,indent=2)+'\n');p.replace(certpath)
    ctx=mp.get_context('spawn')
    try:
        while queue or pending:
            now=time.monotonic()
            if now>=deadline:timed_out=True
            while queue and len(pending)<6 and not timed_out:
                job=queue.pop(0)
                if job[0]<H0+.005 and (bottom_stopped or now>=bottom_deadline):
                    leaves.append({'Ha':job[0],'Hb':job[1],'depth':job[2],'proved':False,'reason':'bottom_stop','history':[]});continue
                output=ctx.Queue();proc=ctx.Process(target=slice_worker,args=(job,output));proc.start();pending[proc]=(job,output)
            for proc,(job,output) in list(pending.items()):
                try:r=output.get_nowait()
                except queue_module.Empty:
                    if time.monotonic()<job[3] and proc.is_alive():continue
                    proc.terminate();proc.join()
                    r={'Ha':job[0],'Hb':job[1],'depth':job[2],'proved':False,'reason':'deadline' if time.monotonic()>=job[3] else 'worker_failure','seconds':0,'history':[]}
                else:proc.join()
                del pending[proc];output.close()
                if 'error' in r:raise RuntimeError(r['error'])
                split=not r['proved'] and r['reason']!='deadline' and (r['Hb']-r['Ha'])/2>=1e-4
                status='SPLIT' if split else ('PROVED' if r['proved'] else 'UNPROVED')
                log(name,f"{r['Ha']:.17g} {r['Hb']:.17g} {r.get('cells',0)} {r.get('rounds',0)} {r.get('D',float('nan')):.17g} {r.get('F_n_ub',float('nan')):.17g} {r.get('margin',float('nan')):.17g} {r['seconds']:.3f} {status} {r['reason']} {r['depth']}")
                if split:
                    attempts.append(r);mid=(r['Ha']+r['Hb'])/2
                    queue.extend([(r['Ha'],mid,r['depth']+1,job[3]),(mid,r['Hb'],r['depth']+1,job[3])])
                else:
                    leaves.append(r)
                    if not r['proved'] and r['Ha']<H0+.005:bottom_stopped=True
                save()
            if timed_out:
                for ha,hb,depth,_ in queue:leaves.append({'Ha':ha,'Hb':hb,'depth':depth,'proved':False,'reason':'deadline','history':[]})
                queue.clear()
            time.sleep(.1)
    finally:
        for proc in pending:proc.terminate();proc.join()
        save()
    log(name,f"# finished wall_seconds={time.monotonic()-start:.3f} proved={sum(r['proved'] for r in leaves)} unproved={sum(not r['proved'] for r in leaves)} timed_out={timed_out}")

def verify():
    cert=json.loads((ROOT/f'certificate-n{CHAIN}.json').read_text());rows=cert['slices']
    assert cert['source_sha256']==source_hashes(),'source mismatch'
    end=DOMAIN_LO
    for i,r in enumerate(rows):
        assert r['Ha']==end and r['Hb']>end,'coverage gap/overlap';end=r['Hb']
        if not r['proved']:continue
        e=r['edges'];assert e[0]==0 and e[-1]==TOP and all(a<b for a,b in zip(e,e[1:])) and len(e)==r['cells']+1
        ub=LIB.target(CHAIN,r['phi'],r['Ha'],r['Hb']);d,_,_=solve(e,r['Ha'],r['Hb'],ub)
        assert ub==r['F_n_ub'] and d==r['D'] and math.nextafter(d-ub,-math.inf)==r['margin'] and r['margin']>0
        log(f'verify-n{CHAIN}.log',f'slice={i} D={d:.17g} F_n_ub={ub:.17g} PASS=True')
    assert end==DOMAIN_HI
    log(f'verify-n{CHAIN}.log',f"replay PASS n={CHAIN} proved={sum(r['proved'] for r in rows)} unproved={sum(not r['proved'] for r in rows)} coverage=[{DOMAIN_LO!r},{DOMAIN_HI!r}]")


def gates():
    (ROOT/'budget-n6.json').write_text(json.dumps({'start_epoch':time.time(),'seconds':HARD_STOP}))
    (ROOT/GATE_LOG).write_text('n=6 gates 3 and 4; range=[%r,%r]; hard_stop_seconds=7200\n' % (DOMAIN_LO,DOMAIN_HI))
    enforce_budget()
    gate3()
    gate4()

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('mode',choices=['gates','run','verify'])
    args=p.parse_args()
    if args.mode!='gates':enforce_budget()
    {'gates':gates,'run':full_run,'verify':verify}[args.mode]()
