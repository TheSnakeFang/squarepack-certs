# O2 for every even n: the analytic reduction

Status 2026-11-01, revised the same day after a blind referee report (§14) and an implementer's issue report. This generalises `../o2cert/LEMMAS.md` (the n = 6 reduction, Lemmas 1–11) to the Morandi pattern with n = 2m ≥ 6 squares, and adds a block decomposition that replaces the n = 6 corner certificate by an analytic local lemma. What is proved here: Lemmas 1–9 and 13–21, Theorems 10, 11, 22 (numbering follows `o2cert` for 1–11; there is no Lemma 12), every proof complete. What is left to a certified program: the finite list of low-dimensional inequalities in §11 (per n ∈ {6, 8, 10}). Conditional on them, Theorem 22 gives O2_n on [H_lo(n), 2] with H_lo(n) = 1.861098, 1.852049, 1.846936; the sliver [H*(n), H_lo(n)) of width < 1e-6 is not covered. Everything that is only numerically supported is labelled as such. The per-pair study in `scratchpad/pairdecomp/REPORT.md` (2026-11-01) was the starting point; its findings were re-derived, and three of them are corrected below (§13).

## 0. Objects and conventions

- n = 2m ≥ 6 even, k := 2 − H, H ∈ [H*(n), 2]. h, G, S(t), κ, m1, A, E, d, d0 = 3 − 2√2 are exactly as in `o2cert/LEMMAS.md` §0–4; none of them depends on n.
- Chain function of the Morandi pattern F C F C … F C (n squares): Φ_M(t; H) = h(t_1) + h(t_n) + Σ_{i=1}^{n−1} κ(t_i, t_{i+1}, dy_i), dy_i = s_i (H − h(t_i) − h(t_{i+1})), s_i = (−1)^{i+1}.
- Dual variables r ∈ R^{n−1}. Right-sign value ρ_j := (−1)^{j+1} r_j (so ρ_j = r_j for odd j, ρ_j = −r_j for even j); σ(r) := Σ_j (−1)^j r_j = −Σ_j ρ_j. Flat orthant F_n := {ρ_j ≥ 0 for all j}. Coordinates 1 and n−1 are the *end* coordinates, the others *interior*.
- Pairs p = 1, …, n−2; pair p consists of coordinates p and p+1. Its odd coordinate gives x_p := ρ_odd ≥ 0 (on F_n), its even coordinate gives Y_p := ρ_even = −r_even ≥ 0. Pair p belongs to square j = p + 1 of the chain.
- Ψ_n(r; H) := m1(r_1) + m1(r_{n−1}) + Σ_{p=1}^{n−2} A(r_odd(p), r_even(p)) + H σ(r). Written out: A(r_1, r_2) + A(r_3, r_2) + A(r_3, r_4) + … + A(r_{n−1}, r_{n−2}).
- Morandi family: r*(T) := (T, −1/T, T, …, −1/T, T) (odd entries T, even entries −1/T), w := x + 1/x, D(x) := 1 + w − √(w(w + 2)) (Lemma 6), and
  f_n(T; H) := n + k (mT + (m − 1)/T) − (n − 2) D(T).
  T_n(H) is the unique zero of ∂_T f_n in [1/2, 3/2] and F_n(H) := f_n(T_n(H); H) (Lemma 6.3). H*(n) ∈ (√2, 2) is the unique root of F_n(H) = n (Lemma 6.3(e)). To 10 digits (numerical, not proof inputs): H*(6) = 1.8610971452, H*(8) = 1.8520484461, H*(10) = 1.8469355214, and T_n(H*(n)) = 0.887997, 0.919183, 0.936728.
- O2_n: Ψ_n(r; H) ≥ F_n(H) for all r ∈ R^{n−1}, H ∈ [H*(n), 2]. By Lemma 2 this is equivalent to Φ_M(t; H) ≥ F_n(H) on [0, π/2]^n. This document reduces O2_n on the smaller range [H_lo(n), 2] (Theorem 22), not on [H*(n), 2].

Note on the range. At H < H*(n), Ψ_n(0; H) = n < F_n(H) (Lemma 2, m1(0) = A(0, 0) = 1), so O2_n is false there. The rounded values 1.861097 and 1.852048 quoted for H*(6), H*(8) lie *below* the true roots (F_6(1.861097) − 6 = +7.1e-7, F_8(1.852048) − 8 = +3.1e-6), so a certificate must start at a rational H_lo > H*(n); §11 uses H_lo = 1.861098, 1.852049, 1.846936 (F_n(H_lo) − n = −4.2e-6, −3.8e-6, −4.3e-6 by the referee's 70-digit computation), and the interval [H*(n), H_lo) stays open.

That F_n(H) is the width of an actual Morandi packing is a statement about the construction and is not used for the lower bound. For n = 6, F_6 = min_θ L(θ, H) of `o2cert` (agreement to 1e-15 at H = 1.87, 1.9, 1.95); for n = 8, 10 F_n reproduces the reference widths in REPORT.md to 1e-10.

## 1. Support-function form and separation (general n)

**Lemma 1.** Unchanged from `o2cert` (it concerns one gap). The hypotheses hold for every gap of Φ_M: |dy_i| = H − h(t_i) − h(t_{i+1}) ∈ [H − √2, H − 1] ⊂ [0, 1] and the half-height of S(t_i) + S(t_{i+1}) is h(t_i) + h(t_{i+1}) ≥ 1. Since h(t_i) + h(t_{i+1}) ≤ √2 < H*(n), dy_i has the sign s_i, so no constraint on t is dropped. Hence κ(t_i, t_{i+1}, dy_i) = inf_r [G(r, t_i) + G(r, t_{i+1}) − r dy_i].

**Lemma 2 (separation).** Φ_M(t; H) = inf_{r ∈ R^{n−1}} Q(t, r; H) with Q = Σ_{j=1}^{n} w_j(t_j; r) + H σ(r), where
w_1 = (1 + r_1) h(t_1) + G(r_1, t_1), w_n = (1 + r_{n−1}) h(t_n) + G(r_{n−1}, t_n), and for 2 ≤ j ≤ n − 1
w_j = (r_{j−1} − r_j) h(t_j) + G(r_{j−1}, t_j) + G(r_j, t_j) (j even), w_j = (r_j − r_{j−1}) h(t_j) + G(r_{j−1}, t_j) + G(r_j, t_j) (j odd).
Consequently inf_t Φ_M(t; H) = inf_r Ψ_n(r; H).

*Proof.* Substitute Lemma 1 into each gap: −r_i dy_i = −s_i H r_i + s_i r_i (h(t_i) + h(t_{i+1})). The H-parts sum to −H Σ_i s_i r_i = H Σ_i (−1)^i r_i = H σ(r). The coefficient of h(t_j) collects s_{j−1} r_{j−1} (from gap j − 1) and s_j r_j (from gap j): for j = 1 it is 1 + r_1 (the 1 from the end term h(t_1)), for j = n it is 1 + s_{n−1} r_{n−1} = 1 + r_{n−1} (n − 1 is odd), for even j it is r_{j−1} − r_j and for odd j ∈ [3, n − 1] it is r_j − r_{j−1}. Each G(r_i, ·) appears in gap i with the two tilts t_i, t_{i+1}, i.e. in w_i and w_{i+1}. Infima over independent variables commute and the inf over [0, π/2)^n equals the min over the closed cube by continuity. Minimising w_1 and w_n over their tilt gives m1(r_1), m1(r_{n−1}); minimising w_j (2 ≤ j ≤ n − 1) gives A(r_{j−1}, r_j) for even j and A(r_j, r_{j−1}) for odd j, which is the term of pair p = j − 1 in Ψ_n. ∎

**Lemma 3, Lemma 4.** Unchanged (they are statements about A and m1 alone). In particular A(x, y) = A(−y, −x), A ≥ 0, m1(x) = 1 + x for x ≥ 0 and 1/√(1 + x²) for x < 0, and A is the minimum over the candidate set {E} ∪ {kink values} of Lemma 3(a).

## 2. The flat orthant

**Lemma 5 (E-identity).** On F_n, Ψ_n(r; H) = n + k Σ_j ρ_j − Σ_{p=1}^{n−2} d(x_p, Y_p), and Σ_j ρ_j = −σ(r).

*Proof.* On F_n every pair has x ≥ 0 ≥ y, so A = E − d = 1 + x_p + Y_p − d(x_p, Y_p). An interior coordinate lies in two pairs and an end coordinate in one, so Σ_p (1 + x_p + Y_p) = (n − 2) + 2 Σ_j ρ_j − ρ_1 − ρ_{n−1}. Adding m1(r_1) + m1(r_{n−1}) = 2 + ρ_1 + ρ_{n−1} and Hσ = −H Σ ρ_j gives n + (2 − H) Σ ρ_j − Σ d. ∎

**Lemma 6 (global deficit cap).** Unchanged: for x, Y ≥ 0, 0 ≤ d(x, Y) ≤ d0, with equality in the upper bound iff x = Y = 1. Its proof gives, with R_x = √(1 + x²),
dX(x, Y) = (1 − 1/R_x)(x + Y) + 1 − R_x = x²(x + Y − R_x)/(R_x(R_x + 1)) for xY ≤ 1, dX(x, Y) = (1 + x + Y) − (x + Y) q(x) for xY ≥ 1, q(u) := (1 + u)/√(1 + u²),
d = max(0, dX, dY) with dY(x, Y) := dX(Y, x), and for x > 0, sup_Y dX(x, Y) = dX(x, 1/x) = D(x) (on the axes d = 0).

**Corollary 6.1.** On F_n, Ψ_n(r; H) ≥ n − (n − 2) d0 + k(−σ(r)).

*Proof.* Lemma 5 and d ≤ d0 for each of the n − 2 pairs. ∎

**Lemma 6.3 (the Morandi family).** (a) Ψ_n(r*(T); H) = f_n(T; H) for every T > 0.
(b) D(x) = D(1/x), D is increasing on (0, 1], decreasing on [1, ∞), D(1) = d0, D'(x) = (x^{−2} − 1)/(P(P + w + 1)) with P = √(w(w + 2)), and D is strictly concave on [1/2, 3/2].
(c) For H ≤ 2, T ↦ f_n(T; H) is strictly convex on [1/2, 3/2]. For H < 2 its derivative has exactly one zero T_n(H) there; T_n(H) ∈ (√((m − 1)/m), 1), it solves
  (2 − H)(m − (m − 1)/T²) = (n − 2) D'(T),      (T-eq)
and T_n is strictly increasing in H, with T_n(2) := 1. F_n(H) = f_n(T_n(H); H) is strictly decreasing, F_n(2) = n − (n − 2) d0, and F_n'(H) = −(mT_n + (m − 1)/T_n) = σ(r*(T_n)).

*Proof.* (a) r*(T) ∈ F_n; every pair is (T, 1/T) and d(T, 1/T) = max(0, dX(T, 1/T), dY(T, 1/T)) = max(0, D(T), D(1/T)) = D(T); there are m odd coordinates equal to T and m − 1 even ones with ρ = 1/T; apply Lemma 5.
(b) D depends on x through w only, which is symmetric under x ↦ 1/x. With Δ(w) = 1 + w − P: Δ'(w) = 1 − (w + 1)/P = −1/(P(P + w + 1)) < 0 (because (w + 1)² − P² = 1) and Δ''(w) = 1/P³. With w' = 1 − x^{−2}, w'' = 2x^{−3}: D' = Δ' w' gives the formula and the monotonicity, and
D'' = (1 − x^{−2})²/P³ − 2/(x³ P (P + w + 1)).
D'' < 0 iff (1 − x^{−2})² x³ (P + w + 1) < 2P². Since P < w + 1 it suffices that (1 − x^{−2})² x³ (w + 1) ≤ P² = w(w + 2); substituting w = (x² + 1)/x this is (x − 1)²(x² + x + 1) ≤ x² + 1. For |x − 1| ≤ 1/2 the left side is ≤ (x² + x + 1)/4 and (x² + x + 1)/4 ≤ x² + 1 ⇔ 3x² − x + 3 ≥ 0, true for all x. (At x = 1 the first term of D'' vanishes and D''(1) < 0 directly.)
(c) ∂²_T f_n = 2k(m − 1)/T³ − (n − 2) D''(T) > 0 on [1/2, 3/2] by (b) and k ≥ 0. ∂_T f_n(1; H) = k ≥ 0 (D'(1) = 0), with equality only at H = 2; ∂_T f_n(1/2; H) = k(4 − 3m) − (n − 2) D'(1/2) < 0. So for H < 2 there is exactly one zero, in (1/2, 1), and it is the minimiser of f_n on [1/2, 3/2]. At the zero D'(T) > 0, so m − (m − 1)/T² > 0. Implicit differentiation: ∂_H ∂_T f_n = −(m − (m − 1)/T²) < 0 at T_n, so dT_n/dH = (m − (m − 1)/T²)/∂²_T f_n > 0. dF_n/dH = ∂_H f_n = −(mT + (m − 1)/T) by stationarity. At H = 2, f_n(T; 2) = n − (n − 2) D(T) has its unique minimum at T = 1. ∎

(d) T_n(H) is the global minimiser of f_n(·; H) over T > 0, so F_n(H) = min_{T > 0} f_n(T; H). Proof: for H < 2, if T < √((m − 1)/m) (< 1) both terms of ∂_T f_n = k(m − (m − 1)/T²) − (n − 2)D'(T) are negative (D' > 0 on (0, 1)), and if T > 1 both are positive; on the remaining interval [√((m − 1)/m), 1] ⊂ [1/2, 3/2] use (c). At H = 2, f_n = n − (n − 2)D(T) and D has its unique maximum at 1.
(e) For every even n ≥ 6 there is a unique H*(n) ∈ (√2, 2) with F_n(H*) = n. Proof (from the referee): by (d), mT + (m − 1)/T ≥ 2√(m(m − 1)) and D ≤ d0, F_n(√2) − n ≥ 2(2 − √2)√(m(m − 1)) − 2(m − 1)d0 ≥ (m − 1)(2(2 − √2) − 2d0) > 0, while F_n(2) − n = −(n − 2)d0 < 0; F_n is continuous and strictly decreasing on [√2, 2] by (c).

**Proposition 6.4 (the H = 2 value).** min_{F_n} Ψ_n(·; 2) = n − (n − 2) d0 = F_n(2) = Φ_M((0, π/4, …, π/4, 0); 2).

*Proof.* Lower bound: Corollary 6.1 at H = 2. Upper bound: at r = (1, −1, 1, …, 1) ∈ F_n every pair is (1, 1) and d(1, 1) = d0 (equality case of Lemma 6), so Lemma 5 gives n + 0 − (n − 2) d0. The chain value is computed in Lemma 7 (set H = 2). The global statement (all r ∈ R^{n−1}) is Theorem 10. ∎

## 3. The tangent bound

**Lemma 7 (tangent bound).** For every H ≤ 2, F_n(H) ≤ F_n(2) + (n − 1)(2 − H) = 4 + (2n − 4)√2 − (n − 1)H. For n = 6, 8, 10 the slope constant is 5, 7, 9.

*Proof.* T_n(H) minimises f_n on [1/2, 3/2] (Lemma 6.3(c)), so F_n(H) ≤ f_n(1; H) = n + k(2m − 1) − (n − 2) D(1) = F_n(2) + (n − 1)k. ∎

Chain-side check (not needed for the proof, but it identifies the bound as a chain value and so as an upper bound for inf Ψ_n by Lemma 2): at tilts (0, π/4, …, π/4, 0), for H ∈ [1 + √2/2, 2], the end gaps have dy = ±(H − 1/2 − √2/2) ∈ [1/2, 1/2 + √2/2] and κ(0, π/4, dy) = 1/2 + √2/2 − (|dy| − 1/2) = 3/2 + √2 − H (axis square plus diamond of radius √2/2), the n − 3 middle gaps have |dy| = H − √2 and κ(π/4, π/4, dy) = √2 − |dy| = 2√2 − H (two diamonds), and h(0) = 1/2. The sum is 1 + 2(3/2 + √2 − H) + (n − 3)(2√2 − H) = 4 + (2n − 4)√2 − (n − 1)H.

## 4. Slopes, clipping, the H = 2 endpoint, the box

**Lemma 8 (slopes).** Unchanged from `o2cert` (statements about A and m1): for x < 0, x ↦ A(x, y) is nondecreasing with slope ≤ 1/√(1 + x²), for every y; for y > 0, y ↦ A(x, y) is nonincreasing with slope ≥ −1/√(1 + y²), for every x; m1'(x) ≤ 2/(3√3) < 0.385 for x < 0. A is Lipschitz, so these one-sided slope bounds integrate.

**Lemma 9 (clipping).** Let c(H) := √(4/H² − 1) for H ∈ (1.385, 2] (c(2) = 0). Define P_H(r) coordinatewise: ρ_1 ↦ max(ρ_1, 0), ρ_{n−1} ↦ max(ρ_{n−1}, 0), and ρ_j ↦ max(ρ_j, −c(H)) for every interior j. Then Ψ_n(P_H(r); H) ≤ Ψ_n(r; H). At H = 2, P_2 maps R^{n−1} into F_n.

*Proof.* Clip one coordinate at a time; each slope bound below holds whatever the other coordinates are. An interior odd coordinate r_j (3 ≤ j ≤ n − 3) is the x of both pairs j − 1 and j, so Ψ_n depends on it through A(r_j, r_{j−1}) + A(r_j, r_{j+1}) − H r_j, whose slope for r_j < 0 is ≤ 2/√(1 + r_j²) − H by Lemma 8; this is ≤ 0 iff |r_j| ≥ c(H). So the function is nonincreasing on (−∞, −c(H)] and raising r_j to −c(H) does not increase Ψ_n. An even coordinate r_j (2 ≤ j ≤ n − 2, always interior) is the y of pairs j − 1 and j: Ψ_n depends on it through A(r_{j−1}, r_j) + A(r_{j+1}, r_j) + H r_j, with slope ≥ H − 2/√(1 + r_j²) ≥ 0 for r_j ≥ c(H); lower r_j to c(H). An end coordinate enters through m1(r_1) + A(r_1, r_2) − H r_1, with slope ≤ 0.385 + 1 − H < 0 for r_1 < 0; raise r_1 to 0 (same for r_{n−1}). ∎

There are n − 3 interior coordinates (m − 2 odd, m − 1 even), and after clipping each has wrong-sign part ρ_j⁻ ≤ c(H). c is decreasing in H; c(H*(6)) = 0.39350, c(H*(8)) = 0.40762, c(H*(10)) = 0.41547, c(1.86) = 0.39523, c(1.9) = 0.32868.

**Theorem 10 (H = 2).** Ψ_n(r; 2) ≥ n − (n − 2) d0 = F_n(2) for all r ∈ R^{n−1}, every even n ≥ 6.

*Proof.* Ψ_n(r; 2) ≥ Ψ_n(P_2(r); 2) ≥ F_n(2) by Lemma 9 and Corollary 6.1 at H = 2. ∎

**Corollary 10.1.** For all r and H: Ψ_n(r; H) = Ψ_n(r; 2) + (2 − H)(−σ(r)) ≥ F_n(2) + (2 − H)(−σ(r)). Hence, for H ≤ 2, −σ(r) ≥ n − 1 implies Ψ_n(r; H) ≥ F_n(2) + (n − 1)(2 − H) ≥ F_n(H) (Lemma 7).

*Proof.* Ψ_n depends on H only through Hσ. ∎

**Theorem 11 (reduction to K_n).** Let R_n(H) := (n − 1) + (n − 3) c(H) and K_n(H) := {r : ρ_1, ρ_{n−1} ∈ [0, R_n], ρ_j ∈ [−c(H), R_n] for interior j}. If Ψ_n(r; H) ≥ F_n(H) on K_n(H) for all H ∈ [H*(n), 2], then O2_n holds.

*Proof.* Let q = P_H(r). If −σ(q) = Σ ρ_j(q) ≥ n − 1, Corollary 10.1 applies. Otherwise the n − 3 interior coordinates contribute at least −(n − 3)c(H) to Σ ρ_j, so every ρ_j(q) ≥ 0 satisfies ρ_j(q) < (n − 1) + (n − 3)c(H), and q ∈ K_n(H). ∎

R_6(H*) = 6.1805, R_8(H*) = 9.0381, R_10(H*) = 11.9083 (n = 6 recovers 5 + 3·c, the old 6.14 with c = 0.38). The decomposition below does not need K_n: Lemma 20 cuts each block domain to a much smaller set directly.

## 5. Pair functions and the telescoping identity

An *admissible split* is a vector a = (a_1, …, a_{n−1}) with a_1 = 0, a_{n−1} = k and a_2, …, a_{n−2} arbitrary reals. Pair p receives the coefficient k − a_p on coordinate p and a_{p+1} on coordinate p + 1; c_x^p, c_Y^p denote the ones on its odd and even coordinate (p odd: c_x^p = k − a_p, c_Y^p = a_{p+1}; p even: c_x^p = a_{p+1}, c_Y^p = k − a_p). So each coordinate's coefficients over the pairs containing it add up to k, and μ_j := a_j − k/2 (2 ≤ j ≤ n − 2) are the multipliers of REPORT.md. Given two admissible splits a (used on right-sign values) and ã (used on wrong-sign values) define, with ρ⁺ = max(ρ, 0), ρ⁻ = max(−ρ, 0),

  g_p(x, Y) := A(x, −Y) − 1 − (1 − c_x^p) x⁺ + (1 − c̃_x^p) x⁻ − (1 − c_Y^p) Y⁺ + (1 − c̃_Y^p) Y⁻.

On x, Y ≥ 0 this is g_p = c_x^p x + c_Y^p Y − d(x, Y), the pair function of REPORT.md.

**Lemma 13 (telescoping).** For every two admissible splits and every r with ρ_1, ρ_{n−1} ≥ 0: Σ_{p=1}^{n−2} g_p(x_p, Y_p) = Ψ_n(r; H) − n. In particular this holds on F_n for every split, and the wrong-sign split ã is invisible on F_n.

*Proof.* Let N_j be the number of pairs containing coordinate j (2 for interior j, 1 for j = 1, n − 1). Summing the linear parts coordinate by coordinate, Σ_p g_p = Σ_p (A_p − 1) − Σ_j [(N_j − k) ρ_j⁺ − (N_j − k) ρ_j⁻] = Σ_p (A_p − 1) − Σ_j (N_j − k) ρ_j, because both splits give coordinate j total coefficient k. Since N_j − k = H + (N_j − 2) and N_j − 2 = −1 exactly at the two ends, this is Σ_p (A_p − 1) − H Σ_j ρ_j + ρ_1 + ρ_{n−1}. On the other hand Ψ_n − n = (m1(r_1) − 1) + (m1(r_{n−1}) − 1) + Σ_p (A_p − 1) + Hσ, with m1(r_1) − 1 = ρ_1 for ρ_1 ≥ 0 and Hσ = −H Σ ρ_j. ∎

## 6. Blocks and the decomposition lemma

A *scheme* is a partition of {1, …, n − 2} into blocks P of consecutive pairs; B_P := Σ_{p ∈ P} g_p is a function of the coordinates z_P of the pairs in P. A coordinate both of whose pairs lie in P is *internal* to P; B_P depends only on the sum k of its two coefficients, so splitting it inside P is a free choice of the proof, not of the scheme. The clipped domain is D_P(H) := {z_P : ρ_1, ρ_{n−1} ≥ 0 if present, ρ_j ≥ −c(H) for interior j}. z*_P denotes the restriction of r*(T_n(H)), i.e. every x = T and every Y = 1/T.

**Lemma 14 (decomposition).** (a) If B_P ≥ β_P on D_P(H) for every block of a scheme, then Ψ_n(r; H) ≥ n + Σ_P β_P for all r ∈ R^{n−1}.
(b) If β_P = B_P(z*_P) for every P, then Ψ_n ≥ Ψ_n(r*(T_n)) = F_n(H), i.e. O2_n at this H.
(c) Conversely, for every scheme and both splits, Σ_P inf_{D_P} B_P ≤ F_n(H) − n, with equality iff every block attains its infimum at z*_P. If moreover H = H*(n), equality also forces B_P(0) = B_P(z*_P) for every block.

*Proof.* (a) Let q = P_H(r). Then Ψ_n(r) ≥ Ψ_n(q) (Lemma 9), each z_P(q) ∈ D_P, and Ψ_n(q) − n = Σ_P B_P(z_P(q)) ≥ Σ β_P (Lemma 13). (b) Σ_P B_P(z*_P) = Ψ_n(r*) − n = F_n − n by Lemmas 13 and 6.3(a). (c) inf_{D_P} B_P ≤ B_P(z*_P), sum over P. At H = H*(n), Σ_P B_P(0) = Ψ_n(0) − n = 0 = Σ_P B_P(z*_P), and B_P(0) ≥ inf B_P = B_P(z*_P) for each P. ∎

So the block obligations are *attained* inequalities: each block function has its global minimum, with value exactly B_P(z*_P), at the interior point z*_P, and at H = H*(n) a second one at 0. No finite interval enclosure can prove such an inequality by itself. It must be split into a local statement near z*_P (Lemmas 16–17, proved below), a local statement near 0 used only for H near H*(n) (Lemmas 21 and 21', proved below), and a strict inequality on the rest of a bounded domain (Lemma 20 gives the bound), which is what §11 asks the program to certify.

## 7. Local structure at the Morandi point

**Lemma 15 (deficit structure and the ridge).** For x, Y > 0:
(a) d(x, Y) = max(0, dX(x, Y), dY(x, Y)), dX as in Lemma 6, dY(x, Y) = dX(Y, x).
(b) On the hyperbola xY = 1, dX = dY = D(x). dX is, for fixed x, a tent in Y with apex on the hyperbola: affine with slope ψ(x) := 1 − 1/√(1 + x²) ∈ [0, 1) for Y ≤ 1/x and affine with slope 1 − q(x) ≤ 0 for Y ≥ 1/x. dY is the same tent in x with apex at x = 1/Y.
(c) (ridge dichotomy) sign(dX − dY) = sign((Y − x)(1 − xY)). Explicitly, dX − dY = (R_x − R_Y)(x + Y − R_x R_Y)/(R_x R_Y) for xY ≤ 1 and dX − dY = (x + Y)(q(Y) − q(x)) for xY ≥ 1. So dX and dY coincide exactly on the hyperbola and on the diagonal x = Y.
(d) Consequently, near the Morandi point (T, 1/T) with T < 1 (so x < Y): below the hyperbola d = max(0, dX) (the x-kink is active), above it d = max(0, dY) (the y-kink is active). At T = 1 (H = 2) the point (1, 1) lies on both switching curves and the four sectors meet there.

*Proof.* (a) For x > 0 > y = −Y the candidates of Lemma 3 are E (at t = 0, π/2) and the two kinks tan t = x, tan t = 1/Y; dX = E − Kx (Lemma 6). The symmetry A(x, y) = A(−y, −x) gives d(x, Y) = d(Y, x) and maps the kink tan t = 1/Y of (x, −Y) to the kink tan t = Y of (Y, −x), so E − Ky = dX(Y, x).
(b) The branch formulas of Lemma 6, rewritten with x²/(R(R + 1)) = (R − 1)/R = ψ(x); q(x) ≥ 1 for x ≥ 0. Both branches give D(x) at Y = 1/x (Lemma 6), and dY(x, 1/x) = dX(1/x, x) = D(1/x) = D(x).
(c) For xY ≤ 1 both are first branches: dX − dY = (x + Y)(1/R_Y − 1/R_x) − (R_x − R_Y) = (R_x − R_Y)[(x + Y)/(R_x R_Y) − 1]. Now (x + Y)² − (1 + x²)(1 + Y²) = −(1 − xY)² ≤ 0, so x + Y − R_x R_Y < 0 off the hyperbola, and sign(R_x − R_Y) = sign(x − Y); together sign(dX − dY) = sign(Y − x). For xY ≥ 1 both are second branches: dX − dY = (x + Y)(q(Y) − q(x)), and q(u)² = 1 + 2/(u + 1/u) is a decreasing function of u + 1/u; (x + 1/x) − (Y + 1/Y) = (x − Y)(1 − 1/(xY)), whose sign is sign(x − Y) when xY > 1, so sign(dX − dY) = sign(x − Y). Both cases equal sign((Y − x)(1 − xY)). (d) follows from (a) and (c). ∎

Write ℓ(u) := c_x u + c_Y/u − D(u) for the value of c_x x + c_Y Y − d along the ridge (when d > 0 there).

**Lemma 16 (local tightness, pair).** Let T ∈ [1/2, 3/2], c_x ≥ 0 and c_Y ∈ R (not necessarily ≥ 0) with the tangential condition
  (Tan) c_x − c_Y/T² = D'(T).
Let N = [x_−, x_+] × [Y_−, Y_+] ∋ (T, 1/T) with x_−, Y_− > 0, and suppose
  (J) J := [min(x_−, 1/Y_+), max(x_+, 1/Y_−)] ⊂ [1/2, 3/2];
  (N1) c_Y ≤ ψ(x_−);  (N1') c_x ≤ ψ(Y_−);
  (N2') c_x x_− + min(c_Y Y_−, c_Y Y_+) ≥ c_x T + c_Y/T − D(T);
  (N3) c_Y ≥ 1 − min(q(x_−), q(x_+));
  (L) ℓ''(u) = 2c_Y/u³ − D''(u) > 0 for every u ∈ J.
Then g(x, Y) := c_x x + c_Y Y − d(x, Y) ≥ g(T, 1/T) = ℓ(T) for all (x, Y) ∈ N.
If c_Y ≥ 0, then (N3) and (L) hold automatically (q ≥ 1 on [0, ∞); D'' < 0 on [1/2, 3/2] by Lemma 6.3(b)) and (N2') is equivalent to
  (N2) c_x (T − x_−) + c_Y (1/T − Y_−) ≤ D(T).

*Proof.* By Lemma 15(a), g = min(c_x x + c_Y Y, c·z − dX, c·z − dY), so it suffices to bound the three terms below by ℓ(T).
(i) On N, c_x x + c_Y Y ≥ c_x x_− + min_{Y ∈ [Y_−, Y_+]} c_Y Y = c_x x_− + min(c_Y Y_−, c_Y Y_+) (c_x ≥ 0; a linear function of Y is minimised at an endpoint), and this is ≥ c_x T + c_Y/T − D(T) = ℓ(T) by (N2').
(ii) Fix x ∈ [x_−, x_+]. By Lemma 15(b), c·z − dX(x, Y) = ℓ(x) + (Y − 1/x)(c_Y − ψ(x)) for Y ≤ 1/x and = ℓ(x) + (Y − 1/x)(c_Y − 1 + q(x)) for Y ≥ 1/x. In the first case Y − 1/x ≤ 0 and c_Y − ψ(x) ≤ c_Y − ψ(x_−) ≤ 0 (ψ increasing, (N1)). In the second, Y − 1/x ≥ 0, and q'(u) = (1 − u)/(1 + u²)^{3/2}, so q increases on [0, 1] and decreases on [1, ∞) and q(x) ≥ min(q(x_−), q(x_+)) on [x_−, x_+]; by (N3), c_Y − 1 + q(x) ≥ 0. So c·z − dX ≥ ℓ(x) for every Y > 0.
(iii) Fix Y ∈ [Y_−, Y_+]. In the same way c·z − dY(x, Y) = ℓ(1/Y) + (x − 1/Y)(c_x − ψ(Y)) for x ≤ 1/Y and = ℓ(1/Y) + (x − 1/Y)(c_x − 1 + q(Y)) for x ≥ 1/Y. The first correction is ≥ 0 by (N1') (ψ(Y) ≥ ψ(Y_−)), the second because c_x ≥ 0 and q(Y) ≥ 1. So c·z − dY ≥ ℓ(1/Y) for every x > 0.
(iv) x ∈ [x_−, x_+] ⊂ J and 1/Y ∈ [1/Y_+, 1/Y_−] ⊂ J. By (L), ℓ is strictly convex on the interval J, and ℓ'(T) = c_x − c_Y/T² − D'(T) = 0 by (Tan) with T ∈ J; so ℓ ≥ ℓ(T) on J. ∎

No second-derivative bound on the smooth pieces is needed: for fixed x (resp. Y) each kink candidate is piecewise affine in the transversal variable, affine on each side of the ridge with a slope change on the ridge (it is not one affine function through the ridge), so the transversal analysis is exact. The only curvature that enters is that of the ridge function ℓ, through (L). The neighbourhood size is limited only by (J), (N1), (N1'), (N2'), (N3), (L).

Why c_Y is allowed to be negative. At the true parameters every c_Y used below is ≥ 0 (Lemma 18(c), Lemma 19(d)). But Lemma 17' asks for the hypotheses on a whole parameter rectangle [T_lo, T_hi] × [H_a, H_b], and on a cell ending at H_b = 2 the strict root bracket forces T_lo < 1 (∂_T f_n(T; 2) = −(n − 2)D'(T) vanishes only at T = 1). At (T_lo, 2) the coefficient formula of Lemma 19(d) gives c_x = 0 and c_Y = −T_lo² D'(T_lo) < 0 (about −1.2e-5 for T_lo = 0.9999; found by the SPEC implementer). The statement above tolerates this: (N3) and (L) have slack about 0.4 and 0.048 there (§12), and (N2') replaces (N2).

*Remark (normal-slope condition).* Let T < 1, c_x ≥ 0, and assume (Tan) and (L) on a neighbourhood of T (ℓ'' > 0 there). Then the transverse condition c_Y ∈ I(T), where
  I(T) := (T² (1 − q(T) − D'(T)), ψ(T)),
is sufficient for (T, 1/T) to be a strict local minimiser of g. At an endpoint of I(T) one affine transverse segment is flat, so the minimum is not strict; if c_Y lies outside the closure of I(T) there is a descent direction. Without (L) the transverse condition is not sufficient. Referee's example: T = 1/2, c_x = 0, c_Y = −T²D'(T) = −0.0326238 satisfies (Tan) and lies in I(1/2) = (−0.11803, 0.10557), but ℓ''(1/2) = −0.0645 and ℓ(0.501) − ℓ(0.5) = −3.19e−8, a descent along the ridge. Lemma 16 and Theorem 22 assume (L), so nothing downstream changes. (By Lemma 15(d) the active pieces near the point are dX below and dY above the hyperbola. Moving down from the point at x = T changes g by (Y − 1/T)(c_Y − ψ(T)), moving right at Y = 1/T changes it by (x − T)(c_x − 1 + q(T)), and c_x − 1 + q(T) > 0 ⇔ c_Y > T²(1 − q(T) − D'(T)) under (Tan); along the ridge ℓ is strictly convex by (L).) Numerically I(0.888) = (−0.337, 0.252), I(0.937) = (−0.370, 0.270), I(0.999) = (−0.414, 0.293); at the true parameters every c_Y used below is in [0, 0.127] and every c_x in [0, 0.154]. The interval quoted in REPORT.md, ≈ [−0.54, 0.42], is in a different, unstated normalisation and is not used. (N1), (N1') and (N3) are uniform sufficient forms of this condition on a box and remain valid at T = 1.

**Lemma 17 (local tightness, blocks).** Let P be a block whose orthant function is B_P = Σ_v C_v v − Σ_{p ∈ P} d(x_p, Y_p) (v over the coordinates of P). If the coefficient of each internal coordinate can be split between its two pairs so that every pair of P satisfies the hypotheses of Lemma 16 with the same T and box factors I_x = [x_−, x_+], I_Y = [Y_−, Y_+], then B_P ≥ B_P(z*_P) on the product box N_P := Π_{odd v} I_x × Π_{even v} I_Y. For a 3-variable block {(2j − 1, 2j), (2j + 1, 2j)} (shared Y), B_P(·, Y, ·) separates for fixed Y into two one-variable problems, and the statement is the pair lemma applied to both sides.

*Proof.* B_P = Σ_{p ∈ P} g_p with the chosen split, each g_p ≥ g_p(T, 1/T) on its factor of N_P, and Σ_p g_p(T, 1/T) = B_P(z*_P). ∎

**Lemma 17' (interval parameters).** Let [H_a, H_b] be an H-cell and T_n(H) ∈ [T_lo, T_hi] for all H in the cell. Suppose the coefficients of the pairs are explicit functions c(T, H) with c_x ≥ 0 that satisfy (Tan) identically at T = T_n(H) (Lemma 18), and that (J), (N1), (N1'), (N2'), (N3), (L) hold for all (T, H) ∈ [T_lo, T_hi] × [H_a, H_b] with one fixed box N such that (T, 1/T) ∈ N for all T ∈ [T_lo, T_hi]. (c_Y ≥ 0 is not required on the rectangle.) Then for every H in the cell, every block of the scheme satisfies B_P ≥ B_P(z*_P(H)) on N_P.

*Proof.* At the true point (T_n(H), H), which lies in the parameter box, all hypotheses of Lemma 16 hold, (Tan) exactly. Internal coordinates are split by the pair coefficients of Lemma 18, which sum to the block coefficient exactly at the true point (Lemma 19(d)). ∎

So the stationarity equation is never checked with intervals; only inequalities are, and over a parameter box that contains the true (T_n(H), H).

## 8. Stationarity and the even-star scheme

**Lemma 18 (stationary split).** For H < 2 and T > 0 consider the n − 2 tangential equations c_x^p − c_Y^p/T² = D'(T), p = 1, …, n − 2, in the n − 3 unknowns a_2, …, a_{n−2}.
(a) Equations p = 1, …, n − 3 have a unique solution (the system is triangular with nonzero diagonal), so the coefficient matrix has rank n − 3. Equation n − 2 holds as well iff T solves (T-eq), i.e. iff T = T_n(H) in [1/2, 3/2].
(b) When T solves (T-eq), the solution of the full system is, with k = 2 − H,
  a_{2i+1} = k i/(m − 1) (0 ≤ i ≤ m − 1),  a_{2i} = k/2 + (k T²/2)(m − 2i)/(m − 1) (1 ≤ i ≤ m − 1),
  i.e. μ_{2i+1} = k(i/(m − 1) − 1/2) (independent of T) and μ_{2i} = (k T²/2)(m − 2i)/(m − 1). For other T the first n − 3 equations are solved by the recurrence of the proof (μ_{2i+1} = −k/2 − 2iβ, μ_{2i} = T²(β + k/2 + 2(i − 1)β), β = k(1 − T^{−2})/2 − D'(T)), not by this closed form.
(c) μ_{n−j} = −μ_j (antisymmetry), μ_m = 0 (for m even and for m odd), and every pair coefficient is ≥ 0 for T ≤ 1. The pair coefficients are: pair 2i + 1 (0 ≤ i ≤ m − 2): c_x = k(m − 1 − i)/(m − 1), c_Y = (k/2)(1 + T²(m − 2 − 2i)/(m − 1)); pair 2i (1 ≤ i ≤ m − 1): c_x = k i/(m − 1), c_Y = (k/2)(1 − T²(m − 2i)/(m − 1)). Every pair has c_Y = T²(c_x − D'(T)).

*Proof.* Put β := k(1 − T^{−2})/2 − D'(T). Equation p reads, for odd p, k − a_p − a_{p+1}/T² = D'(T), i.e. μ_{p+1} = T²(β − μ_p); for even p, a_{p+1} − (k − a_p)/T² = D'(T), i.e. μ_{p+1} = −β − μ_p/T². Starting from μ_1 = −k/2 this determines μ_2, …, μ_{n−2} uniquely from equations 1, …, n − 3, and two steps compose to μ_{p+2} = μ_p − 2β (p odd). Hence μ_{2i+1} = −k/2 − 2iβ and μ_{2i} = T²(β + k/2 + 2(i − 1)β). The last equation (p = n − 2, even) holds iff μ_{n−1} = k/2, i.e. −k/2 − 2(m − 1)β = k/2, i.e. β = −k/(2(m − 1)), i.e. D'(T) = (k/2)(1 + 1/(m − 1) − 1/T²), which is (T-eq) divided by 2(m − 1). Substituting β gives (b). Antisymmetry: n − (2i + 1) = 2(m − 1 − i) + 1 and n − 2i = 2(m − i) in the formulas. Nonnegativity: |T²(m − 2 − 2i)/(m − 1)| ≤ T² ≤ 1. The relation c_Y = T²(c_x − D') is (Tan). ∎

For n = 8, H = 1.9 (T = 0.9321368): μ = (+0.02896, −0.01667, 0, +0.01667, −0.02896), REPORT.md's numbers; the closed form agrees with REPORT's task2.json multipliers to 2e-16 at all 12 (n, H) there.

**Certified handling of T_n(H).** On an H-cell [H_a, H_b] pick rationals T_lo < T_hi and verify with outward rounding ∂_T f_n(T_lo; H) < 0 < ∂_T f_n(T_hi; H) at H = H_a and H = H_b; since ∂_T f_n(T; H) = k(m − (m − 1)/T²) − (n − 2)D'(T) is affine in H for fixed T, the signs hold on the whole cell, and by the intermediate value theorem and Lemma 6.3(c) T_n(H) ∈ (T_lo, T_hi) for every H in the cell. The coefficients of Lemma 18(b) are then intervals and Lemma 17' applies. F_n(H) is never needed exactly: F_n(H) ≤ f_n(T̂; H) for any T̂ (Lemma 6.3(c)), and f_n(T̂; H) is affine in H.

**Definition (even-star scheme).** For 1 ≤ j ≤ m − 1, block j consists of the two pairs that contain the even coordinate 2j: pairs 2j − 1 = (2j − 1, 2j) and 2j = (2j + 1, 2j). Its variables are x_l := ρ_{2j−1}, Y := ρ_{2j}, x_r := ρ_{2j+1}. The even coordinate is internal, so only the split of the odd coordinates matters: on right-sign values use Lemma 18 (a_{2i+1} = k i/(m − 1)); on wrong-sign values of interior odd coordinates use the reversed split ã_{2i+1} := k(m − 1 − i)/(m − 1), 1 ≤ i ≤ m − 2 (ã_1 = 0, ã_{n−1} = k; end coordinates are never wrong-sign on D_P). The block function is

  B_j(x_l, Y, x_r) = s(x_l, Y; β_j, β̃_j) + s(x_r, Y; α_j, α̃_j) − (2 − k) Y,  s(x, Y; c, c̃) := A(x, −Y) − 1 − (1 − c) x⁺ + (1 − c̃) x⁻,

  β_j = k(m − j)/(m − 1), α_j = k j/(m − 1), β̃_j = k(j − 1)/(m − 1), α̃_j = k(m − 1 − j)/(m − 1),

on D_j(H) = {x_l ≥ −c(H) (≥ 0 if j = 1), Y ≥ −c(H), x_r ≥ −c(H) (≥ 0 if j = m − 1)}. On the orthant B_j = β_j x_l + kY + α_j x_r − d(x_l, Y) − d(x_r, Y). Blocks j and m − j are mirror images (x_l ↔ x_r), so only j ≤ m/2 need be checked.

**Lemma 19 (even-star scheme).** (a) Σ_{j=1}^{m−1} B_j = Ψ_n − n whenever ρ_1, ρ_{n−1} ≥ 0.
(b) B_j(T, 1/T, T) = 2(f_n(T; H) − n)/(n − 2) for every j and T; at T = T_n(H) it is 2(F_n(H) − n)/(n − 2) =: rhs_n(H), the same for all blocks, ≤ 0 iff H ≥ H*(n).
(c) The block functions depend on H only through k (affinely), not on T.
(d) B_j ≥ rhs_n(H) on N_{1/4} := [T − 1/4, T + 1/4] × [1/T − 1/4, 1/T + 1/4] × [T − 1/4, T + 1/4], T = T_n(H), for every H ∈ [H_lo(n), 2] and n ∈ {6, 8, 10}, given the scalar checks (H0) of §11.
(e) The odd split is forced: if a scheme of even-star type (any split of the odd coordinates) has every block minimised at z*, then a_{2j+1} − a_{2j−1} = k/(m − 1) for all j, i.e. the split of Lemma 18.

*Proof.* (a) Lemma 13 with the stated splits (the even split is irrelevant because each even coordinate is internal to its block). (b) β_j + α_j = km/(m − 1), so B_j(T, 1/T, T) = kmT/(m − 1) + k/T − 2D(T) = (2/(n − 2))[k(mT + (m − 1)/T) − (n − 2)D(T)]. (c) Read off. (d) Split Y's coefficient as γ_l = T²(β_j − D'(T)), γ_r = T²(α_j − D'(T)); then γ_l + γ_r = T²(km/(m − 1) − 2D'(T)) = k by (T-eq), so this is a legal split, and the pairs (β_j, γ_l), (α_j, γ_r) satisfy (Tan) — they are the pair coefficients of Lemma 18. Check Lemma 16 on N_{1/4}(T) for T ∈ [T_0, 1] (T_n is increasing, Lemma 6.3(c)), using T_n(H_lo(n)) ≥ T_0 = 0.887 (n = 6), 0.919 (n = 8), 0.936 (n = 10), which is the certified sign check ∂_T f_n(T_0; H_lo) < 0 in (H0), and k ≤ 2 − H_lo(n) ≤ 0.1531: (J) T − 1/4 ≥ 0.637 ≥ 1/2, 1/(1/T + 1/4) ≥ 1/(1/0.887 + 1/4) ≥ 0.726, T + 1/4 ≤ 5/4, 1/(1/T − 1/4) ≤ 1/(1 − 1/4) = 4/3; (N1) γ ≤ T²β ≤ k ≤ 0.139, 0.148, 0.154 against ψ(T − 1/4) ≥ ψ(0.637), ψ(0.669), ψ(0.686) ≈ 0.1566, 0.1688, 0.1754 (for n = 6, 8, 10; values rounded down); (N1') c_x ≤ k ≤ 0.154 < 0.2 = ψ(3/4) ≤ ψ(1/T − 1/4); (N2) (c_x + γ)/4 ≤ 2k/4 ≤ 0.077 < 0.1707 ≈ D(0.887) ≤ D(T); and γ ≥ T²k/(2(m − 1)) ≥ 0 because D'(T) = (k/2)(1 + 1/(m − 1) − 1/T²) ≤ k/(2(m − 1)). Lemma 17 finishes. (e) Restrict B_j to the curve Y ↦ (1/Y, Y, 1/Y), which passes through z* at Y = 1/T and on which both pairs sit on their ridges, so d = D(1/Y) for both (Lemma 15(b)) and B_j = Λ_j(Y) := kY + (β_j + α_j)/Y − 2D(1/Y). An interior minimum at Y = 1/T forces Λ_j'(1/T) = k − (β_j + α_j)T² + 2T²D'(T) = 0, i.e. β_j + α_j = k/T² + 2D'(T) = km/(m − 1) by (T-eq). With β_j = k − a_{2j−1}, α_j = a_{2j+1} this is a_{2j+1} − a_{2j−1} = k/(m − 1), and a_1 = 0 fixes the split. ∎

Relation to REPORT.md. For n = 6 the even-star blocks are REPORT's two end triples. For n = 8 REPORT's scheme (two end triples, middle pairs 3 and 4 single) is the even-star scheme with block 2 split into its pairs; since inf(g_3 + g_4) ≥ inf g_3 + inf g_4, the even-star obligations are implied by REPORT's. For n = 10 the same holds with blocks 2 and 3 split. The decisive difference is the origin: single pairs of the stationary split have values at z* equal to rhs_n/2 + kT(m − 2 − 2i)/(m − 1) (pair 2i + 1) and rhs_n/2 − kT(m − 2i)/(m − 1) (pair 2i) (from Lemma 18; consecutive pairs 2i + 1, 2i + 2 cancel, which is why the even-star blocks all equal rhs_n), and some of these are positive before H reaches H*(n) for n ≥ 10 (REPORT's failure at pair 3), whereas every even-star block has the value rhs_n ≤ 0.

## 9. Slivers, tails and the origin

**Lemma 20 (slivers and tail).** (a) For every pair function and all (x, Y): g_p(x, Y) ≥ g_p(x⁺, Y⁺) − c̃_x x⁻ − c̃_Y Y⁻.
(b) On D_j(H), B_j(z) ≥ β_j x_l⁺ + kY⁺ + α_j x_r⁺ − 2d0 − c(H)(β̃_j + α̃_j + k). Hence B_j(z) > rhs_n(H) whenever β_j x_l⁺ + kY⁺ + α_j x_r⁺ > Θ_j(H) := rhs_n(H) + 2d0 + c(H)(β̃_j + α̃_j + k).
(c) For H < 2, Θ_j(H)/k ≤ 2(n − 1)/(n − 2) + c(H)(2m − 3)/(m − 1), so the region left over is bounded uniformly in H ∈ [H_lo(n), 2) (H = 2 is Theorem 10): Y⁺ ≤ Θ_j/k, x_l⁺ ≤ Θ_j/β_j, x_r⁺ ≤ Θ_j/α_j.

*Proof.* (a) By Lemma 8, A(x, y) ≥ A(0, y) − x⁻ (x < 0, slope ≤ 1) and A(x', y) ≥ A(x', 0) − y⁺ (y > 0, slope ≥ −1); with y = −Y this is A(x, −Y) ≥ A(x⁺, −Y⁺) − x⁻ − Y⁻. The linear part of g_p changes by (1 − c̃_x)x⁻ + (1 − c̃_Y)Y⁻ when (x, Y) is replaced by its projection, which leaves −c̃_x x⁻ − c̃_Y Y⁻ in total. (b) Apply (a) to both pairs of block j; on D_j the wrong-sign parts are ≤ c(H) and their coefficients add to β̃_j + α̃_j + k; at the projection B_j = β_j x_l⁺ + kY⁺ + α_j x_r⁺ − d − d ≥ … − 2d0 (Lemma 6). (c) rhs_n + 2d0 = (2/(n − 2))(F_n − F_n(2)) ≤ 2(n − 1)k/(n − 2) by Lemma 7, and β̃_j + α̃_j = k(m − 2)/(m − 1). ∎

For the weakest variable (coefficient k/(m − 1)) the bound in (c) is (n − 1) + (n − 3)c(H) = R_n(H), the K_n box of Theorem 11 again; all other variables are cut much shorter (table in §11).

**Lemma 21 (origin).** (a) For |x|, |Y| ≤ 1/2: A(x, −Y) ≥ 1 + (x + Y)⁺ − x² − Y².
(b) Every pair function satisfies g_p ≥ (x + Y)⁻ + c_x x⁺ − c̃_x x⁻ + c_Y Y⁺ − c̃_Y Y⁻ − x² − Y² there.
(c) For the even-star block j, with κ0 := k/(m − 1): B_j(z) ≥ κ0 |z|_∞ − 4|z|²_∞ on D_j ∩ {|z|_∞ ≤ 1/2}. In particular B_j ≥ 0 ≥ rhs_n(H) on N_0 := {|z|_∞ ≤ κ0/4} for H ∈ [H*(n), 2], and B_j ≥ κ0²/16 on {|z|_∞ = κ0/8}.

*Proof.* (a) Write u = x⁻, v = Y⁻ and use 1/√(1 + s²) ≥ 1 − s²/2. Quadrant x, Y ≥ 0: dX, dY ≤ 0 because x + Y ≤ 1 ≤ R_x, R_Y (first branches, Lemma 6), so A = E = 1 + x + Y. Quadrant x = −u ≤ 0 ≤ Y: E = 1 + Y, and the two kinks of Lemma 3 (tan t = 1/u, tan t = 1/Y) evaluate to
K1 = (2 − u + Y + 2uY + |u − Y|)/(2R_u), K2 = (2 + Y − u + 2Y² + |Y − u|)/(2R_Y).
If Y ≥ u: K1 = (1 + Y − u + uY)/R_u ≥ (1 + Y − u) − 0.875u² (the numerator is ≤ 1.75) and K2 = (1 + Y − u + Y²)/R_Y ≥ (1 + Y − u) + Y²(1 − (1 + Y + Y²)/2) ≥ 1 + Y − u. If Y < u: K1 = (1 + uY)/R_u ≥ 1 − 0.625u², K2 = R_Y ≥ 1, and (x + Y)⁺ = 0. So A ≥ 1 + (x + Y)⁺ − u². Quadrant x ≥ 0 ≥ Y: apply the previous case to A(x, −Y) = A(Y, −x) (symmetry), which gives the bound with Y² in place of u². Quadrant x = −u, Y = −v both ≤ 0: E = 1, the kinks are tan t = 1/u and tan t = v and both evaluate to (1 − uv)/R_u resp. (1 − uv)/R_v (the second by the same symmetry), so A ≥ 1 − uv − max(u, v)²/2 ≥ 1 − u² − v², and (x + Y)⁺ = 0.
(b) g_p = (A − 1) − (x + Y) + c_x x⁺ − c̃_x x⁻ + c_Y Y⁺ − c̃_Y Y⁻ and (x + Y)⁺ − (x + Y) = (x + Y)⁻.
(c) Summing (b) over the two pairs, the Y-coefficients add to k on both signs: B_j ≥ B1 − (x_l² + x_r² + 2Y²) with B1 = kY + σ_l + σ_r, σ(x, Y) := (x + Y)⁻ + c x⁺ − c̃ x⁻, (c, c̃) = (β_j, β̃_j) resp. (α_j, α̃_j). Lower bounds for σ: if Y ≥ 0, σ = c x for x ≥ 0 and σ ≥ −c̃Y + (1 − c̃)(x⁻ − Y)⁺ for x < 0; if Y = −v < 0, σ ≥ c·max(x, v) for x ≥ 0 and σ = v + (1 − c̃)x⁻ for x < 0. Put κ1 := k − β̃_j − α̃_j = k/(m − 1) (for j = 1 or m − 1 the end side is never negative and κ1 = k − α̃_1 = k/(m − 1) as well) and κ2 := β_j + α_j − k = k/(m − 1). For Y ≥ 0: B1 ≥ κ1 Y + Σ_s [c_s x_s⁺ + (1 − c̃_s)(x_s⁻ − Y)⁺], which is ≥ min(κ1, c_l, c_r, 1 − c̃_l, 1 − c̃_r)|z|_∞ by inspecting which coordinate attains |z|_∞. For Y = −v < 0: B1 ≥ κ2 v + Σ_s [c_s (x_s⁺ − v)⁺ + (1 − c̃_s) x_s⁻] (using v + (1 − c̃)u ≥ c v + (1 − c̃)u), again ≥ min(κ2, c_l, c_r, 1 − c̃_l, 1 − c̃_r)|z|_∞. Here c_l, c_r ≥ k/(m − 1) and 1 − c̃ ≥ 1 − k, so B1 ≥ κ0|z|_∞, and the remainder is ≤ 4|z|²_∞. ∎

**Lemma 21' (origin, five-variable block; the referee's repair).** Let L be the block of §11 for n = 10, 0 < k ≤ 1, and z = (x_1, Y_2, x_3, Y_4, x_5) ∈ D_L (so x_1 ≥ 0) with |z|_∞ ≤ 1/2. Then B_L(z) ≥ (k/2)|z|_∞ − 8|z|²_∞. Hence B_L ≥ 0 ≥ rhs_L on N_0^L := {|z|_∞ ≤ k/16}, and B_L ≥ k²/128 on {|z|_∞ = k/32}. The first-order constant k/2 is sharp (attained at (0, 1, −1, 1, −1)); without x_1 ≥ 0 the first-order part equals −k/2 at (−1, 1, −1, 1, −1), a point outside D_L.

*Proof.* Apply Lemma 21(b) to the four pairs (x_1, Y_2), (x_3, Y_2), (x_3, Y_4), (x_5, Y_4). Inside L the coefficients of Y_2, x_3, Y_4 add to k on both signs, x_1 has k, and x_5 has k/2 on both signs (a_5 = ã_5 = k/2). The eight squared terms are x_1², Y_2², x_3², Y_2², x_3², Y_4², x_5², Y_4², at most 8|z|²_∞ in total. So B_L ≥ B1_L − 8|z|²_∞ with
B1_L = kx_1 + kY_2 + kx_3 + kY_4 + (k/2)x_5 + Σ_{i=1}^{4} s_i⁻,  s_1 = x_1 + Y_2, s_2 = Y_2 + x_3, s_3 = x_3 + Y_4, s_4 = Y_4 + x_5.
Since Σ_i s_i = x_1 + 2Y_2 + 2x_3 + 2Y_4 + x_5, B1_L = (k/2)x_1 + Σ_i [(k/2)s_i + s_i⁻] = (k/2)x_1 + Σ_i [(k/2)s_i⁺ + (1 − k/2)s_i⁻] ≥ (k/2)(x_1 + Σ_i |s_i|), using x_1 ≥ 0 and 1 − k/2 ≥ k/2. Successively |Y_2| ≤ |s_1| + x_1, |x_3| ≤ |s_2| + |Y_2|, |Y_4| ≤ |s_3| + |x_3| and |x_5| ≤ |s_4| + |Y_4|, so |z|_∞ ≤ x_1 + Σ_i |s_i|. The two consequences follow from (k/2)ρ − 8ρ² ≥ 0 for ρ ≤ k/16 and = k²/128 at ρ = k/32. ∎

Lemma 21 is where the reversed wrong-sign split is needed: with ã = a (the orthant split) a middle even-star block has κ1 = k − (β_j + α_j) = −k/(m − 1) < 0 and dips below 0 next to the origin along x_l = x_r = −Y < 0, by about −k²/(4(m − 1)²) (seen numerically: −5.9e-4 for n = 8 at H = H*(8) + 1e-4 with the orthant split in the slivers; `explore_origin.log`). With the reversed split the dip is gone.

## 10. Assembly

**Theorem 22.** Let n ∈ {6, 8, 10} and H_lo(n) := 1.861098, 1.852049, 1.846936 (rationals). Suppose the program certifies (H0), (T), (Loc) and (C) of §11 for the scheme of §11 on H-cells covering [H_lo(n), 2]. Then Ψ_n(r; H) ≥ F_n(H) for all r ∈ R^{n−1} and all H ∈ [H_lo(n), 2], i.e. O2_n holds on [H_lo(n), 2].

The interval [H*(n), H_lo(n)) (length < 1e-6 in each case) is **not** covered. Any scheme achieving equality in Lemma 14(c) at H* must have both z* and 0 as minimisers of every block; the n = 10 even-star end block shows this fails there. Covering [H*(n), H_lo(n)) would need a root-constrained boundary certificate, which is not part of this reduction.

*Proof.* At H = 2 this is Theorem 10. Let H ∈ [H_lo(n), 2). By (H0) and the monotonicity of F_n (Lemma 6.3(c)), F_n(H) < n, so rhs_P(H) < 0 for every block. By Lemma 14(a),(b) it suffices that B_P ≥ rhs_P on D_P for each block, and this is assembled from four pieces. On the part of D_P outside the coordinate caps of §11, it is Lemma 20(b),(c); the caps contain the tail-cut set {Σ_v C_v v⁺ ≤ Θ_P(H)} for every H < 2. On N_cell it is Lemmas 16, 17 and 17' via (Loc) and (T). On N_0 it is Lemma 21 (triples) or Lemma 21' (the 5-variable block), because rhs_P < 0. On the rest it is (C). ∎

Mechanics on an H-cell [H_a, H_b] (all with outward rounding). This is exactly what the program checks.
1. (T) Choose rationals T_lo < T_hi with T_hi − T_lo ≤ 1/4. Check ∂_T f_n(T_lo; H_e) < 0 < ∂_T f_n(T_hi; H_e) at H_e = H_a and H_e = H_b. ∂_T f_n is affine in H, so the signs hold on the cell, and T_n(H) ∈ (T_lo, T_hi) there (§8). On a cell ending at 2, necessarily T_lo < 1 < T_hi.
2. (Loc) Take the fixed box N_cell := I_x × I_Y × I_x (resp. its five-factor product for L), with I_x = [T_hi − 1/4, T_lo + 1/4] and I_Y = [1/T_lo − 1/4, 1/T_hi + 1/4], rounded inward. Then check, on the stored rounded endpoints (x_−, x_+) of I_x and (Y_−, Y_+) of I_Y and with directed rounding, that x_− ≤ T_lo ≤ T_hi ≤ x_+ and Y_− ≤ 1/T_hi ≤ 1/T_lo ≤ Y_+. This makes N_cell nonempty and contains (T, 1/T) for every T ∈ [T_lo, T_hi]. If the check fails, reject or subdivide the cell. T_hi − T_lo ≤ 1/4 alone does not imply the Y part: with T_lo = 0.76 and T_hi = 1.01, (1, 1) is excluded.
   For each pair of the block, take c_x ∈ {β_j, α_j} (for L: k, k/4, 3k/4, k/2) as an interval function of H and c_Y := T²(c_x − D'(T)) as an interval function of (T, H). Over the whole rectangle [T_lo, T_hi] × [H_a, H_b], check (J), (N1), (N1'), (N2'), (N3) and (L) of Lemma 16 with (x_−, x_+, Y_−, Y_+) taken from N_cell.
   For (L), check c_Y > sup_{u ∈ J} u³ D''(u)/2, with D'' from the closed form in Lemma 6.3(b), by interval subdivision of J.
   Do **not** check c_Y ≥ 0. It fails on cells ending at 2 and is not needed (Lemma 16). c_x ≥ 0 holds by construction (c_x is a nonnegative multiple of k). (Tan) is never checked: it holds exactly at the true (T_n(H), H) by Lemma 18, and Lemma 17' needs only that point to lie in the rectangle, which step 1 guarantees.
3. (U) Fix one rational T̂ for the cell and set U(H) := 2(f_n(T̂; H) − n)/(n − 2) for triples, U_L(H) := (f_10(T̂; H) − 10)/2 for L. Use the same T̂ at both endpoints. Then U ≥ rhs (Lemma 6.3(c)) and U is affine in H.
4. (Dom) Use c := c(H_a) rounded up, the caps of §11 (valid for every H in [H_lo, 2)), and N_0 := {|z|_∞ ≤ ρ_0} with ρ_0 = κ0(H_b)/4 = k(H_b)/(4(m − 1)) for triples and ρ_0 = k(H_b)/16 for L, rounded down. N_0 may be omitted, i.e. the origin certified by (C), on any cell. For H_b = 2, ρ_0 = 0 and nothing is excluded.
5. (C) Check B_P(z; H_e) > U(H_e) at H_e = H_a and H_e = H_b, on a cover of (caps ∩ D_P(H_a)) minus N_cell minus N_0. "Minus N_cell" means: at least one coordinate lies outside its factor of N_cell, so the region is a union, one piece per coordinate. Likewise for N_0. B_P(z; H) − U(H) is affine in H for fixed z, so endpoint positivity on this common domain gives positivity on the whole cell.
6. Use the separable structure. For a triple block, minimise over x_l and x_r separately for each Y-box. For L, minimise over x_1, x_3 and x_5 separately for each (Y_2, Y_4)-box.
Steps 1–5 together with Lemmas 16–21' make tail, local ridge, local origin and certified complement exhaust D_P.

## 11. What the computation must certify

Notation: k = 2 − H, c = c(H) = √(4/H² − 1), s(x, Y; c, c̃) = A(x, −Y) − 1 − (1 − c)x⁺ + (1 − c̃)x⁻ (A by the candidate set of Lemma 3; invalid-sign kink candidates must not be used), d0 = 3 − 2√2, D and f_n as in §0. Every inequality below is strict, certified on H-cells covering the stated range with the mechanics of §10. The local and origin lemmas are proved (Lemmas 16–21'); the program checks only (H0), (T), (Loc) and (C).

**Common to all n.**
- (H0) f_n(T̂; H_lo) < n for a rational T̂, with H_lo = 1.861098 (n = 6), 1.852049 (n = 8), 1.846936 (n = 10). The rounded 1.861097 and 1.852048 would make this false. Also check ∂_T f_n(T_0; H_lo) < 0 at T_0 = 0.887, 0.919, 0.936 respectively (referee's values: −1.47e-3, −3.8e-4, −1.94e-3). Since T_n is increasing, this gives T_n(H) ≥ T_0 on [H_lo, 2], the bound used in Lemma 19(d).
- (T), (Loc) per cell as in §10, steps 1–2.
- H = 2 needs nothing (Theorem 10); cells may end at H_b = 2.
- Excluded neighbourhoods: N_cell (§10, step 2) and N_0 (§10, step 4).

**n = 6 (m = 3), H ∈ [1.861098, 2].** Scheme: even-star blocks j = 1, 2 (pairs {1, 2}, {3, 4}), mirror images; certify j = 1 only.
- B_1(x_1, Y_2, x_3) = s(x_1, Y_2; k, ·) + s(x_3, Y_2; k/2, k/2) − (2 − k)Y_2, with x_1 ≥ 0.
- Domain: x_1 ∈ [0, 3.091], Y_2 ∈ [−c, 3.091], x_3 ∈ [−c, 6.181], c ≤ c(1.861098) < 0.3935. The caps come from Lemma 20(c) with c(H_lo): Θ/k ≤ 3.09025.
- RHS: rhs_6 = (F_6 − 6)/2; κ0 = k/2.
- (C) for j = 1. Grid margin outside N_{1/4} ∪ N_0 (§12): ≥ 6.0e-3 for H ≥ 1.87, and ≈ κ0·dist near the origin as H → H_lo.

**n = 8 (m = 4), H ∈ [1.852049, 2].** Scheme: even-star blocks j = 1, 2, 3; j = 3 mirrors j = 1; certify j = 1, 2.
- B_1 = s(x_1, Y_2; k, ·) + s(x_3, Y_2; k/3, 2k/3) − (2 − k)Y_2, x_1 ≥ 0.
- B_2(x_3, Y_4, x_5) = s(x_3, Y_4; 2k/3, k/3) + s(x_5, Y_4; 2k/3, k/3) − (2 − k)Y_4.
- Domains: c ≤ 0.4077 (c(1.852049) = 0.407617…); Θ/k ≤ 3.01270.
  - B_1: x_1, Y_2 ≤ 3.013, x_3 ≤ 9.039.
  - B_2: Y_4 ≤ 3.013, x_3, x_5 ≤ 4.520.
- RHS: rhs_8 = (F_8 − 8)/3, κ0 = k/3.
- (C) for j = 1, 2. REPORT's scheme (middle pairs single) is not sufficient near H_lo once the slivers are included (§13).

**n = 10 (m = 5), H ∈ [1.86, 2]: even-star scheme.** Blocks j = 1..4; j = 4 and 3 mirror j = 1 and 2; certify j = 1, 2.
- B_1 = s(x_1, Y_2; k, ·) + s(x_3, Y_2; k/4, 3k/4) − (2 − k)Y_2, x_1 ≥ 0.
- B_2(x_3, Y_4, x_5) = s(x_3, Y_4; 3k/4, k/4) + s(x_5, Y_4; k/2, k/2) − (2 − k)Y_4.
- Domains: c ≤ 0.3953 (c(1.86) = 0.395225…); Θ/k ≤ 2.94165.
  - B_1: x_1, Y_2 ≤ 2.942, x_3 ≤ 11.767.
  - B_2: x_3 ≤ 3.923, Y_4 ≤ 2.942, x_5 ≤ 5.884.
- RHS: rhs_10 = (F_10 − 10)/4 ≤ −0.029 on this range, so N_0 is not needed.
- (C) for j = 1, 2. This covers [1.8736, 2]. It is implied by REPORT's end-triple plus single-pair obligations wherever those hold.
- The even-star end block j = 1 fails for H < 1.84911 (grid). At H*(10) the minimum of B_1 − rhs is −2.6e-3, at x_1 = 0, Y_2 ≈ 0.667, x_3 ≈ 1.498: a "half-Morandi" configuration. On [1.86, 2) the grid margin outside N_{1/4} is ≥ 6.0e-3.

**n = 10, H ∈ [1.846936, 1.86]: two 5-variable blocks.** Blocks L = pairs {1, 2, 3, 4} = {(1,2), (3,2), (3,4), (5,4)} with variables (x_1, Y_2, x_3, Y_4, x_5), and its mirror R = pairs {5, 6, 7, 8} with (x_9, Y_8, x_7, Y_6, x_5). They share x_5 (μ_5 = 0, a_5 = ã_5 = k/2); x_3, Y_2, Y_4 are internal to L. Certify L only.
- B_L = s(x_1, Y_2; k, ·) + [A(x_3, −Y_2) + A(x_3, −Y_4) − 2 − (2 − k)x_3] + s(x_5, Y_4; k/2, k/2) − (2 − k)(Y_2 + Y_4).
- On the orthant, B_L = k(x_1 + Y_2 + x_3 + Y_4) + (k/2)x_5 − d(x_1, Y_2) − d(x_3, Y_2) − d(x_3, Y_4) − d(x_5, Y_4).
- Domain: x_1 ≥ 0, the other four ≥ −c, c ≤ 0.4155.
- Tail (Lemma 20(a) for the four pairs, with positive parts): B_L > rhs_L whenever k(x_1⁺ + Y_2⁺ + x_3⁺ + Y_4⁺) + (k/2)x_5⁺ > Θ_L := rhs_L + 4d0 + (7/2)k·c. Since rhs_L + 4d0 = (F_10 − F_10(2))/2 ≤ 9k/2, Θ_L/k ≤ 4.5 + 3.5c < 5.9542. Caps: x_1, Y_2, x_3, Y_4 ≤ 5.955, x_5 ≤ 11.909.
- RHS: rhs_L = (F_10 − 10)/2 = B_L(T, 1/T, T, 1/T, T).
- Local: N_cell^5 (Lemma 17 with the four pairs of Lemma 18; their c_x are k, k/4, 3k/4, k/2, checked in (Loc)).
- Origin: Lemma 21' (proved; no computation): N_0^L = {|z|_∞ ≤ k/16}.
- (C) for L, organised as outer (Y_2, Y_4)-boxes and three inner one-variable minimisations (x_1 given Y_2, x_3 given (Y_2, Y_4), x_5 given Y_4). Grid check (§12): passes at H*(10) + 1e-6, 1.848, 1.85, 1.86, 1.8736 and 1.9, with margin ≥ 3.9e-3 outside N (by Y).
- This block is the union of even-star blocks 1 and 2, so it is implied by them wherever they hold. It is needed only on [1.846936, 1.86].

## 12. Numerical sanity checks (not proofs)

Scripts in `scratchpad/o2n-draft/` (float64, squarepack venv): `common.py` (objects, closed forms), `gates.py` → `gates.log`, `blocks.py` → `blocks.log`, `five.py` → `five.log`, `tabulate_params.py` → `tabulate_params.log`, `origin5.py` → `origin5.log`, `explore_origin.py` → `explore_origin.log`, `probe_j1.py`.

- F_n(2) identity, n = 6, 8, …, 20: Ψ_n(1, −1, …; 2), the chain at tilts (0, π/4, …, π/4, 0) (Minkowski hull, brute force) and f_n(T_n(2); 2) all equal n − (n − 2)d0, max error 1.8e-14. min over 9000 random r ∈ [−4, 4]^{n−1} of Ψ_n(r; 2) − F_n(2): +0.295.
- Tangent bound, 10 H ∈ [H*(n), 2] per n, n = 6..20: gap F_n(2) + (n − 1)(2 − H) − F_n(H) ∈ [0, 8.2e-3] (0 at H = 2); the chain at (0, π/4, …, 0), f_n(1; H) and Ψ_n(1, −1, …; H) equal the bound to 2.1e-14.
- Telescoping (Lemma 13) at 8000 random r (n = 6..12, ρ_1, ρ_{n−1} ≥ 0, other coordinates of either sign) with random admissible a and ã: max error 2.0e-14; even-star blocks: 1.7e-14; orthant form with the stationary split: 2.1e-14.
- Deficit structure: |d − max(0, dX, dY)| ≤ 2.7e-15 on a 1200² grid of (0, 5]²; ridge dichotomy sign(dX − dY) = sign((Y − x)(1 − xY)): 0 mismatches in 1 438 800 points; on xY = 1, |dX − D|, |dY − D| ≤ 5.3e-15; candidate-set A vs t-grid + ternary refinement at 1000 random points: 2.7e-15; max D'' on [1/2, 3/2] = −0.0206.
- Stationarity: closed form (Lemma 18) vs least squares (rank n − 3 in every case) for n = 6..20 at 4 H: 1.9e-16; vs REPORT's task2.json at its T: 2.2e-16; tangential residual at T_n(H): 1e-16. n = 8, H = 1.9 gives μ = (+0.02896, −0.01667, 0, +0.01667, −0.02896).
- Local lemma on 400 random admissible (T, c, N) (T ∈ [0.55, 1], boxes up to 0.45): 0 failures, min g − g(pt) over 26 000 samples per box (incl. points on and next to the ridge) −6.7e-16. Control: with c_Y > ψ(T) the point is not a local minimum in 200/200 cases. Hypotheses of Lemma 19(d) with ρ = 1/4 on a 60-point H-grid per n: min slacks N1 0.049, N1' 0.073, N2 0.101.
- 2000 random orthant r per n (half log-normal around r*, half uniform in [0, 5]): (Ψ_n − Ψ_n(r*)) − (S(r) − S(r*)) ≤ 2.9e-14 with S the even-star sum, and min(Ψ_n − Ψ_n(r*)) = +0.091, +0.286, +0.408 for n = 6, 8, 10.
- Origin: A(x, −Y) − [1 + (x + Y)⁺ − x² − Y²] ≥ +2.6e-8 on 2e6 samples of [−1/2, 1/2]²; min B1/|z|_∞ = k/(m − 1) to 5 digits for n = 6, 8, 10 at H*(n) + 1e-6; min B_j on |z|_∞ ≤ κ0/4: ≥ +2e-9. 5-variable block: see G9b below (Lemma 21', κ0^L = k/2 exactly).
- Even-star blocks, grid check on the clipped, tail-cut domain (x and Y steps 0.002 up to 3, 0.02 beyond, ridge points x = 1/Y added): min(B_j − rhs_n) ∈ [0, 2.2e-7] (attained at z*), and outside N_{1/4}: n = 6: ≥ 6.0e-3 for H ≥ 1.87; n = 8: ≥ 6.0e-3 for H ≥ 1.86; n = 10: ≥ 6.0e-3 for H ≥ 1.86 (1.07e-3 at H = 1.85, where the end block nears its failure); at H = H*(n) + 1e-6 the outside-N minimum is the origin, 2.3e-6 ≈ −rhs. Grid-valid thresholds for the even-star end block: n = 10: H ≥ 1.84911; n = 12: H ≥ 1.85268 (n = 6, 8: all of [H*(n), 2]).
- 5-variable block (n = 10), grid 0.005 with ridge candidates for x_3: min(B_L − rhs_L) ∈ [1e-8, 2.6e-6] at z*, margin ≥ 3.9e-3 for (Y_2, Y_4) not both within 0.1 of 1/T, at H ∈ {H*(10) + 1e-6, 1.848, 1.85, 1.86, 1.8736, 1.9}.
- Revision gates (`rect_check.py` → `rect_check.log`, `gates_rev.py` → `gates_rev.log`):
  - G11: hypotheses (J), (N1), (N1'), (N2'), (N3), (L) of the revised Lemma 16 over parameter rectangles [T_n(H_a) − 5e-4, T_n(H_b) + 5e-4] × [H_a, H_b] (21 × 21 samples, J on 401 points). Cells have width 0.005 from H_lo to 2, the last one ending at 2, with N_cell as in §10. Results:
    - n = 6: 28 cells, min slacks N1 0.060, N1' 0.109, N2' 0.112, N3 0.399, L 0.048, containment 0.240.
    - n = 8: 30 cells, min slacks 0.053, 0.086, 0.105, 0.399, 0.048.
    - n = 10: 31 cells, min slacks 0.049, 0.073, 0.101, 0.399, 0.048.
    - The sampled c_Y goes down to −9.9e-4, −5.4e-4, −4.3e-4 (negative only near H = 2), confirming that γ ≥ 0 cannot be required on rectangles while the new hypotheses hold with large slack.
  - G6b: the revised Lemma 16 on 400 random admissible boxes with c_Y ∈ [−0.02, 0.25] (15 boxes with c_Y < 0): 0 failures, min g − g(pt) +7.5e-16.
  - G9b (Lemma 21'): |B1_L − (referee's form)| ≤ 2.7e-15. With x_1 ≥ 0, the sampled min of B1_L/|z|_∞ is ≥ k/2, and the value is exactly k/2 at (0, 1, −1, 1, −1); without x_1 ≥ 0, the value at (−1, 1, −1, 1, −1) is −k/2 (k = 0.14, 0.15, 0.153064). Min of B_L on |z|_∞ ≤ k/16: ≥ +3e-10.
  - Tail caps recomputed from Lemma 20(c) at c(H_lo): Θ/k ≤ 3.090244 (n = 6), 3.012695 (n = 8), 2.941644 (n = 10 at 1.86), and Θ_L/k ≤ 5.954153 (5-block).

## 13. What did not work, and corrections to REPORT.md

- Pure pair scheme (REPORT, Task 2): fails at the end pairs' origin below H ≈ 1.898–1.911; not usable on the full range. Explained by Lemma 18: the single-pair values at z* are rhs_n/2 ± kT(·)/(m − 1) (end of §8), not all ≤ 0.
- REPORT's end-triple scheme checked only the orthant. With the clipped wrong-sign slivers included (unavoidable after Lemma 9) its single middle pairs dip below 0 near the origin by ≈ (c_x − c_Y)²/2 ≈ 3e-4 (n = 8, pairs 3, 4 at H*(8) + 1e-4: −2.96e-4 against a value at z* of −1.16e-4), so it fails in a window of width ≈ 3e-4 above H*(8), and similarly just above its n = 10 threshold 1.87353. The even-star scheme with the reversed wrong-sign split (Lemma 21) removes this. Grid accuracy: REPORT's own caveat (+7e-4 bias at step 0.01) is the same order as these effects; the numbers here use step 0.002–0.0025.
- Even-star for n ≥ 10 fails near H*(n) at the half-Morandi configuration (§11); hence the 5-variable alternative for n = 10 on [1.846936, 1.86]. Its validity there is numerical only and is obligation (C).
- "Convexity of D along the ridge" (REPORT, Method notes) is really concavity of D (D'' < 0 on [1/2, 3/2]); what is convex is the ridge function ℓ = c_x u + c_Y/u − D(u).
- REPORT's admissible normal-slope interval ≈ [−0.54, 0.42] could not be reproduced in any normalisation tried; the interval I(T) of the Remark after Lemma 16 replaces it.
- The rounded H*(6) = 1.861097, H*(8) = 1.852048 are below the true roots (§0); the certified ranges start at the rationals 1.861098, 1.852049, 1.846936, and [H*(n), H_lo(n)) is not covered (Theorem 22).
- First version of Lemma 16 required c_Y ≥ 0 and Lemma 17' asked for it over the whole parameter rectangle; that is unverifiable on the last H-cell (found by the SPEC implementer, `README-attempt2.md`). Repaired by the present Lemma 16 (§7).
- Not done: the certified program itself; coverage of [H*(n), H_lo(n)); n ≥ 12 (the even-star end block fails below 1.85268 for n = 12, so larger blocks are needed near H*(12)).

## 14. Referee record

Blind Codex review 2026-11-01 (`scratchpad/o2n-review/REVIEW.md`, 15 findings, verdict "No, not literally as written"; the underlying zero-loss reduction judged sound). Disposition:

1. MAJOR, (C0) false as displayed without x_1 ≥ 0. Agreed. Adopted the referee's exact repair as Lemma 21' (κ0^L = k/2, sharp at (0, 1, −1, 1, −1); B_L ≥ 0 on |z|_∞ ≤ k/16) after checking the identity and the bound (proof in §9; gate G9b). The computational obligation (C0) is removed.
2. MAJOR, the obligations do not reach the exact H*(n). Agreed. Theorem 22 is now stated on [H_lo(n), 2] with the rational H_lo, and says that [H*(n), H_lo) is not covered; §0 and the status line say the same.
3. MINOR, inward-rounded c caps and unproved tail tables. Agreed. c caps now 0.3935, 0.4077, 0.3953, 0.4155 (all ≥ the exact values), and the per-coordinate tails in §11 are now the analytic Lemma 20(c) bounds at c(H_lo), rounded up (3.091/6.181; 3.013/9.039/4.520; 2.942/11.767/3.923/5.884; 5.955/11.909).
4. NOTE, Lemmas 1–5 correct. No change.
5. NOTE, endpoint notation. Agreed: Lemma 6 now says "equality in the upper bound" and states sup_Y dX = D(x) for x > 0 (d(0, Y) = 0).
6. NOTE, Lemma 7 "for every H". Agreed: now "for every H ≤ 2".
7. NOTE, Lemmas 8–11 correct. No change.
8. NOTE, Lemmas 13–14 correct. No change.
9. NOTE, "affine across the ridge" needs "on each side". Agreed; the paragraph after Lemma 16 now says piecewise affine with a slope change on the ridge.
10. NOTE, (i) Lemma 18(b) should say the closed form solves the full system only at compatible T; (ii) μ_m = 0 also for odd m; (iii) T_n is the global minimiser over T > 0 without appeal to O2. All agreed and added (Lemma 18(b),(c); Lemma 6.3(d)).
11. MINOR, "[0, 0.127]" false for c_x; ψ values rounded; T_n(H*) bounds not proved by a table. Agreed: the remark now separates c_Y ∈ [0, 0.127] and c_x ∈ [0, 0.154]; ψ values marked ≈; the bounds T_n ≥ 0.887, 0.919, 0.936 are now the scalar checks in (H0), and Lemma 19(d) is stated on [H_lo(n), 2] conditional on them.
12. NOTE, 5-block tail uses k(x_1 + Y_2 + x_3 + Y_4)⁺ instead of positive parts. Agreed; §11 now uses the sum of positive parts, as Lemma 20 gives.
13. NOTE, Lemma 20(c) divides by k, 0/0 at H = 2. Agreed: (c) is now stated for H < 2, and H = 2 is Theorem 10 (as in the assembly).
14. NOTE, implementation requirements (same T̂ at both endpoints, N_cell nonempty and containing the bracket, union coverage, largest c / smallest radius). Agreed; §10 steps 1–6 now say these explicitly.
15. MINOR, existence of H*(n) left implicit. Agreed; added as Lemma 6.3(e) with the referee's argument (F_n(√2) − n ≥ 2(2 − √2)√(m(m − 1)) − 2(m − 1)d0 > 0). The ten printed digits remain numerical and are not proof inputs.

Second blind pass 2026-11-01: 15 findings, 0 MAJOR, 3 MINOR, all applied. (i) The normal-slope remark after Lemma 16 now assumes (L); the referee's counterexample is recorded there. (ii) The N_cell containment in §10 step 2 is now an explicit post-rounding check. (iii) The statement about minimisers at H* in §10 is now conditional. Verdict: conditional yes on [H_lo(n), 2].

Implementer issue (SPEC.md check 2, γ ≥ 0 over the rectangle, `README-attempt2.md`, exact rational witness γ ≈ −1.2e-5 at (T, H) = (0.9999, 2)). Agreed. Lemma 16 now allows c_Y < 0, replacing c_Y ≥ 0 by (N2') (corner minimum), (N3) (c_Y ≥ 1 − min q on [x_−, x_+]) and (L) (ℓ'' > 0 on J, an interval check). Lemma 17' and §10 step 2 list exactly the hypotheses checked over the rectangle; γ ≥ 0 is no longer checked. Gate G11 checks the new hypotheses over sampled rectangles on 0.005-cells, including the last cell, with min slacks N1 0.049, N1' 0.073, N2' 0.101, N3 0.399, L 0.048 (c_Y down to −1e-3 with the ±5e-4 brackets used).
