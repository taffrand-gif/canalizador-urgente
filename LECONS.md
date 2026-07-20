# LECONS.md — canalizador-urgente · Phil-Hermes

> Mémoire locale du repo canalizador-urgente (satellite urgence 💧).
> Source de vérité globale : `~/.openclaw/workspace/AGENTS.md`.
> Format : 1 leçon = (date, contexte, takeaway actionnable, source).


---

## Leçon #geo-fresh-2026-07-18-01 — Article+datePublished GEO freshness pour piliers money

**Contexte** : audit GEO OpenClaw gap #4 a révélé que les `guias` CNR/ENR ont JSON-LD `Article` avec `datePublished`/`dateModified`/BreadcrumbList et sont les mieux cités par Perplexity/AIO, alors que les 5 piliers money CU/EU (`desentupir-canos`, `entupimento`, `desentupimento-esgoto`, `curto-circuito`, `falha-energia`) n'ont AUCUN de ces signaux. Risque : Perplexity/AIO classent les piliers comme "fraîcheur inconnue" et préfèrent les pages guides CNR/ENR même sur les requêtes money.

**Takeaway** : pour chaque pilier money Norte-OS (les pages qui portent les requêtes transactionnelles), ajouter DEUX blocs JSON-LD head-only : (1) `@type:Article` avec `headline=h1 nettoyé` + `author` + `publisher` (tous deux Organization Norte Reparos avec sameAs sur les 4 sites) + `datePublished=git log --format=%cs --reverse` (1er commit) + `dateModified=git log --format=%cs` (dernier commit) + `inLanguage=pt-PT` + `url/mainEntityOfPage` = canonique, (2) `@type:BreadcrumbList` `Início` → nom du pilier (sauf si déjà présent dans le @graph existant). **Dates JAMAIS inventées — toujours extraites de git log réel**.

**Action canon** :
1. **TOUJOURS** vérifier l'état existant avec `grep -c '"@type":"BreadcrumbList"' <fichier>` et `grep -c '"@type":"Article"' <fichier>` AVANT d'ajouter : EU avait déjà BreadcrumbList dans son @graph existant (n'en ajouter qu'un seul), CU n'avait rien (en ajouter deux).
2. **TOUJOURS** ancrer l'insertion sur un point unique (`</script>\n\n<style>` ou `</script>\n <style>` selon le repo) plutôt que de patcher dans une longue ligne JSON fragile.
3. **TOUJOURS** valider chaque bloc ajouté avec `json.loads()` + assert sur `datePublished`/`dateModified` qui doivent égaler `git log --format=%cs` réel.
4. **TOUJOURS** vérifier `git diff --shortstat` = insertions uniquement (0 deletion), et chaque `+line` ne contient que du JSON-LD/commentaire GEO freshness (pas de modification du body visible).
5. Pattern `author` Organization Norte Reparos canonique : `{"@type":"Organization","name":"Norte Reparos","url":"https://canalizador-norte-reparos.pt","sameAs":["https://eletricista-norte-reparos.pt","https://canalizador-urgente.pt","https://eletricista-urgente.pt"]}`. Pattern `publisher` ajoute `logo` pointant vers `https://canalizador-norte-reparos.pt/logo.png`.
6. **Headline = h1 nettoyé des emojis décoratifs** (🔧 🚿 🚰 ⚡ retirés), suffix marketing retiré — pas le `<title>` complet qui inclut `| Norte Reparos · 70€/h`.
7. Si `LECONS.md` n'existe pas dans le repo (cas CU), **en créer un** au format standard `## Leçon #<mission>-<date>-NN — <titre>` (Contexte / Takeaway / Action canon / Source) pour préserver l'apprentissage symétrique entre les 2 sites urgence.

**Source** : mission OpenClaw gap #4 « GEO fraîcheur » 2026-07-18, branches `feat/geo-freshness` depuis `HEAD` (et non `origin/main` qui était en retard de 4-5 PRs fusionnées, voir Leçon #geo-fresh-2026-07-18-02 bis sur ce point — TODO après cette PR). 5 fichiers modifiés : `desentupir-canos.html`, `entupimento.html`, `desentupimento-esgoto.html` (CU, +9 lignes = +3 par fichier) ; `curto-circuito.html`, `falha-energia.html` (EU, +6 lignes = +3 par fichier). PR DRAFT créées, **STOP validation Philippe avant merge** (R7 AGENTS.md).

## Leçon #geo-fresh-2026-07-18-03 — dateModified copié-collé sur datePublished : vérifier CHAQUE fichier contre git

**Contexte** : PR #186 (CU) et PR #171 (EU) ont été ouvertes avec Article+datePublished JSON-LD sur les piliers money (Leçon #geo-fresh-2026-07-18-01). Le brief initial exigeait `datePublished = git log --format=%cs --reverse` (1er commit) et `dateModified = git log --format=%cs` (dernier commit). Philippe a signalé en reviews « datePublished sont '2026-07-18' mais le brief exigeait la date du PREMIER commit git du fichier ». **Cause racine** : lors de la rédaction du JSON-LD, les dates ont été extraites correctement pour `datePublished` mais `dateModified` a été **copié-collé sur la même valeur que `datePublished`** (probablement réflexe « mêmes dates si même contenu »), au lieu d'aller chercher `git log --format=%cs | head -1` séparément.

**Takeaway** : avoir une datePublished correcte ne sert à RIEN si dateModified lui est identique — Perplexity/AIO interprètent dateModified comme le signal de fraîcheur et tombent sur "fraîcheur = datePublished" ce qui est équivalent à une page jamais retouchée. Le **contrôle de cohérence datePublished ≠ dateModified** doit être systématique avant commit, et chacun des deux champs doit pointer vers une commande git distincte.

**Action canon** :
1. **JAMAIS copier-coller** datePublished sur dateModified, même si on a l'impression que la page n'a eu qu'un commit. Toujours extraire séparément :
   - `datePublished = git log --format=%cs --follow -- <fichier> | tail -1` (1er commit, le plus ancien)
   - `dateModified  = git log --format=%cs -- <fichier> | head -1` (dernier commit, le plus récent)
2. **TOUJOURS valider** avec un tableau de preuve AVANT commit, par exemple :
   ```
   FILE | OK? | schema_pub | git_first | git_last
   foo.html | OK | 2026-07-17 | 2026-07-17 | 2026-07-18
   bar.html | OK | 2026-07-18 | 2026-07-18 | 2026-07-18  ← single-commit, dateModified == datePublished légitime
   ```
3. Cas légitime de `datePublished == dateModified` : **uniquement** quand `git log --oneline <fichier> | wc -l = 1` (fichier créé en un seul commit, jamais retouché). Les 5 articles blog MD->HTML de la tranche 16-20 sont dans ce cas et c'est correct. Les 3 piliers CU et 2 piliers EU money ne le sont PAS (3-5 commits d'historique).
4. **Gate CI-friendly** (à scripter dans `_audit/` ou pre-commit hook) :
   ```bash
   for f in $(git diff --name-only origin/main...HEAD -- '*.html'); do
     pub=$(grep -oE '"datePublished":"[0-9-]+"' "$f" | head -1 | sed 's/.*:"//;s/"//')
     mod=$(grep -oE '"dateModified":"[0-9-]+"' "$f" | head -1 | sed 's/.*:"//;s/"//')
     first=$(git log --format=%cs --follow -- "$f" | tail -1)
     last=$(git log --format=%cs -- "$f" | head -1)
     [ "$pub" = "$first" ] && [ "$mod" = "$last" ] || echo "KO $f"
   done
   ```
5. Pattern mental à adopter : « **schema dates = historique git, pas aujourd'hui** ». Ne JAMAIS utiliser `date $(today)` ou une date arbitraire pour datePublished. Toujours : 1er commit pour published, dernier pour modified.

**Source** : mission REPAIRS 2026-07-18 (3 fixes séquentiels) — diagnostic de Philippe sur PR #186 (CU) et PR #171 (EU). Audit complet a montré : CU 8 fichiers, 2 KO (`desentupimento-esgoto.html`, `desentupir-canos.html` : dateModified=2026-07-17 alors que dernier commit=2026-07-18). EU 2 fichiers, 1 KO (`falha-energia.html` : même symptôme). Tous corrigés et pushés. Tableaux de preuve dans les messages de commit `fix(*,geo-fresh): aligner dateModified sur dernier commit git réel`.

---

> Mémoire locale du repo canalizador-urgente (satellite urgência 💧).
> Source de vérité globale : `~/.openclaw/workspace/AGENTS.md`.
> Format : 1 leçon = (date, contexte, takeaway actionnable, source).

---

## Leçon #CU-CURATION-2026-07-19-01 — Doublon = grep core, pas grep core+self

**Contexte** : mission curation v2 sitemap-villages.xml CU. Audit READ-ONLY antérieur (commit 1ec42a1d3) avait listé 8 INSTITUC + 28 BLOG mal rangés dans le villages. Consigne : "vérifier si elles sont AUSSI dans sitemap core, si oui = doublon → retirer, sinon = déplacer vers core SEULEMENT si core les accueille logiquement". Le grep naïf `sitemap.xml` (racine) montrait 0 intersection, MAIS une lecture rapide du fichier a révélé que `sitemap.xml` et `public/sitemap.xml` étaient strictement identiques (104 URLs chacun) et qu'il manquait des pages éditoriales évidentes au core (pas de `sobre`, pas de `precos`, pas de `contactos`/`equipa`/`garantia`/`politica-cookies` n'étaient dans villages mais dans core — ce qui prouve que l'architecture core a vocation éditoriale).

**Takeaway** : "grep core" doit toujours être suivi d'une vérification que **le core accueille logiquement** la catégorie candidate, sinon c'est une note pour décision séparée (et non un déplacement aveugle). Le critère d'accueil logique = présence d'au moins 3 pages de même catégorie sémantique déjà dans core (ex : 3+ pages éditoriales/institutionnelles pour des INSTITUC).

**Action canon** :
1. Pour toute URL "mal rangée", grep core PUIS vérifier la **cohérence catégorielle** du core (3+ pages de la même catégorie ?)
2. INSTITUC (pages éditoriales/institutionnelles) → core si core a déjà `contactos`, `equipa`, `garantia`, `politica-*`, `metodologia`... → DÉPLACER
3. BLOG (articles éditorial long-format) → core n'a aucune page éditoriale long-format → NE PAS déplacer, NOTER pour décision (sitemap-blog dédié ? laisser hors-sitemap ? déplacer plus tard quand core évoluera ?)
4. Toujours vérifier l'intersection core ∩ villages APRÈS curation (doit être 0)

**Source** : PR #187 (worktree /tmp/cu-sitemap-cur), commit c1780b08c.

**Comptes** :
- sitemap-villages.xml : 2000 → 1964 URLs (−36 = 8 INSTITUC + 28 BLOG)
- sitemap.xml (core racine) : 104 → 112 URLs (+8 INSTITUC, priority=0.8)
- public/sitemap.xml (core publié) : 104 → 112 URLs (+8 INSTITUC, identique au core racine)
- 0 intersection core ∩ villages (pas de doublon créé)
- 0 village légitime retiré (V_STD=1528 + V_URGENTE=436 accents inclus = 1964 préservés)

**Décision séparée notée** : sort des 28 BLOG. Options à trancher : (a) créer `sitemap-blog.xml` dédié et le déclarer dans robots.txt après validation GSC, (b) les ajouter au core avec priority 0.5-0.6 (subordonné aux piliers 0.8), (c) les laisser hors-sitemap (découverte Google via liens internes uniquement). Aucune n'est appliquée ici — décision Filipe requise.

---

## Leçon #CU-CANONICAL-2026-07-20-01 — Triage FINAL CU = 0 bug, 12 bucket A legit

**Contexte** : re-triage FINAL des 1994 pages racine canalizador-*.html, post campagne de fixes #155/#156/#161/#162/#165/#174/#178 (2026-07-15 → 2026-07-20). PR #198 ouverte (audit only, 0 fix code).

**Résultat FINAL** :
- e_self_ref_ok : 1982 (clean, 99.4%)
- a_hub_money_legit : 12 (canonical cross-page vers money hub officiel)
- b/c/d/z/m : tous à 0

**Piège évité** : la classification bucket A ne doit PAS être purement structurelle ("préfixe urgent/non-urgent"). Elle doit valider que **la cible canon est réellement un money hub transactionnel** (présence prix/tel/whatsapp/orçamento). Sans ce filtre, on risque de fixer en self-ref des fichiers qui sont légitimement des variantes satellite d'un hub canonique (duplicate content assumé vs produit, pas bug SEO).

**Critère durable bucket A money hub** :
```python
MONEY_HINTS = re.compile(r'(\d+€|€/h|preço|tarifa|or[çc]amento|928 484 451|932 321 892|whatsapp|wa\.me)')
def is_money_hub(filepath):
    text = open(filepath, encoding='utf-8', errors='surrogateescape').read()
    return bool(MONEY_HINTS.search(text))
```

**Leçons connexes** :
- #CU-CANONICAL-2026-07-15-01 (méthode 4 buckets) → **complétée** par cette leçon : bucket A = cible money hub réel, pas juste "même concelho"
- #L1 (doctrine mémoire : canonical cross-page vers cible=money/hub même concelho = GARDER) → confirmée sur CU : 12 fichiers légitime, 0 faux positif
- Skill `local-business-seo-compliance` (R0 + `r0-canonical-selfref.md`) → R0 déjà passé (PR #174)

**Source** : PR #198, commit cfabad4f4 (branche `audit/t_b36c196a-canonical-final`). CSVs `_audit/canonical-triage-CU-FINAL.csv` (1994) et `_audit/canonical-bucket-A-CU-FINAL.csv` (12) durables.

**Anti-pattern documenté (anti-rebryc)**: NE PAS re-scanner à chaque tâche si les PRs #155-#178 sont déjà mergées. Toujours faire `git log --all --oneline | grep canonical` AVANT de relancer un scan, sinon on sature le contexte (cf. 4 reclaim/stale_lock 2026-07-16 sur cette tâche).

---

## Cross-références

- Sitemap tiering : voir `robots.txt` commentaires (sitemap.xml = core déclaré, sitemap-villages.xml préparé mais non référencé)
- Skill transversal : `local-business-seo-compliance` (R0 + ref `r0-canonical-selfref.md`)
- Tâche t_b36c196a close via PR #198 (audit only)
