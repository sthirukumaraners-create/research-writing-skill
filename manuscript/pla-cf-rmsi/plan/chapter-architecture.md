# Chapter architecture

Target journal: Polymer(Korea), general article, English. Required body headings are Introduction, Experimental, Results, and Discussion. Abstract and References are supporting files. A separate Related Work chapter is not used. The journal limit is about 12 template pages including figures and tables, and the abstract must stay between 100 and 150 words. Chapter minima are therefore shorter than a full-length computer-science article and are set in non-whitespace characters.

## Required chapter files

- chapters/00-Abstract.md | min_chars=550 | agent=controller | placeholders=no
- chapters/01-introduction.md | min_chars=4500 | agent=required | placeholders=no
- chapters/02-experimental.md | min_chars=4200 | agent=required | placeholders=no
- chapters/03-results.md | min_chars=4500 | agent=required | placeholders=no
- chapters/04-discussion.md | min_chars=4500 | agent=required | placeholders=no
- chapters/05-References.md | min_chars=1800 | agent=controller | placeholders=no

## Locked decisions

- Title: A Relative Multimode Strength Index for Screening Fused-Filament Parameters of Short-Carbon-Fiber PLA
- One observation per response per run. No within-run standard error.
- Infill density held constant. The percentage is not in the record and must not be invented.
- Specimen dimensions are not in the record and must not be invented.
- Nozzle 220 °C and bed 55 °C were the temperatures used.
- Manufacturer-reported filament data may be tabulated only as manufacturer-reported.
- RMSI values and level means must be copied from figures/data/rmsi_scores.csv and figures/data/factor_level_means.csv after rounding as specified in plan/numerical-record.md.
- Citations are superscript numbers matching refs/references.md. The Introduction must also contain at least eight parenthetical author-year markers of the form (Omer et al., 2025), because those markers are real citations of the same sources.
- Prose is original. Do not reuse sentences from abstracts or from the uploaded draft.
