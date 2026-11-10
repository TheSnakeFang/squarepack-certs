# Lower bounds for unit-square packings in slabs and trapezoids

Source, working notes, simulators and review reports for the note *Lower bounds for the waste of unit-square
packings in slabs and trapezoids* (Kevin Fang, draft v0.1, 2026-11-09, https://doi.org/10.5281/zenodo.24099178).

**Status: claimed, not verified.** The proofs were found and written by Claude (Anthropic) working as a research
agent under my direction, in one day. They have been reviewed only by language models and tested by floating-point
simulation. No person has checked them line by line and nothing is formalised. Unlike the rest of this repository,
there is no certificate here that a program can check.

## What is claimed

Ω = {0 ≤ x ≤ L, 0 ≤ y ≤ g(x)}, packed with unit squares with disjoint interiors; W is the uncovered area.

- **Theorem 1.1 (thin regions).** g concave, g ≤ M, 0 < δ ≤ 2/5, 0 < τ ≤ 0.08, 0.502·M·τ² ≤ δ′. Then
  L − |A(δ, δ′)| ≤ W/δ + 1350·W/τ + √(21·τ·M·L·W), where A is the set of x with g(x) within [N − δ′, N + δ] of an
  integer N.
- **Corollaries.** A sloped ceiling g = w + ζx with rise ζL ≥ 1 and M = w + ζL has W ≥ 4·10⁻⁵·L/√M. An
  L × (m + ½) rectangle with m ≥ 125 has W ≥ 5·10⁻⁴·L/√(m + ½). An L × M rectangle with fractional part f has
  W ≥ 5·10⁻⁵·L·min(f, √((1 − f)/M)).
- **Theorem 1.5 (any width).** g = w + ζx with 0 < ζ ≤ 1 and rise R = ζL ≥ 1. Then W ≥ 7·10⁻⁶·√(LR). This is
  Conjecture 1 of H. D. Bui, *Square packing with O(x^0.6) wasted area* (arXiv:2508.04603), with a constant.

Nothing is claimed for the waste of a square or for c*(k) over all packings. Section 8 of the note says what the
bounds imply for the constructions of Bui, McClenagan and Ryu, given the decompositions those papers describe.

## Files

| path | content |
|---|---|
| `note/main.pdf`, `note/*.tex` | the note (build: `tectonic main.tex` in `note/`) |
| `notes/slab-lower-bound.md`, `notes/wedge-lower-bound.md` | the working notes the note was typeset from, with their revision history. The review reports use the numbering of these files |
| `tools/slab_constants.py` | recomputes the counts behind 1350 and 21 and checks the corollaries on grids (instant) |
| `tools/slab_flow_check.py` | the vertical flow of Section 3 on 22 packings (about 30 s) |
| `tools/wedge_flow_check.py` | the straight flow of Sections 5 to 7 on 31 packings (about 8 min) |
| `tools/wedge_staircase_check.py` | the straight flow on staircase packings of up to 199,030 squares, where most paths arrive (about 4 min) |
| `notes/prop75-checks.md` | added 2026-11-10: what was checked about the last step (Proposition 7.5) after the note, with the results |
| `tools/wedge_constants.py` | added 2026-11-10: the 70 numerical claims of Sections 5 to 7 and the proof of Theorem 1.5 in exact rational arithmetic (instant) |
| `tools/wedge_prop75_check.py` | added 2026-11-10: the lines of the proof of Proposition 7.5 with measured values; its two sheared-stack cases bring Lemma 7.4 to 0.997 of its bound (about 5 min) |
| `tools/wedge_prop75_a2.py` | added 2026-11-10: the same lines on a 715,290-square staircase where 78.6% of the paths arrive, window by window (about 100 min, 4.3 GB, resumable) |
| `reports/` | added 2026-11-10: the reports written by those three tools |
| `reviews/` | the six blind language-model reviews, unedited apart from a local scratch path removed from three of them |

Numbering: Theorem S and Theorem B of the working notes are Theorems 1.1 and 1.5 of the note. Slab Lemmas 2.1, 2.2,
Corollary 2.3 keep their numbers; slab Lemma 3.1 is Lemma 3.1; slab Lemmas 4.1 to 4.3 are Lemmas 3.2 to 3.4; wedge
Lemmas 3.1 to 3.3 are Lemmas 5.1 to 5.3; wedge Lemmas 4.1 to 4.4 and Corollary 4.5 are Lemmas 6.1 to 6.4 and
Corollary 6.5; wedge Lemma 5.1 is Lemma 7.1; wedge Lemmas 6.1 to 6.3 are Lemmas 7.2 to 7.4; wedge Proposition 7.1 is
Proposition 7.5.

## Running the simulators

Python 3 standard library only. From this folder:

```
mkdir -p runs/k2c-exponent-2026-11-09
python3 -I tools/slab_constants.py
python3 -I tools/slab_flow_check.py
python3 -I tools/wedge_flow_check.py
python3 -I tools/wedge_staircase_check.py
python3 -I tools/wedge_constants.py
python3 -I tools/wedge_prop75_check.py
python3 -I tools/wedge_prop75_a2.py --selftest
python3 -I tools/wedge_prop75_a2.py --run --alpha 0.03 --L 320 --width 1
```

All but the first write their reports under `runs/` (not tracked; the reports of `wedge_flow_check.py` and
`wedge_staircase_check.py` are 4 to 5 MB each, and the long run leaves a 407 MB checkpoint). Apart from
`wedge_constants.py`, which is exact arithmetic on constants, they are floating point. None is a certificate.

No test packing satisfies the hypothesis of Proposition 7.5, which needs a waste below about L/84500 (the note says
L/34000, which is what remains once τ is chosen as in the proof of Theorem 1.5). When the note was written no
simulator ran that step at all. Since 2026-11-10 it is tested this far: the hypothesis is used only to get that 3/4 of
the floor paths arrive, and on a staircase where 78.6% arrive every later line of the proof holds with measured
values. The lines that carry the waste hold there with a factor of about a million to spare, so they are not tested
sharply, and the step from small waste to 3/4 arrival is still only the written argument. `notes/prop75-checks.md`
has the numbers and the limits.

## Reviews

| file | reviewer | scope | verdict |
|---|---|---|---|
| `slab-lower-bound-review-2026-11-09.md` | Claude Opus 5.5 | slab note v0.1 | sound with fixes; one claim about other authors' walls withdrawn |
| `wedge-lower-bound-review-2026-11-09.md` | Claude Opus 5.5 | wedge note v0.1 | sound with fixes |
| `wedge-lower-bound-review-codex-2026-11-09.md` | OpenAI Codex | wedge note v0.2 | sound with fixes |
| `wedge-lower-bound-judge-A-codex-2026-11-09.md` | OpenAI Codex | wedge note v0.3, Sections 1 to 4 | no fatal error, four gaps |
| `wedge-lower-bound-judge-B-codex-2026-11-09.md` | OpenAI Codex | wedge note v0.3, Sections 5 to 8 | no fatal error, gaps in Section 8 only |
| `slab-lower-bound-judge-codex-2026-11-09.md` | OpenAI Codex | slab note v0.2 | no fatal error, four gaps, two errors in a superseded outline |

Each reviewer worked from the text alone and was told to assume there is an error. Every gap they found is repaired
in the note. None of these is a referee's report, and models reviewing a text written by a model can share its
mistakes. A reading by a person, of Section 7 in particular, is what this needs.

## Credits

The waste lemma between two squares of different tilt is Roth and Vaughan's (J. Combin. Theory Ser. A 24, 1978). Its
proof here, the idea of following paths through the squares along their normals, the height identity and the rule of
keeping direction in gaps are Sungjoon Ryu's (the k² − c preprints, doi:10.5281/zenodo.23194104 and
doi:10.5281/zenodo.23212643). The conjecture is H. D. Bui's. Evan Daniel's notes on the exponent of c*(k)
(https://github.com/evand/square-packing, `tasks/k2c-exponent/README.md`) posed the question. The simulators were
written with OpenAI Codex.
