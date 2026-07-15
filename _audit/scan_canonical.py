#!/usr/bin/env python3
"""
Scan CU canalizador-*.html pour triage canonical cross-page.

Méthode : parser tolérant regex + lxml fallback.
Sortie : CSV avec colonnes :
  file, canon_target, status_bucket, notes
  status_bucket ∈ {self_ref, a_hub_same_concelho, b_bug_case_study_blog, c_money_other_concelho, d_broken_404_empty, e_self_ref_ok, x_multi_canonical, y_no_canonical, z_parse_error}

GATE : compte exact par bucket + CSV triage _audit/canonical-triage-CU.csv
"""
import os
import re
import sys
import csv
import json
from pathlib import Path

ROOT = Path(".")
HTML_FILES = sorted(ROOT.glob("canalizador-*.html"))
print(f"# Fichiers candidats: {len(HTML_FILES)}", file=sys.stderr)

# Regex tolérant (multi-ligne, casse flexible)
RE_CANON = re.compile(
    r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
RE_CANON_ALT = re.compile(
    r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']',
    re.IGNORECASE,
)

CONCELHOS = set()
with open("/tmp/cu-concelhos-slugs.txt") as f:
    for line in f:
        s = line.strip()
        if s:
            CONCELHOS.add(s)
print(f"# Concelhos officiels: {len(CONCELHOS)}", file=sys.stderr)

# Catégories cibles canon
BLOG_PAT = re.compile(r"^https?://[^/]+/blog/", re.IGNORECASE)
CASE_PAT = re.compile(r"^https?://[^/]+/case-study", re.IGNORECASE)
CONCELHOS_PAT = re.compile(r"^https?://[^/]+/concelhos/", re.IGNORECASE)

results = []
multi_count = 0
empty_canon = 0
parse_err = 0

for fp in HTML_FILES:
    slug = fp.name  # ex: canalizador-braganca.html
    # slug-ville (sans préfixe canalizador- ni extension)
    m = re.match(r"^canalizador-(.+)\.html$", slug)
    if not m:
        continue
    ville_slug = m.group(1)

    # Lire en binaire pour tolérer encoding cassé (comme ENR)
    try:
        raw = fp.read_bytes()
        # Tenter utf-8 strict d'abord
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            # Fallback latin-1 pour lecture (canonical toujours ASCII)
            text = raw.decode("latin-1", errors="replace")
    except Exception as e:
        results.append({
            "file": slug,
            "canon_target": "",
            "status_bucket": "z_parse_error",
            "notes": f"read error: {e}",
        })
        parse_err += 1
        continue

    # Trouver TOUS les <link canonical> (flag MULTI)
    canons = RE_CANON.findall(text) + RE_CANON_ALT.findall(text)
    # Dedup en gardant ordre
    seen = set()
    canons_uniq = []
    for c in canons:
        if c not in seen:
            seen.add(c)
            canons_uniq.append(c)

    n_canons = len(canons_uniq)
    if n_canons == 0:
        results.append({
            "file": slug,
            "canon_target": "",
            "status_bucket": "y_no_canonical",
            "notes": "",
        })
        continue
    if n_canons > 1:
        multi_count += 1
        # Prendre le premier mais flaguer
        canon = canons_uniq[0]
        notes = f"MULTI_CANONICAL ({n_canons} found): {'|'.join(canons_uniq)}"
    else:
        canon = canons_uniq[0]
        notes = ""

    # Cible vide ?
    if not canon.strip():
        empty_canon += 1
        results.append({
            "file": slug,
            "canon_target": canon,
            "status_bucket": "d_broken_404_empty",
            "notes": "empty target" + (" | " + notes if notes else ""),
        })
        continue

    # Extraire path canon
    canon_path = re.sub(r"^https?://[^/]+", "", canon).rstrip("/")
    canon_path_noext = canon_path.removesuffix(".html")
    expected_self = f"/canalizador-{ville_slug}"

    # === CLASSIFICATION ===
    if canon_path_noext == expected_self:
        # self-ref parfait
        results.append({
            "file": slug,
            "canon_target": canon,
            "status_bucket": "e_self_ref_ok",
            "notes": notes,
        })
        continue

    # Bucket B : cible case-study ou blog
    if CASE_PAT.match(canon) or BLOG_PAT.match(canon):
        results.append({
            "file": slug,
            "canon_target": canon,
            "status_bucket": "b_bug_case_study_blog",
            "notes": notes or "cible = case-study|blog",
        })
        continue

    # Bucket D : cible concelhos/ (inhabituel pour page racine)
    if CONCELHOS_PAT.match(canon):
        results.append({
            "file": slug,
            "canon_target": canon,
            "status_bucket": "d_broken_404_empty",
            "notes": "cible = /concelhos/ (non-money racine)" + (" | " + notes if notes else ""),
        })
        continue

    # Bucket A : cible = canalizador-urgente-{concelho-officiel} (money hub légitime)
    # Bucket B-typo : cible = canalizador-{slug-bizarre/non-officiel} (typo probable → fix self-ref)
    m_urg = re.match(r"^/canalizador-urgente-(.+)$", canon_path_noext)
    if m_urg:
        cible_slug = m_urg.group(1)
        # Si le slug cible est un concelho officiel parmi nos 33 hubs → bucket A
        if cible_slug in CONCELHOS:
            results.append({
                "file": slug,
                "canon_target": canon,
                "status_bucket": "a_hub_same_concelho",
                "notes": "cible = hub urgence concelho officiel" + (" | " + notes if notes else ""),
            })
            continue
        # Sinon → bucket C (revue manuelle, money autre non-officiel)
        results.append({
            "file": slug,
            "canon_target": canon,
            "status_bucket": "c_money_other_concelho",
            "notes": "cible=canalizador-urgente-{slug non-officiel}" + (" | " + notes if notes else ""),
        })
        continue

    # Bucket D-typo : cible = canalizador-{slug} mais slug bizarre (pas self, pas urgence)
    # On classifie ici selon heuristique slug "money" probable
    m2 = re.match(r"^/canalizador-(.+)$", canon_path_noext)
    if m2:
        cible_slug = m2.group(1)
        # Si slug source == slug cible mais avec extension ou variante → bucket A (GARDER)
        if cible_slug == ville_slug:
            results.append({
                "file": slug,
                "canon_target": canon,
                "status_bucket": "a_hub_same_concelho",
                "notes": "variante self (extension)" + (" | " + notes if notes else ""),
            })
            continue
        # Sinon → bucket C (revue manuelle potentielle typo ou money autre)
        results.append({
            "file": slug,
            "canon_target": canon,
            "status_bucket": "c_money_other_concelho",
            "notes": "cible=autre slug canalizador- non-officiel" + (" | " + notes if notes else ""),
        })
        continue

    # Bucket D : cible = autre chose (URL malformée, autre path bizarre)
    results.append({
        "file": slug,
        "canon_target": canon,
        "status_bucket": "d_broken_404_empty",
        "notes": "cible malformée/non-standard" + (" | " + notes if notes else ""),
    })

# === ÉCRITURE CSV ===
out_csv = ROOT / "_audit" / "canonical-triage-CU.csv"
out_csv.parent.mkdir(exist_ok=True)
with out_csv.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["file", "canon_target", "status_bucket", "notes"])
    w.writeheader()
    w.writerows(results)

# === COMPTE PAR BUCKET ===
from collections import Counter
counts = Counter(r["status_bucket"] for r in results)

summary = {
    "total_files": len(results),
    "multi_canonical_count": multi_count,
    "empty_canon_count": empty_canon,
    "parse_err_count": parse_err,
    "counts_per_bucket": dict(counts),
}
with open(ROOT / "_audit" / "canonical-triage-CU-summary.json", "w") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print(json.dumps(summary, indent=2, ensure_ascii=False))
print(f"# CSV écrit: {out_csv} ({len(results)} lignes)", file=sys.stderr)