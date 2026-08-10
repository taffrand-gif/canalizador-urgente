# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-06
- Tâche exécutée : **R11 + R145 — violation détectée en lecture, traitée en priorité (R11/R12).** Les 2 tâches prévues du `SEO_PLAN` (A1, A2) restent 🛑 STOP-gatées, non touchées. **PROTOTYPE SUR 1 SEULE PAGE** (AGENTS.md §12) sur `calculadora-de-preco.html` — **le même fichier que le prototype PR #200 sur `eletricista-urgente`, qui est MERGÉE**, donc le pattern de retrait est déjà validé par Philippe.
- Branche créée : `loop/2026-08-06-canalizador-urgente-r11-r145-prototype` (depuis `origin/main`, **en worktree**)
- Commits : `9614d3f75` (calculadora-de-preco.html), puis `38fe02516` (SEO_PLAN.md HISTORIQUE)
- PR ouverte : https://github.com/taffrand-gif/canalizador-urgente/pull/240
- Résultat : ✅ 2 commits, 2 fichiers (1 par commit, atomique). **3 défauts corrigés, tous par retrait ou réparation d'artefact, zéro invention.** Témoins R8 : `demoram a chegar` 1→0 · `" conforme zona"` 1→0 · `começa em 130 EUR` 1→0 · `130 EUR` 1→0 · `Trabalham Atendimento — ligue 928 484 451/7d?` 1→0 · `Trabalham 24h/7d?` 0→1 · `Mão de obra: 65 EUR/h` 1→1 (conservé) · `24h/7d` 5→5 (conservé, R145 l'autorise ici). Delta −165 octets. **Tous les blocs JSON-LD re-parsés = valides**, `FAQPage` 5→4 questions toutes avec réponse réelle. Attente GO merge + GO batch Philippe (R7).

## 🛑 2 GISEMENTS CHIFFRÉS — DÉCISION REQUISE

### (a) Prix inventé `Desde 130` — **73 fichiers** ⚠️ LE PLUS URGENT
`Desde 130` sur **73 fichiers**, `130 EUR` sur **66**, `130€` sur 18, `130 €` sur 7.
`PRICING-CANONIQUE.md` ne connaît **aucun minimum de 130 €** : la grille verrouillée est **65 €/h + deslocação Z1=15 € · Z2=25 € · Z3=35 € · Z4=45 € · Z5=55 € · Z6=65 €**. Le « 130 » des documents internes désigne le **rayon de 130 km** autour de Macedo de Cavaleiros — **pas un prix**.
➡️ **C'est un prix faux servi en production sur ~73 pages.** Violation R11 active. Priorité au-dessus de (b).
**Décision demandée** : autoriser le batch, et indiquer la formulation retenue — retrait pur (comme dans le prototype) ou une phrase de remplacement choisie par Philippe.

### (b) FAQ vide — **816 fichiers** (le gisement d'`eletricista-urgente` existe aussi ici)
Le `context.md` d'EU demandait de vérifier ce défaut ici. **Vérifié, il y est.** Une purge R145 antérieure a laissé des `acceptedAnswer` cassées dans le JSON-LD `FAQPage`, sur la question « Quanto tempo demoram a chegar? » :

| Occurrences | Valeur de `text` |
|---|---|
| 809 | `" conforme zona"` — vide : commence par une espace, sans sujet ni verbe |
| 5 | `" min conforme zona. Diagnóstico por telefone em poucos minutos — ligue 928 484 451, atenção dedicada orçamento por escrito por telefone ao telefone."` |
| 1 | `"Diagnóstico por telefone em poucos minutos — … Tempo conforme zona e disponibilidade da equipa."` |
| 1 | `"5 - atendimento urgente conforme zona. Atendimento urgente ao telefone."` |

**Pourquoi la réponse n'est pas réparable** : la question porte sur un **délai d'arrivée**. R145 interdit le délai chiffré, R11 interdit d'inventer, « mediante confirmação por telefone » est banni → **aucune réponse honnête ET conforme n'existe**. Retrait du couple Q/R = seule issue. Le vide honnête > le faux.
**Décision demandée** : autoriser (ou non) le batch sur les 815 fichiers restants. ⚠️ Traiter les 4 variantes séparément et **re-parser le `FAQPage` de chaque fichier après patch** — c'est le contrôle manquant qui a créé le gisement.

## ✅ RÉSOLU ce run — point d'escalade #2 (« orçamento por escrito »)
La contradiction **AGENTS.md §13 (gabarit, verrouillé 15/06) vs ruling Filipe 2026-07-08** est **tranchée dans la pratique** : l'entrée `SEO_PLAN.md` du 2026-08-04 (PR #229) applique explicitement *« R12 … règle postérieure 2026-07-08 respectée (`preço confirmado antes de qualquer intervenção`, zéro `orçamento por escrito`) »*.
➡️ **Le ruling prime sur le gabarit §13.** Formule de remplacement validée : **`preço confirmado antes de qualquer intervenção`**.
➡️ **TÂCHE SUIVANTE RECOMMANDÉE** : reporter ce ruling dans `AGENTS.md` §13 (1 fichier = 1 PR, sans risque) pour supprimer l'ambiguïté définitivement — sinon chaque run repaiera le coût de l'arbitrage. Puis grep `orçamento por escrito` sur ce repo et purger vers la formule validée (chantier à chiffrer avant GO).
⚠️ Attention : sur les sites `*-norte-reparos`, « Orçamento por escrito em 48h » est au contraire le **vocabulaire validé** (`shared/siteConfig.ts` L108/L124). **La même formule est bannie ici et prescrite là-bas.**

## Tâche suivante recommandée
1. **`AGENTS.md` §13 — reporter le ruling 2026-07-08** (voir ci-dessus). 1 fichier, risque nul, débloque tous les runs futurs.
2. Si GO sur le gisement (a) : batch `Desde 130` / `130 EUR` sur 73 fichiers.
3. Si GO sur le gisement (b) : batch FAQ sur 815 fichiers.
4. Sinon : appliquer la **méthode d'audit par point d'entrée** (celle qui produit les PR utiles sur CNR/ENR) adaptée à un site statique — auditer les pages les plus crawlées (`index.html`, `precos.html`, `calculadora-de-preco.html`, `perguntas-frequentes.html`, `zona-intervencao.html`) plutôt que le repo entier.

## Apprentissages (self-improving)
- 🔴 **FAUX NÉGATIF D'AUDIT CONFIRMÉ ET REPRODUIT.** L'audit du 29/07 sur ce repo avait conclu **`130 EUR` → 0 occurrence**. La réalité est **66 fichiers**. C'est exactement le piège documenté le **même jour** dans le `context.md` d'`eletricista-urgente` : *« passer un motif contenant `€` à `git grep -F` via une boucle inline `zsh -c` mange le motif et renvoie 0 résultat »*. **Le piège s'est reproduit sur un autre repo parce que la leçon n'était consignée que dans un seul `context.md`.** ➡️ **Règle : tout grep à motif non-ASCII (`€`, accents, guillemets imbriqués) passe par un script Python/bash, jamais une boucle inline.** ➡️ **Méta-règle : une leçon de tooling vaut pour les 4 repos et doit être copiée dans les 4 `context.md` le jour où elle est apprise.**
- 🔴 **Ne jamais faire confiance à un audit « 0 occurrence » sans contrôle positif.** Avant de conclure qu'un motif est absent, greper un motif **dont on sait qu'il est présent** pour prouver que la commande fonctionne. Le tableau « 11 motifs, 0 occurrence » du 29/07 est désormais suspect **en entier** — il devra être refait par script.
- **R145 autorise « 24h/7 dias » sur ce site** (AGENTS.md L125/L166). Ce qui est banni, ce sont les promesses de délai personnalisées (« atendimento prioritário », « mediante confirmação por telefone »). ⚠️ C'est **l'inverse** des sites `*-norte-reparos` (installation) où « 24h » est une violation R12 par cannibalisation d'intent. **La même chaîne est violation sur 2 sites et conforme sur les 2 autres.** Ne pas purger « 24h » ici par réflexe.
- Le grep `24h/7d` (sans espaces) **rate** les variantes réelles du site : `24h/7`, `24 h/7 dias`. Utiliser `24\s*h[/ ]`.
- **Les artefacts des purges automatisées touchent aussi les `name` de questions**, pas seulement les réponses. Ex. trouvé ce run : `"Trabalham Atendimento — ligue 928 484 451/7d?"` (numéro injecté au milieu de « Atendimento 24h/7d »). Ils sont **grammaticalement cassés**, donc les corriger n'invente rien — gisement propre à faible risque.
- **Toute purge de conformité doit re-parser le JSON-LD après coup** : retirer une sous-chaîne d'un `acceptedAnswer` produit du JSON syntaxiquement valide mais **sémantiquement vide**, qu'aucun linter ne détecte. C'est précisément ce contrôle manquant qui a créé le gisement de 816 fichiers. Contrôle à ajouter à tout batch : re-parser chaque bloc `FAQPage`, vérifier que chaque `text` fait > 20 caractères. ⚠️ Ne pas ajouter « commence par une majuscule » comme critère bloquant : une réponse légitime peut commencer par un chiffre (« 65 €/h + deslocação… »).
- Ce repo est un site **statique pur** : pas de `package.json`, pas de build, `vercel.json` en rewrites `/(.*)` → `/$1.html`. Pas de `tsc` possible — la vérification post-patch se fait par grep + **re-parsing JSON**.
- Ce site utilise « 65 € » (avec espace) et « 65 EUR », pas seulement « 65€ » → adapter les greps R8.
- **Les corrections ne sont PAS propagées entre repos, et les LEÇONS non plus.** C'est le pattern le plus coûteux du cycle, observé 3 fois : `seo.keywords` (14 j), `FAQLocal.tsx` (6 j), et maintenant le piège de grep `€` (jamais propagé → a produit un faux négatif ici).

## Edge cases détectés
- **Worktree obligatoire sur ce repo** : la copie de travail est sale en permanence (6 fichiers au 06/08) et posée sur une branche feature d'une autre automation (`fix/cu-conformite-phones-recursos-gratuitos-t_6220b236`). Ne jamais y faire `git checkout` ni `reset --hard`. Patron : `git worktree add -q ~/work/Sites/_worktrees/loop-YYYY-MM-DD/cu -b <branche> origin/main`.
- 🔴 **Le `/tmp` du sandbox et le `/tmp` du host sont DEUX systèmes de fichiers distincts.** Un worktree créé dans `/tmp` via desktop-commander est **invisible** au sandbox. Les worktrees doivent être créés **sous `~/work/Sites/`** (monté des deux côtés).
- 🔴 **Les commandes `git` ne fonctionnent PAS depuis le sandbox dans un worktree** : le fichier `.git` d'un worktree contient un chemin **absolu host** qui ne résout pas côté sandbox → `fatal: not a git repository`. Dans un worktree : grep/lecture au sandbox, **tout `git` via desktop-commander**.
- Le sandbox `mcp__workspace__bash` n'a ni `gh` ni credentials Git en écriture → tout git/gh passe par `mcp__desktop-commander__start_process` (host macOS, `gh` authentifié `taffrand-gif`). En revanche il est **excellent et rapide** pour tous les grep/lecture sur les 2452 fichiers HTML montés.
- `mcp__workspace__web_fetch` **refuse les URL non présentes dans la conversation** (« URL not in provenance set ») → impossible de vérifier le HTML servi en prod depuis le loop. Pour trancher le doublon `public/`, il faut un `curl` host-side via desktop-commander.
- `_archive/` contient de vieux fichiers avec violations — **NE PAS patcher `_archive/`**, et l'exclure de tous les greps d'audit.
- `calculadora-de-preco.html` : zones décalées vs AGENTS.md (Z1=20 € dans le calculateur JS vs 15 € dans AGENTS) — écart possiblement intentionnel (urgence ≠ normal). **NE PAS toucher la logique JS sans GO Philippe.** Non touché ce run (seul le JSON-LD a été patché).
- Corps de PR long : `cat > /tmp/pr-xxx.md <<'EOF'` puis `gh pr create --body-file`, jamais `--body` inline.

## Blocages connus
1. **Gisement (a) `Desde 130` — 73 fichiers, prix faux en production** = 🛑 attente GO batch. **Le plus urgent du repo.**
2. **Gisement (b) FAQ vide — 816 fichiers** = 🛑 attente GO batch (prototype ci-dessus + PR #200 mergée sur EU comme précédent).
3. **A1** (refonte homepage Doctrine §12) = 🛑 STOP attente Philippe depuis le 28/06.
4. **A2** (8 pages /zonas/) = 🛑 STOP attente GO explicite.
5. **Doublon `public/` ↔ racine — 99 fichiers.** `./index.html` et `public/index.html` ont divergé dans les deux sens (racine = maillage blog récent + H1 ancien ; `public/` = H1 conforme §13 + pas de maillage). Source de vérité indéterminable : `vercel.json` ne déclare **ni `outputDirectory` ni `buildCommand`**, il n'y a **pas de `package.json`** — déploiement statique zéro-config, Vercel peut servir la racine **ou** auto-détecter `public/`. **Décision demandée** : (a) `public/` est-il déployé ou mort ? (b) si mort → le supprimer (99 fichiers de contenu dupliqué = risque SEO) ; (c) si vivant → quel fichier fait foi ?
6. « **resposta imediata** » dans le H1 racine : R145 bannit « atendimento prioritário » et « mediante confirmação » mais pas littéralement « resposta imediata ». Même famille sémantique. Ambigu → non touché. **Décision demandée.**
7. Zones tarif du calculateur JS vs AGENTS.md (Z1=20 € vs 15 €) : ambiguïté, laissé en place.
8. **Le tableau d'audit « 11 motifs, 0 occurrence » du 29/07 est SUSPECT EN ENTIER** (voir §Apprentissages) — à refaire par script avant de s'y fier.
9. 5 PR ouvertes sur ce repo au 06/08 (#228, #231, #232, #238, #239) + **#240 (ce run)**. Sur les 4 repos cumulés : **60 PR ouvertes**. Le goulot est le merge, pas la production.

## Instructions améliorées pour prochain run
1. 🔴 **Pré-flight** : `rm -f ~/work/Sites/canalizador-urgente/.git/*.lock` (zsh dit « no matches found » s'il n'y en a pas — normal).
2. 🔴 **Travailler en worktree sous `~/work/Sites/`** : `git worktree add -q ~/work/Sites/_worktrees/loop-YYYY-MM-DD/cu -b loop/YYYY-MM-DD-canalizador-urgente-{tache} origin/main`. Jamais `/tmp`, jamais la copie principale.
3. 🔴 **Tout grep à motif non-ASCII passe par un script Python/bash**, jamais une boucle inline `zsh -c`. Et **toujours un contrôle positif** (greper un motif connu présent) avant de conclure « 0 occurrence ».
4. **Ne PAS purger « 24h » sur ce site** — R145 l'autorise explicitement. C'est l'inverse des sites installation.
5. **Ne pas se fier au tableau d'audit du 29/07** : refaire par script.
6. Tâche suivante : **`AGENTS.md` §13 — reporter le ruling 2026-07-08** (1 fichier, risque nul), puis les batchs (a) et (b) si GO.
7. **Après tout patch d'un JSON-LD : re-parser TOUS les blocs `application/ld+json` du fichier** et vérifier que chaque `acceptedAnswer.text` fait > 20 caractères. C'est le contrôle qui manque aux purges automatisées.
8. **Répartition des outils** : grep/lecture/scripts d'analyse → `mcp__workspace__bash` ; git/gh/curl → `mcp__desktop-commander__start_process`.
9. PR : `cat > /tmp/pr-xxx.md <<'EOF'` + `gh pr create --body-file`.
10. 🔴 **Vérifier que `context.md` est bien arrivé sur `main`** en fin de run : `git show origin/main:context.md | head -6` doit afficher la date du jour.
11. Nettoyer : `git worktree remove ~/work/Sites/_worktrees/loop-YYYY-MM-DD/cu` puis `git worktree prune`.
12. Pour vérifier ce qui est servi en prod : `curl -sI https://canalizador-urgente.pt/` host-side (le web_fetch du sandbox est bloqué par la provenance).
