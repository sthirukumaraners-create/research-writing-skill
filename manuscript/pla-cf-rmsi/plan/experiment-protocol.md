# Experiment protocol

This record is a completed nine-run screen, not a machine-learning benchmark. The protocol states what was supplied and what the calculations may claim.

## Material and process

- Filament: Bambu Lab PLA-CF, PLA with chopped carbon fiber, black.
- Manufacturer-reported melt flow index: 3.7 ± 0.6 g/10 min.
- Manufacturer-reported density: 1.22 g/cm3. This is not a measured part density.
- Temperatures used: nozzle 220 °C, bed 55 °C.
- Printer: Bambu Lab. Model number not supplied.
- Infill density: held constant. Percentage not supplied.
- Factors: layer thickness 0.1, 0.2, 0.3 mm; printing speed 30, 45, 60 mm/s; raster angle 0°, 45°, 90°.
- Design: Taguchi L9, one run at each listed combination in the numerical record.

## Responses

- Tensile strength, ASTM D638, one value per run.
- Compressive strength, ASTM D695, one value per run.
- Flexural strength, ASTM D790, one value per run.
- Specimen geometry, test speed, and support span were not supplied.

## Metrics

- Min-max normalization within each response across the nine runs.
- RMSI: equal-weight arithmetic mean of the three normalized scores, times 100.
- Maximin: minimum of the three normalized scores.
- Descriptive level means and the sample standard deviation across the nine runs.

## Comparisons

- Main comparison: RMSI rank versus maximin rank on the same nine runs.
- Factor comparison: L9 level means of RMSI and of the three strengths.
- No external baseline print, no neat-PLA control, no second printer, and no confirmation run.

## Ablation and generalization

- There is no module ablation. The only sensitivity built into the analysis is the second decision rule, maximin versus the equal-weight mean.
- The index is not generalized beyond the nine runs. A different data set would change the minima and maxima.

## Efficiency and explainability

- Not applicable. No compute-time claim and no model explanation are part of the study.

## Allowed claims

- Which run leads the equal-weight score.
- Which run leads the worst-case normalized score.
- Which factor shows the largest spread in mean RMSI inside this array.
- Where a raw strength does not follow that RMSI pattern, especially compression.

## Disallowed claims

- Statistical significance, percentage contribution, or an optimized service setting.
- Any strength, dimension, or infill value that is not in the numerical record.
