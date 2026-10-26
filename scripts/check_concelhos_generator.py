#!/usr/bin/env python3
"""Test : échoue si le générateur concelhos est dégelé alors que la source est incomplète,
ou si une page concelho porte un priceRange avec montants. Code 1 = échec."""
import json, os, re, subprocess, sys, glob
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errs = []
data = json.load(open(os.path.join(R, "data/concelhos.json")))
need = ("desloc_day", "desloc_night", "hour_day", "hour_night")
missing = [c["slug"] for c in data if not all(k in c.get("price", {}) for k in need)]
r = subprocess.run([sys.executable, os.path.join(R, "scripts/gen_concelhos.py")], capture_output=True, text=True)
frozen = r.returncode != 0 and "gelé" in (r.stderr + r.stdout)
if missing and not frozen:
    errs.append(f"{len(missing)} concelhos sans desloc_day/desloc_night/hour_* et générateur non gelé")
for f in sorted(glob.glob(os.path.join(R, "concelhos/*.html"))):
    if re.search(r'"priceRange"\s*:\s*"[^"]*\d', open(f, encoding="utf-8").read()):
        errs.append("priceRange chiffré: " + os.path.relpath(f, R))
print(f"frozen={frozen} incomplete_records={len(missing)} pages={len(glob.glob(os.path.join(R,'concelhos/*.html')))}")
for e in errs: print("ECHEC", e)
sys.exit(1 if errs else 0)
