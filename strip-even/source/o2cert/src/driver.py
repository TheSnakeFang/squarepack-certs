#!/usr/bin/env python3
"""Certified O2 bounds. No package installs, network, or repository operations."""
import argparse, ctypes as ct, hashlib, heapq, json, math, multiprocessing as mp
import os, pathlib, time, functools, concurrent.futures, runpy
from decimal import Decimal, getcontext
import numpy as np
from scipy.optimize import minimize_scalar
ROOT=pathlib.Path(__file__).resolve().parent.parent
D=ct.c_double; P=ct.POINTER(D); LIB=ct.CDLL(str(ROOT/'src/kernel.dylib'))
for name,n in [('a_bound',4),('m_bound',2),('a_reference',2)]:
    f=getattr(LIB,name); f.argtypes=[D]*n+[ct.c_int];f.restype=D
LIB.m_reference.argtypes=[D];LIB.m_reference.restype=D
LIB.target.argtypes=[D,D];LIB.target.restype=D
LIB.dense_batch.argtypes=[ct.c_int,P,P,P]
LIB.dense_m_batch.argtypes=[ct.c_int,P,P]
LIB.inner.argtypes=[D]*7+[ct.c_int,ct.c_int,D,ct.POINTER(ct.c_int)];LIB.inner.restype=D
getcontext().prec=60
DN=lambda x:math.nextafter(x,-math.inf)
UP=lambda x:math.nextafter(x,math.inf)
def decimal_bound(s,upper):
    q=Decimal(s);f=float(q)
    if upper and Decimal(f)<q:f=UP(f)
    if not upper and Decimal(f)>q:f=DN(f)
    return f
TOP=decimal_bound('6.14',True); LOW=decimal_bound('-0.38',False); YTOP=decimal_bound('0.38',True)
J=(decimal_bound('0.740900',True),decimal_bound('1.15',False))
q=-Decimal(1)/Decimal('0.890900')-Decimal('0.15');f=float(q)
JE=(UP(f) if Decimal(f)<q else f,decimal_bound('-0.85',False))
H0=decimal_bound('1.87',False)
def log(name,msg):
    with (ROOT/name).open('a') as f:f.write(msg+'\n')
    print(msg,flush=True)
def save(path,obj):
    p=ROOT/path;t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n');t.replace(p)
def hashes():return {n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ('src/kernel.c','src/kernel.dylib','src/driver.py','src/verify_parallel.py','SPEC.md','LEMMAS.md')}
def ref():
    p=ROOT/'../runs/openmath-2026-10-27/m4check.py';ns={}
    text='\n'.join(l for l in p.read_text().splitlines()[:29] if not l.startswith(('from targets','sys.path','import numpy','from scipy')))
    exec(compile(text,str(p),'exec'),ns);return ns['kappa']
def L(t,h):return 2+(4-(3*h-2)*math.cos(t))/math.sin(t)+(4-2*h*math.sin(t))/math.cos(t)
def theta(h):return float(minimize_scalar(lambda t:L(t,h),bounds=(.3,1.2),method='bounded',options={'xatol':1e-15}).x)
def cells():
    e=[float(Decimal('1.87')+Decimal('.13')*i/8) for i in range(9)];e[0]=H0;e[-1]=2.
    return [(a,b) for a,b in zip(e,e[1:])]
def A(x,y):return LIB.a_reference(x,y,0)
def psi(r,h):
    x,y,z,w,u=r
    return LIB.m_reference(x)+LIB.m_reference(u)+A(x,y)+A(z,y)+A(z,w)+A(u,w)+h*(-x+y-z+w-u)
def dense_job(pair):
    x,y=pair;x=np.ascontiguousarray(x);y=np.ascontiguousarray(y);out=np.empty(len(x));LIB.dense_batch(len(x),x.ctypes.data_as(P),y.ctypes.data_as(P),out.ctypes.data_as(P));return out
def dense_m_job(x):
    x=np.ascontiguousarray(x);out=np.empty(len(x));LIB.dense_m_batch(len(x),x.ctypes.data_as(P),out.ctypes.data_as(P));return out

def gates(workers):
    start=time.monotonic();rng=np.random.default_rng(20261031);results={}
    log('gates.log',f'START seed=20261031 workers={workers} source_hashes={json.dumps(hashes())}')
    n=200000;x=rng.uniform(-8,8,n);y=rng.uniform(-8,8,n)
    with mp.Pool(workers) as pool:refs=np.concatenate(pool.map(dense_job,list(zip(np.array_split(x,workers),np.array_split(y,workers)))))
    lower=np.array([LIB.a_bound(a,a,b,b,2) for a,b in zip(x,y)]);gap=refs-lower
    with mp.Pool(workers) as pool:mr=np.concatenate(pool.map(dense_m_job,np.array_split(x,workers)))
    ml=np.array([LIB.m_bound(a,a,0) for a in x]);mg=mr-ml
    v=int(np.sum((gap<0)|(gap>1e-9)))+int(np.sum((mg<0)|(mg>1e-9)))
    kappa=ref();err=0.
    for i in range(2000):
        a,b=rng.uniform(0,math.pi/2,2);dy=rng.uniform(-.9,.9)
        # All support kinks plus dense r sampling; linear pieces attain their minima at kinks.
        rs=np.r_[np.linspace(-100,100,20001),math.tan(a),-1/math.tan(a),math.tan(b),-1/math.tan(b)]
        g=lambda t:(np.abs(math.cos(t)+rs*math.sin(t))+np.abs(math.sin(t)-rs*math.cos(t)))/2
        dual=float(np.min(g(a)+g(b)-rs*dy));err=max(err,abs(dual-kappa(a,b,dy)))
    v+=int(err>1e-9);results['G1']={'pairs':n,'dense_points':20001,'dual_triples':2000,'violations':v,'max_A_gap':float(gap.max()),'min_A_gap':float(gap.min()),'max_m_gap':float(mg.max()),'dual_max_error':err}
    gate_record('G1',results,start)
    worst=[-math.inf]*4;v=0;n=100000
    for i in range(n):
        widths=10**rng.uniform(-8,math.log10(2),2);lo=rng.uniform(-8,8-widths);hi=lo+widths
        if i<n//2:
            if i%3==0:lo[0]=-widths[0]*rng.random();hi[0]=lo[0]+widths[0]
            elif i%3==1:lo[1]=-widths[1]*rng.random();hi[1]=lo[1]+widths[1]
            else:
                # Rectangle contains an exact point on xy=-1.
                a=rng.uniform(.2,4)*rng.choice([-1,1]);b=-1/a
                lo=np.array([a,b])-widths*rng.random(2);hi=lo+widths
        bs=[LIB.a_bound(*[lo[0],hi[0],lo[1],hi[1]],m) for m in (0,1)]
        ms=[LIB.m_bound(lo[0],hi[0],m) for m in (0,1)]
        for a,b in rng.uniform(lo,hi,(20,2)):
            vals=[bs[0]-A(a,b),bs[1]-A(a,b),ms[0]-LIB.m_reference(a),ms[1]-LIB.m_reference(a)]
            for j,e in enumerate(vals):worst[j]=max(worst[j],e);v+=int(e>0)
        if (i+1)%20000==0:log('gates.log',f'G2 progress boxes={i+1} violations={v}')
    results['G2']={'boxes':n,'samples_per_box':20,'straddling_boxes':50000,'violations':v,'max_excess_plain_centered_A_m':worst};gate_record('G2',results,start)
    v=0;worst=-math.inf
    for i in range(20000):
        yl,wl=rng.uniform(-TOP,YTOP,2);yu,wu=[rng.uniform(a,YTOP) for a in (yl,wl)];h=rng.uniform(H0,2)
        # Full inner B&B with a small budget: valid at every budget, gate tests assembly.
        lower,_=bound((yl,yu,wl,wu),h,31,1e-4,False)
        for _ in range(10):
            r=[rng.uniform(0,TOP),rng.uniform(yl,yu),rng.uniform(LOW,TOP),rng.uniform(wl,wu),rng.uniform(0,TOP)]
            excess=lower-psi(r,h);worst=max(worst,excess);v+=int(excess>0)
        if (i+1)%5000==0:log('gates.log',f'G3 progress boxes={i+1} violations={v}')
    results['G3']={'boxes':20000,'samples_per_box':10,'violations':v,'max_excess':worst};gate_record('G3',results,start)
    errors=[];v=0
    for h in (1.87,1.9,1.95,1.99,2):
        t=theta(h);T=math.tan(math.pi/2-t);e=abs(psi([T,-1/T,T,-1/T,T],h)-L(t,h));errors.append(e);v+=int(e>1e-8)
    excess=-math.inf
    for a,b in cells():
        t=theta((a+b)/2)
        for h in rng.uniform(a,b,50):
            e=L(theta(h),h)-L(t,h);excess=max(excess,e);v+=int(e>1e-12)
    results['G4']={'identity_H':[1.87,1.9,1.95,1.99,2],'identity_errors':errors,'H_samples_per_cell':50,'violations':v,'max_minimum_minus_trial':excess};gate_record('G4',results,start)
    v=0;distance=0.
    for h in rng.uniform(1.87,2,10000):
        T=math.tan(math.pi/2-theta(h));d=max(abs(J[0]-T),abs(J[1]-T),abs(JE[0]+1/T),abs(JE[1]+1/T));distance=max(distance,d);v+=int(d>.32)
    exact_odd=(Decimal('.740900'),Decimal('1.15'));exact_even=(q,Decimal('-.85'))
    included=all(Decimal(a)>=e[0] and Decimal(b)<=e[1] for (a,b),e in [(J,exact_odd),(JE,exact_even)])
    v+=int(not included);results['G5']={'H_samples':10000,'max_sup_distance':distance,'inward_inclusion':included,'J_odd':J,'J_even':JE,'violations':v};gate_record('G5',results,start)
    save('gates.json',{'passed':True,'results':results,'source_hashes':hashes(),'seconds':time.monotonic()-start});log('gates.log',f'ALL PASS seconds={time.monotonic()-start:.6f}')
def gate_record(k,results,start):
    r=results[k];r['elapsed_seconds']=time.monotonic()-start;r['passed']=r['violations']==0
    log('gates.log',k+' '+json.dumps(r));save('gates.partial.json',results)
    if not r['passed']:raise RuntimeError(k+' failed; main run is forbidden')

@functools.lru_cache(maxsize=250000)
def inn(lo,hi,yl,yu,wl,wu,h,kind,budget,tol):
    n=ct.c_int();v=LIB.inner(lo,hi,yl,yu,wl,wu,h,kind,budget,tol,ct.byref(n));return v,n.value

def bound(rect,h,budget,tol,exclusion=True):
    yl,yu,wl,wu=rect;inside=yl>=JE[0] and yu<=JE[1] and wl>=JE[0] and wu<=JE[1]
    def b(kind,rng):return inn(*rng,yl,yu,wl,wu,h,kind,budget,tol) if kind==2 else inn(*rng,*( (yl,yu) if kind==1 else (wl,wu)),0.,0.,h,1,budget,tol)
    full=[b(1,(0.,TOP)),b(2,(LOW,TOP)),b(3,(0.,TOP))];n=sum(a[1] for a in full)
    sets=[[(a[0]) for a in full]]
    if exclusion and inside:
        sets=[]
        for k in range(3):
            lower=0. if k!=1 else LOW
            p=[b(k+1,(lower,J[0])),b(k+1,(J[1],TOP))];n+=sum(a[1] for a in p)
            s=[a[0] for a in full];s[k]=min(a[0] for a in p);sets.append(s)
    val=min(DN(DN(s[0]+s[1])+s[2]) for s in sets)
    # H positive on the entire domain. Sum and multiplication still round down.
    return DN(val+DN(h*DN(yl+wl))),n

def rect_test(rect,a,b,t,budget,tol):
    margins=[];n=0
    for h in (a,b):
        lb,k=bound(rect,h,budget,tol);n+=k;margins.append(DN(lb-LIB.target(t,h)))
    return min(margins),n

def cell_job(job):
    ident,a,b,seconds,maxboxes,budget,tol=job;start=time.monotonic();t=theta((a+b)/2);path=f'cells/{ident}.json'
    old=ROOT/path
    if old.exists():
        r=json.loads(old.read_text());assert r['source_hashes']==hashes();leaves=r['rectangles'];queue=[tuple(x) for x in r['pending']];tested=r['outer_boxes'];innern=r['inner_boxes'];elapsed=r['seconds']
    else:
        edges=[-TOP,JE[0],JE[1],YTOP];queue=[(edges[i],edges[i+1],edges[j],edges[j+1]) for i in range(3) for j in range(3)];leaves=[];tested=innern=0;elapsed=0.
    # Priority queue uses negative area: resolve largest outer rectangles first.
    heap=[(-((r[1]-r[0])*(r[3]-r[2])),r) for r in queue];heapq.heapify(heap);reason='complete';lastsave=start
    discards=sum(1 for row in leaves if len(row)>5 and row[5]=='sigma')
    def record():
        obj={'id':ident,'Ha':a,'Hb':b,'theta':t,'L_upper':[LIB.target(t,a),LIB.target(t,b)],'rectangles':leaves,'pending':[list(x[1]) for x in heap],'outer_boxes':tested,'inner_boxes':innern,'discards':discards,'seconds':elapsed+time.monotonic()-start,'proved':not heap,'reason':reason,'min_margin':min((r[4] for r in leaves if r[4] is not None),default=None),'budget_inner':budget,'tol_inner':tol,'source_hashes':hashes()};save(path,obj);return obj
    while heap:
        if time.monotonic()-start>=seconds:reason='time_budget';break
        if tested>=maxboxes:reason='outer_box_budget';break
        _,r=heapq.heappop(heap)
        # Corollary 10.1: exact H=2 bound plus affine H dependence.
        # This certifies directly against F6, not against the trial L.
        sigma_lower=DN(DN(LOW-r[1])-r[3])
        if sigma_lower>=5:
            leaves.append([*r,None,'sigma']);tested+=1;discards+=1
            continue
        margin,k=rect_test(r,a,b,t,budget,tol);tested+=1;innern+=k
        if margin>0:leaves.append([*r,margin])
        else:
            yl,yu,wl,wu=r
            if yu-yl>=wu-wl:m=yl+(yu-yl)*.5;children=[(yl,m,wl,wu),(m,yu,wl,wu)]
            else:m=wl+(wu-wl)*.5;children=[(yl,yu,wl,m),(yl,yu,m,wu)]
            for c in children:heapq.heappush(heap,(-((c[1]-c[0])*(c[3]-c[2])),c))
        if time.monotonic()-lastsave>30:record();lastsave=time.monotonic()
    return record()

def run(args):
    gate=json.loads((ROOT/'gates.json').read_text());assert gate['passed'] and gate['source_hashes']==hashes(),'current kernel must pass gates'
    (ROOT/'cells').mkdir(exist_ok=True);start=time.monotonic();jobs=[];records=[];attempts=[]
    old=json.loads((ROOT/'certificate.json').read_text()) if (ROOT/'certificate.json').exists() else None
    if old:
        assert old['source_hashes']==hashes()
        attempts=old.get('attempts',[])
        initial=old['cells']
    else:initial=[{'id':f'H{i}','Ha':a,'Hb':b,'proved':False} for i,(a,b) in enumerate(cells())]
    for r in initial:
        if r['proved']:records.append(r)
        else:jobs.append((r['id'],r['Ha'],r['Hb'],args.seconds,args.max_boxes,args.inner_budget,args.tol))
    def checkpoint(unstarted,pending):
        # Placeholder rows preserve exact H coverage even between completions.
        queued=[{'id':j[0],'Ha':j[1],'Hb':j[2],'proved':False,'reason':'queued'} for j in unstarted+list(pending.values())]
        save('certificate.json',{'format':1,'domain':[H0,2.],'J_odd':J,'J_even':JE,'source_hashes':hashes(),'cells':sorted(records+queued,key=lambda x:x['Ha']),'attempts':attempts,'wall_seconds':time.monotonic()-start,'complete':not queued and all(r['proved'] for r in records)})
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
        pending={}
        while jobs or pending:
            while jobs and len(pending)<args.workers:
                j=jobs.pop(0);pending[pool.submit(cell_job,j)]=j
            checkpoint(jobs,pending)
            done,_=concurrent.futures.wait(pending,timeout=1,return_when=concurrent.futures.FIRST_COMPLETED)
            for f in done:
                j=pending.pop(f);r=f.result();depth=len(r['id'])-len(r['id'].rstrip('ab'))
                log('run.log',json.dumps({k:v for k,v in r.items() if k not in ('rectangles','pending','source_hashes')}))
                if not r['proved'] and depth<args.split_depth:
                    attempts.append({k:v for k,v in r.items() if k not in ('rectangles','pending')})
                    mid=(r['Ha']+r['Hb'])/2
                    # Warm-start children from the exact parent partition.
                    partition=[v[:4] for v in r['rectangles']]+r['pending']
                    for suffix,aa,bb in [('a',r['Ha'],mid),('b',mid,r['Hb'])]:
                        ident=r['id']+suffix;row=dict(r,id=ident,Ha=aa,Hb=bb,rectangles=[],pending=partition,outer_boxes=0,inner_boxes=0,seconds=0.,proved=False)
                        save(f'cells/{ident}.json',row)
                        jobs.append((ident,aa,bb,args.seconds,args.max_boxes,args.inner_budget,args.tol))
                else:records.append(r)
                checkpoint(jobs,pending)
    checkpoint([],{});log('run.log',f'FINISH wall_seconds={time.monotonic()-start:.6f} complete={all(r["proved"] for r in records)}')

def verify():
    start=time.monotonic();c=json.loads((ROOT/'certificate.json').read_text());assert c['source_hashes']==hashes();count=0
    end=H0
    for row in c['cells']:
        assert row['Ha']==end and row['Hb']>end
        end=row['Hb']
    assert end==2.

    for row in c['cells']:
        assert row['L_upper']==[LIB.target(row['theta'],h) for h in (row['Ha'],row['Hb'])]
        rectangles=row['rectangles'];pending=row['pending']
        # Disjoint interior and exact domain coverage: recursive dyadic cells are
        # reconstructed from partition rectangles by an independent sweep.
        allrect=rectangles+pending;ys=sorted(set([-TOP,YTOP]+[r[i] for r in allrect for i in (0,1)]))
        for l,u in zip(ys,ys[1:]):
            active=sorted((r[2],r[3]) for r in allrect if r[0]<=l and r[1]>=u)
            end=-TOP
            for x,y in active:assert x==end and y>x;end=y
            assert end==YTOP
        for r in rectangles:
            if len(r)>5 and r[5]=='sigma':assert DN(DN(LOW-r[1])-r[3])>=5
            else:
                v,_=rect_test(tuple(r[:4]),row['Ha'],row['Hb'],row['theta'],row['budget_inner'],row['tol_inner']);assert v>0
            count+=1
        log('verification.log',f'{row["id"]} certified_rectangles={len(rectangles)} pending_rectangles={len(pending)} full_cell={row["proved"]} replay=PASS partition=PASS')
    complete=c['complete'];log('verification.log',f'REPLAY PASS rectangles={count} complete_domain={complete} seconds={time.monotonic()-start:.6f}');return complete

def report():
    c=json.loads((ROOT/'certificate.json').read_text()) if (ROOT/'certificate.json').exists() else None
    g=json.loads((ROOT/'gates.partial.json').read_text()) if (ROOT/'gates.partial.json').exists() else {}
    lines=['# O2 certified computation report','',('**All H-cells certified.**' if c and c['complete'] else '**Partial computation; O2 is not certified by this run.**'),'','## Gates','', 'Results below are copied from gates.partial.json and gates.log.','']
    for k,r in g.items():lines.append(f'- {k}: `{json.dumps(r)}`')
    lines+=['','## Per-H-cell results','','| Cell | Ha | Hb | Outer boxes | Inner boxes | Discards | Minimum margin | Seconds | Complete |','|---|---:|---:|---:|---:|---:|---:|---:|---|']
    if c:
        for r in c['cells']:lines.append(f'| {r["id"]} | {r["Ha"]:.17g} | {r["Hb"]:.17g} | {r["outer_boxes"]} | {r["inner_boxes"]} | {r["discards"]} | {r["min_margin"]} | {r["seconds"]:.6f} | {r["proved"]} |')
        lines+=['',f'Main wall time: {c["wall_seconds"]:.6f} seconds. Missing full-cell certificates: '+', '.join(r['id']+' ('+r['reason']+')' for r in c['cells'] if not r['proved'])+'.']
    lines+=['','## Implementation and assumptions','','C kernel reuses o1dp nextafter arithmetic and eight-ulp libm padding. Every interval operation is outward rounded and asserts ordered endpoints. The eight-ulp libm accuracy premise is retained; this is not a proof of the platform libm. Python uses the requested venv, numpy and scipy. Sources and shared library are hashed. No network, git commands, or writes outside o2cert were used.','', 'Candidate bounds, global-Lipschitz centred forms, best-first inner B&B, affine H endpoint tests, product exclusion, per-cell checkpoints and deterministic saved-rectangle replay are implemented. Full and excluded inner intervals use directed decimal endpoints. Adjacent cells share endpoints. Partition verification checks exact coverage and disjoint interiors of certified plus pending rectangles; pending regions are not certified.','', '## Deviations and open work','','The simpler constant Lipschitz option is used instead of interval AD. Inner searches stop at a fixed box budget, which the spec permits; this can leave conservative lower bounds. Outer selection uses largest area first rather than smallest bound. Initial outer partition aligns with exclusion boundaries. The discard count is zero: full inner ranges have min(-sigma) below five, and the current separable implementation does not expose smaller joint inner boxes for this shortcut. H-cell splitting is not yet implemented. Full H-cells may remain open at the configured time/box limit; the same driver resumes their queues.','', '## Issues with the spec','','None identified in LEMMAS.md or SPEC.md during implementation. See the separate corner audit for issues in the supplied swarm proof and arithmetic.','', '## Reproduce','','```sh','clang -O2 -shared -fPIC src/kernel.c -o src/kernel.dylib','../.venv/bin/python src/driver.py gates --workers 8','../.venv/bin/python src/driver.py run --workers 8','../.venv/bin/python src/driver.py verify','../.venv/bin/python src/driver.py report','```','']
    (ROOT/'README.md').write_text('\n'.join(lines))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['gates','run','verify','report']);p.add_argument('--workers',type=int,default=min(8,os.cpu_count() or 1));p.add_argument('--seconds',type=float,default=300);p.add_argument('--max-boxes',type=int,default=20000);p.add_argument('--inner-budget',type=int,default=255);p.add_argument('--tol',type=float,default=1e-5);p.add_argument('--split-depth',type=int,default=1);a=p.parse_args()
    {'gates':lambda:gates(a.workers),'run':lambda:run(a),'verify':lambda:runpy.run_path(str(ROOT/'src/verify_parallel.py'),run_name='__main__'),'report':lambda:runpy.run_path(str(ROOT/'src/finish_report.py'))}[a.mode]()
