# Exact numerical constants audit

Source: paper-wedge/main.tex lines239-434 (Sections5-7 and the proof of Theorem1.5). Standard library only. All arithmetic uses Fraction; there are no floating point comparisons. Square-root bounds use integer square roots at denominator10^30. Sine and cosine use alternating Taylor sums with signed remainders; pi uses Machin identity and alternating arctangent sums. Displayed decimal endpoints are rounded outward to12 places. Every free-parameter reduction is explained in the final column and in source comments. This validates arithmetic conditional on the stated geometric premises, not the proof.

| Where | Claim | Result | Upper bound on lhs | Lower bound on rhs | Whole-range reduction / evidence |
|---|---|---|---:|---:|---|
| 5, l243 | 2 tau <= 0.16 | PASS | 0.160000000000 | 0.160000000000 | Increasing in tau; tau <= 0.08. |
| 5, l262-264 | cos(tau)>0 | PASS | 0.000000000000 | 0.996801706302 | Worst case tau=0.08; cos is decreasing on [0,0.08]. |
| 5, l264 | cos(tau)-sin(tau)>0 | PASS | 0.000000000000 | 0.916887012333 | Worst case tau=0.08; cos-sin decreases on this interval. |
| 5, l264,296 | cos(0.16)>0 (positive normal product) | PASS | 0.000000000000 | 0.987227283375 | Angle between flat normals has absolute value <=0.16. |
| 5, l243,405 | 2 tau < pi/4 (orientation distance is absolute angle) | PASS | 0.160000000000 | 0.785398163397 | Worst case tau=0.08; below the modulo-pi/2 midpoint. |
| 5, l274 | sec(theta)>=1 for 0<=theta<=0.16 | PASS | 1.000000000000 | 1.012937969644 | Cos lies in (0,1]; hence every sec factor is >=1. Endpoint bound verifies positivity. |
| 5, l241,280 | 1+zeta^2 <= 2 for zeta in [0,1] | PASS | 2.000000000000 | 2.000000000000 | Increasing in zeta; atan is increasing, giving atan(zeta)<=pi/4. |
| 5, l280 | cos(phi-atan(zeta))>0 | PASS | 0.945398163398 | 1.570796326794 | \|phi-atan(zeta)\| <= 0.08+pi/4 <= 0.16+pi/4 < pi/2; ensures a positive denominator. |
| 5, l280 | cos(atan(zeta)) >= 1/sqrt(2) | PASS | 2.000000000000 | 2.000000000000 | Square both positive sides: 1+zeta^2<=2 for zeta<=1. |
| 5, l280 | sin(atan(zeta)) >= zeta/sqrt(2) | PASS | 2.000000000000 | 2.000000000000 | Divide by zeta>0 and square; same worst case zeta=1. |
| 5, l303 | unit-square horizontal/vertical extent <= sqrt(2) | PASS | 2.000000000000 | 2.000000000000 | For any angle, (\|cos\|+\|sin\|)^2 <=2(cos^2+sin^2)=2 by (\|cos\|-\|sin\|)^2>=0. |
| 6, l323 | delta <= 2/5 (local distance applies) | PASS | 0.031250000000 | 0.400000000000 | The common sqrt(2) cancels. |
| 6, l327 | 21.35 < pi(1.9+sqrt(2)/2)^2 | PASS | 21.350000000000 | 21.353423388754 | Positive factors; rational lower enclosures. |
| 6, l327 | pi(1.9+sqrt(2)/2)^2 <21.36 | PASS | 21.353423388755 | 21.360000000000 | Positive factors; rational upper enclosures; interprets 21.35... prefix. |
| 6, l327 | disc area <22 => at most21 disjoint unit areas | PASS | 21.353423388755 | 22.000000000000 | An integer count bounded by a number <22 is <=21, conditional on containment. |
| 6, l327 | (1+sqrt(2))(sqrt(2)+delta)<3.49 | PASS | 3.489657736198 | 3.490000000000 | Positive factors; delta fixed. |
| 6, l327 | 3.49<4 => at most3 (hence4) floor squares | PASS | 3.490000000000 | 4.000000000000 | Integer area count; conditional on the stated box containment. |
| 6, l327 | 50(21+4sqrt(2))<1333 | PASS | 1332.842712474620 | 1333.000000000000 | Use upper sqrt(2) enclosure. |
| 6, l327 | 1333<=1350 | PASS | 1333.000000000000 | 1350.000000000000 | No free parameters; proves the displayed tilt-death coefficient. |
| 6, l341 | cos(tau)-sin(tau)>0.9 | PASS | 0.900000000000 | 0.916887012333 | Decreases in tau; worst tau=0.08. |
| 6, l341 | delta<0.9 (separation from floor probes) | PASS | 0.031250000000 | 0.900000000000 | Delta=1/32. |
| 6, l347 | 4 tan(theta)/cos(theta) <=4.3 theta | PASS | 4.104173321389 | 4.300000000000 | For theta>0 divide by theta; sin(theta)/theta<=1, cos(theta)>=cos(0.16). theta=0 by continuity. |
| 6, l345 | delta/cos(theta)<1 (backward crossing stays inside length1) | PASS | 0.031654311552 | 1.000000000000 | theta<=0.16; cos bounded below; permits sufficiently small positive eta. |
| 6, l354 | 2 delta <2/5 (local rectangle distance applies) | PASS | 0.062500000000 | 0.400000000000 | Common sqrt(2) cancels. |
| 6, l354 | tan(theta)<=1.01 theta, theta<=0.16 | PASS | 0.995738794667 | 0.997072000000 | In v=theta^2 the RHS-LHS is 0.01-(1.01/2-1/6)v-v^2/120, decreasing. Check v=0.16^2; theta=0 by continuity. |
| 6, l354 | tan(a)<=1.01 a, a<=tau<=0.08 | PASS | 0.998933674667 | 1.006768000000 | Same decreasing polynomial margin; endpoint a=0.08. |
| 6, l354 | 2*1.01=2.02 | PASS | 2.020000000000 | 2.020000000000 | Two lateral sides. |
| 6, l354 | 2.02+4.3=6.32 | PASS | 6.320000000000 | 6.320000000000 | Combined ordered-pair coefficient. |
| 6, l354; 7, l375 | 1.9+sqrt(2)/2<2.61 | PASS | 2.607106781187 | 2.610000000000 | Containment radius enlarges to2.61. |
| 6, l354; 7, l375 | pi*2.61^2<22 => at most21 unit squares | PASS | 21.400843315520 | 22.000000000000 | Integer count conditional on disc containment. |
| 6, l354 | 21*20=420 ordered pairs | PASS | 420.000000000000 | 420.000000000000 | Distinct squares; unordered pairs give half. |
| 6, l354 | two walls *4 squares=8 | PASS | 8.000000000000 | 8.000000000000 | Conditional on the claimed per-wall box bound (listed separately below). |
| 6, l354 | 2*1.01*delta*tan(tau)<0.01 | PASS | 0.005060800985 | 0.010000000000 | Increasing tan on [0,0.08]; worst tau=0.08, fixed delta. |
| 6, l354 | 50(6.32*420+2.02*4+1.01*8)<=134000 | PASS | 133528.000000000000 | 134000.000000000000 | Derives the corollary coefficient from the stated multiplicities. |
| 6, l351 | 1/delta+134000 delta<=4250 | PASS | 4219.500000000000 | 4250.000000000000 | Delta=1/32. |
| 7, l369 | (2/5)^(-1)=5/2 | PASS | 2.500000000000 | 2.500000000000 | Reciprocal line-waste threshold. |
| 7, l369 | 2 tau*(5/2)<=0.4 | PASS | 0.400000000000 | 0.400000000000 | Increasing in tau; endpoint0.08. |
| 7, l375 | 21 choose2=210 | PASS | 210.000000000000 | 210.000000000000 | Unordered distinct pairs. |
| 7, l375 | sqrt(2)*50*210<14850 | PASS | 14849.242404917499 | 14850.000000000000 | Upper rational sqrt enclosure. |
| 7, l364-375 | 14850+0.4<=14851 | PASS | 14850.400000000000 | 14851.000000000000 | Adds bad and not-bad contributions. |
| 7, l405 | sin(tau)<=tau for all 0<=tau<=0.08 | PASS | 1.000000000000 | 1.000000000000 | sin(tau)/tau<=1 follows by integrating cos(u)<=1; tau=0 by limit. Then MVT bounds \|cos(phi)-cos(phi-prime)\|<=tau \|phi-phi-prime\|. |
| 7, l405 | cos(0.08)-1/4-1/32>0.7 | PASS | 0.700000000000 | 0.715551706302 | Cos decreases with tau; worst tau=0.08. |
| 7, l412,416 | delta<=1/4 | PASS | 0.031250000000 | 0.250000000000 | Non-aligned-level branch and large-Theta branch. |
| 7, l415-416 | 1-cos(phi)<=0.51 tau^2 for \|phi\|<=tau | PASS | 0.500000000000 | 0.510000000000 | 1-cos(phi)=integral sin(u)du<=phi^2/2<=tau^2/2; divide by tau^2>0. |
| 7, l415 | j(1-0.51 tau^2)>1/2 for j>=1 | PASS | 0.500000000000 | 0.996736000000 | Coefficient positive, expression increases in j and decreases in tau; worst j=1,tau=0.08. |
| 7, l415 | delta<=1/2 | PASS | 0.031250000000 | 0.500000000000 | Bounds any positive drop by1/2. |
| 7, l416 | j(1-0.51 tau^2)-1/4-delta>=1/2 | PASS | 0.500000000000 | 0.715486000000 | Same monotonicity; worst j=1,tau=0.08. |
| 7, l425 | 1-1/4=3/4 | PASS | 0.750000000000 | 0.750000000000 | Death bound <=L/4 gives arriving measure >=3L/4. |
| 7, l425 | 3/(4sqrt(2))>=0.53 | PASS | 0.530000000000 | 0.530330085889 | Worst zeta=1 in cos(atan(zeta)); \|G\|>=3L/4. |
| 7, l425 | 1-0.53=0.47 | PASS | 0.470000000000 | 0.470000000000 | Complement measure bound. |
| 7, l425 | 2*0.47=0.94 | PASS | 0.940000000000 | 0.940000000000 | Count each skip against width1/(2zeta). |
| 7, l429 | (3/(4sqrt(2)))R-1/32>=0.499R for R>=1 | PASS | 0.499000000000 | 0.499080085889 | Divide by R>0; -delta/R increases in R, worst R=1. |
| 7, l429 | 0.94/32<=0.0294 | PASS | 0.029375000000 | 0.029400000000 | Rounded skip loss (strictly less, by0.000025). |
| 7, l429 | 0.499-0.0294>=0.4696 | PASS | 0.469600000000 | 0.469600000000 | Exact subtraction. |
| 7, l429 | 0.499-0.94/32>=0.4696 | PASS | 0.469600000000 | 0.469625000000 | Direct exact check before the intermediate upward rounding of skip loss. |
| 7, l429 | 14851/0.7<=21216 | PASS | 21215.714285714286 | 21216.000000000000 | Divide the tube bound by positive0.7. |
| 7, l429 | 0.47*21216<0.4696*21300 | PASS | 9971.520000000000 | 10002.480000000000 | Preserves a slightly weaker final coefficient. |
| Theorem1.5, l433 | sqrt(LR)<=L when R<=L | PASS | 1.000000000000 | 1.000000000000 | Divide positive L^2: R/L=zeta<=1; square roots preserve order. |
| Theorem1.5, l433 | 10800*(7e-6)<=0.0756 | PASS | 0.075600000000 | 0.075600000000 | Increasing in W/L; endpoint7e-6; W>0 gives tau>0. |
| Theorem1.5, l433 | 0.0756<=0.08 | PASS | 0.075600000000 | 0.080000000000 | Tau lies in the proposition range. |
| Theorem1.5, l433 | 1350/10800=1/8 | PASS | 0.125000000000 | 0.125000000000 | Cancel W>0 after substituting tau=10800W/L; holds for every positive W,L. |
| Theorem1.5, l433 | 4250*(7e-6)<=0.03 | PASS | 0.029750000000 | 0.030000000000 | Increasing in W/L, worst endpoint. |
| Theorem1.5, l433 | 0.01<=0.01L for L>=R>=1 | PASS | 0.010000000000 | 0.010000000000 | Increasing in L; worst L=1. |
| Theorem1.5, l433 | 0.03+1/8+0.01<=1/4 | PASS | 0.165000000000 | 0.250000000000 | Divide by L; all three terms bounded for entire stated range. |
| Theorem1.5, l433 | sharper hypothesis bound:0.02975+1/8+0.01<=1/4 | PASS | 0.164750000000 | 0.250000000000 | Same bound before rounding0.02975 up to0.03. |
| Theorem1.5, l433 | 21300*10800=230040000 | PASS | 230040000.000000000000 | 230040000.000000000000 | Substitution into the proposition. |
| Theorem1.5, l433 | sqrt(0.47/(21300*10800))>=4.5e-5 | PASS | 0.465831000000 | 0.470000000000 | Square positive quantities; equivalent exact rational comparison. |
| Theorem1.5, l433 | 4.5e-5>=7e-6 | PASS | 0.000007000000 | 0.000045000000 | Multiply by nonnegative sqrt(LR). |
| Theorem1.5, l433 | W=0:0.01<=L/4 for L>=1 | PASS | 0.010000000000 | 0.250000000000 | Worst L=1 gives the proposition hypothesis at tau=0.08. |
| Theorem1.5, l433 | W=0:0.47R>0 for R>=1 | PASS | 0.000000000000 | 0.470000000000 | Increasing in R, worst R=1; contradiction. |

## Claims not reduced to finite arithmetic

- 5, l245: Local rectangle constants: distance sqrt(2)+2/5, charge theta/50, radius1.9. These are imported geometric claims from Corollary local, whose proof is outside Sections5-7; this checker uses them as premises.
- 6, l354: At most4 squares per wall and exactly2 exceptional left-wall squares: the text imports Section walls and supplies no finite enclosure/count computation here. The arithmetic using4,8,2 is checked above; the geometric applicability is not certified.
- 5-7: Packing-dependent density1, gap W/delta, probe measures2 delta tan(theta) and delta tan(a), conflict projection4 delta tan(theta)/cos(theta), disjoint tubes, and drop/tube identities are geometric/measure statements. Their numerical relaxations are checked above; exact arithmetic alone does not verify those statements.

70 exact claims checked; 0 FAIL; 3 separately listed unchecked premise groups. Runtime 0.000804 seconds.
