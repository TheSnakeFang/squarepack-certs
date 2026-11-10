#!/usr/bin/env python3
"""Offline interval and sampled audit of wedge-lower-bound.md. No dependencies.
Only writes runs/k2c-exponent-2026-11-09/wedge-flow-check.md.
Geometry copied/adapted from slab_flow_check.py: Square, SAT, spatial index,
analytic edge casting and lattice/column generators. Run with python3 -I.
"""
import math
import random
import time
from collections import defaultdict, Counter
from dataclasses import dataclass
from pathlib import Path
EPS = 2e-10
TOL = 2e-7
REPORT = Path('runs/k2c-exponent-2026-11-09/wedge-flow-check.md')
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


def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def mul(a,t): return (a[0]*t,a[1]*t)
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def theta(a,b):
    d=abs(a-b)%(math.pi/2)
    return min(d,math.pi/2-d)
def val(a,x): return a[0]*x+a[1]
def plus(a,b): return (a[0]+b[0],a[1]+b[1])
def scale(a,s): return (a[0]*s,a[1]*s)
def const(x): return (0.,x)
def point(p,x): return (val(p[0],x),val(p[1],x))
def moving(p,n,r): return (plus(p[0],scale(r,n[0])),plus(p[1],scale(r,n[1])))
def unique(xs):
    out=[]
    for x in sorted(xs):
        if not out or x-out[-1]>EPS: out.append(x)
    return out

def union(xs):
    out=[]
    for a,b in sorted(xs):
        if b-a<=EPS: continue
        if out and a<=out[-1][1]+EPS: out[-1]=(out[-1][0],max(b,out[-1][1]))
        else: out.append((a,b))
    return out

def measure(xs): return sum(b-a for a,b in union(xs))
def onseg(p,a,b):
    v=sub(b,a); w=sub(p,a)
    return abs(cross(v,w))<=EPS*(1+math.hypot(*v)) and dot(w,sub(p,b))<=EPS

def inside_poly(p,poly):
    area=sum(cross(a,b) for a,b in zip(poly,poly[1:]+poly[:1]))
    if abs(area)<EPS:
        return any(onseg(p,a,b) for a,b in zip(poly,poly[1:]+poly[:1]))
    sign=1 if area>0 else -1
    return all(sign*cross(sub(b,a),sub(p,a))>=-EPS for a,b in zip(poly,poly[1:]+poly[:1]))

def intersection_points(a,b):
    pts=[p for p in a if inside_poly(p,b)]+[p for p in b if inside_poly(p,a)]
    for p,q in zip(a,a[1:]+a[:1]):
        v=sub(q,p)
        for r,s in zip(b,b[1:]+b[:1]):
            w=sub(s,r); det=cross(v,w)
            if abs(det)<1e-14: continue
            t=cross(sub(r,p),w)/det; u=cross(sub(r,p),v)/det
            if -EPS<=t<=1+EPS and -EPS<=u<=1+EPS: pts.append(add(p,mul(v,t)))
    return pts

class Region:
    def __init__(self,name,L,w,z,candidates):
        self.name,self.L,self.w,self.z=name,L,w,z
        self.squares=[]; self.cells=defaultdict(list)
        # Greedy acceptance, then a separately enumerated SAT validation below.
        for q in candidates:
            if not self.inside(q): continue
            vv=q.vertices(); ids=set()
            for cell in self.boxcells(vv): ids.update(self.cells.get(cell,()))
            if any(overlap(q,self.squares[k]) for k in ids): continue
            k=len(self.squares); self.squares.append(q)
            for cell in self.boxcells(vv): self.cells[cell].append(k)
        self.W=L*w+z*L*L/2-len(self.squares)
        self.emitters={-1:((0.,0.),(1.,0.),(0.,1.),L)}
        for k,q in enumerate(self.squares):
            c,s=math.cos(q.a),math.sin(q.a)
            self.emitters[k]=(q.vertices()[3],(c,s),(-s,c),1.)

    @staticmethod
    def boxcells(vv):
        return [(i,j) for i in range(math.floor(min(p[0] for p in vv)),math.floor(max(p[0] for p in vv))+1)
                for j in range(math.floor(min(p[1] for p in vv)),math.floor(max(p[1] for p in vv))+1)]
    def inside(self,q):
        return all(-EPS<=x<=self.L+EPS and -EPS<=y<=self.w+self.z*x+EPS for x,y in q.vertices())
    def validate(self):
        pairs=set()
        for ids in self.cells.values():
            for j,k in enumerate(ids):
                for l in ids[j+1:]: pairs.add((min(k,l),max(k,l)))
        assert all(self.inside(q) for q in self.squares)
        assert all(not overlap(self.squares[k],self.squares[l]) for k,l in pairs)
        assert self.W>=-EPS
        return len(pairs)
    def near(self,poly):
        ids=set()
        for cell in self.boxcells(poly): ids.update(self.cells.get(cell,()))
        return ids
    def hit(self,e,n,previous,ids,delta):
        # Analytic line/edge ray casting; upward entry edges only, no occupancy grid.
        den=n[1]-self.z*n[0]
        r=(self.w+self.z*e[0]-e[1])/den
        best=(max(0.,r),-2,-1)
        if n[0]>1e-14:
            t=(self.L-e[0])/n[0]
            if t<best[0]: best=(max(0.,t),-3,1)
        if n[0]<-1e-14:
            t=-e[0]/n[0]
            if t<best[0]: best=(max(0.,t),-3,0)
        for k in ids:
            if k==previous: continue
            vv=self.squares[k].vertices()
            for side,(a,b) in enumerate(zip(vv,vv[1:]+vv[:1])):
                edge=sub(b,a); det=cross(n,edge)
                # CCW polygon: an entry has cross(edge,n)>0.
                if det>=-1e-13: continue
                t=cross(sub(a,e),edge)/det
                u=cross(sub(a,e),n)/det
                if t>=-EPS and -EPS<=u<=1+EPS:
                    cand=(max(0.,t),k,side)
                    if t<=best[0]+EPS and (t<best[0]-EPS or k>=0): best=cand
        return best

    def profiles(self,delta):
        profiles={}; nearby={}
        for k,(base,u,n,length) in self.emitters.items():
            if k>=0 and abs(self.squares[k].a)>=.08: continue
            rect=[base,add(base,mul(u,length)),add(add(base,mul(u,length)),mul(n,delta)),add(base,mul(n,delta))]
            ids=self.near(rect)-{k}; nearby[k]=ids
            cuts=[0.,length]
            for j in ids:
                vv=self.squares[j].vertices()
                for p in vv:
                    cuts.append(dot(sub(p,base),u))
                for a,b in zip(vv,vv[1:]+vv[:1]):
                    A=dot(sub(a,base),n); B=dot(sub(b,base),n)
                    if abs(B-A)>1e-14:
                        for h in (0.,delta):
                            t=(h-A)/(B-A)
                            if 0<=t<=1: cuts.append(dot(sub(add(a,mul(sub(b,a),t)),base),u))
            # Boundary lines intersect the near/far edge of the swept rectangle.
            for normal,c0 in (((1.,0.),0.),((1.,0.),self.L),((-self.z,1.),self.w)):
                den=dot(normal,u)
                if abs(den)>1e-14:
                    for h in (0.,delta): cuts.append((c0-dot(normal,base)-h*dot(normal,n))/den)
            cuts=unique(max(0.,min(length,s)) for s in cuts)
            pieces=[]
            for lo,hi in zip(cuts,cuts[1:]):
                if hi-lo<=EPS: continue
                mid=(lo+hi)/2; e=add(base,mul(u,mid))
                r,j,side=self.hit(e,n,k,ids,delta)
                if r>delta+EPS: rr=(0.,delta); j,side=-4,-1
                else:
                    if j>=0:
                        vv=self.squares[j].vertices(); a,b=vv[side],vv[(side+1)%4]
                        edge=sub(b,a); den=cross(n,edge)
                        rr=(-cross(u,edge)/den,cross(sub(a,base),edge)/den)
                    else:
                        normal,c0= ((-self.z,1.),self.w) if j==-2 else ((1.,0.),self.L if side else 0.)
                        den=dot(normal,n)
                        rr=(-dot(normal,u)/den,(c0-dot(normal,base))/den)
                a=add(base,mul(u,lo)); b=add(base,mul(u,hi))
                poly=[a,b,add(b,mul(n,max(0.,val(rr,hi)))),add(a,mul(n,max(0.,val(rr,lo))))]
                pieces.append((lo,hi,rr,j,side,poly))
            profiles[k]=pieces
        return profiles

def conflict_intervals(r,profiles,tau):
    active={k for k in profiles if k<0 or abs(r.squares[k].a)<tau}
    cells=defaultdict(set)
    for k in active:
        base,u,n,l=r.emitters[k]
        # index all component boxes (floor is long but shallow).
        for p in profiles[k]:
            for cell in r.boxcells(p[5]): cells[cell].add(k)
    pairs=set()
    for ids in cells.values():
        for k in ids:
            for j in ids:
                if k<j: pairs.add((k,j))
    bypair=defaultdict(list)
    for k,j in pairs:
        for a in profiles[k]:
            amin=[min(p[d] for p in a[5]) for d in (0,1)]
            amax=[max(p[d] for p in a[5]) for d in (0,1)]
            for b in profiles[j]:
                if any(max(p[d] for p in b[5])<amin[d]-EPS or min(p[d] for p in b[5])>amax[d]+EPS for d in (0,1)): continue
                pts=intersection_points(a[5],b[5])
                if not pts: continue
                for first,other in ((k,j),(j,k)):
                    base,u,_,_=r.emitters[first]
                    ss=[dot(sub(p,base),u) for p in pts]
                    if max(ss)-min(ss)>EPS: bypair[first,other].append((min(ss),max(ss)))
    bypair={p:union(v) for p,v in bypair.items()}
    merged=defaultdict(list)
    for (k,j),v in bypair.items(): merged[k].extend(v)
    return bypair,{k:union(v) for k,v in merged.items()}

def split(lo,hi,aff,cuts):
    if abs(aff[0])<1e-14: return [(lo,hi)]
    xx=unique([lo,hi]+[(c-aff[1])/aff[0] for c in cuts if lo+EPS<(c-aff[1])/aff[0]<hi-EPS])
    return list(zip(xx,xx[1:]))

@dataclass
class PathRun:
    lo: float
    hi: float
    kind: str
    chain: tuple
    entries: tuple
    segments: tuple
    G: tuple
    V: tuple
    end: tuple
    hit: int

    @property
    def N(self): return len(self.chain)
    def D(self,r): return sum(1-math.cos(r.squares[k].a) for k in self.chain)

def flow(r,profiles,conf,delta,tau):
    # State consists entirely of affine functions of the original floor x.
    todo=[(0.,r.L,-1,(1.,0.),const(0.),const(0.),(),(),())]; out=[]
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
                out.append(PathRun(a,b,'conflict',chain,entries,segs,G,V,e,em)); continue
            rr=plus(scale(s,p[2][0]),const(p[2][1])); total=plus(G,rr)
            for aa,bb in split(a,b,total,[delta]):
                m=(aa+bb)/2; j,side=p[3:5]
                if val(total,m)>delta+EPS or j==-4:
                    travel=plus(const(delta),scale(G,-1)); kind='gap'
                else: travel=rr; kind=None
                q=moving(e,n,travel); sg=segs+((e,q,'gap',em),)
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
                    out.append(PathRun(aa,bb,kind,chain,entries,sg,newG,newV,q,j)); continue
                qb,qu,qn,_=r.emitters[j]
                # Bottom left = top left - normal; s is the dot product there.
                bottom=sub(qb,qn)
                sj=plus(scale(plus(q[0],const(-bottom[0])),qu[0]),scale(plus(q[1],const(-bottom[1])),qu[1]))
                top=moving(q,qn,const(1.))
                todo.append((aa,bb,j,sj,newG,newV,chain+(j,),entries+((j,sj,q[1]),),sg+((q,top,'square',j),)))
    return sorted(out,key=lambda p:p.lo)

def x_at(p,x,y):
    # Monotone piecewise linear polyline evaluated at an actual height.
    for a,b,_,_ in p.segments:
        A=point(a,x); B=point(b,x)
        if A[1]-EPS<=y<=B[1]+EPS:
            if B[1]-A[1]<EPS: return A[0]
            return A[0]+(B[0]-A[0])*(y-A[1])/(B[1]-A[1])
    return point(p.end,x)[0]

def ordered(p,x,q,X):
    ymax=min(point(p.end,x)[1],point(q.end,X)[1])
    ys={0.,ymax}
    for path,t in ((p,x),(q,X)):
        for a,b,_,_ in path.segments:
            ys.update(point(v,t)[1] for v in (a,b) if 0<=point(v,t)[1]<=ymax)
    return min((x_at(q,X,y)-x_at(p,x,y) for y in ys),default=X-x)
def staircase(L,w,z):
    return [Square(i+.5,j+.5) for i in range(int(L)) for j in range(math.floor(w+z*i+1e-12))]

def lattice_candidates(L,w,z,a,l,eps):
    # Copied lattice basis/inverse from slab_flow_check.py, clipped by Region.
    c,s=math.cos(a),math.sin(a); ii=[]; jj=[]
    for x,y in ((0,0),(L,0),(0,w),(L,w+z*L)):
        U=x*c+y*s; V=-x*s+y*c
        ii.append((U-eps*V)/(1+l*eps)); jj.append((l*U+V)/(1+l*eps))
    return [Square((i+j*eps)*c-(j-i*l)*s,(i+j*eps)*s+(j-i*l)*c,a)
            for i in range(math.floor(min(ii))-2,math.ceil(max(ii))+3)
            for j in range(math.floor(min(jj))-2,math.ceil(max(jj))+3)]

def layers(L,w,z,alpha,fan=False):
    # Axis lower layers plus independently tuned normal columns. Search integers
    # j,k to minimize ceiling slack, with k near 1/z and j about w-k.
    c,s=math.cos(alpha),math.sin(alpha); kmax=min(int(w*.8),int(1/z)+10)
    columns=[]; heights={}
    for col in range(int(L*c)):
        a=alpha if not fan or col<L*c/2 else alpha*.83
        c,s=math.cos(a),math.sin(a)
        base=col/c+kmax*math.sin(alpha)+.02
        best=None
        for k in range(max(1,kmax//2),kmax+1):
            # Highest ceiling deficit at a vertex, with j=0.
            trial=[Square(base+.5*c-(t+.5)*s,.5*s+(t+.5)*c,a) for t in range(k)]
            cap=min(w+z*x-y for q in trial[-1:] for x,y in q.vertices())
            j=max(0,math.floor(cap+1e-12))
            slack=cap-j
            if best is None or slack<best[0]: best=(slack,j,trial)
        _,j,trial=best
        columns.extend(Square(q.x,q.y+j,q.a) for q in trial)
        # Under each vertical unit cell use the minimum supporting column height.
        for q in trial:
            for i in range(max(0,math.floor(q.x-.8)),min(int(L),math.ceil(q.x+.8))):
                heights[i]=min(heights.get(i,j),j)
    grid=[Square(i+.5,h+.5) for i in range(int(L)) for h in range(heights.get(i,0))]
    return grid+columns

def perturbed(base,seed):
    rng=random.Random(seed)
    candidates=[]
    for q in base:
        if rng.random()<.035: continue
        if rng.random()<.025:
            q=Square(q.x+rng.uniform(-.025,.025),q.y+rng.uniform(-.025,.025),q.a+rng.uniform(-.018,.018))
        candidates.append(q)
    return candidates

def packings():
    for w in (3,12,40): yield Region('a-stair-w%d'%w,60,w,.05,staircase(60,w,.05))
    for w in (3,30):
        a=math.atan(.05); c,s=math.cos(a),math.sin(a)
        candidates=[Square((i+.5)*c-(w*c-.5-j)*s,(i+.5)*s+(w*c-.5-j)*c,a)
                    for i in range(65) for j in range(math.ceil(w+4))]
        yield Region('b-ceiling-w%d'%w,60,w,.05,candidates)
    for l,eps in ((.2,.006),(.35,.0105),(.15,.0027)):
        yield Region('c-lattice-%g-%g'%(l,eps),60,30,.05,lattice_candidates(60,30,.05,.03,l,eps))
    for z,L,w in ((.01,150,100),(.02,100,75),(.05,60,40)):
        for a in (math.sqrt(2*z),.07):
            yield Region('d-layers-z%g-a%.4f'%(z,a),L,w,z,layers(L,w,z,a))
    yield Region('e-fan',80,45,.02,layers(80,45,.02,.065,True))
    for seed in (17,29,83):
        yield Region('f-stair-seed%d'%seed,60,12,.05,perturbed(staircase(60,12,.05),seed))
        yield Region('f-layers-seed%d'%seed,80,50,.02,perturbed(layers(80,50,.02,.065),seed))
    # Closest disjoint oblique top sides: full probe strips overlap in a wedge.
    for a in (.019,.049,.079):
        c,s=math.cos(a),math.sin(a)
        for sign in (1,-1):
            yield Region('g-crossing-%+.3f'%(sign*a),4,1.03,.25,
                         [Square(1,.5*(c+s),sign*a),Square(1+c+s,.5*(c+s),-sign*a)])
    yield Region('g-wall',4,1.05,.25,[Square(.5,.5),Square(3.5,.5),Square(2,1.02,.03)])
    # Opposite tilts, missing level, and shared-side zero probes.
    yield Region('g-index-pairing',12,3.01,.1,
                 staircase(12,1,0)+[Square(2+i*1.08,1.54+j*1.03,(-1)**i*.045) for i in range(8) for j in range(3)])
    yield Region('g-empty',4,0.,.25,[])
    # Nonvacuous paid-drop stress: same N, tiny orientation difference across
    # tall near-parallel columns, with a ceiling shallow enough to face them.
    # This is deliberately sparse; it tests index pairing, not small waste.
    n=600; z=.0001; candidates=[]
    for col,a in enumerate((.019,.0189)):
        c,s=math.cos(a),math.sin(a); base=n*math.sin(.019)+.1+col*1.1
        candidates.extend(Square(base+.5*c-(j+.5)*s,.5*s+(j+.5)*c,a) for j in range(n))
    w=max(y-z*x for q in candidates for x,y in q.vertices())+.0001
    yield Region('g-paid-index-columns',10000,w,z,candidates)

class Checks:
    def __init__(self): self.items=defaultdict(list); self.witnesses=[]
    def le(self,k,label,lhs,rhs,tol=TOL,witness=None):
        ok=lhs<=rhs+tol
        self.items[k].append((ok,label,lhs,rhs))
        if not ok: self.witnesses.append((k,label,lhs,rhs,witness))
    def cell(self,k):
        v=self.items[k]
        if not v: return 'PASS (no eligible objects)'
        # The tightest normalized comparison; identities are residual <= tolerance.
        worst=max(v,key=lambda a:(a[2]-a[3])/max(1,abs(a[3])))
        return '%s %s: %s ≤ %s'%('PASS' if all(a[0] for a in v) else 'FAIL',worst[1],fmt(worst[2]),fmt(worst[3]))

def fmt(x):
    if math.isinf(x): return 'inf'
    return '%.9g'%x

def check(r,profiles,bypair,conf,delta,tau):
    paths=flow(r,profiles,conf,delta,tau); checks=Checks()
    arr=[p for p in paths if p.kind=='arrival']; counts=Counter()
    density=Counter(); height_err=slope_err=entry_err=0.; min_order=math.inf
    samplepaths=[]
    for p in paths:
        counts[p.kind]+=p.hi-p.lo
        for k in p.chain: density[k]+=p.hi-p.lo
        # Three interior samples in every exact itinerary interval.
        for f in (.2113248654,.5,.7886751346):
            x=p.lo+f*(p.hi-p.lo); samplepaths.append((x,p))
            if p.kind=='arrival': height_err=max(height_err,abs(r.w+r.z*point(p.end,x)[0]-(p.N-p.D(r)+val(p.V,x))))
            h=0.; lasta=0.; kap=1.
            ei=0
            for a,b,kind,k in p.segments:
                if kind=='gap': h+=point(b,x)[1]-point(a,x)[1]
                else:
                    phi=r.squares[k].a; kap/=math.cos(phi-lasta)
                    _,ss,hh=p.entries[ei]; ei+=1
                    entry_err=max(entry_err,abs(val(hh,x)-h))
                    slope_err=max(slope_err,abs(ss[0]-kap))
                    h+=math.cos(phi); lasta=phi
        if p.kind=='arrival':
            kap=1.; a=0.
            for k in p.chain:
                b=r.squares[k].a; kap/=math.cos(b-a); a=b
            kp=kap*math.cos(math.atan(r.z))/math.cos(a-math.atan(r.z)) if p.N else 1.
            slope_err=max(slope_err,abs(p.end[0][0]-kp),abs(p.V[0]-r.z*kp))
            checks.le(2,'1≤κ',1.,kap)
            checks.le(2,'cosζ′≤κ′',math.cos(math.atan(r.z)),kp)
        if p.kind=='tilt':
            angles=[0.]+[r.squares[k].a for k in p.chain]+[r.squares[p.hit].a]
            variation=sum(theta(a,b) for a,b in zip(angles,angles[1:]))
            checks.le(5,'τ≤Σθ',tau,variation,witness=(p.lo,p.hi,p.chain+(p.hit,)))
    checks.le(1,'height residual',height_err,TOL,0)
    checks.le(1,'entry residual',entry_err,TOL,0)
    checks.le(2,'affine slope residual',slope_err,TOL,0)
    for (x,p),(X,q) in zip(samplepaths,samplepaths[1:]):
        margin=ordered(p,x,q,X); min_order=min(min_order,margin)
        checks.le(3,'polyline crossing',-margin,0.,witness=(x,X,p.chain,q.chain))
    for p,q in zip(arr,arr[1:]):
        checks.le(3,'arrival ordering',val(p.end[0],p.hi)-val(q.end[0],q.lo),0.)
    checks.le(4,'square density',max(density.values(),default=0.),1.)
    checks.le(5,'gap',counts['gap'],r.W/delta)
    checks.le(5,'tilt',counts['tilt'],1350*r.W/tau)
    # Independently sample each top side on a fine uniform grid. Count grid points
    # analytically in each interval, equivalent to visiting all 8192 midpoints.
    emitter_grid=8192; max_grid_error=0.; conflict_peak=(0.,None)
    lateral=defaultdict(list); walls=defaultdict(list)
    for em,pp in profiles.items():
        if em>=0 and abs(r.squares[em].a)>=tau: continue
        for lo,hi,rr,k,side,poly in pp:
            if k>=0 and abs(r.squares[k].a)<tau and side in (1,3): lateral[em,k].append((lo,hi))
            if k==-3: walls[em,side].append((lo,hi))
    for (em,k),v in lateral.items():
        angle=theta(0. if em<0 else r.squares[em].a,r.squares[k].a)
        checks.le(6,'lateral pair',measure(v),2*delta*math.tan(angle),witness=(em,k,v))
    for (em,side),v in walls.items():
        a=0. if em<0 else abs(r.squares[em].a)
        checks.le(6,'wall',measure(v),delta*math.tan(a),witness=(em,side,v))
    for (em,k),v in bypair.items():
        angle=theta(0. if em<0 else r.squares[em].a,0. if k<0 else r.squares[k].a)
        mm=measure(v); bound=0. if min(em,k)<0 else 4.3*delta*angle
        checks.le(7,'floor conflict' if min(em,k)<0 else 'conflict pair',mm,bound,witness=(em,k,v))
        length=r.emitters[em][3]
        n=sum(max(0,math.ceil(b/length*emitter_grid-.5)-math.ceil(a/length*emitter_grid-.5)) for a,b in v)
        max_grid_error=max(max_grid_error,abs(n*length/emitter_grid-mm))
        if bound>0 and mm/bound>conflict_peak[0]: conflict_peak=(mm/bound,(em,k,mm,bound))
    # Include zero pairs explicitly, rather than silently leaving an empty check.
    checks.le(6,'zero pairs',0.,0.); checks.le(7,'floor conflict',measure(conf.get(-1,())),0.)
    non=r.L-counts['arrival']-counts['exceptional']
    cor_rhs=(4250*r.W+1350*r.W/tau+.01) if delta==1/32 else (r.W/delta+1350*r.W/tau+134000*delta*r.W+.01)
    checks.le(8,'nonarrival',non,cor_rhs)
    boundaries=[]; positive=0.; tube_sum=0.; aligned_min=math.inf; paid_ratio=0.; geometry_res=0.; dich_slack=math.inf
    for k,(p,q) in enumerate(zip(arr,arr[1:]),1):
        x,X=p.hi,q.lo
        V,Vp=val(p.V,x),val(q.V,X); drop=V-Vp
        Delta=val(q.end[0],X)-val(p.end[0],x)
        D,Dp=p.D(r),q.D(r); P,Pp=D-p.N,Dp-q.N
        checks.le(9,'6.1 residual',abs(drop-((P-Pp)-r.z*Delta)),TOL,0)
        checks.le(9,'Δ≥0',-Delta,0.); checks.le(9,'drop≤δ',drop,delta)
        positive+=max(0.,drop)
        # Tube points are strictly interior and ordered even for a one-run J.
        # Boundary limits are used for §6; actual tube Y uses these interior points.
        xp=p.hi-min((p.hi-p.lo)/4,1e-8)
        xq=q.lo+min((q.hi-q.lo)/4,1e-8)
        levels=[]; cumulative=0.; Theta=0.
        for i,(left,right) in enumerate(zip(p.entries,q.entries),1):
            a,_,hh=left; b,_,h2=right
            angle=theta(r.squares[a].a,r.squares[b].a)
            aligned=tau*cumulative<.25; cumulative+=angle
            if aligned: Theta+=angle
            h=val(hh,xp); H=h+math.cos(r.squares[a].a)
            v=val(h2,xq); Vh=v+math.cos(r.squares[b].a)
            low,high=max(h,v),min(H,Vh); Y=max(0.,high-low)
            tube_sum+=angle*Y
            if drop>EPS and aligned:
                aligned_min=min(aligned_min,Y); checks.le(11,'aligned overlap',.7,Y,witness=(k,i,a,b))
            # Sample horizontal tubes at three heights, including angle-zero levels.
            if Y>EPS:
                for f in (.2113248654,.5,.7886751346):
                    y=low+f*Y; xx=x_at(p,xp,y); XX=x_at(q,xq,y)
                    # Independent local-frame membership of endpoints.
                    for sid,pos in ((a,xx),(b,XX)):
                        sq=r.squares[sid]; c,s=math.cos(sq.a),math.sin(sq.a)
                        U=(pos-sq.x)*c+(y-sq.y)*s; Vc=-(pos-sq.x)*s+(y-sq.y)*c
                        geometry_res=max(geometry_res,max(abs(U),abs(Vc))-.5)
                    # Enumerate all squares actually met by the horizontal segment.
                    hits=[]; ids=r.near([(xx,y),(XX,y)])
                    for sid in ids:
                        vv=r.squares[sid].vertices(); hitsx=[]
                        for A,B in zip(vv,vv[1:]+vv[:1]):
                            if abs(B[1]-A[1])>1e-14 and min(A[1],B[1])-EPS<=y<=max(A[1],B[1])+EPS:
                                hitsx.append(A[0]+(B[0]-A[0])*(y-A[1])/(B[1]-A[1]))
                        if hitsx and min(max(hitsx),XX)-max(min(hitsx),xx)>EPS:
                            hits.append((min(hitsx),sid))
                    hits.sort(); ids=[sid for _,sid in hits]
                    if a==b: variation=0.
                    else:
                        variation=sum(theta(r.squares[u].a,r.squares[v].a) for u,v in zip(ids,ids[1:]))
                        checks.le(12,'segment endpoints',0. if ids and ids[0]==a and ids[-1]==b else 1.,0.,witness=(k,i,y,a,b,ids))
                    checks.le(12,'triangle θ',angle,variation,witness=(k,i,y,a,b,ids))
            levels.append((i,a,b,angle,aligned,Y))
        if drop>EPS:
            paid=tau*Theta; skip=q.N>p.N and Delta>=1/(2*r.z)-TOL
            checks.le(11,'drop paid or skip',drop,math.inf if skip else paid,witness=(k,p.chain,q.chain))
            if paid>EPS: paid_ratio=max(paid_ratio,drop/paid)
            dich_slack=min(dich_slack,max(paid-drop,Delta-1/(2*r.z) if q.N>p.N else -math.inf))
        boundaries.append((k,p.N,q.N,D,Dp,P,Pp,val(p.V,p.lo),V,Vp,val(q.V,q.hi),drop,Delta,Theta,levels))
    checks.le(9,'empty-boundary residual',0.,TOL,0)
    checks.le(10,'positive drops',math.sin(math.atan(r.z))*counts['arrival']-delta,positive)
    checks.le(11,'empty-boundary residual',0.,0.)
    checks.le(12,'tube endpoints residual',max(0.,geometry_res),TOL,0)
    checks.le(12,'sideways',tube_sum,14851*r.W)
    hypothesis=4250*r.W+1350*r.W/tau+.01<=r.L/4
    if delta==1/32 and hypothesis: checks.le(13,'Prop7.1',.47*r.z*r.L,21300*tau*r.W)
    checks.le(13,'Theorem B',7e-6*math.sqrt(r.L*r.z*r.L),r.W)
    return dict(checks=checks,paths=paths,arr=arr,counts=counts,boundaries=boundaries,tube=tube_sum,
                paid_ratio=paid_ratio,aligned_min=aligned_min,positive=positive,conflict_peak=conflict_peak,
                grid_error=max_grid_error,hypothesis=hypothesis,min_order=min_order)
def verify_rays(r,profiles,delta):
    # Unindexed local-axis slab clipping is independent of edge intersections.
    emit=list(profiles)
    for i in range(24):
        em=emit[(i*7919)%len(emit)]; base,u,n,length=r.emitters[em]
        s=((i*.6180339887498949+.38196601125)%1)*length
        e=add(base,mul(u,s)); best=delta
        den=n[1]-r.z*n[0]
        best=min(best,max(0.,(r.w+r.z*e[0]-e[1])/den))
        if abs(n[0])>1e-14: best=min(best,max(0.,((r.L if n[0]>0 else 0.)-e[0])/n[0]))
        for k,q in enumerate(r.squares):
            if k==em: continue
            c,ss=math.cos(q.a),math.sin(q.a)
            low,high=-math.inf,math.inf
            for axis in ((c,ss),(-ss,c)):
                b=dot(sub(e,(q.x,q.y)),axis); d=dot(n,axis)
                if abs(d)<1e-14:
                    if abs(b)>.5+EPS: low,high=1.,0.; break
                else:
                    A=(-.5-b)/d; B=(.5-b)/d
                    low=max(low,min(A,B)); high=min(high,max(A,B))
            if low<=high+EPS and low>=-EPS and high>=-EPS: best=min(best,max(0.,low))
        p=next(p for p in profiles[em] if p[0]-EPS<=s<=p[1]+EPS)
        assert abs(val(p[2],s)-best)<2e-8,(r.name,em,s,val(p[2],s),best)

def summary_cell(c,k):
    labels={}
    for a in c.items[k]:
        old=labels.get(a[1])
        if old is None or a[2]-a[3]>old[2]-old[3]: labels[a[1]]=a
    if not labels: return 'PASS (no eligible objects: 0 ≤ 0)'
    return '<br>'.join('%s %s: %s ≤ %s'%('PASS' if a[0] else 'FAIL',a[1],fmt(a[2]),fmt(a[3])) for a in labels.values())

def witness_squares(r,w):
    # Read ids from the semantic witness rather than interpreting every integer
    # (boundary/level numbers are not square ids).
    k,label,lhs,rhs,v=w
    if v is None: return []
    if k in (6,7): ids=v[:2] if label!='wall' else v[:1]
    elif k==3: ids=v[2]+v[3]
    elif k==5: ids=v[2]
    elif k==11 and label=='drop paid or skip': ids=v[1]+v[2]
    elif k==11: ids=v[2:4]
    elif k==12: ids=v[3:5]+tuple(v[5])
    else: ids=()
    return sorted(set(i for i in ids if isinstance(i,int) and 0<=i<len(r.squares)))

def shrink_pair(r,delta,tau,w):
    """Deletion-minimize pair failures, recomputing actual truncated probes.

    Removing obstacles only enlarges probes. For a witnessed pair retain just
    its two squares, then try each singleton. Other failures retain witnessed
    chains and are explicitly labelled unreduced if not revalidated.
    """
    ids=witness_squares(r,w)
    if w[0] not in (6,7): return ids,False
    def fails(keep):
        rr=Region('reduction',r.L,r.w,r.z,[r.squares[i] for i in keep])
        pp=rr.profiles(delta); bp,cf=conflict_intervals(rr,pp,tau)
        if w[0]==7:
            return any(measure(v)>(0. if min(a,b)<0 else 4.3*delta*theta(rr.squares[a].a,rr.squares[b].a))+TOL for (a,b),v in bp.items())
        vv=defaultdict(list)
        for em,pieces in pp.items():
            if em>=0 and abs(rr.squares[em].a)>=tau: continue
            for lo,hi,_,hit,side,_ in pieces:
                if hit>=0 and abs(rr.squares[hit].a)<tau and side in (1,3): vv[em,hit].append((lo,hi))
                elif hit==-3: vv[em,-10-side].append((lo,hi))
        for (em,hit),v in vv.items():
            a=0. if em<0 else rr.squares[em].a
            bound=delta*math.tan(abs(a)) if hit<0 else 2*delta*math.tan(theta(a,rr.squares[hit].a))
            if measure(v)>bound+TOL: return True
        return False
    if not fails(ids): return ids,False
    for sid in list(ids):
        trial=[i for i in ids if i!=sid]
        if fails(trial): ids=trial
    return ids,True

def main():
    start=time.monotonic(); results=[]; metadata=[]; detail=[]; failures=[]
    print('Building and validating packings; all computations offline.',flush=True)
    for r in packings():
        pairs=r.validate(); metadata.append((r.name,r.L,r.w,r.z,len(r.squares),r.W,pairs))
        for delta in (1/32,1/8):
            pp=r.profiles(delta); verify_rays(r,pp,delta)
            for tau in (.02,.05,.08):
                bp,conf=conflict_intervals(r,pp,tau)
                v=check(r,pp,bp,conf,delta,tau)
                results.append((r.name,delta,tau,r.W,v))
                # Full interval and boundary inventory, serialized immediately so
                # large geometric objects need not stay alive across packings.
                tag='%s δ=%g τ=%g'%(r.name,delta,tau)
                detail+=['','### '+tag,'',
                         'Arriving J_k=(a,b), in order (endpoints excluded):',
                         '`'+repr([(p.lo,p.hi) for p in v['arr']])+'`','',
                         'Boundary tuples: (k,N,N′,D,D′,P,P′,G̃(a_k+),G̃(b_k−),G̃(a_(k+1)+),G̃(b_(k+1)−),drop,Δ,Θ). '
                         'Each following level list is (i,Z_i,Z_i′,θ_i,aligned,|Y_i|). Square ids are zero based.']
                for boundary in v['boundaries']:
                    detail.append('`'+repr(boundary[:-1])+'` levels `'+repr(boundary[-1])+'`')
                if not v['boundaries']: detail.append('No consecutive arriving intervals.')
                detail.append('Largest nonzero conflict-pair ratio and witness (emitter ids, measured length, bound): `'+repr(v['conflict_peak'])+'`.')
                detail+=['','Tube sum = %s; 14851W = %s; ratio = %s. Maximum positive drop/(τΘ) = %s; '
                         'minimum aligned overlap = %s. Arrival measure = %s; positive drops = %s. '
                         'Independent 8192-point emitter-grid maximum measure discrepancy = %s.'%(
                             fmt(v['tube']),fmt(14851*r.W),fmt(v['tube']/(14851*r.W)) if r.W else 'NA',
                             fmt(v['paid_ratio']),fmt(v['aligned_min']),fmt(v['counts']['arrival']),fmt(v['positive']),fmt(v['grid_error']))]
                for w in v['checks'].witnesses:
                    ids,reduced=shrink_pair(r,delta,tau,w)
                    failures.append((tag,w,[(i,r.squares[i]) for i in ids],reduced,(r.L,r.w,r.z)))
                # Retain only compact statistics for final tables.
                for key in ('paths','arr','boundaries'): del v[key]
                print('%s: arrivals=%.6g checks=%s t=%.1fs'%(tag,v['counts']['arrival'],
                      ','.join(str(k) for k in range(1,14) if any(not a[0] for a in v['checks'].items[k])) or 'PASS',time.monotonic()-start),flush=True)
    out=['# Wedge flow numerical audit — 2026-11-09','',
         '## Method','',
         'Offline Python 3 standard library. Read the entire draft before implementation. Square vertices, four-axis '
         'separating-axis packing validation, analytic edge casting, spatial cells and lattice/column constructions '
         'are copied/adapted from tools/slab_flow_check.py; the original is untouched. Each candidate is accepted '
         'only if contained and SAT-disjoint from all previous candidates. A second independently enumerated '
         'pair validation checks the finished packing. Each packing/delta also checks 24 emitter rays against '
         'unindexed square-axis slab clipping. All packings satisfy 0<ζ≤1 and ζL≥1.','',
         'For every potential emitter, split its top-side coordinate at projected obstacle vertices and at '
         'intersections of obstacle/boundary edges with the near and far edges of its δ-strip. On each piece '
         'the first-hit distance is affine, capped at δ, so the actual swept probe region is a convex quadrilateral '
         '(possibly a line). Intersect nearby regions, including their boundaries; project intersection vertices '
         'onto each emitter tangent and union the resulting intervals. This computes conflicts using **all '
         'potential probes**, not travelled probes. Degenerate line regions use segment membership/intersection. '
         'Only flat squares emit. Conflicts are recomputed for every τ. Independent top-side sampling uses '
         '8192 uniform midpoints on every emitter (counted analytically from interval endpoints), independent of floor paths.','',
         'Instead of estimating measures solely on a floor grid, propagate affine intervals through the exact '
         'profile breaks, conflict endpoints and the cumulative-gap cutoff. All path coordinates, square-entry '
         'coordinates/heights, raw gap G and vertically weighted gap G̃ are affine on each resulting open interval. '
         'Compute measures by interval length; sample three interior points in **every** resulting itinerary cell. '
         'Check neighboring sampled polylines directly at every vertex height of both paths; their difference is '
         'linear between those heights. Also check ordered arrival limits. Heights and slopes are checked on all cells. '
         'This avoids missing short arriving intervals in an ordinary fixed floor grid. Numeric tolerances: '
         'SAT/partition 2e-10, reported inequality/residual 2e-7; strict positive-drop tests use 2e-10.','',
         'Tubes use points within min(quarter cell width,1e-8) of facing arrival endpoints, so adjacent tubes have '
         'disjoint interiors. Boundaries use one-sided affine limits. Pair i-th squares by index, intersect their '
         'actual crossing-height intervals, and sample each nonempty Y_i at three heights. At each height, independently '
         'enumerate all squares met by the horizontal segment and check endpoint membership and the orientation '
         'triangle inequality. Integrate θ_i|Y_i| exactly for the chosen tube endpoints. No universal proof is inferred '
         'from these finite tests.','',
         '## Ambiguities','',
         '- The note calls J_k “intervals of arriving x” but N,D need not be constant on a connected arrival set '
         'if its itinerary changes. Use the finite itinerary partition from Lemma 3.1(a), retaining harmless extra '
         'affine-profile cuts; all J_k and all boundaries are listed below.',
         '- r*=0: exclude the emitting square and intersect entry-facing edges of other squares. A square event '
         'wins a ceiling/wall tie; vertex priority precedes steepness. Closed endpoint contacts are included in '
         'conflict geometry; isolated conflicted parameter points have zero measure and are excluded from the open cells.',
         '- Gap equality continues; strict excess dies. A gap is along the last square normal, vertical only at the floor. '
         'A conflict death stops at the emitter before travelling any part of its new probe.',
         '- The draft fixes δ=1/32. For δ=1/8, report (4.5) using its unspecialized bound W/δ+1350W/τ+134000δW+0.01; '
         'also stress-test the 0.7 aligned-overlap and 6.3 dichotomy at this larger δ, without claiming the draft proves them there. '
         'Proposition 7.1 is evaluated only at δ=1/32; its hypothesis is recorded explicitly.',
         '- θ is orientation distance modulo π/2, angles in radians, and flat means strict |φ|<τ. '
         '“Surviving paths” includes all prefixes before death; the polyline tests include those prefixes.',
         '- Lateral measure counts both lateral sides for each ordered emitter/square pair. Wall measures are per wall. '
         'Noninteracting ordered pairs have measure zero and automatically satisfy the bounds.',
         '- Layers: tune integer upper-column counts k and axis layer heights j to minimize ceiling slack, with k '
         'between half and all of min(0.8w,1/ζ+10); retain all valid candidates greedily. The requested α=√(2ζ) '
         'exceeds every tested τ for ζ≥0.01, so those upper columns are steep. Also use α=0.07 to obtain genuinely '
         'flat upper columns and test the intended drop mechanism. Fan uses α and 0.83α.',
         '- Exceptional/isolated parameter points have zero length; the interval audit does not enumerate every '
         'isolated vertex/conflict point. A vertex condition holding throughout a cell is reported exceptional. '
         'There is no positive-measure replacement for exceptional points.',
         '- No finite set of explicit packings can test a universal statement on all packings. In particular '
         'passing large-constant waste inequalities or an implication with false hypothesis is weak evidence.','',
         '## Packings and validation','',
         '| Packing | L | w | ζ | squares | W | independently checked SAT pairs |',
         '|---|---:|---:|---:|---:|---:|---:|']
    for m in metadata: out.append('| '+' | '.join(str(x) if isinstance(x,(str,int)) else fmt(x) for x in m)+' |')
    out+=['','## All 13 checks, per packing and parameter choice','',
          'Each cell gives PASS/FAIL and both numerical sides. Repeated objects are summarized by the largest residual '
          'for each named comparison, so every subcheck appears. 1=3.1(c); 2=3.1(b,d); 3=3.2; 4=3.3; '
          '5=4.1/4.2; 6=4.3; 7=4.4; 8=4.5; 9=6.1 identity/order/cap; 10=Lemma 6.1; '
          '11=6.2/6.3; 12=5.1 and its segment claim; 13=7.1 and Theorem B. '
          'In column 10 the lower bound is written as RHS of the lemma ≤ measured positive drops. '
          'For 11 the skip branch is shown as an infinite permissible RHS; actual N,N′,Δ and paid RHS are in the boundary inventory.','',
          '| Packing | δ | τ | '+ ' | '.join(str(k) for k in range(1,14))+' | Prop7.1 hypothesis |',
          '|---|---:|---:|'+ '|'.join(['---']*14)+'|']
    for name,d,t,W,v in results:
        out.append('| %s | %s | %s | %s | %s |'%(name,fmt(d),fmt(t),' | '.join(summary_cell(v['checks'],k) for k in range(1,14)),
                   'true' if d==1/32 and v['hypothesis'] else 'false' if d==1/32 else 'outside δ=1/32'))
    out+=['','## Tightest cases','',
          'For each named comparison below: minimum signed slack RHS−LHS over all packing/parameter rows '
          '(identities use the stated residual tolerance). Zero-object equalities can be tight without being informative.','',
          '| Check | comparison | slack | packing | δ | τ | LHS | RHS |','|---:|---|---:|---|---:|---:|---:|---:|']
    for k in range(1,14):
        labels=sorted({a[1] for _,_,_,_,v in results for a in v['checks'].items[k]})
        for label in labels:
            choices=[(a[3]-a[2],name,d,t,a[2],a[3]) for name,d,t,_,v in results for a in v['checks'].items[k] if a[1]==label]
            slack,name,d,t,lhs,rhs=min(choices)
            out.append('| %d | %s | %s | %s | %s | %s | %s | %s |'%(k,label,fmt(slack),name,fmt(d),fmt(t),fmt(lhs),fmt(rhs)))
    out+=['','## Layers: tightness of Lemmas 6.3 and 5.1','',
          '| Packing | δ | τ | arriving length | positive drops | max drop/(τΘ) | min aligned Y | ΣθY | 14851W | ΣθY/(14851W) |',
          '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for name,d,t,W,v in results:
        if name.startswith(('d-','e-','f-layers','g-paid')):
            out.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |'%(name,fmt(d),fmt(t),fmt(v['counts']['arrival']),fmt(v['positive']),fmt(v['paid_ratio']),fmt(v['aligned_min']),fmt(v['tube']),fmt(14851*W),fmt(v['tube']/(14851*W)) if W else 'NA'))
    out+=['','## Failures and anomalies','']
    if not failures: out.append('- No failed sampled/interval checks. This is numerical evidence, not a proof.')
    # Deduplicate repeated witnesses, but count all failing parameter rows below.
    seen=set()
    for tag,w,ss,reduced,region in failures:
        key=(w[0],w[1],repr(ss),region)
        if key in seen: continue
        seen.add(key)
        out+=['- FAIL '+tag+': check %d %s: %s > %s; witness `%r`.'%(w[0],w[1],fmt(w[2]),fmt(w[3]),w[4]),
              '  Region (L,w,ζ) = `%r`; %s square list (cx,cy,φ), followed by vertices:'%(region,'deletion-minimal revalidated' if reduced else 'involved (not certified minimal)'),
              '  `'+repr([(i,(q.x,q.y,q.a),q.vertices()) for i,q in ss])+'`']
    nh=sum(v['hypothesis'] for _,d,_,_,v in results if d==1/32)
    out+=['- Proposition 7.1 hypothesis held in %d rows; all other instances are vacuous implications, not substantive confirmation.'%nh,
          '- α=√(2ζ) layers do not provide the predicted mostly-arriving flat-flow regime because α>τ. '
          'The alternate shallow layers quantify actual arrival and drop coverage in the table above.',
          '- Additional adversarial tests: opposite-tilt close side-by-side squares (crossing potential probes), '
          'wall-hugging contacts, alternating signs with a missing/index-shifted layer, an empty wedge, holes, '
          'and three reproducible removal/nudge/rotation seeds. No assumptions of vertical gaps or travelled-only conflicts.',
          '- Interval decomposition is numerical rather than symbolic exact arithmetic. Very small cells below 2e-10 '
          'are merged; all conclusions remain bounded numerical tests.','',
          '%d packings; %d parameter rows; %d failing rows; runtime %.2f seconds.'%(
              len(metadata),len(results),sum(bool(v['checks'].witnesses) for _,_,_,_,v in results),time.monotonic()-start),
          '', '## Arrival intervals and all boundary/level objects']
    out+=detail
    REPORT.write_text('\n'.join(out)+'\n')
    print('Wrote',REPORT,'runtime',round(time.monotonic()-start,2),'seconds; failures',len(failures),flush=True)
    return 1 if failures else 0

if __name__=='__main__':
    raise SystemExit(main())
