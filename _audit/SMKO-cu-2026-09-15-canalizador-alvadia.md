# SMKO-cu-2026-09-15 — canalizador-alvadia dans sitemap.xml

## Verdict : KO PONCTUEL RÉFUTÉ

L'URL `https://canalizador-urgente.pt/canalizador-alvadia` est **SAINE**. Aucune modification du sitemap.xml. Re-tester au prochain delta.

## 1. Preuve initiale (brief)

- Tâche Kanban `t_3abf4307` (pool-keeper, 2026-09-15)
- Signalement : sitemap-delta 2026-09-15 marque l'URL avec HTTP code 000 (≠ 200)
- URL concernée : `https://canalizador-urgente.pt/canalizador-alvadia`
- Présence sitemaps : `sitemap.xml` ligne 44 + `public/sitemap.xml` ligne 44 (duplication connue, hors `sitemap-extra.xml` / `sitemap-villages.xml`)
- `<lastmod>2026-07-27</lastmod>` côté sitemap
- Rapport antérieur `_audit/SMKO-cu-2026-09-14-alvadia.md` (2026-09-14) — déjà KO ponctuel réfuté

## 2. Vérification curl côté worker (6 probes, edge Vercel)

| # | UA | HTTP | size | time_total |
|---|----|------|------|------------|
| 1 | Chrome 124 Linux | **200** | 12 953 B | 0.165 s |
| 2 | Googlebot 2.1 | **200** | 12 953 B | 0.160 s |
| 3 | Bingbot 2.0 | **200** | 12 953 B | 0.220 s |
| 4 | Safari 17 macOS | **200** | 12 953 B | 0.166 s |
| 5 | facebookexternalhit/1.1 | **200** | 12 953 B | 0.157 s |
| 6 | Safari + variante `.html` | **308** | 15 B | 0.158 s |

- **HTTP 200 stable** sur 5/6 probes (Chrome, Googlebot, Bingbot, Safari, Facebook)
- La 308 sur la variante `.html` est comportement Vercel normal : redirect 308 vers l'URL canonique no-extension
- Payload constant 12 953 B (cold-edge présent, hit immédiat)
- Edge Vercel `76.76.21.22` (cf. rapport 2026-09-14)

## 3. Vérification contenu HTML (référence 2026-09-14, non re-crawlé)

```
<title>Canalizador em Alvadia (Ribeira De Pena) — 24h/7d | Norte Reparos</title>
<h1>Canalizador em Alvadia</h1>
meta description conforme (NAP Ribeira De Pena, Z6 65 € taxa, 65 €/h)
last-modified: Mon, 14 Sep 2026 18:36:24 GMT
content-length: 12953
```

- title conforme pattern pSEO (keyword + bénéfice + 24h/7d)
- meta description conforme (prix explicite Zone 6 + 65 €/h + « orçamento por escrito »)
- h1 conforme (anti-keyword stuffing)

## 4. Décision

- **KO ponctuel réfuté** → NE PAS toucher aux sitemaps
- **0 commit** sur `sitemap.xml` / `public/sitemap.xml`
- **0 retrait** de ligne KO
- Consigne ici la preuve et attendre la prochaine indexation GSC (probable cold-edge / quota partagé entre les 4 sites Norte-OS)

## 5. Métadonnées

- Tâche : `t_3abf4307` (assignee `default`)
- Date rapport : 2026-09-15 (BST)
- Commit : N/A (KO ponctuel, aucune modification)
- Verdict : **KO PONCTUEL RÉFUTÉ** = URL SAINE
- Lignes sitemap concernées (à conserver) :
  - `sitemap.xml` ligne 44 : `<url><loc>https://canalizador-urgente.pt/canalizador-alvadia</loc><lastmod>2026-07-27</lastmod></url>`
  - `public/sitemap.xml` ligne 44 : idem

## 6. Leçon

Pas de nouvelle leçon. Confirmation que le pattern « signalement delta 000 sur sitemap.xml » reste systématiquement un **cold-edge transitoire** pour le site `canalizador-urgente.pt` (cf. SMKO antérieurs 2026-09-15 : `canalizador-angueira`, `canalizador-alturas-do-barroso`, `canalizador-almendra` — tous KO ponctuels réfutés avec HTTP 200 stable). Le sitemap ne doit **jamais** être modifié sur la base d'un delta 000 sans re-test curl 4+ probes. 2e confirmation successive sur la même URL à 24h d'écart → renforcer la confiance que ce signal est purement GSC et non réel.
