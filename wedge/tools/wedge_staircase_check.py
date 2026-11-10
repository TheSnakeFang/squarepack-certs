#!/usr/bin/env python3
"""Deterministic offline staircase audit. Run from the repo root with python3 -I.
Only output file: runs/k2c-exponent-2026-11-09/wedge-staircase-check.md.
No third-party packages, network, random geometry nudges, or bytecode files.
"""
import sys
sys.dont_write_bytecode = True
import importlib.util
import math
import random
import statistics
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'runs/k2c-exponent-2026-11-09/wedge-staircase-check.md'
spec = importlib.util.spec_from_file_location('wedge_flow_core', ROOT / 'tools/wedge_flow_check.py')
f = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = f
spec.loader.exec_module(f)
TOL = 2e-7
EPS=f.EPS
const,split,val,plus,scale,moving,point,sub,PathRun = (getattr(f,k) for k in ('const','split','val','plus','scale','moving','point','sub','PathRun'))


def fmt(x):
    return 'n/a' if x is None else ('inf' if math.isinf(x) else '%.12g' % x)


def construct(alpha, delta, tau, variant, L=80., rise=.5):
    """Columns first; all filler candidates subsequently go through Region's SAT."""
    z = rise/L
    q = 1-math.cos(alpha)
    m = math.ceil(rise/q)+20
    # First column's upper-left vertex clears X=0 even when J=0.
    xi0 = m*math.sin(alpha)+.02
    # Set the leftmost column's top ceiling slack to half a q.
    w = m*math.cos(alpha)+math.sin(alpha)-z*.02+q*.5
    columns = []
    meta = []
    xi = xi0
    previous = 0
    current_alpha = alpha
    # Split halfway through the clean group measured at its bottom footprint.
    coefficient=q+z*(math.tan(alpha)-math.sin(alpha))
    split_xi=xi0+(L-math.cos(alpha)-xi0)/(2*(1-z*math.tan(alpha)/coefficient))
    while xi <= L+m*math.tan(alpha):
        a = alpha if variant != 'two-tilts' or xi < split_xi else .8*alpha
        if a != current_alpha:
            # Separate the groups along the old group's right slab boundary.
            # The new normal leans less; minimum joining height controls separation.
            xi += .001
            # Start beyond the previous slab at the joining height, then move
            # right only enough to accommodate the new (higher) top.
            xi += previous*(math.tan(a)-math.tan(current_alpha))
            ca2,sa2,ta2=math.cos(a),math.sin(a),math.tan(a)
            n2=m-previous
            top=previous+n2*ca2+sa2
            xright=xi-previous*ta2+ca2-n2*sa2
            xi += max(0.,(top-z*xright-w)/z)+.001
            current_alpha = a
        ca, sa, ta = math.cos(a), math.sin(a), math.tan(a)
        # The extrema of Y-zX are linear in J; all four vertices must fit.
        def cap(J):
            n=m-J; px=xi-J*ta
            return max(J+aa*sa+ee*ca-z*(px+aa*ca-ee*sa)
                       for aa in (0,1) for ee in (0,n))
        fit=[J for J in range(previous,m+1) if cap(J)<=w+1e-11]
        if not fit: break
        J=max(fit); n=m-J
        if n<=0: break
        px=xi-J*ta
        if px+ca>L+1e-10: break
        columns.extend(f.Square(px+.5*ca-(i+.5)*sa,J+.5*sa+(i+.5)*ca,a) for i in range(n))
        meta.append((xi,J,n,a))
        previous=J
        xi+=1/ca
    rng=random.Random(20261109)
    layers=[]
    row_offsets={j:rng.random() for j in range(max(m,math.ceil(w+rise)))} if variant=='brick-offsets' else defaultdict(float)
    for j in range(m):
        first=next((v for v in meta if v[1]>j),None)
        if first is None: continue
        start=first[0]-j*math.tan(first[3])
        shift=row_offsets[j]
        for i in range(max(0,math.ceil(L-start))):
            layers.append(f.Square(start+shift+i+.5,j+.5))
    # Left of the first slab at this row: integer grid, clipped by the same filter.
    # Filling every row would be redundant on the right, so bound by its left edge.
    for j in range(math.ceil(w+rise)):
        left=xi0-(j+1)*math.tan(alpha)
        shift=row_offsets[j]
        for i in range(max(0,math.floor(left-shift+1e-10))):
            layers.append(f.Square(shift+i+.5,j+.5))
    removed=[]
    if variant=='removed':
        # Exactly three holes of each type; sparse damage, not a per-square rate.
        for group in (columns,layers):
            ids=set(rng.sample(range(len(group)),min(3,len(group))))
            removed.extend(group[i] for i in sorted(ids))
            group[:]=[sq for i,sq in enumerate(group) if i not in ids]
    r=f.Region('a%s-%s'%(fmt(alpha),variant),L,w,z,columns+layers)
    r.meta=meta; r.m=m; r.xi0=xi0; r.alpha=alpha; r.delta=delta; r.tau=tau
    r.candidates=len(columns)+len(layers); r.removed=removed
    r.window=(0.,L) if alpha==.07 else ((xi0+L)/2-3,(xi0+L)/2+3)
    return r


def independent_validate(r):
    """Independent Y sweep and center/radius SAT; no Region cells/overlap/inside."""
    boxes=[]
    for i,s in enumerate(r.squares):
        c,t=math.cos(s.a),math.sin(s.a)
        ex=(abs(c)+abs(t))/2
        # Linear functional support radii, without using the vertex containment code.
        assert s.x-ex>=-2e-9 and s.x+ex<=r.L+2e-9
        assert s.y-ex>=-2e-9
        rad=(abs(t-r.z*c)+abs(c+r.z*t))/2
        assert s.y-r.z*s.x+rad<=r.w+2e-9
        boxes.append((s.y-ex,s.y+ex,s.x-ex,s.x+ex,i))
    active=[]; comparisons=0
    for low,high,left,right,i in sorted(boxes):
        active=[v for v in active if v[0]>low+1e-9]
        a=r.squares[i]
        for top,lft,rgt,k in active:
            if min(right,rgt)-max(left,lft)<=1e-9: continue
            b=r.squares[k]; dx=b.x-a.x; dy=b.y-a.y
            separated=False
            for angle in (a.a,a.a+math.pi/2,b.a,b.a+math.pi/2):
                c,s=math.cos(angle),math.sin(angle)
                radius=sum((abs(math.cos(t-angle))+abs(math.sin(t-angle)))/2 for t in (a.a,b.a))
                if abs(dx*c+dy*s)>=radius-2e-9:
                    separated=True; break
            assert separated, ('overlap',i,k,a,b)
            comparisons+=1
        active.append((high,left,right,i))
    return comparisons


# Adapted affine flow core: restricted initial interval and persistent histories.
# Persistent lists avoid quadratic tuple copying on thousands of levels.
def interval_flow(r,profiles,conf,delta,tau):
    # State consists entirely of affine functions of the original floor x.
    todo=[(r.window[0],r.window[1],-1,(1.,0.),const(0.),const(0.),None,None,None)]; out=[]
    def flatten(node):
        result=[]
        while node is not None:
            v,node=node; result.append(v)
        return tuple(reversed(result))
    while todo:
        lo,hi,em,s,G,V,chain,entries,segs=todo.pop()
        base,u,n,_=r.emitters[em]
        cuts=[p[0] for p in profiles[em]]+[p[1] for p in profiles[em]]
        cuts += [c for ab in conf.get(em,()) for c in ab]
        for a,b in split(lo,hi,s,cuts):
            mid=(a+b)/2; sm=val(s,mid)
            p=next(p for p in profiles[em] if p[0]-EPS<=sm<=p[1]+EPS)
            e=(plus(const(base[0]),scale(s,u[0])),plus(const(base[1]),scale(s,u[1])))
            if any(c-EPS<sm<d+EPS for c,d in conf.get(em,())):
                out.append(PathRun(a,b,'conflict',flatten(chain),flatten(entries),flatten(segs),G,V,e,em)); continue
            rr=plus(scale(s,p[2][0]),const(p[2][1])); total=plus(G,rr)
            for aa,bb in split(a,b,total,[delta]):
                m=(aa+bb)/2; j,side=p[3:5]
                if val(total,m)>delta+EPS or j==-4:
                    travel=plus(const(delta),scale(G,-1)); kind='gap'
                else: travel=rr; kind=None
                q=moving(e,n,travel); sg=segs if abs(travel[0])+abs(travel[1])<1e-12 else ((e,q,'gap',em),segs)
                newG=plus(G,travel); newV=plus(V,scale(travel,n[1]))
                if kind is None:
                    if j==-2: kind='arrival'
                    elif j==-3: kind='wall'
                    else:
                        qm=point(q,m)
                        if any(math.dist(qm,v)<1e-10 for v in r.squares[j].vertices()): kind='exceptional'
                        elif abs(r.squares[j].a)>=tau: kind='tilt'
                        elif side!=0: kind='lateral'
                if kind:
                    out.append(PathRun(aa,bb,kind,flatten(chain),flatten(entries),flatten(sg),newG,newV,q,j)); continue
                qb,qu,qn,_=r.emitters[j]
                # Bottom left = top left - normal; s is the dot product there.
                bottom=sub(qb,qn)
                sj=plus(scale(plus(q[0],const(-bottom[0])),qu[0]),scale(plus(q[1],const(-bottom[1])),qu[1]))
                top=moving(q,qn,const(1.))
                todo.append((aa,bb,j,sj,newG,newV,(j,chain),((j,sj,q[1]),entries),((q,top,'square',j),sg)))
    return sorted(out,key=lambda p:p.lo)


def path_points(p,x):
    return [f.point(p.segments[0][0],x)]+[f.point(b,x) for a,b,kind,k in p.segments]


def order_margin(p,x,q,X):
    """Linear merge of the two height-monotone polylines, independent of x_at."""
    A=path_points(p,x); B=path_points(q,X); i=j=0
    margin=X-x; ymax=min(A[-1][1],B[-1][1])
    def at(P,i,y):
        while i+1<len(P) and P[i+1][1]<y-1e-10: i+=1
        while i+1<len(P) and P[i+1][1]-P[i][1]<1e-12: i+=1
        if i+1==len(P): return P[i][0],i
        t=(y-P[i][1])/(P[i+1][1]-P[i][1])
        return P[i][0]+t*(P[i+1][0]-P[i][0]),i
    for y in sorted(set(v[1] for v in A+B if 0<=v[1]<=ymax)):
        xx,i=at(A,i,y); XX,j=at(B,j,y)
        margin=min(margin,XX-xx)
    return margin


def runs(values):
    """Lossless index run encoding for theta_i / aligned predicates."""
    out=[]
    for i,v in enumerate(values,1):
        if out and out[-1][2]==v: out[-1]=(out[-1][0],i,v)
        else: out.append((i,i,v))
    return '; '.join('%s:%s'%((str(a) if a==b else '%d-%d'%(a,b)),fmt(v)) for a,b,v in out)


def audit(r,paths):
    arr=[p for p in paths if p.kind=='arrival']; failures=[]; checks=defaultdict(list)
    def le(number,label,lhs,rhs,witness=None):
        ok=lhs<=rhs+TOL
        checks[number].append(ok)
        if not ok: failures.append((number,label,lhs,rhs,witness))
    counts=Counter(); gap_emitters=Counter()
    height=slope=0.; minorder=math.inf
    for p in paths:
        counts[p.kind]+=p.hi-p.lo
        if p.kind=='gap': gap_emitters['floor' if not p.chain else ('layer' if r.squares[p.chain[-1]].a==0 else 'tilted')]+=p.hi-p.lo
        # Every affine identity is checked at both limiting endpoints.
        if p.kind=='arrival':
            D=p.D(r)
            for x in (p.lo,p.hi):
                height=max(height,abs(r.w+r.z*f.val(p.end[0],x)-(p.N-D+f.val(p.V,x))))
                le(1,'vertical gap range',-f.val(p.V,x),0.)
                le(1,'vertical gap budget',f.val(p.V,x),r.delta)
            kap=1.; last=0.
            for k in p.chain:
                a=r.squares[k].a; kap/=math.cos(a-last); last=a
            kp=kap*math.cos(math.atan(r.z))/math.cos(last-math.atan(r.z)) if p.N else 1.
            slope=max(slope,abs(p.end[0][0]-kp),abs(p.V[0]-r.z*kp))
            le(1,'arrival derivative positive',math.cos(math.atan(r.z)),p.end[0][0])
        # Within each affine itinerary ordering is reduced to its two limiting paths.
        margin=order_margin(p,p.lo,p,p.hi); minorder=min(minorder,margin)
        le(2,'within-itinerary order',-margin,0.,(p.lo,p.hi))
    for p,q in zip(paths,paths[1:]):
        margin=order_margin(p,p.hi,q,q.lo); minorder=min(minorder,margin)
        le(2,'adjacent limiting paths',-margin,0.,(p.hi,q.lo))
    le(1,'height identity residual',height,TOL)
    le(1,'slope identity residual',slope,TOL)
    le(2,'floor partition measure',abs(sum(counts.values())-(r.window[1]-r.window[0])),TOL)
    boundaries=[]; pos=cost=theta_sum=0.; skips=0; ratios=[]; minY=math.inf
    for k,(p,q) in enumerate(zip(arr,arr[1:]),1):
        drop=f.val(p.V,p.hi)-f.val(q.V,q.lo)
        Delta=f.val(q.end[0],q.lo)-f.val(p.end[0],p.hi)
        D,Dp=p.D(r),q.D(r)
        resid=abs(drop-(D-p.N-Dp+q.N-r.z*Delta))
        le(3,'6.1 identity',resid,TOL,(k,p.hi,q.lo))
        le(3,'drop budget',drop,r.delta,(k,p.hi,q.lo))
        le(2,'arrival ordering',-Delta,0.,(k,p.hi,q.lo))
        # Distinct interior representatives on either side of every boundary.
        xp=p.hi-min((p.hi-p.lo)/4,1e-7)
        xq=q.lo+min((q.hi-q.lo)/4,1e-7)
        cumulative=Theta=bcost=0.; angles=[]; aligned=[]; Ys=[]
        for i,(e,ee) in enumerate(zip(p.entries,q.entries),1):
            a,_,h=e; b,_,hh=ee
            angle=f.theta(r.squares[a].a,r.squares[b].a)
            isaligned=r.tau*cumulative<.25
            cumulative+=angle
            if isaligned: Theta+=angle; aligned.append(i)
            h1=f.val(h,xp); h2=f.val(hh,xq)
            Y=max(0.,min(h1+math.cos(r.squares[a].a),h2+math.cos(r.squares[b].a))-max(h1,h2))
            bcost+=angle*Y; angles.append(angle); Ys.append(Y)
            if isaligned:
                minY=min(minY,Y)
                bound=.7 if r.delta==1/32 else math.cos(r.tau)-.25-r.delta
                le(6,'aligned overlap',bound,Y,(k,i,a,b,xp,xq))
        skip=Delta>=1/(2*r.z)-TOL
        skips+=skip
        if drop>f.EPS:
            pos+=drop
            le(5,'paid or skip',drop,math.inf if skip and q.N>p.N else r.tau*Theta,(k,p.N,q.N,Delta,xp,xq))
            if not skip: ratios.append(drop/(r.tau*Theta) if Theta else math.inf)
        theta_sum+=Theta; cost+=bcost
        boundaries.append(dict(k=k,N=p.N,Np=q.N,D=D,Dp=Dp,drop=drop,Delta=Delta,resid=resid,
                               Theta=Theta,angles=runs(angles),aligned=runs([int(i<=len(aligned)) for i in range(1,len(angles)+1)]),
                               minY=min(Ys,default=math.inf),maxY=max(Ys,default=0.),cost=bcost,skip=skip,
                               coordinates=(p.hi,q.lo)))
    lower=math.sin(math.atan(r.z))*counts['arrival']-r.delta
    le(4,'Lemma 6.1',lower,pos)
    le(7,'Lemma 5.1',cost,14851*r.W)
    combined=r.tau*theta_sum+r.delta*skips
    le(8,'combined inequality',pos,combined)
    return dict(arr=arr,counts=counts,gap_emitters=gap_emitters,failures=failures,checks=checks,height=height,slope=slope,minorder=minorder,
                boundaries=boundaries,positive=pos,lower=lower,cost=cost,theta=theta_sum,skips=skips,
                ratios=ratios,minY=minY,combined=combined)


def render(r,a,elapsed,validated,stages):
    lines=['## '+r.name,'',
           '| Quantity | Value |','|---|---:|']
    def row(k,v): lines.append('| %s | %s |'%(k,v))
    for k,v in [('L',r.L),('rise',r.z*r.L),('zeta',r.z),('w',r.w),('alpha',r.alpha),('delta',r.delta),('tau',r.tau),
                ('m',r.m),('xi_0',r.xi0),('columns',len(r.meta)),('accepted squares',len(r.squares)),('candidates rejected',r.candidates-len(r.squares)),
                ('waste W',r.W),('waste / area',r.W/(r.L*r.w+r.z*r.L*r.L/2)),('arrival measure',a['counts']['arrival']),
                ('arrival fraction in audited window',a['counts']['arrival']/(r.window[1]-r.window[0])),('itinerary intervals',len(a['allpaths'])),
                ('arriving intervals',len(a['arr'])),('positive-drop boundaries',len(a['ratios'])+sum(b['skip'] and b['drop']>f.EPS for b in a['boundaries'])),
                ('height residual',a['height']),('slope residual',a['slope']),('minimum order margin (limits)',a['minorder']),
                ('sum positive drops',a['positive']),('sin(zeta-prime) * arrival measure - delta',a['lower']),
                ('check 4 lower / positive drops',a['lower']/a['positive'] if a['positive'] else None),
                ('sum Theta',a['theta']),('skips',a['skips']),('non-skip positive-drop ratio max',max(a['ratios'],default=None)),
                ('non-skip positive-drop ratio median',statistics.median(a['ratios']) if a['ratios'] else None),
                ('minimum aligned overlap',a['minY']),('aligned overlap bound',.7 if r.delta==1/32 else math.cos(r.tau)-.25-r.delta),
                ('sum theta_i * Y_i',a['cost']),('14851 W',14851*r.W),('local cost ratio sum / W',a['cost']/r.W),
                ('check 7 sum / (14851 W)',a['cost']/(14851*r.W)),('combined RHS',a['combined']),
                ('check 8 positive drops / RHS',a['positive']/a['combined'] if a['combined'] else None),
                ('independent SAT candidate pairs',validated),('runtime seconds',elapsed)]:
        row(k,fmt(v))
    for kind,value in sorted(a['counts'].items()): row('ending measure: '+kind,fmt(value))
    for kind,value in sorted(a['gap_emitters'].items()): row('gap death last emitter: '+kind,fmt(value))
    for n in range(1,9): row('check '+str(n),('PASS' if all(a['checks'][n]) else 'FAIL')+' (%d comparisons)'%len(a['checks'][n]))
    lines+=['','Audited floor window: `'+repr(r.window)+'`; fraction denominator is its width. Full-floor arrival lower bound: '+fmt(a['counts']['arrival']/r.L)+'.','','Stage seconds: '+', '.join(k+'='+fmt(v) for k,v in stages.items())+'.','',
            'Columns `(xi, J, n, alpha)`:', '', '`'+'; '.join('('+', '.join(fmt(x) for x in v)+')' for v in r.meta)+'`','',
            'Arriving intervals J_k (open endpoints):','',
            '; '.join('%d: (%s, %s)'%(i,fmt(p.lo),fmt(p.hi)) for i,p in enumerate(a['arr'],1)), '',
            '| k | N | N-prime | D_k | D_next | drop | Delta | (6.1) residual | Theta | skip | theta_i index runs | aligned index runs (1=yes) | min Y | max Y | sum theta Y |',
            '|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---:|---:|---:|']
    for b in a['boundaries']:
        lines.append('| '+' | '.join(str(b[k]) if k in ('k','N','Np','skip','angles','aligned') else fmt(b[k]) for k in
                     ('k','N','Np','D','Dp','drop','Delta','resid','Theta','skip','angles','aligned','minY','maxY','cost'))+' |')
    if r.removed:
        lines+=['','Removed squares (center X, center Y, angle): `'+repr([(s.x,s.y,s.a) for s in r.removed])+'`.']
    return lines


def main():
    started=time.monotonic(); sections=[]; summary=[]; allfail=[]
    for alpha,delta,tau in ((.07,1/8,.08),(.02,1/32,.05)):
        for variant in (('clean','removed','two-tilts','brick-offsets') if alpha==.07 else ('clean',)):
            t=time.monotonic(); r=construct(alpha,delta,tau,variant); stages={'construction':time.monotonic()-t}
            print(r.name,'squares',len(r.squares),'columns',len(r.meta),flush=True)
            u=time.monotonic(); validated=independent_validate(r); stages['validation']=time.monotonic()-u
            u=time.monotonic(); profiles=r.profiles(delta); stages['profiles']=time.monotonic()-u
            u=time.monotonic(); bypair,conf=f.conflict_intervals(r,profiles,tau); stages['conflicts']=time.monotonic()-u
            u=time.monotonic(); paths=interval_flow(r,profiles,conf,delta,tau); stages['flow']=time.monotonic()-u
            u=time.monotonic(); a=audit(r,paths); stages['audit']=time.monotonic()-u
            a['allpaths']=paths
            elapsed=time.monotonic()-t
            print('  arrival',fmt(a['counts']['arrival']/(r.window[1]-r.window[0])),'deaths',dict(a['counts']),'failures',len(a['failures']),'seconds',fmt(elapsed),flush=True)
            sections+=render(r,a,elapsed,validated,stages)
            summary.append((r.name,a['counts']['arrival']/(r.window[1]-r.window[0]),a['lower']/a['positive'] if a['positive'] else 0.,max(a['ratios'],default=0.),a['cost']/r.W,a['positive']/a['combined'] if a['combined'] else 0.,len(a['failures'])))
            for failure in a['failures']: allfail.append((len(r.squares),r.name,failure,r))
            del profiles,bypair,conf,paths,a
    elapsed=time.monotonic()-started
    lines=['# Staircase wedge flow audit','',
           'Generated by `python3 -I tools/wedge_staircase_check.py`. All numbers below are from this run. Standard library only. Full floor (0,80) for all four alpha=0.07 variants; a six-unit interior floor window for one alpha=0.02 clean case (see its table).', '',
           '## Construction and verification','',
           'Rise is 0.5 and L=80. m=ceil(rise/(1-cos(alpha)))+20. Slabs have xi spacing sec(alpha); each J is the largest monotone integer satisfying all ceiling vertex inequalities. Tilted candidates precede axis-layer candidates in the containment/SAT filter. Each layer begins at the first slab with J>j. Additional integer grid candidates fill the left wedge only where a full cell fits. The two-tilt groups use slab-boundary separation at the joining height, with the additional horizontal gap needed for the new top to fit. Fixed random seed: 20261109.', '',
           'The imported simulator constructs exact affine itinerary pieces using analytic ray/edge intersections and a spatial index. It computes conflicts before flow. Independent validation uses a separate Y sweep, center/radius SAT and linear-functional containment; it does not call the constructor overlap or containment predicates. All packings passed this validation. Arithmetic is floating point, not a formal certificate; comparison tolerance is 2e-7, validation contact tolerance 2e-9. The ordering audit merges complete polylines at all vertex heights, both within each affine interval and across adjacent interval limits. Affine height/slope identities use endpoint limits, not just interior samples.', '',
           '| Packing | Arrival fraction | check 4 lower/drops | check 5 max drop/(tau Theta) | check 7 sum/W | check 8 drops/RHS | failures |',
           '|---|---:|---:|---:|---:|---:|---:|']
    lines+=['| '+' | '.join(str(x) if isinstance(x,str) else fmt(x) for x in row)+' |' for row in summary]
    lines+=['','## Ambiguities','',
            '- “Lowest vertex” in the specification is P (minimum Y), whereas minimum X is the top-left vertex. xi_0=m sin(alpha)+0.02 clears the latter. Containment tests every vertex.',
            '- “As far as they fit” means increasing i>=0, then the common acceptance filter. Left fillers start on the integer X grid; brick rows use one independent uniform offset per integer Y row, shared by the main layer and left-filler families.',
            '- “A few removed” means exactly three uniformly sampled tilted and three layer candidates before filtering, fixed seed. Removed candidate coordinates are listed.',
            '- The two-tilt split is halfway across the clean columns measured by their bottom footprints, excluding the left-wall clearance strip. The split is computed from the linear ceiling constraint before rounding J. Slab separation at the minimum joining height, plus the required ceiling-clearance gap, separates the groups; its arrival penalty is reported.',
            '- Intervals are the simulator’s affine partition, including harmless extra cuts from projected vertices. Extra zero-drop boundaries are retained. No positive-measure exceptional intervals are discarded.',
            '- Boundary drops and Delta use one-sided limits; tube representatives lie 1e-7 or one quarter interval width inside the adjacent intervals. The two representatives in an interval remain strictly ordered. theta index runs are lossless; aligned status is reported for every paired index; Y minima/maxima summarize the individually checked levels.',
            '- Lemma 6.2 is checked on all aligned levels, including zero or negative drop boundaries. At delta=1/8 its threshold is cos(tau)-1/4-delta; raw minima are also reported. The paid-or-skip inequality itself has no 0.7 constant to replace.',
            '- A skip in check 8 means Delta>=1/(2 zeta), as in Proposition 7.1. Check 5 additionally requires N-prime>N. Positive means drop>2e-10, matching the geometry epsilon. Smaller signed drops remain in the boundary table.',
            '- “True local cost” is reported as sum(theta_i |Y_i|)/W, as explicitly requested; W is actual total area minus accepted square count. This is not an independent computation of tube-local uncovered area.',
            '- The optional alpha=0.02 case is the clean packing only. The four variants are all run at alpha=0.07. Full small-angle sweeps were interrupted during exploratory runs because the deep layer seams multiply affine itineraries; the six-unit window keeps the final run bounded while its Lemma 6.1 lower bound remains positive. Geometry and independent validation still cover the full 199030-square packing.',
            '- No Proposition 7.1 small-waste hypothesis is assumed. No claim of validating that hypothesis or the theorem follows from these numerical checks.', '',
            '## Failures and anomalies','']
    if allfail:
        allfail.sort(key=lambda v:(v[0],v[1],str(v[2])))
        lines.append('%d failed comparisons. Smallest tested packing with a failure:'%len(allfail))
        n,name,fail,r=allfail[0]
        lines+=['',repr((n,name,fail)),'']
        wit=fail[-1]
        if fail[0]==6:
            _,_,i,j,x,X=wit
            for k in (i,j): lines.append('Square %d: center=%r; angle=%r; vertices=%r.'%(k,(r.squares[k].x,r.squares[k].y),r.squares[k].a,r.squares[k].vertices()))
    else: lines.append('No failed comparisons.')
    for name,arrival,*_ in summary:
        if arrival<=.6: lines.append('- '+name+': arrival target not met. The ending-measure table identifies the dominant death; construction diagnosis below.')
    lines+=['', 'Small-angle diagnosis: m sin(alpha) is about rise*cot(alpha/2), so wall clearance alone can consume much of an 80-wide floor. The alpha=0.02 runs therefore audit an interior floor window; their full-floor lower bounds are also reported explicitly. Brick offsets create holes at the layer/tilt seam: random row phases leave up to one unit horizontally unsupported, much larger than delta. SAT rejection prevents plugging those holes with squares on that same row phase. The two-tilt ceiling-clearance gap also creates deaths. Compare ending measures with the clean case; low-arrival variants are diagnoses, not successful majority-arrival claims.', '',
            'Total runtime: '+fmt(elapsed)+' seconds.']
    lines+=['']+sections
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text('\n'.join(lines)+'\n')
    print('REPORT',REPORT,'total seconds',fmt(elapsed),'failures',len(allfail),flush=True)


if __name__=='__main__':
    main()
