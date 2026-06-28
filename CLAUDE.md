# CLAUDE.md — Configuration Claude Code (Norte-OS)

> Lu par Claude Code dans VSCode. **Ne duplique pas la doctrine** : voir `./AGENTS.md`.
> Daté du 2026-06-28 par Philippe Braganca.

## Site
- **Domaine** : canalizador-urgente.pt
- **NAP** : +351 928 484 451 | Norte Reparos | Trás-os-Montes
- **Métier** : plomberie (💧) — site satellite de `canalizador-norte-reparos.pt`
- **Doctrine** : **Transparence Radicale** (PAS Doctrine A+ — voir `./AGENTS.md` §12)
- **État au 28/06/2026** : 🔴 EN ATTENTE REFONTE (~25k violations héritées)
- **Stack** : statique Vite + HTML/CSS
- **Déploiement** : `git push` → Vercel auto

## Commandes & outils Atlas
- `git fetch && git status` AVANT toute modif (#154)
- Pas de `npm run test`/`lint`/`build` standard — sites statiques
- Slash commands : `/goal` (boucle audit), `/loop`, `/review`

## Workflow patch (rappel court — ⚠️ DIFFÉRENT des sites `-norte-reparos`)
1. **Lire `./AGENTS.md` §11-13** EN ENTIER (Doctrine Transparence Radicale + zéro invention + gabarit)
2. **STOP validation Philippe OBLIGATOIRE** pour tout batch (cf. §12) — *AUCUN batch de pages avant prototype 1 page validé*
3. Témoin grep décomposé AVANT (motifs R12 §12 : délais chiffrés inventés, anonymat réseau, "resposta prioritária")
4. Patch 1 fichier à la fois (R15 : max 95 fichiers/commit, justifié)
5. Témoin grep APRÈS + commit référencé leçon
6. Push SANS `--force` (R6)

## Doctrine complète
➡️ `./AGENTS.md` (Doctrine Transparence Radicale, NAP 928, R11-R13 — gabarit page)

## Patterns R12 à supprimer (DIFFÉRENTS des `-norte-reparos`)
- ❌ Délais chiffrés inventés : "resposta em 30min", "chegamos em X minutos", "tempo médio"
- ❌ Anonymat réseau : "nossa equipa de profissionais" sans visage, "central de atendimento"
- ❌ Phrases "resposta prioritária / mediante confirmação" (R145)
- ✅ OK : "24h/7 dias" (disponibilité), "orçamento por escrito antes de qualquer intervenção"

## Plan stratégique SEO/GEO
➡️ `./SEO_PLAN.md` (vision, état actuel, TODO par phase, historique — priorité 🔴 refonte)

**OBLIGATOIRE** : toute IA / agent / harnais travaillant sur ce repo DOIT :
1. **Lire `AGENTS.md` EN ENTIER** (§11 + §12 + §13 = ZÉRO INVENTION + Transparence Radicale + gabarit)
2. **Lire `SEO_PLAN.md` EN ENTIER** (tâche A1 = refonte homepage = PRIORITÉ 1)
3. **Consigner toute action** dans la section `🔄 HISTORIQUE` du `SEO_PLAN.md`
4. **Suivre l'ordre strict** : A1 (homepage) → A2 (8 pages /zonas/) → B1/B2 (différenciation) → C (backlinks)
5. **JAMAIS merger dans `main`** sans STOP validation Philippe (branche = `prototype-home`)

## Pas touche
- ❌ Pas de duplication de règles ici
- ❌ Pas de duplication du plan dans `SEO_PLAN.md`
- ❌ Pas de batch sans GO Philippe + prototype 1 page
- ❌ Pas de copier-coller automatique (R12 §validation)
- ❌ Pas d'invention de chantiers/témoignages (R11)
- ❌ Pas de merge `prototype-home` → `main` sans STOP
