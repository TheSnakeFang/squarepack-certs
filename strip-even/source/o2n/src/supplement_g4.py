"""Add one independent random H per n: core G4 has 299 random H plus H=2."""
import sys,hashlib,pathlib
import numpy as np,mpmath as mm
import driver as d
mm.mp.dps=80;rng=np.random.default_rng(2026110104);rows=[]
for n in (8,6,10):
 h=float(rng.uniform(float(d.LO[n]),2));m=d.setup(n,max(float(d.LO[n]),h-.0025),min(2,h+.0025));hh=mm.mpf(h);k=n//2
 f=lambda t:n+(2-hh)*(k*t+(k-1)/t)-(n-2)*(1+t+1/t-mm.sqrt((t+1/t)*(t+1/t+2)))
 t=mm.findroot(lambda z:mm.diff(f,z),(.85,1.1));gap=float(mm.mpf(d.fi(n,m['T_hat'],h)[1])-f(t));assert m['T_lo']<t<m['T_hi'] and gap>=0
 rows.append({'n':n,'H':h,'bracket':[m['T_lo'],m['T_hi']],'root':str(t),'trial_upper_minus_minimum':gap,'violations':0})
obj={'random_H_per_n_added':1,'combined_random_H_per_n':300,'combined_endpoint_H_per_n':1,'rows':rows,'hashes':d.hashes(),'supplement_source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}
d.write('supplemental-gates.json',obj);d.log('G4 supplement '+__import__('json').dumps(obj),'gates.log')

# Older o2cert G1 support-function/hull cross-check, retained for completeness.
import math
from hull_reference import kappa
worst=0.
for _ in range(2000):
 a,b=rng.uniform(0,math.pi/2,2);dy=rng.uniform(-.9,.9)
 rs=np.r_[np.linspace(-100,100,20001),math.tan(a),-1/math.tan(a),math.tan(b),-1/math.tan(b)]
 gg=lambda t:(np.abs(math.cos(t)+rs*math.sin(t))+np.abs(math.sin(t)-rs*math.cos(t)))/2
 dual=float(np.min(gg(a)+gg(b)-rs*dy));worst=max(worst,abs(dual-kappa(a,b,dy)))
assert worst<=1e-9
obj['legacy_G1_dual_hull']={'triples':2000,'max_error':worst,'violations':0}
obj['hull_reference_sha256']=hashlib.sha256((d.R/'src/hull_reference.py').read_bytes()).hexdigest()
d.write('supplemental-gates.json',obj);d.log('G1 dual-hull supplement '+__import__('json').dumps(obj['legacy_G1_dual_hull']),'gates.log')
# Exact rational comparisons for the printed coordinate caps, using the C
# outward upper bound on Theta/k. Avoid any float arithmetic in these ratios.
from fractions import Fraction
checks=[]
for n,five in [(8,False),(6,False),(10,False),(10,True)]:
 t=d.tail(n,five);theta=Fraction(t['theta_over_k_upper'])
 for j in ([1] if five else d.blocks(n)):
  rr,yr=d.domains(n,j,five)
  targets=[theta,theta,2*theta] if five else [theta*(n//2-1)/(n//2-j),theta*(n//2-1)/j]
  slacks=[Fraction(r[1])-target for r,target in zip(rr,targets)]+[Fraction(yr[1])-theta]
  assert min(slacks)>0
  checks.append({'n':n,'five':five,'j':j,'minimum_cap_slack_exact':str(min(slacks))})
obj['exact_cap_checks']=checks
obj['supplement_source_sha256']=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
d.write('supplemental-gates.json',obj)
d.log('Exact rational cap comparisons PASS '+__import__('json').dumps(checks),'gates.log')
