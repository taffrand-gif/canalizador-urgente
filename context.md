# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-23
- Tâche prévue : rang 1 (contrôler `comparacao.html` d'EU — **relève du repo EU, traité là-bas**) et rang 2 (suite du sweep `LECONS.md`).
- Tâche réellement exécutée : **un balayage structurel systématique de TOUT le dépôt**, transposé de la découverte faite sur ENR le même run. Il a sorti un défaut que ni le sweep `LECONS.md`, ni le compteur de conformité, ni l'audit de sitemap ne voyaient.
- **1 PR ouverte** :
  - **#273** — https://github.com/taffrand-gif/canalizador-urgente/pull/273 — branche `loop/2026-08-23-cu-html-structure` — 2 commits, 1 fichier de production + `SEO_PLAN.md`

### 1. 🔴 `contactos.html` était la SEULE page du dépôt servie en mode quirks (PR #273)
Le fichier commençait **directement** par `<script type="application/ld+json">` : ni `<!DOCTYPE html>`, ni `<html lang="pt-PT">`, ni `<head>` — alors qu'il porte bien un `</head>` (L42) et un `</html>` (L75). Témoins : `<html>` **0/1**, `<head>` **0/1**.

**Deux conséquences réelles, sur une money page de conversion** : (a) sans DOCTYPE, le navigateur bascule en **mode quirks** — modèle de boîte hérité, rendu différent de toutes les autres pages ; (b) sans `<html lang>`, **aucun signal de langue** pour les crawlers ni les lecteurs d'écran.

**Preuve d'unanimité** : sur les **2 454** fichiers HTML du dépôt, `contactos.html` est le **seul** sans DOCTYPE **et** le **seul** sans `<html lang>`. Sur 2 075 pages racine, 5 variantes de prologue coexistent — mais **`lang="pt-PT"` est unanime à 2 074/2 075**. Prologue transplanté **verbatim** de `sobre.html` ; **le prologue résultant en est byte-identique** (forme partagée par 410 pages).
- **Témoins R8** : `<html>` **0/1 → 1/1** · `<head>` **0/1 → 1/1** · DOCTYPE **absent → présent** · `<html lang>` **0 → 1** · `<body>`/`<header>`/`<main>`/`<section>` **inchangés**.

### 2. 🔎 Résultat du balayage : CU est le plus sain des 4 repos
Sur **2 454** fichiers HTML (équilibre de 10 balises, validité JSON de chaque bloc `ld+json`, doublons byte-à-byte, DOCTYPE, `<html lang>`) : **3 fichiers à problème**.
- `blog/canalizador-urgente-guia-completo.html` — 5 JSON-LD invalides — **déjà pris par la PR #269**.
- `contactos.html` — **traité** (#273).
- `canalizador-desentupimento-vimioso.html` — **consigné**, voir §3.

**Un résultat négatif est un résultat** : inutile de relancer la chasse structurelle sur CU au prochain run.

### 3. `vimioso` — un `<header>` jamais fermé, et un point de fermeture INDÉTERMINÉ
`<header role="banner">` est ouvert L70 et jamais fermé : **tout le corps du document est nesté dans le `<header>`**. Seul des **77** fichiers `canalizador-desentupimento-*` dans ce cas.
Trois invariants de jumeaux convergent — `<p class="answer-first">` dans le `<header>` **70/70**, `<aside class="doctrine-transparence">` dans le `<header>` **66/77**, `</header>` juste après un `</a>` de CTA **69/70** — **et pourtant le point reste indéterminé** : vimioso n'a **ni ce CTA à cet endroit, ni `<main>`**, et porte un bloc « HERO BOX » qu'**aucun** des 70 jumeaux ne possède. **Trois quasi-preuves ne font pas une preuve.** Fermer au jugé serait un choix, pas une restauration.

## ✅ Gate merge — aucun gate actif
Vérifié ce run : **aucune mention d'attente de merge**. Aucun gate réécrit. 5 PR étaient ouvertes ; la #273 a été ouverte quand même.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Entre le 06/08 et le 09/08, « Attente GO merge (R7) » a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**. **Ne jamais réécrire un gate de ce type.**

## 🎯 FILE DE TÂCHES LOOP — état au 2026-08-23

| Rang | Cible | Statut |
|---|---|---|
| — | `contactos.html` — prologue de document absent | ✅ **traité ce run (#273)** |
| **1** | 🔴 **`contactos.html` — `Z1 (0-30 km): . Z2 (31-50 km): . Z3 (51-90 km): . Z4 (91-130 km): .`** | ⏸ **des valeurs de délai purgées ont laissé des deux-points suivis d'un point, servis en clair au visiteur.** Le **retrait de la phrase** est possible sans invention (R4/R145 interdisent d'y écrire un délai) — mais la zone est **prise par la PR #264**. Même famille : `menos de Atendemos 24h/7 dias, mediante confirmação…`, phrase cassée par la même purge. **Dès #264 mergée.** |
| **2** | **`canalizador-desentupimento-vimioso.html` — `<header>` jamais fermé** | 🛑 **point de fermeture indéterminé** (voir §3). Demande **un arbitrage d'une ligne** : « fermer le `<header>` après le `<p class="answer-first">` » suffirait. Sinon reste en file. |
| **3** | **Le reste du sweep `LECONS.md`** | ⏳ sans GO. `LECONS.md` fait 904 lignes ; le sweep du 21/08 a couvert 10 motifs. **Le passage des signatures de `LECONS.md` doit être une étape FIXE du loop, pas une recommandation.** |
| **4** | **Corruption `repar`→`arranj` — 33 occurrences / 19 fichiers sur CU** | ⏳ **GO périmètre.** **Aucun `href` touché sur CU** : le défaut y est purement textuel. |
| **5** | **`Você` — 15 occurrences / ~13 fichiers** | 🛑 corpus INTERDIT, GO requis. ℹ️ **Chercher les doublons d'abord** : 4 sont tombés le 22/08 sans consommer le GO. |
| **6** | Les **2 variantes hybrides** de `Quanto custa a deslocação?` (`Z3: 35 € e 65 €/h`) | ⏳ 2 fichiers, motif unique, sans GO |
| **7** | Les **6 réponses de `Atendem 24h/7d?`** portant `garantimos atenção após contacto telefónico` | ⏳ sans GO |
| **8** | Chercher sur CU les défauts trouvés sur EU : statistiques non sourcées (`N% dos/das`) et `Sem custo extra de fim de semana` | ⏳ sans GO |
| **9** | `streetAddress: "Trás-os-Montes, Portugal"` sur `contactos.html` + `canalizador-frioes.html` | ⏳ incohérent R5 — ce n'est pas une adresse |
| 10 | Ajouter un **§NAP à `AGENTS.md`** et `Sob marcação` à `PRICING.md` | ⏳ **RÉTROGRADÉ.** Voir §Apprentissages : sur CNR ce run, le §NAP manquant n'était **pas** le blocage annoncé — la valeur était dans `shared/serviceConfig.ts` depuis le début. **Confort, pas préalable.** |

## Tâche suivante recommandée
1. **Rang 3 — le sweep `LECONS.md`, en étape fixe.** C'est la seule tâche substantielle du repo sans GO ni PR bloquante.
2. **Rang 1 dès #264 mergée** — le `Z1 (0-30 km): .` est visible par le visiteur sur une money page.
3. **Rangs 6, 7, 8** — tous sans GO, tous petits.
4. **Poser en une ligne la question du rang 2** (où fermer le `<header>` de vimioso).
5. **Ne PAS relancer le balayage structurel sur CU** : 3 fichiers sur 2 454, la famille est close.
6. **Si GO (g)** : les 38 fichiers `orçamento escrito é gratuito` (prototype en revue, PR #267).

## Apprentissages (self-improving)
- 🔴 **NOUVEAU — un balayage structurel de TOUT le dépôt coûte une commande et vaut mieux qu'un sweep de motifs.** Sur ENR il a sorti 3 pages dont le corps entier était avalé par un `<script>` non fermé ; ici, **la seule page du dépôt en mode quirks**. Aucun compteur de conformité, aucun grep de vocabulaire, aucun audit de sitemap ne les voyait. ➡️ **Étape fixe sur les 4 repos : équilibre des balises + validité JSON-LD + doublons byte-à-byte + DOCTYPE + `<html lang>`.**
- 🔴 **NOUVEAU — le dépôt entier est le meilleur juge de ce qui manque à un fichier.** « Il manque un DOCTYPE » est une opinion ; « 2 454 sur 2 454 en ont un sauf celui-ci, et 2 074 sur 2 075 écrivent `lang="pt-PT"` » est une preuve. ➡️ **Avant de restaurer, compter la population. La variante majoritaire n'est pas toujours la bonne — mais l'unanimité, elle, tranche.**
- 🔴 **NOUVEAU — ne pas fermer une balise au jugé.** Sur `vimioso`, trois invariants convergeaient à 70/70, 66/77 et 69/70, et le point de fermeture reste pourtant indéterminé parce que le fichier porte un bloc qu'aucun jumeau n'a. **Trois quasi-preuves ne font pas une preuve. Consigner bat deviner.**
- 🔴 **NOUVEAU (leçon CNR de ce run) — « valeur non sourçable » se PROUVE en remontant la chaîne de définition, jamais en constatant l'absence d'un §NAP.** Sur CNR, un rang est resté bloqué un run entier pour ce motif : la valeur était dans `shared/serviceConfig.ts` L43, c'est-à-dire dans le fichier que l'expression cassée **nomme elle-même**. ➡️ **Distinguer « aucune source » de « source pas encore cherchée ».** Le §NAP d'`AGENTS.md` reste souhaitable — **comme confort, pas comme préalable** ; le rang 10 a été rétrogradé en conséquence.
- 🔴 **Un résultat NÉGATIF est un résultat.** 3 fichiers sur 2 454 : le savoir évite de relancer la chasse. Même valeur que le `0` du sweep `${…}` sur ENR.
- 🔴 **Un compteur de balises ÉQUILIBRÉ peut signaler une duplication, pas une santé.** `<header>` 2/2 et `<h1>` 2/2 étaient **dupliqués**. ➡️ **Compter les balises uniques par document (`<h1>`, `<header>`, `<main>`), pas seulement leur équilibre.**
- 🔴 **Avant de patcher une chaîne interdite, chercher si elle vit dans un DOUBLON.** Le bon niveau n'est ni la chaîne ni la page : **c'est le bloc**.
- 🔴 **Prouver qu'une suppression ne perd rien AVANT de supprimer.** Segmenter la copie à retirer sur `</li|p|td|h2|h3>`, vérifier que chaque segment > 45 caractères se retrouve dans la copie conservée.
- 🔴 **Un GO peut devenir inutile si on attaque le défaut au bon niveau.** Les 4 `Você` du 22/08 sont partis sans qu'aucune décision de pronom n'ait été prise.
- 🔴 **Un « TODO post-merge » écrit dans `LECONS.md` n'est exécuté par personne.** ➡️ **Étape FIXE du loop, pas recommandation.**
- 🔴 **Quand un défaut RÉCIDIVE, chercher le GÉNÉRATEUR, pas la page.** ⚠️ **La chaîne de génération a maintenant produit CINQ familles de défauts distinctes sur les 4 repos** : marqueurs `##style##`, corps de page dupliqués, JSON-LD tronqué écrasant un `<style>` (ENR), JSX non compilé (CNR), prologue de document absent (CU). **Un audit du générateur rapporterait plus que la somme des correctifs.**
- 🔴 **Un marqueur de gabarit non substitué n'apparaît dans aucun compteur.** `grep -rIoE '##[a-zA-Z_]{3,}##'` **et sa famille élargie** (`{{…}}`, `%%…%%`, `__…__`, `${…}`).
- 🔴 **Une PR qui répare un fichier ne répare pas sa famille.** Repasser le contrôle sur l'ensemble du motif de nom.
- 🔴 **Un titre de PR ne dit pas ce que la PR couvre.** **5ᵉ run consécutif** que `gh pr view <n> --json files` évite un conflit.
- 🔴 **La signature d'une corruption de batch, c'est le MOT INEXISTANT.**
- 🔴 **Un batch de conformité peut corrompre la RÈGLE qu'il applique** (`fb9dd2415`). Tout batch doit exclure `AGENTS.md`, `SEO_PLAN.md`, `context.md`, `CLAUDE.md`, `LECONS.md`. Avant d'escalader une contradiction : `git log -S "<fragment>" -- AGENTS.md`.
- 🔴 **Le compteur R12 sur-compte** : R145 **autorise** `24h/7 dias`.
- **Ne pas sur-purger.** R4 se viole dans les deux sens.

## Edge cases détectés
- **`gh` et les credentials Git n'existent QUE sur le host macOS.** Sandbox : `git fetch` OK, **`git push` impossible**. **Répartition** : lecture / grep / parsing Python / **écriture de fichiers** → sandbox ; `git` en écriture / `gh` → `mcp__desktop-commander__start_process`.
- **Le `/tmp` du sandbox ≠ le `/tmp` du host.** Worktrees **et** `--body-file` de PR sous `~/work/Sites/_worktrees/`.
- 🔴 **Un worktree n'est PAS un dépôt git vu depuis le sandbox** : `git show`/`diff`/`log` y rendent des **compteurs à zéro** trompeurs. ➡️ **Tout témoin se compte en Python sur le CONTENU des fichiers.**
- 🔴 **`comparacao.html` est à la RACINE sur CU**, dans `client/public/` sur CNR et ENR. **Ne pas présumer de l'arborescence entre repos** : `find . -name '<fichier>'` avant tout. Idem pour les remotes : CNR a `github` **et** `origin` (diffuser contre `github/main`) ; CU et ENR n'ont qu'`origin`.
- ⚠️ **Un script Python qui accumule des exemples peut faire exploser la sortie** (196 000 caractères sur ENR ce run, résultat tronqué et inutilisable). **Borner explicitement ce qu'on imprime** en balayant des milliers de fichiers.
- 🔴 **Le filtre sandbox qui mute `https://schema.org` est COSMÉTIQUE à l'affichage** mais **`https://***` sur disque est un vrai défaut** : distinguer en relisant les octets, pas la sortie du terminal.
- 🔴 **`grep -P` n'existe pas sur macOS** ; **zsh ne fait pas de word-splitting**. Pour tout motif non trivial : **Python**.
- 🔴 **`git commit -m` multiligne est fragile en zsh** → `git commit -F -`. Corps de PR : `--body-file`.
- **Worktree obligatoire** (R-WT). **Jamais `reset --hard` / `checkout -- .` / `stash` / `clean`** sur le checkout partagé.

## Blocages connus
1. ⏸ **`Z1 (0-30 km): .` sur `contactos.html`** — réparable sans invention (retrait de la phrase), mais **la zone est prise par la PR #264**. Rang 1 dès son merge.
2. 🛑 **`vimioso` — où fermer le `<header>` ?** Arbitrage d'une ligne. Voir §3.
3. 🛑 **GO périmètre — corruption `repar`→`arranj` sans limite de mot** : **523 occurrences / 258 fichiers** sur les 4 repos (CU 33/19). La partie « liens » est livrée sur CNR (#323) et ENR (#363) ; **CU n'a aucun `href` touché**. Le blocage porte sur `Parranjo`→`Preparação` : restauration *probable* mais **pas prouvable par un fichier sur disque**. **Un GO d'une ligne débloque les 523.**
4. 🛑 **`Você` — ~180 occurrences sur les 4 repos** (CU 15). Corpus INTERDIT `LECONS.md`. GO requis.
5. 🛑 **Batch (a) `Suplemento 30-50%` — 815 fichiers.** Attente GO.
6. 🛑 **Batch (b) / (b2) — questions de délai, 813 + 331 fichiers.** Attente GO.
7. ⚠️ **`https://***` résiduel : 5 occurrences dans `blog/canalizador-urgente-guia-completo.html`** — fichier de la **PR #269, toujours ouverte**. ⚠️ **La PR #268 réécrit la même ligne et y CONSERVE le `***`** : si elle merge en premier, elle republie la corruption. **Résolution par `git merge`, jamais rebase (R6)** : garder le contenu de #268 sur la ligne 26 et y restaurer `"https://schema.org","`.
8. ⚠️ **`streetAddress: "Trás-os-Montes, Portugal"`** sur `contactos.html` et `canalizador-frioes.html` — incohérent R5.
9. ℹ️ **`AGENTS.md` de CU ne porte pas de §NAP** — **rétrogradé en confort** (voir §Apprentissages). Ce n'était pas le blocage annoncé sur CNR.
10. ⚠️ **Aucune des CINQ familles de défauts de génération n'a de cause racine identifiée.** **La chaîne de génération de pages statiques mérite un audit dédié — c'est le point de levier le plus élevé des 4 repos.**
