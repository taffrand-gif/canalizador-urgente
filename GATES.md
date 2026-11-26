# Gate CU — pilote desentupimento général

- **Dépôt** : `canalizador-urgente`
- **Worktree** : `/Users/admin/work/Sites/_worktrees/seo-pilot-cu-desentupimento-20261126`
- **Branche** : `seo/pilot-cu-desentupimento-20261126`
- **Périmètre servi** : `desentupir-canos.html` uniquement
- **Intention** : desentupimento urgente général (canos, pias, lavatórios, ralos, esgoto), sans lot local, sans blog, sans génération de masse
- **Arbitrage** : cette page est le hub canonique parce que son title/H1/canonical ciblent déjà le service général et que `/sitemap.xml` contient une entrée dédiée ; les pages `canalizador-desentupimento-<localidade>` restent hors périmètre du pilote.
- **GO requis** : aucun merge, Ready ou déploiement production sans GO nommé de Filipe.

## Empreintes du lot

- **BASE** : `ed9fb26d39c49e6458c2f94558016f2e6d1398ed`
- **HEAD** : `ea5af60487cf83a84a42c887ed7616f1a877b099`
- **FILES_SHA256** : `4b2c7922301e5efa2306743fc4bc3818c1a1c13beb42bc02e56d06058a12cf6e`
- **POPULATION surface gate** : `2587` fichiers texte scannés ; **lot servi** : `desentupir-canos.html` (1 fichier)

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

## Preuves source obtenues après le commit `ea5af60487cf83a84a42c887ed7616f1a877b099`

- `git diff --check` : OK.
- Contrôles Python : canonical attendu, `tel:` CU, WhatsApp CU, Ridgid K9-102, câmara endoscópica, absence DGEG/TR​​IESP/wallbox : OK.
- JSON-LD : 1 bloc parsé ; H1 : 1.
- Sitemaps XML : tous les `sitemap*.xml` parsés ; URL canonique présente dans `sitemap.xml`.
- Dépôt statique : aucun `package.json` ; build applicatif : N/A, artefact = HTML source.

## Résultat done-gate v3.14

- Passage source tenté avec `done-gate.py` : `BLOCKED` car la commande initiale testait un HEAD sans le commit du lot ; le second passage a aussi exigé les témoins multi-couche et la variante JSON-LD du lot.
- Sonde DOM officielle tentée sur `http://127.0.0.1:8765/desentupir-canos.html` : `BLOCKED` par la politique d’exécution (`Permission denied` sur le bind local) ; aucune preuve DOM n’est revendiquée.
- `vercel.json` est signalé hors lot par le gate mais présent dans la surface servie ; aucune modification de ce fichier.
- Preview publique et production : `NON VÉRIFIÉES` ; pas de merge, Ready, promotion ou production.

## Statut

`PARTIEL / PASS_SOURCE` par contrôles déterministes dédiés ci-dessus ; `PASS_BUILD`, `PASS_HTTP`, `PASS_DOM`, `PASS_PREVIEW` et `PASS_PRODUCTION` : `NON VÉRIFIÉ`.

## FINI attendue

`FINI = [commande][desentupir-canos.html][commit][source][niveau][production inchangée][exceptions: aucune]`
