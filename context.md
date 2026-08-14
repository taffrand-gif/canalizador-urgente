# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-14
- Tâche exécutée : **tâche n°4 du `context.md` du 13/08 (« sans GO ») — audit JSON-LD des points d'entrée les plus crawlés**, puis correction de ce que l'audit a trouvé.
- Branche : `loop/2026-08-14-canalizador-urgente-jsonld-entrypoints` (depuis `origin/main`, **en worktree**)
- Commits : `aa5c06ba0` (`zona-intervencao.html`), `aa3aff340` (`calculadora-de-preco.html`), + le commit `SEO_PLAN.md`
- PR ouverte : https://github.com/taffrand-gif/canalizador-urgente/pull/261
- Résultat : ✅ 2 fichiers de production. **Et un nouveau motif d'artefact de purge, invisible au grep comme au parsing du JSON-LD.**

### Audit — 7 points d'entrée, 26 blocs `ld+json`, tous JSON-valides
Motifs cherchés dans **toutes les valeurs de chaînes, à toute profondeur** : `rápid`, `prioritári`, `Desde 130`, `Suplemento 30-50`, `por escritoEUR`, `gratuit`, `conforme zona`, `imediat`, `acceptedAnswer.text` < 20 car., doublons `X e X`.

| Point d'entrée | Verdict |
|---|---|
| `index.html` · `public/index.html` · `precos.html` · `perguntas-frequentes.html` | ✅ **propres** |
| `contactos.html` | ⏭️ **déjà couvert par la PR #260** (ouverte) — **non retouché**, pour ne pas créer de conflit |
| `zona-intervencao.html` · `calculadora-de-preco.html` | 🔴 **corrigés ici** |

### Ce qui a été corrigé
1. **`zona-intervencao.html`** — prix inventé `Desde 130 EUR (1h)… Suplemento 30-50%…` → **transplant verbatim** de la réponse conforme déjà en production sur `calculadora-de-preco.html` (même repo, **même Question**) : `65 €/h + deslocação (Z1: 15€ a Z6: 65€). Mínimo 1h. Acréscimo +50% fora de horas úteis.` Question de délai (`em poucos minutos` + artefact `garantimos atenção após contacto telefónico ao telefone`) → **retrait du couple Q/R**. `Trabalham 24h/7d?` **conservé** (R145 l'autorise).
2. **`calculadora-de-preco.html`** — (a) le `FAQPage` finissait par `Resposta rápida, 24h/7d…` : **`Resposta rápida` est la formulation exactement bannie** par R145 → retrait du seul fragment banni, `24h/7d` conservé.
   (b) 🔴 **La table de zones portait une colonne `Tempo` intégralement cassée** : 3 cellules sur 6 contenaient **un paragraphe de CTA entier écrasé dans une cellule de délai**, préfixé d'un `&lt;` orphelin ; 2 vides ; 1 hors-sujet (`Sob marcação`). **Colonne retirée intégralement** — aucun délai par zone n'est sourçable dans `PRICING.md`, et R145 interdit le délai chiffré. Table ramenée à `Zona | Cidades | €`, **6 lignes × 3 cellules**.

Témoins R8 — `zona-intervencao.html` : `Desde 130` **1→0** · `Suplemento 30-50` **1→0** · `poucos minutos` **1→0** · `garantimos atenção` **1→0** · `Quanto tempo demoram a chegar` **1→0** · `65 €/h + deslocação` **0→1** · `24h/7d` **3→3** (contrôle positif).
`calculadora-de-preco.html` : `Resposta rápida` **1→0** · `poucos minutos` **3→0** · `Tempo</th>` **1→0** · `24h/7d` **5→5** · `65 EUR/h` **2→2** (grille intacte).
Contrôle structurel : **4/4 puis 6/6 blocs re-parsés valides**, `FAQPage` de `zona-intervencao.html` **3 → 2 questions**, **0 `acceptedAnswer.text` < 20 caractères**.

⚠️ **`Sob marcação` (Z6) est tombé avec la colonne `Tempo`.** Il est **absent de `PRICING.md` de CU** — non restauré ailleurs (R4). **Si c'est une vraie règle d'offre, l'ajouter d'abord à `PRICING.md`.**
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
Vérifié ce run : aucune mention d'attente dans les 4 `context.md`. Aucun gate réécrit.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Entre le 06/08 et le 09/08, cette mention a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**.

🆕 **Corollaire découvert ce run (sur CNR)** : le statut `MERGED` de l'API GitHub **n'est pas une preuve de présence en production** — la PR CNR #300, pourtant `MERGED`, a été annulée par une réécriture de `main`. ➡️ **Contrôle de fin de run : `git merge-base --is-ancestor <mergeCommit> <remote>/main`.** À passer aussi sur CU au prochain run.
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
1. **Si GO (a)** : batch `Suplemento 30-50%` — un seul motif, referme (c) et (d). Les PR #260 et #261 en montrent le rendu exact sur 3 pages.
2. **Si GO (b)** : les 808 `acceptedAnswer.text == "conforme zona"`, **puis re-parser le `FAQPage` de chaque fichier**. ⚠️ **Avant d'exécuter, refaire le comptage avec le PRÉDICAT « Question », pas la valeur de réponse** — sur EU, la même correction de prédicat a fait passer le gisement de **526 à 953**. **Le chiffre 808 est probablement sous-estimé.**
3. **Sans GO — priorité** : **ventiler par parsing TOUTES les Questions du `FAQPage`** de CU, comme fait sur EU ce run (2 396 fichiers en quelques secondes au sandbox). EU a livré 3 gisements jamais inventoriés en une passe, dont **une contradiction de prix en production** (2 réponses opposées à la même Question). **CU n'a jamais été ventilé.**
4. **Sans GO** : chercher sur CU les 2 défauts trouvés sur EU ce run — `Sem custo extra de fim de semana` (contredit la majoration +50 %) et la fourchette de prix inventée `varia entre X€ e Y€`.
5. **Sans GO** : chercher le motif `<td>` contenant `&lt; ` suivi de plus de 40 caractères — signature de la colonne de délai écrasée trouvée ce run. **Jamais recherché ailleurs que sur `calculadora-de-preco.html`.**
## Apprentissages (self-improving)
- 🔴 **NOUVEAU — un artefact de purge peut se loger dans une CELLULE DE TABLEAU, et aucun contrôle existant ne le voyait.** Une substitution a remplacé une valeur de délai (`&lt; 30 min`) par un paragraphe de CTA entier, sans consommer le `&lt;` qui la précédait → 3 cellules d'un tableau de prix remplies d'un CTA. Ni le grep de motifs connus, ni le parsing du JSON-LD ne le détectent. ➡️ **Signature de détection à ajouter : `<td>` contenant `&lt; ` suivi de plus de 40 caractères.** Même famille que `por escritoEUR` : *une substitution qui ne consomme ni son contexte gauche ni son contexte droit*.
- 🔴 **NOUVEAU — l'artefact `)EUR` n'est pas propre à CU.** Il existe aussi sur `eletricista-urgente` (15 fichiers), trouvé le même run. ➡️ **Tout défaut documenté sur un repo doit être recherché sur les 3 autres dans le run qui suit.**
- 🔴 **NOUVEAU — vérifier les PR ouvertes AVANT de patcher un fichier.** `contactos.html` portait exactement les mêmes défauts que `zona-intervencao.html`, mais la PR #260 les corrige déjà : le retoucher aurait créé un conflit de merge pour rien. ➡️ **`gh pr list` + liste des fichiers touchés, en début de run.**
- 🔴 **NOUVEAU — le prédicat d'un gisement doit être la QUESTION, pas la valeur de réponse.** Démontré sur EU ce run : `" conforme zona"` donnait 526, la Question `Quanto tempo demoram a chegar?` donne **953** (4 variantes, dont une à 418 fichiers jamais documentée). ➡️ **Le chiffre 808 de la cible (b) de CU est à recompter avec le bon prédicat avant tout GO.**
- 🟢 **L'audit par parsing des points d'entrée est rentable et tient dans un run.** 7 fichiers, 26 blocs, 2 gisements réels — dont un invisible à tous les contrôles précédents.
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
