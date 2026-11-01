"""Outward-rounded interval arithmetic + the 1-D functions of the corner certificate.
Self-contained; all ops round outward with math.nextafter."""
import math

class I:
    __slots__=('lo','hi')
    def __init__(self,lo,hi=None):
        self.lo=float(lo); self.hi=float(lo if hi is None else hi)
        assert self.lo <= self.hi
    def __repr__(self): return "[%.9g,%.9g]"%(self.lo,self.hi)
def C(x):
    r=I(0.0); r.lo=math.nextafter(float(x),-math.inf); r.hi=math.nextafter(float(x),math.inf); return r
def add(a,b): return I(math.nextafter(a.lo+b.lo,-math.inf),math.nextafter(a.hi+b.hi,math.inf))
def sub(a,b): return I(math.nextafter(a.lo-b.hi,-math.inf),math.nextafter(a.hi-b.lo,math.inf))
def neg(a): return I(-a.hi,-a.lo)
def mul(a,b):
    p=(a.lo*b.lo,a.lo*b.hi,a.hi*b.lo,a.hi*b.hi)
    return I(math.nextafter(min(p),-math.inf),math.nextafter(max(p),math.inf))
def div(a,b):
    if b.lo<=0.0<=b.hi: raise ZeroDivisionError("interval divisor contains 0")
    p=(a.lo/b.lo,a.lo/b.hi,a.hi/b.lo,a.hi/b.hi)
    return I(math.nextafter(min(p),-math.inf),math.nextafter(max(p),math.inf))
def ab(a):
    if a.lo>=0.0: return I(a.lo,a.hi)
    if a.hi<=0.0: return I(-a.hi,-a.lo)
    return I(0.0,max(-a.lo,a.hi))
def sq(a): return mul(a,a)
def sqrt_i(a):
    assert a.lo>=0.0
    return I(pad(math.sqrt(a.lo),False),pad(math.sqrt(a.hi),True))
def acos_i(a):
    return I(pad(math.acos(min(1.0,a.hi)),False),pad(math.acos(max(-1.0,a.lo)),True))
def tan_i(a):
    return I(pad(math.tan(a.lo),False),pad(math.tan(a.hi),True))
def hull(a,b): return I(min(a.lo,b.lo),max(a.hi,b.hi))

# ---------- a(rho) = 2(1-rho^2-2rho^3+2(1-rho^2)^{3/2})/(3-5rho^2)   [exact extremal value] ----------
def a_f(rho):
    """a(rho) = 2*(1-rho^2-2 rho^3+2 (1-rho^2)^{3/2})/(3-5 rho^2)"""
    r2=sq(rho); t=sqrt_i(sub(C(1.0),r2)); t3=mul(sq(t),t)
    num=add(sub(sub(C(1.0),r2),mul(C(2.0),mul(r2,rho))),mul(C(2.0),t3))
    den=sub(C(3.0),mul(C(5.0),r2))
    return mul(C(2.0),div(num,den))
def da_f(rho):
    """a'(rho) as an interval enclosure (symbolic derivative)."""
    r2=sq(rho); t=sqrt_i(sub(C(1.0),r2))
    num=sub(sub(C(1.0),r2),mul(C(2.0),mul(r2,rho)))
    num=add(num,mul(C(2.0),mul(sq(t),t)))
    den=sub(C(3.0),mul(C(5.0),r2))
    # N = num, D = den ;  N' = -2rho -6rho^2 - 6 rho t   ;  D' = -10 rho
    dnum=sub(sub(neg(mul(C(2.0),rho)),mul(C(6.0),r2)),mul(C(6.0),mul(rho,t)))
    dden=neg(mul(C(10.0),rho))
    return mul(C(2.0),div(sub(mul(dnum,den),mul(num,dden)),sq(den)))

# ---------- arc profile and its derivatives ----------
def Pf(z):                       # P(z) = (1+z)/sqrt(1+z^2)
    return div(add(C(1.0),z),sqrt_i(add(C(1.0),sq(z))))
def A_f(z,H):
    return mul(add(z,div(C(1.0),z)),sub(Pf(z),mul(H,C(0.5))))
def d1A_f(z,H):
    R2=add(C(1.0),sq(z)); R=sqrt_i(R2)
    Pp=div(sub(C(1.0),z),mul(R2,R))
    return add(mul(sub(C(1.0),div(C(1.0),sq(z))),sub(Pf(z),mul(H,C(0.5)))),mul(add(z,div(C(1.0),z)),Pp))
def d2A_f(z,H):
    R2=add(C(1.0),sq(z)); R=sqrt_i(R2); R3=mul(R2,R); R5=mul(R3,R2)
    Pp=div(sub(C(1.0),z),R3)
    Ppp=sub(div(C(-1.0),R3),div(mul(C(3.0),mul(z,sub(C(1.0),z))),R5))
    t1=mul(div(C(2.0),mul(sq(z),z)),sub(Pf(z),mul(H,C(0.5))))
    t2=mul(C(2.0),mul(sub(C(1.0),div(C(1.0),sq(z))),Pp))
    t3=mul(add(z,div(C(1.0),z)),Ppp)
    return add(add(t1,t2),t3)

# ---------- the three exact B-candidates for x>0>y, u=-y>0 ----------
def lam_f(z,H):                  # lam_X = (H*R-(2+z))/(2 z R)
    R=sqrt_i(add(C(1.0),sq(z)))
    return div(sub(mul(H,R),add(C(2.0),z)),mul(C(2.0),mul(z,R)))
def Bend_f(x,u,H):
    c=sub(C(1.0),mul(H,C(0.5)))
    return add(C(1.0),mul(c,add(x,u)))
def BX_f(x,u,H):
    Rx=sqrt_i(add(C(1.0),sq(x))); S=add(x,u); W=sub(C(1.0),mul(x,u))
    return sub(div(add(add(sq(Rx),mul(S,add(C(2.0),x))),ab(W)),mul(C(2.0),Rx)),mul(mul(H,C(0.5)),S))
def BY_f(x,u,H):
    Ru=sqrt_i(add(C(1.0),sq(u))); S=add(x,u); W=sub(C(1.0),mul(x,u))
    return sub(div(add(add(sq(Ru),mul(S,add(C(2.0),u))),ab(W)),mul(C(2.0),Ru)),mul(mul(H,C(0.5)),S))

# ---------- rigorous T(H) = tan(acos rho(H)),  a(rho(H)) = H ----------
def a_prime_negative_ok():
    lo,hi=pad(math.sqrt(0.5),False),0.75
    worst=-1e9
    for k in range(200):
        r=I(grid(I(lo,hi),k,200),grid(I(lo,hi),k+1,200))
        v=da_f(r); worst=max(worst,v.hi)
    return worst
def T_enclosure(Hcell):
    """Rigorous T = tan(acos rho) for all H in Hcell, using a strictly decreasing on
    [1/sqrt2, 0.75] (checked by a_prime_negative_ok).  a(1/sqrt2)=2 and a(0.75)<1.87."""
    r1,r2=pad(math.sqrt(0.5),False),0.75
    for _ in range(120):
        if r2-r1<1e-14: break
        m=0.5*(r1+r2); am=a_f(C(m))
        if am.lo>Hcell.hi: r1=m
        elif am.hi<Hcell.lo: r2=m
        else: break
    return tan_i(acos_i(I(r1,r2)))

# Endpoints of subdivisions are shared binary64 numbers: interpolation need
# not round outward internally, but the first and last must be exact parents.
def grid(a,k,n):
    return a.lo if k==0 else a.hi if k==n else a.lo+(a.hi-a.lo)*k/n
def pad(x,positive):
    for _ in range(8): x=math.nextafter(x, math.inf if positive else -math.inf)
    return x
def down(x): return math.nextafter(x,-math.inf)
def up(x): return math.nextafter(x,math.inf)
