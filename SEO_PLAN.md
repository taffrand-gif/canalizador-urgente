<!-- SOURCE D'ADRESSAGE.
     Le dispatch ne lit QUE le bloc entre les ancres
     CHANTIERS:BEGIN / CHANTIERS:END. Tout le reste de ce fichier
     est de la documentation : lisible, non adressable, sans effet
     sur l'ordonnancement — quels que soient son titre, sa date ou
     sa position.
     N'y écrire aucune trace de run : les traces vont dans
     JOURNAL.md. L'état lu et l'état écrit ne sont jamais le même
     fichier. -->

# 📄 SEO_PLAN.md — Mémoire vivante du projet

> **Fichier de coordination multi-IA / multi-agents / multi-harnais**
> Toute IA travaillant sur ce repo DOIT lire ce fichier avant toute action.
> Toute modification du projet DOIT être consignée ici.

**Propriétaire** : Philippe Braganca (Filipe)
**Site** : https://canalizador-urgente.pt
**Repo** : `taffrand-gif/canalizador-urgente` (working copy locale : `~/work/Sites/canalizador-urgente/`)
**Branche prod** : `main` | **Branche dev/prototype** : `prototype-home` ⚠️ (déjà active)
**NAP** : +351 928 484 451 | Norte Reparos | Trás-os-Montes
**Doctrine site** : **Transparence Radicale** (AGENTS.md §12)
**AGENTS.md** : verrouillé 14/06/2026 + R11 (ZÉRO INVENTION) + R12 (TRANSPARENCE RADICALE)

---

## 🗺️ ROADMAP MONOPOLE — TODO ce repo (CU, urgence) — owner exécution : **Hermes**

<!-- CHANTIERS:BEGIN -->
| ID | Chantier | Prio | Statut | PR | Gate | Prédicat (reproductible) |
|---|---|---|---|---|---|---|
| B2 | Corriger doublon homepage | HAUTE | FAIT | — | — | — |
| X-R12 | « mesma pessoa » / « mesmo técnico » servis en production | HAUTE | A_FAIRE | — | — | `mesma pessoa\|mesmo t[ée]cnico` · **ORDRE IMPOSÉ : prescription → contrôles → rendu → contenu.** (1) `AGENTS.md` **l.115** « Phrase obligatoire » ET **l.155** bloc « Quem somos » — les DEUX, sinon la prescription survit là où un agent lit pour rédiger. (2) contrôles qui verrouillent la violation : `_audit/md-6-10-gate.py:73` la rapporte comme marqueur MANQUANT, `_audit/verify_t_ec555aaf.py:93` `required_literals` min 1 — corriger le contenu d'abord fait échouer deux gates verts. (3) rendu `.hermes-p1-hub-prototype/p1_hub_render_v2.py:110` qui l'émet. (4) **production 4** — `blog/canalizador-24-horas-guia-completo.html` · `blog/canalizador-urgente-guia-completo.html` · `public/.well-known/ai-plugin.json` · `tools/enrich_cu_desentup.py` (faux positif : commentaire de doctrine). **Travail réel : 3 fichiers de contenu + 5 sources.** Les sources sont hors recensement (`_audit/`, `.hermes-…`, `.md` racine) : le total « 4 » les masque. Contrôle positif `mesm` = 530. |
| X-MAIL | Email `privaterelay.appleid.com` publié comme contact | HAUTE | A_FAIRE | — | — | `privaterelay\.appleid\.com` · **production CU 1** — `public/.well-known/ai-plugin.json`. Contrôle positif `appleid` = 1. |
| T1-MONEY | Aligner H1 + sub homepage sur query money 'canalizador urgente' (CPC=14.63 EUR, vol=170, score=2487.10 — DFSEO 16/07) | HAUTE | ⏸ DRAFT | [#335](https://github.com/taffrand-gif/canalizador-urgente/pull/335) | GO Filipe (R7) | `canalizador[\s-]?urgente` (H1 l.252 + sub l.253) ; occurrences homepage 4 → 6 (+50 %) ; témoins R8 cf. JOURNAL.md (zone `t_be736a00`) ; PR #334 CLOSED (1ʳᵉ itération remplacée par #335 sur même branche, refacto push) |
| T2-MONEY-WEAK | Renforcer homepage (WEAK sur 3 impr / 0 clic / pos 14.3 — même query broad money 'canalizador urgente') : +FAQPage JSON-LD 5 questions (close dette SEO_PLAN l.128), +section 'Situações que pedem um canalizador urgente' 385 mots visibles 6 cas typiques equipment réel, +6 liens internes /zonas/ (Bragança/Mirandela/Chaves/Macedo/Vila Real/Lamego — homepage avait 0 lien sortant) ; **+fix R145 'menos de duas horas'** +meta OG/Twitter/keywords +title 112→93 car avec 65 €/h (Doctrine §12.1 transparence HAUT) | HAUTE | ⏸ DRAFT | [#337](https://github.com/taffrand-gif/canalizador-urgente/pull/337) | GO Filipe (R7) | branche `fix/cu-t2-money-weak-canalizador-urgente-t_3a35e691` ; commits `5a7dce57c` (FAQPage+Situações+/zonas/) + `8b96006cb` (R145 fix + OG/Twitter + title — t_3a35e691) + `0be88052b` (docs SEO_PLAN) + **`f31d2c73a`** (JSON-LD schema.org restore — review t_348c33e6 P0 : les 2 blocs homepage avaient `https://***@type` corrompu au lieu de `https://schema.org`, JSON invalide, dette SEO_PLAN l.128 NON fermée ; fix 2/2 blocs parses OK, schema.org×2, `***@type` 2→0) ; homepage 478 lignes / 2340 mots ; FAQPage JSON-LD 0→1 (5 questions, parse OK) + LocalBusiness restauré ; /zonas/ liens 0→6 ; H1+sub INCHANGES (PR #335) ; R145 'X horas' occurrences 1→0 ; Doctrine §12 65€/h×6 Z×21 +50%×3 orçamento×3 NAP×13 Ridgid×2 ROLeak×2 FLIR×1 INTACTS ; OG×9 + Twitter×5 + keywords×1 ajoutés ; **PR #337 OPEN** (4 commits, pushé, attente GO Filipe pour merge — R7 STOP MERGE) |
||| **R145-RESIDU** | Purger traces R145 « atendimento mediante confirmação por chamada » (l.90 résidu vivant) — **300 occ / 131 fichiers** `origin/main@06e77261a` | HAUTE | ⏸ STOP_FORMULATION | — | **GO Filipe R7 (l.90)** | Prédicat `for f in $(git ls-tree -r --name-only origin/main | grep '\.html$'); do git show origin/main:$f 2>/dev/null | grep -qE 'mediate confirmação|mediate confirmacao' && echo "$f"; done | wc -l` = **131 ✅** vérifié `t_edbf1a3e` 2026-09-21 + revérifié **`t_5893aef8` 2026-09-21** ; **Stratification recompte live t_5893aef8** : 11 `blog/*.html` + 32 `concelhos/*.html` + 88 racine `canalizador-*.html` (incl. `top-10-fugas-mais-comuns.html`, `zona-intervencao.html`, `desentupimento-esgoto.html`, `canalizador-urgente-{chaves,braganca}.html`, `canalizador-{sanfins-do-douro,macores,fuga-agua-braganca,esquentador-braganca,autoclismo-braganca,cotas}.html`, +87 `canalizador-desentupimento-*.html`) ; **4 formulations distinctes** : `mediante confirmação por chamada` ×185 (FAQ + CTA pSEO, dominante) ; `mediante confirmação de viagem` ×64 (meta description concelhos, calcul ETA substitué) ; `mediante confirmação por telefone` ×9 (résidu historique FAQ blocs pSEO) ; variantes contextuelles (`em toda a região`, `antes da deslocação`, `após chamada`) ×42 (titres H1/H2 + intro FAQ). **Découpage R15 ≤95 fichiers/commit proposé** : (V0) **46 fichiers** = 11 blog + 32 concelhos + 3 nationales (top-10, zona-intervencao, desentupimento-esgoto) — sous R15, scope le plus visible/stratégique ; (V1) **85 fichiers** = 87 `canalizador-desentupimento-*.html` − 2 déjà en V0 (canalizador-desentupimento-{xinzo-de-limia,…}) ; (V2) **reste** = 8 canalizador-*.html racine hors blog/concelhos/desentupimento (urgente-{chaves,braganca}, sanfins, macores, fuga-agua-braganca, esquentador-braganca, autoclismo-braganca, cotas). **Collision hotspot réévaluée t_5893aef8** : PR #333 `feat/cu-pilote-prix-urgent-t_51a7829f` (OPEN, 4 fichiers modifiés vs main : JOURNAL + SEO_PLAN + `preco-canalizador-urgente-tras-os-montes-2026.html` + `public/.well-known/ai-plugin.json`) — **AUCUNE collision** : la branche ne touche aucun des 131 fichiers R145-RESIDU (vérifié par `git diff origin/main feat/cu-pilote-prix-urgent-t_51a7829f --stat` = 4 fichiers, dont 1 nouveau). Les `mediate confirmação` détectés sur cette branche viennent de `_archive/canalizador-urgente-pre-r12-massif-2026-06-28/blog/*.html` (archives pré-A1, **hors périmètre origin/main**). **PR #337** `fix/cu-t2-money-weak-canalizador-urgente-t_3a35e691` (OPEN) = scope strict homepage, **AUCUNE collision**. **Décision mouvement `t_5893aef8` 2026-09-21** : ⏸ **STOP_FORMULATION** = **NE PAS ouvrir PR draft** tant que la formulation de remplacement n'est pas tranchée par Filipe (SEO_PLAN l.43 « M0 — STOP Filipe — trancher mediante confirmação »). La formulation candidate SEO_PLAN l.37 « disponibilidade 24h/7 dias, confirmada por telefone antes da deslocação » est **UN CANDIDAT parmi d'autres** ; AGENTS.md §12 « gabarit standard » ne la valide pas explicitement. 4 formulations distinctes × contextes (CTA / meta description / FAQ / titre) = **la décision Filipe doit couvrir les 4 patterns**, pas un seul. **R7 STOP MERGE obligatoire** (ligne 90 + AGENTS.md §12 urgence) + gate doc-only (PROTOCOLE R07) ; **AGENTS.md §12 « validation 1 prototype avant batch »** s'applique aussi : pas de V0=46 fichiers en 1 PR avant GO. Reformulations candidates par pattern (à arbitrer) : (a) `por chamada` → « confirmação por chamada antes da deslocação » (drop « mediante ») ; (b) `de viagem` → calcul ETA réel (~XX min, ~YY km) — **demande chiffres OSRM par concelho** (cf. l.50-83 plan P0 prix/zones OSRM) ; (c) `por telefone` (résidu) → suppression simple (déjà purgé en PR #264 2026-08-11, ce résidu = re-génération batch pSEO à investiguer) ; (d) variantes contextuelles → reformulation site-wide « confirmamos a janela de chegada ao telefone antes da deslocação » (cf. pattern déjà présent FAQPage Sernancelhe l.61 « Confirmamos a janela de chegada ao telefone antes da deslocação »). **Pré-requis pour reprise** : GO explicite Filipe sur les 4 reformulations + levée R7. Prochaine itération = ouvrir 1 PR draft V0 strict (46 fichiers, sous R15) après GO. |
<!-- CHANTIERS:END -->

> Roadmap phasée maître : `~/work/Sites/MONOPOLE_SEO_2026Q3.md` §ROADMAP PHASÉE. Site urgence = **phase 1b** (après CNR/ENR validés). ⚠️ **JAMAIS merger main sans STOP validation Filipe** (AGENTS.md urgence).

- [x] **M0** — Purge conformité R11/R12 (marcas/parceiros, programa-fidelidade, case-study, comparacao) — FAIT.
- [ ] **M0 — STOP Filipe** — trancher `mediante confirmação` (CLAUDE.md le liste R145-INTERDIT, encore présent) : purger ou tolérer + MAJ doctrine.
- [ ] **M1 (phase 1b)** — Maillage COMPLET statique : 39 hubs (33 concelhos + 6 distritos) → localités (page **primaire** only) ; remontant breadcrumb localité→hub ; latéral 6-8 sœurs. Signal unique/hub. Localités RÉELLES only. R15 (≤95 fichiers/commit), grep AVANT/APRÈS, 0 lien 404. **GO Filipe avant merge.**
- [x] ✅ **M3** — (schema LocalBusiness/Plumber/areaServed/FAQPage **déjà présents** ✅) — **FERMÉ 2026-08-17** par re-vérif `t_489b9113` : Homepage 3 blocs JSON-LD (`Plumber`+`LocalBusiness`+`ProfessionalService` + `FAQPage`+`areaServed` 10 villes + `geo` Macedo), 33 hubs concelhos + 6 distritos + 4 pages prix datées 2026 (Article+LocalBusiness+Organization) déjà conformes. Reste **dette mineure hors-scope cette tâche** : (a) `streetAddress` "Trás-os-Montes, Portugal" à retirer de `contactos.html` (SAB, incohérent R5 — c'est une **chaîne non-adresse** dans le champ adresse, à remplacer par rien ou retirer la clé) ; (b) idem `canalizador-frioes.html` ; (c) `+351****4451` (4 astérisques = corruption NAP) dans `contactos.html` JSON-LD à remplacer par `+351 928 484 451`. Ne **PAS** ouvrir ici — créer une carte fille ou post-2026-08-17 batch correctif. Détail : master §M3 DESIGN ; cf. ligne CNR 34 même refacto. Leçon #447-bis.
- [ ] **M4** — Combler features (0 actuellement) : `BreadcrumbList` schema + image sitemap (alt géo). Review schema **BLOQUÉ** (0 avis réel → boucle collecte). Détail : master §M4 DESIGN.

---

## 🆕 P0 — Prix/zones OSRM (CU) — dry-run 04/07/2026

> **Mission en cours** (doctrine doc-only, pattern #327) : consigner ici le périmètre P0 avant toute modification code.
> **Source de vérité** : `~/work/Sites/norte-os-marketing/prototypes/zonas-data.json` (914) + `~/Documents/ObsidianVault/NORTE-OS/Methodologie/GRILLE-ZONES-OFFICIELLE-2026-06-24.md` (fallback concelho).
> **Barème** : Z1=15€ · Z2=25€ · Z3=35€ · Z4=45€ · Z5=55€ · Z6=65€ (déplacement) · MO 65€/h canal · majoration +50% MO+dép.
> **R145** : limité au bloc `<div class="zone-info">` ; R145 hors-bloc et `mediante confirmação` = mission séparée (pending Filipe, R7 : urgence = JAMAIS merger main sans STOP validation).
> **Doctrine** : normalisation idempotente depuis source, **jamais inventer une zone pour NO_RESOL**.
> **Artefacts** : `~/work/Sites/_audit/phase0-dryrun/CU_audit.{csv,json}`.

### Counts CU (lecture seule dry-run)

| Couche | Pages | OK | NO-OP | AJUSTER | INCOHERENT | NO_RESOL |
|---|---:|---:|---:|---:|---:|---:|
| `canalizador-*.html` racine (villes + service×localité) | 1828 | 487 | 0 | 1047 | 173 | 121 |

### Villes-sèdes (focus critique — fort trafic / haute valeur)

| Ville | Zone OSRM | Badge actuel | Statut |
|---|---|---|---|
| **Chaves** | Z4 | Z6 / incohérent | ❌ AJUSTER + INCOHERENT |
| **Bragança** | Z2 | Z3 / incohérent | ❌ AJUSTER + INCOHERENT |
| **Vila Real** | Z4 | Z5 / incohérent | ❌ AJUSTER + INCOHERENT |

### Plan d'attaque CU

- [ ] Branche `fix/prix-zones-osrm` (CU) + prototype `canalizador-chaves.html` (racine) → STOP diff Filipe → GO batch R15 (**JAMAIS merger main sans GO Filipe** — AGENTS.md urgence §12)
- [ ] Vague 0 INCOHERENT (173) en premier = badge=1/prix=65€ caractéristique urgence, patch idempotent corrige badge + prix depuis grille
- [ ] Vague 1-N : AJUSTER restant (1047) en vagues ≤95 fichiers/commit
- [ ] Mission M-NO_RESOL séparée (121 localités) — décision Filipe par catégorie

### Liens artefacts

- Audit complet : `~/work/Sites/_audit/phase0-dryrun/CU_audit.{csv,json}`
- NO_RESOL consolidés : `~/work/Sites/_audit/phase0-no-resol/CU.txt` (121 lignes)

---

## 🏆 STRATÉGIE MONOPOLE SERP/GEO → voir `~/work/Sites/MONOPOLE_SEO_2026Q3.md`

> Plan maître cross-sites (établi 30/06/2026). Objectif: occuper **plusieurs surfaces d'un seul résultat** par requête (Local Pack + 2 domaines organic + AI Overview + PAA + image pack + étoiles).
|> Rôle de ce site (urgence plomberie) = **2e slot organique** sur "canalizador <ville>" via intent distinct. Prérequis refonte Transparence Radicale = **quasi ✅ FAIT** au 2026-08-17 (A1 homepage + A2 services × district + A3 570 services + A4 1827 villes + P0 70→65 €/h ×1476 = ~3 900 fichiers doctrine-conformes) ; gisements résiduels revérifiés `origin/main@06e77261a` 2026-09-18 par `t_886e0153` : (a) **stale 🔴 items §ÉTAT lignes 119-127 = ✅ CLOS** par PR #312 (`t_a07cc45d` / `t_318b6f69` 2026-09-01, commit `3d7200ddd`) ; (b) **traces R145 `mediante confirmação` = 🟡 RÉSIDU VIVANT** — recompte live `git ls-tree -r --name-only origin/main -- '*.html' | xargs git show origin/main:{}` = **300 occurrences / 131 fichiers** sur `origin/main`. PR #264 (`849af3c3d` 2026-08-11) avait purgé la formulation « mediante confirmação por telefone » sur les zones/FAQ ; le résidu restant est principalement la formulation réduite **« atendimento mediante confirmação por chamada »** (FAQ + CTA pSEO). **Gating R7 : STOP Filipe obligatoire avant toute PR draft** (site urgence = JAMAIS merger main sans validation). Prédicat reproductible : `for f in $(git ls-tree -r --name-only origin/main | grep '\.html$'); do git show origin/main:$f 2>/dev/null | grep -qE 'mediante confirmação|mediante confirmacao' && echo "$f"; done | wc -l` ≥ 131.
> Priorités globales: **P0** purge/trust + différenciation → **P1** double organic (GBP exclu) → **P2** GEO → **P3** qualité pSEO → **P4** SERP features.
> ⚠️ Risques: doorway/PBN (intent urgence≠installation obligatoire), scaled-content (signal local unique/page). Véracité R11/R12 prime.

---

## 🎯 VISION — Ce qu'on veut devenir

**Objectif business** : être la **référence dépannage plomberie d'urgence** sur Trás-os-Montes via SEO + GEO pur.

**Périmètre site** : URGENCE uniquement (fuga, entupimento, cano rebentado). PAS d'installation (c'est `canalizador-norte-reparos.pt`).

**Promesse homepage** : "Fuga de água? Cano rebentado? 65€/h, deslocação Z1-Z6, orçamento por escrito antes da intervenção. Ligue agora."

**Cible SEO** :
- Top 5 Google sur "canalizador urgente Bragança" / "fuga água urgente"
- Cité par Google AI Overview sur "preço canalizador urgente"
- Appels nuit/WE/feriado captés

**Cible business** : 20-50 appels/mois d'urgence (à fort taux de conversion).

---

## 📊 ÉTAT ACTUEL (au 28/06/2026)

### Forces SEO/GEO (à PROTÉGER)
- ✅ 2016 fichiers HTML = beaucoup de pages longue traîne potentielles
- ✅ Robots.txt : 15+ crawlers IA ouverts (R10)
- ✅ Sitemap.xml présent
- ✅ NAP cohérent : 928 484 451
- ✅ Branche `prototype-home` déjà active
- ✅ Doctrine Transparence Radicale verrouillée par AGENTS.md §12

### ✅ Bloc obsolète — toutes les entrées closes de fait par la refonte A1 Doctrine §12 (NO-OP légitime groupé, revalidation 2026-09-01)

> **Origine du bloc** : audit initial pré-A1 daté du **2026-06-28** (mesures T₀ : `index.html` = 16-39 éléments HTML ; aucun claim chiffré postérieur n'a été re-validé). Clos par **PR #45 squash `133166359` du 29/06/2026** (commit `380c1667c`, refonte A1 Doctrine §12 — homepage from scratch 422 lignes). Revalidé en plusieurs passes : `t_bb4ef8ea` (2026-08-17, JOURNAL.md l.46) + `t_33a93e6c` (2026-08-17, JOURNAL.md l.1382) + `t_4a1bce6d` (2026-08-17, JOURNAL.md l.1398) + `t_916db1b1` (2026-09-01, JOURNAL.md l.1554) + `t_bfbf0caf` (2026-09-01, parent Kanban) + `t_a07cc45d` (2026-09-01, ce patch).
>
> **Recompte live 2026-09-01** sur `origin/main@a6ac26620` :
> - `index.html` = **492 lignes / 235 éléments HTML** (cible historique 194 au 17/08 dépassée, enrichissement continu depuis)
> - Grille prix canonique Doctrine §12.1 : **65 €/h ×5, Zona 1–6 ×6, +50% majoration, "orçamento por escrito antes de qualquer intervenção, sem surpresas" ×3** — INTACT
> - **schema.org Plumber + LocalBusiness + ProfessionalService + FAQPage ×2** INTACT (l.45, l.48)
> - 5 outils réels Doctrine §12.6 INTACTS : Ridgid K9-102 ×2, ROLeak Aqua 3Plus ×2, FLIR E96 ×2 (l.384 FAQ + sections descriptives)
> - **8/8 pages `/zonas/` prioritaires PRÉSENTES** (canalizador-urgente-{braganca,mirandela,vila-real,chaves,miranda-do-douro,mogadouro,vinhais,lamego}.html — PR #46 merge A2 ✅)
> - **NAP inchangé** : `+351 928 484 451` (l.45, l.247, l.257, l.384)
> - **Différenciation d'intention DOCUMENTÉE** SEO_PLAN.md l.85 + l.86 (slot urgence ≠ slot programmé CNR, intent distinct)
> - **B2 doublon homepage** ✅ FAIT (PR #67 squash `4144f002a` MERGED 01/07/2026, tracé SEO_PLAN.md l.32 tableau CHANTIERS:BEGIN)

**Détail par entrée (toutes ✅)** :

- ✅ **L.119 (ex-🔴) Homepage squelettique 16-39 éléments** — clos par PR #45 (29/06/2026). Recompte 2026-09-01 = **235 éléments HTML** sur 492 lignes (`index.html`). Cible 194 du 17/08 dépassée.
- ✅ **L.120 (ex-🔴) Grille de prix 65€/h + Z1-Z6 Doctrine §12.1** — clos par PR #45. Recompte : `65 €/h` ×5, `Zona 1..6` ×6 (zone-cards l.284-289), `+50%` l.292, `orçamento por escrito` ×3 dont l.275.
- ✅ **L.121 (ex-🔴) "fala sempre com a mesma pessoa, não um call center" Doctrine §12.2** — **CADUQUE par override R152** (Annexe A verrouillée 30/06/2026 par Philippe). AGENTS.md l.218-220 : formulation collective prime (« a nossa equipa », « os nossos técnicos », « contacte-nos », « garantimos ») ; « fala sempre com a mesma pessoa » est désormais banni côté HTML/PT visible. Recompte 2026-09-01 : `nossa equipa/contacte-nos/garantimos` ×7, `fala sempre com a mesma pessoa` = 0. Variante PT validée l.306 : « Falamos consigo diretamente, sem intermediários nem call center ». **Pas un oubli de mise en œuvre** : c'est un arbitrage Filipe 29/07/2026 (Annexe A prime sur §12.2).
- ✅ **L.122 (ex-🔴) Équipement réel (Ridgid K9-102, ROLeak, FLIR) Doctrine §12.6** — clos par PR #45. Recompte : Ridgid K9-102 ×2, ROLeak Aqua 3Plus ×2, FLIR E96 ×2 (l.384 FAQ fuite).
- ✅ **L.123 (ex-🔴) FAQ honnête** — clos par PR #45. Recompte : 7 questions FAQ (JSON-LD FAQPage l.48 : custo / 24h / tempo chegada / orçamento / domingo-feriado / tipos / cobertura Bragança-Chaves-Vila Real).
- ✅ **L.124 (ex-🔴) schema.org FAQPage** — clos par PR #45. Recompte : `FAQPage` ×2 (l.48 JSON-LD + meta).
- ✅ **L.125 (ex-🔴) Pages /zonas/ = 0** — clos par PR #46 (A2 ✅). Recompte : 8/8 pages présentes (canalizador-urgente-{braganca,mirandela,vila-real,chaves,miranda-do-douro,mogadouro,vinhais,lamego}.html).
- ✅ **L.126 (ex-🟠) Doublon homepage `./index.html` ET `./public/index.html`** — clos par **PR #67 squash `4144f002a` MERGED 01/07/2026** (synchronisation copie conforme de `index.html`, canonical + sitemap neutralisent la copie). Tracé SEO_PLAN.md l.32 tableau CHANTIERS:BEGIN.
- ✅ **L.127 (ex-🟠) Pas de différenciation d'intention vs CNR** — clos par SEO_PLAN.md l.85 (« 2e slot organique via intent distinct ») + l.86 (« P0 purge/trust + différenciation ») + index.html l.37 (title « 24h/7 »), l.38 (description « urgente »), l.257 (h1 « resposta imediata »), l.48 FAQ « Para trabalhos programados (não urgentes), usamos a página principal canalizador-norte-reparos.pt ». Recompte : intention urgence clairement différenciée de l'intention programmée CNR.

**Doctrine appliquée** : R11 zéro invention ✅ (aucun contenu fabriqué ; décompte lu dans git + filesystem recompte 2026-09-01) ; R12 Doctrine Transparence Radicale ✅ (recompte live confirme intégrité prix/équipement/FAQPage/schema.org/zonas) ; R145 zéro délai chiffré (pas de modification) ; Annexe A formulation collective ✅ (override R152 pivoté 30/06/2026) ; R7 STOP MERGE ✅ (0 merge sans GO Filipe) ; R3 audit lecture-seule ✅ ; R8 témoins git show+grep comptabilisés ; leçon #447 recompte live AVANT toute affirmation chiffrée ✅ ; leçon `kanban-stale-cu-homepage-count-2026-09-01-03` (extension) appliquée ✅ ; leçon #469 anti-doublon ✅ (vérifié : aucune autre carte CEO n'a déjà requalifié ce bloc).

**Référence pattern** : wording aligné sur CNR/SEO_PLAN.md l.388 (« schema LocalBusiness/areaServed/FAQPage déjà présents ✅ »).

**Origine PR/commits référencés** : PR #45 squash `133166359` du 29/06/2026 (commit `380c1667c`, A1 Doctrine §12) ; PR #46 (A2 ✅) ; PR #67 squash `4144f002a` MERGED 01/07/2026 (B2 doublon).

### Doctrine Transparence Radicale (R12) — 10 sections à appliquer
1. Transparence prix (HAUT) : 65€/h canal, Z1=15€ à Z6=65€, +50% nuit/WE/feriado
2. Phrase obligatoire : "orçamento por escrito antes de qualquer intervenção, sem surpresas"
3. Artisan local identifiable : "fala sempre com a mesma pessoa, não um call center"
4. Honnêteté / diagnostic transparent
5. Traçabilité : facture NIF, seguro RC
6. Équipement EXACT : Ridgid K9-102, ROLeak Aqua 3Plus, FLIR, câmara 30m
7. Marques : Grohe, Sanitana (véridiques)
8. FAQ honnête
9. Zones d'intervention
10. CTA téléphone + WhatsApp

### Interdits (RAPPELS)
- ❌ Pas de chantiers inventés (R4 + R11)
- ❌ Pas d'avis/témoignages inventés
- ❌ Pas de délais chiffrés type "resposta em X minutos"
- ❌ Pas d'adresse précise (R5 géo-neutre)
- ❌ Pas de mention "instalação, projeto, remodelação"
- ❌ Pas de `git push --force` (R6)
- ❌ Pas d'auto-merge (R7)

---

## 🗺️ ROADMAP — 3 phases

### 🟥 PHASE A — Refondre ce site selon Doctrine Transparence Radicale (S1-S2) ← **PRIORITÉ 1**
Voir TODO DÉTAILLÉE ci-dessous

### 🟧 PHASE B — Différencier les 4 homepages (S3)
- B1. Homepage distincte de `canalizador-norte-reparos.pt` par l'intention
- B2. Corriger le doublon homepage

### 🟨 PHASE C — Backlinks externes (continu S5+)

---

## 📋 TODO DÉTAILLÉE pour ce repo

### 🟥 A1 — Homepage complète selon Doctrine §12 (S1) ← **CRITIQUE**

**Statut** : ✅ FAIT (Hermes multi-agent, 29/06/2026 — commit 380c1667c, merge 133166359)
**Priorité** : CRITIQUE
**Effort** : ~4h
**Risque** : MOYEN

**Branche** : `prototype-home` ⚠️ JAMAIS merger dans `main` sans STOP validation Philippe (R3 + R7)

**Sections à créer (ordre imposé par AGENTS.md §12)** :
1. H1 unique : "🚨 Canalizador Urgente 24h — Trás-os-Montes"
2. Bloc prix HAUT : 65€/h + grille Z1-Z6 + +50% nuit/WE/feriado
3. "Quem somos" : "Fala sempre com a mesma pessoa, não um call center"
4. Équipement réel : Ridgid K9-102, ROLeak Aqua 3Plus, FLIR
5. Services urgence : Fuga água, entupimento, cano rebentado
6. FAQ honnête : 5-10 questions
7. Zones : Bragança, Mirandela, Vila Real, Chaves
8. Témoignages honnête : "Estamos a recolher as primeiras avaliações"
9. CTA final : Tel +351 928 484 451 + WhatsApp
10. Schema.org FAQPage (JSON-LD)

**Règles** : R3 (STOP), R4 (zéro invention), R5 (géo-neutre), R8 (témoin), R9 (grille), R11 (zéro invention), R12 (Doctrine)

**Témoin R8** :
```bash
wc -l index.html
grep -c "65€" index.html
grep -c "schema.org" index.html
grep -c "fala sempre com a mesma pessoa" index.html
```

### 🟥 A2 — 8 pages /zonas/ prioritaires (S2)
**8 fichiers** : `canalizador-urgente-{braganca,vila-real,mirandela,chaves,miranda-do-douro,mogadouro,vinhais,lamego}.html`
**Effort** : ~8h | **Risque** : BAS

### 🟧 B2 — Corriger doublon homepage (S3)
**Statut** : ✅ FAIT (PR loop/2026-06-29-canalizador-urgente-b2-doublon-homepage, 29/06/2026)
**Problème** : `./index.html` ET `./public/index.html` — doublon avec canonical cassé + R12 violations
**Solution** : `public/index.html` remplacé par copie conforme de `index.html` (A1 Doctrine §12)

---

## 🛡️ RÈGLES DU PROJET

- R1-R9 : voir AGENTS.md
- R10 : robots.txt IA ouvertes (déjà OK)
- R11 : ZÉRO INVENTION (verrouillée 15/06/2026)
- R12 : DOCTRINE TRANSPARENCE RADICALE (verrouillée 15/06/2026)
- Branche dev : `prototype-home` (DÉJÀ active)
- Branche prod : `main` — JAMAIS toucher sans STOP validation
- Doctrine : Transparence Radicale (PAS A+)
- Positionnement : URGENCE uniquement

---

## 🤖 RÈGLES DE COORDINATION MULTI-IA

### Travail en parallèle
1. **Verrouillage logique** : agent ajoute ligne HISTORIQUE avec `⏳ En cours` avant de commencer
2. **HISTORIQUE en premier** : si `⏳ En cours` sur la même tâche → attendre
3. **Pas de concurrence sur le même fichier**
4. **Mise à jour HISTORIQUE** AVANT et APRÈS
5. **Branches séparées** par agent : `agent-claude-A1`, `agent-codex-A1`
6. **Merge vers main** : UNIQUEMENT STOP validation Philippe (R7)
7. ⚠️ **JAMAIS `replace_all=true` sans unicité vérifiée** (incident 28/06/2026)

### Anti-conflits
- Patch homepage : 1 seul agent à la fois
- Patch page /zonas/ : 1 par ville
- Backlink externe : coordination humaine
- Merge : Philippe uniquement
- **Inventer témoignage/chantier : PERSONNE (R11 + R12)**

---

## 📝 NOTES pour les futures IA

### Contexte critique
- **Ce site viole sa propre doctrine** (AGENTS.md §12)
- Priorité #1 = finir ce qui a été commencé
- Branche `prototype-home` = bac à sable

### Pièges à éviter
- ❌ Ne PAS inventer témoignages/chantiers (R11)
- ❌ Ne PAS promettre délais chiffrés
- ❌ Ne PAS mentionner "instalação, remodelação, projeto"
- ❌ Ne PAS merger dans `main` sans STOP
- ❌ Ne PAS utiliser `replace_all=true` sans contexte

---

**Dernière MAJ** : 2026-09-21 00:46 — **PR #337 OPEN (5 commits, pushé)** — T2-MONEY-WEAK `canalizador urgente` homepage reinforcement + **JSON-LD schema.org RESTORE** (review t_348c33e6 P0 fix commit `f31d2c73a` : les 2 blocs homepage avaient `https://***@type` corrompu au lieu de `https://schema.org`, JSON invalide, dette SEO_PLAN l.128 NON fermée + LocalBusiness perdu ; fix 2/2 blocs parses OK `python3 -c "..."` → `OK 2`, occurrences `schema.org` 0→2, `***@type` 2→0). Branche `fix/cu-t2-money-weak-canalizador-urgente-t_3a35e691`, commits : `5a7dce57c` (FAQPage+Situações+/zonas/) + `fb3d2fdc2` (docs SEO_PLAN) + `8b96006cb` (R145 fix + OG/Twitter + title + meta keywords) + `0be88052b` (docs SEO_PLAN v2) + **`f31d2c73a`** (JSON-LD schema.org restore). Suite logique PR #335 CLOSED (T1-MONEY H1+sub) — vague 2 money broad `canalizador urgente` (CPC=14.63 EUR, score=2487.10). R7 STOP MERGE : attente GO Filipe pour merge. Mesure J+7/J+14 via gsc-trajectoire-cron.sh dim 22h (baseline 3 impr / 0 clic / pos 14.3, cible top 10 SERP). **Hotspot pré-existant (hors-scope) signalé** : `public/index.html` l.323-324 dit "Filipe atende" + "é ele quem faz/chega/emite" + "fala comigo" — viole Annexe A pronom collectif. Prédat commit f2000345e8 (PR #152, 30/06/2026, R12 equipa batch). À traiter dans X-R12 vague PME-solo séparée, **PAS** dans scope T2-MONEY-WEAK.

**Prochaine action** : **🚨 URGENCE R12 — fix(r12): 70€/h → 65€/h sur 1504 fichiers** (Doctrine §12 cassée, copier-coller hérité, ~30 min en 6 sub-agents parallèles par lots de ~250 fichiers). Pattern attendu : `70 €/h` / `70€/h` / `70 € / h` / `70€/H` / `70 € / hora` etc. — vérifier aussi `105€/h Domingo` (70×1.5) qui doit devenir `97.50€/h` (65×1.5). Cross-check : eletricista-urgente.pt doit rester à 70€/h, NE PAS toucher ce repo.

