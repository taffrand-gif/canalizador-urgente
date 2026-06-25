#!/usr/bin/env python3
"""Commit les fichiers modifiés par batch de 50."""
import subprocess
import sys
from pathlib import Path

BATCH_SIZE = 50

# Récupérer les fichiers modifiés
result = subprocess.run(['git', 'diff', '--name-only'], capture_output=True, text=True)
modified_files = [f for f in result.stdout.strip().split('\n') if f]
print(f"Total fichiers modifiés: {len(modified_files)}")

# Exclure les scripts Python (à committer séparément)
files_to_commit = [f for f in modified_files if not f.endswith('.py')]
print(f"Fichiers HTML/JS à committer: {len(files_to_commit)}")

# Commit par batch
batch_num = 0
for i in range(0, len(files_to_commit), BATCH_SIZE):
    batch = files_to_commit[i:i+BATCH_SIZE]
    batch_num += 1
    
    # git add ce batch
    subprocess.run(['git', 'add'] + batch, check=True)
    
    # Commit
    msg = f"[Atlas] StickyCallBar mobile batch {batch_num}/{(len(files_to_commit) + BATCH_SIZE - 1) // BATCH_SIZE} - {len(batch)} fichiers"
    subprocess.run(['git', 'commit', '-m', msg], check=True)
    print(f"  Commit batch {batch_num}: {len(batch)} fichiers")

# Commit scripts Python
subprocess.run(['git', 'add', 'inject_stickybar.py', 'commit_batches.py'], check=False)
subprocess.run(['git', 'commit', '-m', '[Atlas] Scripts Python injection StickyCallBar'], check=False)

print(f"\nTerminé: {batch_num} commits créés")
