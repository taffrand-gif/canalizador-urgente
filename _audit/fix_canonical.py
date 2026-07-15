#!/usr/bin/env python3
"""
Fix canonical self-ref pour buckets B+D (CU canalizador-urgente).

Lit _audit/canonical-triage-CU.csv, sélectionne status_bucket in
{b_bug_case_study_blog, d_broken_404_empty}, et patch chaque fichier
pour remplacer la cible canon par self-ref.

DRY-RUN par défaut. --apply pour écrire.
GATE : 30 fichiers attendus, 1 ligne/fichier, 0 modification collatérale.
"""
import csv
import re
import sys
import argparse
from pathlib import Path

ROOT = Path(".")
CSV = ROOT / "_audit" / "canonical-triage-CU.csv"

RE_CANON = re.compile(
    r'(<link[^>]+rel=["\']canonical["\'][^>]+href=["\'])([^"\']+)(["\'])',
    re.IGNORECASE,
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Écrire les changements")
    args = ap.parse_args()

    if not CSV.exists():
        print(f"ERREUR: {CSV} introuvable. Lancer d'abord scan_canonical.py.", file=sys.stderr)
        sys.exit(1)

    targets = []
    with CSV.open() as f:
        for row in csv.DictReader(f):
            if row["status_bucket"] in ("b_bug_case_study_blog", "d_broken_404_empty"):
                targets.append(row)

    print(f"# Fichiers à fixer: {len(targets)}", file=sys.stderr)

    fixed = 0
    skipped = 0
    errors = []
    diff_log = []

    for t in targets:
        fp = ROOT / t["file"]
        if not fp.exists():
            errors.append(f"ABSENT: {t['file']}")
            continue

        # slug self-ref attendu
        m = re.match(r"^canalizador-(.+)\.html$", t["file"])
        if not m:
            errors.append(f"NOM INATTENDU: {t['file']}")
            continue
        expected_self = f"https://canalizador-urgente.pt/canalizador-{m.group(1)}"

        try:
            raw = fp.read_bytes()
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("latin-1", errors="replace")

        old_canon = t["canon_target"]
        # Remplacer UNIQUEMENT l'occurrence qui match old_canon
        # Si old_canon apparaît plusieurs fois dans le fichier, on les remplace toutes
        # (canonical devrait être unique)
        count = text.count(old_canon)
        if count == 0:
            errors.append(f"CIBLE INTROUVABLE: {t['file']} (cherché '{old_canon}')")
            continue
        if count > 1:
            errors.append(f"CIBLE MULTIPLE ({count}x): {t['file']}")
            continue

        new_text = text.replace(old_canon, expected_self, 1)

        # Vérifier qu'on a bien 1 canonical et qu'il pointe vers self-ref
        new_canons = RE_CANON.findall(new_text)
        if len(new_canons) != 1:
            errors.append(f"POST-FIX MULTI CANON: {t['file']} ({len(new_canons)} canon)")
            continue
        if new_canons[0][1] != expected_self:
            errors.append(f"POST-FIX MAUVAISE CIBLE: {t['file']} ({new_canons[0][1]})")
            continue

        diff_log.append((t["file"], old_canon, expected_self, t["status_bucket"]))

        if args.apply:
            # Réécrire en utf-8 strict, en préservant l'encoding binaire d'origine
            # On a décodé en utf-8 strict → on réécrit en utf-8 sans BOM
            new_bytes = new_text.encode("utf-8")
            if new_bytes == raw:
                errors.append(f"NO-OP: {t['file']} (octets identiques)")
                continue
            fp.write_bytes(new_bytes)
            fixed += 1
        else:
            skipped += 1

    # === RAPPORT ===
    print("=" * 70)
    if args.apply:
        print(f"MODE: APPLY (écriture réelle)")
    else:
        print(f"MODE: DRY-RUN (lecture seule)")
    print(f"Fichiers à fixer: {len(targets)}")
    print(f"Fixed:   {fixed}")
    print(f"Skipped: {skipped}")
    print(f"Errors:  {len(errors)}")
    print("=" * 70)

    if errors:
        print("\n# ERREURS :")
        for e in errors:
            print(f"  - {e}")

    print("\n# DIFF (uniquement lignes modifiées) :")
    for f, old, new, bucket in diff_log:
        print(f"  [{bucket}] {f}")
        print(f"    - {old}")
        print(f"    + {new}")

    if not args.apply:
        print(f"\n# Pour appliquer : python3 _audit/fix_canonical.py --apply")


if __name__ == "__main__":
    main()