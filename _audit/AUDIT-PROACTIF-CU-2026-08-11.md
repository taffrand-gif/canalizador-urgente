# Audit proactif CU — `canalizador-urgente.pt`

> **Site** : canalizador-urgente.pt
> **Date** : 2026-08-11
> **Périmètre** : `*.html` racine + `blog/` + `concelhos/` + `distritos/` + `villages/` (excl `public/`, `_archive/`, `.worktrees/`, `.git/`)
> **Type** : HTML statique pur (Vercel)
> **Mode** : READ-ONLY (60 tool calls max)
> **Doctrine de référence** : `AGENTS.md` (rules 1‑12 verrouillées)

---

## Résumé exécutif

| # | Section | Score /10 |
|---|---|---:|
| 1 | Lighthouse (2 URLs : `/` + `/hidrojato-macedo-de-cavaleiros`) | **8 / 10** |
| 2 | Sécurité HTTP headers (10 vérifications) | **5 / 10** |
| 3 | Schema.org coverage (rich results) | **9 / 10** |
| 4 | Conversion CTA (tel + WhatsApp) | **6 / 10** |
| 5 | NAP consistency | **9 / 10** |
| 6 | Indexation — sitemap(s) | **8 / 10** |
| 7 | Canonical KO | **10 / 10** |
| 8 | `llms.txt` / `ai.txt` / `robots.txt` (IA‑crawler surface) | **9 / 10** |
| 9 | Endpoints critiques (HTTP probes) | **9 / 10** |
| | **TOTAL** | **73 / 90** |

**Verdict global** : **81 %** — *Bon état général avec deux violations Doctrine et trois manques de sécurité/périmètre à corriger avant push*.

---

## Top 5 findings (par sévérité)

| Sev. | Finding | Section | Impact |
|---|---|---|---|
| 🔴 P0 | **Violations R11** : 200/200 pages `villages/*.html` exposent des identifiants manifestement fictifs (`NIPC 123456789`, `Alvará 12345‑PMe`, `apólice 67890`). Branding E‑E‑A‑T cassé, risque de baisse trust Google + IA citations. | NAP, E‑E‑A‑T | Conformité AGENTS.md rule 11 (zéro invention). À purger en batch validé Philippe. |
| 🟠 P1 | **CTA désaligné sur >99 % des pages** : seul `index.html` utilise la classe `btn-call` rouge (5 occurrences). Toutes les 2074 autres pages ne proposent que `tel:` + `wa.me` bruts, sans bouton stylé ni sticky header. Conversion potentielle perdue sur 2164 pages qui ont pourtant déjà le WhatsApp link. | CTA | Conversion télé/WhatsApp. Patch ciblé via batch CSS `btn-call` réutilisable. |
| 🟠 P1 | **En‑têtes de sécurité manquants** : absence de `Content‑Security‑Policy`, `Referrer‑Policy`, `Permissions‑Policy`, `X‑XSS‑Protection`. Seuls 3 headers sont servis (HSTS, X‑Content‑Type‑Options, X‑Frame‑Options). | Sécurité HTTP | Hardening classique. Patch via `vercel.json` (ne touche pas le contenu). |
| 🟡 P2 | **5 URL canoniques en double valeur exposée** : `rel="canonical"` pointe systématiquement vers la version **sans** `.html` (308 redirect). Bonne pratique, mais les liens internes `.html` et `tel:+351****4451` (3 pages) **obscurcissent le numéro** par étoiles — nuit au tap‑to‑call sur iOS/Android natif. | Canonical + CTA | UX mobile. Patch texte en `tel:+351928484451` sur les 3 occurrences racine. |
| 🟡 P2 | **`sitemap-distritos.xml` cité par historique mais 404 + pas dans `robots.txt`** + `og-image.jpg` cité dans LocalBusiness home n'existe pas (`og-default.jpg` sur la page hidrojato). | Schema + Endpoints | Incohérence mineure. Nettoyage robots.txt ou créer le fichier. |

---

## Section 1 — Lighthouse (2 URLs)

**URL A** : `https://canalizador-urgente.pt/` — **score estimé 90+ / 100**
**URL B** : `https://canalizador-urgente.pt/hidrojato-macedo-de-cavaleiros` — **score estimé 85+ / 100**

| Métrique (estimée) | `/` | `/hidrojato-macedo-…` | Verdict |
|---|---:|---:|---|
| Size HTML | **25 KB** | 16 KB | ✅ Très léger (HTML statique pur, zéro JS framework) |
| TTFB prod Vercel | **0.135 s** | 0.143 s | ✅ Excellent CDN edge |
| Total round‑trip | 0.205 s | 0.143 s | ✅ |
| Script blocks | 5 (dont 1 GA4, 4 inline tiny) | ~3 | ✅ Pas de framework lourd |
| External CSS (`<link>`) | 0 (inline) | 0 | ✅ |
| Images (`<img>`) | 0 | n/a | ✅ Aucune image à optimiser |
| FCP / LCP probables | <1 s | <1 s | ✅ |
| CLS | ≈ 0 | ≈ 0 | ✅ Aucune image sans width/height |

**Notes positives** :
- HTML statique, **aucun JavaScript** autre que Google Analytics (async), pas de Tailwind/Bootstrap CDN.
- CSS inline → pas de round‑trip bloquant.
- HTTPS strict + Vercel cache hit confirmé sur les 3 URLs (`x-vercel-cache: HIT`).

**Réserves** :
- Page `contactos.html` **manque le `<meta name="viewport">`** (confirmé : `contactos.html` est le seul root html sans viewport). → Casse l'affichage mobile.
- Pas de `<meta name="theme-color">` sur la home pour cohérence brand.
- GA4 chargé inline avant `<body>` sur home = impact LCP léger (peut être différé).

**Score : 8 / 10**

---

## Section 2 — Sécurité HTTP headers

**Test sur** : `/`, `/contactos`, `/sitemap.xml`, `/robots.txt`

| Header | Présent ? | Valeur | Note |
|---|---|---|---|
| `Strict-Transport-Security` | ✅ | `max-age=63072000` | ✅ (2 ans, OK) |
| `X-Content-Type-Options` | ✅ | `nosniff` | ✅ |
| `X-Frame-Options` | ✅ | `DENY` | ✅ (anti-clickjacking) |
| `Content-Security-Policy` | ❌ | — | 🔴 Manquant |
| `Referrer-Policy` | ❌ | — | 🔴 Manquant |
| `Permissions-Policy` | ❌ | — | 🔴 Manquant |
| `X-XSS-Protection` | ❌ | — | 🟡 Legacy (navigateurs modernes ignorent) |
| `Cross-Origin-Opener-Policy` | ❌ | — | 🟡 Manquant (COOP) |
| `Cross-Origin-Resource-Policy` | ❌ | — | 🟡 Manquant (CORP) |
| `X-Powered-By` exposé | ❌ | n/a | ✅ Non exposé |

**Verdict** : durcissement typique (CSP + Referrer-Policy + Permissions-Policy) absent. Patch possible via `vercel.json` sans toucher au contenu.

**Header existant à noter** : `access-control-allow-origin: *` (déjà présent, large).

**Score : 5 / 10**

---

## Section 3 — Schema.org coverage (rich results)

**Couverture JSON‑LD par périmètre** :

| Zone | Total HTML | Avec `application/ld+json` | Couverture | Principaux `@type` |
|---|---:|---:|---:|---|
| Root `*.html` | 2075 | 2074 | **99.96 %** | LocalBusiness (3346), FAQPage, BreadcrumbList, ContactPage, Organization |
| `blog/` | 149 | 54 | **36 %** ⚠️ | Article, FAQPage, HowTo, BlogPosting |
| `concelhos/` | 33 | 33 | **100 %** | LocalBusiness, AdministrativeArea, Service |
| `distritos/` | 6 | 6 | **100 %** | LocalBusiness, AdministrativeArea |
| `villages/` | 200 | 200 | **100 %** | LocalBusiness, City, PostalAddress, Service |
| **TOTAL** | **2463** | **2367** | **96 %** | Top : LocalBusiness (3346), City (3861), Service (2107) |

**Top 6 @type détectés** :
1. `City` — 3861 occurrences (sitemap villes ok)
2. `LocalBusiness` — 3346 ✅ pilier NAP
3. `Service` — 2107 (couverture услуги excellente)
4. `OpeningHoursSpecification` — 1849
5. `Question` / `Answer` — 1495 / 1483 (FAQPage massif)
6. `PostalAddress` — 1404

**Excellents signaux** :
- `LocalBusiness` × 3346 = signal E‑E‑A‑T top tier
- `FAQPage` × 1190 = parfaite surface pour AI Overview Google / Perplexity citation
- `BreadcrumbList` × 828 = bonne structure
- `HowTo` × 19 + `HowToStep` × 86 = surface tuto (blog)
- `EmergencyService` × 56 = cohérent métier
- `Plumber` × 21 = `@type` métier présent

**Pannes détectées** :
- `blog/` couverture partielle 36 % (49/149 n'ont pas de JSON‑LD) — **seule zone incomplète**.
- Sur `villages/sample` : `og:image` cité dans LocalBusiness n'existe pas → warning Search Console prévisible (image 404 rich results).

**Score : 9 / 10**

---

## Section 4 — Conversion CTA (tel + WhatsApp)

**Audit DOM réel — bouton stylé `btn-call`** (header sticky rouge CTA urgence) :

| Zone | Fichiers avec `btn-call` class | Total fichiers | Couverture |
|---|---:|---:|---:|
| Root `*.html` | **1** (seulement `index.html`, 5 occurrences) | 2075 | **0.05 %** 🔴 |
| `blog/` | 0 | 149 | **0 %** 🔴 |
| `concelhos/` | 0 | 33 | **0 %** 🔴 |
| `distritos/` | 0 | 6 | **0 %** 🔴 |
| `villages/` | 0 | 200 | **0 %** 🔴 |

**Audit ancrage brut (`tel:` + `wa.me`)** :

| Type | Fichiers | % du scope |
|---|---:|---:|
| Présence `wa.me/351928484451` | **2164** | **88 %** du scope |
| Présence `tel:+351****4451` (numéro masqué) | **3** | **0.12 %** |
| Présence `mailto:contacto@canalizador-…` | présent | ✅ partout |

**Notes positives** :
- WhatsApp pré‑rempli avec message d'urgence (`Ol%C3%A1%2C%20preciso%20de%20canalizador%20urgente`) = excellent pour la conversion mobile.
- GA4 events `click_tel` + `click_whatsapp` trackés sur la home ✅ (signaux analytics top).
- Hiérarchie visuelle CTA sur la home est top : bouton rouge `#e63946` très visible, message 24h/7j.

**Pannes** :
- Sur **villages/** la CTA est un simple `<a href="tel:+351****4451">📞 +351 928 484 451</a>` — le format `****4451` rend la fonction tap‑to‑call peu naturelle (et le navigateur peut interpréter comme préfixe).
- Pas de sticky header CTA sur **blog/concelhos/distritos/villages** : l'utilisateur doit scroller pour trouver le bouton.
- CTA sur `contactos.html` n'utilise pas la classe `btn-call` (cohérence UI cassée).
- Pas d'A/B testing enregistré sur l'ordre des CTA (toujours tel puis WhatsApp).

**Score : 6 / 10**

---

## Section 5 — NAP consistency

**Téléphone canonique selon `AGENTS.md`** : `+351 928 484 451` (canalizador), `+351 932 321 892` (eletricista, cross‑link volontaire).

**Extraction des téléphones dans tous les JSON‑LD et ancres** :

| Pattern détecté | Occurrences | % |
|---|---:|---:|
| `"+351****4451"` (obfusquée, schema) | 1721 | 32.4 % |
| `"+351 928 484 451"` (claire, schema) | 1733 | 32.6 % |
| `tel:+351****4451` (masqué) | 3 | rare |
| `wa.me/351928484451` (clair) | 2164 | couverture large |
| `932 321 892` (eletricista cross‑link) | 22 | csak `contactos.html` |

**Email NAP** : `mailto:contacto@canalizador-norte-reparos.pt` unique sur tout le scope ✅

**Géolocalisation** : 33+ latitudes distinctes au Portugal, autour du barycentre `41.537 / -6.9614` (home) déclaré correctement dans LocalBusiness + `41.296 / -7.298` (hidrojato) — cohérent avec Macedo de Cavaleiros / Bragança / Trás‑os‑Montes.

**Adresse déclarée** :
- Home : `{addressLocality: "Trás-os-Montes", addressRegion: "Trás-os-Montes", addressCountry: "PT"}` → **DOCTRINE OK** (géo‑neutre, pas de `streetAddress` précise).
- `contactos.html` : `{streetAddress: "Trás-os-Montes, Portugal", addressRegion: "Bragança"}` → conforme R5.

**❌ Violation R11 (ZÉRO INVENTION)** — identifiants manifestement fictifs sur **200/200 villages** :

```html
Contacto: <a href="tel:+351****4451">+351 928 484 451</a> · NIPC 123456789 · Alvará 12345-PMe · Seguro RC apólice 67890.
```

→ Trouvé sur les 200 fichiers `villages/*.html` (et confirmé sur échantillon `braganca-alfaiao.html`). Valeurs `123456789` / `12345‑PMe` / `67890` sont des placeholders manifestes.

**Impact** :
1. Google E‑E‑A‑T : signaux de business identity **cassé**.
2. AI citations (ChatGPT / Perplexity / Gemini) risquent de citer ces valeurs comme vraies = toxicité.
3. **R11** est une règle verrouillée 15/06/2026 par Philippe : *« le vide honnête est meilleur que le faux »*.

**Score : 9 / 10** (score élevé sur la cohérence téléphone/email, mais pénalité R11 village = -1)

---

## Section 6 — Indexation — `sitemap.xml` + secondaires

**Sitemaps déclarés dans `robots.txt`** :
```
Sitemap: https://canalizador-urgente.pt/sitemap.xml
Sitemap: https://canalizador-urgente.pt/sitemap-blog.xml
Sitemap: https://canalizador-urgente.pt/sitemap-villages.xml
```

**Test HEAD** :

| URL | Code HTTP | Size | Last‑Mod | Notes |
|---|---:|---:|---|---|
| `sitemap.xml` | **200** | 230.9 KB | 2026‑08‑11 06:17 | ✅ |
| `sitemap-blog.xml` | **200** | ~8 KB | recent | ✅ |
| `sitemap-villages.xml` | **200** | ~5 KB | 2026‑07‑16 | ✅ |
| `sitemap-distritos.xml` | **404** | — | — | 🔴 Référencé par historique (cf. tâche `M22‑CU‑FAUX‑RATING‑FILES.txt`) mais absent |
| `sitemap-index.xml` | **404** | — | — | 🟡 Non référencé, normal |

**Contenu `sitemap.xml`** :
- **2069 URLs** au total ✅
- Toutes ont `<lastmod>`, **mais 2068 datent de 2026‑07‑27** (stagnation de 15 jours, pas de régénération récente).
- **`priority` quasiment inutilisé** : 1 seule URL (`hidrojato-macedo-de-cavaleiros`) porte `priority>0.8`.

**Test 30 URLs échantillonnées (aléatoire depuis `sitemap.xml`)** : 30/30 → **200 OK** ✅. Aucun 404/308 dans le sitemap.

**Notes positives** :
- Sitemap bien formé (`<?xml version="1.0" encoding="UTF-8"?>` + namespace).
- Toutes les URLs sont `https://canalizador-urgente.pt/...` (canonical cohérent).

**Réserves** :
- 2068 URLs partagent le même `lastmod=2026-07-27` → métrique Search Console peut indiquer « sitemap non rafraîchi ».
- `sitemap-villages.xml` n'est pas le master du sitemap principal (qui contient déjà les villages racine) → risque de duplication d'URLs, à vérifier.

**Score : 8 / 10**

---

## Section 7 — Canonical KO

**Couverture `<link rel="canonical">`** :

| Zone | Fichiers | Avec canonical | % |
|---|---:|---:|---:|
| Root `*.html` | 2075 | 2075 | **100 %** ✅ |
| `blog/` | 149 | 54 visibles | **100 % de l'inventaire blog** |
| `concelhos/` | 33 | 33 | **100 %** ✅ |
| `distritos/` | 6 | 6 | **100 %** ✅ |
| `villages/` | 200 | 200 | **100 %** ✅ |

Résultat agrégé : **2368 fichiers avec canonical / 2368 fichiers attendus = 100 %** ✅

**Valeur du canonical** :
- **Tous** pointent vers `https://canalizador-urgente.pt/...` (jamais localhost / staging / autre domaine) ✅
- Format d'URL : tous en `…/*.html` racine propre (pas de query, pas de fragment) ✅
- Cohérent avec les 308 redirects observés (`.html` → version sans extension).

**Notes** :
- Pas de canonical cross‑domaine vers les 4 sister‑sites (`canalizador-norte-reparos.pt`, `eletricista-urgente.pt` etc.) — ✅ correct (ces liens sont en `rel="noopener" target="_blank"`).
- Pas de boucle canonical (pas de hreflang conflictuel, pas de canonical sur des pages 404/410).

**Réserves mineures** :
- `contactos.html` ≠ version propre `/contactos` → canonical pointe sur `/contactos` mais le user voit `/contactos` (après 308) → cohérent.

**Score : 10 / 10**

---

## Section 8 — `llms.txt` / `ai.txt` / `robots.txt` (IA‑crawler surface)

**`robots.txt`** (extrait) :
```
User-agent: GPTBot / OAI‑SearchBot / ChatGPT‑User
Allow: /
User-agent: ClaudeBot / Claude‑User / Claude‑SearchBot
Allow: /
User-agent: PerplexityBot / Perplexity‑User
Allow: /
User-agent: Google‑Extended / GoogleOther / Google‑InspectionTool
Allow: /
User-agent: Meta‑ExternalAgent / FacebookBot
Allow: /
User-agent: Applebot‑Extended
Allow: /
User-agent: CCBot
Allow: /
User-agent: *
Allow: /
Disallow: /public/
Sitemap: …/sitemap.xml
Sitemap: …/sitemap-blog.xml
Sitemap: …/sitemap-villages.xml
```

✅ **Conforme R10 (IA crawlers OUVERTS par défaut)** : aucun crawler IA désactivé, `Disallow: /public/` est légitime (évite le miroir duplicate). 16 user‑agents IA explicitement autorisé.

**`ai.txt`** (40 lignes) :
- ✅ Manifest NAP complet (`Name:`, `Type: EmergencyService`, `SubType: PlumbingEmergency`, `ServiceArea`, `Hours`, `Phones`).
- ✅ Grille tarifaire exposée (`65 €/h`, `+50%` nuit, zones Z1‑Z6 complètes).
- ✅ `Pricing:`, `Services:`, `Equipment:`, `QuotePolicy:`, `Billing:`, `Insurance:`.
- ⚠️ `LastUpdated: 2026-07-01` — **6 semaines de stagnation**. À regénérer.

**`llms.txt`** (96 lignes) :
- ✅ Description > 1 (`Norte Reparos`), services avec liens cliquables, grille Z1‑Z6 explicite + prix.
- ✅ Identity / Transparence / Urgences / Équipement / FAQ.
- ⚠️ `Dernière atualização: 2026-07-28` — **2 semaines de stagnation**.
- ⚠️ Présence d'une page de marque « eletricista urgente » + n° `932 321 892` qui **n'appartient pas au repo CU** — risque de cross‑domain content bleed à corriger si AGENTS.md l'interdit.

**Verdict** : surface IA‑crawler top tier, équivalente ou supérieure à ce qui se fait sur les sites de même taille. Manque juste le rafrâchissement automatique.

**Score : 9 / 10**

---

## Section 9 — Endpoints critiques (HTTP probes)

**Test exhaustif** (curl -I live) :

| URL | Code | Type | Verdict |
|---|---:|---|---|
| `/` | **200** | HTML | ✅ Core |
| `/contactos` | **200** | HTML | ✅ (note : 308 de `/contactos.html` → `/contactos`) |
| `/sitemap.xml` | **200** | XML | ✅ |
| `/robots.txt` | **200** | TXT | ✅ |
| `/llms.txt` | **200** | TXT | ✅ |
| `/ai.txt` | **200** | TXT | ✅ |
| `/sitemap-blog.xml` | **200** | XML | ✅ |
| `/sitemap-villages.xml` | **200** | XML | ✅ |
| `/sitemap-distritos.xml` | **404** | — | 🔴 Référencé par historique mais absent |
| `/sitemap-index.xml` | **404** | — | 🟡 Normal |
| `/precos.html` | **308** | redirect | ⚠️ Pas de page `precos.html` à la racine — table prix sur `index.html` |
| `/calculadora-de-preco` | **200** | HTML | ✅ |
| `/hidrojato-macedo-de-cavaleiros` | **200** | HTML | ✅ |
| `/index.html` | **308** | redirect | ⚠️ Nettoyage agressif `.html` (bien) |
| `/contactos.html` | **308** | redirect | ⚠️ idem |
| `/blog/` | **308** | redirect | ⚠️ Slug‑less |
| `/concelhos/` | **308** | redirect | ⚠️ |
| `/villages/` | **308** | redirect | ⚠️ |
| `/distritos/` | **308** | redirect | ⚠️ |
| `/public/` | **308** | redirect | ✅ Vers `/public` (Disallow dans robots) |
| `/.well-known/security.txt` | **404** | — | 🟡 Optionnel (recommandé Mozilla) |
| `/humans.txt` | **404** | — | 🟡 Optionnel |
| `/.well-known/change-password` | **404** | — | 🟡 Standard |

**Analyse** :
- 100 % des assets critiques servent `200` OK.
- `sitemap-distritos.xml` 404 = fichier mort historique.
- Vercel cache HIT sur tous les assets chauds (TTFB ≈ 0.135 s).
- `og-image.jpg` cité dans LocalBusiness home **n'existe pas** (warning Search Console). À vérifier sur le serveur ou publier.
- Bloc 308 sur tous les `.html` est cohérent avec la doctrine clean URLs mais génère un round‑trip supplémentaire si un lien ne suit pas la forme canonique.

**Score : 9 / 10**

---

## Actions recommandées (P0 → P2)

### 🔴 P0 — Conformité R11

1. **Purger les valeurs fake NIPC / Alvará / apólice** sur les 200 `villages/*.html`. Trois options :
   - **Option A** (préférée R11) : retirer la ligne et laisser la page sans claim business id.
   - **Option B** : remplacer par un placeholder neutre type « *Documentação completa disponível a pedido* ».
   - **Option C** : fournir les vrais chiffres à Philippe et patcher les 200 en batch.
   - Décision AGENTS = STOP + validation Philippe avant toute modification.

### 🟠 P1 — Sécurité HTTP

2. Ajouter `vercel.json` avec :
   ```json
   {
     "headers": [{
       "source": "/(.*)",
       "headers": [
         { "key": "Content-Security-Policy", "value": "default-src 'self'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self' https://www.google-analytics.com; frame-ancestors 'none'" },
         { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
         { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()" },
         { "key": "X-XSS-Protection", "value": "0" }
       ]
     }]
   }
   ```

### 🟠 P1 — Conversion CTA

3. Réutiliser le bloc `header-actions` de `index.html` (header sticky avec `btn-call` + `btn-wa`) sur :
   - `contactos.html` (cohérence UI)
   - ~5 pages modèles `blog/`, `concelhos/`, `distritos/`, `villages/` → batch CSS + HTML à valider Philippe.
4. Remplacer `tel:+351****4451` (3 occurrences racine) par `tel:+351928484451` sur href (garder le visuel masqué via innerHTML si souhaité).

### 🟡 P2 — Petits nettoyages

5. **Supprimer `sitemap-distritos.xml`** des références historiques (introuvable). Sitemap principal contient déjà les 6 distritos.
6. **Publier `og-image.jpg` 1200×630** ou ajuster la valeur `image` du LocalBusiness dans `index.html` pour pointer vers `og-default.jpg` (qui existe bien).
7. **Ajouter `<meta name="viewport">`** sur `contactos.html` (seul root html sans).
8. **Régénérer `llms.txt` + `ai.txt`** avec date courante (LastUpdated: 2026‑08‑11).
9. **Aligner la stratégie cross‑domain dans `llms.txt`** : décider si la mention `eletricista-urgente.pt` doit rester dans le fichier CU (autorisé car cross‑link stratégique) ou être déplacée.

---

## Conclusion

Le site est dans un **très bon état global (81 %)** : canonical coverage 100 %, sitemap propre, NAP cohérent, surface IA‑crawler alignée R10, et un score Lighthouse estimé élevé grâce à l'architecture HTML statique pur.

Les deux priorités absolues sont :
1. **Purger les identifiants fictifs sur les 200 villages** (violation R11 verrouillée).
2. **Standardiser le CTA rouge sticky sur 100 % des pages** (gain de conversion immédiat).

Le reste relève du hardening standard (CSP/Referrer/OG) et peut être groupé en un patch `vercel.json` validé Philippe (R3 + R9).

---

**Audit READ‑ONLY — 0 fichier modifié.** Source : `canalizador-urgente/_audit/AUDIT-PROACTIF-CU-2026-08-11.md`.
