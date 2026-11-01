"""Loud randomized gates; fixed reproducible seed, no weakened thresholds."""
import time, math, multiprocessing as mp
import numpy as np
import mpmath as mm
import driver as d

def dense_job(data):
 x,y=data;x=np.ascontiguousarray(x);y=np.ascontiguousarray(y);a=np.empty(len(x));m=np.empty(len(x));d.LIB.dense_batch(len(x),x.ctypes.data_as(d.P),y.ctypes.data_as(d.P),a.ctypes.data_as(d.P));d.LIB.dense_m_batch(len(x),x.ctypes.data_as(d.P),m.ctypes.data_as(d.P));return a,m

def main(args):
 t0=time.monotonic();rng=np.random.default_rng(20261101);results={};mm.mp.dps=65
 def record(name,obj):
  obj['passed']=obj['violations']==0;obj['elapsed_seconds']=time.monotonic()-t0;results[name]=obj;d.log(name+' '+__import__('json').dumps(obj),'gates.log');d.write('gates.partial.json',results)
  if not obj['passed']:raise RuntimeError(name+' FAILED; certification forbidden')
 d.log('START seed=20261101 workers='+str(args.workers),'gates.log')
 n=200000;x=rng.uniform(-8,8,n);y=rng.uniform(-8,8,n)
 with mp.Pool(args.workers) as pool:r=pool.map(dense_job,list(zip(np.array_split(x,args.workers),np.array_split(y,args.workers))))
 ar=np.concatenate([a for a,m in r]);mr=np.concatenate([m for a,m in r]);lower=np.array([d.LIB.a_bound(a,a,b,b,2) for a,b in zip(x,y)]);ml=np.array([d.LIB.m_bound(a,a,0) for a in x]);gap=ar-lower;mg=mr-ml
 v=int(np.sum((gap<0)|(gap>1e-9))+np.sum((mg<0)|(mg>1e-9)));err=[0.,0.,0.]
 for u in rng.uniform(.5,1.5,1000):
  z=mm.mpf(float(u));f=lambda z:1+z+1/z-mm.sqrt((z+1/z)*(z+1/z+2))
  for order in range(3):
   target=float(mm.diff(f,z,order));iv=d.di(u,order=order);e=max(iv[0]-target,target-iv[1],0);err[order]=max(err[order],abs(sum(iv)/2-target));v+=int(e>1e-10)
 record('G1_points_D',{'points':n,'dense_points_per_reference':20001,'D_points':1000,'violations':v,'A_gap_min':float(gap.min()),'A_gap_max':float(gap.max()),'m_gap_min':float(mg.min()),'m_gap_max':float(mg.max()),'D_Dp_Dpp_max_error':err})
 v=0;worst=[-math.inf]*4
 for i in range(100000):
  widths=10**rng.uniform(-8,math.log10(2),2);lo=rng.uniform(-8,8-widths);hi=lo+widths
  if i<50000:
   if i%3<2:k=i%3;lo[k]=-widths[k]*rng.random();hi[k]=lo[k]+widths[k]
   else:
    a=rng.uniform(.2,4)*rng.choice([-1,1]);lo=np.array([a,-1/a])-widths*rng.random(2);hi=lo+widths
  bs=[d.LIB.a_bound(lo[0],hi[0],lo[1],hi[1],mode) for mode in (0,1)];ms=[d.LIB.m_bound(lo[0],hi[0],mode) for mode in (0,1)]
  for a,b in rng.uniform(lo,hi,(20,2)):
   ref=d.A(a,b);mref=1+a if a>=0 else 1/math.sqrt(1+a*a);es=[bs[0]-ref,bs[1]-ref,ms[0]-mref,ms[1]-mref]
   for j,e in enumerate(es):worst[j]=max(worst[j],e);v+=int(e>0)
  if (i+1)%20000==0:d.log(f'G1_box progress={i+1} violations={v}','gates.log')
 record('G1_boxes_centered',{'boxes':100000,'points_per_box':20,'straddling_boxes':50000,'violations':v,'max_excess_plain_centered_A_m':worst})
 for n,five in [(8,False),(6,False),(10,False),(10,True)]:
  v=0;worst=-math.inf
  for i in range(20000):
   j=int(rng.choice(d.blocks(n)));rr,yr=d.domains(n,j,five);h=rng.uniform(float(d.LO[n]),2);ys=[]
   for _ in range(2 if five else 1):
    a,b=sorted(rng.uniform(*yr,2));ys.extend([a,b])
   if not five:ys.extend([0.,0.])
   xr=[];vals=[]
   for side,rg in enumerate(rr):
    a,b=sorted(rng.uniform(*rg,2));xr.append([a,b]);yy=ys if five and side==1 else (ys[:2]+[0.,0.] if side==0 or not five else ys[2:]+[0.,0.]);val,_,_=d.inner(n,j,side,five,[a,b],yy,h,31,1e-4);vals.append(val)
   lower=d.LIB.assemble((d.D*len(vals))(*vals),len(vals),*ys,h,int(five))
   for _ in range(20):
    xs=[rng.uniform(*r) for r in xr];y=rng.uniform(*ys[:2]);z=[xs[0],y,xs[1]]
    if five:z += [rng.uniform(*ys[2:]),xs[2]]
    ref=d.lref(h,z) if five else d.bref(n,j,h,z);e=lower-ref;worst=max(worst,e);v+=int(e>0)
   if (i+1)%5000==0:d.log(f'G2 n={n} five={five} progress={i+1} violations={v}','gates.log')
  record(f'G2_n{n}'+('_five' if five else ''),{'boxes':20000,'points_per_box':20,'violations':v,'max_excess':worst})
 v=0;errors=[0.,0.,0.,0.]
 for n in [8,6,10]:
  for _ in range(200):
   t=rng.uniform(.5,1.5);h=rng.uniform(float(d.LO[n]),2);z=[t if i%2==0 else 1/t for i in range(n-1)];e=abs(d.fref(n,t,h)-d.psi(n,h,z));errors[0]=max(errors[0],e);v+=int(e>1e-10)
   for j in d.blocks(n):
    e=abs(d.bref(n,j,h,[t,1/t,t])-2*(d.fref(n,t,h)-n)/(n-2));errors[1]=max(errors[1],e);v+=int(e>1e-12)
  for _ in range(500):
   h=rng.uniform(float(d.LO[n]),2);z=rng.uniform(-.4,5,n-1);z[0]=abs(z[0]);z[-1]=abs(z[-1]);e=abs(sum(d.bref(n,j,h,z[2*j-2:2*j+1]) for j in range(1,n//2))-d.psi(n,h,z)+n);errors[2]=max(errors[2],e);v+=int(e>1e-10)
 for _ in range(500):
  z=rng.uniform(-.4,5,5);z[0]=abs(z[0]);h=rng.uniform(float(d.LO[10]),2);e=abs(d.lref(h,z)-d.bref(10,1,h,z[:3])-d.bref(10,2,h,z[2:]));errors[3]=max(errors[3],e);v+=int(e>1e-10)
 record('G3',{'family_points_per_n':200,'telescoping_per_n':500,'five_identity_points':500,'violations':v,'max_errors':errors})
 v=0;err=0.;mingap=math.inf
 for n in [8,6,10]:
  for h in list(rng.uniform(float(d.LO[n]),2,299))+[2.]:
   a=max(float(d.LO[n]),h-.0025);b=min(2,h+.0025);meta=d.setup(n,a,b);hh=mm.mpf(float(h));m=n//2
   DD=lambda t:1+t+1/t-mm.sqrt((t+1/t)*(t+1/t+2));f=lambda t:n+(2-hh)*(m*t+(m-1)/t)-(n-2)*DD(t)
   t=mm.findroot(lambda t:mm.diff(f,t),(.85,1.1));v+=int(not meta['T_lo']<t<meta['T_hi']);trial=d.fi(n,meta['T_hat'],h)[1];delta=float(mm.mpf(trial)-f(t));mingap=min(mingap,delta);v+=int(delta<0);err=max(err,abs(float(t)-d.root(n,h)))
 record('G4',{'H_per_n':300,'violations':v,'max_root_error':err,'min_upper_trial_gap':mingap})
 v=0;minimum=math.inf;negmin=math.inf
 for n in [8,6,10]:
  for i in range(2000):
   h=2. if i<100 else rng.uniform(float(d.LO[n]),2);meta=d.setup(n,max(float(d.LO[n]),h-.0025),min(2,h+.0025));z=[rng.uniform(*meta['Ix']),rng.uniform(*meta['Iy']),rng.uniform(*meta['Ix'])];j=int(rng.choice(d.blocks(n)));gap=d.bref(n,j,h,z)-2*(d.fref(n,d.root(n,h),h)-n)/(n-2);minimum=min(minimum,gap);v+=int(gap< -1e-12)
 # Negative cY with Tan: cX=cY/T^2+D'(T), retain all revised hypotheses.
 count=0;attempts=0
 while count<2000:
  attempts+=1;t=rng.uniform(.92,.995);cy=rng.uniform(-.002,0);cx=cy/t**2+sum(d.di(t,order=1))/2
  if cx<0:continue
  xl,xu=t-.2,t+.2;yl,yu=1/t-.2,1/t+.2;jl=min(xl,1/yu);ju=max(xu,1/yl);ell=cx*t+cy/t-(1+t+1/t-math.sqrt((t+1/t)*(t+1/t+2)))
  psi=lambda u:1-1/math.sqrt(1+u*u);q=lambda u:(1+u)/math.sqrt(1+u*u)
  if not (.5<=jl and ju<=1.5 and cy<=psi(xl) and cx<=psi(yl) and cx*xl+min(cy*yl,cy*yu)>=ell and cy>=1-min(q(xl),q(xu))):continue
  if any(cy<=u**3*d.di(u,order=2)[1]/2 for u in np.linspace(jl,ju,65)):continue
  count+=1;x=rng.uniform(xl,xu);y=rng.uniform(yl,yu);g=d.A(x,-y)-1-x-y+cx*x+cy*y;gap=g-ell;negmin=min(negmin,gap);v+=int(gap< -1e-12)
 record('G5',{'local_points_per_n':2000,'negative_cY_instances':count,'negative_attempts':attempts,'violations':v,'min_block_gap':minimum,'min_negative_pair_gap':negmin})
 v=0;mins=[]
 for n in [8,6,10]:
  minimum=math.inf
  for _ in range(2000):
   h=rng.uniform(float(d.LO[n]),2);j=int(rng.choice(d.blocks(n)));rho=(2-h)/(4*(n//2-1));z=rng.uniform(-rho,rho,3)
   if j==1:z[0]=abs(z[0])
   gap=d.bref(n,j,h,z);minimum=min(minimum,gap);v+=int(gap<0)
  mins.append(minimum)
 minimum=cone=math.inf
 for _ in range(2000):
  h=rng.uniform(float(d.LO[10]),2);k=2-h;z=rng.uniform(-k/16,k/16,5);z[0]=abs(z[0]);gap=d.lref(h,z);minimum=min(minimum,gap);v+=int(gap<0)
  z=rng.uniform(-1,1,5);z[0]=abs(z[0]);z/=max(abs(z));sums=[z[i]+z[i+1] for i in range(4)];b=k*sum(z[:4])+k*z[4]/2+sum(max(-x,0) for x in sums);gap=b-k/2;cone=min(cone,gap);v+=int(gap< -1e-12)
 record('G6',{'origin_points_per_n':2000,'five_origin_points':2000,'cone_points':2000,'violations':v,'min_triple_values':mins,'min_five':minimum,'min_cone_slack':cone})
 d.write('gates.json',{'passed':True,'results':results,'seconds':time.monotonic()-t0,'hashes':d.hashes()});d.log(f'ALL PASS wall_seconds={time.monotonic()-t0:.6f}','gates.log')
