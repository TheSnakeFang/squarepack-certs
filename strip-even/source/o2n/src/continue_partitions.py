"""Continue saved five-block partitions verbatim, without discarding proven boxes.
Optional exact-key memoization stores compact copies of deterministic inner results.
"""
import argparse,array,functools,hashlib,heapq,itertools,json,multiprocessing as mp,pathlib,shutil,time
import driver as d
_REAL=None
@functools.lru_cache(maxsize=2048)
def _cached(n,j,side,five,rr,ys,h,budget,tol):
 v,count,leaves=_REAL(n,j,side,five,rr,ys,h,budget,tol,True)
 packed=array.array('d',itertools.chain.from_iterable(leaves)).tobytes()
 return v,count,packed

def cached_inner(n,j,side,five,rr,ys,h,budget,tol,trace=False):
 v,count,packed=_cached(n,j,side,five,tuple(rr),tuple(ys),h,budget,tol)
 if trace:
  a=array.array('d');a.frombytes(packed);leaves=[[a[i],a[i+1]] for i in range(0,len(a),2)]
 else:leaves=[]
 return v,count,leaves

def init():
 global _REAL
 _REAL=d.inner;d.inner=cached_inner

def work(job):
 path,limit=job;meta=d.read(path);assert meta['five'];start=time.monotonic()
 accepted=meta['accepted'];heap=[(-((r['rect'][1]-r['rect'][0])*(r['rect'][3]-r['rect'][2])),tuple(r['rect'])) for r in meta['pending']];heapq.heapify(heap)
 tested=meta['outer_tested'];inner=meta['inner_boxes'];minimum=meta['min_margin'];best=meta['best_failed']
 while heap and time.monotonic()-start<limit and d.rss_bytes()<230*1024**2:
  _,rect=heapq.heappop(heap);v,k,_=d.evaluate(meta,1,rect,511,.00002);tested+=1;inner+=k
  if v>0:
   v,k,trace=d.evaluate(meta,1,rect,511,.00002,True);assert v>0;inner+=k
   leafpath=f'cells/{meta["id"]}-leaves/{len(accepted):07d}.json.gz';d.write(leafpath,trace)
   accepted.append({'j':1,'rect':rect,'margin':v,'inner_file':leafpath,'inner_sha256':hashlib.sha256((d.R/leafpath).read_bytes()).hexdigest()});minimum=v if minimum is None else min(minimum,v)
  else:
   best=v if best is None else max(best,v);i=0 if rect[1]-rect[0]>=rect[3]-rect[2] else 2;m=rect[i]+(rect[i+1]-rect[i])*.5
   if m==rect[i] or m==rect[i+1]:heapq.heappush(heap,(0,rect));break
   for lo,hi in ((rect[i],m),(m,rect[i+1])):
    child=list(rect);child[i:i+2]=[lo,hi];heapq.heappush(heap,(-((child[1]-child[0])*(child[3]-child[2])),tuple(child)))
 meta.update(accepted=accepted,pending=[{'j':1,'rect':r} for _,r in heap],outer_tested=tested,inner_boxes=inner,min_margin=minimum,best_failed=best,seconds=meta['seconds']+time.monotonic()-start,complete=not heap,peak_worker_rss_bytes=max(meta['peak_worker_rss_bytes'],d.rss_bytes()),memoization='2048 exact-key packed inner partitions; counts include cache hits')
 d.write(path,meta)
 return {k:v for k,v in meta.items() if k not in ('accepted','pending')}|{'outer_boxes':len(accepted),'pending_boxes':len(heap),'file':path,'sha256':hashlib.sha256((d.R/path).read_bytes()).hexdigest()}

def main():
 p=argparse.ArgumentParser();p.add_argument('manifest');p.add_argument('cells',nargs='+');a=p.parse_args();c=d.read(a.manifest);assert c['hashes']==d.hashes() and d.read('gates.json')['hashes']==d.hashes()
 selected=[]
 for path in a.cells:
  m=d.read(path);selected.append((m['Ha'],m['Hb']))
 d.coverage(selected,*c['range'])
 # Preserve old partial manifests, including their hashes, before extending them.
 for row in c['attempts']:
  if row['file'] in a.cells:
   old=row['file'];new='cells/archive-'+pathlib.Path(old).name;shutil.copyfile(d.R/old,d.R/new);row['file']=new
 previous=c['wall_seconds'];start=time.monotonic();deadline=start+max(0,10800-previous-60);done=[];running={};todo=list(a.cells)
 def checkpoint():
  c.update(cells=sorted(done,key=lambda r:r['Ha']),queued=todo,running=list(running.values()),complete=not todo and not running and all(x['complete'] for x in done),wall_seconds=previous+time.monotonic()-start,continue_source_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest())
  d.write(a.manifest,c)
 pool=mp.Pool(6,initializer=init)
 try:
  while (todo or running) and time.monotonic()<deadline:
   while todo and len(running)<6:
    path=todo.pop(0);running[pool.apply_async(work,((path,max(.01,deadline-time.monotonic()-10)),))]=path
   checkpoint();ready=[r for r in running if r.ready()]
   for r in ready:
    path=running.pop(r);result=r.get();done.append(result);d.log(json.dumps(result));checkpoint()
   if not ready:time.sleep(.25)
  checkpoint()
 finally:pool.terminate();pool.join()
 d.log(f'CONTINUED PARTITIONS complete={c["complete"]} total_wall_seconds={c["wall_seconds"]}')
if __name__=='__main__':main()
