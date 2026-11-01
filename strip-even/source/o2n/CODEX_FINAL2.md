Stopped on a new specification conflict, documented in [README.md](README.md).

The required `γ = T²(cₓ − D′(T)) ≥ 0` over independent T/H rectangles is impossible for any final cell ending at H=2: strict bracketing forces T_lo<1, making γ negative at `(T_lo,2)` and nearby H<2.

Exact rational checks confirmed:
- 4 derivative-bracket signs passed.
- 8 negative-γ witnesses verified; at H=2, γ < **−1.213142766585369×10⁻⁵**.
- G1–G6: **not run, 0 trials**.

| Range | Cells | Outer/inner boxes | Min margin | Certified H range | Run time |
|---|---:|---:|---|---|---:|
| n=8 | 0 | 0/0 | N/A | empty | 0 s |
| n=6 | 0 | 0/0 | N/A | empty | 0 s |
| n=10 even-star | 0 | 0/0 | N/A | empty | 0 s |
| n=10 five-block | 0 | 0/0 | N/A | empty | 0 s |

Deviation: the mandated stop prevented kernel implementation, gates, runs, replay, and corrected-domain κ₀ᴸ computation. SPEC.md and LEMMAS.md remain unchanged. Whether the remaining obligations close is untested.

Next action: resolve the rectangular γ requirement identified in the README.