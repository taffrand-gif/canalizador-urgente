# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-19
- Tâches prévues : `context.md` du 14/08, **n°3** (« ventiler par parsing TOUTES les Questions du `FAQPage` de CU — **CU n'a jamais été ventilé** ») et **n°5** (signature `<td>` contenant `&lt; ` + >40 car, *jamais cherchée ailleurs que sur `calculadora-de-preco.html`*).
- Tâches réellement exécutées : **les deux.**
- Branche (depuis `origin/main`, **en worktree**) : `loop/2026-08-19-cu-ventilation`
- Commits : 2 (1 fichier de production + `SEO_PLAN.md`)
- PR ouverte : **#267** — https://github.com/taffrand-gif/canalizador-urgente/pull/267
- Résultat : ✅ 1 fichier corrigé. **Et 3 gisements jamais inventoriés.**

### Ventilation exhaustive — 2 454 fichiers, 6 960 blocs `ld+json`, **5 JSON invalides**, **1 164 Questions distinctes**

#### 🔴 Trois gisements nouveaux
| Question | Fichiers | Var. | Réponse | Verdict |
|---|---:|---:|---|---|
| **`Tempo de resposta?`** | **331** | 1 | `para emergências, 24h/7d incluindo fins de semana.` | commence par **`para` en minuscule** — le délai a été mangé par une purge. Question de délai → **retrait du couple Q/R** |
| **`Garantia e fatura?`** | **332** | 1 | `Sim, 2 anos garantia e fatura com NIF.` | engagement chiffré — **et contradiction** : `Oferecem garantia?` (47) répond `garantia escrita … conforme orçamento`, **sans durée** |
| **`Fazem orçamento sem compromisso?`** | **38** | 1 | `o orçamento escrito é gratuito` | **`PRICING.md` L51 interdit littéralement « orçamento gratuito »** |

#### Gisements connus — confirmés à l'unité près
| Question | Fichiers | Var. | Détail |
|---|---:|---:|---|
| `Quanto custa uma urgencia de canalizacao?` | 817 | 5 | `por escritoEUR` **698** · `Desde 130 EUR` **62** · double-point **52** · ✅ conforme **4** · `gratuito` **1** |
| `Quanto tempo demoram a chegar?` | 813 | 3 | `conforme zona` **807** · artefact CTA **5** · ✅ conforme **1** |
| `Trabalham 24h/7d?` | 817 | 2 | ✅ conforme (R145 autorise) |
| `Atendem 24h/7d?` | 55 | 4 | 49 ✅ · **6 portent `garantimos atenção após contacto telefónico`** |
| `Quanto custa a deslocação?` | 56 | 16 | 14 cohérentes Z1-Z6 · **2 hybrides** (`Z3: 35 € e 65 €/h de mão de obra`) |
| `O que está incluído no preço?` | 36 | 6 | ✅ 6 variantes = 6 zones, cohérentes |

#### ✅ Question tranchée — `A altitude obriga a medidas especiais?` : 45 fichiers, **45 variantes**
Le `context.md` d'**EU** la laissait ouverte (« soit du contenu légitimement localisé, soit du bruit »). **Réponse : légitimement localisé** — altitude réelle + jours de gel par commune. **Ne pas traiter comme gisement.** Confirmé à l'identique sur EU (40/40).

### Production — `zonas-deslocacao.html`
Signature `<td>` + `&lt; ` + >40 car passée sur les **2 454 fichiers** : **3 hits, tous dans ce seul fichier**, aucun ailleurs. Défaut **identique** à `calculadora-de-preco.html` (PR #261).
- Colonne `Tempo de Chegada` : 3 cellules sur 6 = un paragraphe de CTA écrasé dans une cellule de délai, préfixé d'un `&lt;` orphelin ; 2 vides ; 1 hors-sujet (`Sob marcação`). **Colonne retirée** — aucun délai par zone n'est sourçable dans `PRICING.md`, R145 interdit le délai chiffré. Table : `Zona | Localidades | Deslocação`, **6 × 3**.
- `Orçamento: gratuito` → `por escrito` (`PRICING.md` L51).
- 2 `<li>` retirés : `técnicos com experiência ( para eletricidade` (parenthèse orpheline) et doublon `X: X` portant deux fois `em poucos minutos`.
- **Témoins R8** : `Tempo de Chegada` **1→0** · `poucos minutos` **5→0** · `garantimos atenção` **5→0** · `&lt;` **3→0** · `Sob marcação` **1→0** · `gratuito` **1→0** · `15€`/`65€` **4→4** (contrôle positif). **4/4 blocs JSON-LD valides.**
- Fichier **sans jumelle `public/`** → hors blocage n°5. **Aucune PR ouverte ne le touche** (#264, #243 vérifiées).

⚠️ **`Sob marcação` (Z6) est tombé avec la colonne — 2ᵉ fois.** Toujours **absent de `PRICING.md`**. **Si c'est une vraie règle d'offre, l'ajouter d'abord à `PRICING.md`** — il ne sera pas restauré depuis une page (R4).

## ✅ Gate merge — aucun gate actif
Vérifié ce run sur les 4 `context.md` : **aucune mention d'attente de merge**. Aucun gate réécrit.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Entre le 06/08 et le 09/08, cette mention a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**.

## 🛑 GISEMENTS CHIFFRÉS — DÉCISIONS REQUISES (prédicat = **Question** + variante)

| # | Cible | Fichiers | Traitement |
|---|---|---:|---|
| **(g)** | **Q `Fazem orçamento sem compromisso?` → `gratuito`** | **38** | ✅ **MEILLEUR CANDIDAT POUR UN PREMIER GO** — substitution `gratuito` → `por escrito`. Motif unique, **interdiction verbatim `PRICING.md` L51**, prototype visible dans la PR #267 |
| (a) | `Suplemento 30-50%` → `Acréscimo +50% fora de horas úteis` | **815** | surensemble : referme (c) `por escritoEUR` (698) et (d) `Desde 130 EUR` (62) |
| (b) | Q `Quanto tempo demoram a chegar?` | **813** | retrait du couple Q/R + re-parse du `FAQPage` |
| **(b2)** | **Q `Tempo de resposta?` — NOUVEAU** | **331** | retrait du couple Q/R + re-parse |
| **(f)** | **Q `Garantia e fatura?` — NOUVEAU** | **332** | **arbitrage** : `2 anos` est-il l'offre réelle ? Contradiction avec `Oferecem garantia?` (47) |
| (e) | `mediante confirmação por telefone/7d` (suffixe orphelin) | 15 | retrait du suffixe — **PR #264 ouverte dessus** |

⚠️ Rappel : **exclure explicitement `AGENTS.md`, `SEO_PLAN.md`, `context.md`, `CLAUDE.md`** de tout batch (leçon `fb9dd2415`).

## Tâche suivante recommandée
1. **Si GO (g)** : les 38 fichiers `orçamento escrito é gratuito`. **Le plus petit, le mieux sourcé, le prototype est déjà en revue.**
2. **Sans GO — localiser les 5 blocs `ld+json` JSON-INVALIDES** relevés par le parseur ce run. Il les compte, il ne les a pas encore nommés. Ajouter le nom de fichier + l'erreur au rapport.
3. **Sans GO** — uniformiser les **2 variantes hybrides** de `Quanto custa a deslocação?` (`Z3: 35 € e 65 €/h de mão de obra`) sur le patron majoritaire. 2 fichiers, motif unique.
4. **Sans GO** — les **6 réponses de `Atendem 24h/7d?`** portant l'artefact `garantimos atenção após contacto telefónico`.
5. **Sans GO** — chercher sur CU les défauts trouvés sur EU ce run : statistiques non sourcées (`N% dos/das`, **~60 fichiers sur EU**) et `Sem custo extra de fim de semana` (22 sur EU).
6. **Ajouter `Sob marcação` à `PRICING.md`** si c'est une vraie règle d'offre — sinon il restera perdu.

## Apprentissages (self-improving)
- 🔴 **NOUVEAU — le prédicat d'un gisement, c'est le SUJET de la question, pas son libellé.** `Tempo de resposta?` (331) et `Quanto tempo demoram a chegar?` (813) sont **le même défaut sous deux libellés**. Six runs ont compté le second sans jamais voir le premier. ➡️ **Regrouper les Questions par thème (délai / prix / garantie) AVANT de compter.** Corollaire : la réponse conforme d'une Question sert de **source verbatim** à ses sœurs.
- 🔴 **NOUVEAU — une signature de détection écrite dans un `context.md` doit être passée sur TOUT le repo dès le run suivant.** Celle du 14/08 a trouvé son fichier en **4 secondes de parsing**. Coût nul, une money page corrigée. ➡️ **Toute signature écrite = tâche du run suivant, pas une note.**
- 🔴 **NOUVEAU — deux Questions DIFFÉRENTES d'un même thème peuvent se contredire.** Le contrôle écrit sur EU portait sur les variantes **d'une même** Question. `Garantia e fatura?` (2 ans) vs `Oferecem garantia?` (sans durée) montre qu'il faut **croiser les Questions d'un même thème**.
- 🔴 **NOUVEAU — le prédicat `gratuit` de `PRICING.md` L51-53 n'avait jamais été grepé, sur aucun des 4 repos.** Passé partout ce run : **CU 38 fichiers + 1 page** · **CNR 6** (PR #319) · **ENR 2** (PR #351). ➡️ **`grep -c 'gratuit'` au contrôle d'ouverture des 4 repos.**
- 🔴 **Un artefact de purge peut se loger dans une CELLULE DE TABLEAU.** Ni le grep de motifs connus, ni le parsing du JSON-LD ne le voient. Signature : `<td>` contenant `&lt; ` suivi de plus de 40 caractères. **Confirmée productive ce run.** Même famille que `por escritoEUR` : *une substitution qui ne consomme ni son contexte gauche ni son contexte droit*.
- 🔴 **Vérifier les PR ouvertes AVANT de patcher un fichier.** `gh pr view <n> --json files --jq '.files[].path'` en début de run.
- 🔴 **Un batch partiellement appliqué laisse un gisement PLUS GRAND que celui qu'il corrigeait** (73 → 698, `EUR` non consommé). **Toute substitution doit inclure le contexte droit**, et **recompter les DEUX motifs après exécution**.
- 🔴 **Chercher le SURENSEMBLE avant de demander un GO.** `Suplemento 30-50%` (815) contient `por escritoEUR` (698) et `Desde 130` (62).
- 🔴 **Un échantillonnage à 95 % peut manquer la page qui compte.** Contrôle exhaustif par fichier, jamais statistique.
- 🔴 **Les violations les plus graves sont dans le JSON-LD**, pas dans le corps de page, et aucun compteur de composants ne les voit.
- 🔴 **Ne jamais dériver une cible de batch d'un `grep` ; la dériver du PARSING.**
- 🔴 **Un batch de conformité peut corrompre la RÈGLE qu'il applique** (`fb9dd2415`). Exclure `AGENTS.md`, `SEO_PLAN.md`, `context.md`, `CLAUDE.md`. Avant d'escalader une contradiction de doctrine : `git log -S "<fragment>" -- AGENTS.md`.
- **R145 autorise explicitement `24h/7d` sur ce repo.** Ce qui est banni : les promesses de **délai**. ⚠️ C'est **l'inverse** des sites `*-norte-reparos`. **Ne pas purger « 24h » ici.**
- **Corriger un prix faux par RETRAIT du total, ou par transplant verbatim d'une réponse conforme déjà en production — jamais par recalcul.**
- Ce site utilise « 65 € » (avec espace) et « 65 EUR », pas seulement « 65€ » → adapter les greps R8.

## Edge cases détectés
- **`gh` et les credentials Git n'existent QUE sur le host macOS.** Sandbox = lecture / grep / parsing Python / **écriture de fichiers** (2 454 fichiers parsés en quelques secondes) ; `git` en écriture / `gh` → `mcp__desktop-commander__start_process`. **C'est la répartition la plus efficace.**
- **Le `/tmp` du sandbox ≠ le `/tmp` du host.** Worktrees sous `~/work/Sites/_worktrees/loop-YYYY-MM-DD/` — lisibles depuis le sandbox.
- **Les commandes `git` ne fonctionnent PAS depuis le sandbox dans un worktree** (chemin absolu host dans `.git`). **L'écriture de fichiers, si.**
- 🔴 **`gh pr diff <n>` peut dépasser la limite de sortie de l'outil.** Préférer `gh pr view <n> --json files`.
- 🔴 **zsh ne fait PAS de word-splitting** — `set -- $var` dans une boucle échoue silencieusement.
- 🔴 **`grep -P` n'existe pas sur macOS** — dans une chaîne `&&` il fait échouer silencieusement tout le reste. **Python pour tout motif non trivial.**
- 🔴 **`git commit -m` multiligne avec backticks/parenthèses est fragile en zsh.** `git commit -F -` + heredoc `<<'MSG'`.
- **Worktree obligatoire** (R-WT) : la copie de travail est sale en permanence. **Jamais `git checkout`, `reset --hard`, `stash` ni `clean`.** Vérifié ce run : cette mention est bien une **interdiction**, pas une prescription — rien à corriger.

## Blocages connus
1. 🛑 **Batch (a) `Suplemento 30-50%` — 815 fichiers.** Attente GO.
2. 🛑 **Batch (b) / (b2) — questions de délai, 813 + 331 fichiers.** Attente GO.
3. 🛑 **(f) `Garantia e fatura?` — 332 fichiers.** Arbitrage : `2 anos` est-il l'offre réelle ?
4. ⚠️ **`Sob marcação` (Z6)** absent de `PRICING.md` — perdu deux fois avec une colonne de délai. À rétablir dans `PRICING.md` si c'est une vraie règle.
5. ⚠️ **Doublon `public/` ↔ racine** — arbitrage conjoint avec EU.
6. ⚠️ **5 blocs `ld+json` JSON-invalides** — comptés, pas encore nommés.
