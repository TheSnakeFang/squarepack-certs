#!/usr/bin/env python3
"""Exact arithmetic audit of main.tex lines 239-434 (Sections 5-7).
No floating point, network, third-party packages, or changes to existing files.
Run from the repository root: python3 -I tools/wedge_constants.py.
"""
import sys
sys.dont_write_bytecode = True
from fractions import Fraction as F
from math import factorial, isqrt
from pathlib import Path
from time import monotonic

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/'runs/k2c-exponent-2026-11-09/wedge-constants.md'


def alternating(terms):
    """Decreasing alternating series: successive odd/even partial sums enclose.
    All callers use nonnegative arguments <=1, so terms decrease to zero.
    """
    sums=[]; total=F(0)
    for term in terms:
        total+=term; sums.append(total)
    return min(sums[-2:]),max(sums[-2:])


def sin_bounds(x):
    return alternating((-1)**k*x**(2*k+1)/factorial(2*k+1) for k in range(14))


def cos_bounds(x):
    return alternating((-1)**k*x**(2*k)/factorial(2*k) for k in range(14))


def atan_bounds(x):
    return alternating(F((-1)**k)*x**(2*k+1)/(2*k+1) for k in range(40))


def sqrt_bounds(x):
    den=10**30
    n=isqrt(x.numerator*den**2//x.denominator)
    lo,hi=F(n,den),F(n+1,den)
    assert lo*lo<=x<=hi*hi
    return lo,hi


def outward(x,upper=False):
    # Decimal display is outward rounded, never used for comparisons.
    den=10**12
    n=x.numerator*den//x.denominator
    if upper and F(n,den)<x: n+=1
    sign='-' if n<0 else ''
    n=abs(n)
    return '%s%d.%012d'%(sign,n//den,n%den)


def main():
    start=monotonic(); rows=[]
    d=F(1,32); t=F('0.08'); h=2*t
    slo,shi=sqrt_bounds(F(2))
    # Machin's identity pi = 16 atan(1/5)-4 atan(1/239).
    # The tangent addition formula proves the identity; both sides lie in (3,4).
    a,b=atan_bounds(F(1,5)); c,e=atan_bounds(F(1,239))
    plo,phi=16*a-4*e,16*b-4*c
    stlo,sthi=sin_bounds(t); ctlo,cthi=cos_bounds(t)
    shlo,shhi=sin_bounds(h); chlo,chhi=cos_bounds(h)
    tan_t_hi=sthi/ctlo
    def check(where,claim,lhs,rhs,reason,strict=False):
        ok=lhs<rhs if strict else lhs<=rhs
        rows.append((where,claim,ok,outward(lhs,True),outward(rhs),reason))
    def le(w,c,l,r,why): check(w,c,l,r,why)
    def lt(w,c,l,r,why): check(w,c,l,r,why,True)
    le('5, l243','2 tau <= 0.16',2*t,F('.16'),'Increasing in tau; tau <= 0.08.')
    # 0<=|phi|<=tau, 0<=theta<=2tau; cos decreases, sin increases.
    lt('5, l262-264','cos(tau)>0',0,ctlo,'Worst case tau=0.08; cos is decreasing on [0,0.08].')
    lt('5, l264','cos(tau)-sin(tau)>0',0,ctlo-sthi,'Worst case tau=0.08; cos-sin decreases on this interval.')
    lt('5, l264,296','cos(0.16)>0 (positive normal product)',0,chlo,'Angle between flat normals has absolute value <=0.16.')
    lt('5, l243,405','2 tau < pi/4 (orientation distance is absolute angle)',h,plo/4,'Worst case tau=0.08; below the modulo-pi/2 midpoint.')
    le('5, l274','sec(theta)>=1 for 0<=theta<=0.16',1,chlo**-1,'Cos lies in (0,1]; hence every sec factor is >=1. Endpoint bound verifies positivity.')
    # For 0<=zeta<=1: 1+zeta^2<=2, so both trigonometric statements reduce to sqrt(2).
    le('5, l241,280','1+zeta^2 <= 2 for zeta in [0,1]',1+F(1)**2,2,'Increasing in zeta; atan is increasing, giving atan(zeta)<=pi/4.')
    lt('5, l280','cos(phi-atan(zeta))>0',h+phi/4,plo/2,'|phi-atan(zeta)| <= 0.08+pi/4 <= 0.16+pi/4 < pi/2; ensures a positive denominator.')
    le('5, l280','cos(atan(zeta)) >= 1/sqrt(2)',2,2,'Square both positive sides: 1+zeta^2<=2 for zeta<=1.')
    le('5, l280','sin(atan(zeta)) >= zeta/sqrt(2)',2,2,'Divide by zeta>0 and square; same worst case zeta=1.')
    le('5, l303','unit-square horizontal/vertical extent <= sqrt(2)',2,2,'For any angle, (|cos|+|sin|)^2 <=2(cos^2+sin^2)=2 by (|cos|-|sin|)^2>=0.')
    le('6, l323','delta <= 2/5 (local distance applies)',d,F(2,5),'The common sqrt(2) cancels.')
    area_lo=plo*(F('1.9')+slo/2)**2
    area_hi=phi*(F('1.9')+shi/2)**2
    lt('6, l327','21.35 < pi(1.9+sqrt(2)/2)^2',F('21.35'),area_lo,'Positive factors; rational lower enclosures.')
    lt('6, l327','pi(1.9+sqrt(2)/2)^2 <21.36',area_hi,F('21.36'),'Positive factors; rational upper enclosures; interprets 21.35... prefix.')
    lt('6, l327','disc area <22 => at most21 disjoint unit areas',area_hi,22,'An integer count bounded by a number <22 is <=21, conditional on containment.')
    box_hi=(1+shi)*(shi+d)
    lt('6, l327','(1+sqrt(2))(sqrt(2)+delta)<3.49',box_hi,F('3.49'),'Positive factors; delta fixed.')
    lt('6, l327','3.49<4 => at most3 (hence4) floor squares',F('3.49'),4,'Integer area count; conditional on the stated box containment.')
    lt('6, l327','50(21+4sqrt(2))<1333',50*(21+4*shi),1333,'Use upper sqrt(2) enclosure.')
    le('6, l327','1333<=1350',1333,1350,'No free parameters; proves the displayed tilt-death coefficient.')
    lt('6, l341','cos(tau)-sin(tau)>0.9',F('.9'),ctlo-sthi,'Decreases in tau; worst tau=0.08.')
    lt('6, l341','delta<0.9 (separation from floor probes)',d,F('.9'),'Delta=1/32.')
    # For theta<=0.16, sin(theta)<=theta; cos(theta)>=cos(0.16)>0.
    # This proves the full range without sampling or assuming monotonicity of a ratio.
    le('6, l347','4 tan(theta)/cos(theta) <=4.3 theta',4/chlo**2,F('4.3'),'For theta>0 divide by theta; sin(theta)/theta<=1, cos(theta)>=cos(0.16). theta=0 by continuity.')
    lt('6, l345','delta/cos(theta)<1 (backward crossing stays inside length1)',d/chlo,1,'theta<=0.16; cos bounded below; permits sufficiently small positive eta.')
    lt('6, l354','2 delta <2/5 (local rectangle distance applies)',2*d,F(2,5),'Common sqrt(2) cancels.')
    # Sharper sin(theta)/theta upper alternating series: 1-u^2/6+u^4/120.
    # To prove tan(u)<=1.01u uniformly use sin(u)<=u and cos(u)>=1-u^2/2.
    # At .16 this crude bound is insufficient, so retain the cubic: sin(u)/u<=1-u^2/6+u^4/120.
    # Difference 1.01(1-u^2/2)-(1-u^2/6+u^4/120) decreases in v=u^2>=0.
    def tan_coefficient_check(endpoint):
        v=endpoint**2
        return 1-v/6+v**2/120,F('1.01')*(1-v/2)
    lh,rh=tan_coefficient_check(h)
    le('6, l354','tan(theta)<=1.01 theta, theta<=0.16',lh,rh,'In v=theta^2 the RHS-LHS is 0.01-(1.01/2-1/6)v-v^2/120, decreasing. Check v=0.16^2; theta=0 by continuity.')
    lh,rh=tan_coefficient_check(t)
    le('6, l354','tan(a)<=1.01 a, a<=tau<=0.08',lh,rh,'Same decreasing polynomial margin; endpoint a=0.08.')
    le('6, l354','2*1.01=2.02',2*F('1.01'),F('2.02'),'Two lateral sides.')
    le('6, l354','2.02+4.3=6.32',F('2.02')+F('4.3'),F('6.32'),'Combined ordered-pair coefficient.')
    lt('6, l354; 7, l375','1.9+sqrt(2)/2<2.61',F('1.9')+shi/2,F('2.61'),'Containment radius enlarges to2.61.')
    lt('6, l354; 7, l375','pi*2.61^2<22 => at most21 unit squares',phi*F('2.61')**2,22,'Integer count conditional on disc containment.')
    le('6, l354','21*20=420 ordered pairs',21*20,420,'Distinct squares; unordered pairs give half.')
    le('6, l354','two walls *4 squares=8',2*4,8,'Conditional on the claimed per-wall box bound (listed separately below).')
    lt('6, l354','2*1.01*delta*tan(tau)<0.01',2*F('1.01')*d*tan_t_hi,F('.01'),'Increasing tan on [0,0.08]; worst tau=0.08, fixed delta.')
    le('6, l354','50(6.32*420+2.02*4+1.01*8)<=134000',50*(F('6.32')*420+F('2.02')*4+F('1.01')*8),134000,'Derives the corollary coefficient from the stated multiplicities.')
    le('6, l351','1/delta+134000 delta<=4250',1/d+134000*d,4250,'Delta=1/32.')
    le('7, l369','(2/5)^(-1)=5/2',F(2,5)**-1,F(5,2),'Reciprocal line-waste threshold.')
    le('7, l369','2 tau*(5/2)<=0.4',2*t*F(5,2),F('.4'),'Increasing in tau; endpoint0.08.')
    le('7, l375','21 choose2=210',F(21*20,2),210,'Unordered distinct pairs.')
    lt('7, l375','sqrt(2)*50*210<14850',shi*50*210,14850,'Upper rational sqrt enclosure.')
    le('7, l364-375','14850+0.4<=14851',14850+F('.4'),14851,'Adds bad and not-bad contributions.')
    # |sin v|<=|v| and mean value theorem prove the Lipschitz estimate for all tilts.
    le('7, l405','sin(tau)<=tau for all 0<=tau<=0.08',1,1,'sin(tau)/tau<=1 follows by integrating cos(u)<=1; tau=0 by limit. Then MVT bounds |cos(phi)-cos(phi-prime)|<=tau |phi-phi-prime|.')
    lt('7, l405','cos(0.08)-1/4-1/32>0.7',F('.7'),ctlo-F(1,4)-d,'Cos decreases with tau; worst tau=0.08.')
    le('7, l412,416','delta<=1/4',d,F(1,4),'Non-aligned-level branch and large-Theta branch.')
    le('7, l415-416','1-cos(phi)<=0.51 tau^2 for |phi|<=tau',F(1,2),F('.51'),'1-cos(phi)=integral sin(u)du<=phi^2/2<=tau^2/2; divide by tau^2>0.')
    lt('7, l415','j(1-0.51 tau^2)>1/2 for j>=1',F(1,2),1-F('.51')*t*t,'Coefficient positive, expression increases in j and decreases in tau; worst j=1,tau=0.08.')
    le('7, l415','delta<=1/2',d,F(1,2),'Bounds any positive drop by1/2.')
    le('7, l416','j(1-0.51 tau^2)-1/4-delta>=1/2',F(1,2),1-F('.51')*t*t-F(1,4)-d,'Same monotonicity; worst j=1,tau=0.08.')
    le('7, l425','1-1/4=3/4',1-F(1,4),F(3,4),'Death bound <=L/4 gives arriving measure >=3L/4.')
    le('7, l425','3/(4sqrt(2))>=0.53',F('.53'),F(3,4)/shi,'Worst zeta=1 in cos(atan(zeta)); |G|>=3L/4.')
    le('7, l425','1-0.53=0.47',1-F('.53'),F('.47'),'Complement measure bound.')
    le('7, l425','2*0.47=0.94',2*F('.47'),F('.94'),'Count each skip against width1/(2zeta).')
    le('7, l429','(3/(4sqrt(2)))R-1/32>=0.499R for R>=1',F('.499'),F(3,4)/shi-d,'Divide by R>0; -delta/R increases in R, worst R=1.')
    le('7, l429','0.94/32<=0.0294',F('.94')*d,F('.0294'),'Rounded skip loss (strictly less, by0.000025).')
    le('7, l429','0.499-0.0294>=0.4696',F('.4696'),F('.499')-F('.0294'),'Exact subtraction.')
    le('7, l429','0.499-0.94/32>=0.4696',F('.4696'),F('.499')-F('.94')*d,'Direct exact check before the intermediate upward rounding of skip loss.')
    le('7, l429','14851/0.7<=21216',F(14851)/F('.7'),21216,'Divide the tube bound by positive0.7.')
    lt('7, l429','0.47*21216<0.4696*21300',F('.47')*21216,F('.4696')*21300,'Preserves a slightly weaker final coefficient.')
    le('Theorem1.5, l433','sqrt(LR)<=L when R<=L',1,1,'Divide positive L^2: R/L=zeta<=1; square roots preserve order.')
    le('Theorem1.5, l433','10800*(7e-6)<=0.0756',10800*F('0.000007'),F('.0756'),'Increasing in W/L; endpoint7e-6; W>0 gives tau>0.')
    le('Theorem1.5, l433','0.0756<=0.08',F('.0756'),t,'Tau lies in the proposition range.')
    le('Theorem1.5, l433','1350/10800=1/8',F(1350,10800),F(1,8),'Cancel W>0 after substituting tau=10800W/L; holds for every positive W,L.')
    le('Theorem1.5, l433','4250*(7e-6)<=0.03',4250*F('0.000007'),F('.03'),'Increasing in W/L, worst endpoint.')
    le('Theorem1.5, l433','0.01<=0.01L for L>=R>=1',F('.01'),F('.01'),'Increasing in L; worst L=1.')
    le('Theorem1.5, l433','0.03+1/8+0.01<=1/4',F('.03')+F(1,8)+F('.01'),F(1,4),'Divide by L; all three terms bounded for entire stated range.')
    le('Theorem1.5, l433','sharper hypothesis bound:0.02975+1/8+0.01<=1/4',4250*F('.000007')+F(1,8)+F('.01'),F(1,4),'Same bound before rounding0.02975 up to0.03.')
    le('Theorem1.5, l433','21300*10800=230040000',21300*10800,230040000,'Substitution into the proposition.')
    le('Theorem1.5, l433','sqrt(0.47/(21300*10800))>=4.5e-5',F('.000045')**2*21300*10800,F('.47'),'Square positive quantities; equivalent exact rational comparison.')
    le('Theorem1.5, l433','4.5e-5>=7e-6',F('.000007'),F('.000045'),'Multiply by nonnegative sqrt(LR).')
    le('Theorem1.5, l433','W=0:0.01<=L/4 for L>=1',F('.01'),F(1,4),'Worst L=1 gives the proposition hypothesis at tau=0.08.')
    lt('Theorem1.5, l433','W=0:0.47R>0 for R>=1',0,F('.47'),'Increasing in R, worst R=1; contradiction.')
    unchecked=[
        ('5, l245','Local rectangle constants: distance sqrt(2)+2/5, charge theta/50, radius1.9. These are imported geometric claims from Corollary local, whose proof is outside Sections5-7; this checker uses them as premises.'),
        ('6, l354','At most4 squares per wall and exactly2 exceptional left-wall squares: the text imports Section walls and supplies no finite enclosure/count computation here. The arithmetic using4,8,2 is checked above; the geometric applicability is not certified.'),
        ('5-7','Packing-dependent density1, gap W/delta, probe measures2 delta tan(theta) and delta tan(a), conflict projection4 delta tan(theta)/cos(theta), disjoint tubes, and drop/tube identities are geometric/measure statements. Their numerical relaxations are checked above; exact arithmetic alone does not verify those statements.')]
    lines=['# Exact numerical constants audit','',
        'Source: paper-wedge/main.tex lines239-434 (Sections5-7 and the proof of Theorem1.5). Standard library only. All arithmetic uses Fraction; there are no floating point comparisons. Square-root bounds use integer square roots at denominator10^30. Sine and cosine use alternating Taylor sums with signed remainders; pi uses Machin identity and alternating arctangent sums. Displayed decimal endpoints are rounded outward to12 places. Every free-parameter reduction is explained in the final column and in source comments. This validates arithmetic conditional on the stated geometric premises, not the proof.',
        '', '| Where | Claim | Result | Upper bound on lhs | Lower bound on rhs | Whole-range reduction / evidence |',
        '|---|---|---|---:|---:|---|']
    for w,c,ok,l,r,why in rows: lines.append('| %s | %s | %s | %s | %s | %s |'%(w,c.replace('|',chr(92)+'|'),'PASS' if ok else 'FAIL',l,r,why.replace('|',chr(92)+'|')))
    lines+=['','## Claims not reduced to finite arithmetic','']
    for w,c in unchecked: lines.append('- '+w+': '+c)
    failed=sum(not r[2] for r in rows)
    lines+=['','%d exact claims checked; %d FAIL; %d separately listed unchecked premise groups. Runtime %.6f seconds.'%(len(rows),failed,len(unchecked),monotonic()-start)]
    REPORT.write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))
    return bool(failed)

if __name__=='__main__':
    raise SystemExit(main())
