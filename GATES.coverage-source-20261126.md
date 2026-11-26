# GATES — CU coverage source 2026-11-26

BASE: ed9fb26d3
HEAD: à produire après commit
FILES_SHA256: À CALCULER PAR LE gate
POPULATION: page Requejo + 4 sitemaps + source precos-zonas + IndexNow + index A-Z + index Schema.org local + maillage Mahíde + résidus Moimenta/Tavira dans HTML/LLM/index PAA
BRANCH: fix/cu-coverage-source-20261126

## Objectif mesurable
Retirer de CU la page commerciale espagnole Requejo de Sanabria, sa donnée source et toutes ses surfaces d’indexation/maillage, puis retirer les surfaces servies Moimenta da Beira et Tavira hors couverture, sans modifier les pages portugaises autorisées ni la source de classification `indexable:false`.

## Source active
`canalizador-requejo-de-sanabria.html` est la page supprimée. Le slug était aussi présent dans `precos-zonas.json`, `canalizador-urgente-indexnow-urls.txt`, `indice-a-z.html`, `localizacoes/index.html` et le bloc related de `canalizador-mahde.html`. Les URLs étaient présentes dans `public/sitemap.xml`, `public/sitemap-villages.xml`, `sitemap.xml` et `sitemap-villages.xml`.

## Gate
- Motif : `requejo-de-sanabria|Requejo de Sanabria`.
- Attendu : zéro résidu hors historiques d’audit et gates ; ancienne URL HTTP 404 après production.
- Invariants : téléphone, WhatsApp, CTA, GA4, Consent Mode, RGPD, prix, pages CU portugaises.
- Régénération : `python3 scripts/build_sitemap_full.py https://canalizador-urgente.pt` rejoué ; aucune URL Requejo ne revient.
- Structure : `precos-zonas.json` valide ; quatre sitemaps XML valides.
- Production : aucun merge sans GO nommé.

## Sous-lot résiduel Moimenta/Tavira

- Manifest : `_audit/cu-coverage-source-residual-manifest-20261126.json`.
- Avant patch : 21 fichiers/41 lignes Moimenta da Beira, 16 fichiers/35 lignes Tavira dans les surfaces HTML/XML/TXT/LLM, plus 21 liens PAA dans l’index A-Z.
- Après patch : zéro Moimenta da Beira, zéro Tavira et zéro Requejo dans les surfaces HTML/XML/TXT contrôlées ; zéro URL exclue dans les quatre sitemaps et les deux listes IndexNow.
- Résidus autorisés : `data/concelhos.json` garde l’enregistrement Moimenta da Beira avec `indexable:false` comme source de classification ; `scripts/build_data.py` garde son commentaire explicatif. Ce ne sont pas des surfaces servies.
- Invariants : `canalizador-moimenta.html` conservée ; Vila Nova da Rainha non modifiée ; aucun CU Production.

## Chaîne visée
source → artefact → sitemap/IndexNow/DOM → HTTP → production

## Rsultats finaux excuts 2026-11-26

- `python3 scripts/build_sitemap_full.py https://canalizador-urgente.pt` : PASS_REGEN_SITEMAP_NO_EXCLUDED_URLS ; 2 095 URLs gnres ; `sitemap.xml` et `public/sitemap.xml` crits.
- Source/structure : PASS_SOURCE_JSON ; `data/concelhos.json` valide ; 6 XML valides ; `python3 -m py_compile scripts/build_data.py scripts/build_sitemap_full.py` russi.
- Surfaces servies : PASS_HTML_XML_TXT_ZERO ; 2 461 fichiers HTML/XML/TXT contrlllls, hors `_archive` historique et `_audit` ; zro `Moimenta da Beira`, `Tavira` ou `Requejo de Sanabria`.
- IndexNow : PASS_INDEXNOW_ZERO ; 5 fichiers contrlllls ; zro URL exclue.
- Invariants : PASS_INVARIANTS ; `/canalizador-moimenta` conserve ; `canalizador-vila-nova-da-rainha.html` inchange et prsente dans les sitemaps + IndexNow principal ; source Moimenta `indexable:false` conserve.
- Hygine : PASS_DIFF_CHECK ; `git diff --check` russi.
- NON VRIFI : CI/Preview et HTTP Production ; aucun merge ni dploiement Production dans ce lot.
