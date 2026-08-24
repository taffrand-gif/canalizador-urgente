# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-24
- Tâche prévue : rang 3 — le sweep `LECONS.md` passé en **étape fixe**.
- Tâche réellement exécutée : **la tâche prévue**. Elle a sorti un défaut qu'aucun contrôle du loop ne pouvait voir.
- **1 PR ouverte** :
  - **#274** — https://github.com/taffrand-gif/canalizador-urgente/pull/274 — branche `loop/2026-08-24-cu-sweep` — 12 commits, **11 fichiers de production** + `SEO_PLAN.md`
- ✅ **#273 a mergé** (le prologue de `contactos.html` est en production).

### 1. 🔴 Du JSON parfaitement valide qui n'émet AUCUNE donnée structurée
27 propriétés `"type"` au lieu de `"@type"` dans les blocs `ld+json` de **11 pages** — `Answer` ×22, `Organization` ×5.

Ces blocs **passent `json.loads`**. C'est exactement pourquoi ni le compteur de conformité, ni le balayage structurel du 23/08 ne les voyaient : **les deux ne testaient que la validité JSON.** `schema.org`, lui, exige `@type` — une propriété `type` nue n'est pas reconnue, donc **les réponses de FAQ et les éditeurs de ces 11 pages n'étaient pas rattachés au graphe**.

🔴 **Validité JSON ≠ validité schema.org. Le loop n'avait que le premier contrôle.**

**Témoin d'unanimité** : avant patch, **toutes** les autres occurrences du dépôt écrivaient déjà `"@type"`. Après patch : `"type"` nu = **0 sur tout le dépôt**.

### 2. 🔴 Cinq noms de Question de FAQ corrompus, servis aux crawlers
`Atendem Atendimento — ligue 928 484 451/7d?` (×3) et `Atendem Atendemos 24h/7d?` (×2) : **un numéro de téléphone injecté au milieu d'un intitulé de question**, artefact d'une purge automatisée antérieure.

Restaurés depuis le **jumeau intact du même fichier** : chacun de ces 5 fichiers porte un **premier** bloc `FAQPage`, **deux lignes plus haut**, avec `Atendem 24h/7d?`. Donneur à distance de deux lignes → zéro invention.

### 3. Le prédicat brut avait 60 % de faux positifs
« Nom de nœud contenant un numéro de téléphone » sortait **10 fichiers**. **Six étaient des noms d'étapes `HowToStep`** (`Ligue 928 484 451 e descreva os sintomas`, `Ligue 928 484 451 em segurança`, `Documentar com foto e ligar 928 484 451`), où le numéro est légitime.

➡️ **Un numéro dans un `name` n'est une anomalie que si le `name` est celui d'une `Question`.** La requalification en lecture a divisé le périmètre par 2,5.

## ✅ Gate merge — aucun gate actif
Vérifié ce run : **aucune mention d'attente de merge**. Aucun gate réécrit. 5 PR étaient ouvertes ; la #274 a été ouverte quand même.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Entre le 06/08 et le 09/08, « Attente GO merge (R7) » a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**. **Ne jamais réécrire un gate de ce type.**

## 🎯 FILE DE TÂCHES LOOP — état au 2026-08-24

| Rang | Cible | Statut |
|---|---|---|
| — | 27 `"type"` → `"@type"` + 5 noms de Question restaurés (11 pages) | ✅ **traité ce run (#274)** |
| **1** | 🔴 **Ordre de merge #268 / #269** | 🛑 **ARBITRAGE — risque de régression.** La **#268 est toujours ouverte et réécrit la ligne 26 de `blog/canalizador-urgente-guia-completo.html` en y CONSERVANT le `***`**. La **#269** corrige les 5 blocs `@context` masqués du même fichier. **Si #268 merge après #269, la corruption revient en production.** Signalé pour la 2ᵉ fois (déjà le 20/08). **Merger #268 d'abord, ou la rebaser.** |
| **2** | 🔴 **`contactos.html` — `Z1 (0-30 km): . Z2 (31-50 km): . Z3 (51-90 km): . Z4 (91-130 km): .`** | ⏸ **des valeurs de délai purgées ont laissé des deux-points suivis d'un point, servis en clair au visiteur** sur une money page. Le **retrait de la phrase** est possible sans invention (R4/R145 interdisent d'y écrire un délai) — mais la zone est **prise par la PR #264**. **Dès #264 mergée.** |
| **3** | **10 pages à meta description dont une phrase entière est répétée deux fois** | ⏳ **aucun GO, petit périmètre, surface SERP.** `canalizador-travancas` · `canalizador-grijo-de-parada` · `canalizador-urgente-castelaos` · `canalizador-urgente-castelãos` · `canalizador-urgente-cortiços` · `canalizador-urgente-açoreira` · `canalizador-urgente-acoreira` · `public/canalizador-urgente-podence` · `public/canalizador-urgente-corticos` · `distritos/braganca`. **Prédicat : phrase de plus de 25 caractères présente 2 fois dans la même `<meta name="description">`.** ⚠️ Le doublon de `castelaos`/`castelãos` et `acoreira`/`açoreira` suggère aussi un **problème de pages en double par accent** — à vérifier. |
| **4** | **`garantimos atenção após contacto telefónico` — 20 occ / 9 fichiers de production, dont 6 en META DESCRIPTION** | ⏳ **aucun GO.** R145/R11 : promesse de garantie. Le run du 14/08 en a déjà retiré une sur `zona-intervencao.html` **par transplant verbatim** d'une réponse conforme du même repo — le patron existe. ⚠️ **La moitié des occurrences sont en meta description : surface SERP, pas seulement JSON-LD.** |
| **5** | 🛑 **Les 5 fichiers du run portent DEUX blocs `FAQPage` avec les MÊMES questions** | 🛑 **ARBITRAGE.** Un bloc ancien (555 o, « Telefone 928 484 451. ») et un récent (766 o) qui énonce les **4 engagements de `PRICING.md` verbatim**. **Non byte-identiques**, donc le prédicat de retrait mécanique (md5 par bloc, méthode EU #314) **ne s'applique pas**. Même situation que les deux `FAQPage` de `precos.html` sur ENR. **Question d'une ligne : garder le récent, retirer l'ancien ?** Le prédicat de segments >45 caractères est déjà passé et **il autorise le retrait de l'ancien** — mais la doctrine du repo exige la byte-identité, donc **GO requis pour lever le prédicat**. |
| **6** | **`Diagnóstico por telefone em poucos minutos` — 5 134 occurrences / 1 084 fichiers** | 🛑 **GO périmètre.** `poucos minutos` est déjà traité comme R145 (purgé de `calculadora-de-preco.html` le 14/08). **À cette échelle c'est le plus gros gisement de conformité du repo.** |
| **7** | **`canalizador-desentupimento-vimioso.html` — `<header>` jamais fermé** | 🛑 **point de fermeture indéterminé.** Trois invariants convergent (70/70, 66/77, 69/70) et **ne suffisent pas** : vimioso n'a ni le CTA de fermeture, ni `<main>`, et porte un bloc « HERO BOX » qu'aucun des 70 jumeaux ne possède. **Un arbitrage d'une ligne suffirait** : « fermer le `<header>` après le `<p class="answer-first">` ». |
| **8** | **Corruption `repar`→`arranj` — 33 occurrences / 19 fichiers** | ⏳ **GO périmètre.** **Aucun `href` touché sur CU** : le défaut y est purement textuel. |
| **9** | **`Você` — 15 occurrences / ~13 fichiers** | 🛑 corpus INTERDIT, GO requis. ℹ️ **Chercher les doublons d'abord** : 4 sont tombés le 22/08 sans consommer le GO. |
| **10** | Les **2 variantes hybrides** de `Quanto custa a deslocação?` (`Z3: 35 € e 65 €/h`) | ⏳ **3 fichiers de production** (`canalizador-meixedo`, `canalizador-gimonde`, `canalizador-gondesende`), motif unique, sans GO. Recompté ce run. |
| **11** | Chercher sur CU les défauts trouvés sur EU : `N% dos/das` et `Sem custo extra de fim de semana` | ⏳ **mesuré ce run** : `N% dos/das` = **697 occ / 144 fichiers** (dont la moitié dans `_archive/`, hors production) ; `Sem custo extra de fim de semana` = **76 occ / 26 fichiers, TOUS dans `_archive/`** → **non-violation en production, famille close.** Reste à requalifier le `N% dos/das` **hors `_archive/`**. |
| **12** | `streetAddress: "Trás-os-Montes, Portugal"` sur `contactos.html` + `canalizador-frioes.html` | ⏳ incohérent R5 — ce n'est pas une adresse |
| 13 | Ajouter un **§NAP à `AGENTS.md`** et `Sob marcação` à `PRICING.md` | ⏳ **RÉTROGRADÉ** — confort, pas préalable. |

## Tâche suivante recommandée
1. **Rang 3 — les 10 meta descriptions à phrase dupliquée.** Aucun GO, petit périmètre, surface SERP. **Vérifier en même temps l'hypothèse des pages en double par accent** (`castelaos`/`castelãos`, `acoreira`/`açoreira`) : si elle se confirme, c'est un défaut de canonicalisation, bien plus gros que les meta.
2. **Rang 4 — `garantimos atenção após contacto telefónico`**, 9 fichiers, patron de transplant déjà validé le 14/08.
3. **Poser les trois questions d'une ligne** : ordre de merge #268/#269 (rang 1, **risque de régression**), retrait du `FAQPage` ancien (rang 5), fermeture du `<header>` de vimioso (rang 7).
4. **Rang 11 — requalifier `N% dos/das` hors `_archive/`.**
5. **Ne PAS relancer le balayage structurel HTML sur CU** : 3 fichiers sur 2 454, la famille est close. **Mais y ajouter le contrôle `@type`** (voir Apprentissages) et le repasser une fois à ce titre.

## Apprentissages (self-improving)
- 🔴 **NOUVEAU — validité JSON ≠ validité schema.org, et le loop n'avait que le premier contrôle.** 27 nœuds passaient `json.loads` sans porter de `@type` : le JSON est valide, la donnée structurée est nulle. ➡️ **Ajouter au balayage structurel un contrôle SÉMANTIQUE : tout objet d'un bloc `ld+json` doit porter `@type`.** Deux contrôles, pas un. Un bloc « valide » peut n'émettre aucune donnée.
- 🔴 **NOUVEAU — un prédicat brut peut avoir 60 % de faux positifs et rester utile, à condition de requalifier EN LECTURE avant de patcher.** « `name` contenant un numéro » sortait 10 fichiers, 6 étaient des `HowToStep` légitimes. **La requalification a divisé le périmètre par 2,5.** Elle n'est pas une formalité.
- 🔴 **NOUVEAU — le donneur le plus sûr est le jumeau le plus PROCHE.** Les 5 noms corrompus avaient leur version saine **deux lignes plus haut, dans le même fichier**. ➡️ **Chercher le donneur dans le fichier avant de le chercher dans le dépôt.** (Corollaire du 23/08 sur ENR : la valeur `@context` manquante était aussi dans le même fichier.)
- 🔴 **NOUVEAU — le témoin d'unanimité transforme une opinion en preuve.** « Il faut écrire `@type` » est une opinion ; « 0 occurrence de `type` nu dans tout le dépôt après patch » est un fait. Même méthode que le DOCTYPE le 23/08 (2 454/2 454).
- 🔴 **NOUVEAU — `_archive/` fausse tous les compteurs.** `Sem custo extra de fim de semana` rendait 76 occurrences ; **les 76 sont dans `_archive/`**, donc **zéro violation en production**. ➡️ **Exclure `_archive/` de tout compteur de conformité**, et le dire dans le rapport. Sans cette exclusion, une famille close ressemble à un gisement.
- 🔴 **Un balayage structurel de TOUT le dépôt coûte une commande et vaut mieux qu'un sweep de motifs.** ➡️ Étape fixe sur les 4 repos : équilibre des balises + validité JSON-LD + **présence de `@type` sur chaque objet** + doublons byte-à-byte + DOCTYPE + `<html lang>`.
- 🔴 **Le dépôt entier est le meilleur juge de ce qui manque à un fichier.** **Avant de restaurer, compter la population. L'unanimité tranche.**
- 🔴 **Ne pas fermer une balise au jugé.** Trois quasi-preuves ne font pas une preuve. **Consigner bat deviner.**
- 🔴 **Un résultat NÉGATIF est un résultat.** 3 fichiers sur 2 454 ; 76 occurrences toutes archivées. Le savoir évite de relancer la chasse.
- 🔴 **Un compteur de balises ÉQUILIBRÉ peut signaler une duplication, pas une santé.** Compter les balises **uniques par document** (`<h1>`, `<header>`, `<main>`), pas seulement leur équilibre.
- 🔴 **Avant de patcher une chaîne interdite, chercher si elle vit dans un DOUBLON.** Appliqué ce run : les 5 noms corrompus vivent bien dans un bloc dupliqué — mais **les deux blocs ne sont pas byte-identiques**, donc le retrait mécanique n'est pas permis. **On patche la chaîne ET on consigne le bloc.**
- 🔴 **Prouver qu'une suppression ne perd rien AVANT de supprimer.** Segmenter sur `</li|p|td|h2|h3>`, vérifier que chaque segment > 45 caractères se retrouve dans la copie conservée. Le prédicat est passé ce run sur le `FAQPage` ancien et **il autorise son retrait** — mais la doctrine du repo exige en plus la byte-identité, donc GO.
- 🔴 **« Valeur non sourçable » se PROUVE en remontant la chaîne de définition.** Distinguer « aucune source » de « source pas encore cherchée ».
- 🔴 **Ventiler par famille avant de choisir le périmètre** (leçon CNR #327) : chercher le **sous-ensemble homogène**, c'est lui qui rend le contrôle exhaustif possible en une commande.
- 🔴 **Un défaut DÉJÀ RÉPARÉ qui revient est un générateur non corrigé** (leçon ENR #371). `git log -S <motif>` avant de patcher.
- 🔴 **Un GO peut devenir inutile si on attaque le défaut au bon niveau.**
- 🔴 **Un « TODO post-merge » écrit dans `LECONS.md` n'est exécuté par personne.** ➡️ **Étape FIXE du loop, pas recommandation.** Appliqué ce run — et le sweep a payé.
- 🔴 **Quand un défaut RÉCIDIVE, chercher le GÉNÉRATEUR, pas la page.** ⚠️ **La chaîne de génération a maintenant produit SIX familles de défauts distinctes sur les 4 repos** : marqueurs `##style##`, corps de page dupliqués, JSON-LD tronqué écrasant un `<style>` (ENR), JSX non compilé (CNR), prologue de document absent (CU), **mutation `@context` (ENR + CU)**. **Un audit du générateur rapporterait plus que la somme des correctifs.**
- 🔴 **Une PR qui répare un fichier ne répare pas sa famille.** Repasser le contrôle sur l'ensemble du motif de nom.
- 🔴 **Un titre de PR ne dit pas ce que la PR couvre.** **6ᵉ run consécutif** que `gh pr view <n> --json files` évite un conflit.

## Edge cases détectés
- **Ce repo n'a QU'UN remote : `origin`.**
- 🔴 **`_audit/LECONS.md` leçon #407 (18/07)** : le filtre sandbox Hermes mute `https://schema.org","@type":` en `https://***@type":`. **Le même défaut existe sur ENR** (`LECONS.md` L#003, 28/07). ➡️ **Écrire les JSON-LD en Python pur, jamais en heredoc shell ni via un tool runtime, et contrôler le BLOB git après commit.**
- **`gh` et les credentials Git n'existent QUE sur le host macOS.** Répartition : lecture / grep / parsing Python / **écriture de fichiers** → sandbox `mcp__workspace__bash` ; `git` en écriture / `gh` → `mcp__desktop-commander__start_process`.
- **Le `/tmp` du sandbox ≠ le `/tmp` du host.** Un `--body-file` de PR doit être écrit sous `~/work/Sites/_worktrees/`, jamais dans `/tmp`. **Et il faut le supprimer après le `gh pr create`.**
- 🔴 **Un worktree n'est PAS un dépôt git vu depuis le sandbox** : `git show`/`diff`/`log` y rendent des **compteurs à zéro** trompeurs. ➡️ **Tout témoin se compte en Python sur le CONTENU des fichiers.**
- ⚠️ **Borner explicitement ce qu'on imprime** en balayant ~2 900 fichiers : un dict d'exemples fait exploser la sortie.
- 🔴 **`grep -P` n'existe pas sur macOS** ; **`grep -E` de macOS ne matche pas de façon fiable les accents** (faux négatif silencieux observé sur CNR ce run) ; **`grep -c '***'` échoue en zsh**. **Pour tout motif accentué ou non trivial : Python.**
- 🔴 **`git commit -m` multiligne est fragile en zsh** → `printf … | git commit -F -`. **Préférer l'ASCII dans les messages de commit**, l'UTF-8 dans les fichiers. Corps de PR : `--body-file`, jamais `--body` inline.
- **Boucle de commits atomiques** : `for f in $(git diff --name-only); do git add "$f"; … git commit -F -; done` respecte « 1 fichier = 1 commit » sans un appel d'outil par fichier.
- **Worktree obligatoire** (R-WT). **Jamais `reset --hard` / `checkout -- .` / `stash` / `clean`** sur le checkout partagé. Aucun `context.md` ne *prescrit* de `reset --hard`.

## Blocages connus
1. 🛑 **RANG 1 — risque de RÉGRESSION : la PR #268 republierait la corruption `@context` que la #269 corrige.** Signalé pour la 2ᵉ fois (déjà le 20/08). **Ordre de merge à arbitrer.**
2. 🛑 **Retrait du `FAQPage` ancien sur 5 pages** — le prédicat de segments l'autorise, la doctrine de byte-identité ne le permet pas. **GO d'une ligne.**
3. 🛑 **Fermeture du `<header>` de `canalizador-desentupimento-vimioso.html`** — point indéterminé. **GO d'une ligne.**
4. 🛑 **GO périmètre — `Diagnóstico por telefone em poucos minutos`** : 5 134 occurrences / 1 084 fichiers. Le plus gros gisement du repo.
5. 🛑 **GO périmètre — corruption `repar`→`arranj`** : 33 occ / 19 fichiers sur CU, 523 sur les 4 repos.
6. 🛑 **`Você`** — corpus INTERDIT, GO requis. **Chercher les doublons d'abord.**
7. ⏸ **`contactos.html` `Z1 (0-30 km): .`** — pris par la PR #264.
8. 🛑 **Batch FAQ (~815 fichiers)** et **batch prix (~73)** de la PR #240 — périmètre parké. Rappel d'une ligne.
9. ⚠️ **La chaîne de génération de pages statiques reste non auditée : SIX familles de défauts distinctes lui sont désormais imputables sur les 4 repos.** C'est le point de levier le plus élevé.
