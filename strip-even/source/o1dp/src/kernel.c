#include <math.h>
#include <stdlib.h>
#include <float.h>
#include <stddef.h>
/* Compile without fast-math. Each arithmetic operation used for a bound is
   rounded outward. libm sin/cos are assumed within 8 ulps (see README). */
static double dn(double x){return nextafter(x,-INFINITY);}
static double up(double x){return nextafter(x,INFINITY);}
static double pad(double x,int dir){for(int k=0;k<8;k++)x=nextafter(x,dir?INFINITY:-INFINITY);return x;}
typedef struct{double l,u;} I;
typedef struct{I c,s,h;double a,b;} Cell;
static I add(I a,I b){return (I){dn(a.l+b.l),up(a.u+b.u)};}
static I sub(I a,I b){return (I){dn(a.l-b.u),up(a.u-b.l)};}
static I mul(I a,I b){double p[]={a.l*b.l,a.l*b.u,a.u*b.l,a.u*b.u};double l=p[0],u=p[0];for(int j=1;j<4;j++){l=fmin(l,p[j]);u=fmax(u,p[j]);}return (I){dn(l),up(u)};}
static I divi(I a,I b){return mul(a,(I){dn(1/b.u),up(1/b.l)});}
static I trig(double x,int s){return (I){pad(s?sin(x):cos(x),0),pad(s?sin(x):cos(x),1)};}
static I q(double x){return add(trig(x,0),trig(x,1));}
static Cell cell(double a,double b){
 Cell z;z.a=a;z.b=b;
 z.c=(I){fmax(0,pad(cos(b),0)),fmin(1,pad(cos(a),1))};
 z.s=(I){fmax(0,pad(sin(a),0)),fmin(1,pad(sin(b),1))};
 I qa=q(a),qb=q(b);double hi=fmax(qa.u,qb.u);
 /* pi/4 lies between the two adjacent floats bracketing M_PI/4. */
 if(a<=nextafter(M_PI_4,INFINITY)&&b>=nextafter(M_PI_4,-INFINITY))hi=up(pad(sqrt(2.0),1));
 z.h=(I){dn(fmin(qa.l,qb.l)*.5),up(hi*.5)};return z;
}
/* Every facet support is (1 + cos(delta) + |sin(delta)|)/2.
   On |delta| in [0,pi/2], q is concave, hence its minimum is at
   an endpoint. Difference endpoints and the evaluations are outward. */
static double supportlo(Cell a,Cell b){
 double l=dn(a.a-b.b),u=up(a.b-b.a);
 double near=(l<=0&&u>=0)?0:fmin(fabs(l),fabs(u));
 double far=fmin(nextafter(M_PI_2,INFINITY),fmax(fabs(l),fabs(u)));
 return dn(dn(1+fmin(q(near).l,q(far).l))*.5);
}
static double term(double support,I dy,I ny,double nx){
 if(nx<=0)return INFINITY;
 double num=dn(support-mul(dy,ny).u);
 return fmax(0,dn(fmax(0,num)/nx));
}
static I neg(I a){return (I){-a.u,-a.l};}
static I scale(I a,double x){return mul(a,(I){x,x});}
static I displacement(Cell a,Cell b,I H,int r,int s){
 I ya=r?sub(H,a.h):a.h,yb=s?sub(H,b.h):b.h;
 return sub(yb,ya);
}
static double correlated(Cell a,Cell b,I H,I dy,int r,int s,int owner,int sine){
 Cell k=owner?b:a,other=owner?a:b;
 /* delta = t_owner - t_other. At delta=0 the generalized derivative
    of |sin(delta)| includes both one-sided values. */
 I sd=sub(mul(k.s,other.c),mul(k.c,other.s));
 I cd=add(mul(k.c,other.c),mul(k.s,other.s));
 I sign=k.a>other.b?(I){1,1}:k.b<other.a?(I){-1,-1}:(I){-1,1};
 I ds=scale(add(neg(sd),mul(sign,cd)),.5);
 I hp=scale(sub(k.c,k.s),.5);
 I ddy=scale(hp,owner?(1-2*s):(2*r-1));
 I ny=sine?neg(k.c):k.s, dny=sine?k.s:k.c;
 I derivative=sub(sub(ds,mul(ddy,ny)),mul(dy,dny));
 /* Move away from the smallest-nx face: +t for sin, -t for cos. */
 double B=sine?derivative.l:-derivative.u;
 double e=sine?k.a:k.b;
 Cell face=cell(e,e);
 int endpoint=(sine&&e==0)||(!sine&&e==nextafter(M_PI_2,INFINITY));
 if(endpoint){
  face.c=(I){sine?1:0,sine?1:0};
  face.s=(I){sine?0:1,sine?0:1};face.h=(I){.5,.5};
 }
 Cell fa=owner?a:face,fb=owner?face:b;
 I fdy=displacement(fa,fb,H,r,s);
 I fny=sine?neg(face.c):face.s;
 double A=dn(supportlo(fa,fb)-mul(fdy,fny).u),aa=fmax(0,A);
 double c=endpoint?0:(sine?face.s.u:face.c.u);
 /* Interiority gives N(e)>=max(A,0)=aa. Mean value gives
    N>=aa+x B, and nx<=c+x. If aa+x B is negative, the ratio
    bound is nonpositive and N/nx>=0 already suffices. Otherwise
    N/nx >= (aa+x B)/(c+x) >= min(aa/c,B), or B when c=0.
    Take max with the unchanged plain bound and zero. */
 return c>0?fmin(dn(aa/c),B):B;
}
static double g(Cell a,Cell b,double sup,I dy,I H,int r,int s){
 /* At each point kappa is the minimum over eligible normals. Each
    eligible term >= its box term_lb; ineligible normals included by
    the box only decrease the minimum. Numerators are pointwise >=0
    because (0,dy) is in Delta. Thus clipping num.lo to zero is safe.
    The other four signed normals have nx<=0 throughout this domain. */
 double z=INFINITY;
 for(int owner=0;owner<2;owner++)for(int sine=0;sine<2;sine++){
  Cell k=owner?b:a;I ny=sine?neg(k.c):k.s;
  double nx=sine?k.s.u:k.c.u;
  if(nx<=0)continue;
  double plain=term(sup,dy,ny,nx);
  double ratio=correlated(a,b,H,dy,r,s,owner,sine);
  double lemma=0,W=0;
  int use_lemma=0;
  if(r==1&&s==0&&sine&&a.b<=1&&b.b<=1){
   W=fmax(a.b,b.b);use_lemma=1;
  }else if(r==0&&s==1&&!sine&&
           a.a>=up(nextafter(M_PI_2,INFINITY)-1)&&
           b.a>=up(nextafter(M_PI_2,INFINITY)-1)){
   W=up(nextafter(M_PI_2,INFINITY)-fmin(a.a,b.a));use_lemma=1;
  }
  /* SPEC addendum 2: for C->F sine normals in [0,W], let m be
     the larger tilt. The joint estimate N>=m(1-3W/4-W^2/4),
     nx<=m and nonnegative coefficient give the same lower bound
     for N/nx. Reflect t about pi/2 for F->C cosine normals.
     No other role/normal/corner combination receives this candidate.
     Enclose pi/2 and its eligibility threshold upward; round each
     positive penalty operation up and each subtraction down. */
  if(use_lemma){
   double linear=up(up(3*W)/4),quadratic=up(up(W*W)/4);
   lemma=dn(dn(1-linear)-quadratic);
  }
  z=fmin(z,fmax(plain,fmax(ratio,fmax(lemma,0))));
 }
 return fmax(0,z);
}
static void gaps(Cell a,Cell b,I H,double out[4]){
 double sup=supportlo(a,b);I d00=sub(b.h,a.h),d01=sub(sub(H,b.h),a.h);
 out[0]=g(a,b,sup,d00,H,0,0);out[1]=g(a,b,sup,d01,H,0,1);
 out[2]=g(a,b,sup,(I){-d01.u,-d01.l},H,1,0);out[3]=g(a,b,sup,(I){-d00.u,-d00.l},H,1,1);
}
double gap(double a,double b,double c,double d,double ha,double hb,int r,int s){double x[4];gaps(cell(a,b),cell(c,d),(I){ha,hb},x);return x[2*r+s];}
double h_lower(double a,double b){return cell(a,b).h.l;}
double point(double a,double b,double dy){double ca=cos(a),sa=sin(a),cb=cos(b),sb=sin(b);double sup=(1+fabs(cos(a-b))+fabs(sin(a-b)))*.5;double z=INFINITY;double nx[]={ca,sa,cb,sb},ny[]={sa,-ca,sb,-cb};for(int i=0;i<4;i++)if(nx[i]>0)z=fmin(z,(sup-dy*ny[i])/nx[i]);return z;}
double target(double theta,double H){I c=trig(theta,0),s=trig(theta,1),four={4,4},two={2,2},hv={H,H},three={3,3};I a=divi(sub(four,mul(sub(mul(three,hv),two),c)),s);I b=divi(sub(four,mul(mul(two,hv),s)),c);return add(add(two,a),b).u;}
/* Layout [position][role][flag][cell]. W carries the flag already set
   in the prefix, not a separately accumulated suffix flag. */
#define IDX(p,r,f,c) ((((size_t)(p)*2+(r))*2+(f))*n+(c))
int solve(int n,const double *edges,double ha,double hb,double *result,unsigned char *binding){
 Cell *cells=malloc(sizeof(Cell)*n);double *v=malloc(sizeof(double)*24*n),*w=malloc(sizeof(double)*24*n);
 if(!cells||!v||!w){free(cells);free(v);free(w);return -1;}
 for(int c=0;c<n;c++)cells[c]=cell(edges[c],edges[c+1]);
 for(size_t k=0;k<(size_t)24*n;k++)v[k]=w[k]=INFINITY;
 for(int r=0;r<2;r++)for(int c=0;c<n;c++){v[IDX(0,r,0,c)]=cells[c].h.l;w[IDX(5,r,1,c)]=cells[c].h.l;}
 for(int p=0;p<5;p++){
  int j=4-p;
  for(int a=0;a<n;a++)for(int b=0;b<n;b++){
   double gs[4];gaps(cells[a],cells[b],(I){ha,hb},gs);
   for(int r=0;r<2;r++)for(int s=0;s<2;s++)for(int f=0;f<2;f++){
    int ff=f||(r==s);double gg=gs[2*r+s];
    double z=dn(v[IDX(p,r,f,a)]+gg);size_t ix=IDX(p+1,s,ff,b);if(z<v[ix])v[ix]=z;
    z=dn(gg+w[IDX(j+1,s,ff,b)]);ix=IDX(j,r,f,a);if(z<w[ix])w[ix]=z;
   }
  }
 }
 double d=INFINITY,u=INFINITY;
 for(int r=0;r<2;r++)for(int f=0;f<2;f++)for(int c=0;c<n;c++){
  double z=dn(v[IDX(5,r,f,c)]+cells[c].h.l);if(z<u)u=z;if(f&&z<d)d=z;
 }
 result[0]=d;result[1]=u;
 /* V includes only the left endpoint h, W only the right endpoint h;
    there is no shared vertex cost to subtract, including at i=1,6. */
 for(int c=0;c<n;c++){
  binding[c]=0;
  for(int p=0;p<6;p++)for(int r=0;r<2;r++)for(int f=0;f<2;f++)if(dn(v[IDX(p,r,f,c)]+w[IDX(p,r,f,c)])<result[2])binding[c]=1;
 }
 free(cells);free(v);free(w);return 0;
}
