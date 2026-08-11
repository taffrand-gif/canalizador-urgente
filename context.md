# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-11
- Tâche exécutée : **R11/R12 — violation détectée en lecture, traitée en priorité : restauration du ruling Filipe 2026-07-08 dans `AGENTS.md` §12 L129, corrompu par le batch declaim `fb9dd2415` (PR #119).**
- Branche : `loop/2026-08-11-canalizador-urgente-agents-ruling` (depuis `origin/main`, **en worktree**)
- Commits : `18acae4a4` (`AGENTS.md`, **1 ligne**), puis `7c0b054e0` (`SEO_PLAN.md`)
- PR ouverte : https://github.com/taffrand-gif/canalizador-urgente/pull/246
- Résultat : ✅ 2 commits, 2 fichiers. Restauration **verbatim**, octet pour octet, depuis la pré-image `fb9dd2415^:AGENTS.md`. Contrôle d'identité programmatique : bloc restauré **== pré-image → True** ; **== version corrompue → False**. `git diff --numstat AGENTS.md` = **1 ligne modifiée**.

## ✅ RÉSOLU ce run — le point d'escalade n°2 était une CORRUPTION, pas un arbitrage

Le `context.md` du 06/08 demandait de « reporter le ruling 2026-07-08 dans `AGENTS.md` §13 » pour lever la contradiction :

> §13 (L113, L154) **impose** la phrase « orçamento por escrito antes de qualquer intervenção »
> §12 (L129) **l'INTERDIT** sur toute page

**Cette contradiction n'a jamais existé.** `git show fb9dd2415 -- AGENTS.md` → 1 ligne changée :

- **AVANT** : « ni certificat, ni **relatório técnico** (de conformidade), ni ficha … INTERDIT : … « **relatório técnico** », « **fichas eletrotécnicas** » … »
- **APRÈS** : « ni certificat, ni **orçamento por escrito** (de conformidade), ni ficha … INTERDIT : … « **orçamento por escrito** », « **trabalho profissional** » … »

Le commit `fb9dd2415` (« retrait total promesses document → travail réel », **2003 fichiers**) annonce dans son propre message `1610 fichiers 'relatório técnico' → 'orçamento por escrito'` — **et, plus bas, « GARDE : AGENTS.md §12 doctrine inchangée ».** La substitution de masse a balayé `AGENTS.md` avec les pages : **le changement était non intentionnel de l'aveu de son propre auteur.**

**Double dégât, corrigé ce run :**
1. Une formule légitime interdite : « orçamento por escrito » = **19 202 occurrences / 2 427 fichiers** en production, soit la quasi-totalité du site en violation de son propre `AGENTS.md`.
2. **Le ruling silencieusement désarmé** : « relatório técnico » et « fichas eletrotécnicas » ne figuraient plus dans la liste INTERDIT depuis le 09/07.

➡️ **La tâche « reporter le ruling dans §13 » est SANS OBJET.** Ne pas la rouvrir.
➡️ Contrôle de production : `relatório técnico` **0 occ / 0 fichiers**, `fichas eletrotécnicas` **0 / 0** — la purge de la PR #119 tient, restaurer l'interdit **ne rouvre aucun chantier**.
➡️ **Vérifié ce run : les `AGENTS.md` de CNR, ENR et EU ne portent PAS cette corruption.** Le défaut est propre à CU.

## ✅ Gate merge — CADUC, vérifié ce run
Le `context.md` du 06/08 portait « Attente GO merge + GO batch Philippe (R7) » en citant la PR **#240**. Vérification `gh pr view` ce run : **#240 MERGED**, ainsi que #269 (CNR) et #295 (ENR). **Gate effacé.**

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Entre le 06/08 et le 09/08, cette mention a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**. Ne jamais réécrire un gate de ce type.

## 🛑 2 GISEMENTS CHIFFRÉS — DÉCISION REQUISE (inchangés)

### (a) Prix inventé `Desde 130` — ~73 fichiers ⚠️ LE PLUS URGENT
`PRICING-CANONIQUE.md` ne connaît **aucun minimum de 130 €** : la grille verrouillée est **65 €/h + deslocação Z1=15 € · Z2=25 € · Z3=35 € · Z4=45 € · Z5=55 € · Z6=65 €**. Le « 130 » des documents internes désigne le **rayon de 130 km** autour de Macedo de Cavaleiros — **pas un prix**. C'est un prix faux servi en production. **Décision demandée** : autoriser le batch, et indiquer la formulation — retrait pur (comme le prototype PR #240, mergé) ou phrase de remplacement.
⚠️ **À recompter par script en début de prochain run** (le chiffre 73 date du 06/08 et n'a pas été revérifié ce run).

### (b) FAQ vide — ~816 fichiers
Une purge R145 antérieure a laissé des `acceptedAnswer` cassées dans le JSON-LD `FAQPage` sur « Quanto tempo demoram a chegar? » — dont **809** valant `" conforme zona"` (commence par une espace, sans sujet ni verbe).
🔎 **SOURCE IDENTIFIÉE ce run, côté `eletricista-urgente`, et elle vaut ici** : ce ne sont **pas** les générateurs de pages, ce sont les **scripts de purge eux-mêmes**. Sur EU, `scripts/r12_blog_safe_cleanup.py` L49-50 remplace par **`"Deslocação conforme zona Z"`** et `scripts/r12_hubs_cleanup.py` L37-45 par **`"< Deslocação conforme zona tarifária Z"`** — la chaîne de remplacement **se termine par un `Z` orphelin**, le numéro de zone n'étant jamais concaténé. **C'est un fragment de gabarit inachevé.** ➡️ **Vérifier si les mêmes scripts (ou leurs jumeaux) existent sur CU** — s'ils sont one-shot et non un build, **un batch sur les 816 fichiers ne sera pas annulé au prochain déploiement**.
**Décision demandée** : autoriser le batch. ⚠️ Traiter les 4 variantes séparément et **re-parser le `FAQPage` de chaque fichier après patch** — c'est le contrôle manquant qui a créé le gisement.

## Tâche suivante recommandée
1. **Chercher sur CU les jumeaux de `r12_blog_safe_cleanup.py` / `r12_hubs_cleanup.py`** (audit lecture seule, sans GO) et vérifier s'ils régénèrent ou non. C'est ce qui conditionne le GO batch (b).
2. **Recompter par script les 2 gisements** (a) et (b), avec **contrôle positif** obligatoire, et comparer aux chiffres ci-dessus. Un gisement qui ne diminue pas malgré un merge = quelque chose le régénère.
3. Sinon : **méthode d'audit par point d'entrée** adaptée au statique — auditer les pages les plus crawlées (`index.html`, `precos.html`, `calculadora-de-preco.html`, `perguntas-frequentes.html`, `zona-intervencao.html`) plutôt que le repo entier.

## Apprentissages (self-improving)
- 🔴 **NOUVEAU, et c'est la leçon la plus importante du run sur les 4 repos — un batch de conformité peut corrompre la RÈGLE qu'il applique.** `fb9dd2415` a substitué dans `AGENTS.md` en même temps que dans les 2003 pages, et a **désarmé le ruling** tout en croyant l'appliquer. ➡️ **Règle : tout batch de substitution doit exclure explicitement `AGENTS.md`, `SEO_PLAN.md`, `context.md`, `CLAUDE.md`.** Les fichiers de doctrine ne sont jamais des cibles de purge de contenu.
- 🔴 **NOUVEAU — une contradiction dans une règle verrouillée doit être traitée comme une CORRUPTION jusqu'à preuve du contraire, pas comme un arbitrage à demander.** Le réflexe « demander à Philippe de trancher » a coûté **5 semaines** ici, là où `git log -S` donnait la réponse en une commande. ➡️ **Avant d'escalader une contradiction de doctrine : `git log -S "<fragment>" -- AGENTS.md`.**
- 🔴 **Corollaire : un « claim » qui met 2 427 fichiers sur 2 452 en violation n'est pas une règle, c'est un bug.** L'ordre de grandeur est en soi un signal de diagnostic. Quand une règle condamne la quasi-totalité du site, suspecter la règle avant le site.
- **Le même mécanisme de substitution hors contexte explique les artefacts des autres repos** : « Eletricista precisa de **Orçamento por escrito**? » (ENR, corrigé PR #307 ce run), « Desligue o disjuntor geral **mediante confirmação** » (ENR — **contresens de sécurité**), « Técnico **Atendimento 24h** » (CNR, PR #280).
- 🔴 **Tout grep à motif non-ASCII (`€`, accents, guillemets imbriqués) passe par un script Python/bash, jamais une boucle inline `zsh -c`** — le motif est mangé et renvoie 0. Ce piège a produit un faux négatif documenté (`130 EUR` annoncé à 0, réalité 66 fichiers).
- 🔴 **Ne jamais faire confiance à un audit « 0 occurrence » sans CONTRÔLE POSITIF.** Greper un motif dont on sait qu'il est présent pour prouver que la commande fonctionne.
- **R145 autorise « 24h/7 dias » sur ce site** (AGENTS.md L125/L166). Ce qui est banni : les promesses de délai personnalisées (« resposta prioritária », « mediante confirmação por telefone »). ⚠️ C'est **l'inverse** des sites `*-norte-reparos`. **Ne pas purger « 24h » ici par réflexe.**
- Le grep `24h/7d` (sans espaces) **rate** les variantes réelles : `24h/7`, `24 h/7 dias`. Utiliser `24\s*h[/ ]`.
- **Toute purge de conformité doit re-parser le JSON-LD après coup** et vérifier que chaque `acceptedAnswer.text` fait > 20 caractères. ⚠️ Ne pas exiger « commence par une majuscule » : une réponse légitime peut commencer par un chiffre.
- 🔴 **Corollaire nouveau : la chaîne de REMPLACEMENT d'un script de purge doit être une phrase complète et testée sur un échantillon**, jamais un fragment de gabarit. C'est un `"…zona Z"` inachevé qui a produit des centaines de réponses vides.
- Ce repo est un site **statique pur** : pas de `package.json`, pas de build, `vercel.json` en rewrites. Pas de `tsc` — vérification par grep + **re-parsing JSON**.
- Ce site utilise « 65 € » (avec espace) et « 65 EUR », pas seulement « 65€ » → adapter les greps R8.

## Edge cases détectés
- **Worktree obligatoire** : la copie de travail est sale en permanence et posée sur une branche feature d'une autre automation. **Jamais `git checkout`, `reset --hard`, `stash` ni `clean`** (R-WT).
- **Le `/tmp` du sandbox ≠ le `/tmp` du host.** Worktrees sous `~/work/Sites/_worktrees/` (monté des deux côtés).
- **Les commandes `git` ne fonctionnent PAS depuis le sandbox dans un worktree** (le `.git` contient un chemin absolu host). Dans un worktree : grep/lecture au sandbox, **tout `git` via desktop-commander**.
- 🔴 **Ce checkout porte régulièrement des `.git/*.lock` et `.git/objects/maintenance.lock` orphelins**, non supprimables depuis le sandbox (permissions). Pré-flight **host-side** obligatoire.
- 🔴 **`set -e` + zsh : un glob sans correspondance (`rm -f .git/*.lock`) fait AVORTER tout le script.** Utiliser `setopt null_glob`.
- Le sandbox n'a ni `gh` ni credentials Git en écriture → tout git/gh via `mcp__desktop-commander__start_process`. Il est en revanche **excellent** pour les grep/scripts sur les ~2452 fichiers HTML montés.
- `mcp__workspace__web_fetch` **refuse les URL non présentes dans la conversation** (« URL not in provenance set ») → impossible de vérifier le HTML servi en prod depuis le loop. Pour trancher le doublon `public/`, il faut un `curl` host-side.
- `_archive/` contient de vieux fichiers avec violations — **NE PAS patcher `_archive/`**, l'exclure de tous les greps.
- `calculadora-de-preco.html` : zones décalées vs AGENTS.md (Z1=20 € dans le JS vs 15 €) — écart possiblement intentionnel (urgence ≠ normal). **NE PAS toucher la logique JS sans GO.**
- Corps de PR long : fichier + `gh pr create --body-file`, jamais `--body` inline.

## Blocages connus
1. **Gisement (a) `Desde 130`** = 🛑 attente GO batch. **Le plus urgent du repo.**
2. **Gisement (b) FAQ vide (~816 fichiers)** = 🛑 attente GO batch. Verrou technique **probablement levé** (voir §(b)), à confirmer côté CU.
3. **A1** (refonte homepage Doctrine §12) = 🛑 STOP attente Philippe depuis le 28/06.
4. **A2** (8 pages /zonas/) = 🛑 STOP attente GO explicite.
5. **Doublon `public/` ↔ racine — 99 fichiers.** `vercel.json` ne déclare **ni `outputDirectory` ni `buildCommand`**, pas de `package.json` → Vercel peut servir la racine **ou** auto-détecter `public/`. **Décision demandée** : (a) `public/` est-il déployé ou mort ? (b) si mort → le supprimer (99 fichiers dupliqués = risque SEO) ; (c) si vivant → quel fichier fait foi ?
6. « **resposta imediata** » dans le H1 racine : R145 bannit « resposta prioritária » et « mediante confirmação » mais pas littéralement celle-ci. Même famille sémantique. **Décision demandée.**
7. **Le tableau d'audit « 11 motifs, 0 occurrence » du 29/07 est SUSPECT EN ENTIER** (faux négatif de grep non-ASCII) — à refaire par script avant de s'y fier.

## Instructions améliorées pour prochain run
1. **Pré-flight host-side** : `setopt null_glob` puis `rm -f ~/work/Sites/canalizador-urgente/.git/*.lock ~/work/Sites/canalizador-urgente/.git/objects/*.lock`.
2. **Worktree obligatoire** : `git worktree add -q ~/work/Sites/_worktrees/loop-YYYY-MM-DD/cu -b loop/YYYY-MM-DD-canalizador-urgente-{tache} origin/main`. **Jamais `/tmp`, jamais la copie principale, jamais `reset --hard`/`stash`/`clean`.**
3. **Recompter les 2 gisements par script Python** (motifs non-ASCII) **avec contrôle positif**, et comparer aux chiffres ci-dessus.
4. **Chercher les jumeaux des scripts de purge** (`r12_*`) sur ce repo — one-shot ou build ? C'est ce qui conditionne le GO batch (b).
5. **Ne PAS purger « 24h » sur ce site** — R145 l'autorise.
6. **Avant d'escalader une contradiction de doctrine : `git log -S "<fragment>" -- AGENTS.md`.**
7. Après tout patch d'un JSON-LD : **re-parser TOUS les blocs `application/ld+json`** et vérifier chaque `acceptedAnswer.text` (> 20 caractères).
8. **Vérifier que `context.md` est arrivé sur `main`** : `git show origin/main:context.md | head -6` doit afficher la date du jour.
9. Nettoyer : `git worktree remove …` puis `git worktree prune`. Si le retrait échoue, laisser en place et le signaler — ne jamais forcer.
