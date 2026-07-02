# MISSION HERMES P0.6 — DOMINATION : PRIX JUSTES EN PROD + OFFENSIF — 2026-07-03

> Audit CEO #4 : tier-1-bis vérifié **0 résiduel** contre-mesure indépendante (828→0). Bravo,
> défaut audit #3 corrigé proprement. **9/10.** Maintenant : la vision. Le monopole SERP/GEO
> (MONOPOLE_SEO_2026Q3.md) ne se gagne pas avec des commits en draft — il se gagne avec des
> prix justes DEVANT les clients et du trust irréprochable. Ordre strict U1→U4.

## État mesuré (script v3, 03/07 après tier-1-bis)

KO1 180 · KO2 323 · KO2bis 11 · KO2ter 2 693 (zone_attendue 419 + body_seul ~2 274) ·
KO3 653 · KO4 214 = **4 074 KO restants** · NO_RESOL unknown 6 561 (D3, ne pas toucher le fond).

## U1 — Finir P0.5 tiers 2-N (les prix faux restants)

Même machine que le tier 1 (elle marche, 828→0 prouvé) : vagues ≤100, page entière,
self-audit AVANT/APRÈS dans chaque commit, re-run final AVANT tout claim « fin ».
Ordre par impact client visible : KO3 prix body (653, argent affiché faux) →
KO2ter zone_attendue + body_seul → KO1 badges (180) → KO2 JSON-LD (323) →
KO4 délais R145 -urgente (214). Sur pages NO_RESOL : cohérence interne seulement
(aligner sur badge), fond du contenu = D3 Filipe.
**Clôture U1 = sortie script : 0 KO sur périmètre résolu, collée dans le commit final.**

## U2 — MISE EN PROD (le vrai déblocage domination)

Tout le travail depuis le 02/07 est en branche draft. Les clients voient ENCORE les vieux prix.
1. Self-audit final 4 repos (U1 fini) + grep témoins R8 → rapport de merge par repo.
2. PRs #127 CNR / #114 ENR / #101 CU / #101 EU : draft → **ready for review** avec le rapport.
3. **STOP — merge main = validation Filipe** (doctrine repo, jamais merger sans GO).
   Prépare TOUT pour que le GO de Filipe = 1 clic par PR.
4. Post-merge (dès GO reçu) : vérifier déploiement Vercel OK + purge cache Cloudflare +
   spot-check 5 pages en PROD (curl) par repo — les bons prix visibles, preuve à l'appui.

## U3 — P0.3 FAUX AVIS (parallèle à U1, ne dépend de rien)

`GoogleReviews.tsx` CNR+ENR : 6+4 faux avis codés en dur, **EN PROD, risque légal actif**
(DECO + R11 + E-E-A-T). Plus gros ROI trust/heure du backlog. Purger composant + schema
Review associé → remplacer par bloc honnête (garanties réelles : orçamento por escrito
ANTES, 7/7, DGEG en attente co-signature LDE). JAMAIS de faux substitut. Branche dédiée,
PR ready, même STOP merge.

## U4 — OFFENSIF (dès U2 mergé) : les 2 chantiers monopole

1. **M1 maillage hub↔localité** : hubs concelhos/distritos à 2 liens sortants (norme 10-30),
   38 pages CNR+ENR puis les 4 repos. Cause n°1 identifiée du sous-ranking. Vagues+self-audit
   (compteur liens/hub AVANT/APRÈS).
2. **M2 différenciation intent** norte vs urgente (`seoKeywords.ts`, H1/FAQ distincts,
   261 localités communes) : stop cannibalisation = 2 résultats organiques par requête
   au lieu d'1 = cœur du monopole multi-surfaces.

## Décisions Filipe (rien d'autre ne bloque)

| # | Décision | Impact |
|---|---|---|
| GO merge | 4 PRs ready après U1 | les prix justes passent en prod |
| D1 | "Chegada ~min" CNR 1873 pages : purger (reco CEO : purger, cohérence ENR=0) | conformité |
| D2 | "mediante confirmação" purge globale | conformité |
| D3 | 6 561 NO_RESOL : fallback concelho / prune | fin normalisation totale |
| D4 | ≥1 avis client réel (WhatsApp+consentement) — action Filipe hors code | débloque étoiles P4 |

## Garde-fous inchangés

Transparence Radicale prime. JAMAIS inventer (prix/avis/délai/chantier). Pas de dist/,
-es exclues, R145 strict -urgente, SAB : adresse rue jamais publique. Réversible = décide
et documente ; merge/prod/301 = STOP Filipe.
