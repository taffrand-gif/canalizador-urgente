# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-25
- Tâche prévue : **rang 3 — les meta descriptions à phrase dupliquée**. ✅ **Exécutée** (11 pages, et non 10).
- Tâche additionnelle : **vérifier l'hypothèse des « pages en double par accent »** posée le 24/08. ✅ **Hypothèse CONFIRMÉE, et bien plus grosse que la tâche prévue.**
- **1 PR ouverte** :
  - **#275** — https://github.com/taffrand-gif/canalizador-urgente/pull/275 — branche `loop/2026-08-25-cu-meta-dupliquee` — 12 commits, **11 fichiers de production** + `SEO_PLAN.md`
- État de #274 (run du 24/08) : **toujours ouverte**. 5 PR ouvertes, inchangé depuis le 24/08.

### 1. ⚠️ Le premier prédicat a rendu 0, et le 0 était faux
Le prédicat initial découpait la description en **phrases** et cherchait deux phrases égales → **0 sur 2453 pages**. Or le segment répété est un **sous-segment** : la première occurrence porte un préfixe (`…45€ deslocação, `) ou vit **entre parenthèses** (`carrazeda`). Aucune phrase n'est strictement égale à une autre.

Le 0 a été confronté au contenu réel d'une page nommée par le run du 24/08 → défaut du prédicat exposé en une commande. **Prédicat correct : le plus long SOUS-SEGMENT répété, pas la phrase répétée.**

**11 pages** (et non 10 — `canalizador-urgente-carrazeda-de-ansiães.html` manquait à la liste du 24/08). 3 formes distinctes. **Correction = suppression pure de la seconde occurrence**, aucun mot ajouté. **Témoin : 11 → 0 sur 2453 pages.**

### 2. 🔴 VERDICT — pages en double par accent : confirmé, et c'est le plus gros défaut d'indexation du repo

| Mesure | Valeur |
|---|---|
| Paires de chemins identiques **à l'accent près** | **179** |
| Paires byte-identiques | **0** — tous les md5 diffèrent |
| Paires avec **un seul** jumeau en `noindex,follow` (dedup correcte) | 172 |
| Paires avec **LES DEUX** jumeaux en `noindex` | **7** |
| Pages `noindex` issues de ces paires | **186** |
| **…dont présentes dans un sitemap** | **186 / 186** |

Aucune paire n'étant byte-identique, **la méthode de retrait mécanique EU #314 (md5 par bloc) ne s'applique pas.**

🔴 **Sept CONCELHOS n'ont aucune page indexable** (les deux jumeaux en `noindex`) : **Alijó · Carrazeda de Ansiães · Freixo de Espada à Cinta · Freixo de Numão · Mouçós · São João da Pesqueira · Tabuaço**. Ce sont des concelhos, pas des hameaux.

🔴 **Les 186 pages `noindex` sont listées dans les 4 sitemaps** (`sitemap.xml`, `sitemap-villages.xml`, `public/sitemap.xml`, `public/sitemap-villages.xml` ; `sitemap-villages.xml` = 1998 `<loc>` dont **180 accentuées**). C'est le signal **« Submitted URL marked 'noindex' »** de la Search Console : le sitemap demande l'indexation de pages qui la refusent.

## ✅ Gate merge — aucun gate actif
Vérifié ce run : **aucune mention d'attente de merge**. Aucun gate réécrit. 5 PR étaient ouvertes ; la #275 a été ouverte quand même.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Entre le 06/08 et le 09/08, « Attente GO merge (R7) » a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**. **Ne jamais réécrire un gate de ce type.**

## 🎯 FILE DE TÂCHES LOOP — état au 2026-08-25

| Rang | Cible | Statut |
|---|---|---|
| — | 11 meta descriptions à segment dupliqué | ✅ **traité ce run (#275)** |
| **1** | 🔴 **Ordre de merge #268 / #269** | 🛑 **ARBITRAGE — risque de RÉGRESSION.** La **#268 est toujours ouverte et réécrit la ligne 26 de `blog/canalizador-urgente-guia-completo.html` en y CONSERVANT le `***`** ; la **#269** corrige les 5 blocs `@context` masqués du même fichier. **Si #268 merge après #269, la corruption revient en production.** Signalé pour la **3ᵉ fois** (20/08, 24/08, 25/08). **Merger #268 d'abord, ou la rebaser.** |
| **2** | 🔴 **NOUVEAU — 186 URLs `noindex` présentes dans les 4 sitemaps** (186/186) | 🛑 **GO PÉRIMÈTRE.** Signal GSC « Submitted URL marked 'noindex' ». Suppression mécanique, zéro invention, mais 186 lignes × 4 fichiers **générés** → batch. ⚠️ **La vraie question est en amont : le générateur produit-il deux fichiers par localité par conception, ou est-ce un artefact ?** |
| **3** | 🔴 **NOUVEAU — 7 concelhos sans aucune page indexable** : Alijó · Carrazeda de Ansiães · Freixo de Espada à Cinta · Freixo de Numão · Mouçós · São João da Pesqueira · Tabuaço | 🛑 **ARBITRAGE d'une ligne** : lequel des deux jumeaux passe en `index` ? (Convention observée sur les 172 paires saines : **le jumeau SANS accent est l'indexable.**) **Sept concelhos hors index, c'est du chiffre d'affaires, pas de la conformité.** |
| **4** | 🔴 **`contactos.html` — `Z1 (0-30 km): . Z2 (31-50 km): . Z3 (51-90 km): . Z4 (91-130 km): .`** | ⏸ des valeurs de délai purgées ont laissé des deux-points suivis d'un point, **servis en clair au visiteur** sur une money page. Le **retrait de la phrase** est possible sans invention — mais la zone est **prise par la PR #264**. **Dès #264 mergée.** |
| **5** | **`garantimos atenção após contacto telefónico` — 20 occ / 9 fichiers, dont 6 en META DESCRIPTION** | ⏳ **aucun GO.** R145/R11 : promesse de garantie. Le run du 14/08 en a retiré une par **transplant verbatim** — le patron existe. ⚠️ **La moitié est en meta description : surface SERP.** **Meilleur rapport effort/valeur restant sans GO.** |
| **6** | 🛑 **5 fichiers portent DEUX blocs `FAQPage` avec les MÊMES questions** | 🛑 **ARBITRAGE.** Un bloc ancien (555 o) et un récent (766 o) énonçant les 4 engagements de `PRICING.md` verbatim. **Non byte-identiques** → le prédicat de retrait mécanique ne s'applique pas. Même situation que les deux `FAQPage` de `precos.html` sur ENR. **Question d'une ligne : garder le récent, retirer l'ancien ?** |
| **7** | **`Diagnóstico por telefone em poucos minutos` — 5 134 occurrences / 1 084 fichiers** | 🛑 **GO périmètre.** `poucos minutos` est déjà traité comme R145 (purgé de `calculadora-de-preco.html` le 14/08). **Le plus gros gisement de conformité du repo.** |
| **8** | **`canalizador-desentupimento-vimioso.html` — `<header>` jamais fermé** | 🛑 **point de fermeture indéterminé.** Trois invariants convergent et ne suffisent pas. **Un arbitrage d'une ligne suffirait** : « fermer le `<header>` après le `<p class="answer-first">` ». |
| **9** | **Corruption `repar`→`arranj` — 33 occ / 19 fichiers** | ⏳ **GO périmètre.** **Aucun `href` touché sur CU** : le défaut y est purement textuel. |
| **10** | **`Você` — 15 occ / ~13 fichiers** | 🛑 corpus INTERDIT, GO requis. ℹ️ **Chercher les doublons d'abord** : 4 sont tombés le 22/08 sans consommer le GO. |
| **11** | 🔴 **NOUVEAU — refaire la mesure `gratuit` avec PÉRIMÈTRE ET MOTIF ÉLARGIS** | ⏳ **Sur CNR ce run, le même prédicat est passé de « ~27 restantes » à 3822 occ / 1723 fichiers** — le compteur antérieur ne balayait qu'un sous-arbre avec un motif littéral. **Le compteur de CU a la même origine.** Une seule commande Python. |
| **12** | Les **2 variantes hybrides** de `Quanto custa a deslocação?` (`Z3: 35 € e 65 €/h`) | ⏳ 3 fichiers (`canalizador-meixedo`, `canalizador-gimonde`, `canalizador-gondesende`), motif unique, sans GO. |
| **13** | Requalifier `N% dos/das` **hors `_archive/`** | ⏳ 697 occ / 144 fichiers dont la moitié dans `_archive/`. ✅ `Sem custo extra de fim de semana` : 76 occ, **toutes dans `_archive/`** → **famille close.** |
| 14 | `streetAddress: "Trás-os-Montes, Portugal"` sur `contactos.html` + `canalizador-frioes.html` | ⏳ incohérent R5 — ce n'est pas une adresse |
| 15 | §NAP à `AGENTS.md` + `Sob marcação` à `PRICING.md` | ⏳ **RÉTROGRADÉ** — confort. |

## Tâche suivante recommandée
1. 🔴 **Poser les DEUX arbitrages d'une ligne qui valent le plus** :
   - rang 1 — **ordre de merge #268/#269** (risque de régression, 3ᵉ signalement) ;
   - rang 3 — **les 7 concelhos hors index** (convention observée : le jumeau sans accent est l'indexable).
2. **Rang 5 — `garantimos atenção após contacto telefónico`**, 9 fichiers, patron de transplant déjà validé le 14/08, dont 6 occurrences en **meta description**. **La meilleure tâche sans GO.**
3. **Rang 11 — remesurer `gratuit` avec périmètre et motif élargis.** Une commande, potentiellement deux ordres de grandeur.
4. **Rang 13 — requalifier `N% dos/das` hors `_archive/`.**
5. **Rang 4 dès #264 mergée.**

## Apprentissages (self-improving)
- 🔴 **NOUVEAU — « un contrôle qui rend 0 doit prouver sa source » a changé ce run.** Le prédicat « deux phrases égales » rendait 0 sur 2453 pages ; c'était un **faux négatif du prédicat**, pas un résultat. ➡️ **Quand un contrôle rend 0 sur une famille qu'un run antérieur a comptée NON VIDE, c'est le CONTRÔLE qui est en cause, pas la famille.** Coût de la vérification : une commande.
- 🔴 **NOUVEAU — duplication ≠ phrase répétée : c'est un SOUS-SEGMENT répété.** Découper en phrases suppose que la répétition respecte la ponctuation ; les préfixes et les parenthèses la brisent. **Prédicat robuste : « plus long sous-segment répété ».**
- 🔴 **NOUVEAU — vérifier une hypothèse laissée par le run précédent peut valoir plus que la tâche prévue.** La tâche valait 11 lignes ; l'hypothèse a sorti **179 paires, 186 URLs en conflit d'indexation, 7 concelhos hors index**. ➡️ **Traiter les « à vérifier » d'un `context.md` comme des tâches de plein droit, pas comme des notes.**
- 🔴 **NOUVEAU — la non-byte-identité ferme une méthode, pas le dossier.** Les 179 paires ne sont pas byte-identiques → EU #314 ne s'applique pas ; le défaut se traite ailleurs (sitemap, `noindex`, canonical). **Ne pas confondre « la méthode connue ne s'applique pas » et « il n'y a rien à faire ».**
- 🔴 **NOUVEAU (transposé de CNR) — un compteur de violation vaut ce que vaut son PÉRIMÈTRE, et le périmètre est presque toujours IMPLICITE.** **Ne jamais écrire « il en reste N » sans écrire sur quel arbre et avec quel motif.** Voir rang 11.
- 🔴 **Validité JSON ≠ validité schema.org.** 27 `"type"` au lieu de `"@type"` passaient `json.loads` et n'émettaient rien. **Deux contrôles distincts.**
- 🔴 **Un prédicat brut peut avoir 60 % de faux positifs.** « Numéro de téléphone dans un `name` » : légitime dans un `HowToStep`, anomalie dans une `Question`. **La requalification en lecture a divisé le périmètre par 2,5.**
- 🔴 **`_archive*` n'est pas de la production.** Toujours l'exclure — et **exclure `_archive-*` aussi**, pas seulement `_archive/` : ce repo porte `_archive-p1-fix-2026-07-16/`, `_archive-p1-prototype-2026-07-16/`, `_archive-wave2-refonte-2026-07-16/`. Un filtre sur `_archive/` seul les laisse passer.
- 🔴 **Ne retirer un doublon que s'il est byte-identique** (md5 par bloc, méthode EU #314).
- 🔴 **Le contrôle des PR ouvertes se fait AVANT de calculer le périmètre.** ⚠️ **Un titre de PR ne dit pas ce qu'elle couvre** — `gh pr view <n> --json files`.
- 🔴 **Quand un défaut récidive, chercher le GÉNÉRATEUR, pas la page.**
- 🔴 **La signature d'une corruption de batch, c'est le MOT INEXISTANT** — par diff des ensembles de mots.
- 🔴 **Le compteur R12 sur-compte** : R145 **autorise** `24h/7 dias`.
- **Ne pas sur-purger.** R4 se viole dans les deux sens.

## Edge cases détectés
- **Ce repo n'a QU'UN remote : `origin`.** (CNR est le seul des 4 à avoir `github` **et** `origin`.)
- ⚠️ **L'ancre du HISTORIQUE diffère d'un repo à l'autre, et ce repo en a TROIS** : `## 🔄 HISTORIQUE P0 (batch 04/07/2026)…` (L206), `## 🔄 HISTORIQUE` (L236, **la bonne**), `## 🔄 HISTORIQUE — 2026-07-03…` (L1312). **Insérer sur une correspondance EXACTE de ligne, jamais sur un `in` de sous-chaîne.**
- **`gh` et les credentials Git n'existent QUE sur le host macOS.** Reconfirmé ce run : `git push --dry-run` depuis le sandbox → `could not read Username for 'https://github.com'`. Répartition : lecture / grep / parsing Python / **écriture de fichiers** → sandbox ; `git` en écriture / `gh` → host.
- **Le `/tmp` du sandbox ≠ le `/tmp` du host.** Worktrees et `--body-file` sous `~/work/Sites/_worktrees/` ou `~/work/Sites/_loop-<date>/`. Le `--body-file` doit vivre **hors du worktree**.
- 🔴 **Un worktree n'est PAS un dépôt git vu depuis le sandbox** : `git show`/`diff`/`log` y rendent des **compteurs à zéro** trompeurs. **Tout témoin se compte en Python sur le CONTENU des fichiers.**
- ⚠️ **Ce repo a ~2450 pages hors archives.** Un `ls`/`find` non borné fait exploser la sortie. **Borner explicitement ce qu'on imprime.**
- 🔴 **`grep -P` n'existe pas sur macOS** ; **`grep -E` de macOS ne matche pas de façon fiable `ç`/`ã`/`õ`** ; **zsh ne fait pas de word-splitting** ; **`set -e` + glob vide fait avorter le script**. **Pour tout motif accentué : Python.**
- 🔴 **`git commit -m` multiligne est fragile en zsh** → `printf … | git commit -F -`. **ASCII dans les messages de commit, UTF-8 dans les fichiers.** Corps de PR : `--body-file`.
- ⚠️ **Les noms de fichiers accentués passent bien en argument `git add`** (vérifié ce run sur `canalizador-urgente-castelãos.html`), mais **la boucle `for f in $(git diff --name-only)` est fiable en zsh** — c'est bien zsh qui ne fait pas de word-splitting, ce qui protège ici.
- **Worktree obligatoire** (R-WT). **Jamais `reset --hard` / `checkout -- .` / `stash` / `clean`** sur le checkout partagé. Aucun `context.md` ne *prescrit* de `reset --hard`.

## Blocages connus
1. 🛑 **RANG 1 — ordre de merge #268 / #269. RISQUE DE RÉGRESSION EN PRODUCTION.** 3ᵉ signalement.
2. 🛑 **NOUVEAU — 186 URLs `noindex` dans les 4 sitemaps** (186/186). GO périmètre.
3. 🛑 **NOUVEAU — 7 concelhos sans aucune page indexable.** Arbitrage d'une ligne. **Impact commercial direct.**
4. ⏸ **`contactos.html`** — zone prise par #264.
5. 🛑 **Deux `FAQPage` par page sur 5 fichiers** — non byte-identiques, GO requis pour lever le prédicat de byte-identité.
6. 🛑 **`Diagnóstico por telefone em poucos minutos` — 5 134 occurrences.** GO périmètre.
7. 🛑 **`canalizador-desentupimento-vimioso.html`** — point de fermeture du `<header>` indéterminé.
8. 🛑 **GO périmètre — `repar`→`arranj`** : 523 occ / 258 fichiers sur les 4 repos.
9. 🛑 **`Você`** — corpus INTERDIT. GO requis.
10. 🛑 **Batch FAQ (~815 fichiers)** et **batch prix (~73)** de la PR #240 — périmètre parké. Rappel d'une ligne.
11. ⚠️ **La chaîne de génération de pages statiques reste non auditée.** Familles connues : `##style##` (CNR/CU/EU) · corps de page dupliqués (CU 2, ENR 3) · JSON-LD tronqué écrasant `<style>` (ENR) · JSX non compilé (CNR) · mutation `@context` (ENR) · perte du `<div>` ouvrant du bloc de liens internes (ENR) · `"type"` au lieu de `"@type"` (CU) · **et désormais la double génération accentuée / non accentuée (CU, 179 paires)**. **Huit familles, une chaîne. C'est le point de levier le plus élevé des 4 repos.**
