# MISSION HERMES P0.5B — CORRECTIF SCRIPT + VAGUES v2 — 2026-07-02 (soir)

> Suite audit Claude/CEO 02/07 soir : **9/10** (baseline 6,5 ; corrigé — les 5 SKILL
> sont bien installés dans `~/.hermes/skills/`, l'audit avait cherché au mauvais endroit). Étalonnage KO1 FERMÉ
> (ton script 57/70/15/29 = 171 = baseline 174 − 3 prototypes, per-repo exact — bravo).
> **GO D5 = CONDITIONNEL** : Filipe a dit GO 02/07 soir, MAIS les vagues sont
> dimensionnées sur des chiffres faux. Ordre strict S0→S4 ci-dessous. Zéro vague avant S2 validé.

## Constat audit (re-mesure avec TON script, 4 repos)

| Métrique | Ton script | Baseline CEO | Verdict |
|---|---:|---:|---|
| KO1 badge ≠ zonas-data.json | 171 (57/70/15/29) | 174 | ✅ fermé (−3 prototypes) |
| KO2bis badge ≠ JSON-LD | **11** | **842** (211/218/211/202) | ❌ écart structurel |
| KO3 prix body ≠ grille | **594** | non compté baseline | ⚠️ ABSENT du plan vagues |
| KO4 délais -urgente | 64 (32 CU + 32 EU) | — | sous-compté |
| NO_RESOL | **7 745 / 13 112 (59%)** | — | angle mort total |

**Cause racine KO2bis** : `audit_page()` fait `return` dès `expected_zone is None`
→ une page NO_RESOL saute TOUS les checks, y compris KO2bis (cohérence interne
badge vs JSON-LD — n'a besoin d'AUCUNE résolution zonas-data) et KO4 (délais —
pareil). 59% du parc jamais audité.

## S0 — Script v2 (`tools/p0.5-self-audit/self-audit-zones.py`)

1. **Déplacer KO2bis et KO4 AVANT le early-return NO_RESOL.** Ces 2 checks ne
   dépendent pas de `expected_zone`. Une page NO_RESOL doit quand même être
   auditée badge-vs-JSON-LD et délais.
2. **Étendre `SERVICE_PREFIXES`** : `preco-canalizador-urgente-`,
   `preco-eletricista-urgente-`, `iluminacao-exterior-` (+ tout préfixe découvert
   au triage S1). Strip aussi le suffixe `-2026` des pages M3.
3. **`SLUG_ALIASES`** (D6) : résoudre chaque slug typo contre zonas-data.json —
   `alfndega*`, `seix0`, `macedo-cavaleiros` (sans "de"). Appliquer UNIQUEMENT si
   correspondance non ambiguë ; sinon laisser NO_RESOL. `fornos-de-algodres` et
   `trancoso` = district Guarda, HORS zone de service → nouvelle catégorie
   `OUT_OF_AREA` (ne pas patcher, lister pour Filipe).
4. Corriger le `SyntaxWarning` ligne 25 (raw string docstring).
5. **Synchroniser les 3 copies du script** — elles divergent déjà (17,4K vs 20,5K) :
   `canalizador-urgente/tools/p0.5-self-audit/` (source canonique, committée),
   `~/.openclaw/workspace/scripts/self-audit-zones.py`,
   `~/.hermes/skills/self-audit-batch/scripts/self-audit-zones.py`.
   Après v2 : même SHA sur les 3 (symlink vers la copie repo accepté).

## S1 — Ré-étalonnage (bloquant)

Lancer script v2 sur les 4 repos. **Poster les chiffres bruts** dans SEO_PLAN + commit :
- KO2bis attendu ≈ 842 − fixes déjà faits (baseline CEO : CNR 211 / ENR 218 / CU 211 / EU 202).
  Écart >10% vs baseline → **STOP, rapport, pas de vague** (leçon #298 : trianguler avant masse).
- Triage NO_RESOL restant **par cause** (préfixe manquant / typo / localité absente / OUT_OF_AREA)
  avec comptes → c'est le dossier D3 pour Filipe. Aucune action de masse sur NO_RESOL.

## S2 — Plan de vagues v2 (bloquant)

Redimensionner avec les vrais chiffres : KO1 restants + KO2bis réels + **les 594 KO3**
(pages prix body pré-OSRM : Z1=20€→15€, Z4=40€→45€…) + KO4 (-urgente, R145).
Vagues ≤100 fichiers, S2 page-entière (definition-of-done-page : les 8 surfaces,
même commit). Poster le plan dans SEO_PLAN. Étalonnage S1 matché = GO D5 couvert,
pas besoin de re-GO. Étalonnage KO = STOP.

## S3 — Exécution vagues

Branche `fix/prix-zones-osrm`, commits `fix(<repo>): P0.5 vague N` avec sortie
self-audit AVANT/APRÈS jointe (comme tes commits wip 17h — c'est le standard).
Garde-fous inchangés : pas de dist/, -es exclues, Offers JSON-LD service intacts,
grille canonique informative intacte, PR draft, pas de merge sans review.

## S4 — Clôture

Self-audit final 4 repos : KO1=0, KO2bis=0, KO3=0, KO4(-urgente)=0 sur périmètre
résolu. Chiffres bruts dans SEO_PLAN + PRs ready for review. Trees propres.

## Restent PENDANTS Filipe (ne pas toucher)

D3 (sort des NO_RESOL après triage S1) · D5-A doublons CNR · D5-B purge
"Chegada ~min" CNR (D1) · D5-C "mediante confirmação" (D2).
