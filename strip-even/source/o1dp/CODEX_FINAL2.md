Gates 1–4 passed:

- **1:** 100,000 points; max error **6.11e−15**.
- **2:** 50,000 boxes × 64 samples; **zero violations**.
- **3:** At 3,200 cells, unconstrained bounds reached **5.9291587403** (slice) and **5.9537358846** (point); point flagged bound **5.9978646990**, approaching 6.
- **4:** 20,000 chains; **zero violations**.

**75 of 76 slices proved. All 76 saved grids replayed successfully.**

| Coverage | Status | Minimum margin | Max cells |
|---|---|---:|---:|
| [1.87, 1.9999990234375] | 75 proved slices | +0.00953242836 | 3,204 |
| [1.9999990234375, 2] | Unproved | −3.31371530756 | 800 |

Full per-slice results are in [README.md](/Volumes/Kevin_SSD/GitHub/squarepack/o1dp/README.md); bounds and grids are in [certificate.json](/Volumes/Kevin_SSD/GitHub/squarepack/o1dp/certificate.json).

Full-run wall time: **98.14 seconds**, maximum six workers. Total resumed work through verification/reporting: **237.8 seconds**.

The final slice stalls because the prescribed interval enclosure loses correlation at H = 2. The eight-ulp libm accuracy assumption remains unverified. No commits; all writes stayed inside `o1dp`.