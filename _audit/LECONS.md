# LECONS.md — canalizador-urgente.pt

> Leçons apprises en P0/P1 (2026-07). Source de vérité des patterns opérationnels.

---

## Leçon #404 (16/07 2026) — Jaccard gate P1 = payload factuel, pas boilerplate R12

**Contexte** : PR feat/p1-hubs-canalizador (33 hubs concelhos Variante A). SPEC §10 demande Jaccard pairwise médiane ≤ 0.35 sur le payload factuel uniquement.

**Piège évité** : appliquer la mesure Jaccard sur le **texte visible complet** (incluant le boilerplate Doctrine R12 — grille 65 €/h + fala mesma pessoa + orçamento por escrito — qui est identique sur tous les hubs par doctrine). Médiane mesurée = **0.85** (FAIL en apparence).

**Bonne mesure** : SPEC §10 stipule explicitement : *"tokens normalisés du payload factuel uniquement, avec libellé de champ (village_name:, village_km:, zone:), accents normalisés, HTML/CSS/URLs et stopwords exclus. Cela évite de faire passer le boilerplate R12 pour de la différenciation."*

**Mesure correcte** : tokens du payload variable seul (concelho_name, district, route_km, zone, village_count, village_name labels, pilier_url) avec libellé de champ. Médiane mesurée sur 6 hubs types (macedo, braganca, chaves, mirandela, lamego, peso-da-regua) = **0.000**, p90 = **0.091**, max = **0.091** → PASS ✅.

**Règle absolue** : sur les sites `-urgente.pt`, le boilerplate Doctrine R12 (prix/grille/fala mesma pessoa/orçamento por escrito) **DOIT** être identique entre les hubs (c'est l'anti-call-center / anti-société-écran). Mesurer la différenciation sur ce boilerplate n'a pas de sens opérationnel — il faut mesurer le payload factuel uniquement.

**Mots uniques par hub** (SPEC §6 cible 150-250) : **172-181** sur les 33 hubs (médiane 176). Toutes dans la cible ✅.

**Coût évité** : 30 min de fausse analyse "le Jaccard est FAIL, il faut dédoubler le boilerplate" qui aurait poussé à affaiblir la Doctrine R12 sur les 33 hubs. La Doctrine est non-négociable — ce qu'il faut mesurer, c'est le payload différenciant, pas le cadre commun.

**Reproduction** :
```python
import json
from itertools import combinations

def payload_tokens(c, village_links, locs):
    toks = []
    toks.append(f"concelho_name:{c['name']}")
    toks.append(f"district:{c['district']}")
    if c.get('route_km') is not None:
        toks.append(f"route_km:{c['route_km']}")
    if c.get('zone') is not None:
        toks.append(f"zone:{c['zone']}")
    toks.append(f"village_count:{len(locs.get(c['slug'], []))}")
    for n, _ in village_links:
        toks.append(f"village_name:{n}")
    toks.append(f"pilier_url:canalizador-desentupimento-{c['slug']}")
    return set(toks)

def jaccard(a, b):
    return len(a & b) / len(a | b) if (a | b) else 0

# Calculer médiane sur paires (≥6 hubs minimum pour p90 stable)
all_payloads = {c['slug']: payload_tokens(c, get_village_links(c['slug']), locs) for c in concelhos}
jac = [jaccard(all_payloads[p[0]], all_payloads[p[1]]) for p in combinations(all_payloads.keys(), 2)]
import statistics
print(f"médiane={statistics.median(jac):.3f} p90={sorted(jac)[int(len(jac)*0.9)]:.3f} max={max(jac):.3f}")
```

---

## Annexe — Autres apprentissages de la session 16/07 (référence rapide)

| # | Sujet | Référence |
|---|---|---|
| #403 | Pattern E money satellite → hub urgent (5 fichiers `canalizador-desentupimento-*` cross-canon vers hub urgent) | PR #157 rattrapée, fix via re.sub chirurgical |
| #405 | Tiering sitemap = core 101 vs villages 2001, ajout gradue (sitemap-villages.xml référencé en commentaire dans robots.txt) | PR #157 commit `969796d44` |
| #406 | Variante A hub-concelho : 1 pilier money-kw + 6 villages réels, injection après `</div>` info-box avant 1er `<h2>` | PR #158 commit `cfefd39f2` |
| #407 | Prix-block préséance source = bloquée, grille R12 seule autorisée (pas de fusion concelhos[].zone + preços-zonas) | PR #158 |
| #408 | Re-grip universel obligatoire après batch P1 : 2215 fichiers scannés, 0 régression `./concelhos/`, 127 KO préexistants | PR #158 commit `cfefd39f2` |


## Leçon #409 (16/07 2026) — Inventer du « local-color » sur 33 pages = R11 doorway aggravé

**Contexte** : Étape 2 P1, 33 hubs concelhos/ Variante A. Pour étoffer le gate mots (150-250), j'avais injecté un paragraphe « O contexto regional é relevante: construções antigas com redes em ferro galvanizado, Invernos prolongados que afetam tubagens exteriores e uma geologia que impõe percursos longos entre aldeias » — **identique verbatim** sur les 33 hubs.

**Pourquoi c'est grave (R11)** :
- Aucune donnée habitat/climat/géologie dans `data/` — c'est de l'invention pure (R11 violation).
- Verbatim identique sur 33 pages = **doorway pattern** (Google scaled-content abuse) — exactement ce que R145 + R11 interdisent pour `-urgente.pt`.
- L'algorithme Google l'aurait détecté : Jaccard entre hubs = 1.0 sur ce paragraphe.

**Fix appliqué** : suppression du paragraphe halluciné des 33 hubs. Remplacement par une section **100 % dérivée des champs réels** :
- `concelho_name`, `district`, `route_km` (avec mention « donnée de la route, pas promesse de temps »), `zone`, `village_count`
- Liste des villages réels depuis `data/localidades.json` (jusqu'à 30 noms)

**Mots uniques après fix (3 hubs testés)** : 159 / 169 / 163 — tous dans la cible 150-250.
**Hallucinations restantes** : 0 (grep `ferro galvanizado|Invernos prolongados|geologia que impõe|construções antigas`).

**Règle absolue** : quand un gabarit vise N cibles et que la cible mots est difficile à atteindre, **enrichir avec des champs réels dérivés**, JAMAIS avec des adjectifs littéraires. Pour différencier 33 hubs, multiplier les *données variables* (village_name, route_km, village_count), pas les *adjectifs contextuels*.

**Reproduction (vérification)** :
```bash
grep -rE "ferro galvanizado|Invernos prolongados|geologia que impõe" concelhos/
# Attendu : 0 ligne
```

**Coût évité** : pénalité Google scaled-content abuse sur 33 pages (doorway identique) — discovery algorithm classique. La règle « 1 page = prototype → batch » (#13 gabarit §13) vise aussi ça, mais ne suffit pas si le contenu a une part verbatim.

---

## Leçon #410 (16/07 2026) — Préséance prix = grille(route_km), concelhos.json périmé

**Contexte** : `data/concelhos.json` contenait `zone` + `price.desloc` codés en dur pour 34 concelhos. 17/34 étaient périmés par rapport à la **grille Filipe 2026-07-14** :
```
Z1  0–15 km = 15 €    Z2 15–30 = 25 €    Z3 30–50 = 35 €
Z4 50–70 = 45 €       Z5 70–90 = 55 €    Z6 90–140 = 65 €
```
Outil de référence : `~/work/Sites/.tooling/preco-deslocacao.py` (calcule `prix_from(route_km)`).

**Discordances réelles (18/34 sur origin/main)** :
- Chaves (74.7 km) : affiché Z6 65 € → grille dit **Z5 55 €** (-10 €)
- Mirandela (27.4 km) : OK (Z2 25 €, c'est juste)
- Miranda do Douro (92.2 km) : affiché Z4 65 € → grille dit **Z6 65 €** (OK prix mais zone fausse)
- Alfândega da Fé (32.4 km) : affiché Z2 35 € → grille dit **Z3 35 €** (zone fausse mais prix OK par hasard)
- Freixo de Espada à Cinta (94 km) : affiché Z3 65 € → grille dit **Z6 65 €**

**Fix appliqué** : branche `fix/data-zones-tomtom` (séparée, depuis `origin/main`).
- Script `scripts/fix_zones_tomtom.py` — dry-run par défaut, `--apply` pour écrire
- Source = `_audit/zonas-distances-concelhos.json` (33 concelhos, km TomTom, src=real_tomtom)
- DoD : 33/33 concelhos (Moimenta excluded — pas de source, indexable=false, route_km=None)

**Préséance tranchée (leçon durable)** : **`price.desloc` = grille(route_km)`. Toute autre source (concelhos.json legacy, preços-zonas.json) = secondaire. Le bloc P1 lit `concelhos[i].price.desloc` mais ce JSON DOIT avoir été aligné sur la grille avant (gating).

**Règle absolue** : **dans les blocs P1 future, ne JAMAIS réinjecter le `price.desloc` depuis concelhos.json sans avoir vérifié qu'il est aligné sur la grille Filipe**. Toujours : `zone = grille(route_km)` → `my_desloc = grille[zone]`. Le script `fix_zones_tomtom.py` est le contrat — appel avant chaque batch.

**Reproduction (vérification)** :
```bash
python3 /Users/admin/work/Sites/.tooling/preco-deslocacao.py "Chaves"
# Attendu : "55€ deslocação  [74.7km · Z5 · fonte=concelho-direct]"
```

**Coût évité** : facturation erronée (10 € de trop sur Chaves par intervention), image client dégradée (incohérence grille vs facturation), potentiel conflit R12 « preço transparente ».
