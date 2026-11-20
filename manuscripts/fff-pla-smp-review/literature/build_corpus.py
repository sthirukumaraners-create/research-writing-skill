#!/usr/bin/env python3
"""Build a verified 2022-2026 open-access Elsevier corpus for the PLA FFF SMP review.

ScienceDirect HTML search is institution-gated in this environment. Records are
taken from Crossref member 78 (Elsevier), kept only when a Creative Commons
license is already in force, then checked with Unpaywall. Abstracts are attached
from the earlier OpenAlex harvest and from DOAJ. No citation is invented here;
records without a Crossref DOI are dropped.
"""

from __future__ import annotations

import html
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

MAILTO = "selva.research@example.com"
UNPAYWALL_EMAIL = "research-writing@example.com"
ROOT = Path(__file__).resolve().parent
TODAY = (2026, 11, 20)

TITLE_QUERIES = [
    '"4D printing" PLA',
    '"4D printing" polylactic',
    '"4D printing" "polylactic acid"',
    '"shape memory" PLA printing',
    '"shape memory" "polylactic acid"',
    '"shape memory" polylactide filament',
    '"shape recovery" PLA',
    '"shape fixity" PLA',
    '"shape memory" "carbon fiber" PLA',
    '"shape memory" "carbon fibre" PLA',
    '"continuous fiber" OR "continuous fibre" "shape memory" PLA',
    '"fused deposition" "shape memory" PLA',
    '"fused filament" "shape memory" PLA',
    '"material extrusion" "shape memory" polylactic',
    'PLA TPU "4D printing"',
    'PLA PBAT "shape memory"',
    'PLA PCL "shape memory" printing',
    '"natural fiber" OR flax OR wood PLA "4D printing"',
    'CNT OR graphene PLA "shape memory" printing',
    '"raster angle" "shape memory" PLA',
    '"carbon fiber" PLA "fused deposition"',
    '"carbon fibre" PLA "fused filament fabrication"',
    '"short carbon fiber" PLA',
    'flax PLA "fused deposition"',
    '"layer thickness" PLA "shape memory"',
    '"infill" PLA "shape memory" printing',
]

PLA = ("pla", "polylactic", "polylactide", "poly(lactic", "poly-lactic", "poly lactic")
SME = (
    "shape memory",
    "shape-memory",
    "4d print",
    "4d-print",
    "shape recovery",
    "shape fixity",
    "shape-recovery",
    "shape-fixity",
)
FIBER = (
    "fiber",
    "fibre",
    "carbon",
    "flax",
    "hemp",
    "jute",
    "basalt",
    "glass",
    "wood",
    "cellulose",
    "cnt",
    "nanotube",
    "graphene",
    "composite",
    "reinforc",
)
PROCESS = (
    "fused deposition",
    "fused filament",
    "fff",
    "fdm",
    "material extrusion",
    "raster",
    "infill",
    "layer ",
    "print",
    "printed",
    "filament",
    "additive",
    "extrusion",
    "nozzle",
    "orientation",
)
# Title-only exclusions. Pharmaceutical and food papers can mention 4D printing
# without being structural SMP composites.
EXCLUDE = (
    "pharmaceut",
    "drug delivery",
    "dosage",
    "tablet",
    "food packaging",
    "tissue engineering scaffold" ,
)


def get_json(url: str, retries: int = 5) -> dict:
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
            time.sleep((3.0 * (i + 1)) if code in {429, 503} else 1.2 * (i + 1))
    raise RuntimeError(str(last))


def has_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def license_in_force(item: dict) -> str:
    for lic in item.get("license") or []:
        url = lic.get("URL") or ""
        if "creativecommons.org" not in url.lower():
            continue
        parts = ((lic.get("start") or {}).get("date-parts") or [None])[0]
        if not parts or not parts[0]:
            return url
        year = parts[0]
        month = parts[1] if len(parts) > 1 and parts[1] else 1
        day = parts[2] if len(parts) > 2 and parts[2] else 1
        if (year, month, day) <= TODAY:
            return url
    return ""


def year_of(item: dict) -> int | None:
    parts = ((item.get("issued") or {}).get("date-parts") or [None])[0]
    if parts and parts[0]:
        return int(parts[0])
    return None


def authors_of(item: dict) -> list[dict]:
    out = []
    for author in item.get("author") or []:
        family = (author.get("family") or "").strip()
        given = (author.get("given") or "").strip()
        if not family and not given:
            # Collaboration names are not used as personal authors.
            name = (author.get("name") or "").strip()
            if name:
                out.append({"family": name, "given": "", "collaboration": True})
            continue
        out.append({"family": family, "given": given, "collaboration": False})
    return out


def classify(title: str) -> tuple[int, str, list[str]]:
    t = title.lower()
    if has_any(t, EXCLUDE) and not has_any(t, ("shape memory", "shape recovery", "shape fixity")):
        return -1, "exclude", []
    if not has_any(t, PLA):
        return -1, "exclude", []
    tags = ["pla"]
    score = 4
    role = ""
    if has_any(t, SME):
        score += 8
        tags.append("sme")
        role = "sme"
    if has_any(t, FIBER):
        score += 3
        tags.append("fiber")
    if has_any(t, PROCESS):
        score += 2
        tags.append("process")
    if role != "sme":
        # Secondary process-structure papers must name both a reinforcement and a printing process.
        if "fiber" in tags and "process" in tags:
            role = "process"
            score += 1
        else:
            return -1, "exclude", tags
    if "review" in t:
        tags.append("review")
        score += 1
    return score, role, tags


def crossref_collect() -> dict[str, dict]:
    found: dict[str, dict] = {}
    for qi, query in enumerate(TITLE_QUERIES, 1):
        # Offset keeps relevance ranking. Cursor paging reorders results and
        # pulls in unrelated "4D" records.
        for page in range(2):
            params = {
                "query.title": query,
                "filter": "from-pub-date:2022-01-01,until-pub-date:2026-11-20,member:78,type:journal-article",
                "rows": "100",
                "offset": str(page * 100),
                "select": "DOI,title,author,container-title,issued,volume,issue,page,license,is-referenced-by-count,publisher",
                "mailto": MAILTO,
            }
            url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
            try:
                data = get_json(url)
            except Exception as exc:  # noqa: BLE001
                print(f"  crossref stop {query[:40]}: {exc}", flush=True)
                break
            msg = data.get("message") or {}
            items = msg.get("items") or []
            kept = 0
            for item in items:
                doi = (item.get("DOI") or "").lower().strip()
                if not doi.startswith("10.1016/"):
                    continue
                year = year_of(item)
                if year is None or year < 2022 or year > 2026:
                    continue
                lic = license_in_force(item)
                if not lic:
                    continue
                title = ((item.get("title") or [""])[0] or "").strip()
                score, role, tags = classify(title)
                if score < 0:
                    continue
                rec = {
                    "doi": doi,
                    "title": html.unescape(title),
                    "year": year,
                    "journal": ((item.get("container-title") or [""])[0] or "").strip(),
                    "volume": item.get("volume") or "",
                    "issue": item.get("issue") or "",
                    "page": item.get("page") or "",
                    "authors": authors_of(item),
                    "cited_by_count": item.get("is-referenced-by-count") or 0,
                    "license": lic,
                    "publisher": item.get("publisher") or "Elsevier",
                    "score": score,
                    "role": role,
                    "tags": tags,
                    "abstract": "",
                    "abstract_source": "",
                    "oa_status": "cc-license",
                    "pdf_url": "",
                }
                prev = found.get(doi)
                if prev is None or rec["score"] > prev["score"]:
                    if prev and prev.get("abstract"):
                        rec["abstract"] = prev["abstract"]
                        rec["abstract_source"] = prev["abstract_source"]
                    found[doi] = rec
                    kept += 1
            print(f"[{qi}/{len(TITLE_QUERIES)}] p{page+1} kept_now={kept} unique={len(found)} {query[:60]}", flush=True)
            if not items:
                break
            time.sleep(0.35)
        time.sleep(0.2)
    return found


def attach_openalex(found: dict[str, dict]) -> None:
    path = ROOT / "candidates.json"
    if not path.exists():
        return
    rows = json.loads(path.read_text())
    n = 0
    for row in rows:
        doi = (row.get("doi") or "").lower()
        abstract = (row.get("abstract") or "").strip()
        if doi in found and abstract and not found[doi]["abstract"]:
            found[doi]["abstract"] = abstract
            found[doi]["abstract_source"] = "openalex"
            n += 1
    print(f"openalex abstracts attached: {n}", flush=True)


def attach_doaj(found: dict[str, dict]) -> None:
    n = 0
    for i, doi in enumerate(list(found), 1):
        if found[doi]["abstract"]:
            continue
        url = "https://doaj.org/api/search/articles/" + urllib.parse.quote("doi:" + doi) + "?pageSize=1"
        try:
            data = get_json(url)
        except Exception:
            continue
        results = data.get("results") or []
        if not results:
            continue
        bib = results[0].get("bibjson") or {}
        abstract = html.unescape((bib.get("abstract") or "").strip())
        if abstract:
            found[doi]["abstract"] = abstract
            found[doi]["abstract_source"] = "doaj"
            n += 1
        if i % 25 == 0:
            print(f"  doaj checked {i}, abstracts {n}", flush=True)
        time.sleep(0.15)
    print(f"doaj abstracts attached: {n}", flush=True)


def attach_unpaywall(found: dict[str, dict]) -> None:
    dropped = []
    for i, doi in enumerate(list(found), 1):
        url = f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={UNPAYWALL_EMAIL}"
        try:
            data = get_json(url)
        except Exception as exc:  # noqa: BLE001
            print(f"  unpaywall miss {doi}: {exc}", flush=True)
            continue
        if not data.get("is_oa"):
            dropped.append(doi)
            continue
        found[doi]["oa_status"] = data.get("oa_status") or found[doi]["oa_status"]
        best = data.get("best_oa_location") or {}
        found[doi]["pdf_url"] = best.get("url_for_pdf") or ""
        found[doi]["oa_url"] = best.get("url") or ""
        if i % 20 == 0:
            print(f"  unpaywall {i}/{len(found)} dropped {len(dropped)}", flush=True)
        time.sleep(0.12)
    for doi in dropped:
        del found[doi]
    print(f"unpaywall dropped non-OA: {len(dropped)}; remaining {len(found)}", flush=True)


def main() -> None:
    found = crossref_collect()
    attach_openalex(found)
    attach_doaj(found)
    attach_unpaywall(found)
    # Prefer abstract-bearing SME papers, then other SME papers, then process papers.
    ranked = sorted(
        found.values(),
        key=lambda r: (
            1 if r["role"] == "sme" else 0,
            1 if r["abstract"] else 0,
            r["score"],
            r["cited_by_count"],
        ),
        reverse=True,
    )
    sme = [r for r in ranked if r["role"] == "sme"]
    process = [r for r in ranked if r["role"] == "process"]
    # Cap at 175. Fill with SME first.
    selected = sme[:175]
    if len(selected) < 175:
        room = 175 - len(selected)
        selected.extend(process[:room])
    out = ROOT / "corpus.json"
    out.write_text(json.dumps(selected, indent=2, ensure_ascii=False))
    with_abs = sum(1 for r in selected if r["abstract"])
    print(
        f"selected {len(selected)} (sme={sum(1 for r in selected if r['role']=='sme')} "
        f"process={sum(1 for r in selected if r['role']=='process')} abstracts={with_abs}) -> {out}"
    )


if __name__ == "__main__":
    main()
