# Referee packet: o1n, the certified O1 computation for n = 8 and n = 10 unit squares in a strip (2026-11-01)

Read-only inputs (do not modify anything under /Volumes/Kevin_SSD/GitHub/squarepack):
- /Volumes/Kevin_SSD/GitHub/squarepack/o1n/SPEC.md (the specification; a delta over ../o1dp/SPEC.md, which you must also read in full)
- /Volumes/Kevin_SSD/GitHub/squarepack/o1n/src/ (C kernel + Python driver), README.md, summary.json, gates-n8.log, gates-n10.log, run-n8.log, run-n10.log, certificate-n8.json, certificate-n10.json
- /Volumes/Kevin_SSD/GitHub/squarepack/docs/strip-n6-reduction.md (the reduction that makes O1 meaningful; its argument is n-independent, check that claim)
- /Volumes/Kevin_SSD/GitHub/squarepack/docs/o1dp-review-codex-2026-10-30.md (the referee report on the n = 6 version; the same checks apply)
- Python: /Volumes/Kevin_SSD/GitHub/squarepack/.venv/bin/python (numpy, scipy). The reference κ is in /Volumes/Kevin_SSD/GitHub/squarepack/runs/openmath-2026-10-27/m4check.py; exec only its first 29 lines, dropping lines starting with "from targets", "sys.path", "import numpy", "from scipy".

Claim under review. For n ∈ {8, 10} and every H in [H_0(n), 2) with H_0(8) = 1.855, H_0(10) = 1.850: for every role pattern σ ∈ {F, C}^n other than the two alternating ones and every tilt vector θ ∈ [0, π/2]^n, the chain function Φ^σ(θ, H) exceeds F_n(H) = min over φ of Φ_M((0, φ, …, φ, 0), H), the alternating-pattern chain at equal middle tilts (the Morandi width). The certificate is a min-plus DP over tilt cells and H-slices with three interval lower bounds per gap, and a per-slice upper bound F_n_ub obtained by evaluating Φ_M at a fixed φ0 with H as an interval.

Act as a strict referee. Do not trust the README; re-derive and re-run. Specifically:
1. The target bound: is F_n_ub(slice) a valid upper bound of F_n(H) for EVERY H in the slice, with the interval-in-H evaluation and the "min over terms of per-term upper bounds" argument? Check the rounding direction of every operation in that code path, including the sign handling of dy as an interval and the division by n_x.
2. The n-parameterization: positions, the flag logic for "alternating" with n squares, the backward pass, the binding test, the final value D = min over (r, c) of V_n + h_lb. Any off-by-one between n − 1 gaps and n squares.
3. The gap bounds (plain, correlated ratio, near-upright lemma) are unchanged from o1dp in mathematics; verify the code is byte-equivalent or equivalent where it matters, and that the lemma's hypotheses (H ≤ 2, H > √2) hold on the lowered H range.
4. Replay both certificates yourself with the verify mode and confirm the per-slice D, F_n_ub and margins; confirm the slices cover [H_0(n), 2] with no gaps and with the stored lower endpoint ≤ H_0(n).
5. Gate 2 and gate 4 soundness: rerun with your own random seeds (≥ 10,000 boxes / 5,000 chains), including both cells near 0 and near π/2 and H near 2 and near H_0(n).
6. Independent spot check: at 20 random slices per n, compute the best non-alternating pattern value by your own optimisation (random starts + local search over θ ∈ [0, π/2]^n) and check it is ≥ D of the slice; and compute F_n(H) at both slice ends by your own minimisation over φ and check F_n_ub ≥ both.
7. Anything else: the lowest slices have margins of 1e−4 order; check those are real (not rounding artefacts) and whether the computation would be sound if a libm cos/sin were off by more than 8 ulps.

Report format: numbered findings labelled MAJOR / MINOR / NOTE, quoting code or log lines, what is wrong, what would fix it. State what you computed with numbers. Finish with a one-paragraph verdict: does o1n certify the claim for n = 8 on [1.855, 2) and n = 10 on [1.850, 2) under its stated premises, yes or no. Write the report to /private/tmp/claude-501/-Volumes-Kevin-SSD-GitHub/42c1ea86-ad33-4af4-8f4e-329f5037d3b2/scratchpad/o1n-review/REVIEW.md. Scratch files only under that directory. No git commands. Time-box every command to 15 minutes.
