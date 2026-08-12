# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-12
- Tâches exécutées : **n°1 (chercher les jumeaux des scripts de purge) et n°2 (recompter les 2 gisements par script, avec contrôle positif)** du `context.md` du 11/08 — les deux qui conditionnent le GO batch.
- Branche : `loop/2026-08-12-canalizador-urgente-audit-gisements` (depuis `origin/main`, **en worktree**)
- PR ouverte : https://github.com/taffrand-gif/canalizador-urgente/pull/256
- Résultat : ✅ **Audit pur — aucune page de production modifiée**, seul `SEO_PLAN.md` change (+72 / −0). 2 452 fichiers HTML scannés, `_archive/` exclu. **Verrou technique levé. Et la cible du batch FAQ annoncée était fausse — elle est corrigée.**

## ✅ RÉSOLU ce run n°1 — verrou technique levé, comme sur EU

Les jumeaux existent, et ils sont **trois** (pas deux) : `scripts/r12_blog_safe_cleanup.py` L54, `scripts/r12_hubs_cleanup.py` L51, **`scripts/r12_mass_cleanup_pass2.py` L57** — tous porteurs de la même chaîne défectueuse **`"Deslocação conforme zona Z"`**, terminée par un `Z` orphelin.

**One-shot, pas une étape de build**, établi par trois contrôles convergents :

- aucune référence à `r12_` dans un `.json` / `.yml` / `.yaml` / `.sh` / `.toml` du repo : **0 résultat**
- **pas de `package.json`**, **pas de `.github/`**
- `vercel.json` = `rewrites` + `headers` seuls, **ni `buildCommand` ni `outputDirectory`**

➡️ **Un batch sur les pages ne sera PAS annulé au prochain déploiement. Le blocage n°2 tombe.**

## 🔴 RÉSOLU ce run n°2 — et c'est le résultat qui change tout : la cible du batch était fausse

| Motif | Occurrences | Fichiers |
|---|---:|---:|
| **CONTRÔLE POSITIF** `65 €` / `65 EUR` | 12 904 | 2 237 |
| `conforme zona Z` (le `Z` orphelin **des scripts**) | **0** | **0** |
| `demoram a chegar` | 816 | **815** |
| ` conforme zona` | 1 173 | 1 159 |
| `Desde 130` | 137 | **73** |
| `130 €` toutes formes | 147 | 80 |

**Les 3 scripts du repo sont armés mais n'ont jamais tiré** : leur `Z` orphelin a **0 occurrence** en production. Le défaut réel vient d'une **4ᵉ passe de purge absente de `scripts/`** — vraisemblablement une commande ad hoc. **Elle n'est donc pas reproductible : le gisement est figé, donc sûr à purger.**

⚠️ **Le diagnostic EU du 11/08 était juste pour EU et faux pour CU.** Ne pas transposer une causalité d'un repo à l'autre sans la vérifier en production.

### Gisement (b) caractérisé au fichier près — et il est plus petit qu'annoncé

Parsing de **tous** les blocs `application/ld+json` des 815 fichiers portant la question :

| `acceptedAnswer.text` | Fichiers |
|---|---:|
| `" conforme zona"` (14 car., espace initiale, ni sujet ni verbe) | **808** |
| `"min conforme zona. Diagnóstico por telefone…"` (`min` orphelin) | 5 |
| `"5 - atendimento urgente conforme zona…"` (`5 -` orphelin) | 1 |
| réponse valide | 1 |

**Blocs JSON-LD non parsables : 0.** Le JSON est syntaxiquement valide — il est sémantiquement vide.

🔴 **Le motif ` conforme zona` NE DOIT PAS servir de cible de batch.** Sur les 1 159 fichiers qui le portent, **1 138 ne l'ont que dans le JSON-LD** ; les **21** qui l'ont aussi dans le body l'ont dans une phrase **légitime et grammaticale** : « com resposta conforme zona e disponibilidade da equipa ». **Un `sed` sur ce motif casserait 21 pages correctes.**

➡️ **Cible exacte du batch : les `acceptedAnswer.text` dont la valeur strippée vaut exactement `conforme zona` — 808 fichiers, zéro faux positif.** Les 3 variantes résiduelles (5 + 1) se traitent séparément.

## ✅ Gate merge — aucun gate actif
Vérifié au run du 11/08 : #240 (CU), #269 (CNR), #295 (ENR), #200 (EU) **toutes MERGED**. Aucun gate réécrit ce run.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Entre le 06/08 et le 09/08, cette mention a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**.

## 🛑 GISEMENTS CHIFFRÉS — DÉCISIONS REQUISES (3 taps)

### (a) Prix inventé `Desde 130` — **73 fichiers** (137 occurrences) ⚠️ LE PLUS URGENT
Chiffre du 06/08 **confirmé au fichier près** ce run. Rien ne l'a purgé, rien ne le régénère. `PRICING-CANONIQUE.md` ne connaît **aucun** minimum de 130 € (grille : 65 €/h + deslocação Z1-Z6 de 15 € à 65 €). Le « 130 » est le **rayon en km** autour de Macedo de Cavaleiros — pas un prix.
**Décision** : autoriser le batch, et indiquer la formulation — retrait pur (patron PR #240, mergé) ou phrase de remplacement.

### (b) FAQ vide — **808 fichiers** (et non ~816, et surtout pas 1 159)
Verrou technique levé, cible désormais sans ambiguïté (voir ci-dessus).
**Décision** : autoriser le batch. ⚠️ Traiter les 3 variantes résiduelles séparément et **re-parser le `FAQPage` de chaque fichier après patch** (`acceptedAnswer.text` > 20 caractères) — c'est le contrôle manquant qui a créé le gisement.

### (c) 🆕 `a a  profissionais` — **34 fichiers** (101 occurrences)
⚠️ **La PR #254 — mergée, et c'est le HEAD de `main` — n'a traité que 14 fichiers.** Le gisement n'est pas clos.
**Décision** : autoriser la finition sur les 34 restants.

### 🆕 Résidu mesuré en passant
`mediante confirmação por telefone/7d` — **37 occurrences / 15 fichiers**. Le `24h` a été substitué en laissant son suffixe `/7d` orphelin. Même famille d'artefact, à traiter avec (c).

⚠️ Rappel appliqué à ces batchs : **exclure explicitement `AGENTS.md`, `SEO_PLAN.md`, `context.md`, `CLAUDE.md`** des substitutions (leçon `fb9dd2415`).

## Tâche suivante recommandée
1. **Si GO (a) ou (b) ou (c)** : exécuter le batch correspondant. Les trois cibles sont désormais chiffrées et sans ambiguïté — **il ne manque que le GO.**
2. **Sans GO** : appliquer la méthode du **parsing plutôt que du grep** aux autres gisements du repo (voir Apprentissages) — commencer par re-vérifier que les autres PR mergées ont bien clos leur gisement, comme #254 ne l'a pas fait.
3. **Sans GO** : audit par point d'entrée des pages les plus crawlées (`index.html`, `precos.html`, `calculadora-de-preco.html`, `perguntas-frequentes.html`, `zona-intervencao.html`).

## Apprentissages (self-improving)
- 🔴 **NOUVEAU — un script cassé dans le repo n'est PAS la preuve qu'il a produit le défaut.** Ici les 3 scripts portent un `Z` orphelin qui a **0 occurrence** en production, tandis que le vrai défaut (` conforme zona`) ne vient d'aucun script versionné. ➡️ **Toujours vérifier que la chaîne défectueuse du script existe réellement en production avant de conclure à la causalité.**
- 🔴 **NOUVEAU — ne jamais dériver une cible de batch d'un `grep` ; la dériver du PARSING.** ` conforme zona` = 1 159 fichiers dont 21 parfaitement légitimes ; le champ parsé donne **808** fichiers et zéro faux positif. **Un écart de 351 fichiers entre le grep et la vérité** — c'est-à-dire entre un batch destructeur et un batch sûr.
- 🔴 **NOUVEAU — vérifier qu'une PR mergée a bien CLOS son gisement.** `a a  profissionais` : la PR #254 annonçait 14 fichiers, il en reste **34**. **Un merge n'est pas une clôture.** ➡️ **Contrôle à ajouter en début de run : recompter le gisement de la dernière PR mergée.**
- 🔴 **Un batch de conformité peut corrompre la RÈGLE qu'il applique.** `fb9dd2415` a substitué dans `AGENTS.md` en même temps que dans 2 003 pages et a **désarmé le ruling** tout en croyant l'appliquer. ➡️ **Tout batch de substitution doit exclure explicitement `AGENTS.md`, `SEO_PLAN.md`, `context.md`, `CLAUDE.md`.**
- 🔴 **Une contradiction dans une règle verrouillée doit être traitée comme une CORRUPTION jusqu'à preuve du contraire, pas comme un arbitrage à demander.** Le réflexe « demander à Philippe » a coûté **5 semaines** là où `git log -S` répondait en une commande.
- 🔴 **Un « claim » qui met 2 427 fichiers sur 2 452 en violation n'est pas une règle, c'est un bug.** L'ordre de grandeur est en soi un signal de diagnostic.
- 🔴 **Tout grep à motif non-ASCII passe par un script Python**, jamais une boucle inline `zsh -c` — le motif est mangé et renvoie 0.
- 🔴 **Ne jamais faire confiance à un audit « 0 occurrence » sans CONTRÔLE POSITIF.** Ce run : `65 €` = 12 904 occ / 2 237 fichiers, donc les 808 / 815 / 73 sont de vrais chiffres.
- **Toute purge de conformité doit re-parser le JSON-LD après coup** et vérifier que chaque `acceptedAnswer.text` fait > 20 caractères. ⚠️ Ne pas exiger « commence par une majuscule » : une réponse légitime peut commencer par un chiffre.
- **R145 autorise « 24h/7 dias » sur ce site** (AGENTS.md L125/L166). Ce qui est banni : les promesses de délai personnalisées. ⚠️ C'est **l'inverse** des sites `*-norte-reparos`. **Ne pas purger « 24h » ici par réflexe.**
- Le grep `24h/7d` (sans espaces) **rate** les variantes réelles : `24h/7`, `24 h/7 dias`. Utiliser `24\s*h[/ ]`.
- Ce repo est un site **statique pur** : pas de `package.json`, pas de build, `vercel.json` en rewrites. Pas de `tsc` — vérification par grep + **re-parsing JSON**.
- Ce site utilise « 65 € » (avec espace) et « 65 EUR », pas seulement « 65€ » → adapter les greps R8.

## Edge cases détectés
- **Worktree obligatoire** : la copie de travail est sale en permanence et posée sur une branche feature d'une autre automation. **Jamais `git checkout`, `reset --hard`, `stash` ni `clean`** (R-WT).
- **Le `/tmp` du sandbox ≠ le `/tmp` du host.** Worktrees sous `~/work/Sites/_worktrees/`.
- **Les commandes `git` ne fonctionnent PAS depuis le sandbox dans un worktree** (le `.git` contient un chemin absolu host). Dans un worktree : grep/lecture au sandbox, **tout `git` via desktop-commander**.
- ⚠️ **Le sandbox ne peut pas supprimer les `.git/objects/*.lock`** (« Operation not permitted ») — `git fetch` émet des warnings d'unlink mais **réussit**. Pré-flight host-side quand même.
- 🔴 **`set -e` + zsh : un glob sans correspondance fait AVORTER tout le script.** Utiliser `setopt null_glob`.
- Le sandbox n'a ni `gh` ni credentials Git → tout git/gh via `mcp__desktop-commander__start_process`. Il est en revanche **excellent et rapide** pour les scripts Python sur les 2 452 fichiers HTML montés (le scan complet + parsing JSON-LD tient en quelques secondes).
- `mcp__workspace__web_fetch` **refuse les URL non présentes dans la conversation** → impossible de vérifier le HTML servi en prod depuis le loop. Pour trancher le doublon `public/`, il faut un `curl` host-side.
- `_archive/` contient de vieux fichiers avec violations — **NE PAS patcher**, l'exclure de tous les greps.
- `calculadora-de-preco.html` : zones décalées vs AGENTS.md (Z1 = 20 € dans le JS vs 15 €) — écart possiblement intentionnel (urgence ≠ normal). **NE PAS toucher la logique JS sans GO.**
- Corps de PR long : fichier + `gh pr create --body-file`, jamais `--body` inline.

## Blocages connus
1. **Gisement (a) `Desde 130` — 73 fichiers** = 🛑 attente GO batch. **Le plus urgent du repo.**
2. **Gisement (b) FAQ vide — 808 fichiers** = 🛑 attente GO batch. **Verrou technique levé, cible sans ambiguïté.**
3. **Gisement (c) `a a  profissionais` — 34 fichiers restants** = 🛑 attente GO.
4. **A1** (refonte homepage Doctrine §12) = 🛑 STOP attente Philippe depuis le 28/06.
5. **A2** (8 pages /zonas/) = 🛑 STOP attente GO explicite.
6. **Doublon `public/` ↔ racine — 99 fichiers.** `vercel.json` ne déclare ni `outputDirectory` ni `buildCommand`, pas de `package.json` → Vercel peut servir la racine **ou** auto-détecter `public/`. **Décision** : (a) `public/` est-il déployé ou mort ? (b) si mort → le supprimer (99 fichiers dupliqués = risque SEO) ; (c) si vivant → quel fichier fait foi ? **Même question ouverte sur EU — un seul arbitrage débloque les 2 repos.**
7. « **resposta imediata** » dans le H1 racine : R145 bannit « resposta prioritária » et « mediante confirmação » mais pas littéralement celle-ci. Même famille sémantique. **Décision demandée.**
