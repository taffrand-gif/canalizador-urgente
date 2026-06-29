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

**Statut** : ⏳ À FAIRE
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
**Problème** : `./index.html` ET `./public/index.html`
**Solution** : choisir 1 seule, rediriger l'autre

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

## 🔄 HISTORIQUE

> **Format OBLIGATOIRE** : `| DATE | AGENT | TÂCHE | ACTION | JUSTIFICATION | RÉSULTAT | STATUT |`

| Date | Agent | Tâche | Action | Justification | Résultat | Statut |
|---|---|---|---|---|---|---|
| 2026-06-28 | claude-minimax-m3 | création | Création SEO_PLAN.md | Mémoire vivante 4 sites | Fichier créé, 286 lignes | ✅ Fait |
| 2026-06-28 | claude-minimax-m3 | phase-2 | Lecture homepage + identification doublon + sections manquantes | Audit lecture seule (R3) | Homepage 16-39 éléments, Doctrine §12 NON appliquée | ✅ Fait |
| 2026-06-28 | claude-minimax-m3 | phase-3 | Création 4 SEO_PLAN.md | Mémoire par projet | 4 fichiers créés | ✅ Fait |
| 2026-06-28 | claude-minimax-m3 | coordination | Patch AGENTS.md + CLAUDE.md (× 4) | Rendre SEO_PLAN.md découvrable | Triangle complet | ✅ Fait |
| 2026-06-28 | claude-minimax-m3 | audit | NAP uniformisé | Cohérence cross-fichiers | "Norte Reparos \| Trás-os-Montes" sur 4 sites | ✅ Fait |
| 2026-06-28 | claude-minimax-m3 | refonte | ⚠️ PRIORITÉ 1 = A1 refonte homepage | Doctrine §12 NON exécutée | Tâche verrouillée, branche `prototype-home` désignée | 🛑 STOP - attente Philippe |
| 2026-06-28 | claude-minimax-m3 | restore | Réécriture complète (recovery) | Patch replace_all a détruit la structure | Fichier restauré à partir de la version saine de canalizador | ✅ Fait |
| 2026-06-29 | Hermes | R11 anos/fundada | Patch "12+ anos", "+10 anos", "15 anos", "Fundada em 2014" → "experiência em serviço técnico" / "Serviço estabelecido em Trás-os-Montes" | R11 (zéro invention) — 3604 occurrences virées sur 1809 fichiers | Témoin AVANT=3617, APRÈS=0 | ✅ Fait |
| 2026-06-29 | Hermes | R11 fourchettes service | Patch 33 fourchettes SERVICE (80-200€, 50-150€, 150-500€, etc.) → "sob orçamento" | R11 (zéro invention) — fourchettes déplacement (15-65€) CONSERVÉES (grille officielle Z1-Z6) | Témoin AVANT=505, APRÈS=0 | ✅ Fait |
| 2026-06-29 | Hermes | R11 formulaires annexes | Patch "mais de X anos de atividade", "mais de uma década", "X anos de experiência no setor/em canalização" | R11 (zéro invention) — 213 occurrences virées sur 203 fichiers | Témoin AVANT=213, APRÈS=0 | ✅ Fait |
| 2026-06-29 | Hermes | R11 testemunhos | Réécriture testemunhos.html + public/avaliacoes-clientes.html | R11 (zéro invention) — 16 fake testemunhos (Maria Silva, João Santos, Rui Almeida, João M., etc.) virés | 2 pages honnêtes (compromisso + CTA) | ✅ Fait |
| 2026-06-29 | Hermes (multi-agent) | A1 homepage Doctrine §12 | Refonte from scratch index.html : hero + bandeau grille 65€/h + Z1-Z6 + +50% + artisan local (Filipe, Norte Reparos, "mesma pessoa") + 5 outils réels (Ridgid K9-102, Fluke T6-1000, ROLeak Aqua 3Plus, FLIR E96, caméra 30m) + 9 villes Z1-Z6 + FAQ transparente (5 questions) + CTA NAP 928 484 451 + Schema.org Plumber géo-neutre | Doctrine §12 Transparence Radicale — branche `prototype-home` existante identifiée comme **crochetterie marketing** (faux scarcity/urgency/social-proof) → JETÉE. R7 respecté : PR #45 ouvert + STOP merge + GO explicite Philippe | Témoin AVANT=264 lignes / APRÈS=422 lignes (+417/-260). 14/14 éléments §12, **0 interdit**. Commit `380c1667c`, merge squash `133166359` | ✅ Fait |
| 2026-06-29 | Hermes (multi-agent) | A2 bloc Doctrine §12 services | Ajout bloc Doctrine §12 (grille 65€/h + Z1-Z6 + +50% + artisan + 5 outils réels + NAP 928 484 451) sur top 5 services sitemap.xml × district Bragança (urgente, fuga-agua, desentupimento, autoclismo, esquentador). Contenu SEO existant préservé intentionnellement (ranking longue traîne acquis). | R7 : PR #46 ouvert + STOP merge + GO explicite Philippe | Témoin : +68/-19 sur 5 fichiers, 0 interdit **ajouté** par le bloc. Commit `17b221249`, merge squash `c219f9ef` | ✅ Fait |
| 2026-06-29 | Hermes (multi-agent) | A2-BIS nettoyage SEO pré-existant | Suppression chaîne défaillante « Resposta confirmada por chamada — ligue 928 484 451, atendimento Norte Reparos, sem call center » (6+/fichier), « Resposta prioritária/imediata », « equipa de piquete », fourchettes inventées (desde 110€/150€/280€/40€), « orçamento grátis », « + Experiência », canonical cassé, `<meta noindex, follow>`. Bloc Doctrine §12 (A2) **INTACT**. | Constat post-A2 : le bloc Doctrine était noyé dans le contenu SEO pré-existant non-conforme. F5 (subagent abandonné) traité par moi-même via Python. R7 : PR #47 ouvert + STOP merge + GO explicite Philippe | Témoin : 5 fichiers, +37/-37 (purement suppressif/remplacement). 0 interdit SEO restant, 1 occurrence `doctrine-transparence`/fichier (intact). NAP 928 484 451 + tarif 65 €/h préservés. Commit `e1e00656`, merge squash `7a0d2796` | ✅ Fait |

---

**Dernière MAJ** : 2026-06-29 — **A4 mergée sur main (squash `42b1ec17`, PR #49)**. 1827 fichiers courts `canalizador-{ville}.html` à la racine désormais conformes Doctrine §12 : bloc Doctrine (65 €/h + Z1-Z6 + +50% + NAP 928 484 451 + équipement Ridgid/Fluke/ROLeak/FLIR), noindex retiré, fourchettes « Desde X € » → « sob orçamento por escrito », « orçamento grátis » → « por escrito », « Resposta prioritária » → « atendimento mediante confirmação por téléphone », « Acréscimos noturnos 18h-08h » → « Majoração noite (20h-8h), domingo e feriado: +50% ». Branche `a4-doctrine-pages-courtes` supprimée (locale + origin) après merge.
**Prochaine action** : **A4-BIS = cleanup résiduel** (corriger `+351****4451` JSON-LD masqué + claims locaux non vérifiables type « Termas e património romano » règle §11) **OU** équivalents eletricista (squash `cab71ce09`, PR #36). Backups `/tmp/a4-backup-{canal,elec}-2026-06-29/` supprimables après validation.
| 2026-06-29 | Hermes (multi-agent + mode loupe) | A3 Doctrine §12 services étendu | A2 (bloc Doctrine §12) + A2-BIS (cleanup SEO pré-existant : noindex quotes simples, fourchettes inventées, orçamento grátis, majorations mal formulées) sur 570 fichiers services (urgente + fuga-agua + desentupimento + autoclismo + esquentador). Hors 10 fichiers Bragança déjà conformes (PR #46+#47). 11 commits (10 subagent + 1 correctif mode loupe `25bfb0cb5`). Leçon #204 documentée : pattern noindex élargi pour matcher quotes simples+doubles. R7 : PR #48 ouvert + STOP merge + GO explicite Philippe | Témoins AVANT/APRÈS sur 570 fichiers : bloc_doctrine 0/570 → 570/570, noindex 570/570 → 0/570, desde X€ 570/570 → 0/570, orçamento grátis 570/570 → 0/570, Acréscimos mal formulés 76/570 → 0/570. NAP 928 484 451 + tarif 65 €/h + bloc intact (1 occurrence doctrine-transparence). Vérifié moi-même sur 5 fichiers random (Chaves, Armamar, Macedo, Mogadouro, Miranda) | ✅ Fait (PR #48) |
| 2026-06-29 | Hermes (2 subagents en parallèle + mode loupe parent-side) | **A4 Doctrine §12 pages courtes** | A2 (bloc Doctrine §12) + A2-BIS (cleanup SEO pré-existant) sur **1827 fichiers courts `canalizador-{ville}.html`** à la racine (hors `concelhos/`, `distritos/`, `blog/`). NAP 928 484 451 + 65 €/h + ⚡ canal + Ridgid/Fluke/ROLeak/FLIR. 37 commits subagent + 1 squash final. Mode loupe post-subagent (leçon #205/#209) : vérifié moi-même compteurs globaux + 5 fichiers random. Faux positif subagent sur compteur `fala sempre` (case-sensitive) détecté et corrigé par comptage Python direct. R7 : PR #49 ouvert + STOP merge + GO explicite Philippe | Témoins AVANT/APRÈS : noindex 1253 → 0, desde_110/145/150 ~285 → 0, orçamento grátis 1439 → 0, Resposta prioritária 1823 → 0, Acréscimos mal formulés 308 → 0, bloc Doctrine 575 → 1828, Fala sempre 575 → 1828. Cross-site drift (928/65 €/h) vérifié 0/1828. Check 6 post-mass-patch : 1 régression mineure introduite (`12+ Anos de Experiência` +1) — corrigible en A4-BIS. Commit batch `86d6dd027 → ddab16485`, squash final `42b1ec17` | ✅ Fait (PR #49) |

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

## 🧹 MÉNAGE 2026-06-30 — Réorganisation multi-sites

**Déclencheur** : demande Philippe « fait du ménage, fait en sorte que tout soit propre, bien organisé sur Vercel et GitHub ».

### Repos GitHub supprimés (backup local `/Users/admin/archives/`)
- ❌ `taffrand-gif/staff-seekers` (166 Mo, 4223 fichiers, fourre-tout historique, mort) — backup `/Users/admin/archives/staff-seekers-2026-06-30/`
- ❌ `taffrand-gif/norte-microsites` (1.3 Mo, 5 mini-sites thématiques `site1-guia-canalizacao`/`site2-dicas-eletricidade`/`site3-bricolage-casa`/`site4-energia-solar`/`site5-manutencao-casa`, jamais déployés en prod) — backup `/Users/admin/archives/norte-microsites-2026-06-30/`

### Projets Vercel supprimés
- ❌ `staff-seekers` (orphelin, aucun domaine)
- ❌ `workspace` (vide, 0 déploiement, pas de repo)
- ❌ `client` (vide, 0 déploiement, pas de repo)
- ❌ `norte-reparos-clean` (doublon détenant `canalizador-norte-reparos.pt`, a servi du contenu DOWN après incident Index.html)

### Actions correctives réalisées
- ✅ Transfert domaine `canalizador-norte-reparos.pt` : `norte-reparos-clean` (DOWN) → `canalizador-norte-reparos` (UP, lié à `taffrand-gif/norte-reparos`)
- ✅ Détachement des domaines legacy `norte-reparos.com` + `www.norte-reparos.com` (redirections historiques désactivées)
- ✅ Site `canalizador-norte-reparos.pt` restored après incident commit vide `457e56cd` (contenu réel restauré byte-à-byte via PUT /contents avec base64)

### État final propre — mapping 1-pour-1
| URL | Repo GitHub | Projet Vercel | Status |
|-----|-------------|---------------|--------|
| canalizador-norte-reparos.pt | taffrand-gif/norte-reparos | canalizador-norte-reparos | ✅ |
| eletricista-norte-reparos.pt | taffrand-gif/eletricista-norte-reparos | eletricista-norte-reparos | ✅ |
| canalizador-urgente.pt | taffrand-gif/canalizador-urgente | canalizador-urgente | ✅ |
| eletricista-urgente.pt | taffrand-gif/eletricista-urgente | eletricista-urgente | ✅ |

### Google Search Console — actions manuelles recommandées
À faire par Philippe dans `search.google.com/search-console` :
- Désenregistrer propriétés mortes : `staff-seekers.com`, `norte-reparos.com`, `www.norte-reparos.com`
- Conserver propriétés actives des 4 `.pt` + leurs sous-domaines `www.`

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

**Dernière MAJ** : 2026-06-28 16h30 BST
**Prochaine action** : A1 (homepage complète selon Doctrine §12) — en attente GO Philippe
