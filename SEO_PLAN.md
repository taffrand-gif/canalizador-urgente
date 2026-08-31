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
| ID | Chantier | Prio | Statut | PR | Gate |
|---|---|---|---|---|---|
| B2 | Corriger doublon homepage | HAUTE | FAIT | — | — |
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
> Rôle de ce site (urgence plomberie) = **2e slot organique** sur "canalizador <ville>" via intent distinct. Prérequis refonte Transparence Radicale = **quasi ✅ FAIT** au 2026-08-17 (A1 homepage + A2 services × district + A3 570 services + A4 1827 villes + P0 70→65 €/h ×1476 = ~3 900 fichiers doctrine-conformes) ; gisements résiduels = traces R145 `mediante confirmação` + stale 🔴 items §ÉTAT lignes 104-108 (audit Kanban `t_bb4ef8ea` 2026-08-17).
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

### Faiblesses SEO/GEO CRITIQUES (PRIORITÉ 1)
- 🔴 Homepage **squelettique** : 16-39 éléments seulement
- 🔴 Manque : grille de prix 65€/h + Z1-Z6 (Doctrine §12.1)
- 🔴 Manque : "fala sempre com a mesma pessoa, não um call center" (Doctrine §12.2)
- 🔴 Manque : section équipement réel (Ridgid K9-102, ROLeak, FLIR)
- 🔴 Manque : FAQ honnête
- 🔴 Manque : schema.org FAQPage
- 🔴 Pages /zonas/ = 0
- 🟠 Doublon homepage : `./index.html` ET `./public/index.html`
- 🟠 Pas de différenciation d'intention vs `canalizador-norte-reparos.pt`

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

**Dernière MAJ** : 2026-09-01 — **rank-push query money 'canalizador urgente' (DFSEO vol=170 CPC=14.63 EUR score=2487.10 — la plus chère du marché portugais) — GAP GSC 28j finie 2026-09-01 (6 impr / 0 clic / pos=22.5)** (Kanban `t_d8c48a6f`). **Approche retenue = renforcement de la page pilier EXISTANTE `blog/canalizador-urgente-guia-completo.html`** (leçon #469 anti-doublon appliquée — page DÉJÀ créée 11/08, title/H1/JSON-LD alignés query exacte 'canalizador urgente', H1 « Canalizador urgente em Trás-os-Montes · Como funciona, quando chamar e quanto custa », JSON-LD BlogPosting+Service+FAQPage+BreadcrumbList+HowTo, prix canonique 65 €/h + Z1-Z6 + +50% + orçamento por escrito ×11, NAP 928 484 451 ×9, FAQ 12 questions = pas de création parasite). **Action = densifier le maillage entrant** vers la page pilier depuis 6 satellites thématiques money (recursos-gratuitos, sinais-alerta-casa-antiga, como-detetar-fuga-agua, top-10-fugas-mais-comuns, top-10-razoes-contratar-canalizador, guia-canalizacao) — 6 cartes « 🚨 Guia Canalizador Urgente » ajoutées dans la section Recursos Uteis (anchor + description identique à celui déjà validé sur homepage + comparacao + calculadora + perguntas-frequentes = cohérence SEO). Total liens entrants guide broad-money sur main : 4 → 10. Bump `dateModified` JSON-LD BlogPosting 2026-08-23 → 2026-09-01 + `lastmod` sitemap-blog.xml URL guide 2026-08-23 → 2026-09-01 (signal freshness). Branche `feat/cu-rankpush-canalizador-urgente-t_d8c48a6f` depuis `origin/main@a6ac26620`, **PR DRAFT #309** ouverte, 1 commit `77b5d4115`, 9 fichiers / +9/-2 (8 satellites + sitemap). Doctrines respectées : R11 zéro invention (aucun exemple chantier/avis/témoignage), R12 (prix canoniques 65 €/h + Z1-Z6 + +50% + orçamento por escrito intacts, NAP 928 préservé), R145 zéro délai chiffré ajouté, Annexe A (zéro « je/eu » ajouté), R6 zéro force-push, R7 zéro merge sans GO Filipe, R3 audit lecture-seule (recompte live avant patch), R8 témoins git diff numstat comptés. **0 hit R12 INTERDIT** côté guide broad-money (resposta prioritária / resposta em X min / mediante confirmação / 24h/7d incluindo / atendimento imediato / disponibilidade imediata = 0 grep post-diff). **0 hit DGEG/TRIESP** côté CU (purge 03/08 préservée). Impact à mesurer J+7 via `gsc-trajectoire-cron.sh` (cron dim 22h) : impressions GSC sur 'canalizador urgente' (baseline 6 → cible >50), position moyenne (22.5 → cible <10), CTR (baseline 0% → cible >2%). **⏳ PR DRAFT #309 — attente GO merge Philippe (R7)**.

**Prochaine action** : PR DRAFT #309 `feat/cu-rankpush-canalizador-urgente-t_d8c48a6f` (9 fichiers, +9/-2, scope strict) en attente GO merge Philippe. Cross-repo référence : leçon #469 anti-doublon (page pilier broad-money DÉJÀ créée antérieurement, on densifie le maillage entrant plutôt que recréer — pattern validé par t_8024328a EU 'eletricista 24 horas').

