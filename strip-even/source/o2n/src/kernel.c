#include <math.h>
#include <assert.h>
#include <stdlib.h>
#include <stdint.h>
/* o1dp conventions: IEEE binary64, no fast-math; outward nextafter after
   every arithmetic operation, eight ulps for libm. */
typedef struct { double l,u; } I;
static double dn(double x){return nextafter(x,-INFINITY);}
static double up(double x){return nextafter(x,INFINITY);}
static double pad(double x,int dir){for(int i=0;i<8;i++)x=nextafter(x,dir?INFINITY:-INFINITY);return x;}
static I iv(double l,double u){assert(l<=u);return (I){l,u};}
static I pt(double x){return iv(x,x);}
static I add(I a,I b){return iv(dn(a.l+b.l),up(a.u+b.u));}
static I neg(I a){return iv(-a.u,-a.l);}
static I sub(I a,I b){return add(a,neg(b));}
static I mul(I a,I b){double p[]={a.l*b.l,a.l*b.u,a.u*b.l,a.u*b.u};double l=p[0],u=l;for(int i=1;i<4;i++){l=fmin(l,p[i]);u=fmax(u,p[i]);}return iv(dn(l),up(u));}
static I divi(I a,I b){assert(b.l>0);return mul(a,iv(dn(1/b.u),up(1/b.l)));}
static I sq(I a){double l=a.l<=0&&a.u>=0?0:fmin(a.l*a.l,a.u*a.u);return iv(fmax(0,dn(l)),up(fmax(a.l*a.l,a.u*a.u)));}
static I root(I a){assert(a.l>=0);return iv(fmax(0,pad(sqrt(a.l),0)),pad(sqrt(a.u),1));}
static I ab(I a){return iv(a.l<=0&&a.u>=0?0:fmin(fabs(a.l),fabs(a.u)),fmax(fabs(a.l),fabs(a.u)));}
static I phi(I x,I y,I c,I s){I cs=add(c,s);I a=add(ab(add(c,mul(x,s))),ab(sub(s,mul(x,c))));I b=add(ab(add(c,mul(y,s))),ab(sub(s,mul(y,c))));return mul(add(add(a,b),mul(sub(x,y),cs)),pt(.5));}
static I kink(I x,I y,I q,int positive){I r=root(add(pt(1),sq(q))),c,s;if(positive){c=divi(pt(1),r);s=divi(q,r);}else{c=divi(neg(q),r);s=divi(pt(1),r);}return phi(x,y,c,s);}
static I candidate(I x,I y){I best=add(add(pt(1),pt(fmax(x.l,0))),pt(fmax(-y.u,0)));/* endpoint upper needs upper ends */best.u=add(add(pt(1),pt(fmax(x.u,0))),pt(fmax(-y.l,0))).u;I qs[]={x,y};for(int j=0;j<2;j++){I q=qs[j],v;if(q.u>0){v=kink(x,y,iv(fmax(q.l,0),q.u),1);best.l=fmin(best.l,v.l);best.u=fmin(best.u,v.u);}if(q.l<0){v=kink(x,y,iv(q.l,fmin(q.u,0)),0);best.l=fmin(best.l,v.l);best.u=fmin(best.u,v.u);}}assert(best.l<=best.u);return best;}
static I mone(I x){double l=add(pt(1),pt(fmax(x.l,0))).l,u=add(pt(1),pt(fmax(x.u,0))).u;if(x.l<0){I v=divi(pt(1),root(add(pt(1),sq(iv(x.l,fmin(0,x.u))))));l=fmin(l,v.l);u=fmin(u,v.u);}/* Extra downward guard also dominates cancellation in the independent
 dense trigonometric reference near negative x. Never weaken the gate. */
 l=sub(pt(l),mul(pt(64*0x1p-52),add(pt(1),pt(fmax(fabs(x.l),fabs(x.u)))))).l;return iv(l,u);}
static double mid(I a){return a.l+(a.u-a.l)*.5;}
static double radius(I a,double c){return up(fmax(up(c-a.l),up(a.u-c)));}
/* A is the minimum over t of globally Lipschitz integrands. Choosing an
   active minimiser at either endpoint bounds each difference by the same
   Lipschitz constant. Equivalently the Clarke subdifferential is in the
   hull of active gradients. This remains valid through every kink. */
static double acentered(I x,I y){double a=mid(x),b=mid(y);I v=candidate(pt(a),pt(b));double d=pad(sqrt(2),1);return sub(pt(v.l),mul(pt(d),add(pt(radius(x,a)),pt(radius(y,b))))).l;}
static double alower(I x,I y){return fmax(candidate(x,y).l,acentered(x,y));}
static double mlower(I x){double m=mid(x);return fmax(mone(x).l,sub(pt(mone(pt(m)).l),pt(radius(x,m))).l);}
double a_bound(double xl,double xu,double yl,double yu,int mode){I x=iv(xl,xu),y=iv(yl,yu);return mode==0?candidate(x,y).l:mode==1?acentered(x,y):alower(x,y);}
double m_bound(double l,double u,int centered){I x=iv(l,u);return centered?sub(pt(mone(pt(mid(x))).l),pt(radius(x,mid(x)))).l:mone(x).l;}
/* Independent long-double point reference, direct trigonometric integrand. */
static long double fp(long double x,long double y,long double t){long double c=cosl(t),s=sinl(t);return (fabsl(c+x*s)+fabsl(s-x*c)+fabsl(c+y*s)+fabsl(s-y*c)+(x-y)*(c+s))/2;}
double a_reference(double xd,double yd,int dense){long double x=xd,y=yd,p=acosl(-1.L)/2,best=fp(x,y,0),q[]={x,y};int besti=0;if(dense){for(int i=1;i<=20000;i++){long double v=fp(x,y,p*i/20000);if(v<best){best=v;besti=i;}}/* Refine around the best dense sample, including nonsmooth minima. */long double l=p*fmax(0,besti-1)/20000,u=p*fmin(20000,besti+1)/20000;for(int i=0;i<72;i++){long double a=(2*l+u)/3,b=(l+2*u)/3;if(fp(x,y,a)<fp(x,y,b))u=b;else l=a;}best=fminl(best,fp(x,y,(l+u)/2));}for(int i=0;i<2;i++){if(q[i]!=0){long double t=q[i]>0?atanl(q[i]):atanl(-1/q[i]);best=fminl(best,fp(x,y,t));}}return (double)best;}
double m_reference(double x){return x>=0?1+x:1/sqrt(1+x*x);}
/* Fast dense-grid reference uses precomputed long-double trig values. */
void dense_batch(int n,const double *x,const double*y,double*out){static long double c[20001],s[20001];static int init=0;if(!init){for(int k=0;k<=20000;k++){long double t=acosl(-1.L)*k/40000;c[k]=cosl(t);s[k]=sinl(t);}init=1;}for(int i=0;i<n;i++){long double a=x[i],b=y[i],best=INFINITY;for(int k=0;k<=20000;k++){long double v=(fabsl(c[k]+a*s[k])+fabsl(s[k]-a*c[k])+fabsl(c[k]+b*s[k])+fabsl(s[k]-b*c[k])+(a-b)*(c[k]+s[k]))/2;best=fminl(best,v);}/* Analytic local refinement of all grid kink brackets. */best=fminl(best,a_reference(x[i],y[i],0));out[i]=(double)best;}}
static I bplain(I x,I y,I w,double h,int kind){I v=iv(alower(x,y),candidate(x,y).u);if(kind==2)v=add(v,iv(alower(x,w),candidate(x,w).u));else { /* x>=0: m1(x)=1+x; preserve cancellation with -H*x. */ assert(x.l>=0);return add(pt(1),add(v,mul(sub(pt(1),pt(h)),x))); }return sub(v,mul(pt(h),x));}
static I bbound(I x,I y,I w,double h,int kind){I v=bplain(x,y,w,h,kind);double c=mid(x),cy=mid(y),cw=mid(w);I v0=bplain(pt(c),pt(cy),pt(cw),h,kind);/* Constant gradient bounds; combined x derivative includes -H. */double d=pad(sqrt(2),1);double dx=kind==2?fmax(fabs(h),up(up(2*d)-h)):fmax(fabs(1-h),fabs(up(up(1+d)-h)));double loss=add(mul(pt(dx),pt(radius(x,c))),mul(pt(d),pt(radius(y,cy)))).u;if(kind==2)loss=add(pt(loss),mul(pt(d),pt(radius(w,cw)))).u;v.l=fmax(v.l,sub(pt(v0.l),pt(loss)).l);return v;}
typedef struct {I x;double lower;} Node;
/* Best-first 1D B&B. An upper witness fixes every variable to a midpoint.
   All live leaf bounds, including unrefined leaves, remain in the minimum. */
double inner(double lo,double hi,double yl,double yu,double wl,double wu,double h,int kind,int budget,double tol,int *count){I y=iv(yl,yu),w=iv(wl,wu);Node *a=malloc(sizeof(Node)*(budget+2));assert(a);int n=1,used=1;a[0]=(Node){iv(lo,hi),bbound(iv(lo,hi),y,w,h,kind).l};double upper=INFINITY;while(1){int k=0;for(int j=1;j<n;j++)if(a[j].lower<a[k].lower)k=j;I x=a[k].x;double c=mid(x);upper=fmin(upper,bplain(pt(c),pt(mid(y)),pt(mid(w)),h,kind).u);if(used+2>budget||upper-a[k].lower<=tol||c<=x.l||c>=x.u){double result=a[k].lower;free(a);*count=used;return result;}I l=iv(x.l,c),r=iv(c,x.u);a[k]=(Node){l,bbound(l,y,w,h,kind).l};a[n++]=(Node){r,bbound(r,y,w,h,kind).l};used+=2;}}
double target(double theta,double H){I c=iv(pad(cos(theta),0),pad(cos(theta),1)),s=iv(pad(sin(theta),0),pad(sin(theta),1));return add(add(pt(2),divi(sub(pt(4),mul(sub(mul(pt(3),pt(H)),pt(2)),c)),s)),divi(sub(pt(4),mul(mul(pt(2),pt(H)),s)),c)).u;}
void dense_m_batch(int n,const double*x,double*out){static long double c[20001],s[20001];static int init=0;if(!init){for(int k=0;k<=20000;k++){long double t=acosl(-1.L)*k/40000;c[k]=cosl(t);s[k]=sinl(t);}init=1;}for(int i=0;i<n;i++){long double a=x[i],best=INFINITY;for(int k=0;k<=20000;k++){long double v=((1+a)*(c[k]+s[k])+fabsl(c[k]+a*s[k])+fabsl(s[k]-a*c[k]))/2;best=fminl(best,v);}if(a<0){long double t=atanl(-1/a),cc=cosl(t),ss=sinl(t);best=fminl(best,((1+a)*(cc+ss)+fabsl(cc+a*ss)+fabsl(ss-a*cc))/2);}out[i]=(double)best;}}
