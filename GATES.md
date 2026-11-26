# Gate CU — pilote desentupimento général

- **Dépôt** : `canalizador-urgente`
- **Worktree** : `/Users/admin/work/Sites/_worktrees/seo-pilot-cu-desentupimento-20261126`
- **Branche** : `seo/pilot-cu-desentupimento-20261126`
- **Périmètre servi** : `desentupir-canos.html` uniquement
- **Intention** : desentupimento urgente général (canos, pias, lavatórios, ralos, esgoto), sans lot local, sans blog, sans génération de masse
- **Arbitrage** : cette page est le hub canonique parce que son title/H1/canonical ciblent déjà le service général et que `/sitemap.xml` contient une entrée dédiée ; les pages `canalizador-desentupimento-<localidade>` restent hors périmètre du pilote.
- **GO requis** : aucun merge, Ready ou déploiement production sans GO nommé de Filipe.

## Population et invariants

- Fichier modifié autorisé : `desentupir-canos.html`.
- Canonical attendu : `https://canalizador-urgente.pt/desentupir-canos`.
- PT-PT ; plomberie CU uniquement ; aucun claim DGEG/TR​​IESP/wallbox.
- Téléphone CU : `928 484 451` ; liens `tel:` et WhatsApp obligatoires.
- Prix autorisés : 70 €/h + 30 € TTC en semaine 09:00–18:00 ; 100 €/h + 50 € TTC après 18:00, nuit, week-ends et jours fériés ; heure commencée due ; déplacement lorsqu’il a lieu.
- Équipements/méthodes publiables sur CU : Ridgid K9-102, câmara endoscópica, fluoresceína, detetor de humidade, luz UV avec fluoresceína lorsque pertinent, desentupimento por alta pressão seulement selon diagnostic.
- Aucun avis, chantier, résultat, garantie, délai d’arrivée chiffré, adresse personnelle, zone non prouvée ou promesse de résultat.
- Sitemap : l’URL canonique doit rester présente ; aucun ajout massif.

## Contrôles reproductibles

### Source

```bash
grep -q '<link rel="canonical" href="https://canalizador-urgente.pt/desentupir-canos">' desentupir-canos.html
grep -q 'href="tel:+351928484451"' desentupir-canos.html
grep -q 'wa.me/351928484451' desentupir-canos.html
python3 - <<'PY'
import json, re
from pathlib import Path
s=Path('desentupir-canos.html').read_text()
blocks=re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
assert blocks
for b in blocks: json.loads(b)
assert s.count('<h1') == 1
assert 'DGEG' not in s and 'TRIESP' not in s and 'wallbox' not in s
PY
```

### Build / HTML / sitemap

```bash
# dépôt statique : contrôler le script de validation présent, sinon documenter N/A
find . -maxdepth 2 -type f \( -name 'package.json' -o -name '*sitemap*' -o -name '*validate*' \) -print
python3 - <<'PY'
from pathlib import Path
import xml.etree.ElementTree as ET
for p in Path('.').glob('sitemap*.xml'):
    ET.parse(p)
assert any('https://canalizador-urgente.pt/desentupir-canos' in p.read_text() for p in Path('.').glob('sitemap*.xml'))
PY
```

### Preview / DOM

- URL Preview à consigner après push : `https://canalizador-urgente-<deployment>.vercel.app/desentupir-canos`.
- `PASS_PREVIEW` seulement après HTTP 200 de la page HTML attendue et DOM Playwright exécuté par le done-gate.
- Une Preview Vercel protégée par login est `NON VÉRIFIÉE`, jamais `PASS_PREVIEW`.

## Statut initial

`PARTIEL / PASS_SOURCE` après audit initial ; build, HTTP, DOM, Preview et production : `NON VÉRIFIÉ`.

## FINI attendue

`FINI = [commande][desentupir-canos.html][commit][source][niveau][production inchangée][exceptions: aucune]`
