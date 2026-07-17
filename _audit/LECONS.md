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


## Leçon #411 (16/07 2026) — `public/` n'est PAS la racine servie par Vercel sur CU/EU

**Contexte** : Wave-2 refonte V2 data-driven. Vérification prod avant merge : `curl https://canalizador-urgente.pt/sitemap.xml` retourne **432 URLs**, alors que mon `public/sitemap.xml` (auto-réparation Wave-1, 101 core + 792 avant ratiboisé) n'est PAS servi prioritairement par Vercel.

**Pourquoi** : sur **CU et EU** (sites statiques HTML sans React Vite), Vercel sert la **racine du repo directement**. Le `vercel.json` a un catchall `/(.*)` → `/$1.html` qui ne s'applique qu'aux routes sans extension — pas aux `.xml` ou `.txt`.

Sur **CNR et ENR** (Vite React), `dist/public/` est servi (généré par `vite build`). Les pages racines sont aussi servies mais l'architecture est différente.

**Erreur vécue** : Wave-1 auto-réparation, j'ai réécrit `public/sitemap.xml` avec 101 URLs core + supprimé `sitemap-plain.xml` + `sitemap-priority.xml`. Commité sur `feat/p0-...`, draft PR, **pas de merge**. Donc :
1. Prod voit toujours le `sitemap.xml` à la racine (généré par `scripts/gen_sitemap.py`, 432 URLs)
2. `public/sitemap.xml` modifié existe mais n'est pas servi prioritairement
3. `public/robots.txt` modifié n'est pas non plus servi — le prod a un robots.txt différent (mentionne « Sitemap: /sitemap-plain.xml » aussi)
4. **Aucun des changements Wave-1 atteint la prod sans merge + deploy**

**Leçon stratégie** :
- **Vérifier AVANT chaque modif sitemap** : `curl -sI https://<domaine>/sitemap.xml | head -1` + `ls -la sitemap*.xml public/sitemap*.xml`
- **Source-of-truth sitemap CU/EU = `scripts/gen_sitemap.py`** (génère `sitemap.xml` à la racine)
- **Pour modifier un sitemap CU/EU**, modifier `scripts/gen_sitemap.py` (pas `public/sitemap.xml`)
- **Robots.txt doit vivre à la racine** (sinon non servi par Vercel)

**Conséquence Wave-2** : la présente refonte V2 est correctement commitée sur `feat/p1-...`, **non mergée** (R3 STOP), donc n'atteint pas la prod. Quand Philippe validera le merge, les changements hub seront bien servis (les `concelhos/*.html` sont à la racine).

**Action recommandée** : mission séparée pour aligner le sitemap core avec `scripts/gen_sitemap.py` CU/EU, post-merge Wave-2.

**Reproduction systématique** :
```bash
# 1. Quel sitemap sert Vercel ?
curl -sI https://canalizador-urgente.pt/sitemap.xml | head -1
# 2. Quel fichier correspond (racine = source-of-truth) ?
ls -la sitemap*.xml public/sitemap*.xml 2>/dev/null
# 3. Robots.txt pointe quoi ?
curl -s https://canalizador-urgente.pt/robots.txt | grep -i "sitemap:"
# 4. robots.txt est-il à la racine (servi) ou public (non-servi) ?
ls -la robots.txt public/robots.txt 2>/dev/null
```

---

## Leçon #411b (16/07 2026) — `apply_section()` double-anchor bug

**Contexte** : script `p1_hub_render_v2.py` (Wave-2 refonte V2). Pendant les tests sur Chaves, l'application de l'infobox faisait disparaître le paragraphe intro `A 75 km de Macedo de Cavaleiros...`.

**Cause** : `apply_section(html, replacement, anchor_open_re, anchor_close_re)` doublait `</div>` quand le pattern open_re incluait déjà `.*?</div>` :
```python
pat = re.compile(anchor_open_re + r'.*?' + anchor_close_re, flags=re.S)
# Si anchor_open_re finit par r'</div>' et anchor_close_re = r'</div>',
# résultat = pattern = anchor_open_re + r'.*?</div>' — capture trop loin.
```
Dans mon test initial, le pattern infobox était : `<div class="info-box">...Zona tarifária:.*?</p>\s*</div>` avec `anchor_close_re=r'</div>'`. La concaténation ajoutait `.*?</div>` APRÈS, capturant jusqu'au `</div>` suivant (le paragraphe CTA ou la fin de page). Résultat : le paragraphe « A 75 km » était englouti.

**Fix** : vérifier si `anchor_close_re in anchor_open_re` avant de l'ajouter :
```python
if anchor_close_re is None:
    pat_re = anchor_open_re
elif anchor_close_re in anchor_open_re:
    pat_re = anchor_open_re  # déjà inclus, ne pas doubler
else:
    pat_re = anchor_open_re + r'.*?' + anchor_close_re
```

**Coût évité** : 30 min de debug regex + risque de casser les pages hub sur un merge.

---

## Leçon #412 (16/07 2026) — Pilier national vs gabarit Variante C : 2 designs distincts

**Contexte** : Mission P2 Phase 1 (CU), 2 pages pilier service-racine (`desentupir-canos.html` + `entupimento.html`). La SPEC §6-8 ne définit Variante C QUE pour `service_kw × concelho` — pas pour un pilier national sans ancrage communal.

**Question initiale** : peut-on appliquer Variante C telle quelle à un pilier sans concelho unique ? Non — Variante C attend `{{concelho_name}}`, `{{district}}`, `{{route_km}}`, `{{price_block}}` : 4 champs sur 6 n'ont pas de source unique. Adapter ou créer un gabarit national distinct ?

**Décision** : **Variante C adaptée, pas recopiée**. Le pilier national n'est PAS un hub-concelho :
- Pas de `{{concelho_name}}` unique → remplacé par liste **33 concelhos indexables** organisés par zone tarifaire Z1–Z6 (vérifiés par `git ls-files`)
- Bloc Transparence tarifaire **HAUT** (Doctrine §12) identique aux hubs : 65 €/h + Z1–Z6 + +50% nuit/WE/feriado
- Section "Onde atuamos" avec maillage vers les 33 hubs réels (pas de constellation villageoise, R0 self-ref hub)
- Symptômes + causes + méthode + équipement RÉEL listés (Ridgid K9-102 + caméra 30 m + molas espirales) — équipement = R12 §1 validé, pas inventé
- FAQ 5 questions answer-first, dont "Quanto custa?" et "Posso fazer sozinho?" (confiance client, R12 §1)
- Pas d'adresse privée, NAP public seul (`+351 928 484 451`), centreïde Trás-os-Montes dans JSON-LD uniquement (R5 géo-neutre)

**Mesures Jaccard (gate spec §10)** :
- `Jaccard(pilier↔hub)` ≈ **0.20** (cible hub↔hub pairwise median ≤0.35 — OK, piliers plus longs et plus didactiques que hubs urgence)
- `Jaccard(pilier↔pilier)` ≈ **0.67** — attendu : 2 piliers nationaux partagent le même gabarit R12 + équipement + FAQ R12 + maillage 33 concelhos. La différenciation vient de l'**intent** (action vs symptôme), pas du payload factuel.

**Différenciation intent vs contenu** :
- `desentupir-canos.html` (intent action "fazer"): focus sur les **types de cano** (cozinha, sanita, lavatório, ralo, caixa inspeção) + méthode + équipement + prévention
- `entupimento.html` (intent symptôme "problema"): focus sur les **signes** (esvaziamento lento, borbulhar, refluxo, mau cheiro) + **causas habituais** + **distinção fuga vs entupimento** + lien sortant vers `/como-detetar-fuga-agua.html` (renforcie le silo fuite à côté)

**Méthode de validation avant commit** :
1. Liste des 33 fichiers cibles générée par script : `for x in concelhos.json → if indexable → fname = canalizador-urgente-{slug}.html; assert fname in git_ls_files`
2. Grille prix figée : checker `65 €/h`, `15 €`, `25 €`, `35 €`, `45 €`, `55 €`, `65 €`, `+50%` tous présents (8 ancres)
3. Équipement réel : checker `Ridgid K9-102`, `câmara de inspeção 30 m`, `molas espirais` tous présents
4. Claim interdits : grep `mesma pessoa|em X minutos|resposta imediata|mediante confirmação|ferro galvanizado|atendimento imediato|garantimos.*min|emitimos.*certificado` → 0 sur les 2 pages
5. Canonical self : `https://canalizador-urgente.pt/{slug-pilier}` exactement
6. Compteur mots utiles (≥3 char, hors stopwords PT) : cible **800-1500** → 805 et 1044 ✓

**Cherry-pick depuis branche sœur** : `data/concelhos.json` corrigé (grille Filipe route_km TOMTOM alignée) est sur la branche `fix/data-zones-tomtom` (commit `0e1baf711`). Cherry-pick ciblé `git checkout 0e1baf711 -- data/concelhos.json` pour importer UNIQUEMENT le JSON, sans les `scripts/fix_zones_tomtom.py` ni les `concelhos/*.html` (qui sont sur une autre mission).

**Coût évité** :
- Refonte Variante C stricto sensu → impossible (pas de concelho unique)
- Création d'un gabarit "D" national à partir de zéro → inutile, Variante C fournit 80% de la structure
- Régression préséance zones (16 discordances historiquement non tranchées) → tranchée par merge `fix/data-zones-tomtom` dans la branche `feat/p1-hubs-canalizador` mais PAS encore dans `origin/main` → cherry-pick ciblé
- Prix BLOQUÉ hérité de la mission précédente → levé par le cherry-pick, le JSON aligné Filipe permet l'affichage prix
- Jaccard 0.67 entre piliers → ACCEPTÉ car c'est le coût d'avoir un gabarit R12 réutilisable (Doctrine §13 "gabarit réutilisable — verrouillée")

**Reproduction systématique** :
```bash
# 1. Lister hubs réels indexables depuis concelhos.json
python3 -c "import json; c=json.load(open('data/concelhos.json')); \
  import subprocess; fs=set(subprocess.run(['git','ls-files'],capture_output=True,text=True).stdout.split()); \
  print([(x['zone'],x['name'],f'canalizador-urgente-{x[chr(34)+chr(115)+chr(108)+chr(117)+chr(103)+chr(34)].strip()}.html') for x in c if x['indexable'] and f'canalizador-urgente-{x['slug']}.html' in fs])"

# 2. Cherry-pick ciblé concelhos.json corrigé depuis branche sœur
git checkout fix/data-zones-tomtom -- data/concelhos.json  # si branche dispo
# OU commit direct :
git checkout 0e1baf711 -- data/concelhos.json

# 3. Gate qualité avant commit
python3 -c "..."
```

---
