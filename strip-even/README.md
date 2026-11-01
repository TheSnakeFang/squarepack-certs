# Six, eight or ten unit squares in a strip of height just below 2

Computational provenance for the theorem *L ≥ F_n(H) for every packing of n ∈ {6, 8, 10} unit squares in an L × H rectangle, H ∈ R_n, with R_6 = [1.862, 2), R_8 = [1.855, 2), R_10 = [1.850, 2)* (Kevin Fang, note `docs/strip-even-note.md` v0.3 in https://github.com/TheSnakeFang/squarepack, commit 99dad02, 2026-11-01; archived as https://doi.org/10.5281/zenodo.23865706, version v0.3 under the concept DOI 10.5281/zenodo.23852983; that record also holds the four leaf tar files listed below). The proof, the certified programs, the lemmas and the five blind referee reports live in that repository:

- `docs/strip-n6-reduction.md`: packings → chain functions (n-independent).
- `o1n/`: O1, the non-alternating role patterns for n = 6 (on [1.862, 1.87]), 8 and 10, certified min-plus dynamic program; `certificate-n{6,8,10}.json` committed there. n = 6 on [1.87, 2) is `o1dp/` (v0.2).
- `o2n/`: O2, the alternating (Morandi) pattern, via the block decomposition of the support-function dual; `LEMMAS.md`, `SPEC.md`, the C kernel, the driver, the four manifests `certificate-n{6,8,10,10-five}.json`.

This directory holds copies of the manifests and the files that are not in the main repository.

| path | content |
|---|---|
| `o1n/` | the three O1 certificates, `summary.json`, environment records, README (copies of the committed files) |
| `o1n-logs.tar.xz` | gates, run, verify and regression logs of o1n (gitignored in the main repository) |
| `o2n/` | the four O2 manifests after the provenance refresh of 2026-11-01, gate records, `verification.json`, `bundle-audit.json`, `report.json`, `build.json`, README |
| `o2n-cells-n6.tar`, `-n8.tar`, `-n10.tar`, `-n10-five.tar` | the per-cell certificates and inner leaf bundles referenced by hash from the manifests (`o2n/cells/`), needed to replay O2: 75 MB, 150 MB, 158 MB and 3.6 GB; too large for this repository, deposited at https://doi.org/10.5281/zenodo.23865706; `o2n-cells.sha256` lists their SHA-256 |

Replay (from a checkout of squarepack at 99dad02 or later, with the tar files unpacked into `o2n/`):

```
cd o1n && ../.venv/bin/python src/driver.py verify --n 8 && ../.venv/bin/python src/driver.py verify --n 10 && ../.venv/bin/python src/run_n6.py verify
cd o2n && ../.venv/bin/python src/driver.py verify --workers 6 && ../.venv/bin/python src/audit_bundle.py
```

Premises and scope are stated in the note §3–4: IEEE-754 binary64 with outward rounding, an 8-ulp libm padding, pinned compiler settings. The slivers [H*(n), lower end of R_n) are not covered.
