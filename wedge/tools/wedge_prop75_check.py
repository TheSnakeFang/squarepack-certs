#!/usr/bin/env python3
"""Full-floor floating point test of Proposition 7.5; no proof certificate.
Run: python3 -I tools/wedge_prop75_check.py. Only writes its Markdown report.
"""
import sys
sys.dont_write_bytecode = True
import importlib.util
import math
import random
import time
import gc
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('staircase',ROOT/'tools/wedge_staircase_check.py')
s=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=s
spec.loader.exec_module(s)
f=s.f
def fmt(x):
    if x is None: return 'n/a'
    if math.isinf(x): return '-inf' if x<0 else 'inf'
    return '%.12g' % x
TOL=2e-7
REPORT=ROOT/'runs/k2c-exponent-2026-11-09/wedge-prop75-check.md'
def construct(alpha, delta, tau, variant, L=80., rise=.5, alpha2=None):
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
        a = alpha if variant != 'two-tilts' or xi < split_xi else alpha2
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
            xi += 0.0  # Let the vertex cap select J; do not add a ceiling-sized joining gap.
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
    r.window=(0.,L)
    return r



def sheared(case, L, alpha, alpha2):
    """Two narrow arriving families; no assertion of majority arrival.
    Within each stack layer i is translated -T*i/(n-1) along its tangent.
    Parallel consecutive squares meet on overlapping top/bottom edges.
    The tilt difference times n is compensated by the second stack's shear,
    keeping both tops close to the same ceiling without a large horizontal gap.
    """
    n=1000; z=1/L; T1=.8; T2=T1+n*(alpha-alpha2)
    x1=n*math.sin(alpha)+T1*math.cos(alpha)+.02
    candidates=[]; meta=[]
    for a,T,x in ((alpha,T1,x1),(alpha2,T2,x1+1.02)):
        c,sa=math.cos(a),math.sin(a)
        for i in range(n):
            shift=-T*i/(n-1)
            candidates.append(f.Square(x+(.5+shift)*c-(i+.5)*sa,
                                      (.5+shift)*sa+(i+.5)*c,a))
        meta.append((x,n,a,T))
    w=max(y-z*x for q in candidates for x,y in q.vertices())+1e-6
    r=f.Region(case,L,w,z,candidates)
    r.window=(0.,L); r.delta=1/32; r.tau=.08; r.m=n; r.meta=meta
    assert len(r.squares)==2*n, 'All specified sheared squares must survive filtering'
    return r


def ratio(lhs,rhs):
    return lhs/rhs if rhs else (0. if lhs==0 else math.copysign(math.inf,lhs))


def evaluate(r,a):
    G=a['counts']['arrival']; bs=a['boundaries']
    X=sum(f.val(p.end[0],p.hi)-f.val(p.end[0],p.lo) for p in a['arr'])
    ds=sum(b['Delta'] for b in bs)
    # Skip counts use the literal threshold, not the audit's tolerance-offset threshold.
    skips=sum(b['Delta']>=1/(2*r.z) for b in bs)
    lines=[]
    def le(tag,claim,lhs,rhs,witness=''):
        ok=lhs<=rhs+TOL
        lines.append((tag,claim,lhs,rhs,ratio(lhs,rhs),ok,witness))
    le('P1','L-|G| <= death bound',r.L-G,r.W/r.delta+1350*r.W/r.tau+134000*r.delta*r.W+.01)
    le('P2','cos(zeta-prime)|G| <= |X-prime|',math.cos(math.atan(r.z))*G,X)
    le('P3','sum Delta <= L-|X-prime|',ds,r.L-X)
    le('P3','-min Delta <= 0',-min((b['Delta'] for b in bs),default=0),0.)
    le('P4','skip count <= 2 zeta sum Delta',skips,2*r.z*ds)
    le('P5','sin(zeta-prime)|G|-delta <= positive drops',math.sin(math.atan(r.z))*G-r.delta,a['positive'])
    le('P6','positive drops <= tau sum Theta + delta skips',a['positive'],r.tau*a['theta']+r.delta*skips)
    eligible=[]
    for b in bs:
        if b['drop']>f.EPS:
            skip=b['Delta']>=1/(2*r.z) and b['Np']>b['N']
            le('P6-boundary','drop <= tau Theta or skip',b['drop'],math.inf if skip else r.tau*b['Theta'],repr(b) if not skip and b['drop']>r.tau*b['Theta']+TOL else '')
            if b['Delta']<1/(2*r.z): eligible.append((ratio(b['drop'],r.tau*b['Theta']),b))
    le('P7','0.7 sum Theta <= sum theta Y',.7*a['theta'],a['cost'])
    le('P7','sum theta Y <= 14851 W',a['cost'],14851*r.W)
    if G+TOL>=.75*r.L and r.z*r.L>=1:
        R=r.z*r.L
        le('P8','0.53 L <= |X-prime|',.53*r.L,X)
        le('P8','sum Delta <= 0.47 L',ds,.47*r.L)
        le('P8','skips <= 0.94 R',skips,.94*R)
        le('P8','0.499 R <= sin(zeta-prime)(3L/4)-delta',.499*R,math.sin(math.atan(r.z))*.75*r.L-r.delta)
        le('P8','0.4696 R <= tau 21216 W',.4696*R,r.tau*21216*r.W)
        le('P8','0.47 R <= 21300 tau W',.47*R,21300*r.tau*r.W)
    worst=max(eligible,key=lambda v:v[0],default=(None,None))
    return lines,worst,X,ds,skips


def outcome_text(results):
    """Header conclusions derived from measured results, never fixed claims."""
    majority=sum(v['G']+TOL>=.75*v['L'] for v in results)
    literal=sum(v['hyp']<=1 for v in results)
    eligible=sum(v['G']+TOL>=.75*v['L'] and v['R']>=1 for v in results)
    intro=('Floating point experiments, not a certificate. %d of %d packings meet the majority-arrival target; %d meet the literal small-waste hypothesis of Proposition 7.5. '
           'The intended nonvacuous replacement is measured arrival >=3L/4; it was %s. '
           'All comparisons use 2e-7 as in the imported audit; positive-drop eligibility uses its 2e-10 geometry epsilon. '
           'A ratio above 1 alone can be within tolerance; witnesses are retained. Zero/zero is displayed as 0, nonzero/zero as signed infinity. '
           'Lower bounds are reversed into lhs <= rhs; thus all ratio columns use that direction.'
           %(majority,len(results),literal,'achieved' if majority else 'not achieved'))
    outcome=('OUTCOME: %d majority-arrival packings; P8 exercised on %d packings. '%(majority,eligible))
    if not eligible:
        outcome+='The requested substantive P8 test remains UNEXERCISED. Passing empty-arrival inequalities is vacuous; this is not evidence for the last proof step. '
    empty=[v for v in results if v['case'] in ('A','B') and v['G']==0]
    if empty:
        outcome+=('The empty A/B staircases have cumulative gap deaths: a path crosses the seam under its column\'s lowest tilted square and the top-to-ceiling gap. '
                  'Their sum is about sin(alpha)+(1-cos(alpha))/2, independently of entry point. '
                  'At alpha=0.07 this is %.12g > delta=1/32, so increasing L alone cannot restore arrivals. '
                  'Arrival requires sin(alpha)+(1-cos(alpha))/2 < delta (hence alpha about 0.03 or less here). '
                  'This diagnoses the specified construction, not an impossibility theorem.'
                  %(math.sin(.07)+(1-math.cos(.07))/2))
    return intro,outcome


def main():
    start=time.monotonic(); sections=[]; summary=[]; attempts=[]; failures=0; outcomes=[]
    # Bounded deterministic list. Stop A/B at the first measured majority success.
    plans=[('A',.07,None,1.,(120.,160.,200.)),
           ('B',.07,None,2.,(80.,)),
           ('C1',.0799,.0798,1.,(10000.,)),
           ('C2',.07999,.0799,1.,(100000.,))]
    for case,alpha,alpha2,R,Ls in plans:
        for L in Ls:
            t=time.monotonic(); stages={}
            def mark(k,previous):
                stages[k]=time.monotonic()-previous
                return time.monotonic()
            print('Starting',case,'L=',L,flush=True)
            r=(construct(alpha,1/32,.08,'clean',L,R) if alpha2 is None else sheared(case,L,alpha,alpha2))
            r.name=case+' L='+fmt(L); u=mark('construct',t)
            validated=s.independent_validate(r); u=mark('independent validation',u)
            profiles=r.profiles(r.delta); u=mark('profiles',u)
            bypair,conf=f.conflict_intervals(r,profiles,r.tau); u=mark('conflicts',u)
            paths=s.interval_flow(r,profiles,conf,r.delta,r.tau); u=mark('flow',u)
            a=s.audit(r,paths); mark('audit',u)
            lines,worst,X,ds,skips=evaluate(r,a)
            frac=a['counts']['arrival']/L
            elapsed=time.monotonic()-t
            attempts.append((case,L,frac,len(r.squares),elapsed))
            hyp=(4250*r.W+1350*r.W/r.tau+.01)/(L/4)
            outcomes.append(dict(case=case,G=a['counts']['arrival'],L=L,R=R,hyp=hyp))
            failed=[v for v in lines if not v[5]]
            failures+=len(failed)+len(a['failures'])
            sections+=['','## '+r.name,'',
              'Parameters: `'+repr(dict(L=L,R=R,zeta=r.z,w=r.w,alphas=(alpha,alpha2),m=r.m,squares=len(r.squares),W=r.W,delta=r.delta,tau=r.tau,window=r.window))+'`.',
              '', '|G|/L = '+fmt(frac)+'; |X-prime| = '+fmt(X)+'; sum Delta = '+fmt(ds)+'; skips = '+str(skips)+'.',
              'Literal proposition hypothesis ratio = '+fmt(hyp)+' (must be <=1; NOT MET).',
              'Majority-arrival target: '+('PASS' if frac>=.75 else 'NOT MET')+'. P8 is ineligible when this target fails.',
              'Independent validation: '+str(validated)+' SAT comparisons, PASS. Stage seconds: `'+repr(stages)+'`.',
              '', '| Line | Comparison (all written lhs <= rhs) | lhs | rhs | lhs/rhs | Result |',
              '|---|---|---:|---:|---:|---|']
            # Summarize passing boundary checks by worst residual; preserve every failure below.
            display=[v for v in lines if v[0]!='P6-boundary']
            boundaries=[v for v in lines if v[0]=='P6-boundary']
            if boundaries: display.append(max(boundaries,key=lambda v:v[2]-v[3]))
            for tag,claim,lhs,rhs,rr,ok,wit in display:
                sections.append('| %s | %s | %s | %s | %s | %s |'%(tag,claim.replace('|',chr(92)+'|'),fmt(lhs),fmt(rhs),fmt(rr),'PASS' if ok else 'FAIL'))
            sections+=['','Existing staircase audit checks 1-8:', '', '| Check | Result | Comparisons |','|---|---|---:|']
            for k in range(1,9): sections.append('| %d | %s | %d |'%(k,'PASS' if all(a['checks'][k]) else 'FAIL',len(a['checks'][k])))
            sections+=['','Largest non-skip positive drop/(tau Theta): '+fmt(worst[0])+'.',
                       'Boundary witness (one-sided limits; square ids in chains below): `'+repr(worst[1])+'`.']
            if worst[1]:
                b=worst[1]; p,q=a['arr'][b['k']-1:b['k']+1]
                sections+=['Facing itinerary chains: `'+repr((p.chain,q.chain))+'`.',
                           'Facing affine paths `(lo,hi,end,V)`: `'+repr([(v.lo,v.hi,v.end,v.V) for v in (p,q)])+'`.']
                if worst[0]>1+TOL:
                    ids=sorted(set(p.chain+q.chain))
                    sections+=['Full involved square geometry `(id,cx,cy,angle)`: `'+repr([(i,r.squares[i].x,r.squares[i].y,r.squares[i].a) for i in ids])+'`.']
            sections+=['','All failure witnesses: `'+repr(failed+a['failures'])+'`.',
                       'Ending measures: `'+repr(dict(a['counts']))+'`.',
                       'Construction metadata: staircase `(xi,J,n,alpha)` or sheared `(base_x,n,alpha,T)` (deterministic packing witness): `'+repr(r.meta)+'`.']
            cells=[]
            for tag in ('P1','P2','P3','P4','P5','P6','P7','P8'):
                vs=[v for v in lines if v[0]==tag]
                cells.append(', '.join(fmt(v[4]) for v in vs) if vs else 'not eligible')
            summary.append('| %s | %s | %d | %s | %s | %s |'%(case,fmt(L),len(r.squares),fmt(frac),' | '.join(cells),fmt(worst[0])))
            print(case,'L',L,'squares',len(r.squares),'arrival',fmt(frac),'max ratio',fmt(worst[0]),'failures',len(failed)+len(a['failures']),'seconds',fmt(elapsed),flush=True)
            del profiles,bypair,conf,paths,a,r
            gc.collect()
            if alpha2 is None and frac>=.75: break
    elapsed=time.monotonic()-start
    intro,outcome=outcome_text(outcomes)
    head=['# Proposition 7.5 full-floor numerical checks','',
      intro,
      '', 'Construction adapted from the published staircase constructor, with full floor, specified rise, explicit second tilt, and no artificial ceiling-clearance horizontal shift at the tilt join. All vertex caps and SAT filters remain for staircase cases. C instead uses the explicitly specified sheared stacks: layer i shifts by -T*i/(n-1) along the square tangent, with n=1000, T1=0.8, T2=T1+n(alpha1-alpha2), base separation1.02, and w=max(Y-zeta X) over candidate vertices plus1e-6. Each constructed packing is independently validated before profiles or flow. All original audit checks 1-8 are rerun, including every boundary and aligned level. Tube cost uses the audit interior representatives (up to 1e-7 from limits), while drop and Delta use limits. P6 uses literal skip thresholds; the imported audit uses its documented 2e-7 threshold offset. P3 second ratio is a signed-zero denominator diagnostic; its lhs and PASS/FAIL matter.',
      '', '| Case | L | Squares | arrival fraction | P1 | P2 | P3 (sum, order) | P4 | P5 | P6 | P7 (lower, upper) | P8 (six lines) | max drop/(tau Theta) |',
      '|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---|---|---:|']
    head+=summary+['',outcome]+['','Every L tried (case,L,arrival fraction,squares,seconds): `'+repr(attempts)+'`.',
       'Budget: A/B stop at first successful L in their stated lists; both C attempts are retained regardless of result. B was cut to L=80 after an exploratory L=240 (about 200000 squares) was interrupted during the expensive full-polyline ordering audit; no completed comparisons or arrival values from that interrupted B run are used here. Earlier A exploratory trials were rerun in this final version. An additional full-floor L=50, R=1 diagnostic also had zero arrivals (all gap deaths); it was inspected before the final run but not put through the complete audit and is not a completed case row. The original unsheared C trials were replaced before execution by two sheared constructions. No broader tilt or length optimization was run. Total runtime %.6f seconds; failed comparisons %d.'%(elapsed,failures)]
    REPORT.write_text('\n'.join(head+sections)+'\n')
    print('Wrote',REPORT,'runtime',elapsed,'failures',failures,flush=True)
    return 1 if failures else 0

if __name__=='__main__':
    raise SystemExit(main())
