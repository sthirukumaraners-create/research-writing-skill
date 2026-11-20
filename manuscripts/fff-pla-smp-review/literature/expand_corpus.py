#!/usr/bin/env python3
"""Deepen the Elsevier OA search and drop title false positives."""

from __future__ import annotations

import html
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

MAILTO = "selva.research@example.com"
UNPAYWALL_EMAIL = "research-writing@example.com"
ROOT = Path(__file__).resolve().parent
TODAY = (2026, 11, 20)

PLA_RE = re.compile(r"(\bpla\b|polylactic|polylactide|poly[\s-]*lactic)", re.I)
SME_RE = re.compile(r"(shape[- ]memory|4d[- ]print|shape recovery|shape fixity|shape[- ]recovery|shape[- ]fixity)", re.I)
FIBER_RE = re.compile(
    r"(carbon fib|flax|hemp|jute|kenaf|sisal|glass fib|continuous fib|short fib|natural fib|"
    r"cellulose|wood fib|wood/pla|bamboo|silk fib|nanotube|\bcnt\b|graphene|basalt|harakeke|"
    r"regenerated cellulose|fibre|fiber)",
    re.I,
)
PROC_RE = re.compile(
    r"(fused deposition|fused filament|\bfff\b|\bfdm\b|3d[- ]print|4d[- ]print|"
    r"material extrusion|additive manufactur|filament)",
    re.I,
)

QUERIES = [
    '"4D printing" PLA',
    '"4D printed" PLA',
    '"4D-printed" PLA',
    '"shape memory" "polylactic acid"',
    '"shape memory" "poly lactic"',
    '"shape-memory" PLA',
    '"shape memory polymer" PLA',
    '"shape recovery" polylactic',
    '"shape fixity" PLA',
    '"carbon fiber" PLA "shape memory"',
    '"carbon fibre" PLA "shape memory"',
    'flax PLA "4D"',
    '"continuous" PLA "shape memory" printing',
    'TPU PLA "shape memory"',
    'PBAT PLA "shape memory"',
    'PCL PLA "shape memory"',
    '"programming" PLA "shape recovery"',
    '"raster" PLA "shape memory"',
    '"infill" PLA "shape memory"',
    '"layer thickness" PLA "4D"',
    '"fused deposition" "shape memory" PLA',
    '"fused filament fabrication" "shape memory" PLA',
    '"carbon fiber" PLA "fused deposition"',
    '"continuous carbon" PLA printing',
    '"short carbon" PLA "fused"',
    'flax PLA "fused deposition"',
    '"glass fiber" PLA "fused filament"',
    'graphene PLA "shape memory"',
    'CNT PLA "shape memory" filament',
    '"wood" PLA "shape memory" printing',
]


def get_json(url: str, retries: int = 5) -> dict:
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": f"research-writing/1.0 (mailto:{MAILTO})"}
            )
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as exc:  # noqa: BLE001
            last = exc
            code = getattr(exc, "code", None)
            time.sleep(3.0 * (i + 1) if code in {429, 503} else 1.0 * (i + 1))
    raise RuntimeError(str(last))


def license_in_force(item: dict) -> str:
    for lic in item.get("license") or []:
        url = lic.get("URL") or ""
        if "creativecommons.org" not in url.lower():
            continue
        parts = ((lic.get("start") or {}).get("date-parts") or [None])[0]
        if not parts or not parts[0]:
            return url
        year, month, day = parts[0], (parts[1] if len(parts) > 1 and parts[1] else 1), (parts[2] if len(parts) > 2 and parts[2] else 1)
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
        if family or given:
            out.append({"family": family, "given": given})
    return out


def classify(title: str) -> tuple[str, int, list[str]] | None:
    if not PLA_RE.search(title):
        return None
    tags = ["pla"]
    score = 4
    if SME_RE.search(title):
        tags.append("sme")
        score += 8
        role = "sme"
    elif FIBER_RE.search(title) and PROC_RE.search(title):
        tags += ["fiber", "process"]
        score += 4
        role = "process"
    else:
        return None
    if FIBER_RE.search(title):
        tags.append("fiber")
        score += 2
    if PROC_RE.search(title):
        tags.append("process")
        score += 1
    if re.search(r"\breview\b", title, re.I):
        tags.append("review")
        score += 1
    return role, score, sorted(set(tags))


def from_crossref_item(item: dict) -> dict | None:
    title = html.unescape(((item.get("title") or [""])[0] or "").strip())
    classified = classify(title)
    if not classified:
        return None
    role, score, tags = classified
    doi = (item.get("DOI") or "").lower().strip()
    year = year_of(item)
    lic = license_in_force(item)
    if not doi.startswith("10.1016/") or year is None or not (2022 <= year <= 2026) or not lic:
        return None
    return {
        "doi": doi,
        "title": title,
        "year": year,
        "journal": html.unescape(((item.get("container-title") or [""])[0] or "").strip()),
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
        "oa_url": "",
    }


def search() -> dict[str, dict]:
    found: dict[str, dict] = {}
    for qi, query in enumerate(QUERIES, 1):
        for page in range(3):
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
                print(f"  stop {query[:40]}: {exc}", flush=True)
                break
            items = (data.get("message") or {}).get("items") or []
            added = 0
            for item in items:
                rec = from_crossref_item(item)
                if not rec:
                    continue
                prev = found.get(rec["doi"])
                if prev is None or rec["score"] > prev["score"]:
                    if prev:
                        rec["abstract"] = prev.get("abstract") or ""
                        rec["abstract_source"] = prev.get("abstract_source") or ""
                        rec["pdf_url"] = prev.get("pdf_url") or ""
                        rec["oa_url"] = prev.get("oa_url") or ""
                        rec["oa_status"] = prev.get("oa_status") or rec["oa_status"]
                    found[rec["doi"]] = rec
                    added += 1
            print(f"[{qi}/{len(QUERIES)}] off={page*100} added={added} unique={len(found)} {query[:55]}", flush=True)
            if len(items) < 100:
                break
            time.sleep(0.3)
    return found


def merge_existing(found: dict[str, dict]) -> None:
    path = ROOT / "corpus.json"
    if not path.exists():
        return
    for row in json.loads(path.read_text()):
        title = html.unescape(row.get("title") or "")
        classified = classify(title)
        if not classified:
            continue
        role, score, tags = classified
        doi = row["doi"].lower()
        row["title"] = title
        row["journal"] = html.unescape(row.get("journal") or "")
        row["role"] = role
        row["score"] = max(score, row.get("score") or 0)
        row["tags"] = tags
        prev = found.get(doi)
        if prev is None:
            found[doi] = row
        else:
            if row.get("abstract") and not prev.get("abstract"):
                prev["abstract"] = row["abstract"]
                prev["abstract_source"] = row.get("abstract_source") or ""
            if row.get("pdf_url") and not prev.get("pdf_url"):
                prev["pdf_url"] = row["pdf_url"]
            if row.get("oa_status") and prev.get("oa_status") == "cc-license":
                prev["oa_status"] = row["oa_status"]
            if row.get("oa_url"):
                prev["oa_url"] = row["oa_url"]


def attach_openalex(found: dict[str, dict]) -> None:
    path = ROOT / "candidates.json"
    if not path.exists():
        return
    n = 0
    for row in json.loads(path.read_text()):
        doi = (row.get("doi") or "").lower()
        abstract = (row.get("abstract") or "").strip()
        if doi in found and abstract and not found[doi].get("abstract"):
            found[doi]["abstract"] = abstract
            found[doi]["abstract_source"] = "openalex"
            n += 1
    print("openalex attached", n, flush=True)


def attach_doaj(found: dict[str, dict]) -> None:
    n = 0
    for doi, rec in found.items():
        if rec.get("abstract"):
            continue
        url = "https://doaj.org/api/search/articles/" + urllib.parse.quote("doi:" + doi) + "?pageSize=1"
        try:
            data = get_json(url)
        except Exception:
            continue
        results = data.get("results") or []
        if results:
            abstract = html.unescape(((results[0].get("bibjson") or {}).get("abstract") or "").strip())
            if abstract:
                rec["abstract"] = abstract
                rec["abstract_source"] = "doaj"
                n += 1
        time.sleep(0.12)
    print("doaj attached", n, flush=True)


def attach_unpaywall(found: dict[str, dict]) -> None:
    dropped = []
    for i, (doi, rec) in enumerate(list(found.items()), 1):
        if rec.get("oa_status") in {"gold", "hybrid", "bronze", "green"} and rec.get("pdf_url"):
            continue
        url = f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={UNPAYWALL_EMAIL}"
        try:
            data = get_json(url)
        except Exception as exc:  # noqa: BLE001
            print("  unpaywall miss", doi, exc, flush=True)
            continue
        if not data.get("is_oa"):
            dropped.append(doi)
            continue
        rec["oa_status"] = data.get("oa_status") or rec["oa_status"]
        best = data.get("best_oa_location") or {}
        rec["pdf_url"] = best.get("url_for_pdf") or rec.get("pdf_url") or ""
        rec["oa_url"] = best.get("url") or rec.get("oa_url") or ""
        if i % 30 == 0:
            print(f"  unpaywall {i} dropped {len(dropped)}", flush=True)
        time.sleep(0.1)
    for doi in dropped:
        found.pop(doi, None)
    print("unpaywall dropped", len(dropped), "remaining", len(found), flush=True)


def main() -> None:
    found = search()
    merge_existing(found)
    attach_openalex(found)
    attach_doaj(found)
    attach_unpaywall(found)
    ranked = sorted(
        found.values(),
        key=lambda r: (
            1 if r["role"] == "sme" else 0,
            1 if r.get("abstract") else 0,
            r.get("score") or 0,
            r.get("cited_by_count") or 0,
        ),
        reverse=True,
    )
    sme = [r for r in ranked if r["role"] == "sme"]
    process = [r for r in ranked if r["role"] == "process"]
    selected = (sme + process)[:175]
    (ROOT / "corpus.json").write_text(json.dumps(selected, indent=2, ensure_ascii=False))
    print(
        f"selected {len(selected)} sme={sum(r['role']=='sme' for r in selected)} "
        f"process={sum(r['role']=='process' for r in selected)} "
        f"abstracts={sum(bool(r.get('abstract')) for r in selected)}"
    )


if __name__ == "__main__":
    main()
