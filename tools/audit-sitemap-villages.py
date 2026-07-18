#!/usr/bin/env python3
"""
Audit qualité sitemap-villages.xml — préparation curation 2026-07-18 canalizador-urgente.pt.

Adapté de tools/audit-sitemap-villages.py (eletricista-urgente.pt) pour canalizador-urgente.pt.

Catégories:
  - V_STD     : /canalizador-<slug>            (village money page long-tail)
  - V_URGENTE : /canalizador-urgente-<slug>    (village variante préfixée "urgente")
  - INSTITUC  : /<page-racine>                 (éditoriales/institutionnelles)
  - BLOG      : /blog/<slug>                   (articles MD convertis HTML)
  - POLLUTION : URLs hors-pattern manifestes

Doctrine : PT-PT, aucun prix inventé, lecture seule.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

V_STD_RE = re.compile(
    r"^https://canalizador-urgente\.pt/canalizador-[a-z0-9à-ÿ-]+$"
)
V_URGENTE_RE = re.compile(
    r"^https://canalizador-urgente\.pt/canalizador-urgente-[a-z0-9à-ÿ-]+$"
)
BLOG_RE = re.compile(
    r"^https://canalizador-urgente\.pt/blog/[a-z0-9à-ÿ-]+$"
)
# Pollution connue spécifique canalizador-urgente (à enrichir si découverte)
POLLUTION_KNOWN: set[str] = set()


def categorize(url: str) -> str:
    path = urlparse(url).path.lstrip("/")
    # Compare pollution only by last path segment
    if path in POLLUTION_KNOWN:
        return "POLLUTION"
    if V_URGENTE_RE.match(url):
        return "V_URGENTE"
    if V_STD_RE.match(url):
        return "V_STD"
    if BLOG_RE.match(url):
        return "BLOG"
    return "INSTITUC"


def load_urls(sitemap_path: Path) -> list[str]:
    text = sitemap_path.read_text(encoding="utf-8")
    return re.findall(r"<loc>([^<]+)</loc>", text)


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--sitemap", default="sitemap-villages.xml")
    p.add_argument("--output", default=None)
    args = p.parse_args()

    sp = Path(args.sitemap)
    if not sp.exists():
        print(f"ERROR: {sp} introuvable.", file=sys.stderr)
        return 1

    urls = load_urls(sp)
    cnt: Counter[str] = Counter()
    pollution_urls: list[str] = []
    instituc_urls: list[str] = []
    blog_urls: list[str] = []
    v_urgente_urls: list[str] = []
    for u in urls:
        cat = categorize(u)
        cnt[cat] += 1
        if cat == "POLLUTION":
            pollution_urls.append(u)
        elif cat == "INSTITUC":
            instituc_urls.append(u)
        elif cat == "BLOG":
            blog_urls.append(u)
        elif cat == "V_URGENTE":
            v_urgente_urls.append(u)

    total = len(urls)
    pct = {k: round(v / total * 100, 2) for k, v in cnt.items()}

    report = {
        "sitemap": str(sp),
        "total_urls": total,
        "by_category": dict(cnt),
        "by_category_pct": pct,
        "pollution_urls": sorted(pollution_urls),
        "instituc_urls": sorted(instituc_urls),
        "blog_count": cnt["BLOG"],
        "v_urgente_count": cnt["V_URGENTE"],
        "v_urgente_sample": sorted(v_urgente_urls)[:10],
        "verdict": {
            "pollution_count": cnt["POLLUTION"],
            "pollution_blocks_declaration": cnt["POLLUTION"] > 0,
        },
        "ran_at": datetime.utcnow().isoformat() + "Z",
    }
    out = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(out + "\n", encoding="utf-8")
        print(f"Rapport écrit dans {args.output}")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
