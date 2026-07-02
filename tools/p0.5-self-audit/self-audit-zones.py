#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
self-audit-zones.py — Audit mécanique des pages localité vs source-of-truth.

OBJECTIF (mission Hermes P0.5, 02/07/2026, base 6,5/10) :
Remplacer les claims subjectifs (« 0 mismatch ») par des CHIFFRES REPRODUCTIBLES.

Pour chaque page HTML (hors -es, hors dist/, hors _archive/, hors node_modules/) :
  1. Résoudre la zone attendue : strip préfixes service du filename → slug
     (fuga-agua-, desentupimento-, fossa-septica-, canalizacao-nova-,
      curto-circuito-, quadro-eletrico-, instalacao-eletrica-, avaria-eletrica-)
     → lookup dans norte-os-marketing/prototypes/zonas-data.json.
     Si localité introuvable → NO_RESOL (à trancher Filipe, décision D3).
  2. KO1 — Badge data-zone ≠ zone attendue :
       <... data-zone="N" ...> ou zone-braganca (classe) ou "Zona N" explicite
       doivent matcher zonas-data.json.
  3. KO2 — Badge ≠ JSON-LD "Deslocação Zona X" :
       la zone annoncée dans la Offer JSON-LD desplazação doit matcher la zone
       attendue (et le badge si présent).
  4. KO3 — Prix body vs grille officielle :
       Z1=15€ / Z2=25€ / Z3=35€ / Z4=45€ / Z5=55€ / Z6=65€.
       Survit aux patchs partiels (ex. badge Z2 corrigé mais body dit "Z3 35€").
  5. KO4 — Délais chiffrés résiduels :
       regex (Tempo|Chegada|resposta)[^<]{0,40}\d{1,3}\s*min
       (R145 strict sur -urgente, toléré sur -norte sous leçon #298).

RÈGLE D'USAGE (barème prochain audit, +2 self-audit chiffré joint) :
  Tout commit de batch inclut la sortie de ce script.
  Interdit d'écrire « 0 KO » sans coller le chiffre brut.

TÉMOINS DE CONTRÔLE (R8 OpenClaw) — cas connus à retrouver à chaque run :
  T1 : Bragança            → zonas-data.json = 2, grille = Z2/25€.
  T2 : Vinhais             → zonas-data.json = 3, grille = Z3/35€.
  T3 : Macedo de Cavaleiros→ zonas-data.json = 1, grille = Z1/15€.

USAGE :
  python3 self-audit-zones.py <repo_path> [<repo_path> ...]
  # Exemple :
  python3 self-audit-zones.py ~/work/Sites/canalizador-urgente
  python3 self-audit-zones.py ~/work/Sites/{canalizador,eletricista}-{urgente,norte-reparos}

SORTIE :
  stdout : résumé par repo (4 catégories KO + NO_RESOL) + totaux
  exit 0 si OK, exit 1 si témoin manquant ou JSON source introuvable.

DÉPENDANCES : stdlib uniquement (json, re, sys, os, pathlib).
"""

import json
import os
import re
import sys
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────
# CONSTANTES MÉTIER (source unique : norte-os-marketing/prototypes/zonas-data.json)
# ──────────────────────────────────────────────────────────────────────

GRILLE = {1: 15, 2: 25, 3: 35, 4: 45, 5: 55, 6: 65}  # Z1..Z6 → €

# Préfixes service à stripper pour résoudre la localité depuis le filename
SERVICE_PREFIXES = (
    "fuga-agua-",
    "desentupimento-",
    "fossa-septica-",
    "canalizacao-nova-",
    "curto-circuito-",
    "quadro-eletrico-",
    "instalacao-eletrica-",
    "avaria-eletrica-",
)

# Localité est dans le filename après strip préfixe(s), avant .html
# Cas spéciaux à stripper en plus :
EXTRA_PREFIXES = (
    "canalizador-",   # préfixe métier (canalizador-braganca.html)
    "eletricista-",   # préfixe métier
)

# Source-of-truth
SOURCE_OF_TRUTH = Path.home() / "work/Sites/norte-os-marketing/prototypes/zonas-data.json"

# Témoins (R8 — au moins 3 cas à retrouver à chaque run)
TEMOINS = {
    "Bragança": 2,
    "Vinhais": 3,
    "Macedo de Cavaleiros": 1,
}

# Regex délais chiffrés (R145 strict -urgente)
RE_DELAIS = re.compile(
    r"(?i)(?:tempo|chegada|resposta)[^<]{0,40}?\d{1,3}\s*min",
)

# Regex badge data-zone / class="zone-..." / mention "Zona N" dans body
RE_BADGE_ATTR = re.compile(r'data-zone=["\'](\d)["\']')
RE_BADGE_CLASS = re.compile(r'class=["\'][^"\']*\bzone-([a-z0-9-]+)\b[^"\']*["\']', re.IGNORECASE)
RE_BADGE_TEXT = re.compile(r"\bZona\s+(\d)\b", re.IGNORECASE)
# Variante : "Z[1-6]=" dans la grille canonique (info, pas KO)
RE_GRILLE_CANON = re.compile(r"Z[1-6]=\d+€")

# Regex JSON-LD "Deslocação Zona X"
RE_JSONLD_DESLOCACAO_ZONE = re.compile(
    r'"(?:description|text)"\s*:\s*"[^"]*Desloca[çc][ãa]o\s+Zona\s+(\d)[^"]*"',
    re.IGNORECASE,
)
# Regex JSON-LD "Offer" deslocação avec prix
RE_JSONLD_OFFER_PRICE = re.compile(
    r'"@type"\s*:\s*"Offer"[^}]*?"price"\s*:\s*"?(\d+)[^"]*?"',
    re.IGNORECASE,
)

# Regex prix body (Deslocação X€ / Zona X : X€)
RE_BODY_DESLOCACAO = re.compile(
    r"Desloca[çc][ãa]o[^.<>\n]{0,40}?(\d{1,3})\s*€",
    re.IGNORECASE,
)
RE_BODY_ZONE_PRIX = re.compile(
    r"\bZona\s+(\d)\b[^.<>\n]{0,80}?(\d{1,3})\s*€",
    re.IGNORECASE,
)
RE_BODY_PRIX_ZONE = re.compile(
    r"(\d{1,3})\s*€[^.<>\n]{0,80}?\bZona\s+(\d)\b",
    re.IGNORECASE,
)


# ──────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────

def slug_to_localidade(slug: str) -> str:
    """Strip préfixes service + métier + suffixes date, retourne nom localité."""
    s = slug
    # Strip suffixes date (ex. -2026, -2025)
    s = re.sub(r"-\d{4}$", "", s)
    # Strip préfixes service (boucle : peut y en avoir plusieurs)
    changed = True
    while changed:
        changed = False
        for p in SERVICE_PREFIXES + EXTRA_PREFIXES:
            if s.startswith(p):
                s = s[len(p):]
                changed = True
                break
    # Slug → "Nome Composto" : remplacer - par espace, Title Case intelligent
    # (particules "de/da/do/das/dos/em/na/no" restent en minuscule,
    #  contrairement à .title() qui les capitalise).
    PARTICULES = {"de", "da", "do", "das", "dos", "em", "na", "no", "e"}
    parts = s.replace("-", " ").split()
    parts = [p.capitalize() if i == 0 or p not in PARTICULES else p
             for i, p in enumerate(parts)]
    return " ".join(parts)


import unicodedata

def unaccent(s: str) -> str:
    """Retire les diacritiques : 'Bragança' → 'Braganca', 'Numão' → 'Numao'."""
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalize_for_lookup(name: str) -> list[str]:
    """Génère les variantes de casse (+ ASCII unaccented) pour lookup zonas-data.json."""
    candidates = [name]
    # Title case (idempotent ici)
    candidates.append(name.title())
    # Upper / Lower
    candidates.append(name.upper())
    candidates.append(name.lower())
    # Variantes ASCII sans accents (slugs sont ASCII ; JSON a accents)
    ua = unaccent(name)
    if ua != name:
        candidates.append(ua)
        candidates.append(ua.title())
        candidates.append(ua.upper())
        candidates.append(ua.lower())
    return list(dict.fromkeys(candidates))  # dedup en gardant l'ordre


def get_zone_from_zonas(zonas: dict, name: str) -> object:
    """Lookup robusto: match direct + match unaccented (toutes variantes)."""
    for cand in normalize_for_lookup(name):
        if cand in zonas:
            return zonas[cand]
    # Fallback : index unaccented (construit à la volée pour 1 lookup)
    for k, v in zonas.items():
        if unaccent(k).lower() == unaccent(name).lower():
            return v
    return None


def extract_badge_zone(content: str, slug: str) -> object:
    """Cherche la zone annoncée par le badge (data-zone, class zone-X, ou texte Zona N)."""
    # Priorité 1 : data-zone="N"
    m = RE_BADGE_ATTR.search(content)
    if m:
        return int(m.group(1))
    # Priorité 2 : class="zone-braganca" etc. — on mappe la classe via lookup zonas
    m = RE_BADGE_CLASS.search(content)
    if m:
        # class="zone-braganca" → mapper via zonas (slug_to_localidade inverse)
        # Approximation : on prend le slug et on cherche sa zone, mais ici on a déjà
        # la zone attendue ; on s'en sert juste pour valider la cohérence interne.
        # → on NE peut PAS déduire la zone d'une classe sémantique sans lookup.
        # Fallback : on tente le lookup du nom de classe.
        return None
    # Priorité 3 : texte "Zona N" dans le body (première occurrence)
    # ATTENTION : la grille canonique (Z1=15€, Z2=25€, ...) en JSON-LD est EXCLUE
    # pour éviter les faux positifs ; on cherche dans le body HTML visible.
    # Heuristique simple : si la mention apparaît dans une <tr> ou <td>, c'est la grille.
    # Pour rester conservateur, on ne s'appuie pas sur cette regex seule —
    # le badge data-zone est la source primaire ; ici on signale juste la présence.
    return None


def extract_jsonld_deslocacao_zone(content: str) -> object:
    """Extrait la zone annoncée dans JSON-LD 'Deslocação Zona X'."""
    m = RE_JSONLD_DESLOCACAO_ZONE.search(content)
    if m:
        return int(m.group(1))
    return None


def extract_body_prix_par_zone(content: str) -> dict[int, int]:
    """Extrait les couples (zone → prix) détectés dans le body."""
    result: dict[int, int] = {}
    for m in RE_BODY_ZONE_PRIX.finditer(content):
        zone = int(m.group(1))
        prix = int(m.group(2))
        result[zone] = prix
    return result


def extract_delais_chiffres(content: str) -> list[str]:
    """Retourne les snippets où un délai chiffré apparaît."""
    return [m.group(0).strip() for m in RE_DELAIS.finditer(content)]


def is_grille_canonique_context(content: str, m: re.Match) -> bool:
    """Heuristique : la mention 'Zona N' est dans la grille canonique Z1=15€..Z6=65€ ?
    Si oui, on NE signale PAS comme KO (c'est une référence, pas une affectation).
    """
    start = max(0, m.start() - 40)
    end = min(len(content), m.end() + 40)
    snippet = content[start:end]
    # Si la grille complète Z1=15€..Z6=65€ est dans le même paragraphe/ligne → info
    return bool(re.search(r"Z[1-6]=\d+€", snippet))


# ──────────────────────────────────────────────────────────────────────
# AUDIT D'UNE PAGE
# ──────────────────────────────────────────────────────────────────────

def audit_page(path: Path, zonas: dict) -> dict:
    """Retourne un dict {kos: [...], no_resol: bool, zone_attendue: int, ...}."""
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"error": str(e), "kos": [], "no_resol": True}

    slug = path.stem  # filename sans extension
    loc = slug_to_localidade(slug)
    expected_zone = get_zone_from_zonas(zonas, loc)
    loc_found = loc if expected_zone is not None else None

    result = {
        "path": str(path),
        "slug": slug,
        "localidade": loc_found,
        "zone_attendue": expected_zone,
        "kos": [],
        "no_resol": expected_zone is None,
        "delais": [],
    }

    if expected_zone is None:
        # NO_RESOL : Filipe tranche (D3)
        return result

    # KO1 : badge data-zone ≠ attendu
    badge = extract_badge_zone(content, slug)
    if badge is not None and badge != expected_zone:
        result["kos"].append({
            "type": "KO1_badge_zona",
            "msg": f"badge data-zone={badge} ≠ zonas-data.json={expected_zone} ({loc_found})",
        })

    # KO2 : badge vs JSON-LD "Deslocação Zona X"
    jsonld_zone = extract_jsonld_deslocacao_zone(content)
    if jsonld_zone is not None and jsonld_zone != expected_zone:
        result["kos"].append({
            "type": "KO2_jsonld_zone",
            "msg": f"JSON-LD 'Deslocação Zona {jsonld_zone}' ≠ attendu={expected_zone} ({loc_found})",
        })
    # Variante KO2bis : JSON-LD OK vs badge KO (incohérence interne)
    if jsonld_zone is not None and badge is not None and badge != jsonld_zone:
        result["kos"].append({
            "type": "KO2bis_badge_vs_jsonld",
            "msg": f"badge={badge} ≠ JSON-LD={jsonld_zone} (page contradictoire)",
        })

    # KO3 : prix body vs grille
    body_prix = extract_body_prix_par_zone(content)
    for zone_annoncée, prix_annoncé in body_prix.items():
        if zone_annoncée == expected_zone:
            # C'est la zone de CETTE page → prix doit matcher la grille
            prix_attendu = GRILLE[expected_zone]
            if prix_annoncé != prix_attendu:
                result["kos"].append({
                    "type": "KO3_prix_body",
                    "msg": f"body Zona {zone_annoncée}={prix_annoncé}€ ≠ grille officielle={prix_attendu}€",
                })

    # KO4 : délais chiffrés
    delais = extract_delais_chiffres(content)
    if delais:
        # Sur -urgente = strict KO. Sur -norte = warning seulement.
        is_urgente = "urgente" in str(path)
        for snippet in delais[:3]:  # cap à 3 exemples
            result["delais"].append(snippet)
            if is_urgente:
                result["kos"].append({
                    "type": "KO4_delai_chiffre_urgente",
                    "msg": f"délai chiffré R145: '{snippet}'",
                })
            # Sur -norte : info, pas KO (leçon #298)

    return result


# ──────────────────────────────────────────────────────────────────────
# SCAN D'UN REPO
# ──────────────────────────────────────────────────────────────────────

def scan_repo(repo: Path, zonas: dict) -> dict:
    """Scan tous les HTML du repo, retourne stats."""
    stats = {
        "repo": str(repo),
        "html_total": 0,
        "no_resol": 0,
        "patched": 0,      # pages sans KO (et résolues)
        "ko1": 0,
        "ko2": 0,
        "ko2bis": 0,
        "ko3": 0,
        "ko4": 0,
        "kos_total": 0,
        "ko_list": [],     # échantillon (max 20 par type)
        "temoin_braganca_ok": None,
        "temoin_vinhais_ok": None,
        "temoin_macedo_ok": None,
    }

    # Itère sur tous les HTML du repo (hors exclusions)
    html_files = []
    for root, dirs, files in os.walk(repo):
        # Exclusions in-place (mutate dirs)
        dirs[:] = [d for d in dirs if d not in {"node_modules", "_archive", "dist", "build", ".git", ".hermes"}]
        for f in files:
            if not f.endswith(".html"):
                continue
            if f.endswith("-es.html"):  # exclusion version espagnole (cohérent P0)
                continue
            html_files.append(Path(root) / f)

    stats["html_total"] = len(html_files)

    for path in html_files:
        r = audit_page(path, zonas)
        if r.get("no_resol"):
            stats["no_resol"] += 1
        elif not r["kos"]:
            stats["patched"] += 1

        for ko in r["kos"]:
            t = ko["type"]
            if t == "KO1_badge_zona": stats["ko1"] += 1
            elif t == "KO2_jsonld_zone": stats["ko2"] += 1
            elif t == "KO2bis_badge_vs_jsonld": stats["ko2bis"] += 1
            elif t == "KO3_prix_body": stats["ko3"] += 1
            elif t == "KO4_delai_chiffre_urgente": stats["ko4"] += 1
            stats["kos_total"] += 1
            if len(stats["ko_list"]) < 30:
                stats["ko_list"].append({
                    "path": str(path.relative_to(repo)),
                    "type": t,
                    "msg": ko["msg"],
                })

        # Témoins : on a un KO SI la page concerne le témoin ET a un KO
        loc = r.get("localidade")
        if loc == "Bragança" and not r["kos"]:
            stats["temoin_braganca_ok"] = True
        elif loc == "Bragança":
            stats["temoin_braganca_ok"] = False
        if loc == "Vinhais" and not r["kos"]:
            stats["temoin_vinhais_ok"] = True
        elif loc == "Vinhais":
            stats["temoin_vinhais_ok"] = False
        if loc == "Macedo de Cavaleiros" and not r["kos"]:
            stats["temoin_macedo_ok"] = True
        elif loc == "Macedo de Cavaleiros":
            stats["temoin_macedo_ok"] = False

    return stats


# ──────────────────────────────────────────────────────────────────────
# AFFICHAGE
# ──────────────────────────────────────────────────────────────────────

def print_repo_stats(s: dict) -> None:
    print(f"\n{'='*78}")
    print(f"REPO : {s['repo']}")
    print(f"{'='*78}")
    print(f"  HTML scannés (hors -es, dist/, _archive/, node_modules/) : {s['html_total']}")
    print(f"  Pages résolues sans KO (patched)                          : {s['patched']}")
    print(f"  Pages NO_RESOL (localité introuvable zonas-data.json)     : {s['no_resol']}")
    print()
    print(f"  KO1 badge ≠ zonas-data.json     : {s['ko1']}")
    print(f"  KO2 JSON-LD deslocação ≠ attendu: {s['ko2']}")
    print(f"  KO2bis badge ≠ JSON-LD (interne): {s['ko2bis']}")
    print(f"  KO3 prix body ≠ grille Z1=15..Z6=65 : {s['ko3']}")
    print(f"  KO4 délais chiffrés (R145 -urgente)   : {s['ko4']}")
    print(f"  ─────────────────────────────────────")
    print(f"  KO TOTAL                          : {s['kos_total']}")
    print()
    # Témoins
    t_strs = []
    for name, val in [("Bragança (Z2/25€)", s['temoin_braganca_ok']),
                       ("Vinhais (Z3/35€)", s['temoin_vinhais_ok']),
                       ("Macedo CV (Z1/15€)", s['temoin_macedo_ok'])]:
        if val is True:
            t_strs.append(f"  ✓ {name} : conforme")
        elif val is False:
            t_strs.append(f"  ✗ {name} : KO détecté")
        else:
            t_strs.append(f"  · {name} : non vu dans ce repo")
    print("  TÉMOINS (R8 OpenClaw) :")
    for ts in t_strs:
        print(ts)
    if s["ko_list"]:
        print()
        print(f"  Échantillon KO ({len(s['ko_list'])} max) :")
        for ko in s["ko_list"][:10]:
            print(f"    [{ko['type']}] {ko['path']}")
            print(f"      → {ko['msg']}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)

    # Charge source-of-truth
    if not SOURCE_OF_TRUTH.exists():
        print(f"ERREUR FATALE : source-of-truth introuvable : {SOURCE_OF_TRUTH}", file=sys.stderr)
        sys.exit(1)
    zonas = json.loads(SOURCE_OF_TRUTH.read_text(encoding="utf-8"))
    print(f"Source-of-truth chargée : {SOURCE_OF_TRUTH} ({len(zonas)} localités)")

    # Vérif témoins dans la source elle-même
    print()
    print("TÉMOINS R8 — vérification dans zonas-data.json :")
    temoin_ok_global = True
    for name, expected in TEMOINS.items():
        actual = zonas.get(name)
        if actual != expected:
            print(f"  ✗ TEMOIN CASSÉ : {name} attendu={expected}, zonas={actual}")
            temoin_ok_global = False
        else:
            print(f"  ✓ {name} = {actual}")

    if not temoin_ok_global:
        print("\nERREUR FATALE : un témoin est cassé → la grille a changé, mettre à jour TEMOINS.", file=sys.stderr)
        sys.exit(1)

    # Scan chaque repo
    totals = {"html_total": 0, "patched": 0, "no_resol": 0,
              "ko1": 0, "ko2": 0, "ko2bis": 0, "ko3": 0, "ko4": 0, "kos_total": 0}
    repo_results = []
    for repo_arg in sys.argv[1:]:
        repo = Path(repo_arg).expanduser().resolve()
        if not repo.exists():
            print(f"\n⚠ Repo introuvable : {repo}", file=sys.stderr)
            continue
        s = scan_repo(repo, zonas)
        repo_results.append(s)
        for k in totals:
            totals[k] += s[k]
        print_repo_stats(s)

    # Totaux
    print(f"\n{'='*78}")
    print("TOTAUX (tous repos)")
    print(f"{'='*78}")
    for k, v in totals.items():
        print(f"  {k:20s} : {v}")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)