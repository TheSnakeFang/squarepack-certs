#!/usr/bin/env python3
"""Window-owned, native-affine-piece A2 audit. Floating point, not a certificate.

python3 -I tools/wedge_prop75_a2.py --selftest | --probe | --run
No network, dependencies, bytecode, or tracked-file writes.

A window owns pieces whose LEFT endpoint lies in it. Flow starts with the SAME
full-floor interval as the original simulator, pruning states disjoint from the
window without clipping them. Thus a cut inside an affine piece never changes
that piece, its interior representatives, comparisons, or boundary cost. Pieces
crossing a cut belong wholly to the earlier window. This is stronger than adding
a harmless zero boundary: even comparison counts match a full-floor pass.
"""
import sys
sys.dont_write_bytecode = True
import argparse
import collections
import dataclasses
import gc
import hashlib
import importlib.util
import inspect
import json
import math
import os
from pathlib import Path
import resource
import time
import tempfile
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('prop75', ROOT/'tools/wedge_prop75_check.py')
p = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = p
spec.loader.exec_module(p)
s, f = p.s, p.f
TOL = 2e-7
BASE = ROOT/'runs/k2c-exponent-2026-11-09'
ALPHA, LENGTH, WIDTH = .03, 320., 1.
VERSION = 1

# Reuse the actual published flow, changing only its search/pruning domain.
# Full native intervals and midpoints are preserved at every level. Guard the
# textual transformation so an upstream edit cannot silently change semantics.
def native_flow_function():
    src = inspect.getsource(s.interval_flow)
    old = 'todo=[(r.window[0],r.window[1],-1,'
    assert src.count(old) == 1
    src = src.replace(old, 'todo=[(0.,r.L,-1,')
    old = 'lo,hi,em,s,G,V,chain,entries,segs=todo.pop()'
    assert src.count(old) == 1
    src = src.replace(old, old+'\n        if hi <= r.window[0] or lo >= r.window[1]: continue')
    old = 'for aa,bb in split(a,b,total,[delta]):'
    assert src.count(old) == 1
    src = src.replace(old, old+'\n                if bb <= r.window[0] or aa >= r.window[1]: continue')
    ns = dict(vars(s))
    exec(compile(src, '<native full-floor pruning>', 'exec'), ns)
    return ns['interval_flow']
NATIVE_FLOW = native_flow_function()


def rss_gb():
    # macOS reports bytes; Linux reports KiB.
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == 'darwin' else 1e9/1024)


def prepare(alpha, L, rise=1., delta=1/32):
    start = time.monotonic()
    r = p.construct(alpha, delta, .08, 'clean', L, rise)
    print('packing', json.dumps(dict(alpha=alpha,L=L,m=r.m,squares=len(r.squares),W=r.W,
          gap_condition=math.sin(alpha)+(1-math.cos(alpha))/2,delta=delta)), flush=True)
    validated = s.independent_validate(r)
    print('independent validation PASS', validated, 'comparisons;', round(time.monotonic()-start,3), 's', flush=True)
    profiles = r.profiles(r.delta)
    bypair, conf = f.conflict_intervals(r, profiles, r.tau)
    del bypair
    gc.collect()
    setup = time.monotonic()-start
    print('profiles/conflicts ready; setup', round(setup,3), 's; peak RSS GB', round(rss_gb(),3), flush=True)
    return r, profiles, conf, validated, setup


def pack_path(v):
    return None if v is None else dataclasses.asdict(v)


def unpack_path(v):
    def tuples(x):
        return tuple(tuples(y) for y in x) if isinstance(x,list) else x
    return None if v is None else f.PathRun(**{k:tuples(x) for k,x in v.items()})


GLOBAL_LABELS = {'height identity residual','slope identity residual','floor partition measure',
                 'Lemma 6.1','Lemma 5.1','combined inequality'}


class Aggregate:
    def __init__(self, state=None):
        self.t = dict(counts={}, gap_emitters={}, X=0., positive=0., theta=0., cost=0.,
                      skips=0, literal_skips=0, arrivals=0, paths=0, boundaries=0,
                      height=0., slope=0., minorder=math.inf,
                      checks={str(k):[0,0] for k in range(1,9)}, failures=[],
                      worst=None, worst_p6=None)
        self.last_path = self.last_arrival = None
        if state:
            self.t = state['totals']
            self.last_path = unpack_path(state['last_path'])
            self.last_arrival = unpack_path(state['last_arrival'])

    def state(self):
        return dict(totals=self.t,last_path=pack_path(self.last_path),last_arrival=pack_path(self.last_arrival))

    def le(self, k, label, lhs, rhs, witness=None):
        c = self.t['checks'][str(k)]
        c[0] += 1
        if lhs > rhs+TOL:
            c[1] += 1
            self.t['failures'].append((k,label,lhs,rhs,witness))

    def add_check_list(self,k,values):
        c=self.t['checks'][str(k)]
        c[0]+=len(values); c[1]+=sum(not x for x in values)

    def consume(self,r,paths):
        """Audit native owned pieces, then bridge both adjacency relations."""
        if not paths: return []
        r.window=(paths[0].lo, paths[-1].hi)
        a=s.audit(r,paths)
        t=self.t
        # Preserve even the original floating-point summation order.
        for v in paths:
            t['counts'][v.kind]=t['counts'].get(v.kind,0.)+(v.hi-v.lo)
            if v.kind=='gap':
                k='floor' if not v.chain else ('layer' if r.squares[v.chain[-1]].a==0 else 'tilted')
                t['gap_emitters'][k]=t['gap_emitters'].get(k,0.)+(v.hi-v.lo)
            if v.kind=='arrival': t['X']+=f.val(v.end[0],v.hi)-f.val(v.end[0],v.lo)
        t['paths']+=len(paths); t['arrivals']+=len(a['arr'])
        t['height']=max(t['height'],a['height']); t['slope']=max(t['slope'],a['slope'])
        t['minorder']=min(t['minorder'],a['minorder'])
        self.add_check_list(1,a['checks'][1][:-2])
        self.add_check_list(2,a['checks'][2][:-1-len(a['boundaries'])] if a['boundaries'] else a['checks'][2][:-1])
        # Check 2's arrival-order comparisons occur AFTER its partition check.
        self.add_check_list(2,a['checks'][2][-len(a['boundaries']):] if a['boundaries'] else [])
        for k in (3,5,6): self.add_check_list(k,a['checks'][k])
        t['failures'] += [v for v in a['failures'] if v[1] not in GLOBAL_LABELS]
        if self.last_path:
            margin=s.order_margin(self.last_path,self.last_path.hi,paths[0],paths[0].lo)
            t['minorder']=min(t['minorder'],margin)
            self.le(2,'adjacent limiting paths',-margin,0.,(self.last_path.hi,paths[0].lo))
        bs=[]
        if self.last_arrival and a['arr']:
            # Use the original audit's complete boundary calculation, including
            # original interior representatives and all aligned-level checks.
            bridge=s.audit(r,[self.last_arrival,a['arr'][0]])
            for k in (3,5,6): self.add_check_list(k,bridge['checks'][k])
            self.add_check_list(2,bridge['checks'][2][-1:])
            t['failures'] += [v for v in bridge['failures'] if v[0] in (3,5,6) or v[1]=='arrival ordering']
            bs.extend(bridge['boundaries'])
        bs.extend(a['boundaries'])
        for b in bs:
            t['boundaries']+=1; b['k']=t['boundaries']
            t['positive']+=b['drop'] if b['drop']>f.EPS else 0.
            t['theta']+=b['Theta']; t['cost']+=b['cost']
            t['skips']+=int(b['skip'])
            t['literal_skips']+=int(b['Delta']>=1/(2*r.z))
            if b['drop']>f.EPS:
                skip=b['Delta']>=1/(2*r.z) and b['Np']>b['N']
                v=p.ratio(b['drop'],r.tau*b['Theta'])
                if b['Delta']<1/(2*r.z) and (t['worst'] is None or v>t['worst'][0]):
                    t['worst']=(v,b.copy())
                residual=b['drop']-(math.inf if skip else r.tau*b['Theta'])
                if t['worst_p6'] is None or residual>t['worst_p6'][0]:
                    t['worst_p6']=(residual,b.copy())
        self.last_path=paths[-1]
        if a['arr']: self.last_arrival=a['arr'][-1]
        return bs

    def finish(self,r,domain=None):
        t=self.t; width=r.L if domain is None else domain
        self.le(1,'height identity residual',t['height'],TOL)
        self.le(1,'slope identity residual',t['slope'],TOL)
        self.le(2,'floor partition measure',abs(sum(t['counts'].values())-width),TOL)
        self.le(4,'Lemma 6.1',math.sin(math.atan(r.z))*t['counts'].get('arrival',0.)-r.delta,t['positive'])
        self.le(7,'Lemma 5.1',t['cost'],14851*r.W)
        self.le(8,'combined inequality',t['positive'],r.tau*t['theta']+r.delta*t['skips'])


def window_flow(r,profiles,conf,lo,hi,overlap=False):
    r.window=(lo,hi)
    paths=NATIVE_FLOW(r,profiles,conf,r.delta,r.tau)
    return paths if overlap else [v for v in paths if lo <= v.lo < hi]


def selftest():
    start=time.monotonic()
    r,profiles,conf,_,_=prepare(.07,80.,.5,1/8)
    r.window=(0.,r.L)
    paths=s.interval_flow(r,profiles,conf,r.delta,r.tau)
    ref=s.audit(r,paths)
    refvals=dict(G=ref['counts']['arrival'],positive=ref['positive'],theta=ref['theta'],cost=ref['cost'],
                 arrivals=len(ref['arr']),skips=ref['skips'],X=sum(f.val(v.end[0],v.hi)-f.val(v.end[0],v.lo) for v in ref['arr']))
    refchecks={str(k):[len(ref['checks'][k]),sum(not x for x in ref['checks'][k])] for k in range(1,9)}
    # Cuts deliberately inside native arriving pieces; unequal widths, including
    # multiple empty-arrival windows before the first arrival.
    cuts=[0.,3.17,9.823,18.234567,27.128765,49.314159,62.987654,80.]
    signature=[(v.lo,v.hi,v.kind,v.chain,v.entries,v.G,v.V,v.end,v.hit) for v in paths]
    # Force windows with no new owned pieces AFTER an earlier arrival, testing
    # the last-arrival bridge across multiple empty windows as well as JSON I/O.
    first,last=ref['arr'][0].lo,ref['arr'][-1].hi
    dead=next(v for v in paths if v.kind!='arrival' and first<v.lo<v.hi<last and v.hi-v.lo>1e-7)
    cuts=sorted(set(cuts+[dead.lo+(dead.hi-dead.lo)*j/4 for j in (1,2,3)]))
    refboundaries=ref['boundaries']; refcounts=dict(ref['counts'])
    refgap=dict(ref['gap_emitters'])
    del paths,ref
    gc.collect()
    agg=Aggregate(); seen=[]; bs=[]; empty_after_arrival=0
    for lo,hi in zip(cuts,cuts[1:]):
        q=window_flow(r,profiles,conf,lo,hi)
        if not q and agg.last_arrival: empty_after_arrival+=1
        seen.extend((v.lo,v.hi,v.kind,v.chain,v.entries,v.G,v.V,v.end,v.hit) for v in q)
        bs.extend(agg.consume(r,q))
        # Exercise checkpoint carry-over decoding after EVERY window, including
        # empty-arrival windows, without launching --run.
        agg=Aggregate(json.loads(json.dumps(agg.state())))
        del q
        gc.collect()
    agg.finish(r)
    t=agg.t
    measured=dict(G=t['counts']['arrival'],positive=t['positive'],theta=t['theta'],cost=t['cost'],
                  arrivals=t['arrivals'],skips=t['skips'],X=t['X'])
    diff={k:measured[k]-v for k,v in refvals.items()}
    published={'G':.785952101323*80,'positive':.389711537919,'theta':13.58,'cost':12.6576050255}
    pubdiff={k:refvals[k]-v for k,v in published.items()}
    boundarydiff={k:max((abs(a[k]-b[k]) for a,b in zip(bs,refboundaries)),default=0.) for k in ('Delta','drop','Theta','cost')}
    checks={k:[t['checks'][k][i]-refchecks[k][i] for i in (0,1)] for k in refchecks}
    endingdiff={k:t['counts'].get(k,0.)-v for k,v in refcounts.items()}
    gapdiff={k:t['gap_emitters'].get(k,0.)-v for k,v in refgap.items()}
    result=dict(differences=diff,published_differences=pubdiff,boundary_max_differences=boundarydiff,
                check_count_and_failure_differences=checks,ending_differences=endingdiff,gap_emitter_differences=gapdiff,
                empty_owned_windows_after_arrival=empty_after_arrival,window_cuts=cuts,
                native_partition_identical=seen==signature,seconds=time.monotonic()-start,peak_RSS_GB=rss_gb())
    print(json.dumps(result,indent=2),flush=True)
    assert seen==signature and len(bs)==len(refboundaries)
    assert all(abs(x)<=1e-9 for x in (*diff.values(),*pubdiff.values(),*boundarydiff.values(),*endingdiff.values(),*gapdiff.values()))
    assert all(v==[0,0] for v in checks.values())
    assert not t['failures'],t['failures']
    assert empty_after_arrival>=2
    # Exercise the report's disk-backed boundary reader and torn-line recovery.
    # No --run is launched and no A2 result report is created by this test.
    with tempfile.TemporaryDirectory(prefix='a2-selftest-',dir=BASE) as tmp:
        checkpoint=Path(tmp)/'checkpoint.jsonl'
        checkpoint.write_text(json.dumps(dict(boundaries=bs,state=agg.state()))+'\n'+ '{"interrupted":')
        rows=list(read_records(checkpoint))
        assert len(rows)==1 and checkpoint.read_bytes().endswith(b'\n')
        report_path=Path(tmp)/'test-report.md'
        assert not report(r,agg,checkpoint,0,0.,1.,destination=report_path)
        assert 'not a certificate' in report_path.read_text()
    result['checkpoint_roundtrip_and_report']='PASS'
    (BASE/'wedge-prop75-a2-selftest.json').write_text(json.dumps(result,indent=2)+'\n')
    print('SELFTEST PASS',flush=True)


def probe(alpha,L,width):
    r,profiles,conf,validated,setup=prepare(alpha,L)
    results=[]
    for name,lo in [('arriving',(r.xi0+L)/2-width/2),('left-clearance',r.xi0/2-width/2)]:
        hi=lo+width; start=time.monotonic()
        paths=window_flow(r,profiles,conf,lo,hi,True)
        # Overlap pieces are audited intact. Fraction uses clipped measure in
        # the geometric probe window, independent of native ownership.
        G=sum(max(0.,min(v.hi,hi)-max(v.lo,lo)) for v in paths if v.kind=='arrival')
        agg=Aggregate(); agg.consume(r,paths)
        elapsed=time.monotonic()-start
        item=dict(name=name,window=[lo,hi],arrival_fraction=G/width,seconds=elapsed,
                  paths=len(paths),arrivals=agg.t['arrivals'],peak_RSS_GB=rss_gb(),
                  audit_failures=agg.t['failures'])
        print('probe',json.dumps(item),flush=True)
        results.append(item)
        del paths,agg
        gc.collect()
    # Conservative extra right-edge unit counted as dead, middle density
    # extrapolated across the remaining floor. This is a projection, not proof.
    clearance=r.xi0+1.
    frac=results[0]['arrival_fraction']*max(0.,L-clearance)/L
    runtime=setup+(L-r.xi0)*results[0]['seconds']/width+r.xi0*results[1]['seconds']/width
    result=dict(alpha=alpha,L=L,width=width,squares=len(r.squares),m=r.m,xi0=r.xi0,W=r.W,
                validation_comparisons=validated,setup_seconds=setup,windows=results,
                projected_arrival_fraction=frac,projected_runtime_seconds=runtime,peak_RSS_GB=rss_gb(),
                smallest_round_L_projection=10*math.ceil(clearance/(1-.78/results[0]['arrival_fraction'])/10) if results[0]['arrival_fraction']>.78 else None,
                projection_note='Two sampled windows only; rightmost unit pessimistically dead; runtime excludes any position-dependent variation and extra bridge cost.')
    (BASE/'wedge-prop75-a2-probe.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)
    assert all(not x['audit_failures'] for x in results), 'Probe inequality failures retained with witnesses'


def fingerprint(alpha,L,width):
    files=[Path(__file__),ROOT/'tools/wedge_prop75_check.py',ROOT/'tools/wedge_staircase_check.py',ROOT/'tools/wedge_flow_check.py']
    return hashlib.sha256(json.dumps([VERSION,alpha,L,width]).encode()+b''.join(q.read_bytes() for q in files)).hexdigest()


def read_records(path):
    """Stream checkpoints with bounded memory; repair only a torn final line."""
    if not path.exists(): return
    with path.open('r+b') as h:
        while True:
            start=h.tell(); line=h.readline()
            if not line: break
            if not line.endswith(b'\n'):
                h.truncate(start)
                break
            yield json.loads(line)


class Boundaries:
    def __init__(self,path): self.path=path
    def __iter__(self):
        with self.path.open() as h:
            for line in h:
                for b in json.loads(line)['boundaries']: yield b


def report(r,agg,checkpoint,validated,elapsed,width,destination=None):
    t=agg.t
    a=dict(counts=collections.Counter(t['counts']),boundaries=Boundaries(checkpoint),
           arr=[SimpleNamespace(end=((t['X'],0.),),hi=1.,lo=0.)],positive=t['positive'],theta=t['theta'],cost=t['cost'])
    lines,worst,X,ds,skips=p.evaluate(r,a)
    hyp=(4250*r.W+1350*r.W/r.tau+.01)/(r.L/4)
    out=['# Proposition 7.5 case A2','',
         'Floating point experiment, not a certificate. Comparison tolerance 2e-7; geometry epsilon unchanged.', '',
         'Parameters: `'+repr(dict(alpha=r.alpha,L=r.L,R=r.z*r.L,zeta=r.z,delta=r.delta,tau=r.tau,m=r.m,squares=len(r.squares),w=r.w,W=r.W,window_width=width))+'`.',
         '', '|G|/L = '+p.fmt(t['counts'].get('arrival',0.)/r.L)+'; |G| = '+p.fmt(t['counts'].get('arrival',0.))+'. Majority target '+('PASS' if t['counts'].get('arrival',0.)>=.75*r.L else 'FAIL')+'.',
         '|X-prime| = '+p.fmt(X)+'; sum Delta = '+p.fmt(ds)+'; positive drops = '+p.fmt(t['positive'])+'; sum Theta = '+p.fmt(t['theta'])+'; sum theta_i |Y_i| = '+p.fmt(t['cost'])+'; skips = '+str(skips)+'.',
         'Literal hypothesis ratio (4250W+1350W/tau+0.01)/(L/4) = '+p.fmt(hyp)+'. The literal small-waste hypothesis is '+('not met.' if hyp>1 else 'met.'),
         '', '| Line | lhs <= rhs | lhs | rhs | lhs/rhs | Result |','|---|---|---:|---:|---:|---|']
    display=[v for v in lines if v[0]!='P6-boundary']
    boundarylines=[v for v in lines if v[0]=='P6-boundary']
    if boundarylines: display.append(max(boundarylines,key=lambda v:v[2]-v[3]))
    for tag,claim,lhs,rhs,rr,ok,witness in display:
        out.append('| %s | %s | %s | %s | %s | %s |'%(tag,claim.replace('|','\\|'),p.fmt(lhs),p.fmt(rhs),p.fmt(rr),'PASS' if ok else 'FAIL'))
    out+=['','| Audit check | Comparisons | Failures | Result |','|---|---:|---:|---|']
    for k,(n,fail) in t['checks'].items(): out.append('| %s | %s | %s | %s |'%(k,n,fail,'FAIL' if fail else 'PASS'))
    out+=['','Largest non-skip positive drop/(tau Theta): '+p.fmt(worst[0])+'. Witness: `'+repr(worst[1])+'`.',
          'P-line failures (with witnesses): `'+repr([v for v in lines if not v[5]])+'`.',
          'Audit failure witnesses: `'+repr(t['failures'])+'`.',
          'Ending measures by kind: `'+repr(t['counts'])+'`; gap emitters: `'+repr(t['gap_emitters'])+'`.',
          'Native paths: %d; arrivals: %d; boundaries: %d. Independent validation: %d comparisons, PASS. Total measured run seconds: %.6f; peak RSS GB: %.6f.'%(t['paths'],t['arrivals'],t['boundaries'],validated,elapsed,rss_gb()),
          '', 'Windows own whole native affine pieces by their left endpoint. Full-floor flow states are pruned against each window, never clipped; artificial cuts therefore introduce no boundaries and preserve the original audit interior representatives exactly. Both the last complete path and the last arriving path (including complete entry chains and affine limits) are checkpointed. Across empty-arrival windows the latter is retained. Cross-window ordering and arrival boundaries use the same audit calculations as interior boundaries. Global checks are evaluated once on the totals. Every native Delta, drop, Theta and tube cost is stored in the JSON-lines checkpoint.',
          'Checkpoint: `'+str(checkpoint.relative_to(ROOT))+'`. No formal or interval-arithmetic certificate is claimed.']
    (destination or BASE/'wedge-prop75-a2.md').write_text('\n'.join(out)+'\n')
    return any(not v[5] for v in lines) or bool(t['failures'])


def run(alpha,L,width):
    work=BASE/'work'; work.mkdir(exist_ok=True)
    checkpoint=work/'wedge-prop75-a2.jsonl'
    digest=fingerprint(alpha,L,width)
    last_state=None; spent=0.; done=0
    for i,row in enumerate(read_records(checkpoint)):
        assert row['index']==i and row['fingerprint']==digest, 'Checkpoint configuration/source mismatch; preserve it and use a separate work directory'
        last_state=row['state']; spent+=row['seconds']; done=i+1
    agg=Aggregate(last_state)
    del last_state
    r,profiles,conf,validated,setup=prepare(alpha,L)
    n=math.ceil(L/width); start=time.monotonic()
    assert done<=n
    for i in range(done,n):
        t0=time.monotonic(); lo=i*width; hi=min(L,(i+1)*width)
        paths=window_flow(r,profiles,conf,lo,hi)
        bs=agg.consume(r,paths)
        seconds=time.monotonic()-t0; spent+=seconds
        row=dict(index=i,window=[lo,hi],fingerprint=digest,seconds=seconds,boundaries=bs,state=agg.state())
        with checkpoint.open('a') as h:
            h.write(json.dumps(row,separators=(',',':'))+'\n'); h.flush(); os.fsync(h.fileno())
        elapsed=setup+time.monotonic()-start
        # Use measured work rate; clearance and arriving regions can differ.
        remaining=(n-i-1)*spent/(i+1)
        print('window %d/%d arrival %.12g elapsed %.1fs projected remaining %.1fs peak RSS %.3fGB'%(i+1,n,agg.t['counts'].get('arrival',0.),elapsed,remaining,rss_gb()),flush=True)
        del paths,bs,row
        gc.collect()
    agg.finish(r)
    failed=report(r,agg,checkpoint,validated,setup+spent,width)
    print('Wrote',BASE/'wedge-prop75-a2.md', 'FAIL' if failed else 'PASS',flush=True)
    return int(failed)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    for name in ('selftest','probe','run'): mode.add_argument('--'+name,action='store_true')
    parser.add_argument('--alpha',type=float,default=ALPHA)
    parser.add_argument('--L',type=float,default=LENGTH)
    parser.add_argument('--width',type=float,default=WIDTH)
    args=parser.parse_args()
    assert args.width>0 and args.L>0
    if args.selftest: selftest()
    elif args.probe: probe(args.alpha,args.L,args.width)
    else: return run(args.alpha,args.L,args.width)
    return 0

if __name__=='__main__': raise SystemExit(main())
