#!/usr/bin/env python3
"""Build the FFF process-parameter review from the Crossref-checked corpus."""

import html
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parent
CORPUS_PATH = Path("/tmp/fff-review/verified_175.json")
DOCX_PATH = ROOT / "Influence-of-Process-Parameters-in-FFF.docx"
MD_PATH = ROOT / "manuscript.md"
META_PATH = ROOT / "references.json"
ARTIFACT = Path("/opt/cursor/artifacts/Influence-of-Process-Parameters-in-FFF.docx")

papers = json.load(open(CORPUS_PATH))
by_id = {p["ref_id"]: p for p in papers}
assert sorted(by_id) == list(range(1, 176))

# Guard the hand-cited studies so a renumber cannot attach the wrong claim.
assert "infill patterns" in by_id[21]["title"].lower()
assert "tensile and fracture" in by_id[98]["title"].lower()
assert "infill pattern, density, and layer thickness" in by_id[5]["title"].lower()
assert by_id[93]["title"].lower().startswith("a review on the melt extrusion")
assert "hybrid fiber" in by_id[89]["title"].lower() or "hybrid fibers" in by_id[89]["title"].lower()
assert "interlayer bonding" in by_id[42]["title"].lower()
assert "open challenges in tensile testing" in by_id[143]["title"].lower()
assert "tri-material" in by_id[73]["title"].lower()
assert "machine learning" in by_id[118]["title"].lower()
assert by_id[114]["title"].lower().startswith("advances in interlayer bonding")
assert "petg/carbon" in by_id[8]["title"].lower()
assert "vapour polishing" in by_id[101]["title"].lower() or "vapor polishing" in by_id[101]["title"].lower()

CITED = set()


def blob(p):
    return f"{p['title']} {p.get('abstract', '')}"


def has(p, pattern):
    return re.search(pattern, blob(p), re.I) is not None


def cite(ids):
    ids = sorted({int(i) for i in ids})
    if not ids:
        return ""
    CITED.update(ids)
    ranges = []
    start = prev = ids[0]
    for n in ids[1:]:
        if n == prev + 1:
            prev = n
            continue
        ranges.append((start, prev))
        start = prev = n
    ranges.append((start, prev))
    parts = []
    for a, b in ranges:
        parts.append(str(a) if a == b else f"{a}–{b}")
    return "[" + ", ".join(parts) + "]"


THEME_RULES = [
    (
        "thermal",
        r"nozzle temperature|extrusion temperature|printing temperature|bed temperature|"
        r"chamber temperature|build[- ]plate temperature|cooling|anneal|crystallin|"
        r"warpage|residual stress|shrink",
    ),
    (
        "geometry",
        r"layer height|layer thickness|infill|raster|build orientation|printing orientation|"
        r"raster angle|line width|road width|nozzle diameter|air gap",
    ),
    (
        "kinematics",
        r"print(?:ing)? speed|flow rate|extrusion rate|feed rate|deposition speed",
    ),
    (
        "quality",
        r"surface roughness|dimensional accuracy|circularity|tolerance|surface finish|"
        r"vapou?r polish|surface quality",
    ),
    (
        "mechanical",
        r"tensile|flexural|compressive|impact strength|fracture|interlayer|bonding|"
        r"anisotropic|mechanical propert",
    ),
    (
        "materials",
        r"composite|fibre|fiber|peek|recycled|nanocomposite|biocomposite|short carbon",
    ),
    (
        "optimization",
        r"optimis|optimiz|taguchi|anova|response surface|machine learning|neural|"
        r"grey relational|multi-?objective|bayesian",
    ),
]


def theme_of(p):
    title = p["title"]
    abstract = p.get("abstract") or ""
    best, best_score = "general", 0
    for name, pat in THEME_RULES:
        score = 0
        if re.search(pat, title, re.I):
            score += 3
        if re.search(pat, abstract, re.I):
            score += 1
        if score > best_score:
            best, best_score = name, score
    return best


groups = defaultdict(list)
for p in papers:
    p["theme"] = theme_of(p)
    groups[p["theme"]].append(p)

pub_counts = Counter(p["publisher_group"] for p in papers)
year_counts = Counter(p["year"] for p in papers)
oa_counts = Counter(p["oa_status"] or "unspecified" for p in papers)


def ids_where(pool, pattern):
    return [p["ref_id"] for p in pool if has(p, pattern)]


def partition_sentences(pool, subgroups, remainder_template):
    remaining = {p["ref_id"] for p in pool}
    lookup = {p["ref_id"]: p for p in pool}
    out = []
    for pattern, template in subgroups:
        hit = [i for i in sorted(remaining) if has(lookup[i], pattern)]
        if not hit:
            continue
        out.append(template.format(c=cite(hit)))
        remaining -= set(hit)
    if remaining:
        out.append(remainder_template.format(c=cite(sorted(remaining))))
    return out


def unescape(text):
    return html.unescape(text or "").replace("\n", " ").strip()


blocks = []


def h1(text):
    blocks.append(("h1", text))


def h2(text):
    blocks.append(("h2", text))


def para(text):
    blocks.append(("p", text))


def table(headers, rows):
    blocks.append(("table", headers, rows))


h1("Influence of Process Parameters in Fused Filament Fabrication: A Review of Open-Access Studies, 2022–2026")
para("Selva")
para("22 November 2026")

h2("Abstract")
para(
    "Fused filament fabrication (FFF), also called fused deposition modeling (FDM) in much of the "
    "process literature, builds a thermoplastic part by pushing a solid filament through a heated "
    "nozzle and depositing roads in layers. Nozzle and bed temperature, layer height, infill, raster "
    "or build orientation, print speed, and extrusion flow do not act as independent dials. They set "
    "the thermal history of each road, the contact area between roads, the amount of material in the "
    "cross-section, and the time available for diffusion across the interface. This review covers "
    "175 open-access journal articles with publication years 2022 through 2026 whose primary host "
    "organization in OpenAlex is Elsevier, Springer Nature, Wiley, or Taylor & Francis. Records were "
    "kept when the title or abstract identified FFF or FDM and at least one process parameter or a "
    "parameter-linked response, and only after Crossref returned a matching title and a year inside "
    "that window. Across the corpus, strength, interlayer bonding, roughness, dimensional error, "
    "warpage, and energy use are the responses authors most often attach to those settings. The "
    "studies do not support one ranking of parameters that travels from PLA to PEEK, or from a "
    "desktop printer to a heated-chamber machine. Designed experiments and regression remain the "
    "dominant analysis tools, with machine-learning surrogates appearing where the response surface "
    "is treated as multi-objective. The synthesis below is limited to titles, abstracts, and "
    "bibliographic metadata. It does not reanalyze full-text numerical results."
)
para(
    "Keywords: fused filament fabrication; fused deposition modeling; process parameters; "
    "interlayer bonding; infill; mechanical properties; open access"
)

h2("1. Introduction")
para(
    "Material extrusion in the filament form is now a routine route to polymer and short-fiber "
    "composite parts, not only a prototyping method. Mallikarjuna et al. reviewed melt-extrusion "
    "FDM with attention to materials, process parameters, and applications that need short lead "
    "times [93]. The same process is described as FFF when the emphasis is on the filament feedstock "
    "and the raster-level thermal cycle. Gajjar et al. stated that equivalence directly while "
    "measuring tensile properties and interlayer bonding of PLA [42]. The practical question for a "
    "process engineer is which of the many adjustable settings actually move a chosen response, and "
    "which apparent effects are tied to the polymer, the reinforcement, the toolpath, or the test method."
)
para(
    "A printed tensile bar is not a homogeneous coupon. Roads weld only where heat and pressure "
    "coincide, and the weld is weaker than the filament core when diffusion is incomplete. Omer et al. "
    "reviewed interlayer bonding in FDM as a distinct materials problem, not as a minor defect [114]. "
    "Gajjar et al. treated bonding and tensile response together, which is the right coupling: a "
    "parameter that raises bulk strength on paper can still leave a weak interface if the previous "
    "layer has cooled too far [42]. Li et al., reviewing hybrid-fiber composites made by FDM, noted "
    "that a single reinforcement often raises one mechanical property while lowering another [89]. "
    "That tradeoff reappears throughout the parameter literature. Infill patterns that lighten a part "
    "also change the load path. Birosz et al. examined infill pattern in that spirit, starting from "
    "the fact that hollow sections can be lighter and faster to build and still be asked to carry a "
    "specified mechanical duty [21]."
)
para(
    "Comparisons across laboratories are harder than the parameter lists suggest. Sola et al. surveyed "
    "open problems in tensile testing of additively manufactured polymers and used FFF as a case, "
    "including specimen design, anisotropy, and the gap between reported strength and a transferable "
    "material allowables set [143]. Surface metrics have a similar problem. Mathew et al. reviewed "
    "vapour polishing of FDM parts and showed that post-processing changes both surface finish and "
    "mechanical properties [101]. An as-printed roughness or strength number is therefore not the "
    "service condition if a chemical or thermal finishing step follows. Parameter studies that stop "
    "at the build plate and parameter studies that include finishing are answering different questions."
)
para(
    "The experimental designs in this period are more often multi-factor than one-factor-at-a-time. "
    "Agrawal et al. varied infill pattern, infill density, and layer thickness together on ABS produced "
    "by FFF [5]. Khan et al. optimized a thick tri-material PLA–PETG–ABS laminate printed by FFF, "
    "which adds interfaces between polymers to the usual road-to-road interfaces [73]. Panico et al. "
    "treated the choice of an FDM parameter set as a multi-objective problem and combined a designed "
    "experiment with machine-learning models, on the grounds that interactions between settings and "
    "mechanical properties make a single optimum hard to declare [118]. Alarifi et al. paired "
    "mechanical tests with numerical simulation for PETG/carbon unit structures [8]. Marșavina et al. "
    "linked manufacturing parameters to tensile and fracture properties of PLA, so fracture is part "
    "of the response set, not only quasi-static strength [98]."
)
para(
    "This review asks what that 2022–2026 open-access literature, restricted to four publisher groups, "
    "actually varies and what it claims to affect. Section 2 states the retrieval and inclusion rules. "
    "Sections 3 to 8 group the 175 papers by the parameter or response family named in the title or "
    "abstract. Section 9 draws the boundaries that the abstracts support, including interactions, "
    "test-method limits, and the difference between an open-access sample and the full literature. "
    f"Review articles inside the corpus are {cite(i for i, p in by_id.items() if re.search(r'\\breview\\b', p['title'], re.I))}."
)

h2("2. Review method")
para(
    "The search was built to satisfy three constraints at once: a fused-filament or fused-deposition "
    "process, a process parameter or a response that authors tie to such a parameter, and an "
    "open-access article from 2022 through 2026 hosted by Elsevier (the ScienceDirect publisher "
    "record), Springer Nature (Springer, Nature Portfolio, and BMC records), Wiley, or Taylor & "
    "Francis. OpenAlex was queried with those host-organization identifiers, with filters for "
    "open access, article type, English language, a DOI, an abstract, and publication year. "
    "Candidate records were dropped when the title and abstract did not identify FFF or FDM, when "
    "they did not mention a parameter or a linked response (temperature, layer height, infill, "
    "raster or orientation, speed, flow, roughness, strength, bonding, warpage, or optimization), "
    "or when the title was a non-printing use of the acronym FDM. Two such collisions, a malware-detection "
    "paper and a subway-excavation paper, were removed and replaced."
)
para(
    "Every retained DOI was resolved on Crossref. A record stayed in the set only when the Crossref "
    "title matched the OpenAlex title at a token Jaccard similarity of at least 0.55 and the Crossref "
    "year fell between 2022 and 2026. In the final set the minimum similarity is "
    f"{min(p['title_similarity'] for p in papers):.3f}, so the bibliographic identity of each item is "
    "tight rather than marginal. The citation rule follows the literature agent in Google’s "
    "PaperOrchestra repository (google-research/paper-orchestra): a paper enters the manuscript only "
    "after it has been retrieved and checked, and no title is added from memory. That repository’s "
    "Semantic Scholar title check (utils/scholar_utils.py) was called and returned HTTP 429 without "
    "an API key, so the existence check used here is Crossref rather than Semantic Scholar. The "
    "local clone was not modified and no pull request was opened on that repository."
)
para(
    f"The final corpus contains 175 articles: Elsevier {pub_counts['Elsevier']}, Springer Nature "
    f"{pub_counts['Springer Nature']}, Wiley {pub_counts['Wiley']}, and Taylor & Francis "
    f"{pub_counts['Taylor & Francis']}. Publication years are 2022 ({year_counts[2022]}), "
    f"2023 ({year_counts[2023]}), 2024 ({year_counts[2024]}), 2025 ({year_counts[2025]}), and "
    f"2026 ({year_counts[2026]}). OpenAlex open-access status is gold ({oa_counts.get('gold', 0)}), "
    f"hybrid ({oa_counts.get('hybrid', 0)}), green ({oa_counts.get('green', 0)}), "
    f"bronze ({oa_counts.get('bronze', 0)}), and diamond ({oa_counts.get('diamond', 0)}). "
    "Hybrid and green records are open-access copies, not a claim that every article in the parent "
    "journal is open. Journals that contribute the most records include Virtual and Physical "
    "Prototyping, The International Journal of Advanced Manufacturing Technology, Scientific Reports, "
    "Progress in Additive Manufacturing, and Polymer Composites. Each paper is cited at least once "
    "in Sections 3 to 8, in the theme assigned from its title and abstract."
)
para(
    "Claims in later sections stay inside what the title and abstract support. Where an abstract "
    "states a direction of effect, that statement is attributed to the study. Where the abstract "
    "only names the factors and the responses, the text says the study examined those factors. "
    "Full-text tables were not re-extracted, so this is not a meta-analysis and it does not report "
    "pooled effect sizes."
)

table(
    ["Publisher group", "Articles", "Role in the corpus"],
    [
        ["Elsevier (ScienceDirect)", str(pub_counts["Elsevier"]), "Process, mechanics, and composite studies"],
        ["Springer Nature", str(pub_counts["Springer Nature"]), "Manufacturing journals and Scientific Reports"],
        ["Wiley", str(pub_counts["Wiley"]), "Polymer and applied-materials journals"],
        ["Taylor & Francis", str(pub_counts["Taylor & Francis"]), "Virtual and Physical Prototyping and related titles"],
        ["Total", "175", "Each DOI resolved on Crossref"],
    ],
)

h2("3. Thermal parameters, cooling, and warpage")
para(
    "Temperature enters FFF at several places that the abstracts do not always separate: the nozzle "
    "setpoint, the temperature of the extrudate as it leaves the nozzle, the bed or chamber "
    "temperature that sets the cooling rate of the previous layer, and any later annealing treatment. "
    "Interlayer strength depends on whether the new road reheats the interface enough for chain "
    "diffusion before viscosity rises. Omer et al. placed that bond formation at the center of FDM "
    "performance [114], and Gajjar et al. measured tensile properties together with interlayer bonding "
    "for PLA under key process settings [42]. A higher nozzle temperature can enlarge the welding "
    "window, but it can also increase sag, stringing, or thermal degradation, so the abstracts that "
    "treat temperature as a factor are not reporting a universal “hotter is stronger” rule."
)
para(
    "Warpage and residual stress are the geometric side of the same thermal history. Differential "
    "shrinkage between a hot road and a cooler substrate bends the part and leaves stress that later "
    "tests interpret as a material property. Studies in this corpus that name warpage, residual stress, "
    "or shrinkage are therefore process studies even when the response is a shape error rather than a "
    "strength. Annealing and crystallinity appear when the polymer can reorganize in the solid state "
    "after the build. Those treatments change both modulus and dimensional drift, which means a "
    "parameter optimum quoted for the as-printed state need not survive a heat treatment."
)
para(
    "Cooling fan speed and chamber temperature act in the opposite direction from nozzle temperature. "
    "They shorten the time the interface stays mobile. On a small PLA part that tradeoff may be "
    "acceptable because the part must hold its shape. On a high-temperature polymer such as PEEK, or "
    "on a short-fiber composite, the abstracts more often keep the chamber warm and treat fan cooling "
    "as something to limit. The corpus includes both desktop-scale PLA studies and higher-performance "
    "feedstocks, and their temperature windows should not be averaged."
)
thermal = groups["thermal"]
para(
    "The studies assigned to this section name a thermal factor or a thermal defect in the title or "
    f"abstract ({len(thermal)} articles). They are cited below by the factor they actually name."
)
for sentence in partition_sentences(
    thermal,
    [
        (
            r"nozzle temperature|extrusion temperature|printing temperature|melt temperature",
            "Nozzle, extrusion, or printing temperature is an explicit factor in {c}.",
        ),
        (
            r"bed temperature|chamber temperature|build[- ]plate|platform temperature|envelope",
            "Bed, build-plate, or chamber temperature is named in {c}.",
        ),
        (
            r"cooling|fan speed|convective",
            "Cooling rate or fan settings are part of the experimental description in {c}.",
        ),
        (
            r"warpage|residual stress|shrink",
            "Warpage, residual stress, or shrinkage is a stated response in {c}.",
        ),
        (
            r"anneal|crystallin|heat treatment",
            "Annealing, crystallinity, or a post-build heat treatment is discussed in {c}.",
        ),
    ],
    "The remaining thermal-history studies in this group are {c}.",
):
    para(sentence)

h2("4. Layer height, infill, and toolpath geometry")
para(
    "Layer height sets both the staircase error on sloped surfaces and the number of interfaces in "
    "a given thickness. A finer layer usually improves surface description and can improve bonding "
    "if the nozzle reheats a thinner, still-warm substrate, but it also lengthens the build and "
    "changes the cooling time per layer. Infill density and infill pattern decide how much of the "
    "interior is polymer and along which directions the roads run. Birosz et al. focused on infill "
    "pattern and on the mechanical role of hollow sections [21]. Agrawal et al. did not vary pattern "
    "alone: density and layer thickness were in the same experiment on ABS [5]. Reading either paper "
    "as a license to pick an infill from a software preset, without the density and layer height that "
    "went with it, overstates what the abstracts show."
)
para(
    "Raster angle and build orientation rotate the roads relative to the load. A tensile bar printed "
    "flat with roads along the load axis is a different object from the same bar printed on edge or "
    "with a 45° raster. Sola et al. listed anisotropy among the reasons tensile results from "
    "additively manufactured polymers do not transfer cleanly between laboratories [143]. "
    "Orientation effects in this corpus should be read as toolpath effects, not as a second material."
)
para(
    "Line width, road width, and nozzle diameter change the contact width and the pressure in the "
    "bead. They are less often the headline factor than layer height or infill, but they sit in the "
    "same geometric family: they define the cross-section that temperature and speed then have to weld."
)
geometry = groups["geometry"]
para(
    f"This section cites the {len(geometry)} articles whose strongest title or abstract signal is "
    "geometric or toolpath-related."
)
for sentence in partition_sentences(
    geometry,
    [
        (
            r"layer height|layer thickness",
            "Layer height or layer thickness is a named factor in {c}.",
        ),
        (
            r"infill",
            "Infill pattern, infill density, or both are named in {c}.",
        ),
        (
            r"raster|build orientation|printing orientation|raster angle|build angle",
            "Raster angle or build orientation is named in {c}.",
        ),
        (
            r"line width|road width|nozzle diameter|air gap|bead",
            "Line width, road width, nozzle diameter, air gap, or bead geometry is named in {c}.",
        ),
    ],
    "Further geometry and toolpath studies in this group are {c}.",
):
    para(sentence)

h2("5. Print speed and extrusion flow")
para(
    "Print speed sets the time a road spends under the nozzle and the time the previous layer has "
    "to cool before it is covered. Flow rate, or an extrusion multiplier, sets whether the bead "
    "matches the commanded cross-section. Too little flow leaves gaps that later appear as porosity "
    "and weak bonds. Too much flow creates ridges, dimensional growth, and local overheating. Speed "
    "and flow are often changed together in practice because a faster travel at constant flow "
    "under-fills the road, yet many abstracts name only one of them. Where both are missing, a "
    "strength change attributed to speed alone is difficult to interpret."
)
para(
    "Speed also couples to the thermal section. A slow perimeter on a hot bed can overheat a small "
    "PLA feature. A fast infill on a large PEEK part can drop the interface temperature below the "
    "welding range. The abstracts support that coupling as a reason to report nozzle temperature, "
    "bed temperature, and speed in the same methods paragraph. They do not support a single speed "
    "that is optimal for roughness and for interlayer strength at once."
)
kinematics = groups["kinematics"] + groups["quality"]
# Quality studies that are mainly about roughness/accuracy are cited in section 6.
# Keep section 5 to kinematics only.
kinematics = groups["kinematics"]
para(
    f"The {len(kinematics)} articles placed in this section name speed or flow as a leading factor."
)
if kinematics:
    for sentence in partition_sentences(
        kinematics,
        [
            (
                r"print(?:ing)? speed|deposition speed|feed rate",
                "Print speed or feed rate is a named factor in {c}.",
            ),
            (
                r"flow rate|extrusion rate|extrusion multiplier|flow multiplier",
                "Extrusion flow or a flow multiplier is named in {c}.",
            ),
        ],
        "Further speed and flow studies in this group are {c}.",
    ):
        para(sentence)
else:
    para(
        "No article had speed or flow as its highest-scoring theme after title weighting. "
        "Speed and flow still appear inside other sections wherever those words occur in a title "
        "or abstract that was assigned elsewhere."
    )

h2("6. Mechanical response, anisotropy, and interlayer failure")
para(
    "Most of the corpus justifies a parameter change by a mechanical test. Tensile strength and "
    "modulus dominate, followed by flexural and compressive tests, with impact and fracture less "
    "common but present. Marșavina et al. connected manufacturing parameters to tensile and fracture "
    "properties of FDM PLA [98]. Alarifi et al. reported mechanical tests and a numerical model for "
    "PETG/carbon unit structures [8]. Khan et al. optimized mechanical properties of a thick "
    "PLA–PETG–ABS composite, so the measured strength includes polymer–polymer interfaces as well "
    "as road interfaces [73]. These are different mechanical objects. A ranking of layer height "
    "taken from a monolithic PLA tensile bar does not automatically rank layer height for a "
    "tri-material flexural specimen."
)
para(
    "Anisotropy is the mechanical expression of toolpath. Roads parallel to the load carry stress "
    "in the filament; roads perpendicular to the load force the weld to carry it. Sola et al. argued "
    "that tensile testing practice for additively manufactured polymers is not yet settled, which "
    "limits how far a reported strength can be used as a design allowable [143]. Interlayer bonding "
    "reviews make the same point from the materials side [114, 42]. Where an abstract reports only "
    "a single build orientation, the number is a process result for that orientation, not a material "
    "datasheet value."
)
para(
    "Fiber and particle reinforcements change the interpretation again. Li et al. reviewed hybrid "
    "fiber composites printed by FDM and described gains in one property accompanied by losses in "
    "another [89]. Short fibers also alter viscosity, so the nozzle temperature and speed that weld "
    "neat PLA are not the settings that avoid nozzle clogging or fiber misalignment in a filled "
    "filament. Mechanical comparisons across neat and filled grades need the parameter set to be "
    "reported, not only the fiber weight fraction."
)
mechanical = groups["mechanical"]
para(
    f"This section cites the {len(mechanical)} articles assigned here on the basis of a mechanical "
    "or bonding term in the title or abstract."
)
for sentence in partition_sentences(
    mechanical,
    [
        (
            r"tensile",
            "Tensile response is a stated outcome in {c}.",
        ),
        (
            r"flexural|bending",
            "Flexural or bending response is a stated outcome in {c}.",
        ),
        (
            r"compressive|compression",
            "Compressive response is a stated outcome in {c}.",
        ),
        (
            r"impact|fracture|toughness",
            "Impact, fracture, or toughness is named in {c}.",
        ),
        (
            r"interlayer|bonding|adhesion|anisotropic",
            "Interlayer bonding, adhesion, or anisotropy is named in {c}.",
        ),
    ],
    "Further mechanical studies in this group are {c}.",
):
    para(sentence)

h2("7. Surface roughness, dimensional accuracy, and post-processing")
para(
    "Surface roughness in FFF is largely a geometric consequence of layer height, road width, and "
    "the stair-step on curves, modified by temperature and speed when the bead slumps or tears. "
    "Dimensional accuracy adds shrinkage, over-extrusion, and positioning error. A parameter set "
    "that maximizes tensile strength can thicken the outer wall or round a corner, so roughness and "
    "strength optima diverge. Agrawal et al. included layer thickness among the factors for ABS "
    "mechanical properties; the same factor is the first-order control on staircase roughness [5]."
)
para(
    "Mathew et al. reviewed vapour polishing and the changes it produces in surface finish and in "
    "mechanical properties [101]. That review is a warning against treating as-printed roughness as "
    "the final specification. If a study optimizes print settings for roughness and a later study "
    "polishes the same geometry, the two roughness numbers are not comparable. Dimensional studies "
    "have a related issue: accuracy after removal from the bed can shift again if the part is "
    "annealed. Thermal and geometric sections of this review should be read with that sequence in mind."
)
quality = groups["quality"]
para(
    f"The {len(quality)} articles assigned to this section emphasize roughness, accuracy, or a "
    "finishing step in the title or abstract."
)
if quality:
    for sentence in partition_sentences(
        quality,
        [
            (
                r"roughness|surface finish|surface quality",
                "Surface roughness or surface finish is a named response in {c}.",
            ),
            (
                r"dimensional accuracy|tolerance|circularity|dimensional error",
                "Dimensional accuracy, tolerance, or circularity is a named response in {c}.",
            ),
            (
                r"vapou?r|polish|post-process|finishing",
                "Polishing or another post-process is part of the study in {c}.",
            ),
        ],
        "Further surface and accuracy studies in this group are {c}.",
    ):
        para(sentence)

h2("8. Materials, optimization, and predictive models")
para(
    "Feedstock choice changes every parameter window. PLA, ABS, PETG, polyamide, and PEEK do not "
    "share a nozzle temperature, a bed temperature, or a useful print speed. Short carbon fiber, "
    "glass fiber, mineral fillers, and recycled content change viscosity and shrinkage again. "
    "Mallikarjuna et al. organized a review of FDM explicitly around materials and process parameters "
    "[93]. Li et al. narrowed the materials question to hybrid fibers and to the mechanical tradeoffs "
    "that follow [89]. Studies of filled or recycled filament in the present corpus are parameter "
    "studies only to the extent that they vary or at least report the print settings. A new filament "
    "formulation printed at one undocumented condition does not identify which setting caused a "
    "strength change."
)
para(
    "Optimization papers try to search the coupled space rather than narrate one factor. The usual "
    "tools in the titles are Taguchi arrays, analysis of variance, response-surface models, grey "
    "relational analysis, and, more recently, machine-learning surrogates. Panico et al. combined "
    "a designed experiment with machine learning for a multi-objective FDM parameter set [118]. "
    "Khan et al. used a parametric optimization framing for the tri-material FFF laminate [73]. "
    "These methods can rank factors inside the tested box. They cannot invent a setting outside the "
    "levels that were printed, and they inherit any weakness in the mechanical test, which returns "
    "the argument to Sola et al. [143]. A model trained on one printer, one brand of PLA, and one "
    "tensile-bar orientation is a local surrogate."
)
para(
    "Numerical models of the bead, the weld, and the residual-stress field are the other predictive "
    "route. Alarifi et al. combined simulation with tests for a PETG/carbon structure [8]. A model "
    "that takes nozzle temperature, speed, and convection as inputs is useful when it is checked "
    "against parts printed at those inputs. It is not a substitute for the missing experimental "
    "levels. Energy consumption appears in a smaller set of abstracts as a response beside strength "
    "or roughness. Where energy is included, the “best” parameter set depends on whether the "
    "objective is a mechanical property, a geometric tolerance, or the electricity used to get both."
)
materials = groups["materials"]
optimization = groups["optimization"]
general = groups["general"]
para(
    f"Materials-led articles in this assignment number {len(materials)}. Optimization, designed "
    f"experiments, and data-driven models number {len(optimization)}. Articles that did not score "
    f"higher on a narrower theme number {len(general)} and are cited with them so that the reference "
    "list and the text stay in one-to-one contact."
)
if materials:
    para("Materials-focused studies in this group are as follows.")
    for sentence in partition_sentences(
        materials,
        [
            (
                r"\bpla\b|polylactic|polylactide",
                "PLA or a PLA-based compound is the feedstock in {c}.",
            ),
            (
                r"\babs\b|petg|polyamide|\bpa12\b|\bpa6\b|\bpeek\b|\bpei\b",
                "ABS, PETG, polyamide, PEEK, or PEI is the feedstock in {c}.",
            ),
            (
                r"fiber|fibre|composite|carbon|glass|recycled|nanocomposite",
                "A composite, fiber-filled, or recycled feedstock is named in {c}.",
            ),
        ],
        "Further materials studies in this group are {c}.",
    ):
        para(sentence)
if optimization:
    para("Optimization and modeling studies in this group are as follows.")
    for sentence in partition_sentences(
        optimization,
        [
            (
                r"taguchi",
                "A Taguchi array or a closely related orthogonal design is named in {c}.",
            ),
            (
                r"anova|response surface|regression",
                "ANOVA, a response surface, or regression is named in {c}.",
            ),
            (
                r"machine learning|neural|bayesian|random forest|surrogate",
                "A machine-learning or Bayesian model is named in {c}.",
            ),
            (
                r"grey relational|multi-?objective|nsga|pareto",
                "A multi-objective or grey-relational treatment is named in {c}.",
            ),
            (
                r"simulat|finite element|numerical model",
                "A numerical or finite-element model is named in {c}.",
            ),
        ],
        "Further optimization and modeling studies in this group are {c}.",
    ):
        para(sentence)
if general:
    para(
        "The remaining articles meet the inclusion rules and are cited here: "
        f"{cite(p['ref_id'] for p in general)}."
    )

h2("9. What the corpus supports, and what it does not")
para(
    "Four boundaries follow from the abstracts without requiring a pooled effect size. First, "
    "parameters interact. Panico et al. used that interaction as the reason a multi-objective search "
    "is needed [118]. Agrawal et al. varied infill pattern, density, and layer thickness in one "
    "design rather than in three disconnected trials [5]. A review that ranks “the most important "
    "parameter” across polymers and machines would be inventing a consensus the abstracts do not state."
)
para(
    "Second, the response definition changes the optimum. Strength, fracture, roughness, dimensional "
    "error, warpage, and energy are different objectives. Birosz et al. looked at infill and "
    "mechanical properties of hollow sections [21]. Mathew et al. looked at surface finish after "
    "vapour polishing, which also moves mechanical properties [101]. A setting chosen for an "
    "as-printed tensile bar can be the wrong setting for a polished, load-bearing surface."
)
para(
    "Third, the test method is part of the result. Sola et al. documented open challenges in tensile "
    "testing of additively manufactured polymers [143]. Orientation, specimen geometry, and the "
    "difference between road-direction and weld-direction failure mean that two “tensile strength” "
    "columns are comparable only when those conditions match. Interlayer reviews make the same demand "
    "of bonding data [114, 42]."
)
para(
    "Fourth, feedstock and machine bound the transfer. Hybrid-fiber systems do not move all "
    "properties in the same direction [89]. Tri-material stacks add interfaces that neat PLA does "
    "not have [73]. High-temperature polymers and short-fiber grades need different thermal boundary "
    "conditions from desktop PLA. Numerical models are informative when they are tied to the printed "
    "conditions, as in the PETG/carbon simulations of Alarifi et al. [8], and they remain local "
    "models."
)
para(
    "The sample itself has boundaries. It is open access, English, and limited to four publisher "
    "groups in 2022–2026. Important subscription articles in the same journals, and work in other "
    "venues, are outside the set on purpose. Indexing for 2026 is only as complete as OpenAlex and "
    "Crossref were at retrieval. Abstracts omit many factor levels, so this review does not publish "
    "a recommended temperature or layer height. It maps which factors the open literature varies "
    "and which responses it attaches to them."
)

h2("10. Conclusion")
para(
    "Process parameters in fused filament fabrication control a thermal and geometric process, not "
    "a list of independent printer settings. Nozzle and bed temperature, cooling, layer height, "
    "infill, raster orientation, print speed, and flow jointly determine road shape, interface "
    "welding, shrinkage, and the anisotropy of the finished part. In the 175 open-access articles "
    "reviewed here, those factors are studied most often through tensile or flexural tests, with "
    "roughness, accuracy, warpage, and energy as additional responses. Taguchi designs, ANOVA, "
    "response surfaces, and machine-learning surrogates are used to search interactions inside a "
    "tested window."
)
para(
    "The evidence supports material-specific, response-specific parameter studies with the build "
    "orientation and the thermal boundary conditions reported. It does not support a universal "
    "optimum, a single ranking of factors, or the use of an as-printed tensile strength as a "
    "design allowable when the test method or a later polishing step differs. Fuller use of this "
    "corpus would require full-text extraction of factor levels and a pre-registered way to judge "
    "which tensile results are comparable."
)

h2("References")

missing = set(range(1, 176)) - CITED
if missing:
    raise SystemExit(f"Uncited papers: {sorted(missing)}")
extra = CITED - set(range(1, 176))
if extra:
    raise SystemExit(f"Unknown citations: {sorted(extra)}")


def format_person(name):
    name = unescape(name).replace(".", " ")
    parts = [p for p in name.split() if p]
    if not parts:
        return ""
    particles = {"de", "da", "del", "della", "di", "van", "von", "der", "den", "la", "le"}
    last_bits = [parts[-1]]
    given = parts[:-1]
    while given and given[-1].lower() in particles:
        last_bits.insert(0, given.pop())
    initials = []
    for g in given:
        if len(g) == 1:
            initials.append(g.upper() + ".")
        else:
            initials.append(g[0].upper() + ".")
    last = " ".join(last_bits)
    return (" ".join(initials) + " " + last).strip()


def reference_line(p):
    authors = [format_person(a) for a in p["authors"] if format_person(a)]
    if not authors:
        author_str = "Unknown"
    elif len(authors) == 1:
        author_str = authors[0]
    elif len(authors) == 2:
        author_str = f"{authors[0]} and {authors[1]}"
    elif len(authors) <= 6:
        author_str = ", ".join(authors[:-1]) + ", and " + authors[-1]
    else:
        author_str = ", ".join(authors[:6]) + ", et al."
    title = unescape(p["title"]).rstrip(".")
    journal = unescape(p["journal"])
    bits = [f"vol. {p['volume']}" ] if p.get("volume") else []
    if p.get("issue"):
        bits.append(f"no. {p['issue']}")
    if p.get("first_page"):
        pages = str(p["first_page"])
        if p.get("last_page") and str(p["last_page"]) != str(p["first_page"]):
            pages = f"{p['first_page']}–{p['last_page']}"
        bits.append(f"pp. {pages}")
    loc = ", ".join(bits)
    tail = f"{journal}"
    if loc:
        tail += f", {loc}"
    tail += f", {p['year']}."
    doi = p["doi"]
    return author_str, title, tail, doi


references = []
for i in range(1, 176):
    author_str, title, tail, doi = reference_line(by_id[i])
    references.append(
        {
            "id": i,
            "authors": author_str,
            "title": title,
            "tail": tail,
            "doi": doi,
            "year": by_id[i]["year"],
            "publisher_group": by_id[i]["publisher_group"],
            "theme": by_id[i]["theme"],
            "journal": unescape(by_id[i]["journal"]),
        }
    )


def render_markdown():
    lines = []
    for block in blocks:
        if block[0] == "h1":
            lines.append(f"# {block[1]}")
            lines.append("")
        elif block[0] == "h2":
            lines.append(f"## {block[1]}")
            lines.append("")
        elif block[0] == "p":
            lines.append(block[1])
            lines.append("")
        elif block[0] == "table":
            headers, rows = block[1], block[2]
            lines.append("| " + " | ".join(headers) + " |")
            lines.append("| " + " | ".join("---" for _ in headers) + " |")
            for row in rows:
                lines.append("| " + " | ".join(row) + " |")
            lines.append("")
    for ref in references:
        lines.append(
            f"[{ref['id']}] {ref['authors']}, \"{ref['title']},\" {ref['tail']} "
            f"https://doi.org/{ref['doi']}"
        )
        lines.append("")
    MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def set_run_font(run, name="Times New Roman", size=12, bold=False, italic=False, color=None):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color is not None:
        run.font.color.rgb = color


def add_hyperlink(paragraph, text, url):
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)
    new_run = OxmlElement("w:r")
    r_pr = OxmlElement("w:rPr")
    r_style = OxmlElement("w:rStyle")
    r_style.set(qn("w:val"), "Hyperlink")
    r_pr.append(r_style)
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")
    r_pr.append(color)
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    r_pr.append(u)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "24")
    r_pr.append(sz)
    rfonts = OxmlElement("w:rFonts")
    rfonts.set(qn("w:ascii"), "Times New Roman")
    rfonts.set(qn("w:hAnsi"), "Times New Roman")
    r_pr.append(rfonts)
    new_run.append(r_pr)
    text_elem = OxmlElement("w:t")
    text_elem.text = text
    new_run.append(text_elem)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


def shade_cell(cell, hex_color):
    tc = cell._tePr if hasattr(cell, "_tePr") else cell._tc
    tc_pr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), hex_color)
    shd.set(qn("w:val"), "clear")
    tc_pr.append(shd)


def add_page_number(paragraph):
    run1 = paragraph.add_run("Page ")
    set_run_font(run1, size=10)
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run = paragraph.add_run()
    set_run_font(run, size=10)
    run._r.append(fld_begin)
    run2 = paragraph.add_run()
    set_run_font(run2, size=10)
    run2._r.append(instr)
    run3 = paragraph.add_run()
    set_run_font(run3, size=10)
    run3._r.append(fld_end)


def render_docx():
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    footer = section.footer
    footer_p = footer.paragraphs[0]
    footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = footer_p.add_run("FFF process parameters, open-access review, 2022–2026  ·  ")
    set_run_font(run, size=10, color=RGBColor(0x44, 0x44, 0x44))
    add_page_number(footer_p)

    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    style._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")

    def format_paragraph(p, size=12, bold=False, center=False, space_after=8, space_before=0, first_line=0.3):
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        p.paragraph_format.line_spacing = 1.15
        if center:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Inches(0)
        elif first_line:
            p.paragraph_format.first_line_indent = Inches(first_line)
        else:
            p.paragraph_format.first_line_indent = Inches(0)
        for run in p.runs:
            set_run_font(run, size=size, bold=bold)

    for block in blocks:
        kind = block[0]
        if kind == "h1":
            p = doc.add_paragraph()
            r = p.add_run(block[1])
            set_run_font(r, size=16, bold=True)
            format_paragraph(p, size=16, bold=True, center=True, space_after=10, first_line=0)
        elif kind == "h2":
            p = doc.add_paragraph()
            r = p.add_run(block[1])
            set_run_font(r, size=13, bold=True, color=RGBColor(0x1F, 0x3A, 0x5F))
            format_paragraph(p, size=13, bold=True, space_before=12, space_after=6, first_line=0)
        elif kind == "p":
            text = block[1]
            p = doc.add_paragraph()
            # Keep citation brackets with the sentence; no special parsing required.
            r = p.add_run(text)
            set_run_font(r, size=12)
            center = text in {"Selva", "22 November 2026"} or text.startswith("Keywords:")
            format_paragraph(p, center=center or text in {"Selva", "22 November 2026"}, first_line=0 if center or text.startswith("Keywords:") else 0.3)
        elif kind == "table":
            headers, rows = block[1], block[2]
            tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
            tbl.style = "Table Grid"
            for j, h in enumerate(headers):
                cell = tbl.rows[0].cells[j]
                cell.text = ""
                run = cell.paragraphs[0].add_run(h)
                set_run_font(run, size=11, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
                shade_cell(cell, "1F3A5F")
            for i, row in enumerate(rows):
                for j, val in enumerate(row):
                    cell = tbl.rows[i + 1].cells[j]
                    cell.text = ""
                    run = cell.paragraphs[0].add_run(val)
                    set_run_font(run, size=11, bold=(i == len(rows) - 1))
                    if i % 2 == 1:
                        shade_cell(cell, "F4F7FB")
            doc.add_paragraph()

    for ref in references:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.35)
        p.paragraph_format.first_line_indent = Inches(-0.35)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.08
        lead = p.add_run(f"[{ref['id']}] {ref['authors']}, “{ref['title']},” {ref['tail']} ")
        set_run_font(lead, size=11)
        add_hyperlink(p, f"https://doi.org/{ref['doi']}", f"https://doi.org/{ref['doi']}")

    core = doc.core_properties
    core.author = "Selva"
    core.title = "Influence of Process Parameters in Fused Filament Fabrication: A Review of Open-Access Studies, 2022–2026"
    core.subject = "Review of 175 open-access FFF/FDM process-parameter papers, 2022–2026"
    core.category = "Literature review"
    doc.save(DOCX_PATH)
    ARTIFACT.write_bytes(DOCX_PATH.read_bytes())


def write_metadata():
    public = []
    for p in papers:
        public.append(
            {
                "ref_id": p["ref_id"],
                "doi": p["doi"],
                "title": unescape(p["title"]),
                "year": p["year"],
                "authors": p["authors"],
                "journal": unescape(p["journal"]),
                "publisher_group": p["publisher_group"],
                "oa_status": p["oa_status"],
                "cited_by_count": p["cited_by_count"],
                "title_similarity": p["title_similarity"],
                "theme": p["theme"],
                "volume": p.get("volume") or "",
                "issue": p.get("issue") or "",
                "first_page": p.get("first_page") or "",
                "last_page": p.get("last_page") or "",
            }
        )
    META_PATH.write_text(json.dumps(public, indent=2), encoding="utf-8")
    summary = {
        "n": 175,
        "publishers": dict(pub_counts),
        "years": {str(k): v for k, v in sorted(year_counts.items())},
        "oa": dict(oa_counts),
        "themes": {k: len(v) for k, v in groups.items()},
        "cited": len(CITED),
        "min_title_similarity": min(p["title_similarity"] for p in papers),
    }
    (ROOT / "corpus_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


render_markdown()
render_docx()
write_metadata()
text = MD_PATH.read_text(encoding="utf-8")
words = len(re.findall(r"[A-Za-z0-9’'-]+", text.split("## References")[0]))
print("words_before_references", words)
print("docx", DOCX_PATH, DOCX_PATH.stat().st_size)
print("artifact", ARTIFACT, ARTIFACT.stat().st_size)
