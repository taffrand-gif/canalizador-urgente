# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-06-29
- Tâche exécutée : B2 — Correction doublon public/index.html (R12 violations + canonical cassé)
- Branche créée : `loop/2026-06-29-canalizador-urgente-b2-doublon-homepage`
- PR ouverte : https://github.com/taffrand-gif/canalizador-urgente/pull/67
- Résultat : ✅ 1 commit, 1 fichier modifié. SEO_PLAN.md: A1 statut stale corrigé (⏳→✅). PR ouverte, attente merge Philippe.

## Tâche suivante recommandée
- Tâche : A2 — 8 pages /zonas/ prioritaires (Bragança, Vila Real, Mirandela, Chaves, etc.)
- Priorité : HAUTE (CRITIQUE selon SEO_PLAN)
- Note : A2 était "attente GO Philippe" dans la note Hermes — vérifier si GO a été donné avant de commencer

## Apprentissages (self-improving)
- A1 était ✅ FAIT depuis 29/06 (commit 380c1667c) mais le statut SEO_PLAN.md était resté "⏳ À FAIRE" → toujours vérifier HISTORIQUE vs TODO (le TODO peut être stale)
- `public/index.html` dans un repo statique Vercel est servi à `/public/` avec cleanUrls → duplicate content risk si canonical mauvais
- 70€/h → 65€/h fix : déjà fait en prod (0 occurrences hors _archive/) — ne pas refaire
- grep -c "65€" retourne 0 si le site écrit "65 €" (avec espace) → toujours grep "65 €" ET "65€/h" sur ce site

## Edge cases détectés
- Ce site utilise "65 €" (avec espace) pas "65€" → adapter les greps R8 en conséquence
- _archive/ contient de vieux fichiers avec violations — NE PAS patcher _archive/

## Blocages connus
- A2 (/zonas/ pages) était "attente GO Philippe" selon note Hermes 30/06

## Instructions améliorées pour prochain run
1. Vérifier si Philippe a donné GO pour A2 /zonas/ (chercher dans SEO_PLAN.md HISTORIQUE ou messages récents)
2. Pour A2 : créer 8 fichiers HTML statiques `canalizador-urgente-{ville}.html` dans la racine du repo avec contenu Doctrine §12 (grille 65 €/h + Z1-Z6 + équipement + FAQ urgence + NAP 928 484 451)
3. grep R8 sur ce site : utiliser "65 €" (avec espace) pas "65€/h"
4. Si lock file git : utiliser `mcp__desktop-commander__start_process` avec `rm -f ~/work/Sites/{repo}/.git/*.lock && git ...`
