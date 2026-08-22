# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-22
- Tâche prévue : rangs 1 et 2 de la file du 21/08 — sweep `LECONS.md` + les 3 chaînes françaises du corpus INTERDIT.
- Tâche réellement exécutée : **les deux rangs, qui se sont révélés être le MÊME défaut sur un seul fichier.**
- **1 PR — ✅ MERGÉE PENDANT LE RUN** :
  - **#271** — https://github.com/taffrand-gif/canalizador-urgente/pull/271 — branche `loop/2026-08-22-cu-chaines-francaises` — 2 commits, 1 fichier de production + `SEO_PLAN.md`
  - **Présence en production vérifiée** : `git log --oneline` sur `origin/main` porte `0cbc2efb1 … (#271)`. (Contrôle par `(#N)` dans le log — `merge-base --is-ancestor` est faux sur un squash.)

### 🔴 `comparacao.html` contenait DEUX copies complètes de son corps de page
Chacune avec son propre `<header>`, `<h1>`, `<main>` et `<section>` : **L27 (périmée, corrompue) et L29 (corrigée)**. Les deux portent exactement les **mêmes 7 `<h2>`**.

**Contrôle décisif avant patch** — les **seuls** segments présents dans L27 et absents de L29 :
```
• Marque grande nationale: Marcas como EDP, Galp têm mais recursos para grandes obras
• Disponbilidade peças raras: Para marcas exóticas, pode haver délai
• Você precisa de uma marca national (psicologia de marca
• Você tem uma garantia contratual spécifique com outra empresa
• Você precisa de cobertura 100% nationale (Atendemos 24h/7d em Trás-os-Montes
• Você parle uniquement anglais ou français (no futuro
• Compare vous-même. Premier service garanti satisfait ou refait gratuitement.
```
Sept fragments, et **rien d'autre** : les 3 chaînes françaises interdites, les 4 `<li>` en pt-BR `Você` à **parenthèse non fermée** (phrases tronquées, servies telles quelles), et un CTA portant une **garantie non sourcée** (R4/R11).

➡️ **Le correctif n'était pas de rapiécer L27, c'était de la supprimer.** Zéro perte de contenu, prouvée segment par segment. Les 3 chaînes sont tombées **avec** les 4 `Você` — **sans consommer le GO du batch `Você`**, puisqu'il s'agit d'une déduplication et non d'une réécriture de pronom.

- **Témoins R8** (avant mesuré sur `origin/main` intact) : `Marque grande` **1→0** · `satisfait ou refait` **1→0** · `parle uniquement` **1→0** · `Compare vous-même` **1→0** · `Você` **4→0** · `délai`/`spécifique`/`nationale` **4→0** · `Marca grande nacional` **1→1** (préservée) · `<h1>` **2→1** · `<header>` **2/2→1/1** · `<main>` **2/1→1/1** · `<section>` **3/2→2/2** · `<div>` 17/17→10/10 · `<li>` 41/41→22/22.
- Contrôle PR ouvertes avant patch : 4 PR (#269, #268, #264, #243), `comparacao.html` **non pris**.

### Propagation vérifiée sur les 4 repos
| Repo | `<h1>` | `<main>` | `<section>` | État |
|---|---:|---:|---:|---|
| CU | 2 → 1 | 2/1 → 1/1 | 3/2 → 2/2 | ✅ **corrigé ce run (#271)** |
| **ENR** | **3** | **3 / 1** | **3 / 1** | 🛑 **trois copies — mais le fichier est pris par la PR #348** |
| CNR | 1 | 1/1 | 1/1 | ✅ propre |
| **EU** | — | — | — | ⏳ **non contrôlé — à faire au prochain run** |

## ✅ Gate merge — aucun gate actif
Vérifié ce run : **aucune mention d'attente de merge** dans les 4 `context.md`. Aucun gate réécrit.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Une PR en attente ne gèle pas le repo — la #269 est ouverte depuis le 20/08 et n'a empêché ni la #270 ni la #271. Entre le 06/08 et le 09/08, la mention « Attente GO merge (R7) » a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**. **Ne jamais réécrire un gate de ce type.**

## 🎯 FILE DE TÂCHES LOOP — état au 2026-08-22

| Rang | Cible | Statut |
|---|---|---|
| — | `comparacao.html` : copie périmée, 3 chaînes françaises, 4 `Você`, garantie non sourcée | ✅ **traités ce run — #271 MERGÉE, en production** |
| **1** | **Contrôler `comparacao.html` d'EU** avec la même méthode | ⏳ **PROCHAINE TÂCHE, sans GO.** Non contrôlé ce run. CU en avait 2 copies, ENR 3, CNR 0 — **EU est le dernier angle mort de la famille.** |
| **2** | **Le reste du sweep `LECONS.md`** | ⏳ sans GO. Le sweep du 21/08 a couvert 10 motifs et livré une cause racine ; `LECONS.md` (904 lignes) en contient d'autres. **Meilleur rapport effort/résultat, 3 runs de suite.** |
| **3** | **Corruption `repar`→`arranj` — 33 occurrences / 19 fichiers sur CU** | ⏳ **GO périmètre.** Voir §Blocages n°1. **Aucun `href` touché sur CU** : le défaut y est purement textuel. |
| **4** | **`Você` — 15 occurrences / ~13 fichiers restants** (19/14 avant ce run, −4 sur `comparacao.html`) | 🛑 corpus INTERDIT, GO requis (180 sur les 4 repos). ℹ️ **Chercher les doublons d'abord** : 4 sont tombés ce run sans consommer le GO. |
| **5** | Les **2 variantes hybrides** de `Quanto custa a deslocação?` (`Z3: 35 € e 65 €/h`) | ⏳ 2 fichiers, motif unique, sans GO |
| **6** | Les **6 réponses de `Atendem 24h/7d?`** portant `garantimos atenção após contacto telefónico` | ⏳ sans GO |
| **7** | Chercher sur CU les défauts trouvés sur EU : statistiques non sourcées (`N% dos/das`) et `Sem custo extra de fim de semana` | ⏳ sans GO |
| **8** | Ajouter un **§NAP à `AGENTS.md`** et `Sob marcação` à `PRICING.md` | ⏳ **remonté en priorité** : le même manque bloque **19 pages sur CNR** ce run (JSX brut, CTA morts, valeur du téléphone non sourçable). Une ligne, et elle rend applicable la règle #142 sur deux repos. |

## Tâche suivante recommandée
1. **Rang 1 — `comparacao.html` d'EU**, méthode de ce run : hacher les copies, prouver l'absence de perte, supprimer la périmée. Le fichier est **pris par une PR ouverte sur EU** — contrôler avant.
2. **Rang 8 — le §NAP dans `AGENTS.md`** : une ligne, et elle débloque 19 pages sur CNR.
3. **Rang 2 — continuer le sweep `LECONS.md`.** Trois runs de suite, c'est ce qui produit le plus par unité d'effort.
4. **Rangs 5 à 7** — tous sans GO.
5. **Si GO (g)** : les 38 fichiers `orçamento escrito é gratuito` (prototype en revue, PR #267).

## Apprentissages (self-improving)
- 🔴 **NOUVEAU — un compteur de balises ÉQUILIBRÉ peut signaler une duplication, pas une santé.** `<header>` 2/2 et `<h1>` 2/2 étaient parfaitement équilibrés — c'est-à-dire **dupliqués**. Seul `<main>` 2/1 trahissait quelque chose. ➡️ **Compter les balises uniques par document (`<h1>`, `<header>`, `<main>`), pas seulement leur équilibre. Un `<h1>` à 2 est toujours un défaut, même parfaitement fermé.**
- 🔴 **NOUVEAU — avant de patcher une chaîne interdite, chercher si elle vit dans un DOUBLON.** Patcher les 3 chaînes une par une aurait « corrigé » la copie périmée et laissé la page avec deux `<h1>` et un `<main>` non fermé : **un correctif qui aggrave.** Le diff entre les deux copies a donné la réponse en une commande. Même famille que « quand un défaut récidive, chercher le générateur » : le bon niveau n'est ni la chaîne ni la page, **c'est le bloc**.
- 🔴 **NOUVEAU — prouver qu'une suppression ne perd rien, AVANT de supprimer.** Méthode : segmenter la copie à retirer sur `</li|p|td|h2|h3>`, vérifier que chaque segment > 45 caractères se retrouve dans la copie conservée. Les 7 exceptions étaient exactement les 7 défauts. Sans ce contrôle, la suppression aurait été un pari.
- 🔴 **NOUVEAU — un GO peut devenir inutile si on attaque le défaut au bon niveau.** Les 4 `Você` de cette page attendaient un arbitrage depuis le 21/08 ; ils sont partis sans qu'aucune décision de pronom n'ait été prise. ➡️ **Avant de dépenser un arbitrage, vérifier que les occurrences ne sont pas dans du mort.**
- 🔴 **NOUVEAU — `comparacao.html` est un gabarit partagé entre les sites, et il se duplique** (CU 2, ENR 3, CNR 1). **La cause génératrice n'est pas identifiée** — probablement un script d'enrichissement qui ré-injecte le corps sans vérifier sa présence. À retrouver, comme pour le NAP parasite du 21/08.
- 🔴 **Un « TODO post-merge » écrit dans `LECONS.md` n'est exécuté par personne.** ➡️ **Le passage des signatures de `LECONS.md` doit être une étape FIXE du loop, pas une recommandation.**
- 🔴 **Quand un défaut RÉCIDIVE, la page n'est pas le bon niveau de correction : chercher le GÉNÉRATEUR.** ➡️ Avant de nettoyer une occurrence en série, grepper le motif dans `tools/`, `scripts/` et toute la chaîne de build.
- 🔴 **Un marqueur de gabarit non substitué n'apparaît dans aucun compteur.** Contrôle : `grep -rIoE '##[a-zA-Z_]{3,}##'`, **et sa famille élargie** (`{{…}}`, `%%…%%`, `__…__`, `${…}`) — sur CNR cet élargissement a fait passer le résultat de 4 à 76 occurrences.
- 🔴 **Une PR qui répare un fichier ne répare pas sa famille.** ➡️ **Repasser le contrôle sur l'ensemble du motif de nom.** Appliqué sur EU ce run : 79 fichiers scannés, 6 anormaux, famille close.
- 🔴 **Un titre de PR ne dit pas ce que la PR couvre.** Sur ENR ce run, la #348 intitulée « supprime les promesses de délai (R145) » prend `comparacao.html`. **4ᵉ run consécutif** que `gh pr view <n> --json files` évite un conflit.
- 🔴 **Quand `AGENTS.md` ne porte pas la valeur canonique, une règle qui l'invoque est inapplicable.** Le constater et **corriger `AGENTS.md`**, plutôt que recopier depuis un HTML (#142).
- 🔴 **La signature d'une corruption de batch, c'est le MOT INEXISTANT.**
- 🔴 **Un batch de conformité peut corrompre la RÈGLE qu'il applique** (`fb9dd2415`). Tout batch doit exclure `AGENTS.md`, `SEO_PLAN.md`, `context.md`, `CLAUDE.md`, `LECONS.md`. Avant d'escalader une contradiction : `git log -S "<fragment>" -- AGENTS.md`.
- 🔴 **Le compteur R12 sur-compte** : R145 **autorise** `24h/7 dias`.
- **Ne pas sur-purger.** R4 se viole dans les deux sens.

## Edge cases détectés
- **`gh` et les credentials Git n'existent QUE sur le host macOS.** Sandbox : `git fetch` OK, **`git push` impossible**. **Répartition** : lecture / grep / parsing Python / **écriture de fichiers** → sandbox ; `git` en écriture / `gh` → `mcp__desktop-commander__start_process`.
- **Le `/tmp` du sandbox ≠ le `/tmp` du host.** Worktrees sous `~/work/Sites/_worktrees/loop-YYYY-MM-DD/`.
- 🔴 **NOUVEAU — un worktree n'est PAS un dépôt git vu depuis le sandbox** : son `.git` est un fichier pointant vers un chemin macOS. `git show`/`git diff`/`git log` y **échouent** depuis `mcp__workspace__bash`, et un `python3` qui lit leur stdout renvoie des compteurs **à zéro** qui ressemblent à un résultat. **Vérifié ce run : un témoin `<section>` 3/2 a été lu `0/0`.** ➡️ **Tout « avant » mesuré par git se prend depuis le host.**
- 🔴 **NOUVEAU — `comparacao.html` est à la RACINE sur CU**, dans `client/public/` sur CNR et ENR. Ne pas présumer de l'arborescence entre repos : `find . -name '<fichier>'` avant tout.
- 🔴 **Le filtre sandbox qui mute `https://schema.org` est COSMÉTIQUE à l'affichage** mais **`https://***` sur disque est un vrai défaut** : distinguer en relisant les octets, pas la sortie du terminal.
- 🔴 **`grep -P` n'existe pas sur macOS** ; **zsh ne fait pas de word-splitting**. Pour tout motif non trivial : **Python**.
- 🔴 **`git commit -m` multiligne est fragile en zsh** → `git commit -F -`. Corps de PR : `--body-file`.
- **Worktree obligatoire** (R-WT). **Jamais `reset --hard` / `checkout -- .` / `stash` / `clean`** sur le checkout partagé. Vérifié ce run : checkout partagé sur `feat/cu-rankpush-canalizador-urgente-t_a9810c1c`, **32 fichiers non commités** — non touché.

## Blocages connus
1. 🛑 **GO périmètre — corruption `repar`→`arranj` sans limite de mot** : **523 occurrences / 258 fichiers** sur les 4 repos (CU 33/19). La partie « liens » est livrée sur CNR (#323) et ENR (#363) ; **CU n'a aucun `href` touché**. Le blocage porte sur `Parranjo`→`Preparação` : restauration *probable* mais **pas prouvable par un fichier sur disque** → hors R4 sans arbitrage. **Un GO d'une ligne débloque les 523.**
2. 🛑 **`Você` — ~180 occurrences sur les 4 repos** (CU 15 après ce run). Corpus INTERDIT `LECONS.md`. GO requis.
3. 🛑 **Batch (a) `Suplemento 30-50%` — 815 fichiers.** Attente GO.
4. 🛑 **Batch (b) / (b2) — questions de délai, 813 + 331 fichiers.** Attente GO.
5. ⚠️ **`https://***` résiduel : 5 occurrences dans `blog/canalizador-urgente-guia-completo.html`** — fichier de la **PR #269, toujours ouverte**. ⚠️ **La PR #268 réécrit la même ligne et y CONSERVE le `***`** : si elle merge en premier, elle republie la corruption. **Résolution par `git merge`, jamais rebase (R6)** : garder le contenu de #268 sur la ligne 26 et y restaurer `"https://schema.org","`.
6. ⚠️ **`contactos.html` + `canalizador-frioes.html`** : `streetAddress: "Trás-os-Montes, Portugal"` — incohérent R5 (ce n'est pas une adresse).
7. ⚠️ **`AGENTS.md` de CU ne porte toujours pas de §NAP** (rang 8). Le même manque bloque **19 pages sur CNR** ce run.
8. ⚠️ **La cause racine du batch `repar`→`arranj` n'est pas identifiée**, et **celle des duplications de corps de page non plus**. **Trois défauts de duplication distincts en deux runs : la chaîne de génération de pages statiques mérite un audit dédié.**
