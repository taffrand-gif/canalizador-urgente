# GATES. CU coverage deletion 2026-11-25

BASE: origin/main
POPULATION: 18 HTML files explicitly authorized for deletion
SCOPE: confirmed Spain, Moimenta/Tavira/Viseu hors couverture, excluding Vila Verde da Raia (Chaves) and Vila Nova da Rainha (Macedo de Cavaleiros)
EXCLUDED: Chaves, ValpaMdos, reserved CNR PAA pages, all other files
INVARIANTS: no sitemap or generator edits in this deletion step; no production; no merge
CHECKS: exact manifest, git diff --check, deleted paths only, generators inspected before PR
STATUS: pending validation

## Intégration SEO/GEO/AEO 2026-11-27
BASE_EFFECTIVE: 20f80a7a4
OBJECTIF: conserver la population géographique prouvée et appliquer la présentation neutre du prototype CU.
POPULATION_SUPPLÉMENTAIRE: 1 fichier source du commit ca2ef89d6, plus ce gate.
INVARIANTS: `/canalizador-moimenta` (Moimenta de Vinhais), Chaves et Vila Nova da Rainha conservées ; aucune adresse privée ni promesse non sourcée ; téléphone/WhatsApp conservés.
SOURCE: _governance/20-BUSINESS-FACTS.json ; index.html ; sitemaps/générateurs du commit de base.
PREUVES: manifest exact, scan des fichiers présents, JSON-LD parseable, canonical, CTA, sitemap/XML, git diff --check, régénération contrôlée.
STATUT: PARTIEL — intégration rejouée ; aucun merge, Ready ou Production.

## Preuves rejouées — 2026-11-27
- XML des sitemaps : PASS ; exclusions géographiques contrôlées ; `git diff --check`: PASS.
- Contrôle téléphones sur copie temporaire des surfaces servies, avec exclusion explicite de `_archive`: PASS — 2471 fichiers, numéro unique `+351 928484451`.
- `python3 scripts/build_sitemap_full.py https://canalizador-urgente.pt`: PASS — `sitemap.xml` et `public/sitemap.xml` valides, 2095 URLs ; `git diff --check`: PASS.
- Le contrôle natif `node scripts/check-phones.mjs .` reste bloqué par 7 fichiers de `_archive/canalizador-urgente-pre-r12-massif-2026-06-28`, hors surfaces servies ; aucune archive modifiée.
- Build applicatif et typecheck npm : N/A, aucun `package.json` dans ce site statique ; HTTP, DOM, Preview, Production et contrôle Jev : NON VÉRIFIÉS.
