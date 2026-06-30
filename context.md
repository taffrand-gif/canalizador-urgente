# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-06-30
- Tâche exécutée : R4 — FAQ schema calculadora-de-preco.html (prix + tel NAP)
- Branche créée : `loop/2026-06-30-canalizador-urgente-faq-schema-r4`
- PR ouverte : https://github.com/taffrand-gif/canalizador-urgente/pull/68
- Résultat : ✅ 2 commits, 1 fichier modifié. PR ouverte, attente merge Philippe.

## Tâche suivante recommandée
- Tâche : A2 — 8 pages /zonas/ prioritaires (Bragança, Vila Real, Mirandela, Chaves, Miranda do Douro, Mogadouro, Vinhais, Lamego)
- Priorité : HAUTE (CRITIQUE)
- Statut : 🛑 STOP — attente GO explicite Philippe (ne pas créer sans validation)
- Alternative si GO pas encore reçu : vérifier schema.org des pages services (A2-BIS pattern sur eletricista-urgente avait découvert des violations similaires)

## Apprentissages (self-improving)
- calculadora-de-preco.html FAQ JSON-LD avait "Desde 130 EUR" non conforme à grille 65€/h — pattern à checker systématiquement sur eletricista-urgente aussi
- Format telephone schema: "+351-" (tiret) → "+351 " (espace) — NAP uniforme cross-site
- A2 /zonas/ est STOP attente Philippe — ne pas démarrer sans GO écrit dans HISTORIQUE SEO_PLAN

## Edge cases détectés
- Ce site utilise "65 €" (avec espace) pas "65€" → adapter les greps R8 en conséquence
- _archive/ contient de vieux fichiers avec violations — NE PAS patcher _archive/
- calculadora-de-preco.html : zones décalées vs AGENTS.md (Z1=€20 dans calculateur vs 15€ dans AGENTS) → valeur dans l'UI est peut-être différente intentionnellement (urgence vs normal) — NE PAS toucher la logique JS sans GO Philippe

## Blocages connus
- A2 (/zonas/ pages) = 🛑 STOP attente GO Philippe
- Zones tarif calculateur vs AGENTS.md : ambiguïté → laisser en place, noter pour Philippe

## Instructions améliorées pour prochain run
1. Si GO A2 reçu : créer 8 fichiers HTML statiques `canalizador-urgente-{ville}-zona.html` avec contenu Doctrine §12 grille 65 €/h + Z1-Z6 + FAQ urgence + NAP 928 484 451
2. Checker calculadora-de-preco.html de eletricista-urgente pour pattern similaire (130 EUR / 30-50% / +351-)
3. grep R8 : "65 €" (espace) pas "65€/h"
4. Si lock file git : desktop-commander rm host-side
5. SITE COMPLET pour tâches autonomes — prochaine tâche = A2 sur GO Philippe
