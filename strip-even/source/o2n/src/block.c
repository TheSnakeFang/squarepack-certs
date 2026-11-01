/* The refereed candidate and centred-form implementation is copied verbatim. */
#include "kernel.c"
static I dd(I t,int order){
 I one=pt(1),w=add(t,divi(one,t)),p=root(mul(w,add(w,pt(2))));
 if(order==0)return sub(add(one,w),p);
 I a=sub(one,divi(one,sq(t)));
 if(order==1)return neg(divi(a,mul(p,add(add(p,w),one))));
 return sub(divi(sq(a),mul(sq(p),p)),divi(pt(2),mul(mul(sq(t),t),mul(p,add(add(p,w),one)))));
}
void d_interval(double lo,double hi,int order,double*out){I v=dd(iv(lo,hi),order);out[0]=v.l;out[1]=v.u;}
static I fn(int n,I t,I h){int m=n/2;return sub(add(pt(n),mul(sub(pt(2),h),add(mul(pt(m),t),divi(pt(m-1),t)))),mul(pt(n-2),dd(t,0)));}
void f_interval(int n,double lo,double hi,double ha,double hb,int deriv,double*out){I t=iv(lo,hi),h=iv(ha,hb);I v=deriv?sub(mul(sub(pt(2),h),sub(pt(n/2),divi(pt(n/2-1),sq(t)))),mul(pt(n-2),dd(t,1))):fn(n,t,h);out[0]=v.l;out[1]=v.u;}
static I psi_i(I x){return sub(pt(1),divi(pt(1),root(add(pt(1),sq(x)))));}
static I q_i(I x){return divi(add(pt(1),x),root(add(pt(1),sq(x))));}
/* slacks: containment, J, N1, N1', N2', N3, L, minimum cY.
   Coefficients are intervals on the independent T,H rectangle. */
void local_check(double tl,double th,double ha,double hb,double ratio,double xl,double xu,double yl,double yu,double*out){
 I t=iv(tl,th),cx=mul(sub(pt(2),iv(ha,hb)),pt(ratio));
 /* ratio is itself enclosed, since e.g. 1/3 is not binary-exact. */
 cx=mul(sub(pt(2),iv(ha,hb)),iv(dn(ratio),up(ratio)));
 if(ha==hb&&ha==2)cx=pt(0);
 I cy=mul(sq(t),sub(cx,dd(t,1))),ell=sub(add(mul(cx,t),divi(cy,t)),dd(t,0));
 I corner=add(mul(cx,pt(xl)),iv(fmin(mul(cy,pt(yl)).l,mul(cy,pt(yu)).l),fmax(mul(cy,pt(yl)).u,mul(cy,pt(yu)).u)));
 double jl=fmin(xl,divi(pt(1),pt(yu)).l),ju=fmax(xu,divi(pt(1),pt(yl)).u);
 out[0]=fmin(fmin(dn(tl-xl),dn(xu-th)),fmin(dn(divi(pt(1),pt(th)).l-yl),dn(yu-divi(pt(1),pt(tl)).u)));
 out[1]=fmin(dn(jl-.5),dn(1.5-ju));out[2]=sub(psi_i(pt(xl)),cy).l;out[3]=sub(psi_i(pt(yl)),cx).l;
 out[4]=sub(corner,ell).l;out[5]=sub(cy,sub(pt(1),pt(fmin(q_i(pt(xl)).l,q_i(pt(xu)).l)))).l;
 double upper=-INFINITY;
 for(int j=0;j<256;j++){double l=j==0?jl:jl+(ju-jl)*j/256,u=j==255?ju:jl+(ju-jl)*(j+1)/256;I z=iv(l,u);upper=fmax(upper,mul(mul(mul(sq(z),z),dd(z,2)),pt(.5)).u);}
 out[6]=sub(cy,pt(upper)).l;out[7]=cy.l;
}
static I scoef(double h,int n,int j,int side,int wrong){
 int m=n/2,num=side?(wrong?m-1-j:j):(wrong?j-1:m-j);
 return mul(sub(pt(2),pt(h)),divi(pt(num),pt(m-1)));
}
static I s_plain(I x,I y,I w,double h,int n,int j,int side,int five){
 I v=iv(alower(x,neg(y)),candidate(x,neg(y)).u);
 if(five&&side==1){v=add(v,iv(alower(x,neg(w)),candidate(x,neg(w)).u));return sub(sub(v,pt(2)),mul(pt(h),x));}
 I c=five?mul(sub(pt(2),pt(h)),pt(side==0?1:.5)):scoef(h,n,j,side, x.u<=0);
 return sub(sub(v,pt(1)),mul(sub(pt(1),c),x));
}
static double s_bound(I x,I y,I w,double h,int n,int j,int side,int five){
 assert(x.l>=0||x.u<=0);
 I v=s_plain(x,y,w,h,n,j,side,five);double a=mid(x),b=mid(y),c=mid(w),d=pad(sqrt(2),1);
 I v0=s_plain(pt(a),pt(b),pt(c),h,n,j,side,five);
 I coeff=five&&side==1?pt(h):sub(pt(1),five?mul(sub(pt(2),pt(h)),pt(side==0?1:.5)):scoef(h,n,j,side,x.u<=0));
 /* integrand x-slopes are in [0,sqrt(2)] for either sign; two A terms double this. */
 double dx=fmax(fabs(coeff.u),fabs(sub(pt((five&&side==1)?up(2*d):d),coeff).u));
 I loss=add(mul(pt(dx),pt(radius(x,a))),mul(pt(d),pt(radius(y,b))));
 if(five&&side==1)loss=add(loss,mul(pt(d),pt(radius(w,c))));
 return fmax(v.l,sub(pt(v0.l),loss).l);
}
/* Export individual leaf bounds so verify can replay stored leaves without search. */
double leaf_bound(double lo,double hi,double yl,double yu,double wl,double wu,double h,int n,int j,int side,int five){return s_bound(iv(lo,hi),iv(yl,yu),iv(wl,wu),h,n,j,side,five);}
/* Sign crossing is split before entry. Store every live leaf's endpoints. */
double block_inner(double lo,double hi,double yl,double yu,double wl,double wu,double h,int n,int j,int side,int five,int budget,double tol,double*out,int*count){
 I y=iv(yl,yu),w=iv(wl,wu);Node*a=malloc(sizeof(Node)*(budget+2));assert(a);int len=1,used=1;
 a[0]=(Node){iv(lo,hi),s_bound(iv(lo,hi),y,w,h,n,j,side,five)};double upper=INFINITY;
 while(1){int b=0;for(int i=1;i<len;i++)if(a[i].lower<a[b].lower)b=i;
 I x=a[b].x;double m=mid(x);upper=fmin(upper,s_plain(pt(m),pt(mid(y)),pt(mid(w)),h,n,j,side,five).u);
 if(used+2>budget||sub(pt(upper),pt(a[b].lower)).u<=tol||m<=x.l||m>=x.u){
 double result=a[b].lower;for(int i=0;i<len;i++){out[2*i]=a[i].x.l;out[2*i+1]=a[i].x.u;}*count=len;free(a);return result;}
 a[b]=(Node){iv(x.l,m),s_bound(iv(x.l,m),y,w,h,n,j,side,five)};
 a[len++]=(Node){iv(m,x.u),s_bound(iv(m,x.u),y,w,h,n,j,side,five)};used+=2;
 }
}
double assemble(double*vals,int count,double yl,double yu,double wl,double wu,double h,int five){I v=pt(0);for(int i=0;i<count;i++)v=add(v,pt(vals[i]));I y=iv(yl,yu);if(five)y=add(y,iv(wl,wu));return sub(v,mul(pt(h),y)).l;}
/* Fixed cap checks, evaluated once per range rather than recomputed per cell. */
void tail_check(int n,double h,double cap,int five,double*out){
 I hh=pt(h),c=root(sub(divi(pt(4),sq(hh)),pt(1)));
 out[0]=sub(pt(cap),c).l;
 I theta=five?add(pt(4.5),mul(pt(3.5),c)):add(divi(pt(2*(n-1)),pt(n-2)),mul(divi(pt(2*(n/2)-3),pt(n/2-1)),c));
 out[1]=theta.u;
}
