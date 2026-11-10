#!/usr/bin/env python3
"""Deterministic, offline numerical checks of docs/slab-lower-bound.md.

Run from the repository root with python3 -I tools/slab_flow_check.py.
Only the requested Markdown report is written. Geometry uses analytic edge/ray
intersections; sampling estimates measures, never square occupancy.
"""
import math
import random
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

EPS = 2e-10
GRID = 100000
OFFSET = 0.3819660112501051
REPORT = Path('runs/k2c-exponent-2026-11-09/flow-check.md')


@dataclass(frozen=True)
class Square:
    x: float
    y: float
    a: float = 0.0

    def vertices(self):
        c, s = math.cos(self.a), math.sin(self.a)
        return [(self.x + p*c-q*s, self.y+p*s+q*c)
                for p, q in [(-.5,-.5),(.5,-.5),(.5,.5),(-.5,.5)]]


def overlap(a, b):
    # Independent separating-axis test, using projections of all four vertices.
    av, bv = a.vertices(), b.vertices()
    for t in (a.a, a.a+math.pi/2, b.a, b.a+math.pi/2):
        c, s = math.cos(t), math.sin(t)
        aa = [x*c+y*s for x,y in av]
        bb = [x*c+y*s for x,y in bv]
        if min(max(aa),max(bb))-max(min(aa),min(bb)) <= EPS:
            return False
    return True


class Region:
    def __init__(self, name, L, w, z, squares):
        self.name, self.L, self.w, self.z = name,L,w,z
        self.squares = squares
        self.M = max(w,w+z*L)
        self.W = L*w+z*L*L/2-len(squares)
        self.cells = defaultdict(list)
        self.edges = []
        for k,q in enumerate(squares):
            vv = q.vertices()
            ee=[]
            for i in range(4):
                x,y=vv[i]; X,Y=vv[(i+1)%4]
                # edge labels: bottom, right lateral, top, left lateral
                if abs(X-x)>1e-14:
                    slope=(Y-y)/(X-x)
                    ee.append((min(x,X),max(x,X),slope,y-slope*x,i))
            self.edges.append(ee)
            for ix in range(math.floor(min(x for x,y in vv)),math.floor(max(x for x,y in vv))+1):
                for iy in range(math.floor(min(y for x,y in vv)),math.floor(max(y for x,y in vv))+1):
                    self.cells[ix,iy].append(k)

    def inside(self,q):
        return all(-EPS<=x<=self.L+EPS and y>=-EPS and y<=self.w+self.z*x+EPS
                   for x,y in q.vertices())

    def validate(self):
        for k,q in enumerate(self.squares):
            assert self.inside(q), (self.name,'outside',k,q)
        pairs=set()
        for ids in self.cells.values():
            for j,k in enumerate(ids):
                for l in ids[j+1:]:
                    pairs.add((min(k,l),max(k,l)))
        for k,l in pairs:
            assert not overlap(self.squares[k],self.squares[l]), (self.name,'overlap',k,l)
        assert self.W>=-EPS
        return len(pairs)

    def hit(self,x,y,previous,reverse=False):
        # Scan spatial cells in ray order, then intersect actual square edges.
        direction=-1 if reverse else 1
        boundary=0.0 if reverse else self.w+self.z*x
        cy=math.floor(y)
        end=math.floor(boundary)
        best=None
        seen=set()
        for iy in range(cy,end+direction,direction):
            for k in self.cells.get((math.floor(x),iy),()):
                if k==previous or k in seen:
                    continue
                seen.add(k)
                hits=[(m*x+b,e) for lo,hi,m,b,e in self.edges[k]
                      if lo-EPS<=x<=hi+EPS]
                if not hits:
                    continue
                h,e=(max(hits) if reverse else min(hits))
                if direction*(h-y)<-EPS or direction*(boundary-h)<-EPS:
                    continue
                candidate=(max(0.0,direction*(h-y)),k,h,e)
                if best is None or candidate<best:
                    best=candidate
            if best is not None:
                # All cells up to and including candidate's cell were inspected.
                if (not reverse and best[2]<=iy+1+EPS) or (reverse and best[2]>=iy-EPS):
                    break
        if best is None:
            return boundary,-1,-1
        return best[2],best[1],best[3]

    def trace(self,x,reverse=False):
        """Cache maximal relevant geometric trace; parameter cuts are replayed.

        Each event stores (square id, side, cumulative G, N, D, current x).
        Steep at .08 or gap > .4 stops all requested parameter choices.
        """
        y=self.w+self.z*x if reverse else 0.0
        previous=-1
        G=D=0.0
        N=0
        events=[]
        for _ in range(len(self.squares)+2):
            h,k,e=self.hit(x,y,previous,reverse)
            G+=max(0.0,(y-h) if reverse else (h-y))
            events.append((k,e,G,N,D,x))
            if G>.4+EPS or k<0:
                return events
            q=self.squares[k]
            if abs(q.a)>=.08-1e-14:
                return events
            # A vertex is exceptional even when min/max chooses one edge.
            if any(abs(x-X)<1e-11 and abs(h-Y)<1e-11 for X,Y in q.vertices()):
                events[-1]=(k,9,G,N,D,x)
                return events
            if e != (2 if reverse else 0):
                return events
            sign=-1 if reverse else 1
            x-=sign*math.sin(q.a)
            y=h+sign*math.cos(q.a)
            N+=1
            D+=1-math.cos(q.a)
            previous=k
        raise AssertionError('nonterminating trace')



def verify_rays(r):
    """Cross-check edge casting and indexing against unindexed slab clipping."""
    for reverse in (False,True):
        for i in range(64):
            x=(i+OFFSET)*r.L/64
            y=r.w+r.z*x if reverse else 0.0
            direction=-1 if reverse else 1
            boundary=0.0 if reverse else r.w+r.z*x
            expected=boundary
            best=abs(boundary-y)+EPS
            for q in r.squares:
                low,high=-math.inf,math.inf
                c,ss=math.cos(q.a),math.sin(q.a)
                for nx,ny in ((c,ss),(-ss,c)):
                    term=nx*(x-q.x)
                    if abs(ny)<1e-14:
                        if abs(term)>.5+EPS:
                            low,high=1.0,0.0
                            break
                    else:
                        a=q.y+(-.5-term)/ny
                        b=q.y+(.5-term)/ny
                        low=max(low,min(a,b)); high=min(high,max(a,b))
                if low>high+EPS: continue
                hit=high if reverse else low
                distance=direction*(hit-y)
                if -EPS<=distance<best and direction*(boundary-hit)>=-EPS:
                    best=max(0.0,distance); expected=hit
            actual,_,_=r.hit(x,y,-1,reverse)
            assert abs(actual-expected)<2e-8, (r.name,'ray mismatch',x,y,actual,expected)


def classify(region,events,delta,tau,reverse=False):
    chain=[]
    for k,e,G,N,D,x in events:
        if G>delta+EPS:
            return 'gap',N,D,delta,x,tuple(chain)
        if k<0:
            return 'arrival',N,D,G,x,tuple(chain)
        chain.append(k)
        if abs(region.squares[k].a)>=tau-1e-14:
            return 'tilt',N,D,G,x,tuple(chain)
        if e==9:
            return 'exceptional',N,D,G,x,tuple(chain)
        if e!=(2 if reverse else 0):
            return 'lateral',N,D,G,x,tuple(chain)
    raise AssertionError('trace truncated before applicable stop')


def rows(L=40,m=6,brick=False):
    return [Square(i+.5+(.37 if brick and j%2 else 0),j+.5)
            for j in range(m) for i in range(int(L))
            if i+1+(.37 if brick and j%2 else 0)<=L]


def lattice(name,L,w,a,l,eps,z=0):
    c,s=math.cos(a),math.sin(a)
    # Inverse of basis [u-l*n, n+eps*u] bounds lattice indices.
    corners=[(0,0),(L,0),(0,w),(L,w+z*L)]
    ii=[]; jj=[]
    for x,y in corners:
        U=x*c+y*s; V=-x*s+y*c
        ii.append((U-eps*V)/(1+l*eps))
        jj.append((l*U+V)/(1+l*eps))
    r=Region(name,L,w,z,[])
    ss=[]
    for i in range(math.floor(min(ii))-2,math.ceil(max(ii))+3):
        for j in range(math.floor(min(jj))-2,math.ceil(max(jj))+3):
            U=i+j*eps; V=j-i*l
            q=Square(U*c-V*s,U*s+V*c,a)
            if r.inside(q): ss.append(q)
    return Region(name,L,w,z,ss)


def packings():
    yield Region('axis-rows',40,6.5,0,rows())
    for m in (6,20,60):
        k=m+1
        lo,hi=0.0,math.pi/4
        for _ in range(70):
            mid=(lo+hi)/2
            if k*math.cos(mid)+math.sin(mid)>m+.5: lo=mid
            else: hi=mid
        a=(lo+hi)/2; c,s=math.cos(a),math.sin(a)
        L=40
        ss=[]
        # Each stack j*n has x-extent c+k*s; pitch sec(a).
        for i in range(math.ceil(L*c)):
            base=i/c+k*s
            col=[Square(base+.5*c-(j+.5)*s,.5*s+(j+.5)*c,a) for j in range(k)]
            r=Region('',L,m+.5,0,[])
            if all(r.inside(q) for q in col): ss.extend(col)
        yield Region('EG-m%d'%m,L,m+.5,0,ss)
    for a,l,f in ((.03,.2,1),(.015,.35,1),(.045,.15,.6)):
        yield lattice('holes-a%g-l%g'%(a,l),30,8.5,a,l,f*l*math.tan(a))
    a=math.atan(.05); c,s=math.cos(a),math.sin(a)
    clip=Region('',60,3,.05,[])
    ss=[]
    for i in range(65):
        for j in range(8):
            U=i+.5; V=3*c-.5-j
            q=Square(U*c-V*s,U*s+V*c,a)
            if clip.inside(q): ss.append(q)
    yield Region('ceiling-parallel',60,3,.05,ss)
    ss=[]
    for i in range(60):
        ss.extend(Square(i+.5,j+.5) for j in range(math.floor(3+.05*i+1e-12)))
    yield Region('staircase',60,3,.05,ss)
    yield Region('brick',40,6.5,0,rows(brick=True))
    for seed in (17,29,83):
        rng=random.Random(seed)
        ss=[q for q in rows(L=16,m=5,brick=seed!=17) if rng.random()>.28]
        accepted=0
        for k in rng.sample(range(len(ss)),min(30,len(ss))):
            q=ss[k]
            candidate=Square(q.x+rng.uniform(-.08,.08),q.y+rng.uniform(-.08,.08),rng.uniform(-.075,.075))
            empty=Region('',16,5.5,0,[])
            if empty.inside(candidate) and all(not overlap(candidate,b) for j,b in enumerate(ss) if j!=k):
                ss[k]=candidate; accepted+=1
        # Ensure perturbations actually happen, in a removed-square cavity.
        yield Region('perturbed-%d-rot%d'%(seed,accepted),16,5.5,0,ss)
    # Isolated shallow tilt over a gap; mirrored version tests both lateral sides.
    for a in (.06,-.06):
        h=(math.cos(a)+abs(math.sin(a)))/2
        yield Region('overhang-%+.2f'%a,4,3,0,[Square(2,h+.04,a)])
    yield Region('vertex-touch',4,3,0,[Square(1,1,math.pi/4),Square(1+math.sqrt(2),1,math.pi/4)])
    yield Region('wall-hug',4,3,0,[Square(.5,.5),Square(3.5,.5),Square(2,1.55,.035)])
    # Non-vacuous arrivals and active lateral/tilt chains, unlike half-integer rows.
    yield Region('perfect-integer',8,4,0,rows(8,4))
    for a in (.03,-.03):
        c,s=math.cos(a),math.sin(a)
        height=3*c+abs(s)
        clip=Region('',12,height,0,[])
        ss=[]
        for i in range(12):
            base=i/c+3*abs(s)
            for j in range(3):
                q=Square(base+.5*c-(j+.5)*abs(s),.5*abs(s)+(j+.5)*c,abs(a))
                if a<0: q=Square(12-q.x,q.y,a)
                if clip.inside(q): ss.append(q)
        yield Region('flat-arrivals-%+.2f'%a,12,height,0,ss)
    yield Region('tilt-chain',4,3,0,[Square(1.5,.5),Square(1.5,1.56,.09)])
    # A very small single-square lateral-death example with near-zero waste.
    a=.04; c,s=math.cos(a),math.sin(a)
    yield Region('single-tight',c+s,c+s,0,[Square((c+s)/2,(c+s)/2,a)])


def a_measure(r,d):
    if not r.z:
        return r.L if abs(r.w-round(r.w))<=d+EPS else 0.0
    intervals=[]
    for n in range(math.floor(min(r.w,r.w+r.z*r.L)-d)-1,math.ceil(r.M+d)+2):
        aa=(n-d-r.w)/r.z; bb=(n+d-r.w)/r.z
        lo=max(0,min(aa,bb)); hi=min(r.L,max(aa,bb))
        if hi>lo: intervals.append((lo,hi))
    return sum(b-a for a,b in intervals)


def union_length(intervals):
    total=over=0.0
    end=-math.inf
    for a,b in sorted(intervals):
        over+=max(0,min(end,b)-a)
        total+=max(0,b-max(a,end))
        end=max(end,b)
    return total,over


def check(r,forward,backward,d,t):
    h=r.L/GRID
    counts=Counter(); arrivals=[]; intervals=[]
    maxheight=maxtranslation=0.0
    minchain=math.inf
    amin=math.inf
    fail=[]; witnesses=[]
    prev=None; runstart=None; last=None; runs=0
    active=.502*r.M*t*t<=d+EPS
    for i,events in enumerate(forward):
        x=(i+OFFSET)*h
        kind,N,D,G,X,chain=classify(r,events,d,t)
        counts[kind]+=1
        key=(kind,chain)
        if prev is not None and key==prev[0]:
            maxtranslation=max(maxtranslation,abs((x-X)-prev[1]))
        if kind=='arrival':
            err=max(abs(r.w+r.z*X-(N-D+G)),
                    abs(X-(x-sum(math.sin(r.squares[k].a) for k in chain))))
            maxheight=max(maxheight,err)
            arrivals.append(X)
            if active:
                amin=min(amin,r.w+r.z*X-(N-d),N+d-(r.w+r.z*X))
            if active and not N-d-EPS<=r.w+r.z*X<=N+d+EPS:
                witnesses.append(('A inclusion',x,chain))
        if kind=='tilt':
            angles=[0.0]+[r.squares[k].a for k in chain]
            variation=sum(min(abs(b-a),math.pi/2-abs(b-a)) for a,b in zip(angles,angles[1:]))
            minchain=min(minchain,variation)
            if variation<t-EPS: witnesses.append(('chain',x,chain))
        if last!=key:
            if runstart is not None:
                intervals.append((runstart,prevX))
            runstart=X if kind=='arrival' else None
            if kind=='arrival': runs+=1
        elif kind=='arrival':
            pass
        prev=(key,x-X); last=key; prevX=X
    if runstart is not None: intervals.append((runstart,prevX))
    image,over=union_length(intervals)
    arrivals.sort()
    mindist=min((b-a for a,b in zip(arrivals,arrivals[1:])),default=math.inf)
    reverse_count=sum(classify(r,ee,d,t,True)[0]=='arrival' for ee in backward)
    measure={k:counts[k]*h for k in ('gap','tilt','lateral','arrival','exceptional')}
    # Safe interior intervals omit at most one grid cell per itinerary run.
    sample_budget=(2*runs+4)*h
    conservation=max(abs(image-measure['arrival']),abs(reverse_count*h-measure['arrival']))
    bounds=[r.W/d,1350*r.W/t,math.sqrt(max(0,21*t*len(r.squares)*r.W))]
    slacks=[b-measure[k] for b,k in zip(bounds,('gap','tilt','lateral'))]
    A=a_measure(r,d)
    lhs=r.L-A
    rhs=r.W/d+1350*r.W/t+math.sqrt(max(0,21*t*r.M*r.L*r.W))
    checks={'height':maxheight<2e-8,'translation':maxtranslation<2e-8,
            'injectivity':mindist>EPS and over<2e-8,
            'conservation':conservation<=sample_budget+2e-8,
            'gap':slacks[0]>=-2*h-EPS,'tilt':slacks[1]>=-2*h-EPS,
            'chain':minchain>=t-EPS,'lateral':slacks[2]>=-2*h-EPS,
            'A':not witnesses,'S':not active or lhs<=rhs+EPS}
    assert sum(counts.values())==GRID
    fail=[k for k,v in checks.items() if not v]
    return dict(measure=measure,bounds=bounds,slacks=slacks,A=A,lhs=lhs,rhs=rhs,
                active=active,height=maxheight,translation=maxtranslation,image=image,
                reverse=reverse_count*h,conservation=conservation,budget=sample_budget,
                mindist=mindist,over=over,minchain=minchain,amin=amin,fail=fail,witnesses=witnesses,runs=runs)


def fmt(x):
    return '—' if math.isinf(x) else '%.7g'%x


def main():
    start=time.monotonic()
    out=['# Slab flow numerical check — 2026-11-09','',
         '## Method','',
         'Python 3 standard library only; deterministic 100,000-point uniform grids per packing, '
         'offset by (3−√5)/2 cells. All squares are checked for containment using their vertices '
         'and for disjoint interiors using a separate four-axis SAT (absolute tolerance 2e−10). '
         'Waste is exact region area minus square count. Each packing passes 128 ray cross-checks against unindexed square-axis slab clipping. Spatial unit cells accelerate queries only; '
         'every vertical ray intersects analytic square edges. No pixel occupancy is used.', '',
         'Forward traces retain each hit square/side, cumulative gap G, crossing count N, deficit D, '
         'current abscissa and chain. Parameter replay applies gap, ceiling, tilt, lateral and vertex '
         'priority in that order. Every arriving sample checks both (3.1) and integer-band inclusion. '
         'Inclination distance is taken modulo π/2 and includes the floor in tilt chains.', '',
         'Conservation has two checks: union of translated intervals between consecutive samples '
         'with identical itineraries, and independent backward traces from a uniform ceiling grid. '
         'Image overlap is tested on the interior intervals; distinct sampled arrival abscissas are '
         'also tested directly. Translation is checked for all ending types. Measure tolerance is '
         'two grid cells for death inequalities, and (2×arrival itinerary runs+4) cells for conservation. '
         'The latter is a discretization allowance, not an analytic error certificate for arbitrarily '
         'thin missed intervals. Numerical sampling cannot prove the lemmas.', '',
         '## Ambiguities','',
         '- “Reaches δ” in the request versus “would exceed δ” in Section 3: use the note’s strict '
         'exceedance rule; equality permits the next event (tolerance 2e−10).',
         '- A ceiling point belonging to a square follows square-event priority, because step 2 '
         'requires “in no square”. A crossing ending on the ceiling arrives on the following ray '
         'after excluding the square just left.',
         '- Flat-square vertices are exceptional, not one of the four endings; report their measure '
         'separately. Steep-square vertices are tilt deaths. Generic offset avoids most flat vertices; '
         'exact coincidences are retained and reported.',
         '- M is the actual maximum of the affine ceiling. Use δ′=δ, all nine Cartesian choices '
         'of δ and τ, plus the prescribed adaptive τ for each δ (deduplicated). Section 5 checks '
         'are marked NA if its hypothesis fails.',
         '- Erdos–Graham columns mean m+1 squares separated by n, with neighboring column bases '
         'separated by sec(θ); choose the positive nonzero root and discard whole protruding columns. '
         'Staircase columns use the minimum ceiling height over each unit-width column.',
         '- Backward traces use the symmetric top-to-bottom normal crossing and the same gap budget; '
         'this is an independent numerical inverse check, not an additional rule in the note.', '',
         '## Packings and independent validation','',
         '| Packing | L | w | ζ | n | W | SAT candidate pairs |',
         '|---|---:|---:|---:|---:|---:|---:|']
    results=[]; metadata=[]; failures=[]; exceptionals=[]
    for r in packings():
        pairs=r.validate()
        verify_rays(r)
        metadata.append((r,pairs))
        out.append('| %s | %g | %g | %g | %d | %s | %d |'%(r.name,r.L,r.w,r.z,len(r.squares),fmt(r.W),pairs))
        h=r.L/GRID
        forward=[r.trace((i+OFFSET)*h) for i in range(GRID)]
        backward=[r.trace((i+OFFSET)*h,True) for i in range(GRID)]
        for d in (1/24,.2,.4):
            ts=sorted(set((.02,.05,.08,min(.08,math.sqrt(d/(.502*r.M))))))
            for t in ts:
                result=check(r,forward,backward,d,t)
                results.append((r,d,t,result))
                if result['fail']: failures.append((r,d,t,result))
                if result['measure']['exceptional']: exceptionals.append((r.name,d,t,result['measure']['exceptional']))
        print('%s: n=%d W=%.8g (%0.1fs)'%(r.name,len(r.squares),r.W,time.monotonic()-start),flush=True)
    out+=['','## Per-parameter results','',
          'All measures are horizontal lengths. G/T/B/R = gap/tilt/lateral/arrival; E = exceptional. '
          'The three lemma columns give sampled left side ≤ analytic right side. S uses exact |A|. '
          'C is max(image-union error, reverse-grid measure error) / allowed sampling error. '
          'θmin is minimum chain variation among tilt deaths; “—” means no tilt deaths. '
          'H is the maximum residual of either identity in (3.1); Tr is the maximum local translation discrepancy. '
          'Each row’s status covers all checks, including injectivity, A inclusion when active, '
          'and the chain threshold. Rows with NA still test all other checks.','',
          '| Packing | δ | τ | G / T / B / R / E | Gap ≤ W/δ | Tilt ≤ 1350W/τ | Lateral ≤ √(21τnW) | H / Tr | min spacing / overlap | C / budget | θmin ≥ τ | R image / reverse | S: L−A ≤ RHS | Status |',
          '|---|---:|---:|---|---|---|---|---|---|---|---|---|---|---|']
    for r,d,t,v in results:
        mm=v['measure']
        ss=' / '.join(fmt(mm[k]) for k in ('gap','tilt','lateral','arrival','exceptional'))
        le=['%s ≤ %s'%(fmt(mm[k]),fmt(b)) for k,b in zip(('gap','tilt','lateral'),v['bounds'])]
        theorem='%s ≤ %s'%(fmt(v['lhs']),fmt(v['rhs'])) if v['active'] else 'NA (hypothesis)'
        out.append('| %s | %s | %s | %s | %s | %s | %s | %s / %s | %s / %s | %s / %s | %s | %s / %s | %s | %s |'%(
            r.name,fmt(d),fmt(t),ss,*le,fmt(v['height']),fmt(v['translation']),fmt(v['mindist']),fmt(v['over']),fmt(v['conservation']),fmt(v['budget']),fmt(v['minchain']),fmt(v['image']),fmt(v['reverse']),theorem,'FAIL '+','.join(v['fail']) if v['fail'] else 'PASS'))
    out+=['','## Worst slack and numerical residuals','',
          'Slack = analytic RHS minus sampled LHS (no sampling allowance added).','',
          '| Check | Minimum slack | Packing | δ | τ |','|---|---:|---|---:|---:|']
    for k,label in enumerate(('Gap','Tilt','Lateral','Theorem S')):
        choices=[(v['slacks'][k] if k<3 else v['rhs']-v['lhs'],r.name,d,t) for r,d,t,v in results if k<3 or v['active']]
        slack,name,d,t=min(choices)
        out.append('| %s | %s | %s | %s | %s |'%(label,fmt(slack),name,fmt(d),fmt(t)))
    out+=['','Minimum slack among positive-waste packings:','',
          '| Check | Minimum slack | Packing | δ | τ |','|---|---:|---|---:|---:|']
    for k,label in enumerate(('Gap','Tilt','Lateral','Theorem S')):
        choices=[(v['slacks'][k] if k<3 else v['rhs']-v['lhs'],r.name,d,t)
                 for r,d,t,v in results if r.W>EPS and (k<3 or v['active'])]
        slack,name,d,t=min(choices)
        out.append('| %s | %s | %s | %s | %s |'%(label,fmt(slack),name,fmt(d),fmt(t)))
    chain_slack,name,d,t=min((v['minchain']-t,r.name,d,t) for r,d,t,v in results if not math.isinf(v['minchain']))
    out.append('\nMinimum tilt-chain slack Σθ−τ: %s (%s, δ=%s, τ=%s).'%(fmt(chain_slack),name,fmt(d),fmt(t)))
    a_slack,name,d,t=min((v['amin'],r.name,d,t) for r,d,t,v in results if not math.isinf(v['amin']))
    out.append('\nMinimum arrival integer-band margin: %s (%s, δ=%s, τ=%s).'%(fmt(a_slack),name,fmt(d),fmt(t)))
    for key,label in (('height','height/abscissa identities'),('translation','local translation'),('over','arrival interval overlap'),('conservation','conservation difference')):
        v,r,d,t=max((v[key],r.name,d,t) for r,d,t,v in results)
        out.append('\nMaximum %s: %s (%s, δ=%s, τ=%s).'%(label,fmt(v),r,fmt(d),fmt(t)))
    out+=['','## Failures and anomalies','']
    if not failures: out.append('- No failed checks on the sampled paths. This is numerical evidence only.')
    for r,d,t,v in failures:
        out.append('- FAIL %s δ=%s τ=%s: %s.'%(r.name,fmt(d),fmt(t),', '.join(v['fail'])))
        # Pointwise failures reduce to their witnessed chain (deleting other squares
        # leaves that path unchanged). Global measure failures retain full packing.
        witness=v['witnesses'][0] if v['witnesses'] else None
        ids=witness[2] if witness else tuple(range(len(r.squares)))
        out.append('  Witness region L=%r, w=%r, ζ=%r; %s.'%(r.L,r.w,r.z,repr(witness)))
        out.append('  Squares (cx, cy, angle radians): '+repr([(r.squares[k].x,r.squares[k].y,r.squares[k].a) for k in ids]))
    out.append('- Exceptional sampled paths: '+('none.' if not exceptionals else repr(exceptionals)))
    out.append('- All requested packing families were tested; perturbation names state accepted rotations. '
               'Additional probes: mirrored overhangs, vertex contacts, wall-hugging squares, perfect integer '
               'rows (zero waste and arrivals), a flat rotated grid with arrivals, an upright-to-steep chain, '
               'and a single tilted square in its tight bounding rectangle.')
    out.append('- Coarse universal constants make the tilt and Theorem S inequalities loose in most cases; '
               'passing them does not meaningfully certify those constants. Chain, ray geometry, image '
               'overlap and height checks give more direct tests of the flow.')
    elapsed=time.monotonic()-start
    out+=['','%d packings; %d parameter rows; %d FAIL rows. %s forward + reverse starting points per packing. '
          'Runtime %.2f seconds.'%(len(metadata),len(results),len(failures),format(GRID,','),elapsed),'']
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text('\n'.join(out))
    print('Report:',REPORT,'FAIL rows:',len(failures),'seconds:',round(elapsed,2),flush=True)
    return bool(failures)


if __name__=='__main__':
    raise SystemExit(main())
