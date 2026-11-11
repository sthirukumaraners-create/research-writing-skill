# Experimental blueprint

Target file: chapters/02-experimental.md
Minimum: 4200 non-whitespace characters and 6 prose paragraphs.
Follow input, process, output, and reason. No bullet list.

### Paragraph 1
- Role: material input
- Main claim: The filament is Bambu Lab PLA-CF, a PLA containing chopped carbon fiber, printed at 220 °C on a 55 °C bed. Manufacturer-reported melt flow index and density are identified as manufacturer data.
- Evidence IDs: experimental record
- Forbidden content: do not invent fiber weight percent, nozzle diameter, or infill percentage.

### Paragraph 2
- Role: design
- Main claim: Nine runs follow an L9 array on layer thickness, printing speed, and raster angle, with infill density held constant.
- Evidence IDs: numerical record
- Forbidden content: do not claim the raster angle was verified against the specimen long axis.

### Paragraph 3
- Role: measurements
- Main claim: Each run has one ASTM D638 tensile strength, one ASTM D695 compressive strength, and one ASTM D790 flexural strength. Specimen dimensions were not recorded with the strengths.
- Evidence IDs: experimental record
- Forbidden content: do not invent grip speed, span, or specimen type.

### Paragraph 4
- Role: index construction
- Main claim: Each strength is min-max normalized across the nine runs, the three normalized values are averaged with equal weight, and the average is multiplied by 100.
- Evidence IDs: numerical record equations
- Forbidden content: do not say the weights were fitted to a service spectrum.

### Paragraph 5
- Role: second decision rule
- Main claim: The maximin score is the lowest of the three normalized strengths. It asks which run avoids the weakest relative mode.
- Evidence IDs: numerical record
- Forbidden content: do not treat maximin as a statistical lower confidence bound.

### Paragraph 6
- Role: summary quantities
- Main claim: Means and sample standard deviations describe the nine-run columns. Factor level means are L9 averages. No ANOVA is performed because there is no replicate error.
- Evidence IDs: S13 for the screening-design limit; numerical record
- Forbidden content: no p-values.

### Paragraph 7
- Role: boundary
- Main claim: The index can rank only these nine runs, because a new test would change the minima and maxima.
- Evidence IDs: S17 as a brief methodological caution, optional
- Forbidden content: do not promise a confirmation print that was not done.
