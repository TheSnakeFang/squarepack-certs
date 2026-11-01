"""Continue a partial range, preserving completed cells and cumulative budget."""
import argparse,hashlib,multiprocessing as mp,time
import driver as d

def main():
 p=argparse.ArgumentParser();p.add_argument('manifest');p.add_argument('--cell-seconds',type=float,default=1800);a=p.parse_args()
 c=d.read(a.manifest);assert c['hashes']==d.hashes();assert d.read('gates.json')['passed'] and d.read('gates.json')['hashes']==d.hashes()
 start=time.monotonic();previous=c['wall_seconds'];deadline=start+max(0,10800-previous-2)
 done=[r for r in c['cells'] if r['complete']];attempts=list(c['attempts']);todo=list(c['queued'])+list(c['running'])
 for r in c['cells']:
  if not r['complete']:attempts.append(r);m=(r['Ha']+r['Hb'])/2;todo.extend([[r['Ha'],m,r['id']+'a'],[m,r['Hb'],r['id']+'b']])
 assert len(set((a,b,i) for a,b,i in todo))==len(todo)
 running={};pool=mp.Pool(6)
 def checkpoint():
  c.update(cells=sorted(done,key=lambda r:r['Ha']),attempts=attempts,queued=todo,running=list(running.values()),wall_seconds=previous+time.monotonic()-start,complete=not todo and not running and all(r['complete'] for r in done),resume_source_sha256=hashlib.sha256(open(__file__,'rb').read()).hexdigest())
  d.write(a.manifest,c)
 try:
  while (todo or running) and time.monotonic()<deadline:
   while todo and len(running)<6:
    lo,hi,ident=todo.pop(0);meta=d.setup(c['n'],lo,hi,c['five']);seconds=min(a.cell_seconds,max(.01,deadline-time.monotonic()-10));job=pool.apply_async(d.cell_job,((meta,ident,seconds,500000,511,.00002),));running[job]=[lo,hi,ident]
   checkpoint();ready=[j for j in running if j.ready()]
   for job in ready:
    lo,hi,ident=running.pop(job);r=job.get();d.log(__import__('json').dumps(r));
    if r['complete']:done.append(r)
    elif time.monotonic()+30<deadline and hi-lo>1e-7:
     attempts.append(r);m=(lo+hi)/2;todo.extend([[lo,m,ident+'a'],[m,hi,ident+'b']])
    else:done.append(r)
    checkpoint()
   if not ready:time.sleep(.25)
  checkpoint()
 finally:pool.terminate();pool.join()
 d.log(f'RESUMED RANGE complete={c["complete"]} total_wall_seconds={c["wall_seconds"]}')
if __name__=='__main__':main()
