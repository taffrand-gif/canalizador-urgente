# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-27
- Tâches exécutées : **rang 4** (`contactos.html`, énumération de zones amputée) ✅ · **rang 12** (2 variantes hybrides de `Quanto custa a deslocação?`, 3 fichiers) ✅
- Verdicts livrés : **rang 11** (re-mesure `gratuit` élargie) ✅ · **rang 1** (risque de régression `***`) ✅ **CLOS**
- **1 PR ouverte** :
  - **#277** — https://github.com/taffrand-gif/canalizador-urgente/pull/277 — branche `loop/2026-08-27-cu-contactos-zonas-orphelines` — 5 commits, **4 fichiers de production** + `SEO_PLAN.md`
- Branche partie de `origin/main` = `1d7e08b94`.

### 🟢 ÉVÉNEMENT MAJEUR DU RUN — le stock de PR est vide
`gh pr list --state open` rend **0 PR ouverte sur les 4 repos**. Sur CU, #264 → #276 ont toutes mergé.

### 1. 🔴 RANG 1 CLOS — le risque de régression est éteint
Signalé **trois fois** (20/08, 24/08, 25/08) : « si #268 merge après #269, la corruption `***` revient en production ».

**#268 a été FERMÉE sans merge le 26/08** ; #269 a mergé le 26/08. Contrôle sur `blog/canalizador-urgente-guia-completo.html` : **0 occurrence de `***`**, **5 blocs `"@context":"https://schema.org"` tous valides**. **Le rang 1 sort de la file.**

### 2. Rang 4 — le correctif d'une purge ratée est un RETRAIT, pas une restauration
Des valeurs de délai purgées au titre de **R145** avaient laissé `Depende da zona. Z1 (0-30 km): . Z2 (31-50 km): . Z3 (51-90 km): . Z4 (91-130 km): .` servi **en clair au visiteur** sur une money page.

**Aucun donneur** : cette réponse n'existe qu'**une fois sur 2 534 fichiers**. Reconstruire un délai serait **une invention (R4) *et* une violation de R145**. Correctif = **suppression pure** de l'énumération vide, `Depende da zona.` conservée. Témoin : `Z\d \([^)]*\):\s*\.` **4 → 0**, et **0 ailleurs dans le dépôt**.

### 3. Rang 12 — deux grandeurs différentes dans une même réponse
`"Z3: 35 € e 65 €/h de mão de obra."` répondait à « Quanto custa a **deslocação**? » en mélangeant prix de déslocation et taux horaire. Forme transplantée **verbatim** : `"A zona é Z3: 35 € de deslocação, independentes da mão de obra."` — **45 donneurs, 1 seule forme distincte, dont 4 en Z3**. Les 3 fichiers portent déjà `zona Z3` et `Z3 = 35 €` **8 fois chacun**.

### 4. 🔴 RANG 11 LIVRÉ — l'extrapolation depuis CNR est FAUSSE
**Périmètre énoncé** : tout le dépôt hors `_archive*`, hors `_audit/ _backlog/ docs/`, hors les 6 `.md` de doctrine racine, **`blog/*.md` INCLUS** = **2 637 fichiers**. Fenêtre de **60 caractères**.

| Prédicat | CU | ENR | CNR |
|---|---:|---:|---:|
| **`orçamento`↔`gratuit` (60c)** | **110 / 100** | 3 700 / 1 678 | 4 701 / 2 037 |

**Facteur ~40.** Le `context.md` du 25/08 posait « le compteur de CU a la même origine ». **C'est faux.** Le rang 11 de CU **ne vaut pas un GO périmètre** : c'est un lot de 100 fichiers, traitable en run de nuit.

🔴 **Deux familles bloquées par GO sont VIDES dans le HTML servi** :

| Famille | Occurrences | Fichiers | Dans le HTML servi |
|---|---:|---:|---|
| `Você` | 23 | 17 | **0 — 100 % dans des `.md`** |
| corruption `*Parranj*` | 31 | 17 | **0 — 100 % dans des `.md`** |

⚠️ **27 des 103 `.md` ont un jumeau `.html`** ⇒ ce sont des **sources de génération**. Les deux familles sont **latentes, pas closes** : elles reviendront au prochain build. **À router vers l'hygiène de source.**

Autres mesures au même périmètre : `Diagnóstico por telefone em poucos minutos` **5 139 / 1 087** · `Atendimento 24h` **4 200 / 908** · `garantimos atenção` **249 / 190** dont **14 seulement** en forme longue — **le rang 5 sous-comptait d'un facteur 18**.

## ✅ Gate merge — aucun gate actif
Aucune mention d'attente de merge dans le `context.md` lu ce run. Aucun gate réécrit. 0 PR ouverte ; la #277 a été ouverte.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Entre le 06/08 et le 09/08, « Attente GO merge (R7) » a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**. **Ne jamais réécrire un gate de ce type.**

## 🎯 FILE DE TÂCHES LOOP — état au 2026-08-27

| Rang | Cible | Statut |
|---|---|---|
| — | Ordre de merge #268 / #269 | ✅ **CLOS ce run** — #268 fermée sans merge, 0 `***`, 5 `@context` valides |
| — | `contactos.html` énumération amputée · 2 variantes hybrides Z3 | ✅ **traités ce run (#277)** |
| — | Rang 11 — re-mesure `gratuit` élargie | ✅ **livré ce run** — 110 / 100, l'extrapolation CNR est infirmée |
| **1** | 🔴 **7 concelhos sans aucune page indexable** : Alijó · Carrazeda de Ansiães · Freixo de Espada à Cinta · Freixo de Numão · Mouçós · São João da Pesqueira · Tabuaço | 🛑 **ARBITRAGE D'UNE LIGNE** : lequel des deux jumeaux passe en `index` ? Convention observée sur les **172 paires saines** : **le jumeau SANS accent est l'indexable**. **Sept concelhos hors index, c'est du chiffre d'affaires, pas de la conformité.** |
| **2** | 🔴 **186 URLs `noindex` présentes dans les 4 sitemaps** (186/186) | 🛑 **GO PÉRIMÈTRE.** Signal GSC « Submitted URL marked 'noindex' ». Suppression mécanique, zéro invention, mais 186 lignes × 4 fichiers **générés**. ⚠️ **La vraie question est en amont : le générateur produit-il deux fichiers par localité par conception, ou est-ce un artefact ?** |
| **3** | 🟢 **`orçamento`↔`gratuit` — 110 occ. / 100 fichiers** | 🟢 **AUCUN GO — le volume ne le justifie plus.** Correctif prouvé et mergé sur CNR (#327) : `Orçamento gratuito` → `Orçamento por escrito`. **Tâche du prochain run.** ⚠️ Ventiler par famille avant de patcher ; **10 occ. seulement** sont la forme littérale `Orçamento gratuito`. |
| **4** | **`garantimos atenção` — 249 occ. / 190 fichiers** | ⏳ **VENTILER D'ABORD.** Le rang 5 antérieur ne visait que la forme longue (**14 occ. / 9 fic.**) : facteur 18 de sous-comptage. Promesse de garantie non sourcée (R11/R145). **4 occurrences sont en meta description** (surface SERP). |
| **5** | 🛑 **5 fichiers portent DEUX blocs `FAQPage` avec les MÊMES questions** | 🛑 **ARBITRAGE.** Un bloc ancien (555 o) et un récent (766 o) énonçant les 4 engagements de `PRICING.md` verbatim. **Non byte-identiques** → le retrait mécanique ne s'applique pas. Même situation que les deux `FAQPage` de `precos.html` sur ENR. **Question d'une ligne : garder le récent, retirer l'ancien ?** |
| **6** | **`Diagnóstico por telefone em poucos minutos` — 5 139 occ. / 1 087 fichiers** | 🛑 **GO périmètre.** `poucos minutos` est déjà traité comme R145 ailleurs. **Le plus gros gisement de conformité du repo.** |
| **7** | **`Atendimento 24h` — 4 200 occ. / 908 fichiers** | 🛑 **GO périmètre.** ⚠️ **Requalifier d'abord** : R145 **autorise** `24h/7 dias`. Une partie de ce compteur est probablement conforme. |
| **8** | **`canalizador-desentupimento-vimioso.html` — `<header>` jamais fermé** | 🛑 **point de fermeture indéterminé.** Trois invariants convergent et ne suffisent pas. **Un arbitrage d'une ligne suffirait** : « fermer le `<header>` après le `<p class="answer-first">` ». |
| **9** | 🟡 **`Você` (23 occ. / 17 fic.) et `*Parranj*` (31 / 17) — LATENTS EN SOURCE** | 🟡 **REQUALIFIÉS ce run.** **0 occurrence dans le HTML servi** ; 100 % dans des `blog/*.md`, dont **27 ont un jumeau `.html`**. **Ce n'est plus une purge de production mais de l'hygiène de source.** GO plus léger à obtenir : rien n'est servi aujourd'hui. |
| **10** | Requalifier `N% dos/das` **hors `_archive/`** | ⏳ 697 occ / 144 fichiers dont la moitié dans `_archive/`. ✅ `Sem custo extra de fim de semana` : 76 occ, **toutes dans `_archive/`** → **famille close.** |
| 11 | `streetAddress: "Trás-os-Montes, Portugal"` sur `contactos.html` + `canalizador-frioes.html` | ⏳ incohérent R5 — ce n'est pas une adresse |
| 12 | §NAP à `AGENTS.md` + `Sob marcação` à `PRICING.md` | ⏳ **RÉTROGRADÉ** — confort. |

## Tâche suivante recommandée
1. 🟢 **Rang 3 — `orçamento`↔`gratuit`, 110 occ. / 100 fichiers.** **Le GO n'est plus nécessaire : la mesure a divisé le lot par 40.** Correctif déjà mergé sur CNR. **Meilleure tâche sans GO.**
2. 🔴 **Poser le rang 1 à Philippe** — une ligne : « les 7 concelhos hors index, on bascule le jumeau sans accent en `index` ? ». **Impact commercial direct.**
3. **Rang 4 — ventiler `garantimos atenção` par forme** avant tout patch. Une commande Python ; le compteur actuel mélange 249 occurrences de formes différentes.
4. **Rang 5 et rang 8 — deux arbitrages d'une ligne chacun.**
5. **Rang 9 — traiter `Você` / `*Parranj*` comme de l'hygiène de source** : le GO est plus facile à obtenir maintenant qu'on sait que rien n'est servi.

## Apprentissages (self-improving)
- 🔴 **NOUVEAU — une extrapolation inter-repos est une hypothèse, pas un résultat, et elle coûte une commande à tester.** « CU a la même origine que CNR » aurait justifié un **GO périmètre sur un lot imaginaire**. Mesure réelle : **110 contre 4 701, facteur 40**. ➡️ **Ne jamais demander un GO sur un volume extrapolé. Mesurer d'abord.**
- 🔴 **NOUVEAU — le choix d'exclure les `.md` d'un périmètre de production n'est PAS neutre, et il dépend du repo.** Sur CNR et ENR, les `.md` sont de la doctrine qui *cite* les règles (faux positifs systématiques) : les exclure est juste. **Sur CU, `blog/*.md` sont des sources de génération** : les exclure faisait rendre **0** à deux familles qui en comptent 54. ➡️ **Écrire le périmètre ET justifier chaque exclusion, repo par repo.**
- 🔴 **NOUVEAU — « zéro dans le HTML servi » ne veut pas dire « clos ».** 27 des 103 `.md` ont un jumeau `.html` : la violation est **latente dans la source** et reviendra au build. ➡️ **Distinguer explicitement la purge de production de l'hygiène de source — ce sont deux verdicts, pas un.**
- 🔴 **NOUVEAU — un risque signalé trois fois doit être RE-TESTÉ, pas re-signalé.** Le risque #268/#269 s'était éteint tout seul (PR fermée sans merge). Trois runs l'ont reconduit ; une vérification l'a clos. ➡️ **Corollaire du « blocage mécanique » : tout signalement reconduit sans nouveau test est du bruit.**
- 🔴 **NOUVEAU — quand une valeur a été purgée pour une bonne raison, la reconstruire est une double faute.** Le rang 4 se règle par **retrait** précisément parce que R145 interdit de remettre le délai. ➡️ **Le correctif d'une purge ratée est rarement une restauration.**
- 🔴 **NOUVEAU — un donneur unique sur 2 534 fichiers n'est pas un donneur : c'est un orphelin.** **Compter les donneurs est la première chose à faire avant de choisir entre transplanter et retirer.**
- 🔴 **Un blocage « mécanique » n'est pas un arbitrage : il se re-teste à chaque run.** **Toujours écrire, à côté d'un blocage, PAR QUOI il tombe** — un merge, un GO, une mesure.
- 🔴 **« Un contrôle qui rend 0 doit prouver sa source. »** Quand un contrôle rend 0 sur une famille qu'un run antérieur a comptée NON VIDE, **c'est le CONTRÔLE qui est en cause**. ⚠️ Ce run en donne la variante la plus subtile : le contrôle était juste, **c'est le PÉRIMÈTRE qui rendait 0**.
- 🔴 **Duplication ≠ phrase répétée : c'est un SOUS-SEGMENT répété.** Découper en phrases suppose que la répétition respecte la ponctuation ; les préfixes et les parenthèses la brisent.
- 🔴 **Vérifier une hypothèse laissée par le run précédent peut valoir plus que la tâche prévue.**
- 🔴 **La non-byte-identité ferme une méthode, pas le dossier.** **Ne pas confondre « la méthode connue ne s'applique pas » et « il n'y a rien à faire ».**
- 🔴 **Validité JSON ≠ validité schema.org.** `"type"` au lieu de `"@type"` passe `json.loads` et n'émet rien. **Deux contrôles distincts** — les deux passés ce run.
- 🔴 **Certaines chaînes ne survivent pas au canal d'écriture.** `https://schema.org` est muté par les tools runtime **et** par `cat <<EOF`, pas par Python pur (`LECONS.md` L#003). **CONTRÔLER LE BLOB GIT APRÈS COMMIT** — fait ce run sur les 3 fichiers.
- 🔴 **Un prédicat brut peut avoir 60 % de faux positifs.** **La requalification en lecture divise souvent le périmètre par 2 ou plus.**
- 🔴 **`_archive*` n'est pas de la production.** **Exclure `_archive-*` aussi**, pas seulement `_archive/` : ce repo porte `_archive-p1-fix-2026-07-16/`, `_archive-p1-prototype-2026-07-16/`, `_archive-wave2-refonte-2026-07-16/`. Un filtre sur `_archive/` seul les laisse passer.
- 🔴 **Ne retirer un doublon que s'il est byte-identique** (md5 par bloc, méthode EU #314).
- 🔴 **Le contrôle des PR ouvertes se fait AVANT de calculer le périmètre.** ⚠️ **Un titre de PR ne dit pas ce qu'elle couvre** — lire le **diff**.
- 🔴 **Quand un défaut récidive, chercher le GÉNÉRATEUR, pas la page.**
- 🔴 **La signature d'une corruption de batch, c'est le MOT INEXISTANT** — par diff des ensembles de mots.
- 🔴 **Le compteur R12 sur-compte** : R145 **autorise** `24h/7 dias`. (Voir rang 7 : 4 200 occurrences à requalifier avant tout GO.)
- **Ne pas sur-purger.** R4 se viole dans les deux sens.

## Edge cases détectés
- **Ce repo n'a QU'UN remote : `origin`.** (CNR est le seul des 4 à avoir `github` **et** `origin`.)
- ⚠️ **L'ancre du HISTORIQUE diffère d'un repo à l'autre, et ce repo en a CINQ** : `## 🔄 HISTORIQUE P0 (batch 04/07/2026)…` (L206), **`## 🔄 HISTORIQUE` (L236, la bonne)**, `## 🔄 HISTORIQUE — 2026-07-03…` (L1314, L1356), `## 🔄 HISTORIQUE — Run loop 2026-08-12…` (L1519). **Insérer sur une ÉGALITÉ EXACTE de ligne (`assert`), jamais sur un `in` de sous-chaîne.**
- **`gh` et les credentials Git n'existent QUE sur le host macOS.** Reconfirmé ce run : `git push --dry-run` depuis le sandbox → `could not read Username for 'https://github.com'`, et `gh` est absent du `PATH` du sandbox. **Répartition** : lecture / `git fetch` / grep / parsing Python / **écriture de fichiers** → sandbox ; `git` en écriture / `gh` → **host**. Le montage étant partagé, un `git fetch` lancé depuis le sandbox met bien à jour le vrai `.git`.
- **Le `/tmp` du sandbox ≠ le `/tmp` du host.** Worktrees et `--body-file` sous `~/work/Sites/_worktrees/` ou `~/work/Sites/_loop-<date>/`. Le `--body-file` doit vivre **hors du worktree**.
- 🔴 **Un worktree n'est PAS un dépôt git vu depuis le sandbox** : `git show`/`diff`/`log` y rendent des **compteurs à zéro** trompeurs. **Tout témoin se compte en Python sur le CONTENU des fichiers.** ✅ En revanche `git show HEAD:<path>` **dans le worktree depuis le HOST** fonctionne — c'est le canal du contrôle de blob post-commit.
- ⚠️ **Ce repo a ~2 550 pages hors archives.** Un `ls`/`find` non borné fait exploser la sortie. **Borner explicitement ce qu'on imprime.**
- 🔴 **`grep -P` n'existe pas sur macOS** ; **`grep -E` de macOS ne matche pas de façon fiable `ç`/`ã`/`õ`** ; **zsh ne fait pas de word-splitting** ; **`set -e` + glob vide fait avorter le script**. **Pour tout motif accentué : Python.**
- 🔴 **`git commit -m` multiligne est fragile en zsh** → `printf … | git commit -F -`. **ASCII dans les messages de commit, UTF-8 dans les fichiers.** Corps de PR : `--body-file`.
- ⚠️ **Les noms de fichiers accentués passent bien en argument `git add`**, et la boucle `for f in $(…)` est fiable en zsh (c'est justement l'absence de word-splitting qui protège ici).
- **Worktree obligatoire** (R-WT). **Jamais `reset --hard` / `checkout -- .` / `stash` / `clean`** sur le checkout partagé. Vérifié ce run : checkout partagé **non touché**. Aucun `context.md` ne *prescrit* de `reset --hard`.

## Blocages connus
1. 🛑 **RANG 1 — 7 concelhos sans aucune page indexable.** **Tombe par : un arbitrage d'une ligne.** **Impact commercial direct.**
2. 🛑 **RANG 2 — 186 URLs `noindex` dans les 4 sitemaps.** **Tombe par : GO périmètre** — ou, mieux, par la correction du générateur.
3. 🛑 **RANG 5 — deux `FAQPage` par page sur 5 fichiers**, non byte-identiques. **Tombe par : un arbitrage d'une ligne** (garder le récent ?).
4. 🛑 **RANG 6 — `Diagnóstico por telefone em poucos minutos`, 5 139 occ.** **Tombe par : GO périmètre.**
5. 🛑 **RANG 7 — `Atendimento 24h`, 4 200 occ.** ⚠️ **À requalifier avant de demander le GO** : R145 autorise `24h/7 dias`.
6. 🛑 **RANG 8 — `canalizador-desentupimento-vimioso.html`**, point de fermeture du `<header>` indéterminé. **Tombe par : un arbitrage d'une ligne.**
7. ✅ **RÉSOLU — ordre de merge #268 / #269.** #268 fermée sans merge. **Trois signalements pour un risque qui s'était éteint : re-tester, pas re-signaler.**
8. ✅ **RÉSOLU — le stock de PR ouvertes.** 5 → **0**.
9. 🟡 **REQUALIFIÉ — `Você` et `*Parranj*` ne sont PAS servis** (100 % dans des `.md`). **Latents en source**, pas actifs en production. GO plus léger.
10. 🛑 **Batch FAQ (~815 fichiers)** et **batch prix (~73)** de la PR #240 — périmètre parké par Philippe. Rappel d'une ligne, ne pas relancer.
11. 🔴 **La cause racine reste inconnue** pour les 179 paires accentuées, pour les 186 `noindex` en sitemap, et pour les corps de page dupliqués. **Trois défauts issus de la même chaîne de génération.** ➡️ **La question du rang 2 — « le générateur produit-il deux fichiers par localité par conception ? » — est le seul chantier qui change l'ordre de grandeur du backlog.** Même constat, mot pour mot, sur CNR et ENR.
