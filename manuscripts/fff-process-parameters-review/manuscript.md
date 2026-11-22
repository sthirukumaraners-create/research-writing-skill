# Influence of Process Parameters in Fused Filament Fabrication: A Review of Open-Access Studies, 2022–2026

Selva

22 November 2026

## Abstract

Fused filament fabrication (FFF), also called fused deposition modeling (FDM) in much of the process literature, builds a thermoplastic part by pushing a solid filament through a heated nozzle and depositing roads in layers. Nozzle and bed temperature, layer height, infill, raster or build orientation, print speed, and extrusion flow do not act as independent dials. They set the thermal history of each road, the contact area between roads, the amount of material in the cross-section, and the time available for diffusion across the interface. This review covers 175 open-access journal articles with publication years 2022 through 2026 whose primary host organization in OpenAlex is Elsevier, Springer Nature, Wiley, or Taylor & Francis. Records were kept when the title or abstract identified FFF or FDM and at least one process parameter or a parameter-linked response, and only after Crossref returned a matching title and a year inside that window. Across the corpus, strength, interlayer bonding, roughness, dimensional error, warpage, and energy use are the responses authors most often attach to those settings. The studies do not support one ranking of parameters that travels from PLA to PEEK, or from a desktop printer to a heated-chamber machine. Designed experiments and regression remain the dominant analysis tools, with machine-learning surrogates appearing where the response surface is treated as multi-objective. The synthesis below is limited to titles, abstracts, and bibliographic metadata. It does not reanalyze full-text numerical results.

Keywords: fused filament fabrication; fused deposition modeling; process parameters; interlayer bonding; infill; mechanical properties; open access

## 1. Introduction

Material extrusion in the filament form is now a routine route to polymer and short-fiber composite parts, not only a prototyping method. Mallikarjuna et al. reviewed melt-extrusion FDM with attention to materials, process parameters, and applications that need short lead times [93]. The same process is described as FFF when the emphasis is on the filament feedstock and the raster-level thermal cycle. Gajjar et al. stated that equivalence directly while measuring tensile properties and interlayer bonding of PLA [42]. The practical question for a process engineer is which of the many adjustable settings actually move a chosen response, and which apparent effects are tied to the polymer, the reinforcement, the toolpath, or the test method.

A printed tensile bar is not a homogeneous coupon. Roads weld only where heat and pressure coincide, and the weld is weaker than the filament core when diffusion is incomplete. Omer et al. reviewed interlayer bonding in FDM as a distinct materials problem, not as a minor defect [114]. Gajjar et al. treated bonding and tensile response together, which is the right coupling: a parameter that raises bulk strength on paper can still leave a weak interface if the previous layer has cooled too far [42]. Li et al., reviewing hybrid-fiber composites made by FDM, noted that a single reinforcement often raises one mechanical property while lowering another [89]. That tradeoff reappears throughout the parameter literature. Infill patterns that lighten a part also change the load path. Birosz et al. examined infill pattern in that spirit, starting from the fact that hollow sections can be lighter and faster to build and still be asked to carry a specified mechanical duty [21].

Comparisons across laboratories are harder than the parameter lists suggest. Sola et al. surveyed open problems in tensile testing of additively manufactured polymers and used FFF as a case, including specimen design, anisotropy, and the gap between reported strength and a transferable material allowables set [143]. Surface metrics have a similar problem. Mathew et al. reviewed vapour polishing of FDM parts and showed that post-processing changes both surface finish and mechanical properties [101]. An as-printed roughness or strength number is therefore not the service condition if a chemical or thermal finishing step follows. Parameter studies that stop at the build plate and parameter studies that include finishing are answering different questions.

The experimental designs in this period are more often multi-factor than one-factor-at-a-time. Agrawal et al. varied infill pattern, infill density, and layer thickness together on ABS produced by FFF [5]. Khan et al. optimized a thick tri-material PLA–PETG–ABS laminate printed by FFF, which adds interfaces between polymers to the usual road-to-road interfaces [73]. Panico et al. treated the choice of an FDM parameter set as a multi-objective problem and combined a designed experiment with machine-learning models, on the grounds that interactions between settings and mechanical properties make a single optimum hard to declare [118]. Alarifi et al. paired mechanical tests with numerical simulation for PETG/carbon unit structures [8]. Marșavina et al. linked manufacturing parameters to tensile and fracture properties of PLA, so fracture is part of the response set, not only quasi-static strength [98].

This review asks what that 2022–2026 open-access literature, restricted to four publisher groups, actually varies and what it claims to affect. Section 2 states the retrieval and inclusion rules. Sections 3 to 8 group the 175 papers by the parameter or response family named in the title or abstract. Section 9 draws the boundaries that the abstracts support, including interactions, test-method limits, and the difference between an open-access sample and the full literature. Review articles inside the corpus are .

## 2. Review method

The search was built to satisfy three constraints at once: a fused-filament or fused-deposition process, a process parameter or a response that authors tie to such a parameter, and an open-access article from 2022 through 2026 hosted by Elsevier (the ScienceDirect publisher record), Springer Nature (Springer, Nature Portfolio, and BMC records), Wiley, or Taylor & Francis. OpenAlex was queried with those host-organization identifiers, with filters for open access, article type, English language, a DOI, an abstract, and publication year. Candidate records were dropped when the title and abstract did not identify FFF or FDM, when they did not mention a parameter or a linked response (temperature, layer height, infill, raster or orientation, speed, flow, roughness, strength, bonding, warpage, or optimization), or when the title was a non-printing use of the acronym FDM. Two such collisions, a malware-detection paper and a subway-excavation paper, were removed and replaced.

Every retained DOI was resolved on Crossref. A record stayed in the set only when the Crossref title matched the OpenAlex title at a token Jaccard similarity of at least 0.55 and the Crossref year fell between 2022 and 2026. In the final set the minimum similarity is 0.905, so the bibliographic identity of each item is tight rather than marginal. The citation rule follows the literature agent in Google’s PaperOrchestra repository (google-research/paper-orchestra): a paper enters the manuscript only after it has been retrieved and checked, and no title is added from memory. That repository’s Semantic Scholar title check (utils/scholar_utils.py) was called and returned HTTP 429 without an API key, so the existence check used here is Crossref rather than Semantic Scholar. The local clone was not modified and no pull request was opened on that repository.

The final corpus contains 175 articles: Elsevier 45, Springer Nature 47, Wiley 45, and Taylor & Francis 38. Publication years are 2022 (29), 2023 (35), 2024 (26), 2025 (33), and 2026 (52). OpenAlex open-access status is gold (65), hybrid (70), green (16), bronze (12), and diamond (12). Hybrid and green records are open-access copies, not a claim that every article in the parent journal is open. Journals that contribute the most records include Virtual and Physical Prototyping, The International Journal of Advanced Manufacturing Technology, Scientific Reports, Progress in Additive Manufacturing, and Polymer Composites. Each paper is cited at least once in Sections 3 to 8, in the theme assigned from its title and abstract.

Claims in later sections stay inside what the title and abstract support. Where an abstract states a direction of effect, that statement is attributed to the study. Where the abstract only names the factors and the responses, the text says the study examined those factors. Full-text tables were not re-extracted, so this is not a meta-analysis and it does not report pooled effect sizes.

| Publisher group | Articles | Role in the corpus |
| --- | --- | --- |
| Elsevier (ScienceDirect) | 45 | Process, mechanics, and composite studies |
| Springer Nature | 47 | Manufacturing journals and Scientific Reports |
| Wiley | 45 | Polymer and applied-materials journals |
| Taylor & Francis | 38 | Virtual and Physical Prototyping and related titles |
| Total | 175 | Each DOI resolved on Crossref |

## 3. Thermal parameters, cooling, and warpage

Temperature enters FFF at several places that the abstracts do not always separate: the nozzle setpoint, the temperature of the extrudate as it leaves the nozzle, the bed or chamber temperature that sets the cooling rate of the previous layer, and any later annealing treatment. Interlayer strength depends on whether the new road reheats the interface enough for chain diffusion before viscosity rises. Omer et al. placed that bond formation at the center of FDM performance [114], and Gajjar et al. measured tensile properties together with interlayer bonding for PLA under key process settings [42]. A higher nozzle temperature can enlarge the welding window, but it can also increase sag, stringing, or thermal degradation, so the abstracts that treat temperature as a factor are not reporting a universal “hotter is stronger” rule.

Warpage and residual stress are the geometric side of the same thermal history. Differential shrinkage between a hot road and a cooler substrate bends the part and leaves stress that later tests interpret as a material property. Studies in this corpus that name warpage, residual stress, or shrinkage are therefore process studies even when the response is a shape error rather than a strength. Annealing and crystallinity appear when the polymer can reorganize in the solid state after the build. Those treatments change both modulus and dimensional drift, which means a parameter optimum quoted for the as-printed state need not survive a heat treatment.

Cooling fan speed and chamber temperature act in the opposite direction from nozzle temperature. They shorten the time the interface stays mobile. On a small PLA part that tradeoff may be acceptable because the part must hold its shape. On a high-temperature polymer such as PEEK, or on a short-fiber composite, the abstracts more often keep the chamber warm and treat fan cooling as something to limit. The corpus includes both desktop-scale PLA studies and higher-performance feedstocks, and their temperature windows should not be averaged.

The studies assigned to this section name a thermal factor or a thermal defect in the title or abstract (28 articles). They are cited below by the factor they actually name.

Nozzle, extrusion, or printing temperature is an explicit factor in [13–14, 20, 36, 57, 109, 149, 167, 170].

Bed, build-plate, or chamber temperature is named in [16, 100, 107].

Cooling rate or fan settings are part of the experimental description in [2, 43, 45, 71].

Warpage, residual stress, or shrinkage is a stated response in [32, 56, 63, 85, 128, 157, 160].

Annealing, crystallinity, or a post-build heat treatment is discussed in [79, 84, 96, 111, 168].

## 4. Layer height, infill, and toolpath geometry

Layer height sets both the staircase error on sloped surfaces and the number of interfaces in a given thickness. A finer layer usually improves surface description and can improve bonding if the nozzle reheats a thinner, still-warm substrate, but it also lengthens the build and changes the cooling time per layer. Infill density and infill pattern decide how much of the interior is polymer and along which directions the roads run. Birosz et al. focused on infill pattern and on the mechanical role of hollow sections [21]. Agrawal et al. did not vary pattern alone: density and layer thickness were in the same experiment on ABS [5]. Reading either paper as a license to pick an infill from a software preset, without the density and layer height that went with it, overstates what the abstracts show.

Raster angle and build orientation rotate the roads relative to the load. A tensile bar printed flat with roads along the load axis is a different object from the same bar printed on edge or with a 45° raster. Sola et al. listed anisotropy among the reasons tensile results from additively manufactured polymers do not transfer cleanly between laboratories [143]. Orientation effects in this corpus should be read as toolpath effects, not as a second material.

Line width, road width, and nozzle diameter change the contact width and the pressure in the bead. They are less often the headline factor than layer height or infill, but they sit in the same geometric family: they define the cross-section that temperature and speed then have to weld.

This section cites the 20 articles whose strongest title or abstract signal is geometric or toolpath-related.

Layer height or layer thickness is a named factor in [5, 26, 77, 88, 91, 105, 113, 116, 131, 134, 146, 164].

Infill pattern, infill density, or both are named in [21–22, 59, 117, 121, 135].

Raster angle or build orientation is named in [145].

Line width, road width, nozzle diameter, air gap, or bead geometry is named in [54].

## 5. Print speed and extrusion flow

Print speed sets the time a road spends under the nozzle and the time the previous layer has to cool before it is covered. Flow rate, or an extrusion multiplier, sets whether the bead matches the commanded cross-section. Too little flow leaves gaps that later appear as porosity and weak bonds. Too much flow creates ridges, dimensional growth, and local overheating. Speed and flow are often changed together in practice because a faster travel at constant flow under-fills the road, yet many abstracts name only one of them. Where both are missing, a strength change attributed to speed alone is difficult to interpret.

Speed also couples to the thermal section. A slow perimeter on a hot bed can overheat a small PLA feature. A fast infill on a large PEEK part can drop the interface temperature below the welding range. The abstracts support that coupling as a reason to report nozzle temperature, bed temperature, and speed in the same methods paragraph. They do not support a single speed that is optimal for roughness and for interlayer strength at once.

The 1 articles placed in this section name speed or flow as a leading factor.

Print speed or feed rate is a named factor in [173].

## 6. Mechanical response, anisotropy, and interlayer failure

Most of the corpus justifies a parameter change by a mechanical test. Tensile strength and modulus dominate, followed by flexural and compressive tests, with impact and fracture less common but present. Marșavina et al. connected manufacturing parameters to tensile and fracture properties of FDM PLA [98]. Alarifi et al. reported mechanical tests and a numerical model for PETG/carbon unit structures [8]. Khan et al. optimized mechanical properties of a thick PLA–PETG–ABS composite, so the measured strength includes polymer–polymer interfaces as well as road interfaces [73]. These are different mechanical objects. A ranking of layer height taken from a monolithic PLA tensile bar does not automatically rank layer height for a tri-material flexural specimen.

Anisotropy is the mechanical expression of toolpath. Roads parallel to the load carry stress in the filament; roads perpendicular to the load force the weld to carry it. Sola et al. argued that tensile testing practice for additively manufactured polymers is not yet settled, which limits how far a reported strength can be used as a design allowable [143]. Interlayer bonding reviews make the same point from the materials side [114, 42]. Where an abstract reports only a single build orientation, the number is a process result for that orientation, not a material datasheet value.

Fiber and particle reinforcements change the interpretation again. Li et al. reviewed hybrid fiber composites printed by FDM and described gains in one property accompanied by losses in another [89]. Short fibers also alter viscosity, so the nozzle temperature and speed that weld neat PLA are not the settings that avoid nozzle clogging or fiber misalignment in a filled filament. Mechanical comparisons across neat and filled grades need the parameter set to be reported, not only the fiber weight fraction.

This section cites the 58 articles assigned here on the basis of a mechanical or bonding term in the title or abstract.

Tensile response is a stated outcome in [1, 4, 8, 18, 23, 35, 38, 41–42, 50, 53, 58, 66, 73, 75, 80, 87, 90, 92, 94, 98–99, 106, 123, 130, 132, 140, 143, 154, 161, 174–175].

Flexural or bending response is a stated outcome in [34, 46, 51, 67, 74, 102, 124].

Compressive response is a stated outcome in [40, 61, 69, 115, 120, 127, 150, 152–153].

Impact, fracture, or toughness is named in [83, 147, 163].

Interlayer bonding, adhesion, or anisotropy is named in [37, 114].

Further mechanical studies in this group are [33, 86, 89, 165–166].

## 7. Surface roughness, dimensional accuracy, and post-processing

Surface roughness in FFF is largely a geometric consequence of layer height, road width, and the stair-step on curves, modified by temperature and speed when the bead slumps or tears. Dimensional accuracy adds shrinkage, over-extrusion, and positioning error. A parameter set that maximizes tensile strength can thicken the outer wall or round a corner, so roughness and strength optima diverge. Agrawal et al. included layer thickness among the factors for ABS mechanical properties; the same factor is the first-order control on staircase roughness [5].

Mathew et al. reviewed vapour polishing and the changes it produces in surface finish and in mechanical properties [101]. That review is a warning against treating as-printed roughness as the final specification. If a study optimizes print settings for roughness and a later study polishes the same geometry, the two roughness numbers are not comparable. Dimensional studies have a related issue: accuracy after removal from the bed can shift again if the part is annealed. Thermal and geometric sections of this review should be read with that sequence in mind.

The 9 articles assigned to this section emphasize roughness, accuracy, or a finishing step in the title or abstract.

Surface roughness or surface finish is a named response in [17, 101, 112, 125, 137, 169].

Dimensional accuracy, tolerance, or circularity is a named response in [25, 28, 78].

## 8. Materials, optimization, and predictive models

Feedstock choice changes every parameter window. PLA, ABS, PETG, polyamide, and PEEK do not share a nozzle temperature, a bed temperature, or a useful print speed. Short carbon fiber, glass fiber, mineral fillers, and recycled content change viscosity and shrinkage again. Mallikarjuna et al. organized a review of FDM explicitly around materials and process parameters [93]. Li et al. narrowed the materials question to hybrid fibers and to the mechanical tradeoffs that follow [89]. Studies of filled or recycled filament in the present corpus are parameter studies only to the extent that they vary or at least report the print settings. A new filament formulation printed at one undocumented condition does not identify which setting caused a strength change.

Optimization papers try to search the coupled space rather than narrate one factor. The usual tools in the titles are Taguchi arrays, analysis of variance, response-surface models, grey relational analysis, and, more recently, machine-learning surrogates. Panico et al. combined a designed experiment with machine learning for a multi-objective FDM parameter set [118]. Khan et al. used a parametric optimization framing for the tri-material FFF laminate [73]. These methods can rank factors inside the tested box. They cannot invent a setting outside the levels that were printed, and they inherit any weakness in the mechanical test, which returns the argument to Sola et al. [143]. A model trained on one printer, one brand of PLA, and one tensile-bar orientation is a local surrogate.

Numerical models of the bead, the weld, and the residual-stress field are the other predictive route. Alarifi et al. combined simulation with tests for a PETG/carbon structure [8]. A model that takes nozzle temperature, speed, and convection as inputs is useful when it is checked against parts printed at those inputs. It is not a substitute for the missing experimental levels. Energy consumption appears in a smaller set of abstracts as a response beside strength or roughness. Where energy is included, the “best” parameter set depends on whether the objective is a mechanical property, a geometric tolerance, or the electricity used to get both.

Materials-led articles in this assignment number 27. Optimization, designed experiments, and data-driven models number 28. Articles that did not score higher on a narrower theme number 4 and are cited with them so that the reference list and the text stay in one-to-one contact.

Materials-focused studies in this group are as follows.

PLA or a PLA-based compound is the feedstock in [3, 30, 52, 64, 68, 82, 122, 126].

ABS, PETG, polyamide, PEEK, or PEI is the feedstock in [7, 19, 27, 29, 39, 72, 95, 97, 119, 144, 158, 171].

A composite, fiber-filled, or recycled feedstock is named in [49, 62, 93, 136, 148, 151, 162].

Optimization and modeling studies in this group are as follows.

A Taguchi array or a closely related orthogonal design is named in [6, 11–12, 31, 47, 70, 138, 155–156].

ANOVA, a response surface, or regression is named in [60, 65, 118, 141–142].

A machine-learning or Bayesian model is named in [44, 48, 76, 172].

A numerical or finite-element model is named in [9–10, 15, 55].

Further optimization and modeling studies in this group are [24, 81, 103, 110, 129, 133].

The remaining articles meet the inclusion rules and are cited here: [104, 108, 139, 159].

## 9. What the corpus supports, and what it does not

Four boundaries follow from the abstracts without requiring a pooled effect size. First, parameters interact. Panico et al. used that interaction as the reason a multi-objective search is needed [118]. Agrawal et al. varied infill pattern, density, and layer thickness in one design rather than in three disconnected trials [5]. A review that ranks “the most important parameter” across polymers and machines would be inventing a consensus the abstracts do not state.

Second, the response definition changes the optimum. Strength, fracture, roughness, dimensional error, warpage, and energy are different objectives. Birosz et al. looked at infill and mechanical properties of hollow sections [21]. Mathew et al. looked at surface finish after vapour polishing, which also moves mechanical properties [101]. A setting chosen for an as-printed tensile bar can be the wrong setting for a polished, load-bearing surface.

Third, the test method is part of the result. Sola et al. documented open challenges in tensile testing of additively manufactured polymers [143]. Orientation, specimen geometry, and the difference between road-direction and weld-direction failure mean that two “tensile strength” columns are comparable only when those conditions match. Interlayer reviews make the same demand of bonding data [114, 42].

Fourth, feedstock and machine bound the transfer. Hybrid-fiber systems do not move all properties in the same direction [89]. Tri-material stacks add interfaces that neat PLA does not have [73]. High-temperature polymers and short-fiber grades need different thermal boundary conditions from desktop PLA. Numerical models are informative when they are tied to the printed conditions, as in the PETG/carbon simulations of Alarifi et al. [8], and they remain local models.

The sample itself has boundaries. It is open access, English, and limited to four publisher groups in 2022–2026. Important subscription articles in the same journals, and work in other venues, are outside the set on purpose. Indexing for 2026 is only as complete as OpenAlex and Crossref were at retrieval. Abstracts omit many factor levels, so this review does not publish a recommended temperature or layer height. It maps which factors the open literature varies and which responses it attaches to them.

## 10. Conclusion

Process parameters in fused filament fabrication control a thermal and geometric process, not a list of independent printer settings. Nozzle and bed temperature, cooling, layer height, infill, raster orientation, print speed, and flow jointly determine road shape, interface welding, shrinkage, and the anisotropy of the finished part. In the 175 open-access articles reviewed here, those factors are studied most often through tensile or flexural tests, with roughness, accuracy, warpage, and energy as additional responses. Taguchi designs, ANOVA, response surfaces, and machine-learning surrogates are used to search interactions inside a tested window.

The evidence supports material-specific, response-specific parameter studies with the build orientation and the thermal boundary conditions reported. It does not support a universal optimum, a single ranking of factors, or the use of an as-printed tensile strength as a design allowable when the test method or a later polishing step differs. Fuller use of this corpus would require full-text extraction of factor levels and a pre-registered way to judge which tensile results are comparable.

## References

[1] S. AbdulAmeer, F. M. A. Altalbawy, A. H. Adhab, N. Rachchh, J. Tham, R. Kumar, et al., "Simultaneous improvement of thermal and mechanical properties of PP/SEBS/clay nanocomposite produced by Fused Filament Fabrication method," Polymer Engineering & Science, vol. 65, no. 3, pp. 1200–1213, 2024. https://doi.org/10.1002/pen.27068

[2] T. Achyut and P. K. Gurrala, "Investigating the effect of cooling rate on the strength of Fused Filament Fabrication parts using differential scanning calorimetry technique," Journal of Engineering Research, vol. 11, no. 3, pp. 14919, 2023. https://doi.org/10.36909/jer.14919

[3] S. K. Adapa, Jagadish, and S. G. Setti, "Optimization of twin screw melt mixer setup process parameters for better blending of polymers and polymer composites for FDM applications," Next Materials, vol. 8, pp. 100671, 2025. https://doi.org/10.1016/j.nxmate.2025.100671

[4] H. Afshari, F. Taher, S. A. Alavi, M. Afshari, M. R. Samadi, and F. Allahyari, "Studying the effects of FDM process parameters on the mechanical properties of parts produced from PLA using response surface methodology," Colloid and Polymer Science, vol. 302, no. 6, pp. 955–970, 2024. https://doi.org/10.1007/s00396-024-05246-x

[5] A. P. Agrawal, V. Kumar, J. Kumar, P. Paramasivam, S. Dhanasekaran, and L. Prasad, "An investigation of combined effect of infill pattern, density, and layer thickness on mechanical properties of 3D printed ABS by fused filament fabrication," Heliyon, vol. 9, no. 6, pp. e16531, 2023. https://doi.org/10.1016/j.heliyon.2023.e16531

[6] M. N. Ahmad and M. R. Ishak, "A hybrid Taguchi – Machine learning framework in optimizing FDM printing parameters," Next Materials, vol. 13, pp. 103046, 2026. https://doi.org/10.1016/j.nxmate.2026.103046

[7] H. Ahmad, A. Ahmed, S. Waheed, S. Ahmed, A. Tariq, M. A. Khan, et al., "Advancements in fused deposition modelling (FDM): a comparison of advanced composite materials, optimisation strategies, and AI/ML integration," Advances in Materials and Processing Technologies, vol. 12, no. 2, pp. 312–350, 2026. https://doi.org/10.1080/2374068x.2026.2630731

[8] I. M. Alarifi, "Mechanical properties and numerical simulation of FDM 3D printed PETG/carbon composite unit structures," Journal of Materials Research and Technology, vol. 23, pp. 656–669, 2023. https://doi.org/10.1016/j.jmrt.2023.01.043

[9] A. Almesmari, I. Barsoum, and R. K. A. Al-Rub, "Modelling, optimization, and testing of novel cuboidal spherical plate lattice structures," Virtual and Physical Prototyping, vol. 19, no. 1, pp. e2308514, 2024. https://doi.org/10.1080/17452759.2024.2308514

[10] A. Almesmari, I. Barsoum, and R. K. A. Al-Rub, "Topology optimised novel lattice structures for enhanced energy absorption and impact resistance," Virtual and Physical Prototyping, vol. 19, no. 1, pp. e2361463, 2024. https://doi.org/10.1080/17452759.2024.2361463

[11] N. H. Alrasheedi, P. M. Kumar, G. Sivanantham, and D. T. Gebreyohannes, "Multi criteria optimization of FDM process parameters for NylonAF80 filaments using CRITIC CoCoSo and machine learning approaches," Scientific Reports, vol. 16, no. 1, pp. 11213, 2026. https://doi.org/10.1038/s41598-026-38122-5

[12] H. Alzyod and P. Ficzere, "Optimizing fused filament fabrication process parameters for quality enhancement of PA12 parts using numerical modeling and taguchi method," Heliyon, vol. 9, no. 3, pp. e14445, 2023. https://doi.org/10.1016/j.heliyon.2023.e14445

[13] H. Alzyod, L. Borbas, and P. Ficzere, "Rapid prediction and optimization of the impact of printing parameters on the residual stress of FDM-ABS parts using L27 orthogonal array design and FEA," Materials Today: Proceedings, vol. 93, pp. 583–588, 2023. https://doi.org/10.1016/j.matpr.2023.02.213

[14] L. K. Andreasen, E. V. S. Andreasen, W. He, J. Rantanen, and N. Genina, "Insight into manufacturing of bespoke combination drug products containing carvedilol and simvastatin by fused deposition modeling," Pharmaceutical Development and Technology, vol. 30, no. 3, pp. 314–322, 2025. https://doi.org/10.1080/10837450.2025.2475965

[15] S. S. Avro, M. F. Rahman, T. B. Tseng, C. Lin, S. Zaman, and Y. Lin, "Physics-informed multi-head LSTM-based predictive-prescriptive framework for process parameter optimization in fused deposition modeling," Progress in Additive Manufacturing, vol. 11, no. 6, pp. 6209–6234, 2026. https://doi.org/10.1007/s40964-026-01700-0

[16] S. Azhdari, A. Avalos, M. Genest, R. G. Cole, and S. G. Kravchenko, "Analysis of uncertainty-driven thermal histories in fused filament fabrication under material and process variability," Virtual and Physical Prototyping, vol. 21, no. 1, pp. e2628400, 2026. https://doi.org/10.1080/17452759.2026.2628400

[17] N. K. Balasubramainian, L. Kothandaraman, T. Sathish, J. Giri, and M. I. Ammarullah, "Optimization of process parameters to minimize circularity error and surface roughness in fused deposition modelling (FDM) using Taguchi method for biomedical implant fabrication," Advanced Manufacturing: Polymer & Composites Science, vol. 10, no. 1, pp. 2406156, 2024. https://doi.org/10.1080/20550340.2024.2406156

[18] M. N. Bashir, J. S. Lee, M. A. Bou-Rabee, H. G. Mohamed, D. Zhou, I. A. Badruddin, et al., "Investigation of process parameter influence on the mechanical properties of FDM-printed PEEK-carbon fiber composites using RSM and Taguchi methods," Journal of Materials Research and Technology, vol. 36, pp. 10199–10209, 2025. https://doi.org/10.1016/j.jmrt.2025.05.217

[19] I. Bianchi, A. Forcellese, T. Mancia, M. Simoncini, and A. Vita, "Process parameters effect on environmental sustainability of composites FFF technology," Materials and Manufacturing Processes, vol. 37, no. 5, pp. 591–601, 2022. https://doi.org/10.1080/10426914.2022.2049300

[20] E. Billè, M. Franulović, A. Gambitta, D. Liović, A. Rondinella, F. Scalzo, et al., "Experimental investigation on the effect of the Fused Deposition Modeling parameters on the processing of Polyether Ether Ketone," Journal of Materials Research and Technology, vol. 36, pp. 8007–8021, 2025. https://doi.org/10.1016/j.jmrt.2025.04.295

[21] M. T. Birosz, D. Ledenyák, and M. Andó, "Effect of FDM infill patterns on mechanical properties," Polymer Testing, vol. 113, pp. 107654, 2022. https://doi.org/10.1016/j.polymertesting.2022.107654

[22] M. T. Birosz and M. Andó, "Effect of infill pattern scaling on mechanical properties of FDM-printed PLA specimens," Progress in Additive Manufacturing, vol. 9, no. 4, pp. 875–883, 2023. https://doi.org/10.1007/s40964-023-00487-8

[23] H. J. Biswal, M. Metcalf, C. Stefanescu, and P. Lucon, "Development of a laser‐assisted fused deposition modeling process for improvement in bond tensile strength of ABS," Journal of Polymer Science, vol. 62, no. 11, pp. 2503–2514, 2024. https://doi.org/10.1002/pol.20230926

[24] F. Bourseau, S. Grugeon, U. Lafont, and L. Dupont, "3D Printing of solvent-free PEO-Polyolefin solid polymer electrolyte by Fused Filament Fabrication," Virtual and Physical Prototyping, vol. 19, no. 1, pp. e2409975, 2024. https://doi.org/10.1080/17452759.2024.2409975

[25] I. Buj-Corral and E. E. Zayas-Figueras, "Comparative study about dimensional accuracy and form errors of FFF printed spur gears using PLA and Nylon," Polymer Testing, vol. 117, pp. 107862, 2023. https://doi.org/10.1016/j.polymertesting.2022.107862

[26] C. Cappellini, Y. Borgianni, L. Maccioni, and C. Nezzi, "The effect of process parameters on geometric deviations in 3D printing with fused deposition modelling," The International Journal of Advanced Manufacturing Technology, vol. 122, no. 3-4, pp. 1763–1803, 2022. https://doi.org/10.1007/s00170-022-09924-4

[27] B. T. Challa, S. K. Gummadi, K. Elhattab, J. Ahlstrom, and P. Sikder, "In-house processing of 3D printable polyetheretherketone (PEEK) filaments and the effect of fused deposition modeling parameters on 3D-printed PEEK structures," The International Journal of Advanced Manufacturing Technology, vol. 121, no. 3-4, pp. 1675–1688, 2022. https://doi.org/10.1007/s00170-022-09360-4

[28] N. K. Chandraker, G. N. Chander, and R. K. Dubey, "Effect of print orientation on the dimensional accuracy of three-dimensional-printed complete denture models: A comparative analysis of VAT photopolymerization and fused deposition modeling technologies," The Journal of Indian Prosthodontic Society, vol. 26, no. 1, pp. 24–31, 2026. https://doi.org/10.4103/jips.jips_334_25

[29] Y. Chen, Y. Hu, C. Li, J. Chen, Z. Hua, and X. Li, "Influence of Heat Treatment on the Mechanical and Chromatic Properties of Polyetheretherketone‐ TiO 2 Composite Manufactured Using Fused Deposition Modeling," Journal of Applied Polymer Science, pp. e71702, 2026. https://doi.org/10.1002/app.71702

[30] W. J. Chong, D. P. Simunec, A. Trinchi, I. (. Kyratzis, Y. Li, P. Wright, et al., "Advancing the additive manufacturing of PLA-ZnO nanocomposites by fused filament fabrication," Virtual and Physical Prototyping, vol. 19, no. 1, pp. e2285418, 2023. https://doi.org/10.1080/17452759.2023.2285418

[31] U. I. Cicek and A. A. Johnson, "Multi-objective optimization of FDM process parameters for 3D-printed polycarbonate using Taguchi-based Gray Relational Analysis," The International Journal of Advanced Manufacturing Technology, vol. 137, no. 7-8, pp. 3709–3725, 2025. https://doi.org/10.1007/s00170-025-15392-3

[32] C. Croitoru, I. C. Roată, and A. Olah, "The interface is the part: designing functional, graded, and multi-material architectures by multi-polymer fused filament fabrication," Virtual and Physical Prototyping, vol. 21, no. 1, pp. e2743940, 2026. https://doi.org/10.1080/17452759.2026.2743940

[33] E. Cuan-Urquizo and R. G. Silva, "Fused Filament Fabrication of cellular, lattice and porous mechanical metamaterials: a review," Virtual and Physical Prototyping, vol. 18, no. 1, pp. e2224300, 2023. https://doi.org/10.1080/17452759.2023.2224300

[34] D. Dairabayeva, A. Perveen, and D. Talamona, "Influence of fused filament fabrication parameters on the flexural strength of nylon," Manufacturing Letters, vol. 35, pp. 502–508, 2023. https://doi.org/10.1016/j.mfglet.2023.08.002

[35] H. Daoud, Y. Zheng, A. Kulig, N. Agarkov, E. Mese, W. Hofmann, et al., "Influence of Heat Treatment on Microstructure and Mechanical Properties at Elevated Temperatures of Nonweldable Ni‐Based Alloy Printed by Fused Filament Fabrication," Advanced Engineering Materials, vol. 27, no. 24, pp. 2500589, 2025. https://doi.org/10.1002/adem.202500589

[36] M. L. Dezaki, M. Bodaghi, A. Serjouei, S. Afazov, and A. Zolfagharian, "Soft Pneumatic Actuators with Controllable Stiffness by Bio‐Inspired Lattice Chambers and Fused Deposition Modeling 3D Printing," Advanced Engineering Materials, vol. 25, no. 6, pp. 2200797, 2023. https://doi.org/10.1002/adem.202200797

[37] N. Dialami, I. Rivet, M. Cervera, and M. Chiumenti, "Computational characterization of polymeric materials 3D-printed via fused filament fabrication," Mechanics of Advanced Materials and Structures, vol. 30, no. 7, pp. 1357–1367, 2022. https://doi.org/10.1080/15376494.2022.2032496

[38] L. Englert, A. Heuer, M. K. Engelskirchen, F. Frölich, S. Dietrich, W. V. Liebig, et al., "Hybrid material additive manufacturing: interlocking interfaces for fused filament fabrication on laser powder bed fusion substrates," Virtual and Physical Prototyping, vol. 17, no. 3, pp. 508–527, 2022. https://doi.org/10.1080/17452759.2022.2048228

[39] Q. Feng, W. Maier, and H. Möhring, "Application of machine learning to optimize process parameters in fused deposition modeling of PEEK material," Procedia CIRP, vol. 107, pp. 1–8, 2022. https://doi.org/10.1016/j.procir.2022.04.001

[40] J. Ferreira, S. Tavares, and V. Neto, "Influence of geometric and manufacturing parameters on the compressive behaviour of FFF lattices," Polymer International, 2026. https://doi.org/10.1002/pi.70211

[41] O. Fulkerson, E. Inman, A. Rane, H. Noori, A. Deep, and S. Ramesh, "Multi-objective Bayesian optimization of fused filament fabrication parameters for enhanced specific fracture energy in PLA-carbon fiber composites," Advanced Manufacturing: Polymer & Composites Science, vol. 10, no. 1, pp. 2395089, 2024. https://doi.org/10.1080/20550340.2024.2395089

[42] T. Gajjar, R. Yang, L. Ye, and Y. X. Zhang, "Effects of key process parameters on tensile properties and interlayer bonding behavior of 3D printed PLA using fused filament fabrication," Progress in Additive Manufacturing, vol. 10, no. 2, pp. 1261–1280, 2024. https://doi.org/10.1007/s40964-024-00704-y

[43] M. Gamesu and N. K. Akafuah, "Sharp dual-regime thermal transition driven by bead morphology in metal fused filament fabrication: bead-resolved digital twin analysis," Virtual and Physical Prototyping, vol. 21, no. 1, pp. e2675817, 2026. https://doi.org/10.1080/17452759.2026.2675817

[44] G. S. Ganitano, B. Maruyama, and G. L. Peterson, "Accelerated Multiobjective Calibration of Fused Deposition Modeling 3D Printers Using Multitask Bayesian Optimization and Computer Vision," Advanced Intelligent Systems, vol. 7, no. 4, pp. 2400523, 2025. https://doi.org/10.1002/aisy.202400523

[45] N. M. Gebre, I. Cristofolini, M. Zago, and P. Gallo, "Influence of Geometry and Size on Precision and Accuracy in Fused Deposition Modeling (FDM) Additive Manufacturing," Material Design & Processing Communication, vol. 2026, no. 1, pp. 7177386, 2026. https://doi.org/10.1155/mdp2/7177386

[46] M. Ş. Gültekin and C. Özdemir, "Optimization of Flexural Strength of PLA Flexural Test Specimens Produced by FDM Using Taguchi L27 Orthogonal Array and Hybrid Regression Model," Journal of Polymer Science, vol. 64, no. 10, pp. 2122–2137, 2026. https://doi.org/10.1002/pola.70116

[47] M. Ş. Gültekin, "Multi‐Response Optimization of FDM Process Parameters for PLA : The Strength–Energy–Roughness Trade‐Off via Taguchi, ANOVA , and Machine Learning," Journal of Polymer Science, 2026. https://doi.org/10.1002/pola.70363

[48] M. H. Golbabaei, A. Kuhzadmohammadi, Z. Porter, H. Garner, and N. Zhang, "Interpretable machine learning analysis of printing parameter effects on mechanical behavior of FDM-printed polylactic acid," MRS Communications, 2026. https://doi.org/10.1557/s43579-026-01016-8

[49] K. Goryl, M. Kočiško, R. Vandžura, and M. Pollák, "Abrasive waterjet cutting of FFF-printed ASA/aramid composites: Effects of process parameters on kerf taper, surface roughness and edge damage," Materials & Design, vol. 272, pp. 117518, 2026. https://doi.org/10.1016/j.matdes.2026.117518

[50] A. Greco, A. De Luca, R. Sepe, and S. Gerbino, "Investigation on tensile properties of FFF PEEK: Effects of printing parameters and post-processing treatment," Procedia Structural Integrity, vol. 53, pp. 178–184, 2024. https://doi.org/10.1016/j.prostr.2024.01.022

[51] M. S. Hajjaj, R. A. A. Alamoudi, W. A. Babeer, W. Y. Rizg, A. A. Basalah, S. J. Alzahrani, et al., "Flexural strength, flexural modulus and microhardness of milled vs. fused deposition modeling printed Zirconia; effect of conventional vs. speed sintering," BMC Oral Health, vol. 24, no. 1, pp. 38, 2024. https://doi.org/10.1186/s12903-023-03829-8

[52] M. Hamoud, A. B. Elshalakany, M. Gamil, and H. Mohamed, "Investigating the influence of 3D printing parameters on the mechanical characteristics of FDM fabricated (PLA/Cu) composite material," The International Journal of Advanced Manufacturing Technology, 2024. https://doi.org/10.1007/s00170-024-14313-0

[53] S. N. M. F. Han, M. M. Taha, M. R. Mansor, and M. A. A. Rahman, "Investigation of tensile and flexural properties of kenaf fiber-reinforced acrylonitrile butadiene styrene composites fabricated by fused deposition modeling," Journal of Engineering and Applied Science, vol. 69, no. 1, pp. 52, 2022. https://doi.org/10.1186/s44147-022-00109-0

[54] M. M. M. Haque, S. R. Dhrubo, A. Z. Pranto, A. Ahmed, M. M. Arefin, M. Arifuzzaman, et al., "Impact of process parameters and material selection on the mechanical performance of FDM 3D-Printed components," Hybrid Advances, vol. 10, pp. 100502, 2025. https://doi.org/10.1016/j.hybadv.2025.100502

[55] M. Hassan, M. Misra, A. Bardelcik, S. Gregori, and A. K. Mohanty, "Geometric Optimization and Mechanical Performance Enhancement of Auxetic Structures for High‐Impact Applications Through Fused Deposition Modeling," Advanced Engineering Materials, vol. 28, no. 3, pp. e202500265, 2026. https://doi.org/10.1002/adem.202500265

[56] S. Hong, W. Zhang, X. You, X. Yu, and Z. Li, "Effect of raster width on microstructure, anisotropic shrinkage, and mechanical properties of 316 L stainless steel fabricated by metal FDM," Materials Today Communications, vol. 53, pp. 115414, 2026. https://doi.org/10.1016/j.mtcomm.2026.115414

[57] G. Hu and M. Bodaghi, "Direct Fused Deposition Modeling 4D Printing and Programming of Thermoresponsive Shape Memory Polymers with Autonomous 2D‐to‐3D Shape Transformations," Advanced Engineering Materials, vol. 25, no. 19, pp. 2300334, 2023. https://doi.org/10.1002/adem.202300334

[58] Y. Hu, Y. Li, R. B. Ladani, A. P. Mouritz, H. Zhang, and S. Zhao, "3D Printed Continuous Fiber‐Polymer Composites: Fiber Damage and Mechanical Property Reductions Caused by Fused Deposition Modeling," Polymer Composites, vol. 46, no. 17, pp. 16002–16014, 2025. https://doi.org/10.1002/pc.70026

[59] M. A. Islam, M. D. Yunus, K. S. Basaruddin, N. S. Kamarrudin, M. Hassan, and T. Hoang, "Influence of Infill Geometry and Material Type on the Mechanical Performance of FDM-Printed PLA, PLA Wood, and PETG Components," Journal of Materials Engineering and Performance, 2026. https://doi.org/10.1007/s11665-026-15100-6

[60] M. Jabeur and S. Souissi, "Definitive screening design coupled with entropy‐weighted grey relational analysis for optimizing wear and strength of FDM PLA," Polymer International, vol. 75, no. 6, pp. 477–489, 2026. https://doi.org/10.1002/pi.70094

[61] A. Jadali, V. Abedini, and A. Kami, "Investigation of the influence of resin coating and heat treatment on the mechanical properties of topology-optimized parts made of polylactic acid (PLA) by the fused filament fabrication (FFF)," Progress in Additive Manufacturing, vol. 11, no. 10, pp. 10051–10070, 2026. https://doi.org/10.1007/s40964-026-01887-2

[62] F. T. Jahromi, M. Nikzad, K. Prasad, J. Norén, M. Isaksson, A. Arian, et al., "Additive manufacturing of polypropylene micro and nano composites through fused filament fabrication for automotive repair applications," Polymers for Advanced Technologies, vol. 34, no. 3, pp. 1059–1074, 2022. https://doi.org/10.1002/pat.5952

[63] B. Jiang, Y. Chen, L. Ye, L. Chang, and H. Dong, "Residual stress and warpage of additively manufactured SCF/PLA composite parts," Advanced Manufacturing: Polymer & Composites Science, vol. 9, no. 1, pp. 2171940, 2023. https://doi.org/10.1080/20550340.2023.2171940

[64] A. Karadag and O. Ulkir, "Multi‐Parameter Optimization, Machine Learning‐Based Prediction, and Surface Characterization of Bio‐Based FDM Composites," Journal of Applied Polymer Science, vol. 143, no. 33, pp. e70953, 2026. https://doi.org/10.1002/app.70953

[65] M. Karamimoghadam, M. L. Dezaki, A. Zolfagharian, and M. Bodaghi, "Influence of post-processing CO2 laser cutting and FFF 3D printing parameters on the surface morphology of PLAs: Statistical modelling and RSM optimisation," International Journal of Lightweight Materials and Manufacture, vol. 6, no. 2, pp. 285–295, 2023. https://doi.org/10.1016/j.ijlmm.2023.01.004

[66] E. Kargar and A. Ghasemi-Ghalebahman, "Experimental investigation on fatigue life and tensile strength of carbon fiber-reinforced PLA composites based on fused deposition modeling," Scientific Reports, vol. 13, no. 1, pp. 18194, 2023. https://doi.org/10.1038/s41598-023-45046-x

[67] L. W. Kariuki, B. W. Ikua, S. K. Karanja, S. P. Ng'ang'a, and H. Zeidler, "Fused filament fabrication of carbon fiber‐reinforced polymer composite: Effect of process parameters on flexural properties," Engineering Reports, vol. 6, no. 8, pp. e12807, 2023. https://doi.org/10.1002/eng2.12807

[68] F. Kartal, "Mechanical performance optimization in FFF 3D printing using Taguchi design and machine learning approach with PLA /walnut Shell composites filaments," Journal of Vinyl and Additive Technology, vol. 31, no. 3, pp. 622–638, 2025. https://doi.org/10.1002/vnl.22195

[69] V. Karupaiah, V. Narayanan, G. Kannan, O. Das, and V. Shanmugam, "Integrated Design and Process Optimization of FDM‐Fabricated Hexagonal Architected Thin‐Walled PA12 Tubes for Improved Compressive and Energy Absorption Performance," Macromolecular Materials and Engineering, vol. 311, no. 8, pp. e70309, 2026. https://doi.org/10.1002/mame.70309

[70] J. D. Kechagias, S. P. Zaoutsos, D. Chaidas, and N. Vidakis, "Multi-parameter optimization of PLA/Coconut wood compound for Fused Filament Fabrication using Robust Design," The International Journal of Advanced Manufacturing Technology, vol. 119, no. 7-8, pp. 4317–4328, 2022. https://doi.org/10.1007/s00170-022-08679-2

[71] A. Keim, J. Young, C. Hanson, M. Collins, and M. McClain, "Investigating the effect of nonuniform forced convection on local polymer properties and geometric fidelity in fused filament fabrication," npj Advanced Manufacturing, vol. 2, no. 1, pp. 46, 2025. https://doi.org/10.1038/s44334-025-00056-7

[72] M. Kepenekci, B. Gharehpapagh, U. Yaman, and S. Özerinç, "Mechanical performance of carbon fiber‐reinforced polymer cellular structures manufactured via fused filament fabrication," Polymer Composites, vol. 44, no. 8, pp. 4654–4668, 2023. https://doi.org/10.1002/pc.27429

[73] I. Khan, M. Tariq, M. Abas, M. Shakeel, F. Hira, A. A. Rashid, et al., "Parametric investigation and optimisation of mechanical properties of thick tri-material based composite of PLA-PETG-ABS 3D-printed using fused filament fabrication," Composites Part C: Open Access, vol. 12, pp. 100392, 2023. https://doi.org/10.1016/j.jcomc.2023.100392

[74] W. A. Khan, M. Hassan, I. Ahmed, M. Xiao, M. I. Faraz, K. Li, et al., "Insights into flexural and impact properties of polymer based materials printed through fused filament fabrication: Progress in the last decade," International Journal of Lightweight Materials and Manufacture, vol. 7, no. 6, pp. 925–957, 2024. https://doi.org/10.1016/j.ijlmm.2024.05.011

[75] I. Khan, M. Abas, S. Ahmad, A. A. Rashid, and M. Koç, "Fabrication of a low-cost fused filament fabrication-based 3D printer and investigation of the effects of process parameters on mechanical properties of 3D-printed samples," Journal of Engineering Research, vol. 13, no. 3, pp. 1936–1946, 2025. https://doi.org/10.1016/j.jer.2024.06.018

[76] T. Kim, D. Kim, S. Kwon, S. L. Sing, N. Kim, and I. D. Jung, "Reinforcement learning-based toolpath optimisation with 3D U-Net driven rapid thermal prediction," Virtual and Physical Prototyping, vol. 21, no. 1, pp. e2627765, 2026. https://doi.org/10.1080/17452759.2026.2627765

[77] J. Kingman and M. K. Dymond, "Fused filament fabrication and water contact angle anisotropy: The effect of layer height and raster width on the wettability of 3D printed polylactic acid parts," Chemical Data Collections, vol. 40, pp. 100884, 2022. https://doi.org/10.1016/j.cdc.2022.100884

[78] M. Kouassi, A. B. Abdallah, S. Nouira, S. Ballut, J. Fitoussi, M. Shirinbayan, et al., "FDM printing of microneedles based on biocompatible and biodegradable thermoplastic polymers," Journal of Applied Polymer Science, vol. 141, no. 41, pp. e56067, 2024. https://doi.org/10.1002/app.56067

[79] E. Kösemen, M. Bakkal, and A. T. Kuzu, "Enhancing Mechanical Performance of FDM ‐Printed ABS Parts Through Annealing Optimization," Polymer Engineering & Science, vol. 65, no. 9, pp. 4730–4739, 2025. https://doi.org/10.1002/pen.70008

[80] R. Kumaresan, K. Kadirgama, M. Samykano, W. S. W. Harun, A. Thirugnanasambandam, and K. Kanny, "In-depth study and optimization of process parameters to enhance tensile and compressive strengths of PETG in FDM technology," Journal of Materials Research and Technology, vol. 37, pp. 397–416, 2025. https://doi.org/10.1016/j.jmrt.2025.06.013

[81] R. Kumaresan, M. T. Pandurangan, and K. Kanny, "Mechanical and microstructural behavior of FDM-Printed Hyper-PLA by optimizing process parameters," The International Journal of Advanced Manufacturing Technology, vol. 143, no. 5-6, pp. 2677–2693, 2026. https://doi.org/10.1007/s00170-026-17686-6

[82] R. Kumaresan, Y. Petit, A. C. Millon, X. Legrand, K. Kanny, and M. T. Pandurangan, "Effect of FDM process parameters on the mechanical, thermal, and electrical properties of PLA/Cu composite," Progress in Additive Manufacturing, 2026. https://doi.org/10.1007/s40964-026-02004-z

[83] F. Lambiase, A. G. Stamopoulos, F. Pace, and A. Paoletti, "Influence of the deposition pattern on the interlayer fracture toughness of FDM components," The International Journal of Advanced Manufacturing Technology, vol. 128, no. 9-10, pp. 4269–4281, 2023. https://doi.org/10.1007/s00170-023-12223-1

[84] E. Lannunziata, G. Colucci, P. Minetola, and A. Giubilini, "Effect of annealing treatment and infill percentage on 3D-printed PEEK samples by Fused Filament Fabrication," The International Journal of Advanced Manufacturing Technology, vol. 131, no. 9-10, pp. 5209–5222, 2024. https://doi.org/10.1007/s00170-024-13347-8

[85] D. Laumann, D. Spiehl, and E. Dörsam, "Influence of printing material moisture on part adhesion in fused filament fabrication 3D printing," The Journal of Adhesion, vol. 100, no. 5, pp. 380–394, 2023. https://doi.org/10.1080/00218464.2023.2268531

[86] L. Le, M. A. Rabsatt, H. Eisazadeh, and M. Torabizadeh, "Reducing print time while minimizing loss in mechanical properties in consumer FDM parts," International Journal of Lightweight Materials and Manufacture, vol. 5, no. 2, pp. 197–212, 2022. https://doi.org/10.1016/j.ijlmm.2022.01.003

[87] Y. Lei, P. Qu, X. Li, Z. Liu, H. Kong, G. Yang, et al., "Research on the Mechanical Properties and Process Parameters of High‐Speed FDM Printed PLA Components Reinforced With Continuous Carbon Fiber/Epoxy Resin Pins," Polymer Composites, vol. 47, no. 9, pp. 8305–8322, 2025. https://doi.org/10.1002/pc.70689

[88] K. Lei, F. He, and M. Khan, "Tribo-acoustic informatics of FDM printed PLA surfaces under dry sliding: The coupled influence of printing parameters and surface structures," Wear, vol. 599, pp. 206758, 2026. https://doi.org/10.1016/j.wear.2026.206758

[89] S. Li, P. Cheng, S. Ahzi, Y. Peng, K. Wang, F. Chinesta, et al., "Advances in hybrid fibers reinforced polymer-based composites prepared by FDM: A review on mechanical properties and prospects," Composites Communications, vol. 40, pp. 101592, 2023. https://doi.org/10.1016/j.coco.2023.101592

[90] M. Li, Y. Xu, and J. Fang, "Orthotropic mechanical properties of PLA materials fabricated by fused deposition modeling," Thin-Walled Structures, vol. 199, pp. 111800, 2024. https://doi.org/10.1016/j.tws.2024.111800

[91] X. Lou, X. Tang, L. Dong, T. Zhao, F. Wang, L. Zhao, et al., "Influence of layer thickness and extrusion ratio on strand morphology, porosity, surface roughness, and anisotropic mechanical properties in FDM," Scientific Reports, vol. 15, no. 1, pp. 42351, 2025. https://doi.org/10.1038/s41598-025-26253-0

[92] A. De Luca, A. Greco, D. Perfetto, and R. Sepe, "Influence of Building Position and Printing Scheme on Mechanical Properties of Fused Filament Fabrication PLA Specimens," Macromolecular Symposia, vol. 411, no. 1, pp. 2300024, 2023. https://doi.org/10.1002/masy.202300024

[93] B. Mallikarjuna, P. Bhargav, S. Hiremath, K. G. Jayachristiyan, and N. Jayanth, "A review on the melt extrusion-based fused deposition modeling (FDM): background, materials, process parameters and military applications," International Journal on Interactive Design and Manufacturing (IJIDeM), vol. 19, no. 2, pp. 651–665, 2023. https://doi.org/10.1007/s12008-023-01354-0

[94] B. Mallikarjuna, V. Mallesh, M. S. Vardhan, H. G. Vadivudaiyanayak, and P. G. S. Datta, "Effect of Process Parameters on Mechanical Properties in Fused Deposition Modelling of Polyethylene Terephthalate Glycol," Procedia Structural Integrity, vol. 56, pp. 160–166, 2024. https://doi.org/10.1016/j.prostr.2024.02.051

[95] A. Maloney, I. Major, N. Gately, and D. M. Devine, "Exploring Process‐Structure–Property Relationships of PEKK and PEEK in Fused Filament Fabrication," Journal of Applied Polymer Science, vol. 142, no. 34, pp. e57347, 2025. https://doi.org/10.1002/app.57347

[96] I. A. Mansour and S. Pervaiz, "Effect of thermal annealing on mechanical properties of FDM-printed PLA: A desirability function analysis approach," Next Materials, vol. 13, pp. 102979, 2026. https://doi.org/10.1016/j.nxmate.2026.102979

[97] F. Manzoor, A. Golbang, A. McIlhagger, E. Harkin-Jones, D. Crawford, and E. Mancuso, "Effect of Zn-nanoHA concentration on the mechanical performance and bioactivity of 3D printed PEEK composites for craniofacial implants," Plastics, Rubber and Composites, vol. 52, no. 4, pp. 197–203, 2022. https://doi.org/10.1080/14658011.2022.2108986

[98] L. Marșavina, C. Vălean, M. Mărghitaș, E. Linul, N. Razavi, F. Berto, et al., "Effect of the manufacturing parameters on the tensile and fracture properties of FDM 3D-printed PLA specimens," Engineering Fracture Mechanics, vol. 274, pp. 108766, 2022. https://doi.org/10.1016/j.engfracmech.2022.108766

[99] C. L. Martin-Compaired, T. Lemmi, R. Miralbes, and D. Ranz, "Mechanical Property Comparison of Hemp and Flax Fiber Reinforced Polylactic Acid versus Additive-Enhanced and Carbon Fiber Reinforced Polylactic Acid in Fused Deposition Modeling," Journal of Natural Fibers, vol. 23, no. 1, pp. 2619884, 2026. https://doi.org/10.1080/15440478.2026.2619884

[100] C. Massaroni, V. Saroli, Z. Aloqalaa, D. L. Presti, and E. Schena, "Extrusion‐Based Fused Deposition Modeling for Printing Sensors and Electrodes: Materials, Process Parameters, and Applications," SmartMat, vol. 6, no. 4, pp. e70027, 2025. https://doi.org/10.1002/smm2.70027

[101] A. Mathew, S. R. Kishore, A. T. Tomy, M. Sugavaneswaran, S. G. Scholz, A. Elkaseer, et al., "Vapour polishing of fused deposition modelling (FDM) parts: a critical review of different techniques, and subsequent surface finish and mechanical properties of the post-processed 3D-printed parts," Progress in Additive Manufacturing, vol. 8, no. 6, pp. 1161–1178, 2023. https://doi.org/10.1007/s40964-022-00391-7

[102] J. Mazur, P. Sobczak, M. Panasiewicz, P. Łusiak, M. Krajewska, P. Findura, et al., "Mechanical properties and biodegradability of samples obtained by 3D printing using FDM technology from PLA filament with by-products," Scientific Reports, vol. 15, no. 1, pp. 5847, 2025. https://doi.org/10.1038/s41598-025-89984-0

[103] V. Meana, L. Meana, E. Cuesta, A. González, and F. Peña, "Process parameter optimization for alumina ceramic parts manufactured by fused deposition modelling," Scientific Reports, vol. 16, no. 1, pp. 6072, 2026. https://doi.org/10.1038/s41598-026-36153-6

[104] A. Meram and B. Sözen, "Experimental investigation on the effect of printing parameters on the impact response of thin-walled tubes produced by additive manufacturing method," International Journal of Crashworthiness, vol. 28, no. 1, pp. 32–45, 2022. https://doi.org/10.1080/13588265.2022.2045824

[105] A. Milovanović, S. Galațanu, A. Sedmak, L. Marșavina, I. Trajković, C. Popa, et al., "Layer thickness influence on impact properties of FDM printed PLA material," Procedia Structural Integrity, vol. 56, pp. 190–197, 2024. https://doi.org/10.1016/j.prostr.2024.02.055

[106] G. A. P. de Mélo, J. M. A. Barbosa, J. A. P. Carrasco, A. C. C. Holanda, W. F. de Amorim, A. A. Silva, et al., "Analysis of the effects of FDM printing parameters on mechanical properties of parts manufactured with a new type of PLA," The International Journal of Advanced Manufacturing Technology, vol. 143, no. 3-4, pp. 2247–2267, 2026. https://doi.org/10.1007/s00170-026-17508-9

[107] K. Moiduddin, C. Yang, S. K. Murugesan, M. Saleh, M. A. H. Ali, and U. Umer, "Interactive influence of in-situ annealing temperature and thermal processing parameters on defect minimization and strength enhancement in FDM-printed PEEK," The International Journal of Advanced Manufacturing Technology, vol. 146, no. 1-2, pp. 1235–1255, 2026. https://doi.org/10.1007/s00170-026-18895-9

[108] E. Moritzer and C. L. Elsner, "Investigation and Improvement of Processing Parameters of a Copper‐Filled Polymer Filament in Fused Filament Fabrication as a Basis for the Fabrication of Low‐Porosity Metal Parts," Macromolecular Symposia, vol. 404, no. 1, pp. 2100390, 2022. https://doi.org/10.1002/masy.202100390

[109] F. M. Mwania, M. Maringa, and J. Nsengimana, "Investigating the effect of process parameters on the degree of fusion of two adjacent tracks produced through fused deposition modelling of acrylonitrile butadiene styrene," Polymer Testing, vol. 121, pp. 107981, 2023. https://doi.org/10.1016/j.polymertesting.2023.107981

[110] F. Napolitano, E. Cozzolino, I. Papa, A. Astarita, and A. Squillace, "Experimental integrated approach for mechanical characteristic optimization of FDM-printed PLA in an energy-saving perspective," The International Journal of Advanced Manufacturing Technology, vol. 121, no. 5-6, pp. 3551–3565, 2022. https://doi.org/10.1007/s00170-022-09535-z

[111] A. Nassar, G. E. Abouseriaa, A. Alshorbagy, M. Megahed, and E. Nassar, "Effect of infill parameters and thermal annealing on the mechanical behavior of FDM 3D-printed polymer," Scientific Reports, vol. 16, no. 1, pp. 18166, 2026. https://doi.org/10.1038/s41598-026-54969-0

[112] H. O'Connor, G. Singh, A. Kumar, R. Paetzold, M. Celikin, and E. D. O'Cearbhaill, "Fused filament fabrication using stainless steel 316L ‐polymer blend: Analysis and optimization for green density and surface roughness," Polymer Composites, vol. 45, no. 12, pp. 10632–10644, 2024. https://doi.org/10.1002/pc.28496

[113] M. Olam, "Determining of process parameters of the PLA/titanium dioxide/hydroxyapatite filament," Advances in Materials and Processing Technologies, vol. 8, no. 4, pp. 4776–4787, 2022. https://doi.org/10.1080/2374068x.2022.2080332

[114] M. A. E. Omer, I. A. Shaban, A. Mourad, and H. Hegab, "Advances in interlayer bonding in fused deposition modelling: a comprehensive review," Virtual and Physical Prototyping, vol. 20, no. 1, pp. e2522951, 2025. https://doi.org/10.1080/17452759.2025.2522951

[115] R. Paetzold, F. B. Coulter, G. Singh, D. J. Kelly, and E. D. O'Cearbhaill, "Fused filament fabrication of polycaprolactone bioscaffolds: Influence of fabrication parameters and thermal environment on geometric fidelity and mechanical properties," Bioprinting, vol. 27, pp. e00206, 2022. https://doi.org/10.1016/j.bprint.2022.e00206

[116] S. Palanisamy, G. Karuppiah, P. Kumar, S. Dharmalingam, S. Mubarak, C. Santulli, et al., "Effect of Process Parameters and Material Selection on the Quality of 3D Printed Products by Fused Deposition Modeling (FDM): A Review," Advances in Polymer Technology, vol. 2024, no. 1, pp. 3480281, 2024. https://doi.org/10.1155/adv/3480281

[117] J. Č. Panić, N. Todorović, M. Rančić, M. Kalaba, I. Ristić, S. Popović, et al., "Influence of infill pattern on ketoprofen release rate from 3D printed buccal films," Drug Development and Industrial Pharmacy, vol. 52, no. 11, pp. 2302–2315, 2026. https://doi.org/10.1080/03639045.2026.2736231

[118] A. Panico, A. Corvi, L. Collini, and C. Sciancalepore, "Multi objective optimization of FDM 3D printing parameters set via design of experiments and machine learning algorithms," Scientific Reports, vol. 15, no. 1, pp. 16753, 2025. https://doi.org/10.1038/s41598-025-01016-z

[119] K. S. Patel, D. B. Shah, S. J. Joshi, F. K. Aldawood, and M. Kchaou, "Effect of process parameters on the mechanical performance of FDM printed carbon fiber reinforced PETG," Journal of Materials Research and Technology, vol. 30, pp. 8006–8018, 2024. https://doi.org/10.1016/j.jmrt.2024.05.184

[120] S. Patil, T. Sathish, N. A. Othman, B. Tarawneh, and T. Saidani, "Optimization of Compressive Strength Properties in Fused Deposition Modeling 3D Printed PLA / HA Composites for Bone Tissue Engineering Applications," Engineering Reports, vol. 7, no. 5, pp. e70133, 2025. https://doi.org/10.1002/eng2.70133

[121] S. Paulsingarayar, H. Bharath, S. Seenivasan, and K. Geetha, "Ultra High Speed Fused Filament Fabrication of Carbon Fiber‐Reinforced PLA : A Comparative Study of TPMS ‐D and Gyroid Infill Patterns," Polymer Composites, 2026. https://doi.org/10.1002/pc.71695

[122] D. F. Pereira, A. C. Branco, R. Cláudio, A. C. Marques, and C. G. Figueiredo-Pina, "Development of Composites of PLA Filled with Different Amounts of Rice Husk Fibers for Fused Deposition Modeling," Journal of Natural Fibers, vol. 20, no. 1, pp. 2162183, 2023. https://doi.org/10.1080/15440478.2022.2162183

[123] I. Phuangmali, Y. Xu, C. Sun, and L. Lin, "Effect of mechanical recycling on diffusion behavior and mechanical properties of polypropylene in fused filament fabrication," Progress in Additive Manufacturing, vol. 11, no. 9, pp. 8673–8687, 2026. https://doi.org/10.1007/s40964-026-01819-0

[124] C. Popa, M. Mărghitaș, S. Galațanu, and L. Marșavina, "Influence of thickness on the IZOD impact strength of FDM printed specimens from PLA and PETG," Procedia Structural Integrity, vol. 41, pp. 557–563, 2022. https://doi.org/10.1016/j.prostr.2022.05.064

[125] S. Prasad and S. Prakash, "Experimental investigation of laser texturing on surface roughness and wettability of PAHT CF15 fabricated by fused deposition modeling," Polymer Composites, vol. 46, no. 7, pp. 6443–6457, 2024. https://doi.org/10.1002/pc.29370

[126] N. S. R, T. M. N. Tran, S. M. K. Thiagamani, J. Subramanian, S. Krishnasamy, C. Muthukumar, et al., "Micronized Banyan Tree Aerial-Root Powder-Reinforced PLA Biocomposites for Fused Filament Fabrication: Processing, Structure, and Property Relationships," Journal of Natural Fibers, vol. 23, no. 1, pp. 2698852, 2026. https://doi.org/10.1080/15440478.2026.2698852

[127] M. M. Rahman, J. Sultana, S. B. Rayhan, and A. Ahmed, "Optimization of FDM manufacturing parameters for the compressive behavior of cubic lattice cores: an experimental approach by Taguchi method," The International Journal of Advanced Manufacturing Technology, vol. 129, no. 3-4, pp. 1329–1343, 2023. https://doi.org/10.1007/s00170-023-12342-9

[128] K. Rahmani, C. Branfoot, and M. Bodaghi, "Bio-derived PA11/bamboo charcoal/glass fibre composites for fused filament fabrication, warpage control, strength and flame retardancy," Virtual and Physical Prototyping, vol. 20, no. 1, pp. e2589848, 2025. https://doi.org/10.1080/17452759.2025.2589848

[129] S. Raja, M. Jayalakshmi, M. A. Rusho, V. K. Selvaraj, J. Subramanian, S. Yishak, et al., "Fused deposition modeling process parameter optimization on the development of graphene enhanced polyethylene terephthalate glycol," Scientific Reports, vol. 14, no. 1, pp. 30744, 2024. https://doi.org/10.1038/s41598-024-80376-4

[130] P. Rathod, D. Washimkar, N. Ambhore, and P. Anerao, "A review of process parameter optimization to enhance the performance of mechanical properties in Fused Filament Fabrication," Journal of Engineering and Applied Science, vol. 73, no. 1, pp. 182, 2026. https://doi.org/10.1186/s44147-026-01042-2

[131] U. Raza, A. Ahmed, S. Waheed, M. Abid, M. Tahir, A. Zahid, et al., "Recent Advancements in Fused Deposition Modeling," Polymers for Advanced Technologies, vol. 36, no. 1, pp. e70028, 2025. https://doi.org/10.1002/pat.70028

[132] M. Razavi‐Nouri, M. S. Afsharkohan, A. M. Rezadoust, and Z. Zaredar, "Printability and mechanical properties of solution impregnated continuous jute yarn reinforced acrylonitrile butadiene styrene composites fabricated by fused deposition modeling," Polymer Composites, vol. 45, no. 12, pp. 11312–11327, 2024. https://doi.org/10.1002/pc.28567

[133] H. Ren, X. Yang, Z. Wang, X. Xu, R. Wang, Q. Ge, et al., "Smart structures with embedded flexible sensors fabricated by fused deposition modeling-based multimaterial 3D printing," International Journal of Smart and Nano Materials, vol. 13, no. 3, pp. 447–464, 2022. https://doi.org/10.1080/19475411.2022.2095454

[134] C. F. O. Roa, L. A. B. Mendivelso, and L. K. H. Quintero, "Effect of activation temperature and layer height on the geometric recovery of 4D honeycomb structures via fused filament fabrication using PLA/TPU (90/10 wt%) filament," Progress in Additive Manufacturing, vol. 11, no. 8, pp. 7445–7468, 2026. https://doi.org/10.1007/s40964-026-01749-x

[135] L. T. Sanford, I. H. Jaafar, A. Seibi, and A. Gohn, "The effect of infill angle, build orientation, and void fraction on the tensile strength and fracture of 3D printed ASA via fused filament fabrication," Manufacturing Letters, vol. 33, pp. 569–573, 2022. https://doi.org/10.1016/j.mfglet.2022.07.070

[136] J. Schmid, T. Prescher, and J. Keller, "Exploring the impact of FDM process parameters targeting visual appearance on the environmental impact of a product," Progress in Additive Manufacturing, 2026. https://doi.org/10.1007/s40964-026-02059-y

[137] A. Selvam, S. Mayilswamy, R. Whenish, K. Naresh, V. Shanmugam, and O. Das, "Multi-objective optimization and prediction of surface roughness and printing time in FFF printed ABS polymer," Scientific Reports, vol. 12, no. 1, pp. 16887, 2022. https://doi.org/10.1038/s41598-022-20782-8

[138] Z. Shakeri, K. Benfriha, N. Zirak, and M. Shirinbayan, "Mechanical strength and shape accuracy optimization of polyamide FFF parts using grey relational analysis," Scientific Reports, vol. 12, no. 1, pp. 13142, 2022. https://doi.org/10.1038/s41598-022-17302-z

[139] K. Shomenov, M. H. Ali, N. Jyeniskhan, A. Al-Ashaab, and E. Shehab, "Cost-effective sensor-based digital twin for fused deposition modeling 3D printers," International Journal of Computer Integrated Manufacturing, vol. 39, no. 7, pp. 937–956, 2025. https://doi.org/10.1080/0951192x.2025.2504085

[140] D. P. Simunec, P. Kothavade, A. Kafi, J. Dilag, and S. Bateman, "Influence of molecular weight distribution on mechanical and interlayer properties of FFF printed PA12," Progress in Additive Manufacturing, vol. 11, no. 4, pp. 4419–4435, 2026. https://doi.org/10.1007/s40964-026-01594-y

[141] M. Singh and P. S. Bharti, "Grey relational analysis based optimization of process parameters for efficient performance of fused deposition modelling based 3D printer," Journal of Engineering Research, 2022. https://doi.org/10.36909/jer.icmet.17159

[142] I. Siraj and Á. Drégelyi-Kiss, "Empirical comparison of FDM additive manufacturing process parameters by application grey relational analysis and multi-linear regression," The International Journal of Advanced Manufacturing Technology, vol. 138, no. 7-8, pp. 2861–2876, 2025. https://doi.org/10.1007/s00170-025-15688-4

[143] A. Sola, W. J. Chong, D. P. Simunec, Y. Li, A. Trinchi, I. (. Kyratzis, et al., "Open challenges in tensile testing of additively manufactured polymers: A literature survey and a case study in fused filament fabrication," Polymer Testing, vol. 117, pp. 107859, 2023. https://doi.org/10.1016/j.polymertesting.2022.107859

[144] S. Y. Sonaye, K. Elhattab, L. R. Duncan, S. R. Dharmavarapu, V. V. Nayak, E. N. Noshahri, et al., "Influence of fused deposition modeling parameters on the mechanical and thermal properties of 3D-printed PEEK dental endosseous implants," Dental Materials, vol. 42, no. 1, pp. 109–125, 2026. https://doi.org/10.1016/j.dental.2025.09.013

[145] W. Song, X. Zhang, K. Liu, X. Yu, J. Zheng, Y. Chen, et al., "On the coupling effects of temperature and raster angle on the mechanical response and constitutive modelling of FDM-processed SCF-PA12 composites," Virtual and Physical Prototyping, vol. 21, no. 1, pp. e2610023, 2026. https://doi.org/10.1080/17452759.2025.2610023

[146] C. Spanier, C. Schwahn, K. Krey, and A. Ratzmann, "Fused filament fabrication (FFF): influence of layer height on forces and moments delivered by aligners—an in vitro study," Clinical Oral Investigations, vol. 27, no. 5, pp. 2163–2173, 2023. https://doi.org/10.1007/s00784-023-04912-8

[147] A. G. Stamopoulos, S. I. Scipioni, and F. Lambiase, "Experimental characterization of the interlayer fracture toughness of FDM components," Composite Structures, vol. 320, pp. 117213, 2023. https://doi.org/10.1016/j.compstruct.2023.117213

[148] V. N. Sukumaar, S. M. Rangappa, Y. Liu, and S. Siengchin, "A comprehensive review on the influence of fused deposition modelling process parameters upon thermoplastic composite materials," Advanced Industrial and Engineering Polymer Research, vol. 9, no. 2, pp. 281–303, 2026. https://doi.org/10.1016/j.aiepr.2025.11.006

[149] Q. Sun, J. Ma, J. Man, Z. Ali, C. Gao, P. H. Kamm, et al., "Effect of printing parameters and heat treatment on the crystallinity of PEEK by fused filament fabrication," Journal of Materials Research and Technology, vol. 43, pp. 5269–5281, 2026. https://doi.org/10.1016/j.jmrt.2026.07.127

[150] D. Syrlybayev, A. Perveen, and D. Talamona, "Experimental investigation of mechanical properties and energy absorption capabilities of hybrid lattice structures manufactured using fused filament fabrication," The International Journal of Advanced Manufacturing Technology, vol. 125, no. 5-6, pp. 2833–2850, 2023. https://doi.org/10.1007/s00170-023-10922-3

[151] Y. Tao, P. Li, J. Zhang, S. Wang, S. Q. Shi, and F. Kong, "A review of fused filament fabrication of continuous natural fiber reinforced thermoplastic composites: Techniques and materials," Polymer Composites, vol. 44, no. 12, pp. 8200–8222, 2023. https://doi.org/10.1002/pc.27477

[152] A. E. Tetteh, J. A. Smith, D. A. Porter, M. A. Di Prima, and S. M. Kurtz, "Investigating the Impact of Fused Filament Fabrication Process Parameters on the Compressive Properties of Porous PEEK and PEKK Biomaterials," Journal of Biomedical Materials Research Part A, vol. 114, no. 3, pp. e70053, 2026. https://doi.org/10.1002/jbm.a.70053

[153] A. E. Tetteh, J. A. Smith, H. Spece, D. A. Porter, M. A. Di Prima, and S. M. Kurtz, "Optimization of fused filament fabrication process parameters to improve the compressive properties of PEEK and PEKK biomaterials," Journal of the Mechanical Behavior of Biomedical Materials, vol. 173, pp. 107203, 2026. https://doi.org/10.1016/j.jmbbm.2025.107203

[154] A. Thakur, U. K. Vates, and S. Mishra, "Parametric optimization of 3D-printed PLA part using response surface methodology for mechanical properties," Smart Science, vol. 12, no. 1, pp. 91–104, 2023. https://doi.org/10.1080/23080477.2023.2270819

[155] P. Thejasree, N. Manikandan, N. Rajesh, R. Lokanadham, P. C. Krishnamachary, K. Shubham, et al., "Application of Taguchi Grey-Based ANFIS model for prediction of process parameters in fused deposition modelling of PETG," Scientific Reports, vol. 15, no. 1, pp. 37398, 2025. https://doi.org/10.1038/s41598-025-21248-3

[156] O. Ulkir, M. S. Bayraklılar, and M. Kuncan, "Taguchi‐ ANN Hybrid Approach for Evaluating Unsupported Overhang Structures in FDM ‐Printed Polymers," Journal of Polymer Science, vol. 63, no. 23, pp. 5185–5207, 2025. https://doi.org/10.1002/pol.20250752

[157] N. Verma, P. Awasthi, A. Gupta, and S. S. Banerjee, "Fused Deposition Modeling of Polyolefins: Challenges and Opportunities," Macromolecular Materials and Engineering, vol. 308, no. 1, pp. 2200421, 2022. https://doi.org/10.1002/mame.202200421

[158] N. Vidakis, M. Petousis, E. Velidakis, L. Tzounis, N. Mountakis, O. Boura, et al., "Multi-functional polyamide 12 (PA12)/ multiwall carbon nanotube 3D printed nanocomposites with enhanced mechanical and electrical properties," Advanced Composite Materials, vol. 31, no. 6, pp. 630–654, 2022. https://doi.org/10.1080/09243046.2022.2076019

[159] Z. Wang, Z. Guo, Z. Li, and K. Zeng, "Design, manufacture, and characterisation of hierarchical metamaterials for simultaneous ultra-broadband sound-absorbing and superior mechanical performance," Virtual and Physical Prototyping, vol. 18, no. 1, pp. e2111585, 2022. https://doi.org/10.1080/17452759.2022.2111585

[160] P. B. Wang, T. Yang, J. W. Hu, and J. Zhang, "The influence of in situ microfibrillation on the mechanical properties and warpage of low‐density polyethylene/polystyrene composite prepared by fused filament fabrication," Journal of Applied Polymer Science, vol. 141, no. 29, pp. e55671, 2024. https://doi.org/10.1002/app.55671

[161] L. Wang, Z. Liu, T. Qiu, L. Deng, Y. Zhang, and X. Wang, "The influence of internal defects on the fatigue behavior of 4032D polylactic acid in fused deposition modeling," Journal of Materials Research and Technology, vol. 36, pp. 548–560, 2025. https://doi.org/10.1016/j.jmrt.2025.03.138

[162] Q. Wei, R. Yang, X. Zhao, J. Zhou, Y. An, and S. Yang, "Fused deposition modeling of carbon‐reinforced polymer matrix composites: A comprehensive review," Polymer Composites, vol. 44, no. 9, pp. 5313–5345, 2023. https://doi.org/10.1002/pc.27498

[163] K. Winters and E. I. L. Jull, "The role of FFF process parameters on impact strength: a review," The International Journal of Advanced Manufacturing Technology, vol. 143, no. 7-8, pp. 3515–3530, 2026. https://doi.org/10.1007/s00170-026-17540-9

[164] S. Wüstenhagen, T. Wagner, A. Krombholz, P. Hirsch, J. Szep, L. Votta, et al., "High Throughput Screening of Process Parameters for Quality Control of Additive Manufacturing by Fused Filament Fabrication," Macromolecular Symposia, vol. 414, no. 5, pp. e70116, 2025. https://doi.org/10.1002/masy.70116

[165] W. Xiong, W. Wang, X. Lin, C. K. Chua, and K. Zhu, "Gradient structure design and mechanical performance analysis of porous bone scaffold based on FDM technology," Virtual and Physical Prototyping, vol. 21, no. 1, pp. e2617067, 2026. https://doi.org/10.1080/17452759.2026.2617067

[166] Y. Xu, M. Huang, and A. K. Schlarb, "Print path‐dependent contact temperature dependency for 3D printing using fused filament fabrication," Journal of Applied Polymer Science, vol. 139, no. 24, pp. 52337, 2022. https://doi.org/10.1002/app.52337

[167] C. Yancy, Y. Jin, T. Wang, S. Shahriar, J. Zhou, R. Rayegan, et al., "The effects of printing parameters on thermal gradients and cooling rate on mechanical properties in FDM," The International Journal of Advanced Manufacturing Technology, vol. 146, no. 5-6, pp. 3203–3221, 2026. https://doi.org/10.1007/s00170-026-18935-4

[168] T. Yang, J. Leng, J. Hu, P. Wang, M. Edeleva, L. Cardon, et al., "Enhancing thermal conductivity and balancing mechanical properties of 3D-printed iPP/HDPE-based dielectric composites via the introduction of hybrid fillers and tailored crystalline structure," Virtual and Physical Prototyping, vol. 18, no. 1, pp. e2230215, 2023. https://doi.org/10.1080/17452759.2023.2230215

[169] Y. A. Yildirim, B. Yildirim, O. Ulkir, and M. Kuncan, "Experimental and ANN Modeling of Mechanical Properties and Surface Quality in Multi‐Material FDM Printing: Effects of Retraction Parameters," Polymers for Advanced Technologies, vol. 37, no. 5, pp. e70620, 2026. https://doi.org/10.1002/pat.70620

[170] J. Zenzerovic, F. Sordetti, A. Lanzutti, and E. Salvati, "Influence of fused filament fabrication process parameters on the quasi-static mechanical behaviour and failure mechanisms of 316L stainless steel," Engineering Failure Analysis, vol. 186, pp. 110532, 2026. https://doi.org/10.1016/j.engfailanal.2026.110532

[171] S. Zhang, W. Bai, L. Meng, P. Chen, J. Wang, K. Wei, et al., "Hybrid additive manufacturing of high-quality polyetheretherketone (PEEK) -Ag conformal circuits by a laser in-situ crystallisation assisted fused deposition modelling and laser micro-cladding technique," Virtual and Physical Prototyping, vol. 20, no. 1, pp. e2536563, 2025. https://doi.org/10.1080/17452759.2025.2536563

[172] H. Zhang, Y. Yu, X. Liu, N. Liang, Y. Kim, D. Shin, et al., "Autonomous printing process optimisation and in-situ anomaly detection in fused deposition modelling using an integrated data-driven approach," Virtual and Physical Prototyping, vol. 20, no. 1, pp. e2545523, 2025. https://doi.org/10.1080/17452759.2025.2545523

[173] H. Zhou, J. Zhang, S. E. Lim, E. Ferraris, and H. Le Ferrand, "Rationalising the onset of bistability in polylactic acid (PLA) bilayer laminates using Fused Filament Fabrication (FFF)," Virtual and Physical Prototyping, vol. 21, no. 1, pp. e2618395, 2026. https://doi.org/10.1080/17452759.2026.2618395

[174] M. Özkül, F. Kuncan, and O. Ulkir, "Predicting Mechanical Properties of FDM‐Produced Parts Using Machine Learning Approaches," Journal of Applied Polymer Science, vol. 142, no. 20, pp. e56899, 2025. https://doi.org/10.1002/app.56899

[175] A. Zolfaghari, A. G. Roshan, and M. Shakeri, "Investigating physical and mechanical properties of alumina/acrylonitrile butadiene styrene composites manufactured by fused deposition modeling," Polymer Composites, vol. 46, no. 6, pp. 5508–5516, 2024. https://doi.org/10.1002/pc.29307
