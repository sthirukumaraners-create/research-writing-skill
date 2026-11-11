# Table schema

| Table | Purpose | Rows | Metrics | Data source | Replacement owner |
|---|---|---|---|---|---|
| Table 1 | Identify the filament and the fixed temperatures | Properties supplied by the manufacturer or used in printing | MFI, density, temperatures | Supplied material table | Not replaceable; missing fields stay missing |
| Table 2 | Give the L9 layout and the measured strengths | 9 runs | Tensile, compressive, and flexural strength in MPa | Supplied strength table | Not replaceable |
| Table 3 | Show cross-run dispersion | 3 responses | Minimum, maximum, range, mean, sample SD | figures/data/response_dispersion.csv | Calculated |
| Table 4 | Report normalized scores, RMSI, and maximin | 9 runs | nT, nC, nF, RMSI, maximin | figures/data/rmsi_scores.csv | Calculated |
| Table 5 | Report descriptive level means | 3 factors × 3 levels | Mean RMSI and mean strengths | figures/data/factor_level_means.csv | Calculated |

Aggregation rule: sample standard deviation uses the n−1 divisor across the nine runs. Level means are arithmetic means of the three runs at that level. No pooled variance is available.
