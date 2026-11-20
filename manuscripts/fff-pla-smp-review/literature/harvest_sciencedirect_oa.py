#!/usr/bin/env python3
"""Harvest 2022-2026 open-access Elsevier / ScienceDirect works on FFF PLA shape-memory composites.

ScienceDirect HTML search returns an institutional-login wall from this environment.
Records are therefore taken from OpenAlex works whose primary source is published by
Elsevier BV, restricted to open-access article and review records, then checked so
the DOI is an Elsevier 10.1016 journal article (the ScienceDirect journal corpus).
"""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

MAILTO = "selva.research@example.com"
OUT = Path(__file__).resolve().parent / "candidates.json"
ELSEVIER = "https://openalex.org/P4310320990"

QUERIES = [
    '"4D printing" (PLA OR polylactic OR polylactide)',
    '"shape memory" (PLA OR polylactic OR polylactide) (printing OR filament OR FDM OR FFF)',
    '"shape recovery" (PLA OR polylactic) (printed OR printing OR filament)',
    '"shape fixity" (PLA OR polylactic OR polylactide)',
    '"carbon fiber" OR "carbon fibre" (PLA OR polylactic) ("shape memory" OR "4D")',
    '"continuous fiber" OR "continuous fibre" OR "continuous carbon" PLA (shape OR 4D OR printing)',
    '(flax OR hemp OR jute OR "wood flour" OR "natural fiber" OR "natural fibre") PLA ("shape memory" OR "4D printing")',
    '(TPU OR "thermoplastic polyurethane") PLA ("shape memory" OR "4D printing")',
    '"fused deposition" OR "fused filament" OR "material extrusion" PLA ("shape memory" OR "4D")',
    '"raster angle" OR "infill density" OR "layer thickness" PLA ("shape memory" OR recovery OR "4D")',
    '(CNT OR graphene OR nanotube) PLA ("shape memory" OR "4D printing")',
    '"glass fiber" OR "glass fibre" OR basalt PLA ("shape memory" OR "4D") printing',
    'review ("4D printing" OR "shape memory polymer") (PLA OR polylactic OR "additive manufacturing")',
    '"recovery stress" OR "recovery force" PLA (print OR printed OR filament)',
    '"programming temperature" PLA ("shape memory" OR "shape recovery")',
    '"short carbon" PLA (FDM OR "fused deposition" OR filament) (anisotropy OR raster OR orientation)',
    '"polylactic acid" composite "shape memory" (extrusion OR filament OR printed)',
    '"shape memory polymer" "polylactic" (fiber OR fibre OR composite) printing',
    '"4D printing" "carbon fiber" OR "carbon fibre" polymer composite',
    '"fused filament fabrication" (PLA OR polylactic) (fiber OR fibre) (crystallinity OR anisotropy OR interface)',
]

PLA_TERMS = (
    "pla",
    "polylactic",
    "polylactide",
    "poly(lactic",
    "poly(lactide",
    "poly-lactic",
    "poly lactic",
)
SME_TERMS = (
    "shape memory",
    "shape-memory",
    "4d print",
    "4d-print",
    "shape recovery",
    "shape fixity",
    "shape-recovery",
    "shape-fixity",
    "recovery ratio",
    "fixity ratio",
    "stimuli-responsive",
    "stimulus-responsive",
    "morphing",
)
FIBER_TERMS = (
    "fiber",
    "fibre",
    "carbon",
    "flax",
    "hemp",
    "jute",
    "glass",
    "basalt",
    "wood",
    "cellulose",
    "cnt",
    "nanotube",
    "graphene",
    "composite",
    "reinforc",
)
PROCESS_TERMS = (
    "fused deposition",
    "fused filament",
    "fff",
    "fdm",
    "material extrusion",
    "raster",
    "infill",
    "layer thickness",
    "layer height",
    "print speed",
    "nozzle",
    "build orientation",
    "toolpath",
    "extrusion",
    "3d print",
    "additive manufactur",
    "filament",
)
NEG_TERMS = (
    "lithium-ion",
    "perovskite",
    "photocatal",
    "wastewater",
    "asphalt",
    "concrete",
    "supercapacitor",
    "solar cell",
    "covid",
    "vaccine",
    "battery electrode",
)


def get_json(url: str, retries: int = 6) -> dict:
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": f"research-writing/1.0 (mailto:{MAILTO})"},
            )
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as exc:  # noqa: BLE001
            last = exc
            code = getattr(exc, "code", None)
            wait = 8 * (i + 1) if code in {401, 403, 429} else 1.5 * (i + 1)
            print(f"  retry {i+1} code={code} wait={wait}s", flush=True)
            time.sleep(wait)
    raise RuntimeError(f"failed {url[:180]}: {last}")


def reconstruct_abstract(inv: dict | None) -> str:
    if not inv:
        return ""
    pairs = []
    for word, positions in inv.items():
        for pos in positions:
            pairs.append((pos, word))
    pairs.sort()
    return " ".join(word for _, word in pairs)


def has_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def score_record(title: str, abstract: str) -> tuple[int, list[str]]:
    blob = f"{title} {abstract}".lower()
    title_l = title.lower()
    tags = []
    score = 0
    if has_any(blob, NEG_TERMS) and not has_any(blob, SME_TERMS):
        return -100, ["excluded"]
    if not has_any(blob, PLA_TERMS):
        # Allow continuous-fiber SMP papers that discuss PLA as a comparator only if PLA is present.
        return -50, ["no_pla"]
    score += 4 if has_any(title_l, PLA_TERMS) else 2
    tags.append("pla")
    if has_any(blob, SME_TERMS):
        score += 6 if has_any(title_l, SME_TERMS) else 3
        tags.append("sme")
    if has_any(blob, FIBER_TERMS):
        score += 3 if has_any(title_l, FIBER_TERMS) else 1
        tags.append("fiber")
    if has_any(blob, PROCESS_TERMS):
        score += 3 if has_any(title_l, PROCESS_TERMS) else 1
        tags.append("process")
    if "review" in title_l:
        score += 1
        tags.append("review")
    # Core corpus: PLA and a shape-memory/4D signal.
    if "sme" not in tags:
        return score - 20, tags + ["off_scope"]
    return score, tags


def slim_authorships(authorships: list[dict]) -> list[dict]:
    out = []
    for a in authorships or []:
        author = a.get("author") or {}
        name = author.get("display_name") or ""
        if name:
            out.append({"name": name, "position": a.get("author_position")})
    return out


def harvest() -> list[dict]:
    seen: dict[str, dict] = {}
    select = ",".join(
        [
            "id",
            "doi",
            "display_name",
            "publication_year",
            "type",
            "authorships",
            "primary_location",
            "best_oa_location",
            "open_access",
            "abstract_inverted_index",
            "biblio",
            "cited_by_count",
            "is_retracted",
        ]
    )
    for qi, query in enumerate(QUERIES, 1):
        cursor = "*"
        pages = 0
        added = 0
        while cursor and pages < 3:
            params = {
                "search": query,
                "filter": f"publication_year:2022-2026,is_oa:true,primary_location.source.host_organization:{ELSEVIER}",
                "per-page": "50",
                "cursor": cursor,
                "select": select,
                "mailto": MAILTO,
            }
            url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
            try:
                data = get_json(url)
            except Exception as exc:  # noqa: BLE001
                print(f"  skip page after error: {exc}", flush=True)
                break
            results = data.get("results") or []
            pages += 1
            for w in results:
                if w.get("is_retracted"):
                    continue
                if w.get("type") not in {"article", "review"}:
                    continue
                doi = (w.get("doi") or "").replace("https://doi.org/", "").strip().lower()
                if not doi.startswith("10.1016/"):
                    continue
                oa = w.get("open_access") or {}
                if not oa.get("is_oa"):
                    continue
                if oa.get("oa_status") not in {"gold", "hybrid", "bronze", "diamond", "green"}:
                    continue
                best = w.get("best_oa_location") or {}
                oa_url = oa.get("oa_url") or best.get("pdf_url") or best.get("landing_page_url") or ""
                if oa_url.lower().endswith((".jpg", ".png", ".gif", ".jpeg")):
                    # Image-only "oa" records are not readable papers.
                    if not best.get("pdf_url"):
                        continue
                title = (w.get("display_name") or "").strip()
                abstract = reconstruct_abstract(w.get("abstract_inverted_index"))
                sc, tags = score_record(title, abstract)
                if sc < 8:
                    continue
                loc = w.get("primary_location") or {}
                source = loc.get("source") or {}
                biblio = w.get("biblio") or {}
                rec = {
                    "doi": doi,
                    "title": title,
                    "year": w.get("publication_year"),
                    "type": w.get("type"),
                    "journal": source.get("display_name") or "",
                    "issn_l": source.get("issn_l") or "",
                    "authors": slim_authorships(w.get("authorships") or []),
                    "volume": biblio.get("volume") or "",
                    "issue": biblio.get("issue") or "",
                    "first_page": biblio.get("first_page") or "",
                    "last_page": biblio.get("last_page") or "",
                    "cited_by_count": w.get("cited_by_count") or 0,
                    "oa_status": oa.get("oa_status"),
                    "oa_url": oa_url,
                    "landing_page_url": loc.get("landing_page_url") or "",
                    "abstract": abstract,
                    "score": sc,
                    "tags": tags,
                    "openalex_id": w.get("id"),
                }
                prev = seen.get(doi)
                if prev is None or rec["score"] > prev["score"]:
                    seen[doi] = rec
                    added += 1
            cursor = (data.get("meta") or {}).get("next_cursor")
            if not results:
                break
            time.sleep(0.15)
        print(f"[{qi}/{len(QUERIES)}] unique={len(seen)} added_or_updated={added} query={query[:70]}", flush=True)
        # Checkpoint so a later API failure does not discard earlier queries.
        OUT.write_text(json.dumps(list(seen.values()), indent=2, ensure_ascii=False))
    ranked = sorted(seen.values(), key=lambda r: (r["score"], r["cited_by_count"]), reverse=True)
    return ranked


def main() -> None:
    ranked = harvest()
    OUT.write_text(json.dumps(ranked, indent=2, ensure_ascii=False))
    print(f"saved {len(ranked)} candidates -> {OUT}")
    from collections import Counter

    years = Counter(r["year"] for r in ranked)
    tags = Counter(t for r in ranked for t in r["tags"])
    print("years", dict(years))
    print("tags", dict(tags))
    print("top 15:")
    for r in ranked[:15]:
        print(f"  {r['score']:2d} {r['year']} {r['doi']} {r['title'][:110]}")


if __name__ == "__main__":
    main()
