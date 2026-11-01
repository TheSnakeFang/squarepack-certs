#!/usr/bin/env python3
"""O2n certified block computation. All artifacts stay in o2n."""
import argparse, ctypes as ct, hashlib, heapq, itertools, json, gzip, math
import multiprocessing as mp, os, pathlib, time, resource, sys
from decimal import Decimal, localcontext
from fractions import Fraction
import numpy as np
from scipy.optimize import brentq
import mpmath as mm
R=pathlib.Path(__file__).resolve().parent.parent
D=ct.c_double; P=ct.POINTER(D); LIB=ct.CDLL(str(R/'src/kernel.dylib'))
for name,count in [('a_bound',4),('a_reference',2)]:
 f=getattr(LIB,name);f.argtypes=[D]*count+[ct.c_int];f.restype=D
LIB.m_bound.argtypes=[D,D,ct.c_int];LIB.m_bound.restype=D
LIB.d_interval.argtypes=[D,D,ct.c_int,P]
LIB.f_interval.argtypes=[ct.c_int,D,D,D,D,ct.c_int,P]
LIB.local_check.argtypes=[D]*9+[P]
LIB.tail_check.argtypes=[ct.c_int,D,D,ct.c_int,P]
LIB.leaf_bound.argtypes=[D]*7+[ct.c_int]*4;LIB.leaf_bound.restype=D
LIB.block_inner.argtypes=[D]*7+[ct.c_int]*5+[D,P,ct.POINTER(ct.c_int)];LIB.block_inner.restype=D
LIB.assemble.argtypes=[P,ct.c_int]+[D]*5+[ct.c_int];LIB.assemble.restype=D
LIB.dense_batch.argtypes=[ct.c_int,P,P,P];LIB.dense_m_batch.argtypes=[ct.c_int,P,P]
DN=lambda x:math.nextafter(x,-math.inf)
UP=lambda x:math.nextafter(x,math.inf)
LO={6:'1.861098',8:'1.852049',10:'1.846936'}
T0={6:.887,8:.919,10:.936}
NAMES=['containment','J','N1',"N1'","N2'",'N3','L','min_cY']
def bound_decimal(s,up=False):
 q=Decimal(s);f=float(q)
 return UP(f) if up and Decimal(f)<q else DN(f) if not up and Decimal(f)>q else f
def write(path,obj):
 p=R/path;p.parent.mkdir(exist_ok=True,parents=True);tmp=p.with_suffix(p.suffix+'.tmp')
 if p.suffix=='.gz':
  with gzip.open(tmp,'wt') as f:json.dump(obj,f,separators=(',',':'),allow_nan=False)
 else:tmp.write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')
 tmp.replace(p)
def read(path):
 p=R/path
 if p.suffix=='.gz':
  with gzip.open(p,'rt') as f:return json.load(f)
 return json.loads(p.read_text())
def log(s,file='run.log'):
 print(s,flush=True)
 with (R/file).open('a') as f:f.write(s+'\n')
def hashes():
 return {p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in ['SPEC.md','LEMMAS.md','src/kernel.c','src/block.c','src/driver.py','src/gates.py','src/kernel.dylib']}
def di(lo,hi=None,order=0):
 o=(D*2)();LIB.d_interval(lo,lo if hi is None else hi,order,o);return list(o)
def fi(n,t,h,deriv=0,th=None,hh=None):
 o=(D*2)();LIB.f_interval(n,t,t if th is None else th,h,h if hh is None else hh,deriv,o);return list(o)
def df(n,t,h):
 w=t+1/t;p=math.sqrt(w*(w+2));dp=(1/t**2-1)/(p*(p+w+1))
 return (2-h)*(n/2-(n/2-1)/t**2)-(n-2)*dp
def root(n,h):return brentq(lambda t:df(n,t,h),.5,1.5,xtol=5e-15)
def A(x,y):return LIB.a_reference(float(x),float(y),0)
def sref(x,y,c,ctilde):return A(x,-y)-1-(1-(c if x>=0 else ctilde))*x
def bref(n,j,h,z):
 k=2-h;m=n//2;x,y,v=z
 return sref(x,y,k*(m-j)/(m-1),k*(j-1)/(m-1))+sref(v,y,k*j/(m-1),k*(m-1-j)/(m-1))-h*y
def lref(h,z):
 a,y,b,w,c=z;k=2-h
 return sref(a,y,k,0)+A(b,-y)+A(b,-w)-2-h*b+sref(c,w,k/2,k/2)-h*(y+w)
def psi(n,h,z):return 2+z[0]+z[-1]+sum(A(z[i if i%2==0 else i+1],-z[i+1 if i%2==0 else i]) for i in range(n-2))-h*sum(z)
def fref(n,t,h):return n+(2-h)*(n/2*t+(n/2-1)/t)-(n-2)*(1+t+1/t-math.sqrt((t+1/t)*(t+1/t+2)))
def setup(n,a,b,five=False,stored=None):
 tl=stored['T_lo'] if stored is not None else math.floor((root(n,a)-.0005)*1e6)/1e6
 th=stored['T_hi'] if stored is not None else math.ceil((root(n,b)+.0005)*1e6)/1e6
 assert th-tl<.25
 signs=[fi(n,t,h,1) for h in (a,b) for t in (tl,th)]
 assert all(signs[i][1]<0 if i%2==0 else signs[i][0]>0 for i in range(4)),signs
 # Decimal arithmetic specifies exact rational factors, then rounds inward.
 with localcontext() as ctx:
  ctx.prec=80
  ix=[bound_decimal(str(Decimal(th)-Decimal(1)/4),True),bound_decimal(str(Decimal(tl)+Decimal(1)/4),False)]
  iy=[bound_decimal(str(1/Decimal(tl)-Decimal(1)/4),True),bound_decimal(str(1/Decimal(th)+Decimal(1)/4),False)]
 t=stored['T_hat'] if stored is not None else round(root(n,(a+b)/2),12)
 out={'n':n,'Ha':a,'Hb':b,'five':five,'T_lo':tl,'T_hi':th,'T_hat':t,'T_hat_rational':str(Fraction(t)),'derivative_brackets':signs,'Ix':ix,'Iy':iy}
 ratio=[1,.25,.75,.5] if five else sorted(set([(n//2-j)/(n//2-1) for j in blocks(n)]+[j/(n//2-1) for j in blocks(n)]))
 slacks=[]
 for rat in ratio:
  o=(D*8)();LIB.local_check(tl,th,a,b,rat,*ix,*iy,o)
  row=dict(zip(NAMES,o));assert min(row[k] for k in NAMES[:-1])>0,row
  slacks.append({'cx_over_k':rat,**row})
 out['Loc']=slacks
 out['U']=[UP(UP(fi(n,t,h)[1]-n)/(2 if five else (n-2)/2)) for h in (a,b)]
 # Every operation below rounds down. A zero-radius final cell excludes nothing.
 radius=0 if b==2 else DN(DN(2-b)/(16 if five else 4*(n//2-1)))
 out['origin_radius']=radius if out['U'][0]>-DN(radius*radius) else 0
 # Criterion in SPEC is U > -kappa^2/16; radius=kappa/4.
 return out
def tail(n,five):
 h=bound_decimal('1.86' if n==10 and not five else LO[n],False)
 cap=bound_decimal('.4155' if five else {6:'.3935',8:'.4077',10:'.3953'}[n],True)
 out=(D*2)();LIB.tail_check(n,h,cap,int(five),out);assert out[0]>0
 if five:assert out[1]<bound_decimal('5.955',False) and 2*out[1]<bound_decimal('11.909',False)
 else:
  for j in blocks(n):
   rr,yr=domains(n,j);assert out[1]<yr[1]
   assert UP(out[1]*(n//2-1)/(n//2-j))<rr[0][1] and UP(out[1]*(n//2-1)/j)<rr[1][1]
 return {'c_cap':cap,'cap_slack':out[0],'theta_over_k_upper':out[1]}

def h0(n,t=None):
 h=bound_decimal(LO[n],True);hl=bound_decimal(LO[n],False);t=round(root(n,h),12) if t is None else t;v=fi(n,t,hl,hh=h)[1];d=fi(n,bound_decimal(str(T0[n]),False),hl,1,th=bound_decimal(str(T0[n]),True),hh=h)[1]
 assert v<n and d<0
 return {'H':h,'T_hat':t,'f_upper':v,'f_minus_n_upper':UP(v-n),'T0':T0[n],'derivative_upper':d}
def blocks(n):return [1] if n==6 else [1,2]
def domains(n,j,five=False):
 cap=bound_decimal('.4155' if five else {6:'.3935',8:'.4077',10:'.3953'}[n],True)
 if five:return [[0,bound_decimal('5.955',True)],[-cap,bound_decimal('5.955',True)],[-cap,bound_decimal('11.909',True)]],[-cap,bound_decimal('5.955',True)]
 if n==6:tops=['3.091','6.181'];yt='3.091'
 elif n==8:tops=['3.013','9.039'] if j==1 else ['4.520','4.520'];yt='3.013'
 else:tops=['2.942','11.767'] if j==1 else ['3.923','5.884'];yt='2.942'
 return [[0 if j==1 else -cap,bound_decimal(tops[0],True)],[-cap,bound_decimal(tops[1],True)]],[-cap,bound_decimal(yt,True)]
def inner(n,j,side,five,rr,ys,h,budget,tol,trace=False):
 # Each leaf is wholly on one side of x=0, as required by the s formula.
 edges=sorted(set([rr[0],rr[1]]+([0.] if rr[0]<0<rr[1] else [])));lower=math.inf;leaves=[];count=0
 for lo,hi in zip(edges,edges[1:]):
  buf=(D*(2*(budget+2)))();ctn=ct.c_int();v=LIB.block_inner(lo,hi,*ys,h,n,j,side,int(five),budget,tol,buf,ct.byref(ctn));count+=2*ctn.value-1;lower=min(lower,v)
  if trace:leaves.extend([[buf[2*i],buf[2*i+1]] for i in range(ctn.value)])
 return lower,count,leaves
def pieces(meta,rr,ys):
 # Subtract product exclusions as unions over odd-coordinate complements.
 # Initial outer partitions align with all even-factor boundaries.
 regions=[rr]
 for odd,even in [(meta['Ix'],meta['Iy']),([-meta['origin_radius'],meta['origin_radius']],[-meta['origin_radius'],meta['origin_radius']])]:
  if even[1]<=even[0]:continue
  if not all(even[0]<=ys[i] and ys[i+1]<=even[1] for i in range(0,len(ys),2)):continue
  new=[]
  for region in regions:
   for k,r in enumerate(region):
    for seg in [[r[0],min(r[1],odd[0])],[max(r[0],odd[1]),r[1]]]:
     if seg[0]<seg[1]:new.append(region[:k]+[seg]+region[k+1:])
  regions=new
 return regions
def evaluate(meta,j,rect,budget,tol,trace=False):
 n=meta['n'];five=meta['five'];rr,_=domains(n,j,five);ys=list(rect) if five else list(rect)+[0.,0.];regions=pieces(meta,rr,rect)
 minimum=math.inf;count=0;record=[]
 for h,u in zip((meta['Ha'],meta['Hb']),meta['U']):
  cache={}
  for region in regions:
   vals=[];refs=[]
   for side,r in enumerate(region):
    yy=ys if five and side==1 else (ys[:2]+[0.,0.] if side==0 or not five else ys[2:]+[0.,0.])
    key=(side,*r,*yy)
    if key not in cache:
     val,used,leaves=inner(n,j,side,five,r,yy,h,budget,tol,trace);count+=used;cache[key]=(val,len(record))
     if trace:record.append({'h':h,'side':side,'range':r,'ys':yy,'leaves':leaves,'lower':val})
    v,ref=cache[key];vals.append(v);refs.append(ref)
   arr=(D*len(vals))(*vals);v=LIB.assemble(arr,len(vals),*ys,h,int(five));minimum=min(minimum,DN(v-u))
 return minimum,count,record

def rss_bytes():
 r=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
 return r if sys.platform=='darwin' else r*1024

def cell(meta,ident,seconds=120,max_outer=100000,budget=2047,tol=2e-5):
 start=time.monotonic();accepted=[];pending=[];stats={'outer_tested':0,'inner_boxes':0};minimum=None;best_failed=-math.inf
 for j in ([1] if meta['five'] else blocks(meta['n'])):
  _,yr=domains(meta['n'],j,meta['five']);edges=sorted(set([*yr,*[v for v in meta['Iy'] if yr[0]<v<yr[1]],*([-meta['origin_radius'],meta['origin_radius']] if meta['origin_radius']>0 else [])]))
  edges=[v for v in edges if yr[0]<=v<=yr[1]];intervals=list(zip(edges,edges[1:]));rects=[a+b for a in intervals for b in intervals] if meta['five'] else intervals
  heap=[(-math.prod(r[i+1]-r[i] for i in range(0,len(r),2)),tuple(r)) for r in rects];heapq.heapify(heap)
  while heap:
   if time.monotonic()-start>seconds or stats['outer_tested']>=max_outer or rss_bytes()>230*1024**2:break
   _,r=heapq.heappop(heap);v,k,_=evaluate(meta,j,r,budget,tol);stats['outer_tested']+=1;stats['inner_boxes']+=k
   if v>0:
    v,k,trace=evaluate(meta,j,r,budget,tol,True);assert v>0;stats['inner_boxes']+=k
    leafpath=f'cells/{ident}-leaves/{len(accepted):07d}.json.gz';write(leafpath,trace)
    accepted.append({'j':j,'rect':r,'margin':v,'inner_file':leafpath,'inner_sha256':hashlib.sha256((R/leafpath).read_bytes()).hexdigest()});minimum=v if minimum is None else min(minimum,v)
   else:
    best_failed=max(best_failed,v);dim=max(range(0,len(r),2),key=lambda i:r[i+1]-r[i]);mid=r[dim]+(r[dim+1]-r[dim])*.5
    if mid==r[dim] or mid==r[dim+1]:heapq.heappush(heap,(0,r));break
    for l,u in [(r[dim],mid),(mid,r[dim+1])]:
     ch=list(r);ch[dim:dim+2]=[l,u];heapq.heappush(heap,(-math.prod(ch[i+1]-ch[i] for i in range(0,len(ch),2)),tuple(ch)))
  pending.extend({'j':j,'rect':r} for _,r in heap)
 meta=dict(meta,id=ident,accepted=accepted,pending=pending,seconds=time.monotonic()-start,complete=not pending,peak_worker_rss_bytes=rss_bytes(),min_margin=minimum,best_failed=None if best_failed==-math.inf else best_failed,**stats)
 write(f'cells/{ident}.json.gz',meta)
 return {k:v for k,v in meta.items() if k not in ('accepted','pending')}|{'outer_boxes':len(accepted),'pending_boxes':len(pending),'file':f'cells/{ident}.json.gz','sha256':hashlib.sha256((R/f'cells/{ident}.json.gz').read_bytes()).hexdigest()}

def cell_job(args):return cell(*args)
def run(args):
 gate=read('gates.json');assert gate['passed'] and gate['hashes']==hashes()
 ranges=[(8,LO[8],'2',False),(6,LO[6],'2',False),(10,'1.86','2',False),(10,LO[10],'1.86',True)]
 for n,lo,hi,five in ranges:
  tag=f'n{n}'+('-five' if five else '');certpath=f'certificate-{tag}.json'
  if (R/certpath).exists() and read(certpath)['complete']:continue
  start=time.monotonic();deadline=start+args.range_seconds;completed=[];attempts=[]
  edges=[];q=Decimal(lo);end=Decimal(hi)
  while q<end:edges.append(float(q));q=min(q+Decimal('.005'),end)
  edges.append(float(end));edges[0]=bound_decimal(lo,False);edges[-1]=bound_decimal(hi,True)
  todo=[(a,b,f'{tag}-{i:03d}') for i,(a,b) in enumerate(zip(edges,edges[1:]))];running={};hzero=h0(n)
  pool=mp.Pool(args.workers)
  def checkpoint():
   rows=sorted(completed,key=lambda r:r['Ha']);write(certpath,{'range':[edges[0],edges[-1]],'n':n,'five':five,'H0':hzero,'tail':tail(n,five),'cells':rows,'attempts':attempts,'queued':todo,'running':[list(x[:3]) for x in running.values()],'complete':not todo and not running and all(c['complete'] for c in rows),'wall_seconds':time.monotonic()-start,'hashes':hashes()})
  try:
   while (todo or running) and time.monotonic()<deadline:
    while todo and len(running)<args.workers:
     a,b,ident=todo.pop(0);meta=setup(n,a,b,five);limit=min(args.cell_seconds,max(.01,deadline-time.monotonic()-10));job=pool.apply_async(cell_job,((meta,ident,limit,args.max_outer,args.inner_budget,args.tol),));running[job]=(a,b,ident)
    checkpoint()
    done=[j for j in running if j.ready()]
    for job in done:
     a,b,ident=running.pop(job);row=job.get();log(json.dumps(row))
     if row['complete']:completed.append(row)
     elif time.monotonic()+args.cell_seconds<deadline and b-a>1e-7:
      attempts.append(row);mid=a+(b-a)*.5;todo.extend([(a,mid,ident+'a'),(mid,b,ident+'b')])
     else:completed.append(row)
     checkpoint()
    if not done:time.sleep(.2)
   # Worker jobs are always shorter than the remaining range deadline.
   for job,(a,b,ident) in list(running.items()):
    if job.ready():completed.append(job.get());del running[job]
   checkpoint()
  finally:pool.terminate();pool.join()
  log(f'RANGE {tag} complete={read(certpath)["complete"]} wall={time.monotonic()-start:.6f}')

def coverage(intervals,lo,hi):
 rows=sorted(intervals);end=lo
 for l,u in rows:
  assert l==end and u>l,(l,u,end);end=u
 assert end==hi,(end,hi)
def partition(rects,yr,five):
 if not five:coverage([r for r in rects],*yr);return
 xs=sorted(set(yr+[x for r in rects for x in r[:2]]))
 for a,b in zip(xs,xs[1:]):coverage([r[2:] for r in rects if r[0]<=a and r[1]>=b],*yr)
def replay_cell(row):
 assert hashlib.sha256((R/row['file']).read_bytes()).hexdigest()==row['sha256'];c=read(row['file']);fresh=setup(c['n'],c['Ha'],c['Hb'],c['five'],stored=c)
 for k in fresh:assert fresh[k]==c[k],k
 for j in ([1] if c['five'] else blocks(c['n'])):
  _,yr=domains(c['n'],j,c['five']);partition([list(r['rect']) for r in c['accepted']+c['pending'] if r['j']==j],yr,c['five'])
 minimum=math.inf
 for outer in c['accepted']:
  rect=outer['rect'];rr,_=domains(c['n'],outer['j'],c['five']);ys=rect if c['five'] else rect+[0.,0.];regions=pieces(c,rr,rect);bounds={}
  assert hashlib.sha256((R/outer['inner_file']).read_bytes()).hexdigest()==outer['inner_sha256']
  for rec in read(outer['inner_file']):
   r=rec['range'];coverage(rec['leaves'],*r);v=math.inf
   for l,u in rec['leaves']:
    assert l>=0 or u<=0
    v=min(v,LIB.leaf_bound(l,u,*rec['ys'],rec['h'],c['n'],outer['j'],rec['side'],int(c['five'])))
   assert v==rec['lower'];bounds[(rec['h'],rec['side'],*r,*rec['ys'])]=v
  margin=math.inf
  for h,u in zip((c['Ha'],c['Hb']),c['U']):
   for reg in regions:
    vals=[]
    for side,r in enumerate(reg):
     yy=ys if c['five'] and side==1 else (ys[:2]+[0.,0.] if side==0 or not c['five'] else ys[2:]+[0.,0.])
     vals.append(bounds[(h,side,*r,*yy)])
    margin=min(margin,DN(LIB.assemble((D*len(vals))(*vals),len(vals),*ys,h,int(c['five']))-u))
  assert margin>0 and margin==outer['margin'];minimum=min(minimum,margin)
 return {'id':c['id'],'outer_boxes':len(c['accepted']),'pending_boxes':len(c['pending']),'min_margin':None if minimum==math.inf else minimum,'complete':c['complete'],'replay':'PASS','partition':'PASS'}
def verify(args):
 start=time.monotonic();allresults=[]
 for path in sorted(R.glob('certificate-n*.json')):
  c=read(path.name);assert c['hashes']==hashes();assert c['H0']==h0(c['n'],c['H0']['T_hat']);assert c['tail']==tail(c['n'],c['five'])
  if c['complete']:coverage([(r['Ha'],r['Hb']) for r in c['cells']],*c['range'])
  with mp.Pool(args.workers) as pool:
   for r in pool.imap_unordered(replay_cell,c['cells']):allresults.append(r);log(json.dumps(r),'verification.log')
 write('verification.json',{'cells':allresults,'seconds':time.monotonic()-start,'hashes':hashes()})
def report(args):
 rows=[]
 for p in sorted(R.glob('certificate-n*.json')):
  c=read(p.name);cells=c['cells'];ranges=[]
  for r in sorted([r for r in cells if r['complete']],key=lambda r:r['Ha']):
   if ranges and ranges[-1][1]==r['Ha']:ranges[-1][1]=r['Hb']
   else:ranges.append([r['Ha'],r['Hb']])
  rows.append({'run':p.stem,'cells':len([r for r in cells if r['complete']]),'outer':sum(r['outer_boxes'] for r in cells),'inner':sum(r['inner_boxes'] for r in cells),'min_margin':min([r['min_margin'] for r in cells if r['min_margin'] is not None],default=None),'ranges':ranges,'seconds':c['wall_seconds'],'complete':c['complete']})
 write('report.json',rows);print(json.dumps(rows,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['gates','run','verify','report']);p.add_argument('--workers',type=int,default=6);p.add_argument('--range-seconds',type=float,default=10800);p.add_argument('--cell-seconds',type=float,default=180);p.add_argument('--max-outer',type=int,default=200000);p.add_argument('--inner-budget',type=int,default=2047);p.add_argument('--tol',type=float,default=2e-5);a=p.parse_args();assert 1<=a.workers<=6;assert 0<a.range_seconds<=10800
 if a.mode=='gates':
  import gates;gates.main(a)
 else:{'run':run,'verify':verify,'report':report}[a.mode](a)
