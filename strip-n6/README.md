# Six unit squares in a strip of height 1.87 ≤ H < 2

Raw computational provenance for the theorem *L ≥ F6(H) for every packing of six unit squares in an L × H rectangle, 1.87 ≤ H < 2* (Kevin Fang, draft note `docs/strip-n6-note.md` in https://github.com/TheSnakeFang/squarepack, commit 5887dec, 2026-10-31; archived as https://doi.org/10.5281/zenodo.23852984). The proof itself, the certified programs, the lemmas and the three blind referee reports live in that repository:

- `docs/strip-n6-reduction.md`: packings → chain functions (centre-x ordering, pair constraint, vertex reduction, mirror lemma).
- `o1dp/`: O1, the 62 non-alternating role patterns, certified min-plus dynamic program; its `certificate.json` (1.2 MB) is committed there.
- `o2cert/`: O2, the alternating (Morandi) pattern, via the support-function dual Ψ; `LEMMAS.md`, `SPEC.md`, the C kernel, the driver, the corner replay, and `certificate.json.gz`.

This directory holds the O2 files that are too large for, or were left out of, the main repository. They are the output of the search and verification runs, not inputs to the proof; the committed `o2cert/certificate.json.gz` together with `o2cert/src/driver.py verify` is sufficient to replay O2.

| file | content | raw sha256 |
|---|---|---|
| `o2cert/certificate.json.xz` | the final O2 certificate (8 H-cells, 186,155 outer rectangles), identical to the `.gz` in squarepack | `d46bddef…08cbec` (`certificate.sha256`, `raw.sha256`) |
| `o2cert/cells.tar.xz` | per-H-cell certificates `cells/H0.json … H7.json` as written by the search, with the refreshed `source_hashes` | — |
| `o2cert/initial-pass.tar.xz` | the first search pass (`certificate.json`, `gates.json`, `migration.json`, `cells/`, `src/`, `staging/`) before the parallel re-verification | — |
| `o2cert/certificate.before-parallel-verify.json.xz` | the certificate as written by the search, before `verify_parallel.py` and before the provenance refresh of 2026-10-31 | `810371fc…ad97d16` (`raw.sha256`) |

Replay (from a checkout of squarepack at 5887dec or later):

```
cd o2cert && gunzip -k certificate.json.gz && ../.venv/bin/python src/driver.py verify
```

Premises and scope are stated in the note and in `o2cert/LEMMAS.md` §6–8: IEEE-754 binary64 with outward rounding, an 8-ulp libm padding for cos, sin and sqrt, and the swarm's corner certificate identities (replayed with directed rounding in `o2cert/src/corner_impl`). The interval [H*(6), 1.87) with H*(6) = 1.8611… (where F6 = 6) is not covered.
