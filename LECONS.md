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
