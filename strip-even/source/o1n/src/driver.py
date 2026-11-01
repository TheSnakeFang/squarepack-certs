#!/usr/bin/env python3
"""Certified even-n chain DP; run from o1n with ../.venv/bin/python."""
import argparse, ast, ctypes as ct, json, math, multiprocessing as mp
import os, pathlib, random, time, traceback, hashlib, queue as queue_module, resource
import numpy as np
from scipy.optimize import minimize, minimize_scalar
ROOT=pathlib.Path(__file__).resolve().parent.parent
LIB=ct.CDLL(str(ROOT/'src/kernel.dylib'))
D=ct.c_double; I=ct.c_int; P=ct.POINTER(D)
LIB.point.argtypes=[D,D,D]; LIB.point.restype=D
LIB.gap.argtypes=[D,D,D,D,D,D,I,I]; LIB.gap.restype=D
LIB.target.argtypes=[I,D,D,D]; LIB.target.restype=D
LIB.h_lower.argtypes=[D,D]; LIB.h_lower.restype=D
LIB.solve.argtypes=[I,I,P,D,D,P,ct.POINTER(ct.c_ubyte)]; LIB.solve.restype=I
TOP=math.nextafter(math.pi/2,math.inf)
CHAIN=int(os.environ.get("O1N_N",8))
H0={6:1.87,8:1.855,10:1.850}[CHAIN]
DOMAIN_LO=math.nextafter(H0,-math.inf)
GATE_LOG=f"gates-n{CHAIN}.log"
def log(name,msg):
    with (ROOT/name).open('a') as f: f.write(msg+'\n'); f.flush()
    print(msg,flush=True)
def ref():
    # Import only the unmodified reference function definitions; its top-level
    # code otherwise launches a search and imports an unrelated target module.
    p=pathlib.Path(os.environ.get('O1DP_M4CHECK',str(ROOT/'../runs/openmath-2026-10-27/m4check.py')))
    if not p.is_file():
        raise FileNotFoundError(f'm4check reference not found: {p}; default is {ROOT/"../runs/openmath-2026-10-27/m4check.py"}; set O1DP_M4CHECK to an existing m4check.py')
    lines=p.read_text().splitlines()[:29]
    ns={}
    exec('\n'.join(x for x in lines if not x.startswith(('from targets','sys.path','import numpy','from scipy'))),ns)
    return ns['kappa'],ns['h']
def chain_value(ts,roles,H,reference=False):
    fn,h=ref() if reference else (LIB.point,lambda t:(math.cos(t)+math.sin(t))/2)
    hs=[h(t) for t in ts];ys=[H-v if r else v for r,v in zip(roles,hs)]
    return hs[0]+hs[-1]+sum(fn(ts[i],ts[i+1],ys[i+1]-ys[i]) for i in range(len(ts)-1))
def morandi(phi,H,n=None):
    n=CHAIN if n is None else n
    return chain_value([0]+[phi]*(n-2)+[0],[i%2 for i in range(n)],H)
def target(ha,hb=None):
    hb=ha if hb is None else hb
    opt=minimize_scalar(lambda phi:morandi(phi,(ha+hb)/2),bounds=(.001,math.pi/2-.001),method='bounded',options={'xatol':1e-14})
    return LIB.target(CHAIN,opt.x,ha,hb),float(opt.x)
def solve(edges,ha,hb,ub):
    e=np.ascontiguousarray(edges,dtype=np.float64);out=np.array([0.,0.,ub]);bind=np.zeros(len(e)-1,dtype=np.uint8)
    rc=LIB.solve(CHAIN,len(bind),e.ctypes.data_as(P),ha,hb,out.ctypes.data_as(P),bind.ctypes.data_as(ct.POINTER(ct.c_ubyte)))
    if rc:raise MemoryError('C solve allocation')
    return float(out[0]),float(out[1]),bind

def lemma_gate():
    # Extended-precision evaluation of all four individual facet terms,
    # independent of LIB.gap and its interval/ratio implementation.
    rng=np.random.default_rng(20261030);n=200000;T=np.longdouble
    W=rng.uniform(0,1,n).astype(T)
    W[:n//4]=np.power(T(10),rng.uniform(-6,-3,n//4).astype(T))
    t=rng.random(n).astype(T)*W;t1=rng.random(n).astype(T)*W
    H=rng.uniform(H0,2,n).astype(T);H[n//4:n//2]=2
    pi2=np.arccos(T(0));bound=1-T(3)*W/4-W*W/4
    worst=T(np.inf);violations=0
    for mirror in (False,True):
        a,b=(pi2-t,pi2-t1) if mirror else (t,t1)
        sup=(1+np.cos(a-b)+np.abs(np.sin(a-b)))/2
        hs=(np.cos(a)+np.sin(a)+np.cos(b)+np.sin(b))/2
        dy=H-hs if mirror else hs-H
        for owner in (a,b):
            nx=np.cos(owner) if mirror else np.sin(owner)
            ny=np.sin(owner) if mirror else -np.cos(owner)
            exact=(sup-dy*ny)/nx
            slack=exact-bound;worst=min(worst,slack.min())
            violations+=int(np.count_nonzero(slack<0))
    log(GATE_LOG,f'lemma_gate triples={n} terms={4*n} H2={n//4} W_le_1e-3={n//4} violations={violations} min_term_minus_lemma={float(worst):.17g} PASS={violations==0}')
    if violations:raise RuntimeError('Pointwise lemma gate failed')

def gates():
    (ROOT/f"budget-n{CHAIN}.json").write_text(json.dumps({"start_epoch":time.time(),"seconds":21600}))
    rng=random.Random(20261029); kappa,h=ref(); start=time.monotonic()
    log(GATE_LOG,'Gates 1,2,lemma,5,3,4 start seed=20261029 libm_padding=8 ulps corner_pair_boxes=25000 H2_corner_boxes=12500')
    worst=0
    for _ in range(100000):
        a,b=rng.random()*math.pi/2,rng.random()*math.pi/2;dy=rng.uniform(-1,1)
        worst=max(worst,abs(LIB.point(a,b,dy)-kappa(a,b,dy)))
    log(GATE_LOG,f'gate1 samples=100000 max_abs_error={worst:.17g} PASS={worst<=1e-11}')
    if worst>1e-11:raise RuntimeError('Gate 1 failed')
    worst=-math.inf;violations=0
    for j in range(50000):
        wa,wb=[10**rng.uniform(-4,math.log10(.3)) for _ in range(2)]
        if j<25000:
            wa,wb=[10**rng.uniform(-8,math.log10(.3)) for _ in range(2)]
            # Both cells are wholly in the SAME named corner region.
            a,c=rng.uniform(0,.3-wa),rng.uniform(0,.3-wb)
            b,d=a+wa,c+wb
            if rng.random()<.5:
                a,b,c,d=math.pi/2-b,math.pi/2-a,math.pi/2-d,math.pi/2-c
            ha=rng.uniform(1.999,2);hb=2 if j%2==0 else rng.uniform(ha,2)
        else:
            a,c=rng.uniform(0,math.pi/2-wa),rng.uniform(0,math.pi/2-wb);b,d=a+wa,c+wb
            ha=rng.uniform(H0,2);hb=rng.uniform(ha,2)
        r,s=rng.randrange(2),rng.randrange(2)
        lower=LIB.gap(a,b,c,d,ha,hb,r,s)
        for _ in range(64):
            t,u,H=rng.uniform(a,b),rng.uniform(c,d),rng.uniform(ha,hb)
            y0=H-h(t) if r else h(t);y1=H-h(u) if s else h(u)
            delta=lower-kappa(t,u,y1-y0);worst=max(worst,delta);violations+=delta>0
        if (j+1)%5000==0:log(GATE_LOG,f'gate2 progress boxes={j+1} violations={violations} max_G_minus_reference={worst:.17g}')
    log(GATE_LOG,f'gate2 boxes=50000 interior_samples=3200000 violations={violations} max_G_minus_reference={worst:.17g} PASS={violations==0}')
    if violations:raise RuntimeError('Gate 2 failed')
    lemma_gate()
    gate5()
    gate3()
    gate4(rng,start)

def gate4(rng=None,start=None):
    if rng is None:rng=random.Random(20261030)
    if start is None:start=time.monotonic()
    kappa,h=ref()
    edges=np.linspace(0,TOP,201);ub,_=target(DOMAIN_LO,2);dv,uv,_=solve(edges,DOMAIN_LO,2,ub)
    worst=-math.inf;v=0;dpworst=-math.inf
    for j in range(20000):
        ts=[rng.random()*math.pi/2 for _ in range(CHAIN)];roles=[rng.randrange(2) for _ in range(CHAIN)];H=rng.uniform(H0,2)
        ys=[H-h(t) if r else h(t) for r,t in zip(roles,ts)]
        exact=h(ts[0])+h(ts[-1])+sum(kappa(ts[i],ts[i+1],ys[i+1]-ys[i]) for i in range(CHAIN-1))
        ix=np.minimum(199,np.searchsorted(edges,ts,side='right')-1)
        # Fixed-path DP bound: same downward endpoint and edge terms as C DP.
        def hl(k):
            return LIB.h_lower(edges[k],edges[k+1])
        lower=hl(ix[0])
        for i in range(CHAIN-1):
            aa,bb=ix[i],ix[i+1]
            lower=math.nextafter(lower+LIB.gap(edges[aa],edges[aa+1],edges[bb],edges[bb+1],DOMAIN_LO,2,roles[i],roles[i+1]),-math.inf)
        lower=math.nextafter(lower+hl(ix[-1]),-math.inf)
        err=lower-exact;worst=max(worst,err);v+=err>0
        global_d=dv if any(roles[i]==roles[i+1] for i in range(CHAIN-1)) else uv
        dpworst=max(dpworst,global_d-exact);v+=global_d>exact
    log(GATE_LOG,f'gate4 chains=20000 violations={v} max_path_bound_minus_reference={worst:.17g} max_global_DP_minus_reference={dpworst:.17g} PASS={v==0} seconds={time.monotonic()-start:.3f}')
    if v:raise RuntimeError('Gate 4 failed')

def slice_job(job):
    ha,hb,depth,deadline=job;start=time.monotonic();ub,theta=target(ha,hb)
    edges=np.linspace(0,TOP,201)
    if 1.99<hb<2:
        # Same interval kernel, nonuniform cover: resolve nearly singular
        # normals with endpoint widths proportional to the remaining H gap.
        near=[];x=(2-hb)/32
        while x<TOP/2:
            near.append(x);x*=1.08
        edges=np.unique(np.r_[edges,near,[TOP-x for x in near]])
    history=[];stalled=0;reason='round_limit'
    for rnd in range(1,8):
        if time.monotonic()>=deadline:reason='deadline';break
        d,u,binding=solve(edges,ha,hb,ub);margin=math.nextafter(d-ub,-math.inf)
        history.append({'cells':len(edges)-1,'D':d,'unconstrained':u,'margin':margin,'binding_cells':int(binding.sum())})
        if margin>0:reason='proved';break
        if len(history)>1:
            gain=d-history[-2]['D']
            stalled=stalled+1 if gain<1e-4 else 0
        if stalled>=2:reason='stalled';break
        if len(edges)-1>=6400:reason='cell_limit';break
        if rnd==7:reason='round_limit';break
        # A global cell list shared by all chain positions. The C backward
        # pass conditions on the prefix flag; it only accepts final flag 1.
        mids=(edges[:-1]+edges[1:])*.5
        refined=np.sort(np.r_[edges,mids[binding.astype(bool)]])
        if len(refined)>6401:reason='cell_limit';break
        edges=refined
        if len(edges)==history[-1]['cells']+1:reason='no_binding';break
    if not history:
        return {'Ha':ha,'Hb':hb,'depth':depth,'proved':False,'reason':reason,'seconds':time.monotonic()-start,'history':[]}
    last=history[-1]
    return {'Ha':ha,'Hb':hb,'depth':depth,'proved':reason=='proved','reason':reason,'cells':last['cells'],'rounds':len(history),'D':last['D'],'F_n_ub':ub,'phi':theta,'margin':last['margin'],'seconds':time.monotonic()-start,'edges':edges.tolist(),'history':history}


def regression():
    global CHAIN
    old=CHAIN;CHAIN=6
    rows=json.loads((ROOT/'../o1dp/certificate.json').read_text())['slices']
    for ix in (0,len(rows)//2,len(rows)-1):
        r=rows[ix];start=time.monotonic();d,u,_=solve(r['edges'],r['Ha'],r['Hb'],r['F6_ub'])
        ok=d==r['D']
        log('regression-n6.log',f"slice={ix} Ha={r['Ha']:.17g} Hb={r['Hb']:.17g} cells={r['cells']} D={d:.17g} reference_D={r['D']:.17g} error={d-r['D']:.17g} PASS={ok} seconds={time.monotonic()-start:.3f}")
        if not ok:raise RuntimeError('n=6 saved-grid regression failed')
    CHAIN=old

def gate5():
    rng=np.random.default_rng(20261101);worst=-math.inf;point_worst=-math.inf;violations=0
    for j in range(1000):
        n=int(rng.choice([6,8,10]));lo={6:1.87,8:1.855,10:1.85}[n]
        ha=float(rng.uniform(lo,2));hb=float(rng.uniform(ha,2));phi=float(rng.uniform(.001,math.pi/2-.001))
        ub=LIB.target(n,phi,ha,hb)
        for H in np.linspace(ha,hb,50):
            err=morandi(phi,float(H),n)-ub;worst=max(worst,err);violations+=err>0
        point=LIB.target(n,phi,ha,ha);err=point-morandi(phi,ha,n);point_worst=max(point_worst,err);violations+=err<0 or err>1e-12
    log(GATE_LOG,f'gate5 cases=1000 samples=50000 violations={violations} max_chain_minus_upper={worst:.17g} max_point_excess={point_worst:.17g} PASS={violations==0}')
    if violations:raise RuntimeError('Gate 5 failed')

def gate3():
    rng=np.random.default_rng(20261101);start=time.monotonic()
    for ha,hb in [(DOMAIN_LO,H0+.005),(1.9,1.91)]:
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

def source_hashes():
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'src/kernel.c',ROOT/'src/driver.py',ROOT/'SPEC.md']}

def full_run():
    start=time.monotonic()
    budget=ROOT/f'budget-n{CHAIN}.json'
    start_epoch=json.loads(budget.read_text())['start_epoch'] if budget.exists() else time.time()
    deadline=start+max(0,21600-(time.time()-start_epoch));bottom_deadline=min(deadline,start+5400)
    boundaries=[H0+i*.001 for i in range(round((2-H0)/.001)+1)];boundaries[0]=DOMAIN_LO;boundaries[-1]=2.
    # Descending scheduling leaves broad high-H coverage even if the bottom stalls.
    queue=[(a,b,0, min(deadline,bottom_deadline) if a<H0+.005 else deadline) for a,b in reversed(list(zip(boundaries[:-1],boundaries[1:])))]
    leaves=[];attempts=[];pending={};timed_out=False;bottom_stopped=False
    name=f'run-n{CHAIN}.log';certpath=ROOT/f'certificate-n{CHAIN}.json'
    (ROOT/name).write_text('# Ha Hb cells rounds D F_n_ub margin seconds status reason depth\n')
    def save():
        obj={'format':1,'n':CHAIN,'domain':[DOMAIN_LO,2.],'workers':6,'hard_stop_seconds':21600,'bottom_budget_seconds':5400,'wall_seconds':time.monotonic()-start,'total_wall_seconds':time.time()-start_epoch,'timed_out':timed_out,'source_sha256':source_hashes(),'slices':sorted(leaves,key=lambda r:r['Ha']),'superseded_attempts':attempts}
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

def slice_worker(job,output):
    try:
        r=slice_job(job);r["peak_rss_bytes"]=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;output.put(r)
    except BaseException:output.put({'error':traceback.format_exc()})

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
    assert end==2
    log(f'verify-n{CHAIN}.log',f"replay PASS n={CHAIN} proved={sum(r['proved'] for r in rows)} unproved={sum(not r['proved'] for r in rows)} coverage=[{DOMAIN_LO!r},2]")

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['regression','gates','gate3','gate4','gate5','run','verify']);p.add_argument('--n',type=int,choices=[6,8,10],default=CHAIN);a=p.parse_args()
    CHAIN=a.n;os.environ['O1N_N']=str(CHAIN);H0={6:1.87,8:1.855,10:1.85}[CHAIN];DOMAIN_LO=math.nextafter(H0,-math.inf);GATE_LOG=f'gates-n{CHAIN}.log'
    {'regression':regression,'gates':gates,'gate3':gate3,'gate4':gate4,'gate5':gate5,'run':full_run,'verify':verify}[a.mode]()
