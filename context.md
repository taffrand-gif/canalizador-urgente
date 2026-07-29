# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-07-29
- Tâche exécutée : **AUCUNE modification de code.** Audit de conformité complet + escalade de 3 points bloquants.
- Branche créée : `loop/context-2026-07-29-cu` (context.md uniquement, poussée en fast-forward sur `main`)
- PR ouverte : aucune (rien à merger — pas de changement de code)
- Résultat : 🛑 **SITE COMPLET — attente Philippe.** Les 2 seules tâches restantes du SEO_PLAN (A1 refonte homepage, A2 pages /zonas/) sont explicitement STOP-gatées sur un GO de Philippe. Aucune violation non-ambiguë détectée. 3 points à arbitrer ci-dessous.

## Audit de conformité effectué ce run (lecture seule, sur `origin/main`, `_archive/` exclu)
Tous les motifs verrouillés d'AGENTS.md ont été greppés — **0 occurrence sur chacun** :

| Motif | Règle | Occurrences |
|---|---|---|
| `resposta priorit…` | R145 (délai chiffré) | 0 |
| `mediante confirma…` | R145 | 0 |
| `emitimos` | Ruling 2026-07-08 (aucun document émis) | 0 |
| `emissão de certificado` | Ruling 2026-07-08 | 0 |
| `instalações certificadas` | Ruling 2026-07-08 | 0 |
| `trabalho profissional` | Ruling 2026-07-08 | 0 |
| `DGEG` | Ruling 2026-07-08 | 0 |
| `AggregateRating` / `aggregateRating` | R11 / §13 | 0 |
| `+351-` (tiret, NAP non uniforme) | NAP cross-site | 0 |
| `130 EUR` / `Desde 130` | R11 (prix inventé) | 0 |
| `24h/7d` | (rappel : R145 autorise « 24h/7 dias ») | 0 |

➡️ **Le site est propre sur toutes les règles non-ambiguës.** Les correctifs des runs précédents (P0 `d94312630`, B2, A4-BIS) ont tenu.

## 🛑 À ARBITRER PAR PHILIPPE (3 points)

### 1. RÉGRESSION B2 — `public/index.html` et `./index.html` ont re-divergé
`SEO_PLAN.md §B2` est marqué **✅ FAIT** (PR `loop/2026-06-29-canalizador-urgente-b2-doublon-homepage`) avec la solution « `public/index.html` remplacé par copie conforme de `index.html` ». **Ce n'est plus vrai.** Les deux fichiers ont divergé **dans les deux sens** :

| | `./index.html` (racine) | `public/index.html` |
|---|---|---|
| `<title>` | `Canalizador Urgente 24h/7 — … \| Preço conhecido antes` | `Canalizador Urgente — … \| Orçamento escrito antes de intervir` |
| `<h1>` | `Canalizador urgente 24 h/7 dias — resposta imediata em Trás-os-Montes` | `Fuga de água ou cano rebentado? Conhecemos o preço antes de intervir.` |
| `addressLocality` (JSON-LD) | `Trás-os-Montes` | `Macedo de Cavaleiros` |
| `sameAs` (JSON-LD) | 3 entrées | 4 entrées (doublon `canalizador-norte-reparos.pt` avec et sans `/`) |
| Section « Leituras úteis do blog » (maillage interne, 6 liens) | ✅ présente | ❌ absente |

Autrement dit : la **racine** a le maillage blog récent mais le H1 ancien ; `public/` a le H1 conforme §13 (règle d'or « la 1ʳᵉ phrase rassure sur le PRIX ») mais pas le maillage. **Aucun des deux n'est intégralement à jour.**

**Pourquoi le loop n'a pas tranché** : impossible de déterminer de façon fiable lequel des deux est réellement servi en production. `vercel.json` ne déclare **ni `outputDirectory` ni `buildCommand`**, il n'y a **pas de `package.json`** — c'est un déploiement statique zéro-config, et Vercel peut selon les cas servir la racine **ou** auto-détecter `public/` comme répertoire de sortie. `public/` contient **99 fichiers** trackés (pas seulement l'index). Aucun n'est référencé dans `sitemap.xml` (0 occurrence de `public/`).

**Décision demandée** : (a) `public/` est-il déployé ou mort ? (b) Si mort → le supprimer du repo (99 fichiers de contenu dupliqué = risque SEO). (c) Si vivant → quel fichier est la source de vérité, et faut-il fusionner H1-de-`public` + maillage-de-racine ?

### 2. CONTRADICTION INTERNE D'AGENTS.md — « orçamento por escrito »
- **§13 (gabarit, verrouillé 15/06/2026)** donne comme phrase-modèle : *« intervimos com preço claro e **orçamento por escrito** antes de qualquer trabalho »*.
- **Ruling Filipe 2026-07-08 (verrouillé)** liste explicitement **« orçamento por escrito » parmi les formulations INTERDITES** sur toute page.

Les deux homepages utilisent la formule (racine : « Orçamento por escrito antes de intervir » ; `public/` : « orçamento por escrito » + le titre « Orçamento escrito antes de intervir »). Le ruling est **postérieur** au gabarit, donc probablement prioritaire — mais AGENTS.md §12 impose : *« si je ne suis pas certain qu'un élément de positionnement soit conforme, je STOP et demande à Philippe »*. **Le loop a donc STOPPÉ et n'a rien touché.**

**Décision demandée** : le ruling 2026-07-08 abroge-t-il la phrase-modèle §13 ? Si oui, §13 doit être réécrit dans AGENTS.md, et la formule purgée des 4 sites (chantier de masse → GO de périmètre requis).

### 3. « resposta imediata » dans le H1 racine — R145 ?
R145 autorise explicitement « 24h/7 dias » et bannit « resposta prioritária » / « resposta mediante confirmação por telefone ». Le H1 de `./index.html` dit **« resposta imediata »** — même famille sémantique (promesse de délai) mais **pas littéralement dans la liste des bannis**. Ambigu → non touché.

**Décision demandée** : « resposta imediata » tombe-t-il sous R145 ?

## Tâche suivante recommandée
- **Rien d'exécutable en autonomie.** Les 2 tâches SEO_PLAN restantes sont gatées :
  - **A1 — Homepage complète Doctrine §12** : 🛑 STOP attente Philippe (verrouillé depuis le 28/06, ligne 253 du SEO_PLAN).
  - **A2 — 8 pages /zonas/** (`canalizador-urgente-{braganca,vila-real,mirandela,chaves,miranda-do-douro,mogadouro,vinhais,lamego}.html`, ~8h, risque BAS) : 🛑 STOP attente GO explicite.
- Dès qu'un GO arrive sur l'un des 3 points ci-dessus, le point 1 (doublon `public/`) est le plus rentable : c'est un risque de duplicate content sur 99 fichiers, et le fix est mécanique une fois la source de vérité désignée.

## Apprentissages (self-improving)
- **R145 autorise « 24h/7 dias »** — c'est écrit noir sur blanc dans AGENTS.md L125 et L166. Ne PAS purger « 24h » sur les sites urgence par réflexe : ce qui est banni, ce sont les promesses de délai personnalisées (« resposta prioritária », « mediante confirmação por telefone »). ⚠️ C'est **l'inverse** des sites `*-norte-reparos` (installation) où « 24h » est une violation R12 par cannibalisation d'intent. **La même chaîne est violation sur 2 sites et conforme sur les 2 autres.**
- Le grep `24h/7d` (sans espaces) **rate** les variantes réelles du site : `24h/7`, `24 h/7 dias`. Utiliser `24\s*h[/ ]` pour un audit fiable.
- Le ruling « AUCUN DOCUMENT ÉMIS » du 2026-07-08 est la règle la plus récente et la plus large d'AGENTS.md — elle **contredit le gabarit §13** du 15/06. Tout futur run qui rédige de la copy doit être conscient de ce conflit et STOPPER plutôt que choisir.
- Ce repo est un site **statique pur** : pas de `package.json`, pas de build, `vercel.json` en rewrites `/(.*)` → `/$1.html`. Pas de `npx tsc` possible ici (contrairement aux 2 sites `*-norte-reparos`) — la vérification post-patch se fait par grep + inspection HTML.

## Edge cases détectés
- **Worktree obligatoire sur ce repo** : la copie de travail est en permanence sale (`llms.txt` modifié, plus 3+ fichiers HTML untracked à la racine : `desentupir-sanita.html`, `detecao-fuga-agua.html`, `esquentador-avaria.html`) et posée sur la branche `fix/cu-maillage-money`. Ne pas faire `git checkout -b` dedans. Pattern fiable : `git worktree add -q /tmp/cu-ctx -b <branche> origin/main`, travailler là, puis `git worktree remove`.
- Le sandbox `mcp__workspace__bash` **n'a ni `gh` ni credentials Git** → tout git/gh passe par `mcp__desktop-commander__start_process` (host macOS, `gh` authentifié `taffrand-gif`).
- `mcp__workspace__web_fetch` **refuse les URL non présentes dans la conversation** (« URL not in provenance set ») → impossible de vérifier le HTML servi en prod depuis le loop. Pour trancher le point 1, il faut un `curl` host-side via desktop-commander, ou l'API Vercel.
- `_archive/` contient de vieux fichiers avec violations — **NE PAS patcher `_archive/`**, et l'exclure de tous les greps d'audit (`-- ':!_archive'`).
- Ce site utilise « 65 € » (avec espace), pas « 65€/h » → adapter les greps R8.
- `calculadora-de-preco.html` : zones décalées vs AGENTS.md (Z1=20 € dans le calculateur vs 15 € dans AGENTS) — écart possiblement intentionnel (urgence ≠ normal). **NE PAS toucher la logique JS sans GO Philippe.**

## Blocages connus
1. **A1** (refonte homepage Doctrine §12) = 🛑 STOP attente Philippe.
2. **A2** (8 pages /zonas/) = 🛑 STOP attente GO Philippe.
3. **Doublon `public/` ↔ racine** = 🛑 régression B2, source de vérité indéterminable sans info de déploiement (voir §1 ci-dessus).
4. **Contradiction AGENTS.md §13 vs ruling 2026-07-08** sur « orçamento por escrito » (voir §2 ci-dessus).
5. Zones tarif calculateur vs AGENTS.md : ambiguïté → laissé en place.
6. PR #68 (FAQ schema calculadora, run du 30/06) et PR #60 (schema LocalBusiness homepage) — vérifier leur statut de merge.

## Instructions améliorées pour prochain run
1. **Ne pas relancer un audit de conformité complet sur ce site** : il a été fait intégralement le 2026-07-29, 11 motifs verrouillés, 0 occurrence (tableau ci-dessus). Refaire uniquement si du code a été mergé depuis.
2. **Travailler en worktree** (`git worktree add -q /tmp/cu-ctx -b <branche> origin/main`), jamais en `git checkout` dans `~/work/Sites/canalizador-urgente` (copie sale en permanence).
3. **Ne PAS purger « 24h » sur ce site** — R145 l'autorise explicitement. C'est l'inverse des sites installation.
4. Si un GO arrive : traiter le point 1 (doublon `public/`) en premier — meilleur ratio impact/effort.
5. Si aucun GO n'est arrivé : ce site reste **SITE COMPLET — attente Philippe**, ne pas inventer de tâche. Le vide honnête est meilleur que le faux (R11).
6. Pour vérifier ce qui est servi en prod : `curl -sI https://canalizador-urgente.pt/` host-side via desktop-commander (le web_fetch du sandbox est bloqué par la provenance).
