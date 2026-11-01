#!/usr/bin/env python3
"""
D1 -- r-space CORNER certificate.  NINE 1-D/2-D interval conditions, no 5-D search.

THEOREM.  H in [1.87,2], c=1-H/2, T=tan(acos rho(H)) with a(rho(H))=H, mu=cT/2,
r*=(T,-1/T,T,-1/T,T).  If (A1)-(A9) hold then
      Psi(r;H) >= F6(H)   for every r with |r_i-r*_i| <= R_C,  i=1..5.

  XI=[T-R_C,T+R_C], UI=[1/T-R_C,1/T+R_C];  x in XI (odd slot), u in UI (= -r_even),
  W=1-xu, Rx=sqrt(1+x^2), Ru=sqrt(1+u^2), lam(z)=(H sqrt(1+z^2)-(2+z))/(2 z sqrt(1+z^2)),
  B_end=1+c(x+u), B_X=A(x)+lam(x)W+|W|/(2Rx), B_Y=A(u)+lam(u)W+|W|/(2Ru),
  A(z)=(z+1/z)(P(z)-H/2),  Dmax := (1/x_lo)*sup{|A'(z;H)| : z in [1/x_hi,1/x_lo] u UI}.

  The four pair targets are  A(x)+mu W  (pairs 1,4)  and  A(u)  (pairs 2,3), with
  mu forced by grad Phi(r*)=0.  Each target needs all THREE candidates, giving

  (A1) A''(z;H) >= mu                                 z in XI u UI  [Phi convex]
  (A2) lam(x)-1/(2Rx) <= mu <= lam(x)+1/(2Rx)         x in XI   [B_X vs A(x)+muW]
  (A3) |lam(u)| <= 1/(2Ru)                            u in UI   [B_Y vs A(u)]
  (A4) Dmax <= min_{u,H}(lam(u)+1/(2Ru)) - mu_hi             [B_Y vs A(x)+muW, W>0]
  (A5) max A(x) <= 1+c_lo(x_lo+u_lo) - mu_hi(1-x_lo u_lo)     [B_end vs A(x)+muW]
  (A6) max A(u) <= 1+c_lo(x_lo+u_lo)                          [B_end vs A(u)]
  (A7) K(x,u;H) >= 0 on {W >= 0}, K := A[1/x,u] + H/2 - 1/Rx  [B_X vs A(u), W>0]
  (A8) 1/(2Ru) + mu_lo - lam(u) >= Dmax                        [B_Y vs A(x)+muW, W<0]
  (A9) Dmax + max lam(x) <= min 1/(2Rx)                        [B_X vs A(u),    W<0]
Rerun:  python3 run_corner.py [R_C]        log: corner-cert.log
"""
import math, sys, time
from iv import (I, C, add, sub, mul, div, neg, ab, sq, sqrt_i,
                A_f, d1A_f, d2A_f, lam_f, T_enclosure, a_prime_negative_ok)
from a7 import scan7, D0 as D0A7
from iv import grid, down, up as round_up
import json
from decimal import Decimal

RC = float(sys.argv[1]) if len(sys.argv) > 1 else 0.32
NH = 52; NB = 240; NG7 = 12
H0,H1 = 1.87, 2.0

def sc(f, xI, HI, nb=NB, get='lo'):
    best=None; n=0
    for k in range(nb):
        x=I(grid(xI,k,nb), grid(xI,k+1,nb))
        v=f(x,HI); w=v.lo if get=='lo' else v.hi
        best=w if best is None else (min(best,w) if get=='lo' else max(best,w)); n+=1
    return best,n

def main():
    t0=time.time(); log=open('corner-cert.log','w')
    def Wr(s):
        print(s); log.write(s+"\n"); log.flush()
    Wr("D1 CORNER CERTIFICATE  run_corner.py   R_C=%.3f   H in [%.2f,%.2f]   H-cells=%d"%(RC,H0,H1,NH))
    sup_ap=a_prime_negative_ok()
    Wr("sup a'(rho) on [1/sqrt2,0.75] = %.6f  (<0 required; a(1/sqrt2)=2, a(0.75)=1.840086<1.87)"%sup_ap)
    assert sup_ap<0, "monotonicity precondition for the T enclosure failed; refusing to certify"
    Wr("(A7) regimes: divided difference for (1/x-u) >= %.2f, midpoint Taylor below"%D0A7)
    hdr=("H-cell                 T-cell               |    A1      A2      A3      A4      A5      A6      A7      A8      A9  |  boxes  status")
    Wr(""); Wr(hdr); Wr("-"*len(hdr))
    gm={}; tot=0; nopen=0; rows=[]
    KEYS=('A1','A2','A3','A4','A5','A6','A7','A8','A9')
    for hc in range(NH):
        Hl=down(float(Decimal("1.87")+Decimal(".13")*hc/NH)); Hh=round_up(float(Decimal("1.87")+Decimal(".13")*(hc+1)/NH)); Hh=min(Hh,2.0); HI=I(Hl,Hh)
        TI=T_enclosure(HI); Tlo,Thi=TI.lo,TI.hi
        XI=add(TI,I(-round_up(RC),round_up(RC))); UI=add(div(I(1.0),TI),I(-round_up(RC),round_up(RC)))
        cI=sub(C(1.0),mul(HI,C(0.5))); clo=cI.lo
        muI=div(mul(cI,TI),C(2.0)); muhi=muI.hi; mulo=muI.lo
        if XI.lo<=0.0 or UI.lo<=0.0:
            Wr("H[%.4f,%.4f]  R_C too large (window reaches 0)"%(Hl,Hh)); nopen+=1; continue
        n=0; M={}
        f1=lambda z,H: sub(d2A_f(z,H),C(muhi))
        a,nn=sc(f1,XI,HI); n+=nn; b,nn=sc(f1,UI,HI); n+=nn; M['A1']=min(a,b)
        up=lambda x,H: sub(add(lam_f(x,H),div(C(1.0),mul(C(2.0),sqrt_i(add(C(1.0),sq(x)))))),C(muhi))
        lo=lambda x,H: sub(C(mulo),sub(lam_f(x,H),div(C(1.0),mul(C(2.0),sqrt_i(add(C(1.0),sq(x)))))))
        a,nn=sc(up,XI,HI); n+=nn; b,nn=sc(lo,XI,HI); n+=nn; M['A2']=min(a,b)
        f3=lambda u,H: sub(div(C(1.0),mul(C(2.0),sqrt_i(add(C(1.0),sq(u))))),ab(lam_f(u,H)))
        M['A3'],nn=sc(f3,UI,HI); n+=nn
        # Dmax
        Lp,nn=sc(lambda z,H: ab(d1A_f(z,H)), div(I(1.0),XI), HI, get='hi'); n+=nn
        Lq,nn=sc(lambda z,H: ab(d1A_f(z,H)), UI, HI, get='hi'); n+=nn
        Dmax=div(I(max(Lp,Lq)),I(XI.lo)).hi
        g4,nn=sc(lambda u,H: sub(add(lam_f(u,H),div(C(1.0),mul(C(2.0),sqrt_i(add(C(1.0),sq(u)))))),C(muhi)),UI,HI); n+=nn
        M['A4']=sub(I(g4),I(Dmax)).lo
        Ax,nn=sc(lambda x,H: A_f(x,H), XI, HI, get='hi'); n+=nn
        Au,nn=sc(lambda u,H: A_f(u,H), UI, HI, get='hi'); n+=nn
        end=add(I(1.0),mul(I(clo),add(I(XI.lo),I(UI.lo))))
        M['A5']=sub(sub(end,mul(I(muhi),sub(I(1.0),mul(I(XI.lo),I(UI.lo))))),I(Ax)).lo
        M['A6']=sub(end,I(Au)).lo
        # (A7) : 2-D scan over XI x UI, W = 1-xu >= 0
        inv=div(I(1.0),XI); win=I(min(inv.lo,UI.lo),max(inv.hi,UI.hi)); M2g=0.0
        for k in range(60):
            w=I(grid(win,k,60), grid(win,k+1,60))
            M2g=max(M2g, ab(d2A_f(w,HI)).hi)
        ok7=True; m7=None; n7=0
        for a_ in range(NG7):
            xI=I(grid(XI,a_,NG7), grid(XI,a_+1,NG7))
            for b_ in range(NG7):
                uI=I(grid(UI,b_,NG7), grid(UI,b_+1,NG7))
                ok,m,nn=scan7(xI,uI,HI,M2g); ok7&=ok; n7+=nn
                m7=m if m7 is None else min(m7,m)
        n+=n7; M['A7']=-1e9 if not ok7 else (m7 if m7 is not None else 9e9)
        g8,nn=sc(lambda u,H: sub(add(div(C(1.0),mul(C(2.0),sqrt_i(add(C(1.0),sq(u))))),C(mulo)),lam_f(u,H)),UI,HI); n+=nn
        M['A8']=sub(I(g8),I(Dmax)).lo
        lmax,nn=sc(lambda x,H: lam_f(x,H), XI, HI, get='hi'); n+=nn
        rmin,nn=sc(lambda x,H: div(C(1.0),mul(C(2.0),sqrt_i(add(C(1.0),sq(x))))), XI, HI); n+=nn
        M['A9']=sub(I(rmin),add(I(Dmax),I(lmax))).lo
        ms=[M[k] for k in KEYS]; bad=min(ms)<=0.0
        Wr("H[%.4f,%.4f] [%.6f,%.6f] |"%(Hl,Hh,Tlo,Thi)+"".join(" %+.4f"%v for v in ms)
           +" | %6d  %s"%(n,"OPEN" if bad else "PASS"))
        for k,v in zip(KEYS,ms): gm[k]=min(gm.get(k,9e9),v)
        tot+=n; nopen += 1 if bad else 0
        rows.append({"Ha":Hl,"Hb":Hh,"T":[Tlo,Thi],"margins":M,"boxes":n,"passed":not bad})
    Wr("")
    Wr("SUMMARY  R_C=%.3f  H-cells=%d  interval boxes=%d  OPEN=%d  time=%.1fs"%(RC,NH,tot,nopen,time.time()-t0))
    Wr("global min margins: "+"  ".join("%s=%+.5f"%(k,gm[k]) for k in KEYS))
    Wr("VERDICT: "+(("CERTIFIED  Psi(r;H) >= F6(H) for all |r-r*(H)|_inf <= %.3f, H in [1.87,2]"%RC)
                    if nopen==0 else "NOT CERTIFIED at R_C=%.3f (%d open H-cells)"%(RC,nopen)))
    log.close(); open("corner_certificate.json","w").write(json.dumps({"cells":rows,"minimum_margins":gm,"boxes":tot,"open":nopen,"seconds":time.time()-t0},indent=2)+"\n"); return nopen

if __name__=='__main__': sys.exit(0 if main()==0 else 1)
