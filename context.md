# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-21
- Tâche prévue : **tâche n°1 du `context.md` du 20/08** — passer les signatures de corruption de `LECONS.md` sur tout le repo.
- Tâche réellement exécutée : **la tâche prévue**, et elle a livré **la cause racine** d'un défaut classé « 5ᵉ récidive ».
- **PR ouverte : #270** — https://github.com/taffrand-gif/canalizador-urgente/pull/270 — branche `loop/2026-08-21-cu-signatures-lecons` — 7 commits, 6 fichiers.

### Le sweep croisé que `LECONS.md` demandait depuis le 04/08 n'avait jamais été fait
`LECONS.md` porte, depuis le 04/08, un point explicite : *« **TODO post-merge** : grep croisé des 4 sites pour les 11 chaînes signature sur TOUS les fichiers. Si positif : ouvrir un ticket par site. »*
**Toutes les signatures visées étaient encore en production 17 jours plus tard.**

| Signature | CNR | ENR | CU | EU |
|---|---:|---:|---:|---:|
| NAP parasite `tel:+351****` | 5 / 4f | 18 / 5f | **11 / 4f** | 3 / 2f |
| JSON-LD `https://***` | – | 3 / 1f | 5 / 1f | 1 / 1f |
| pt-br `Você` (corpus INTERDIT) | 40 / 35f | 103 / 96f | 19 / 14f | 22 / 16f |
| 6 chaînes françaises interdites | 2 | 6 | 3 | – |

### 🔴 Cause racine : le NAP parasite est écrit en dur dans un GÉNÉRATEUR
`LECONS.md` traitait le parasite comme un **résidu** à nettoyer page par page (« mission séparée `fix/nap-concelhos-deparasite` »). C'en n'était pas un.
**`tools/enrich_cu_desentup.py` L42 : `TELEFONE_E164 = "+351****4451"`.** Chaque page produite par ce script recevait un `href="tel:"` **mort**. C'est pourquoi le défaut revenait après chaque nettoyage (leçon #423 : « 5ᵉ récidive »). **Le générateur est corrigé — premier commit de la PR.** (Symétrique sur EU : `scripts/p1/gen_p1_hub_concelho.py` L15.)

⚠️ **`AGENTS.md` de CU ne porte pas de §NAP.** La règle #142 « toujours repartir d'`AGENTS.md` §NAP » y est donc **inapplicable**. Valeur `+351928484451` reprise de `SEO_PLAN.md` L495 et **corroborée sur disque** par le texte affiché `928 484 451` et le `wa.me/351928484451` de la même ligne (triple concordance, R4). **À ajouter à `AGENTS.md`.**

### 🔴 Second défaut : `##style##` — la feuille de style de `contactos.html` n'était jamais ouverte
Trouvé par le contrôle d'équilibre des balises (recommandation n°2 du `context.md` d'EU).
`contactos.html` L2 portait le marqueur de gabarit `##style##` **à la place de `<style>`** : la feuille de style n'était jamais ouverte, **tout le CSS était servi comme texte visible en haut de la page Contactos**, et le `</style>` de L36 fermait un bloc inexistant. Marqueur résiduel `##endstyle##` (L35) également retiré. Même marqueur sur `calculadora-de-preco.html`.
**Témoin : `<style>`/`</style>` 1/2 → 2/2.**

- **Témoins R8** : `+351****` (hors docs/`_audit`) **5 occ / 4 f → 0** · `##style##`+`##endstyle##` **3 occ / 2 f → 0**.
- Aucun fichier pris par une PR ouverte (contrôle sur les 104 fichiers des PR ouvertes avant patch).

## ✅ Gate merge — aucun gate actif
Vérifié ce run : **aucune mention d'attente de merge** dans les 4 `context.md`. Aucun gate réécrit.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Une PR en attente ne gèle pas le repo — la #269 est ouverte depuis le 20/08 et n'a pas empêché la #270. Entre le 06/08 et le 09/08, la mention « Attente GO merge (R7) » a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**. **Ne jamais réécrire un gate de ce type.**

## 🎯 FILE DE TÂCHES LOOP — état au 2026-08-21

| Rang | Cible | Statut |
|---|---|---|
| — | générateur NAP · 4 pages `tel:` · `##style##` ×2 | ✅ **traités ce run (#270)** |
| **1** | **Les autres signatures de `LECONS.md` jamais grepées** | ⏳ **PROCHAINE TÂCHE, sans GO.** Le sweep de ce run a couvert 10 motifs et livré une cause racine ; `LECONS.md` (904 lignes) en contient d'autres. **Meilleur rapport effort/résultat confirmé 2 runs de suite.** |
| **2** | **3 chaînes françaises du corpus INTERDIT** (`satisfait ou refait`, `parle uniquement`, `Marque grande`) | ⏳ interdites **verbatim** par `LECONS.md`. 3 occurrences, aucun GO. |
| **3** | **Corruption `repar`→`arranj` — 33 occurrences / 19 fichiers sur CU** | ⏳ **GO périmètre.** Voir §Blocages n°1. **Aucun `href` touché sur CU** : le défaut y est purement textuel. |
| **4** | **`Você` — 19 occurrences / 14 fichiers** | 🛑 corpus INTERDIT, GO requis (184 sur les 4 repos) |
| **5** | Les **2 variantes hybrides** de `Quanto custa a deslocação?` (`Z3: 35 € e 65 €/h`) | ⏳ 2 fichiers, motif unique, sans GO |
| **6** | Les **6 réponses de `Atendem 24h/7d?`** portant `garantimos atenção após contacto telefónico` | ⏳ sans GO |
| **7** | Chercher sur CU les défauts trouvés sur EU : statistiques non sourcées (`N% dos/das`) et `Sem custo extra de fim de semana` | ⏳ sans GO |
| 8 | Ajouter un **§NAP à `AGENTS.md`** et `Sob marcação` à `PRICING.md` | ⏳ sinon la règle #142 reste inapplicable ici |

## Tâche suivante recommandée
1. **Rang 1 — continuer le sweep `LECONS.md`.** Deux runs de suite, c'est ce qui a produit le plus par unité d'effort : le 20/08 une money page, ce soir une cause racine.
2. **Rang 2 — les 3 chaînes françaises** : sourcé verbatim, aucun GO.
3. **Rang 8 — le §NAP dans `AGENTS.md`** : une ligne, et elle rend une règle existante applicable.
4. **Si GO (g)** : les 38 fichiers `orçamento escrito é gratuito` (prototype en revue, PR #267).
5. **Rangs 5 à 7** — tous sans GO.

## Apprentissages (self-improving)
- 🔴 **NOUVEAU — un « TODO post-merge » écrit dans `LECONS.md` n'est exécuté par personne.** Celui-ci datait du 04/08 ; **toutes** les signatures qu'il visait étaient encore en production. ➡️ **Le passage des signatures de `LECONS.md` doit être une étape FIXE du loop, pas une recommandation.** C'est un grep, il coûte quelques secondes, et il a livré cette nuit la cause racine d'un défaut classé « 5ᵉ récidive ».
- 🔴 **NOUVEAU — quand un défaut RÉCIDIVE, la page n'est pas le bon niveau de correction : chercher le GÉNÉRATEUR.** Le NAP parasite avait été nettoyé au moins 5 fois page par page. Il était écrit en dur dans deux scripts Python. ➡️ **Avant de nettoyer une occurrence en série, grepper le motif dans `tools/`, `scripts/` et toute la chaîne de build.**
- 🔴 **NOUVEAU — un marqueur de gabarit non substitué ne ressemble pas à une violation et n'apparaît dans aucun compteur.** `##style##` passe tous les audits de conformité, tous les linters JSON-LD, tous les greps de doctrine — et casse le rendu d'une money page. ➡️ **Contrôle à ajouter en fin de run** : `grep -rIoE '##[a-zA-Z_]{3,}##'`, et plus généralement les délimiteurs non résolus (`{{…}}`, `%%…%%`, `__…__`, `${…}` dans du HTML statique).
- 🔴 **NOUVEAU — une PR qui répare un fichier ne répare pas sa famille.** La #312 (EU) a corrigé 2 pages `fuga-corrente` ; **6 sœurs portaient le même défaut, dont celle qu'elle avait touchée**. ➡️ **Après tout correctif sur une page générée, repasser le contrôle sur l'ensemble du motif de nom** et le consigner comme témoin.
- 🔴 **NOUVEAU — la signature d'une corruption de batch, c'est le MOT INEXISTANT.** `grep -rIoE '[[:alpha:]]*<lemme>[[:alpha:]]*' | sort | uniq -c` sort les formes légitimes puis, juste en dessous, les non-mots. Une commande, 523 corruptions révélées sur 4 repos.
- 🔴 **NOUVEAU — quand `AGENTS.md` ne porte pas la valeur canonique, une règle qui l'invoque est inapplicable.** Le constater et **corriger `AGENTS.md`**, plutôt que recopier depuis un HTML (ce qu'interdit #142).
- 🔴 **Vérifier les PR ouvertes AVANT de patcher** : `gh pr view <n> --json files --jq '.files[].path'`. 3ᵉ run consécutif où ce contrôle évite un conflit.
- 🔴 **Un batch de conformité peut corrompre la RÈGLE qu'il applique** (`fb9dd2415`). Tout batch doit exclure `AGENTS.md`, `SEO_PLAN.md`, `context.md`, `CLAUDE.md`, `LECONS.md`. Avant d'escalader une contradiction : `git log -S "<fragment>" -- AGENTS.md`.
- 🔴 **Le compteur R12 sur-compte** : R145 **autorise** `24h/7 dias`. Requalifier avant de patcher.
- **Ne pas sur-purger.** R4 se viole dans les deux sens.

## Edge cases détectés
- **`gh` et les credentials Git n'existent QUE sur le host macOS.** Sandbox : `git fetch` OK, **`git push` impossible**. **Répartition** : lecture / grep / parsing Python / **écriture de fichiers** → sandbox ; `git` en écriture / `gh` → `mcp__desktop-commander__start_process`.
- **Le `/tmp` du sandbox ≠ le `/tmp` du host.** Worktrees sous `~/work/Sites/_worktrees/loop-YYYY-MM-DD/`.
- 🔴 **`grep -P` n'existe pas sur macOS** ; **zsh ne fait pas de word-splitting**. Pour tout motif non trivial : **Python**.
- 🔴 **`git commit -m` multiligne est fragile en zsh** → `git commit -F -`. Corps de PR : `--body-file`.
- 🔴 **Le filtre sandbox qui mute `https://schema.org` est COSMÉTIQUE à l'affichage** (leçon EU) mais **`https://***` sur disque est un vrai défaut** : distinguer les deux en relisant les octets, pas la sortie du terminal.
- **Worktree obligatoire** (R-WT). **Jamais `reset --hard` / `checkout -- .` / `stash` / `clean`** sur le checkout partagé.

## Blocages connus
1. 🛑 **GO périmètre — corruption `repar`→`arranj` sans limite de mot** : **523 occurrences / 258 fichiers** sur les 4 repos (CU 33/19). Formes : `parranjar` 221 (`preparar`), `arranjacao` 113 (`reparacao`), `parranjo` 96 (`preparação`), `parranjada/o/os/as` 41, `parranjou` 14. La partie « liens » est livrée sur CNR (#323) et ENR (#363) ; **CU n'a aucun `href` touché**. Le blocage porte sur `Parranjo`→`Preparação` : restauration *probable* (contextes sans ambiguïté) mais **pas prouvable par un fichier sur disque** → hors R4 sans arbitrage. **Un GO d'une ligne débloque les 523.**
2. 🛑 **`Você` — 184 occurrences / 161 fichiers sur les 4 repos** (CU 19/14). Corpus INTERDIT `LECONS.md`. GO requis.
3. 🛑 **Batch (a) `Suplemento 30-50%` — 815 fichiers.** Attente GO.
4. 🛑 **Batch (b) / (b2) — questions de délai, 813 + 331 fichiers.** Attente GO.
5. ⚠️ **`https://***` résiduel : 5 occurrences dans `blog/canalizador-urgente-guia-completo.html`** — c'est le fichier de la **PR #269, toujours ouverte**. ⚠️ **La PR #268 réécrit la même ligne et y CONSERVE le `***`** : si elle merge en premier, elle republie la corruption. **Résolution par `git merge`, jamais rebase (R6)** : garder le contenu de #268 sur la ligne 26 et y restaurer `"https://schema.org","`.
6. ⚠️ **`contactos.html` + `canalizador-frioes.html`** : `streetAddress: "Trás-os-Montes, Portugal"` — incohérent R5 (ce n'est pas une adresse).
7. ⚠️ **La cause racine du batch `repar`→`arranj` n'est pas identifiée.** **Retrouver le script pour s'assurer qu'il n'est pas rejoué.**
