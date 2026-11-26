# GATES — CU coverage source 2026-11-26

BASE: ed9fb26d3
HEAD: à produire après commit
FILES_SHA256: À CALCULER PAR LE gate
POPULATION: page Requejo + 4 sitemaps + source precos-zonas + IndexNow + index A-Z + index Schema.org local + maillage Mahíde
BRANCH: fix/cu-coverage-source-20261126

## Objectif mesurable
Retirer de CU la page commerciale espagnole Requejo de Sanabria, sa donnée source et toutes ses surfaces d’indexation/maillage, sans modifier les pages portugaises autorisées.

## Source active
`canalizador-requejo-de-sanabria.html` est la page supprimée. Le slug était aussi présent dans `precos-zonas.json`, `canalizador-urgente-indexnow-urls.txt`, `indice-a-z.html`, `localizacoes/index.html` et le bloc related de `canalizador-mahde.html`. Les URLs étaient présentes dans `public/sitemap.xml`, `public/sitemap-villages.xml`, `sitemap.xml` et `sitemap-villages.xml`.

## Gate
- Motif : `requejo-de-sanabria|Requejo de Sanabria`.
- Attendu : zéro résidu hors historiques d’audit et gates ; ancienne URL HTTP 404 après production.
- Invariants : téléphone, WhatsApp, CTA, GA4, Consent Mode, RGPD, prix, pages CU portugaises.
- Régénération : `python3 scripts/build_sitemap_full.py https://canalizador-urgente.pt` rejoué ; aucune URL Requejo ne revient.
- Structure : `precos-zonas.json` valide ; quatre sitemaps XML valides.
- Production : aucun merge sans GO nommé.

## Chaîne visée
source → artefact → sitemap/IndexNow/DOM → HTTP → production
