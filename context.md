# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-13
- Tâche exécutée : **tâche n°2 du `context.md` du 12/08 (« sans GO : re-vérifier que les PR mergées ont bien clos leur gisement »)**, puis **prototype sur une page**.
- Branche : `loop/2026-08-13-canalizador-urgente-r11-prototype-contactos` (depuis `origin/main`, **en worktree**)
- Commits : `d72432c0a` (`contactos.html`, JSON-LD), `b1deaf342` (`contactos.html`, corps de page), le commit `SEO_PLAN.md`
- PR ouverte : https://github.com/taffrand-gif/canalizador-urgente/pull/260 — **mergeable ✅**
- Résultat : ✅ 1 fichier de production. **Et le recompte a trouvé que la cible du batch prix était fausse d'un facteur 11.**

## 🔴 CE RUN — la cible du batch prix était fausse, et le batch avait DÉJÀ été lancé

Parsing des `acceptedAnswer.text` de la Question `« Quanto custa uma urgencia de canalizacao? »`, `_archive/` exclu :

| Variante en production | Fichiers | Verdict |
|---|---:|---|
| `sob orçamento por escritoEUR (1h) com deslocacao incluida. Suplemento 30-50% fora de horas.` | **698** | 🔴 **artefact de purge non documenté** |
| `Desde 130 EUR (1h) com deslocacao incluida. Suplemento 30-50% fora de horas.` | 64 | prix inventé, jamais purgé |
| `Sob orçamento por escrito. 65€/h + deslocação Z1-Z6 (15-65€). Suplemento 30-50% fora de horas..` | 52 | majoration inventée + double point |
| `65 €/h + deslocação (Z1: 15€ a Z6: 65€). Mínimo 1h. Acréscimo +50% fora de horas úteis.` | **1** | ✅ **conforme — source de vérité** |
| `Desde 130 EUR com deslocação incluída…` | 1 | prix inventé |
| `Orçamento prévio gratuito por telefone…` | 1 | « gratuito » banni (doctrine 11/08) |

- 🔴 **`por escritoEUR` — 698 fichiers.** Une purge a bien remplacé `Desde 130` par `sob orçamento por escrito`, **sans consommer le `EUR` qui suivait** → `por escritoEUR (1h)`. **Le batch prix a donc DÉJÀ été lancé, partiellement, et il a créé un gisement 9,5× plus grand que celui qu'il corrigeait.** Aucune trace dans `context.md` ni dans `scripts/`.
- 🔴 **La vraie cible n'est ni 73 ni 698 : c'est `Suplemento 30-50%` — 815 fichiers.** `PRICING.md` verrouille **+50 % ferme** (nuit / week-end / feriado) : la fourchette « 30-50 % » est **inventée sur les 815**, quelle que soit la variante de prix qui la précède. **C'est le surensemble qui contient les 3 défauts, et il n'avait jamais été mesuré.**
- Contrôles positifs : `65 €/h` = 5 441 occ / 2 119 fichiers · `deslocação` = 19 334 occ / 2 335 fichiers.

## ✅ Correction d'une conclusion du 12/08 — et confirmation que `a a  profissionais` est clos
- **` conforme zona` hors JSON-LD** : le `context.md` du 12/08 affirmait que les 21 fichiers concernés l'avaient « dans une phrase légitime et grammaticale ». **Vérifié fichier par fichier sur `origin/main` : vrai pour 20 sur 21.** L'exception unique est **`contactos.html`** — et c'est la page la plus à enjeu du lot (racine, money page) : « Resposta em **conforme zona** úteis », « (média ). Por email: **conforme zona** úteis ». ➡️ **Un échantillonnage juste à 95 % peut manquer exactement la page qui compte.**
- **`a a  profissionais` : 0 occurrence.** Le gisement signalé à 34 fichiers le 12/08 est **clos**. Ne pas le rouvrir.

## ✅ Gate merge — aucun gate actif
Vérifié ce run : aucune mention d'attente dans les 4 `context.md`. **CNR #300 a été mergée pendant le run** ; #260 (ici), #334 (ENR) et #284 (EU) sont ouvertes et **toutes mergeables**.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Entre le 06/08 et le 09/08, cette mention a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**.

## Prototype livré — `contactos.html`
Page choisie parce qu'elle porte **à elle seule les deux gisements** : le batch prix ET le batch FAQ se jugent sur un seul diff.
1. **Q « Quanto custa uma urgencia de canalizacao? »** → **transplant verbatim** de la réponse déjà en production sur `calculadora-de-preco.html` (même repo, même Question). **R4 : le « 130 » n'est pas un prix** — `PRICING.md` en fait le **rayon ROUTE maximal (~130 km)** depuis Macedo de Cavaleiros.
2. **Q « Quanto tempo demoram a chegar? »** → réponse `" conforme zona"` (14 car.) → **retrait du couple Q/R** (question de délai, patron validé par le merge de la PR #200, EU).
3. **Corps de page** → retrait des 2 fragments cassés. **Aucun délai reconstruit** : « 24 horas » n'est plus sourçable, le reconstruire violerait R4.
- Témoins R8 (avant → après) : `Desde 130` **1→0** · `Suplemento 30-50%` **1→0** · ` conforme zona` **3→0** · `Quanto tempo demoram a chegar` **1→0** · `(média )` **1→0** · `65 €/h` **0→1** · `24h/7d` **7→7** (**contrôle positif — R145 autorise `24h/7d` sur ce repo**, rien n'a été sur-purgé).
- Contrôle post-purge : **4/4 blocs JSON-LD re-parsés valides**, 2 questions, **0 `acceptedAnswer.text` < 20 caractères**.

## 🛑 GISEMENTS CHIFFRÉS — DÉCISIONS REQUISES (chiffres corrigés)

| # | Cible | Fichiers | Traitement |
|---|---|---:|---|
| **(a)** | `Suplemento 30-50%` → `Acréscimo +50% fora de horas úteis` | **815** | substitution déterministe, motif unique |
| (b) | `acceptedAnswer.text` == `conforme zona` (JSON-LD) | 808 | retrait du couple Q/R |
| (c) | `sob orçamento por escritoEUR` | 698 | **inclus dans (a)** si (a) réécrit la réponse entière |
| (d) | `Desde 130 EUR` | 73 | **inclus dans (a)** |
| (e) | `mediante confirmação por telefone/7d` (suffixe orphelin) | 15 | retrait du suffixe |

➡️ **(a) est le surensemble : un seul batch, une seule substitution, referme (c) et (d).** La PR #260 en montre le rendu exact sur une page.
⚠️ Rappel appliqué à ces batchs : **exclure explicitement `AGENTS.md`, `SEO_PLAN.md`, `context.md`, `CLAUDE.md`** (leçon `fb9dd2415`).

## Tâche suivante recommandée
1. **Si GO (a)** : exécuter le batch — un seul motif, zéro cas particulier, referme (c) et (d) d'un coup.
2. **Si GO (b)** : retrait du couple Q/R sur les 808, **puis re-parser le `FAQPage` de chaque fichier** (`acceptedAnswer.text` > 20 caractères) — c'est le contrôle manquant qui a créé le gisement.
3. **Sans GO** : appliquer la méthode du **parsing plutôt que du grep** aux autres Questions du `FAQPage`. Ce run n'a ventilé qu'**une seule** des questions ; les autres n'ont jamais été inventoriées. Commencer par `« Trabalham 24h/7d? »` et `« Quanto tempo demoram a chegar? »`.
4. **Sans GO** : auditer `StructuredData` / JSON-LD des points d'entrée les plus crawlés (`index.html`, `precos.html`, `calculadora-de-preco.html`, `perguntas-frequentes.html`, `zona-intervencao.html`) — c'est là qu'étaient les pires violations sur les 3 autres repos ce run.

## Apprentissages (self-improving)
- 🔴 **NOUVEAU — un batch de conformité partiellement appliqué laisse un gisement PLUS GRAND que celui qu'il corrigeait.** 73 → 698, parce que la substitution n'a pas consommé le token suivant (`EUR`). ➡️ **Toute substitution doit inclure le contexte droit dans son motif**, et **recompter les DEUX motifs — l'ancien ET le nouveau — après exécution.**
- 🔴 **NOUVEAU — chercher le SURENSEMBLE avant de demander un GO.** Trois runs ont demandé un GO sur `Desde 130` (73). Le motif qui contient réellement tout le gisement est `Suplemento 30-50%` (815) — jamais mesuré, parce que personne n'avait cherché ce que les variantes avaient **en commun**. ➡️ **Ventiler les variantes d'abord, isoler leur intersection, cibler l'intersection.**
- 🔴 **NOUVEAU — un échantillonnage à 95 % peut manquer la page qui compte.** 20 des 21 occurrences body étaient légitimes ; la 21ᵉ était la money page racine. **Contrôle exhaustif par fichier, jamais statistique.**
- 🔴 **NOUVEAU (pattern des 4 repos ce run) — les violations les plus graves sont dans le JSON-LD**, pas dans le corps de page, et les compteurs de composants ne les voient pas. Vérifié sur CNR, ENR, CU et EU le même run. ➡️ **Auditer le JSON-LD en début de run, indépendamment de tout compteur.**
- 🔴 **Ne jamais dériver une cible de batch d'un `grep` ; la dériver du PARSING.** ` conforme zona` = 1 159 fichiers dont 21 hors JSON-LD ; le champ parsé donne **808** fichiers et zéro faux positif.
- 🔴 **Vérifier qu'une PR mergée a bien CLOS son gisement.** Réappliqué ce run : `a a  profissionais` est **effectivement clos** (0 occurrence), contrairement au constat du 12/08. **Un merge n'est pas une clôture — mais un constat de non-clôture n'est pas éternel non plus. Recompter, toujours.**
- 🔴 **Un script cassé dans le repo n'est PAS la preuve qu'il a produit le défaut.** Les 3 scripts `r12_*.py` portent un `Z` orphelin qui a **0 occurrence** en production. **Le même contrôle a réfuté le même diagnostic sur EU ce run — 2 diagnostics sur 2.** ➡️ **Toujours vérifier que la chaîne défectueuse du script existe réellement en production avant de conclure à la causalité.**
- 🔴 **Un batch de conformité peut corrompre la RÈGLE qu'il applique.** `fb9dd2415` a substitué dans `AGENTS.md` en même temps que dans 2 003 pages et a **désarmé le ruling** tout en croyant l'appliquer. ➡️ **Exclure explicitement `AGENTS.md`, `SEO_PLAN.md`, `context.md`, `CLAUDE.md`.**
- 🔴 **Une contradiction dans une règle verrouillée doit être traitée comme une CORRUPTION jusqu'à preuve du contraire.** Le réflexe « demander à Philippe » a coûté **5 semaines** là où `git log -S` répondait en une commande.
- **R145 autorise explicitement `24h/7d` sur ce repo.** Ce qui est banni : les promesses de **délai** personnalisées. ⚠️ C'est **l'inverse** des sites `*-norte-reparos`. **Ne pas purger « 24h » ici.**
- **Corriger un prix faux par RETRAIT du total, ou par transplant verbatim d'une réponse conforme déjà en production — jamais par recalcul.**
- Ce site utilise « 65 € » (avec espace) et « 65 EUR », pas seulement « 65€ » → adapter les greps R8.

## Edge cases détectés
- **Worktree obligatoire** : la copie de travail est sale en permanence et posée sur une branche feature d'une autre automation. **Jamais `git checkout`, `reset --hard`, `stash` ni `clean`** (R-WT). Vérifié ce run : cette mention est bien une **interdiction**, pas une prescription — rien à corriger.
- **Le `/tmp` du sandbox ≠ le `/tmp` du host.** Worktrees sous `~/work/Sites/_worktrees/loop-YYYY-MM-DD/` — **lisibles depuis le sandbox**, ce qui permet de parser les 2 400+ fichiers HTML en quelques secondes. **C'est la répartition la plus efficace : parsing Python au sandbox, `git`/`gh` au host.**
- **Les commandes `git` ne fonctionnent PAS depuis le sandbox dans un worktree** (le `.git` contient un chemin absolu host).
- 🔴 **`grep -P` n'existe pas sur macOS** — un `grep -P` dans une chaîne `&&` fait **échouer silencieusement tout le reste de la commande** (un `git commit` a été sauté ce run à cause de ça). **Utiliser Python pour tout motif non trivial.**
- 🔴 **`git commit -m` multiligne avec backticks/parenthèses est fragile en zsh.** Utiliser `git commit -F -` avec un heredoc `<<'MSG'`.
- ⚠️ **Le sandbox ne peut pas supprimer les `.git/objects/*.lock`** — `git fetch` émet des warnings d'unlink mais **réussit**.
- Le sandbox n'a ni `gh` ni credentials Git → tout git/gh via `mcp__desktop-commander__start_process` (host, `gh` authentifié `taffrand-gif`).
- L'outil `Edit`/`Write` (chemin host) gère parfaitement les accents et les fichiers HTML sur une seule ligne — plus sûr que `sed` pour un patch chirurgical.
- Corps de PR long : fichier + `gh pr create --body-file`, jamais `--body` inline.
