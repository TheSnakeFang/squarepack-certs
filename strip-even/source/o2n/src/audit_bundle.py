"""Final range/provenance/no-search checks in addition to the full replay."""
import json,pathlib,time,hashlib,inspect
from fractions import Fraction
import driver as d

# For fixed z, B(z; H) - U(H) is affine in H: B depends on H only
# through k=2-H (Lemma 19(c)), and U uses one fixed rational T_hat.
# Thus strict positivity at both H endpoints proves positivity throughout
# the cell. The common coordinate domain uses the fixed c cap, which
# contains the clipped domain at every H in the cell.
def main():
 start=time.monotonic();g=d.read('gates.json');assert g['passed'] and g['hashes']==d.hashes()
 assert all(r['violations']==0 for r in g['results'].values())
 s=d.read('supplemental-gates.json');assert s['hashes']==d.hashes()
 assert s['combined_random_H_per_n']==300 and s['legacy_G1_dual_hull']['violations']==0
 assert (d.R/'src/kernel.c').read_bytes()==(d.R/'src/o2cert_kernel_reference.c').read_bytes()
 expected={'n8':('1.852049','2'), 'n6':('1.861098','2'), 'n10':('1.86','2'), 'n10-five':('1.846936','1.86')}
 results=[]
 def forbidden(*a,**k):raise AssertionError('Verifier attempted a root or inner search')
 d.root=forbidden;d.inner=forbidden
 for tag,(lo,hi) in expected.items():
  c=d.read(f'certificate-{tag}.json');assert c['complete'] and not c['queued'] and not c['running']
  assert c['hashes']==d.hashes()
  if 'continue_source_sha256' in c:
   assert c['continue_source_sha256']==hashlib.sha256((d.R/'src/continue_partitions.py').read_bytes()).hexdigest()
   cg=d.read('cache-gate.json');assert cg['violations']==0 and cg['core_hashes']==d.hashes() and cg['source_sha256']==c['continue_source_sha256']
  if 'resume_source_sha256' in c:assert c['resume_source_sha256']==hashlib.sha256((d.R/'src/resume_range.py').read_bytes()).hexdigest()
  assert all(row['complete'] and row['pending_boxes']==0 for row in c['cells'])
  assert Fraction(c['range'][0])<=Fraction(lo) and Fraction(c['range'][1])>=Fraction(hi)
  d.coverage([(r['Ha'],r['Hb']) for r in c['cells']],*c['range'])
  assert min(c['cells'],key=lambda r:r['Ha'])['U'][0]<0
  assert c['H0']==d.h0(c['n'],c['H0']['T_hat']);assert c['tail']==d.tail(c['n'],c['five'])
  # The full replay already evaluated every leaf. Exercise every parameter
  # check with searches disabled, without duplicating those numerical loops.
  for row in c['cells']:
   fresh=d.setup(row['n'],row['Ha'],row['Hb'],row['five'],stored=row)
   assert all(fresh[k]==row[k] for k in fresh)
  replay_source=inspect.getsource(d.replay_cell)
  assert all(call not in replay_source for call in ('block_inner(', 'inner(', 'root(', 'evaluate('))
  results.append({'run':tag,'requested_rational_range':[lo,hi],'no_search_guard':'PASS','cells':len(c['cells']),'minimum_cY':min(z['min_cY'] for row in c['cells'] for z in row['Loc'])})
 v=d.read('verification.json');assert v['hashes']==d.hashes() and all(r['complete'] and r['pending_boxes']==0 and r['replay']=='PASS' and r['partition']=='PASS' for r in v['cells'])
 assert len(v['cells'])==sum(r['cells'] for r in results)
 d.write('bundle-audit.json',{'passed':True,'rows':results,'seconds':time.monotonic()-start,'hashes':d.hashes()})
 print(json.dumps({'bundle_audit':'PASS','rows':results,'seconds':time.monotonic()-start}))
if __name__=='__main__':main()
