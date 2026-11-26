# GATES. CU coverage deletion 2026-11-25

BASE: origin/main
POPULATION: 18 HTML files explicitly authorized for deletion
SCOPE: confirmed Spain, Moimenta/Tavira/Viseu hors couverture, excluding Vila Verde da Raia (Chaves) and Vila Nova da Rainha (Macedo de Cavaleiros)
EXCLUDED: Chaves, ValpaMdos, reserved CNR PAA pages, all other files
INVARIANTS: no sitemap or generator edits in this deletion step; no production; no merge
CHECKS: exact manifest, git diff --check, deleted paths only, generators inspected before PR
STATUS: pending validation

# GATES — Pilote CU `contador-agua-disparado`

## Périmètre

Une seule page éditoriale : `blog/contador-agua-disparado.html`. Le pilote vise uniquement le snippet et la fraîcheur éditoriale d’une page déjà visible dans GSC.

## CHECK

Conserver le contenu métier, les prix 70 €/h + 30 € et 100 €/h + 50 €, les CTA téléphone/WhatsApp, le canonical, les données structurées et les liens existants. Ne pas toucher aux pages locales, aux générateurs ni au chantier R145.

## EXPECT

Le title, la meta description et les balises OG portent explicitement l’intention `canalizador urgente` sans promesse de délai inventée. `dateModified`, la date visible du footer et le contenu de l’article passent au 25 novembre 2026. Tous les JSON-LD restent parseables et le diff reste limité à cette page et au présent gate.

Aucun merge, push de production ou déploiement n’est autorisé dans ce pilote.

## NON-VÉRIFIÉ

La nouvelle fenêtre GSC homogène et l’attribution des appels/WhatsApp par page restent indisponibles dans cette exécution.
