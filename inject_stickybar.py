#!/usr/bin/env python3
"""Injecte <script src="/sticky-mobile.js" defer></script> avant </body> sur tous les HTML."""
import os
import re
import sys
from pathlib import Path

SCRIPT_TAG = '<script src="/sticky-mobile.js" defer></script>'
BATCH_SIZE = 50

# Fichiers à modifier (HTML racine uniquement, hors public/ et concelhos/)
html_files = sorted([
    f for f in Path('.').glob('*.html')
    if f.is_file()
])

print(f"Total fichiers HTML à traiter: {len(html_files)}")

modified = 0
skipped = 0
batch_count = 0

# Traiter par batchs
for i, f in enumerate(html_files):
    try:
        content = f.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        try:
            content = f.read_text(encoding='latin-1')
        except Exception as e:
            print(f"ERREUR lecture {f.name}: {e}")
            skipped += 1
            continue
    
    # Check si déjà injecté
    if 'sticky-mobile.js' in content:
        skipped += 1
        continue
    
    # Check pattern </body>
    if '</body>' not in content:
        skipped += 1
        continue
    
    # Injecter
    new_content = content.replace('</body>', f'{SCRIPT_TAG}\n</body>')
    f.write_text(new_content, encoding='utf-8')
    modified += 1
    
    # Commit chaque batch de 50 fichiers
    if modified % BATCH_SIZE == 0:
        batch_count += 1
        print(f"  Batch {batch_count} atteint: {modified} fichiers modifiés")

print(f"\nTerminé: {modified} modifiés, {skipped} ignorés")
print(f"Total batches: {(modified // BATCH_SIZE) + (1 if modified % BATCH_SIZE else 0)}")
