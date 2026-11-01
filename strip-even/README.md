# Six, eight or ten unit squares in a strip of height just below 2

Computational provenance for the theorem *L ≥ F_n(H) for every packing of n ∈ {6, 8, 10} unit squares in an L × H rectangle, H ∈ R_n, with R_6 = [1.862, 2), R_8 = [1.855, 2), R_10 = [1.850, 2)* (Kevin Fang, note `docs/strip-even-note.md` v0.3 in https://github.com/TheSnakeFang/squarepack, commit 99dad02, 2026-11-01; archived as https://doi.org/10.5281/zenodo.23865706, version v0.3 under the concept DOI 10.5281/zenodo.23852983; that record also holds the four leaf tar files listed below). The proof, the certified programs, the lemmas and the five blind referee reports live in that repository:

- `docs/strip-n6-reduction.md`: packings → chain functions (n-independent).
- `o1n/`: O1, the non-alternating role patterns for n = 6 (on [1.862, 1.87]), 8 and 10, certified min-plus dynamic program; `certificate-n{6,8,10}.json` committed there. n = 6 on [1.87, 2) is `o1dp/` (v0.2).
- `o2n/`: O2, the alternating (Morandi) pattern, via the block decomposition of the support-function dual; `LEMMAS.md`, `SPEC.md`, the C kernel, the driver, the four manifests `certificate-n{6,8,10,10-five}.json`.

squarepack is private, so `source/` here is the public copy of everything the replay needs. This directory holds that mirror, copies of the manifests and the files that are not in the main repository.

| path | content |
|---|---|
| `o1n/` | the three O1 certificates, `summary.json`, environment records, README (copies of the committed files) |
| `o1n-logs.tar.xz` | gates, run, verify and regression logs of o1n (gitignored in the main repository) |
| `o2n/` | the four O2 manifests after the provenance refresh of 2026-11-01, gate records, `verification.json`, `bundle-audit.json`, `report.json`, `build.json`, README |
| `source/` | tracked source of o1n, o2n, o1dp, o2cert, the note, the reduction and the referee reports, as of squarepack commit c54a94c, plus `pyproject.toml` and `uv.lock` |
| `o2n-cells-n6.tar`, `-n8.tar`, `-n10.tar`, `-n10-five.tar` | the per-cell certificates and inner leaf bundles referenced by hash from the manifests (`o2n/cells/`), needed to replay O2: 75 MB, 150 MB, 158 MB and 3.6 GB; too large for this repository, deposited at https://doi.org/10.5281/zenodo.23865706; `o2n-cells.sha256` lists their SHA-256 |

Replay from this directory alone (Apple clang, arm64, `uv` on the path; the tar files from the Zenodo record sit next to this README):

```
cd source
uv sync --extra tools --extra search
(cd o1n && clang -O2 -std=c11 -D_DARWIN_C_SOURCE -shared -fPIC src/kernel.c -o src/kernel.dylib)
(cd o2n && clang -O2 -ffp-contract=off -shared -fPIC src/block.c -o src/kernel.dylib)
for t in n6 n8 n10 n10-five; do tar -xf ../o2n-cells-$t.tar -C o2n; done
cd o1n && ../.venv/bin/python src/driver.py verify --n 8 && ../.venv/bin/python src/driver.py verify --n 10 && ../.venv/bin/python -c "import sys; sys.path.insert(0, 'src'); import run_n6; run_n6.verify()"
cd ../o2n && ../.venv/bin/python src/driver.py verify --workers 6 && ../.venv/bin/python src/audit_bundle.py
```

Each tar holds paths `cells/...`, so the loop fills `source/o2n/cells/`, where the manifests look them up by hash. `uv sync` installs mpmath, numpy and scipy from `uv.lock`; a plain venv with those three works too. The O2 manifests pin the SHA-256 of `src/kernel.dylib` (`abb136f3…`, see `o2n/build.json`); Apple clang 21.0.0 (clang-2100.1.1.101) on arm64 rebuilds it byte for byte, and any other compiler makes `verify` stop at the hash check. `run_n6.py verify` refuses to run once the two-hour budget in `budget-n6.json` has lapsed, which it has, so the n = 6 replay calls `verify()` directly; it is the same check. On an M-series Mac the o1n replays take about 6 min (n = 8), 9 min (n = 10) and 30 s (n = 6).

Premises and scope are stated in the note §3–4: IEEE-754 binary64 with outward rounding, an 8-ulp libm padding, pinned compiler settings. The slivers [H*(n), lower end of R_n) are not covered.
