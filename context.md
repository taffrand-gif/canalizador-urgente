# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-20
- Tâche prévue : `context.md` du 19/08, **n°2** — « localiser les 5 blocs `ld+json` JSON-invalides ; il les compte, il ne les a pas encore nommés ».
- Tâche réellement exécutée : **la tâche prévue, plus la réparation.**
- Branche (depuis `origin/main`, **en worktree**) : `loop/2026-08-20-cu-jsonld-invalide`
- Commits : 2 (1 fichier de production + `SEO_PLAN.md`)
- PR ouverte : **#269** — https://github.com/taffrand-gif/canalizador-urgente/pull/269
- Résultat : ✅ 1 fichier. **Une money page n'émettait aucune donnée structurée valide depuis le 11/08.**

### Les 5 blocs sont dans UN SEUL fichier — et c'était tous ses blocs
Parsing des **2 487 fichiers HTML / 7 035 blocs `application/ld+json`** : les 5 invalides sont dans `blog/canalizador-urgente-guia-completo.html`, lignes 26 à 30. Ce sont **tous** les blocs JSON-LD de la page : `BlogPosting`, `Service`, `FAQPage`, `BreadcrumbList`, `HowTo`.

```
  cassé : {"@context":"https://***@type":"BlogPosting", …
correct : {"@context":"https://schema.org","@type":"BlogPosting", …
```
La chaîne exacte `schema.org","` avait été remplacée par `***` → JSON cassé dès le caractère 30 (`Expecting ',' delimiter`).

🔎 **Cause racine déjà documentée dans le repo** : `_audit/LECONS.md` **leçon #407 (18/07)** — « filtre sandbox Hermes mute `https://schema.org","@type":` en `https://***@type":` dans les outputs ». **Le piège d'outil était connu et le défaut a été commité quand même** ; personne n'avait cherché s'il avait atteint la production.

⚠️ **La PR #268 (ouverte) réécrit exactement la ligne 26 et y CONSERVE le `***`.** Sans ce correctif, elle republierait la corruption sur le bloc `BlogPosting`. **Résolution si #268 merge en premier — par MERGE, jamais par rebase (R6)** : garder le contenu de #268 sur la ligne 26 et y restaurer `"https://schema.org","`. Les blocs 27-30 ne sont pas dans le diff de #268, donc sans conflit possible.

- **Témoins R8** : `https://***` **5→0** · `"@context":"https://schema.org"` **0→5**. `git diff --numstat` : **5/5** (5 substitutions, aucun autre octet touché).
- **Revalidation** : 5/5 blocs parsent, `@context` correct sur les 5. **Rescan complet après patch : 2 487 fichiers, 7 035 blocs, 0 invalide.**
- Contrôle croisé exécuté **depuis le host**, pas seulement depuis le sandbox — puisque c'est un filtre de sandbox qui produit ce défaut.
- Valeur restaurée **verbatim** depuis les 53 autres pages de `blog/` conformes → zéro invention (R4).

## ✅ Gate merge — aucun gate actif
Vérifié ce run sur les 4 `context.md` : **aucune mention d'attente de merge**. Aucun gate réécrit.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Entre le 06/08 et le 09/08, cette mention a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**.

## 🛑 GISEMENTS CHIFFRÉS — DÉCISIONS REQUISES (prédicat = **Question** + variante)

Aucun n'a été touché ce run. Inventaire inchangé depuis le 19/08.

| # | Cible | Fichiers | Traitement |
|---|---|---:|---|
| **(g)** | **Q `Fazem orçamento sem compromisso?` → `gratuito`** | **38** | ✅ **MEILLEUR CANDIDAT POUR UN PREMIER GO** — substitution `gratuito` → `por escrito`. Motif unique, **interdiction verbatim `PRICING.md` L51**, prototype visible dans la PR #267 |
| (a) | `Suplemento 30-50%` → `Acréscimo +50% fora de horas úteis` | **815** | surensemble : referme (c) `por escritoEUR` (698) et (d) `Desde 130 EUR` (62) |
| (b) | Q `Quanto tempo demoram a chegar?` | **813** | retrait du couple Q/R + re-parse du `FAQPage` |
| (b2) | Q `Tempo de resposta?` | **331** | retrait du couple Q/R + re-parse |
| (f) | Q `Garantia e fatura?` | **332** | **arbitrage** : `2 anos` est-il l'offre réelle ? Contradiction avec `Oferecem garantia?` (47) |
| (e) | `mediante confirmação por telefone/7d` (suffixe orphelin) | 15 | retrait du suffixe — **PR #264 ouverte dessus** |

⚠️ Rappel : **exclure explicitement `AGENTS.md`, `SEO_PLAN.md`, `context.md`, `CLAUDE.md`** de tout batch (leçon `fb9dd2415`).

## Tâche suivante recommandée
1. **Passer les signatures de corruption connues de `_audit/LECONS.md` sur TOUT le repo.** Le motif de la leçon #407 a sorti une money page en 4 secondes de parsing. **`_audit/LECONS.md` en contient d'autres qui n'ont jamais été grepées.** C'est le meilleur rapport effort/résultat identifié à ce jour sur ce repo, et il ne demande aucun GO.
2. **Si GO (g)** : les 38 fichiers `orçamento escrito é gratuito`. Le plus petit, le mieux sourcé, prototype déjà en revue (PR #267).
3. **Sans GO** — uniformiser les **2 variantes hybrides** de `Quanto custa a deslocação?` (`Z3: 35 € e 65 €/h de mão de obra`). 2 fichiers, motif unique.
4. **Sans GO** — les **6 réponses de `Atendem 24h/7d?`** portant l'artefact `garantimos atenção após contacto telefónico`.
5. **Sans GO** — chercher sur CU les défauts trouvés sur EU : statistiques non sourcées (`N% dos/das`, ~60 fichiers sur EU) et `Sem custo extra de fim de semana` (22 sur EU).
6. **Ajouter `Sob marcação` à `PRICING.md`** si c'est une vraie règle d'offre — sinon il restera perdu.

## Apprentissages (self-improving)
- 🔴 **NOUVEAU — un piège d'OUTIL documenté doit être cherché dans les fichiers COMMITÉS, pas seulement évité au moment d'écrire.** La leçon #407 décrit le filtre `schema.org","` → `***` depuis le **18/07** ; personne n'avait passé son motif sur le repo. Coût : **4 secondes de parsing**. Résultat : une money page sans aucune donnée structurée valide depuis le 11/08. ➡️ **Toute leçon décrivant une signature de corruption vaut une passe sur tout le repo au run suivant.** Même principe que « une signature écrite dans un `context.md` est une tâche du run suivant, pas une note » (validé le 19/08) — **étendu ici à `_audit/LECONS.md`, qui n'était pas relu**.
- 🔴 **NOUVEAU — quand le défaut vient d'un filtre de SANDBOX, la vérification doit sortir du sandbox.** Contrôle rejoué depuis le host avant commit.
- 🔴 **NOUVEAU — une PR ouverte peut *perpétuer* un défaut sans l'avoir introduit.** Le contrôle habituel (« quelles PR touchent ce fichier ? ») répond « #268 » et invite à ne rien faire. **La bonne question est « que fait cette PR de la ligne en cause ? »** — ici elle la réécrit et garde le bug.
- 🔴 **Le prédicat d'un gisement, c'est le SUJET de la question, pas son libellé.** `Tempo de resposta?` (331) et `Quanto tempo demoram a chegar?` (813) sont le même défaut sous deux libellés ; six runs ont compté le second sans voir le premier. ➡️ **Regrouper les Questions par thème (délai / prix / garantie) AVANT de compter.**
- 🔴 **Deux Questions DIFFÉRENTES d'un même thème peuvent se contredire.** `Garantia e fatura?` (2 ans) vs `Oferecem garantia?` (sans durée). **Croiser les Questions d'un même thème.**
- 🔴 **Le prédicat `gratuit` de `PRICING.md` L51-53** : CU 38 fichiers + 1 page · CNR 6 (PR #319) · ENR 2 (PR #351). ➡️ `grep -c 'gratuit'` au contrôle d'ouverture des 4 repos.
- 🔴 **Un artefact de purge peut se loger dans une CELLULE DE TABLEAU.** Signature : `<td>` contenant `&lt; ` suivi de plus de 40 caractères.
- 🔴 **Un batch partiellement appliqué laisse un gisement PLUS GRAND que celui qu'il corrigeait** (73 → 698, `EUR` non consommé). **Toute substitution doit inclure le contexte droit**, et **recompter les DEUX motifs après exécution**.
- 🔴 **Chercher le SURENSEMBLE avant de demander un GO.**
- 🔴 **Un échantillonnage à 95 % peut manquer la page qui compte.** Contrôle exhaustif par fichier, jamais statistique.
- 🔴 **Les violations les plus graves sont dans le JSON-LD**, et aucun compteur de composants ne les voit. **Confirmé une 2ᵉ fois ce run, sous une forme nouvelle : le JSON-LD peut être non pas faux mais INVALIDE — donc totalement ignoré.** ➡️ **Ajouter au contrôle d'ouverture : parser tous les blocs `ld+json` et compter les invalides.** 4 s sur 2 487 fichiers.
- 🔴 **Ne jamais dériver une cible de batch d'un `grep` ; la dériver du PARSING.**
- 🔴 **Un batch de conformité peut corrompre la RÈGLE qu'il applique** (`fb9dd2415`). Exclure `AGENTS.md`, `SEO_PLAN.md`, `context.md`, `CLAUDE.md`. Avant d'escalader une contradiction de doctrine : `git log -S "<fragment>" -- AGENTS.md`.
- 🔴 **Le code mort est un gisement sur les repos `*-norte-reparos`** (CNR : 10 violations retirées, PR #321 ; ENR : 4, PR #358). **Sur CU le sujet est différent** — le repo est en HTML statique, pas en composants : l'équivalent y est le **fichier orphelin non lié et non sitemapé**. Piste non explorée.
- **R145 autorise explicitement `24h/7d` sur ce repo.** Ce qui est banni : les promesses de **délai**. ⚠️ C'est **l'inverse** des sites `*-norte-reparos`. **Ne pas purger « 24h » ici.**
- **Corriger un prix faux par RETRAIT du total, ou par transplant verbatim d'une réponse conforme déjà en production — jamais par recalcul.**
- Ce site utilise « 65 € » (avec espace) et « 65 EUR », pas seulement « 65€ » → adapter les greps R8.

## Edge cases détectés
- **`gh` et les credentials Git n'existent QUE sur le host macOS.** Sandbox = lecture / grep / parsing Python / **écriture de fichiers** (2 487 fichiers parsés en quelques secondes) ; `git` en écriture / `gh` → `mcp__desktop-commander__start_process`. **C'est la répartition la plus efficace.** ⚠️ **Mais pas pour tout** : voir la leçon du filtre `***` — un contrôle final depuis le host reste nécessaire quand le contenu en jeu est celui que le filtre mute.
- **Le `/tmp` du sandbox ≠ le `/tmp` du host.** Worktrees sous `~/work/Sites/_worktrees/loop-YYYY-MM-DD/` — lisibles depuis le sandbox.
- **Les commandes `git` ne fonctionnent PAS depuis le sandbox dans un worktree** (chemin absolu host dans `.git`). **L'écriture de fichiers, si.**
- 🔴 `gh pr diff <n>` peut dépasser la limite de sortie → `gh pr view <n> --json files`. **Mais pour savoir ce qu'une PR fait d'une ligne précise, `gh pr diff` filtré par `awk` reste le seul moyen** — utilisé ce run pour établir que #268 conserve le `***`.
- 🔴 **zsh ne fait PAS de word-splitting** ; **`grep -P` n'existe pas sur macOS** → Python pour tout motif non trivial ; **`git commit -m` multiligne est fragile** → `git commit -F -` + heredoc `<<'MSG'`.
- **Worktree obligatoire** (R-WT) : la copie de travail est sale en permanence. **Jamais `git checkout`, `reset --hard`, `stash` ni `clean`.** Vérifié ce run : le checkout partagé était sur `feat/cu-rankpush-canalizador-urgente-t_a9810c1c` avec ~40 fichiers `_audit/SMKO-cu-*` non suivis d'une autre automation — **non touché**. Cette mention est bien une **interdiction**, pas une prescription — rien à corriger.

## Blocages connus
1. 🛑 **Batch (a) `Suplemento 30-50%` — 815 fichiers.** Attente GO.
2. 🛑 **Batch (b) / (b2) — questions de délai, 813 + 331 fichiers.** Attente GO.
3. 🛑 **(f) `Garantia e fatura?` — 332 fichiers.** Arbitrage : `2 anos` est-il l'offre réelle ?
4. ⚠️ **`Sob marcação` (Z6)** absent de `PRICING.md` — perdu deux fois avec une colonne de délai. À rétablir dans `PRICING.md` si c'est une vraie règle.
5. ⚠️ **Doublon `public/` ↔ racine** — arbitrage conjoint avec EU.
6. ✅ **REFERMÉ — les 5 blocs `ld+json` invalides.** Nommés et réparés ce run (PR #269). Rescan : 0 invalide sur 7 035 blocs.
7. ⚠️ **PR #268 collisionne ligne 26** de `blog/canalizador-urgente-guia-completo.html` et y conserve le `***`. Voir la procédure de résolution en §Dernier run.
