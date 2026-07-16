#!/usr/bin/env python3
"""
fix_zones_tomtom — Recalcule zone + price.desloc depuis la grille Filipe (prix→route_km)
pour data/concelhos.json. Source de vérité = `~/work/Sites/_audit/zonas-distances-concelhos.json`.

Grille verrouillée Filipe 2026-07-14 :
  Z1 0-15 km = 15 € · Z2 15-30 = 25 € · Z3 30-50 = 35 € · Z4 50-70 = 45 €
  Z5 70-90 = 55 € · Z6 90-140 = 65 €

Usage (dry-run par défaut ; APPLY pour modifier concelhos.json) :
  python3 scripts/fix_zones_tomtom.py                # dry-run
  python3 scripts/fix_zones_tomtom.py --apply        # écrit concelhos.json

DoD : 34/34 concelhos avec zone==grille(route_km).

Ref : AGENTS.md §10 (Crawlers IA OUVERTS), R11 Zéro Invention, R3 STOP validation,
_audit/SPEC-DIFFERENCIATION-P1-2026-07-16.md §2 & §10 (préséance source = concelhos.json
quand grille(route_km) OK, sinon zones-distances via lookup ZONE_BANDS).
"""
import json, argparse, sys, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZONAS_FILE = Path('/Users/admin/work/Sites/_audit/zonas-distances-concelhos.json')
DATA_FILE = ROOT / 'data' / 'concelhos.json'

ZONE_BANDS = [(15, 1, 15), (30, 2, 25), (50, 3, 35), (70, 4, 45), (90, 5, 55), (140, 6, 65)]


def zone_from_km(km):
    if km is None:
        return None
    for sup, z, p in ZONE_BANDS:
        if km < sup:
            return z, p
    return None


def norm_name(s):
    import unicodedata
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return ' '.join(s.replace('-', ' ').split())


def load_zonas():
    with open(ZONAS_FILE) as f:
        zonas = json.load(f)['concelhos']
    by_norm = {}
    for name, v in zonas.items():
        by_norm[norm_name(name)] = (name, v)
    return by_norm


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true', help='Écrire concelhos.json (sinon dry-run)')
    args = ap.parse_args()

    with open(DATA_FILE) as f:
        concelhos = json.load(f)
    zonas_by_norm = load_zonas()

    fixed = []
    no_source = []
    unchanged = []

    for c in concelhos:
        name = c['name']
        slug = c['slug']
        n = norm_name(name)
        # match par nom ou par slug
        src = zonas_by_norm.get(n)
        if not src:
            for k_norm, (k_name, v) in zonas_by_norm.items():
                if v.get('slug') == slug:
                    src = (k_name, v)
                    break
        if not src:
            no_source.append((name, slug))
            continue
        _, info = src
        km = info.get('km')
        new = zone_from_km(km)
        if new is None:
            continue
        new_zone, new_price = new
        old_zone = c.get('zone')
        old_price = c.get('price', {}).get('desloc') if c.get('price') else None

        if old_zone != new_zone or old_price != new_price:
            fixed.append({
                'name': name,
                'slug': slug,
                'km': km,
                'old': (old_zone, old_price),
                'new': (new_zone, new_price),
            })
            # Patch en mémoire
            c['zone'] = new_zone
            if 'price' not in c or c['price'] is None:
                c['price'] = {'desloc': new_price}
            else:
                c['price']['desloc'] = new_price
        else:
            unchanged.append((name, slug))

    # Bilan dry-run
    print(f"=== {len(concelhos)} concelhos (source = data/concelhos.json) ===")
    print(f"  Corrigés:    {len(fixed)}")
    print(f"  Inchangés:   {len(unchanged)}")
    print(f"  Sans source: {len(no_source)}")
    print()
    if fixed:
        print("CORRECTIONS :")
        for f in fixed:
            print(f"  {f['name']:30} km={f['km']:6.1f}  {f['old']} → {f['new']}")
    if no_source:
        print("SANS SOURCE (à investiguer) :")
        for n, s in no_source:
            print(f"  {n}  ({s})")

    if not args.apply:
        print("\n(Dry-run. Utiliser --apply pour écrire le fichier.)")
        return

    # Backup
    backup = DATA_FILE.with_suffix('.json.bak-pre-zones-fix-2026-07-16')
    shutil.copy2(DATA_FILE, backup)
    print(f"\nBackup → {backup}")
    with open(DATA_FILE, 'w') as f:
        json.dump(concelhos, f, ensure_ascii=False, indent=1)
    print(f"Écrit → {DATA_FILE}")

    # DoD : recharger et vérifier 100 %
    with open(DATA_FILE) as f:
        chk = json.load(f)
    ok = 0
    total_check = 0
    zn = {info.get('slug'): info for _, info in zonas_by_norm.values()}
    for c in chk:
        info = zn.get(c['slug'])
        if not info:
            continue
        total_check += 1
        new = zone_from_km(info.get('km'))
        if new is None:
            continue
        if c.get('zone') == new[0] and c.get('price', {}).get('desloc') == new[1]:
            ok += 1
    print(f"\nDoD : {ok}/{total_check} zone+price == grille(route_km).")
    if ok != total_check:
        print("FAIL DoD", file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
