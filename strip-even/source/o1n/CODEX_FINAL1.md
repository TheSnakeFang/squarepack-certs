Stopped as instructed: the fixed math contains a false assertion. Central symmetry of Δ does **not** make κ even in `dy`.

The prescribed hull reference gives, for `t=t′=0.2`, `H=1.9`, and `d=H−2h(t)`:

- κ(+d) = **0.8741313753697272**
- κ(−d) = **1.166546314512658**

This invalidates the stated argument for target monotonicity. **F_n may still be nonincreasing**, but that needs a different proof; I did not change the math.

Gates and n=6 regression: **not run**. For both n=8 and n=10: **0 slices proved, 0 tested; proved range empty**. Lowest proved H, minimum margin, maximum cells, and solver wall time: N/A.

Saved the explanation in [README.md](README.md) and a reproducible check in [math-check.py](math-check.py). Nothing outside `o1n` was modified; no git commands were used.

Next action: correct or supply a replacement proof for the target-monotonicity premise.