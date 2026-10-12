# Changelog

## 2026-10-12

Bundle for the note "Packing n² − n + 1 unit squares in a square of side less than n, for every
n ≥ 15" (draft v0.3).

- Eight more direct square packings: n = 380, 381, 421, 463, 507, 553, 601, 651 (`nNNNN/`), in the
  same layout as the 2026-10-09 folders.
- Five squeezable rectangles, 17 × 16 / 257, 18 × 17 / 290, 19 × 18 / 325, 21 × 20 / 401,
  22 × 21 / 442 (`rectangles/`).
- Composites (`composites/`): the largest-j composite for each n with 27 ≤ n ≤ 64 (38 files), the
  table of all 230 composites with hashes, and `reproduce.sh`, which regenerates all 230.
- Evan Daniel's certificates used as B pieces and his n = 308, 343, 344 improvements, pinned to
  commits and hashed (`third_party/daniel/`, `third_party/SOURCES.md`); de Winter's n = 211 is
  fetched by `third_party/fetch_unlicensed.sh`, not copied.
- Tools: `tools/glue.py` (Lemma 3, standalone), `tools/rectcheck.py`, `tools/verify_cert_daniel.py`.
- `VERIFICATION.md` (three checkers on every certificate), `MANIFEST.sha256`, rewritten README and
  ATTRIBUTION. `verify.py` and the folders `n0308/`, `n0343/`, `n0344/` are unchanged.

## 2026-10-09

Certificates for s(308) < 18, s(343) < 19 and s(344) < 19 (`n0308/`, `n0343/`, `n0344/`), with the
standalone exact verifier `verify.py`. Submitted to the Squares Project as jlevy/squares#484.
