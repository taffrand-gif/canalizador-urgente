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
