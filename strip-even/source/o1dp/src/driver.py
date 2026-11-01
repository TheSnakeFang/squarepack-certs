#!/usr/bin/env python3
"""Run from o1dp: ../.venv/bin/python src/driver.py {gates,diagnostic}."""
import argparse, ast, ctypes as ct, json, math, multiprocessing as mp
import os, pathlib, random, time, traceback, hashlib, concurrent.futures
import numpy as np
from scipy.optimize import minimize, minimize_scalar
ROOT=pathlib.Path(__file__).resolve().parent.parent
LIB=ct.CDLL(str(ROOT/'src/kernel.dylib'))
D=ct.c_double; I=ct.c_int; P=ct.POINTER(D)
LIB.point.argtypes=[D,D,D]; LIB.point.restype=D
LIB.gap.argtypes=[D,D,D,D,D,D,I,I]; LIB.gap.restype=D
LIB.target.argtypes=[D,D]; LIB.target.restype=D
LIB.h_lower.argtypes=[D,D]; LIB.h_lower.restype=D
LIB.solve.argtypes=[I,P,D,D,P,ct.POINTER(ct.c_ubyte)]; LIB.solve.restype=I
TOP=math.nextafter(math.pi/2,math.inf)
DOMAIN_LO=math.nextafter(1.87,-math.inf)
def log(name,msg):
    with (ROOT/name).open('a') as f: f.write(msg+'\n'); f.flush()
    print(msg,flush=True)
def ref():
    # Import only the unmodified reference function definitions; its top-level
    # code otherwise launches a search and imports an unrelated target module.
    p=pathlib.Path(os.environ.get('O1DP_M4CHECK',str(ROOT/'../runs/openmath-2026-10-27/m4check.py')))
    if not p.is_file():
        raise FileNotFoundError(f'm4check reference not found: {p}; default is {ROOT/"../runs/openmath-2026-10-27/m4check.py"}; set O1DP_M4CHECK to an existing m4check.py')
    tree=ast.parse(p.read_text()); nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('verts','kappa','h')]
    import itertools
    ns={'math':math,'itertools':itertools};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),ns)
    return ns['kappa'],ns['h']
def target(ha):
    f=lambda t:2+(4-(3*ha-2)*math.cos(t))/math.sin(t)+(4-2*ha*math.sin(t))/math.cos(t)
    opt=minimize_scalar(f,bounds=(.01,math.pi/2-.01),method='bounded',options={'xatol':1e-14})
    return LIB.target(opt.x,ha),float(opt.x)
def solve(edges,ha,hb,ub):
    e=np.ascontiguousarray(edges,dtype=np.float64);out=np.array([0.,0.,ub]);bind=np.zeros(len(e)-1,dtype=np.uint8)
    rc=LIB.solve(len(bind),e.ctypes.data_as(P),ha,hb,out.ctypes.data_as(P),bind.ctypes.data_as(ct.POINTER(ct.c_ubyte)))
    if rc:raise MemoryError('C solve allocation')
    return float(out[0]),float(out[1]),bind

def lemma_gate():
    # Extended-precision evaluation of all four individual facet terms,
    # independent of LIB.gap and its interval/ratio implementation.
    rng=np.random.default_rng(20261030);n=200000;T=np.longdouble
    W=rng.uniform(0,1,n).astype(T)
    W[:n//4]=np.power(T(10),rng.uniform(-6,-3,n//4).astype(T))
    t=rng.random(n).astype(T)*W;t1=rng.random(n).astype(T)*W
    H=rng.uniform(1.87,2,n).astype(T);H[n//4:n//2]=2
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
    log('gates.log',f'lemma_gate triples={n} terms={4*n} H2={n//4} W_le_1e-3={n//4} violations={violations} min_term_minus_lemma={float(worst):.17g} PASS={violations==0}')
    if violations:raise RuntimeError('Pointwise lemma gate failed')

def gates():
    rng=random.Random(20261029); kappa,h=ref(); start=time.monotonic()
    log('gates.log','Near-upright lemma gates (i),1,2,4 start seed=20261029 libm_padding=8 ulps corner_pair_boxes=25000 H2_corner_boxes=12500')
    lemma_gate()
    worst=0
    for _ in range(100000):
        a,b=rng.random()*math.pi/2,rng.random()*math.pi/2;dy=rng.uniform(-1,1)
        worst=max(worst,abs(LIB.point(a,b,dy)-kappa(a,b,dy)))
    log('gates.log',f'gate1 samples=100000 max_abs_error={worst:.17g} PASS={worst<=1e-11}')
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
            ha=rng.uniform(1.87,2);hb=rng.uniform(ha,2)
        r,s=rng.randrange(2),rng.randrange(2)
        lower=LIB.gap(a,b,c,d,ha,hb,r,s)
        for _ in range(64):
            t,u,H=rng.uniform(a,b),rng.uniform(c,d),rng.uniform(ha,hb)
            y0=H-h(t) if r else h(t);y1=H-h(u) if s else h(u)
            delta=lower-kappa(t,u,y1-y0);worst=max(worst,delta);violations+=delta>0
        if (j+1)%5000==0:log('gates.log',f'gate2 progress boxes={j+1} violations={violations} max_G_minus_reference={worst:.17g}')
    log('gates.log',f'gate2 boxes=50000 interior_samples=3200000 violations={violations} max_G_minus_reference={worst:.17g} PASS={violations==0}')
    if violations:raise RuntimeError('Gate 2 failed')
    gate4(rng,start)

def gate4(rng=None,start=None):
    if rng is None:rng=random.Random(20261030)
    if start is None:start=time.monotonic()
    kappa,h=ref()
    edges=np.linspace(0,TOP,201);ub,_=target(1.87);dv,uv,_=solve(edges,1.87,2,ub)
    worst=-math.inf;v=0;dpworst=-math.inf
    for j in range(20000):
        ts=[rng.random()*math.pi/2 for _ in range(6)];roles=[rng.randrange(2) for _ in range(6)];H=rng.uniform(1.87,2)
        ys=[H-h(t) if r else h(t) for r,t in zip(roles,ts)]
        exact=h(ts[0])+h(ts[-1])+sum(kappa(ts[i],ts[i+1],ys[i+1]-ys[i]) for i in range(5))
        ix=np.minimum(199,np.searchsorted(edges,ts,side='right')-1)
        # Fixed-path DP bound: same downward endpoint and edge terms as C DP.
        def hl(k):
            return LIB.h_lower(edges[k],edges[k+1])
        lower=hl(ix[0])
        for i in range(5):
            aa,bb=ix[i],ix[i+1]
            lower=math.nextafter(lower+LIB.gap(edges[aa],edges[aa+1],edges[bb],edges[bb+1],1.87,2,roles[i],roles[i+1]),-math.inf)
        lower=math.nextafter(lower+hl(ix[-1]),-math.inf)
        err=lower-exact;worst=max(worst,err);v+=err>0
        global_d=dv if any(roles[i]==roles[i+1] for i in range(5)) else uv
        dpworst=max(dpworst,global_d-exact);v+=global_d>exact
    log('gates.log',f'gate4 chains=20000 violations={v} max_path_bound_minus_reference={worst:.17g} max_global_DP_minus_reference={dpworst:.17g} PASS={v==0} seconds={time.monotonic()-start:.3f}')
    if v:raise RuntimeError('Gate 4 failed')

def diagnostic():
    k,h=ref()
    rows=[]
    for H in (1.87,1.875):
        ub,theta=target(H);phi=math.pi/2-theta
        ts=[0,phi,phi,phi,phi,0];rs=[0,1,0,1,0,1]
        ys=[H-h(t) if r else h(t) for r,t in zip(rs,ts)]
        value=h(ts[0])+h(ts[-1])+sum(k(ts[i],ts[i+1],ys[i+1]-ys[i]) for i in range(5))
        rows.append({'H':H,'L_upper':ub,'theta':theta,'tilts':ts,'reference_Phi':value})
    print(json.dumps(rows,indent=2))

def gate3():
    start=time.monotonic(); k,h=ref(); rng=np.random.default_rng(20261030)
    def chain(x,roles,reference=False):
        ts=x[:6]; H=x[6]; hs=[h(t) for t in ts]
        ys=[H-v if r else v for r,v in zip(roles,hs)]
        fn=k if reference else LIB.point
        return hs[0]+hs[-1]+sum(fn(ts[i],ts[i+1],ys[i+1]-ys[i]) for i in range(5))
    best=6.; witness=([0]*6+[1.87],[0]*6); count=0
    # Include the exact all-upright feasible witness, every nonalternating
    # pattern, random starts, and bounded local searches. This is an upper
    # witness diagnostic only, never a certified lower bound.
    for mask in range(64):
        roles=[(mask>>i)&1 for i in range(6)]
        if all(roles[i]!=roles[i+1] for i in range(5)):continue
        for trial in range(2):
            x=np.r_[rng.uniform(0,math.pi/2,6),rng.uniform(1.87,1.875)]
            opt=minimize(lambda x:chain(x,roles),x,method='Powell',bounds=[(0,math.pi/2)]*6+[(1.87,1.875)],options={'maxiter':120,'xtol':1e-8,'ftol':1e-10})
            value=chain(opt.x,roles,True);count+=1
            if value<best:best=value;witness=(opt.x.tolist(),roles)
    log('gates.log',f'gate3b search local_runs={count} best_reference_nonmorandi={best:.17g} witness={json.dumps(witness)}')
    passed=True
    for ha,hb in [(1.87,1.875),(1.87,1.87)]:
        ub,_=target(ha);limit,_=target(hb);prev=-math.inf
        for n in [200,400,800,1600,3200]:
            d,u,_=solve(np.linspace(0,TOP,n+1),ha,hb,ub)
            ok=u<=limit and u>=prev and d<=best+1e-12
            if ha==hb:ok=ok and d<=6+1e-12
            passed &= ok
            log('gates.log',f'gate3 slice=[{ha},{hb}] cells={n} unconstrained={u:.17g} F6_Hb_upper={limit:.17g} deficit={limit-u:.17g} flagged={d:.17g} flagged_to_6={6-d:.17g} PASS={ok}')
            prev=u
    log('gates.log',f'gate3 PASS={passed} seconds={time.monotonic()-start:.3f}')
    if not passed:raise RuntimeError('Gate 3 failed')

def slice_job(job):
    ha,hb,depth,deadline=job;start=time.monotonic();ub,theta=target(ha)
    edges=np.linspace(0,TOP,201)
    if 1.99<hb<2:
        # Same interval kernel, nonuniform cover: resolve nearly singular
        # normals with endpoint widths proportional to the remaining H gap.
        near=[];x=(2-hb)/32
        while x<TOP/2:
            near.append(x);x*=1.08
        edges=np.unique(np.r_[edges,near,[TOP-x for x in near]])
    history=[];stalled=0;reason='round_limit'
    for rnd in range(1,10):
        if time.monotonic()>=deadline:reason='deadline';break
        d,u,binding=solve(edges,ha,hb,ub);margin=math.nextafter(d-ub,-math.inf)
        history.append({'cells':len(edges)-1,'D':d,'unconstrained':u,'margin':margin,'binding_cells':int(binding.sum())})
        if margin>0:reason='proved';break
        if len(history)>1:
            gain=d-history[-2]['D']
            stalled=stalled+1 if gain<1e-4 else 0
        if stalled>=2:reason='stalled';break
        if len(edges)-1>=6400:reason='cell_limit';break
        if rnd==9:reason='round_limit';break
        # A global cell list shared by all six positions. The C backward
        # pass conditions on the prefix flag; it only accepts final flag 1.
        mids=(edges[:-1]+edges[1:])*.5
        refined=np.sort(np.r_[edges,mids[binding.astype(bool)]])
        if len(refined)>6401:reason='cell_limit';break
        edges=refined
        if len(edges)==history[-1]['cells']+1:reason='no_binding';break
    if not history:
        return {'Ha':ha,'Hb':hb,'depth':depth,'proved':False,'reason':reason,'seconds':time.monotonic()-start,'history':[]}
    last=history[-1]
    return {'Ha':ha,'Hb':hb,'depth':depth,'proved':reason=='proved','reason':reason,'cells':last['cells'],'rounds':len(history),'D':last['D'],'F6_ub':ub,'theta':theta,'margin':last['margin'],'seconds':time.monotonic()-start,'edges':edges.tolist(),'history':history}

def full_run(resume=False):
    start=time.monotonic()
    start_epoch=time.time()
    # Decimal-derived boundaries avoid accumulated stepping error; adjacent
    # slices reuse identical binary64 boundary values.
    boundaries=[1.87+i*.002 for i in range(65)]+[2.]
    boundaries[0]=DOMAIN_LO
    leaves=[];attempts=[];pending={}; timed_out=False
    if resume:
        previous=json.loads((ROOT/'certificate.json').read_text())
        # The initial run's console file was created immediately before it
        # launched. Preserve that wall clock across this implementation retry.
        start_epoch=previous.get('start_epoch',(ROOT/'full-console.log').stat().st_birthtime)
        start=time.monotonic()-(time.time()-start_epoch)
        leaves=[r for r in previous['slices'] if r['proved']]
        attempts=previous['superseded_attempts']+[r for r in previous['slices'] if not r['proved']]
        log('run.log','# RESUME endpoint-graded grids; original eight-hour deadline retained; unfinished jobs discarded')
    else:
        (ROOT/'run.log').write_text('# Ha Hb cells rounds D F6_ub margin seconds status reason depth\n')
    deadline=start+8*3600
    if resume:
        gaps=[];end=DOMAIN_LO
        for r in sorted(leaves,key=lambda r:r['Ha']):
            if r['Ha']>end:gaps.append((end,r['Ha']))
            end=r['Hb']
        if end<2:gaps.append((end,2.))
        queue=[(a,b,0,deadline) for a,b in gaps]
    else:queue=[(a,b,0,deadline) for a,b in zip(boundaries[:-1],boundaries[1:])]
    def save():
        obj={'format':1,'domain':[DOMAIN_LO,2.],'start_epoch':start_epoch,'workers':6,'hard_stop_seconds':28800,'wall_seconds':time.monotonic()-start,'timed_out':timed_out,'assumptions':['IEEE-754 binary64, no fast-math or reassociation','libm sin/cos/sqrt error <= 8 ulps','SPEC vertex reduction and F6 monotonicity'],'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'src/kernel.c',ROOT/'src/driver.py',ROOT/'SPEC.md']},'slices':sorted(leaves,key=lambda r:r['Ha']),'superseded_attempts':attempts}
        temp=ROOT/'certificate.json.tmp';temp.write_text(json.dumps(obj,indent=2)+'\n');temp.replace(ROOT/'certificate.json')
    pool=concurrent.futures.ProcessPoolExecutor(max_workers=6)
    try:
        while queue or pending:
            if time.monotonic()>=deadline:timed_out=True;break
            while queue and len(pending)<6:
                job=queue.pop(0);pending[pool.submit(slice_job,job)]=job
            done,_=concurrent.futures.wait(pending,timeout=1,return_when=concurrent.futures.FIRST_COMPLETED)
            for future in done:
                job=pending.pop(future);r=future.result()
                split=not r['proved'] and r['reason']!='deadline' and r['depth']<11 and r['Hb']-r['Ha']>1e-6
                status='SPLIT' if split else ('PROVED' if r['proved'] else 'UNPROVED')
                log('run.log',f"{r['Ha']:.17g} {r['Hb']:.17g} {r.get('cells',0)} {r.get('rounds',0)} {r.get('D',float('nan')):.17g} {r.get('F6_ub',float('nan')):.17g} {r.get('margin',float('nan')):.17g} {r['seconds']:.3f} {status} {r['reason']} {r['depth']}")
                if split:
                    attempts.append(r);mid=(r['Ha']+r['Hb'])/2
                    queue.extend([(r['Ha'],mid,r['depth']+1,deadline),(mid,r['Hb'],r['depth']+1,deadline)])
                else:leaves.append(r)
                save()
        if timed_out:
            for future,job in pending.items():future.cancel();queue.append(job)
            # Terminate native C calls as well as Python workers at the hard
            # wall-clock limit. No unbounded executor shutdown wait.
            for proc in pool._processes.values():proc.terminate()
            for ha,hb,depth,_ in queue:leaves.append({'Ha':ha,'Hb':hb,'depth':depth,'proved':False,'reason':'deadline','history':[]})
    finally:
        pool.shutdown(wait=not timed_out,cancel_futures=True);save()
    log('run.log',f"# finished wall_seconds={time.monotonic()-start:.3f} proved={sum(r['proved'] for r in leaves)} unproved={sum(not r['proved'] for r in leaves)} timed_out={timed_out}")

def verify():
    def require(ok,message):
        if not ok:raise RuntimeError(f'certificate verification FAIL: {message}')
    def passed(group):print(f'{group} PASS',flush=True)
    cert=json.loads((ROOT/'certificate.json').read_text());rows=cert['slices']
    require(bool(rows),'no slices')
    for i,r in enumerate(rows):
        require(isinstance(r.get('edges'),list) and len(r['edges'])>=2,f'slice {i}: missing or empty saved grid (edges)')
        require(r.get('proved') is True,f'slice {i}: proved must be True')
    passed('saved grids and proved flags')
    require(cert.get('domain')==[DOMAIN_LO,2.],'recorded domain must be [predecessor(1.87), 2]')
    end=DOMAIN_LO
    for i,r in enumerate(rows):
        require(math.isfinite(r['Ha']) and math.isfinite(r['Hb']) and r['Ha']<r['Hb'],f'slice {i}: width must be positive and finite')
        require(r['Ha']==end,f'slice {i}: boundary mismatch ({r["Ha"]!r} != {end!r})')
        end=r['Hb']
    require(end==2.,f'coverage ends at {end!r}, expected 2')
    passed('positive widths, exact shared boundaries and domain coverage')
    for i,r in enumerate(rows):
        e=r['edges']
        require(e[0]==0 and e[-1]==TOP and all(a<b for a,b in zip(e[:-1],e[1:])),f'slice {i}: grid must strictly increase from 0 to nextafter(pi/2, +inf)')
        require(len(e)==r['cells']+1,f'slice {i}: grid/cell count mismatch')
    passed('grid endpoints, strict increase and cell counts')
    for i,r in enumerate(rows):
        require(math.isfinite(r['D']) and math.isfinite(r['F6_ub']),f'slice {i}: nonfinite stored bound')
        require(r['margin']==math.nextafter(r['D']-r['F6_ub'],-math.inf),f'slice {i}: margin is not downward-rounded D - F6_ub')
        require(r['margin']>0,f'slice {i}: proved margin must be positive')
    passed('exact downward-rounded positive margins')
    sources={'SPEC.md':ROOT/'SPEC.md','kernel.c':ROOT/'src/kernel.c',
             'driver.py':ROOT/'src/driver.py','replay_lemma.py':ROOT/'src/replay_lemma.py'}
    for name,path in sources.items():
        require(cert['source_sha256'].get(name)==hashlib.sha256(path.read_bytes()).hexdigest(),f'source hash mismatch: {name}')
    if 'README.md' in cert['source_sha256']:
        require(cert['source_sha256']['README.md']==hashlib.sha256((ROOT/'README.md').read_bytes()).hexdigest(),'source hash mismatch: README.md')
    passed('current source hashes')
    for name,update in [('certificate.before-ratio.json','ratio_update'),('certificate.before-lemma.json','lemma_update')]:
        digest=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
        require(cert['lemma_update']['preserved_backup_sha256'].get(name)==digest,f'preserved backup hash mismatch: {name}')
        require(cert[update]['previous_certificate_sha256']==digest,f'previous certificate hash mismatch: {name}')
    passed('both preserved backup certificate hashes')
    for i,r in enumerate(rows):
        ub,_=target(r['Ha']);d,_,_=solve(r['edges'],r['Ha'],r['Hb'],ub)
        require(d==r['D'],f'slice {i}: recomputed D {d!r} != stored {r["D"]!r}')
        require(ub==r['F6_ub'],f'slice {i}: recomputed F6_ub {ub!r} != stored {r["F6_ub"]!r}')
    passed('recomputed D and F6_ub exactly match stored values')
    print(f"certificate replay PASS: {len(rows)} slices; {sum(r['proved'] for r in rows)} proved",flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['gates','gate3','gate4','diagnostic','run','resume','verify']);a=p.parse_args()
    {'gates':gates,'gate3':gate3,'gate4':gate4,'diagnostic':diagnostic,'run':full_run,'resume':lambda:full_run(True),'verify':verify}[a.mode]()
