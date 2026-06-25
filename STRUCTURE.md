# STRUCTURE — `canalizador-urgente` (canalizador-urgente.pt)

> Site **statique HTML** (satellite SEO du principal `canalizador-norte-reparos.pt`). Pas de build, pas de framework : des fichiers `.html` servis tels quels par Vercel.
> Doc = ce qui EXISTE et est prouvé sur disque (2026-06-22). Pas un idéal.
> ⚠️ **`AGENTS.md` prime sur ce fichier** (9 règles verrouillées Filipe). Lire AGENTS.md avant toute action.
> **PROD** : domaine `canalizador-urgente.pt`. Remote GitHub = source de vérité. Déploiement = **push Git**.

---

## 1. Nature du repo

Pas de `package.json`, pas de bundler. ~1900 pages `.html` autonomes + assets. Vercel sert le statique avec `cleanUrls`. Les pages sont **générées** à partir d'un template à placeholders (§3), pas écrites à la main une par une.

## 2. Arborescence réelle

```
canalizador-urgente/
├── canalizador-<slug>.html ~1900 pages-villes À PLAT à la racine (1 fichier = 1 ville)
├── calculadora-de-preco.html index.html contactos… pages outils/hub
├── blog/ articles .html (~27+ à la racine de blog/)
├── concelhos/ 14 pages hub par concelho
├── distritos/ 6 pages hub par district
├── public/ assets (images, icons)
├── scripts/ génération + maintenance
│ └── archive/ scripts ponctuels passés (lot1-*, logs)
├── vercel.json cleanUrls, redirects, rewrite → .html (§5)
├── sitemap.xml robots.txt llms.txt ai.txt
├── AGENTS.md ⚠️ règles verrouillées (prioritaires)
└── .gitignore .vercel, __pycache__, .DS_Store, *.log
```

**3A — pages-villes à plat, on NE réorganise PAS.** Hiérarchiser en sous-dossiers casserait ~1900 URLs + redirects + sitemap (risque SEO). Le routing est géré par `cleanUrls` (§5), pas par l'arborescence.

## 3. Le template « master R13 » (comment une ville est créée)

Mécanisme = **substitution de placeholders** dans un template HTML, vers `canalizador-<slug>.html`.

🔴 **Le template vit HORS de ce repo** (non versionné avec le site — fragilité connue, voir §6) :
`~/.openclaw/workspace/REVUE_MISSION_18039_2026-06-15/`
- `master-canal-R13.html` — template à placeholders.
- `gabarit-R13-canal.html` — variante/gabarit.
- `canalizador-urgente-braganca.GOLDEN.html` — sortie de référence validée (étalon).

**Placeholders du master** (prouvés) :
`{{CIDADE}}` `{{ZONA}}` `{{SLUG}}` `{{DESLOCACAO}}` `{{PRECO_DESDE}}` `{{PRECO_DESDE_NUM}}` `{{MAILLAGE}}` `{{LOCAL_BUSINESS_TYPE}}`

### Ajouter une ville (procédure)
1. Récupérer le master R13 (chemin ci-dessus).
2. Substituer chaque placeholder (`{{CIDADE}}`, `{{SLUG}}`, `{{ZONA}}`, prix, maillage interne…) pour la nouvelle ville.
3. Écrire le résultat en `canalizador-<slug>.html` à la racine (`slug` = minuscules, sans accent, tirets ; ex. `canalizador-braganca.html`).
4. Comparer la sortie au GOLDEN pour valider la structure.
5. Ajouter l'URL au `sitemap.xml` + maillage interne.
6. `git add` ciblé + commit + push → déploiement auto.

⚠️ Génération de masse = soumise à **R8 (témoins de contrôle)** d'AGENTS.md : compte attendu connu d'avance + réconcilié.

## 4. blog / concelhos / distritos

Mêmes principes statiques : pages `.html` (hub par concelho/district pour le maillage interne, articles dans `blog/`). Pas de génération de framework — fichiers servis directement.

## 5. Routing & déploiement (Vercel statique)

`vercel.json` :
- `cleanUrls: true`, `trailingSlash: false` → URLs sans extension (`/canalizador-braganca` au lieu de `…html`).
- `rewrites`: `{"source":"/(.*)","destination":"/$1.html"}` → mappe l'URL propre vers le fichier `.html` réel.
- `redirects`: 26 entrées (ex. `/es`,`/fr` → 410 ; normalisations `/public/...` → 301). **Ajouter/retirer une page = vérifier l'impact redirects + sitemap.**
- `headers`: cache/sécurité.

**Déploiement** = `git push` sur la branche prod. Jamais d'API/CLI Vercel pour publier (règle R1 d'AGENTS.md). Vercel en ERROR = STOP + rapport, pas d'itération solo sur main.

## 6. Pièges & divergences connus (signalés, NON corrigés — décision Filipe)

- 🔴 **Masters R13 hors repo** : le template générateur n'est pas versionné avec le site. Le site n'est pas reproductible seul. À rapatrier dans le repo (ex. `_templates/`) — décision archi en attente.
- ⚠️ **`canalizador-.html`** existe : slug vide (fichier malformé, artefact de génération). À supprimer après vérif qu'aucune URL ne pointe dessus.
- ⚠️ **Contenu hors cœur de métier** : quelques pages du repo sortent du périmètre canalisation. À examiner/nettoyer (décision Filipe) — non listées ici, non touchées.
- Canonicals : résidu pré-existant de 2 canonicals cross-domain vers des routes inexistantes du principal (déjà flaggé, non touché).

## 7. Hors périmètre

- Site React principal : `canalizador` (`STRUCTURE.md` dédié).
- `microsites`, `fabric` : hors de ce repo.
