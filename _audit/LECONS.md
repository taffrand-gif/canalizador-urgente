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
