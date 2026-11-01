Completed within 30 minutes. No commits or mathematics changes.

- `src/driver.py`: added explicit invariant and hash checks with loud failures; added `O1DP_M4CHECK` override while retaining the default path and restricted AST extraction.
- `src/report.py`: preserves the handwritten README suffix verbatim.
- `certificate.json`: refreshed SPEC and driver hashes, added the previously absent README hash, and recorded old/new values under `provenance_refresh_2026_10_30`.
- `verification.log`: appended the successful verification record.

Verify output:

```text
saved grids and proved flags PASS
positive widths, exact shared boundaries and domain coverage PASS
grid endpoints, strict increase and cell counts PASS
exact downward-rounded positive margins PASS
current source hashes PASS
both preserved backup certificate hashes PASS
recomputed D and F6_ub exactly match stored values PASS
certificate replay PASS: 76 slices; 76 proved
```

Report generation passed. README remained byte-identical, including both handwritten sections and the per-slice table. All grids, bounds, margins, historical provenance, and backup certificates remained unchanged. Sixteen malformed-certificate checks passed under `python -O`.

No unresolved repair issues.

