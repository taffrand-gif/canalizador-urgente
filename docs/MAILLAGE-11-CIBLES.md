# Maillage interne blog money — État après PR-A v2 (10/10 cibles gated couvertes)

> **Statut mis à jour** : PR-A v2 (amendement 18/07 soir) couvre **10/10 cibles gated** avec ≥2 liens entrants chacune (et ≥3 pour 9/10). PR-A v2 est commitable. PR-B (round 2 post-merge #175/#176) ne sert plus qu'à ajouter des liens supplémentaires si besoin, pas à initialiser. Annexe maintenue pour mémoire et pour itérations futures (frères↔frères, etc.).

## Cadrage

Mission CEO 2026-07-18 : « les 11 articles blog money (hors sitemap par design tiering)
doivent être découvrables par maillage depuis les piliers et entre articles frères. »

Liste explicite du brief :
1. `desentupir-sanita` (pilier money — `feat/md-top5` PR #176, **DÉJÀ en prod**)
2. `banheira-entupida-desentupir` (PR #175 feat/md-6-10, **DRAFT**)
3. `desentupir-ralo-chuveiro` (PR #175, **DRAFT**)
4. `duche-entupido-limpar` (PR #175, **DRAFT**)
5. `instalar-banheira` (PR #175, **DRAFT**)
6. `tubo-pvc-vs-cobre` (PR #175, **DRAFT**)
7. `canalizacao-entupida-causas-solucoes` (PR #176, **DRAFT**)
8. `canalizacao-entupida-resolver` (PR #176, **DRAFT**)
9. `canalizacao-velha-substituir` (PR #176, **DRAFT**)
10. `quanto-custa-mudar-canalizacao-antiga-2026` (PR #176, **DRAFT**)
11. `ruidos-canalizacao-diagnostico` (PR #176, **DRAFT**)

## Matrice de maillage par cible (post-merge des PRs contenu)

Format : pour chaque cible, liens entrants prévus depuis les sources. Ancres PT-PT
descriptives (jamais fourre-tout footer), URLs extensionless, en accord avec le
routage Vercel `cleanUrls: true`.

### 1. `/blog/desentupir-sanita` — DÉJÀ en prod ✅

Inclus dans PR-A (5 fichiers modifiés, +14 liens, gate 200 14/14).
- Entrants depuis piliers : 4/4 (desentupimento-esgoto, desentupir-canos, entupimento, index).
- Section « Artigos relacionados » dans l'article : 6 liens dont 3 piliers + 3 articles
  urgência prod (sanita-a-transbordar-urgente, esgoto-rebentado-urgente, fuga-agua-urgente-30min).

### 2. `/blog/banheira-entupida-desentupir` (PR #175 DRAFT)

Ancre type : « Artigo dedicado — Banheira Entupida: 5 Métodos Profissionais para Desentupir ».

Sources à patcher après merge #175 (sections Páginas/Artigos relacionadas) :
- `desentupir-canos.html` — section Páginas relacionadas, § « Quando chamar um profissional »
  ou nouveau § dédié : « Para entupimentos específicos na banheira (causas + 5 métodos) ».
- `entupimento.html` — section Páginas relacionadas, § « Tipos de entupimentos mais comuns » /
  « Entupimentos no lavatório e banheira ».
- `blog/desentupir-sanita.html` — section Artigos relacionados, après merge #175 :
  ajouter ligne « Artigo dedicado — Banheira Entupida (5 métodos profissionais) ».
- `blog/desentupir-ralo-chuveiro.html` (post-merge) — section frères chuveiro↔banheira.
- `blog/duche-entupido-limpar.html` (post-merge) — section frères duche↔banheira.

### 3. `/blog/desentupir-ralo-chuveiro` (PR #175 DRAFT)

Ancre : « Artigo dedicado — Desentupir Ralo do Chuveiro (causas, métodos, quando chamar) ».

Sources :
- `desentupir-canos.html` — section Páginas relacionadas.
- `entupimento.html` — section Páginas relacionadas (ralo = symptôme transverse).
- `blog/desentupir-sanita.html` (post-merge dans l'article) — section Artigos relacionados,
  ajouter ligne ralo do chuveiro.
- `blog/banheira-entupida-desentupir.html` (post-merge #175) — section frères ralo↔banheira.

### 4. `/blog/duche-entupido-limpar` (PR #175 DRAFT)

Ancre : « Artigo dedicado — Duche Entupido: Limpar Passo a Passo Sem Danificar ».

Sources :
- `desentupir-canos.html` — section Páginas relacionadas.
- `entupimento.html` — section Páginas relacionadas.
- `blog/desentupir-sanita.html` — section Artigos relacionados, ajouter ligne duche.
- `blog/banheira-entupida-desentupir.html` (post-merge) — section frères duche↔banheira.
- `blog/desentupir-ralo-chuveiro.html` (post-merge) — section frères duche↔ralo.

### 5. `/blog/instalar-banheira` (PR #175 DRAFT)

Ancre : « Artigo dedicado — Instalar Banheira: Guia Completo para Trás-os-Montes ».
**Note R12** : « instalação » peut empiéter hors-scope si elle devient un tutoriel
travaux neufs. Restreindre aux aspects canalisation (préparation, sifão, escoamento,
pressurização). Décision CEO pendiente pour valider la publication #175.

Sources (post-merge #175) :
- `entupimento.html` — section Páginas relacionadas, § « instalação » si pertinent.
- `blog/desentupir-canos.html` (post-merge #176 sur canalizacao) — section Artigos relacionados.
- `blog/duche-entupido-limpar.html` (post-merge) — si l'installation inclut duche/banheira.

### 6. `/blog/tubo-pvc-vs-cobre` (PR #175 DRAFT)

Ancre : « Artigo dedicado — Tubo PVC vs Cobre: Comparação Honesta para Trás-os-Montes ».
**Note R11** : respect strict factuel. Pas de recommandation tranchée, juste données
et conséquences (durabilidade, custo, instalação, pressão, compatibilité eau dure).

Sources (post-merge #175) :
- `index.html` — section « Leituras úteis do blog » (déjà patchée en PR-A), à étendre
  en PR-B avec ce lien.
- `blog/canalizacao-velha-substituir.html` (post-merge #176) — section Artigos relacionados
  (lien naturel matériau ↔ renovação).
- `blog/canalizacao-entupida-causas-solucoes.html` (post-merge #176) — section Artigos
  relacionados (lien matériau ↔ causa).

### 7. `/blog/canalizacao-entupida-causas-solucoes` (PR #176 DRAFT)

Ancre : « Artigo dedicado — Canalização Entupida: Causas e Soluções ».

Sources :
- `desentupimento-esgoto.html` — section Páginas relacionadas, paragraphe 2 « Para
  causas gerais de entupimento de canalização (não só dentro de casa) » + lien.
- `desentupir-canos.html` — section Páginas relacionadas, ajouter 1 ligne.
- `entupimento.html` — section Páginas relacionadas, ajouter 1 ligne.
- `blog/desentupir-sanita.html` — section Artigos relacionados, ajouter 1 ligne.

### 8. `/blog/canalizacao-entupida-resolver` (PR #176 DRAFT)

Ancre : « Artigo dedicado — Canalização Entupida: Como Resolver em Casa e Quando Chamar ».

Sources :
- `desentupimento-esgoto.html` — section Páginas relacionadas.
- `desentupir-canos.html` — section Páginas relacionadas.
- `entupimento.html` — section Páginas relacionadas.
- `blog/desentupir-sanita.html` — section Artigos relacionados.

### 9. `/blog/canalizacao-velha-substituir` (PR #176 DRAFT)

Ancre : « Artigo dedicado — Canalização Velha: Sinais de que Está na Hora de Substituir ».

Sources :
- `entupimento.html` — section Páginas relacionadas (canalização antiga → entupimento recurrente).
- `blog/canalizacao-entupida-causas-solucoes.html` (post-merge) — section Artigos relacionados.
- `blog/quanto-custa-mudar-canalizacao-antiga-2026.html` (post-merge) — section Artigos relacionados.

### 10. `/blog/quanto-custa-mudar-canalizacao-antiga-2026` (PR #176 DRAFT)

Ancre : « Artigo dedicado — Quanto Custa Mudar Canalização Antiga em 2026 ».

Sources (money-intent frère) :
- `entupimento.html` — section Páginas relacionadas (lien coûts/money).
- `desentupir-canos.html` — section Páginas relacionadas.
- `blog/canalizacao-velha-substituir.html` (post-merge) — section Artigos relacionados.
- `blog/canalizacao-entupida-causas-solucoes.html` (post-merge) — section Artigos relacionados.

### 11. `/blog/ruidos-canalizacao-diagnostico` (PR #176 DRAFT)

Ancre : « Artigo dedicado — Ruídos na Canalização: 9 Sons e o que Cada um Significa ».

Sources (symptôme transverse) :
- `entupimento.html` — section Páginas relacionadas (« ruído » = symptôme d'entupimento
  mais aussi de pressão / válvula).
- `blog/canalizacao-velha-substituir.html` (post-merge) — section Artigos relacionados
  (lien bruit ↔ canalisation ancienne).

## Plan d'exécution post-merge #175 + #176

1. **Attendre GO nominatif Philippe** sur PR #175 ET #176 (R7 strict).
2. **Merge main, fetch origin, rebase feat/maillage-blog** depuis main post-merge.
   Les 10/11 cibles deviennent 200.
3. **Re-jouer gate 200** sur tous les ajouts prévus (gate 200 doit passer à 24-30
   OK contre 1 sur 11 avant).
4. **Itérer `patch` sur les 5 fichiers source piliers + appliquer le maillage frère
   sur les 11 articles blog** (chaque article reçoit ≥2 liens entrants selon matrice ci-dessus).
5. **Push branche `feat/maillage-blog` MAJ** + transformer en PR (toujours DRAFT).
6. **Attendre deuxième GO** Philippe (R7).
7. **Squash-merge** + leçon.

## HORS scope (rappels doctrine)

- ❌ Pas d'ajout href vers 11 cibles tant que #175 / #176 ne sont pas mergés
  (Pitfall #5 NON-NEGOTIABLE, 10/11 URLs = 404 en prod).
- ❌ Pas de réécriture des piliers (prix/grille/contenu doctrinal — R12).
- ❌ Pas de lien vers page doorway templatée (Pitfall #6 — leçon #349).
  Les 11 cibles money sont différenciées (pilier money confirmé + variation d'intention),
  pas de risque doorway.
- ❌ Pas de cross-site link injection (chaque PR site a son propre cycle de merge).

## Bilan chiffré attendu post-PR-B

- Fichiers modifiés PR-B : 4 piliers (extension des Páginas relacionadas existantes
  avec 1-3 liens chacune) + 11 articles blog (section Artigos relacionados, 2-4 liens
  chacun) = 15 fichiers.
- Hrefs ajoutés : ~40-50 (estimation, 2-4 par article × 15 fichiers).
- Gate 200 attendu : 100 % OK (toutes cibles merged = 200 en prod).
- Articles money découverts : 11/11 (vs 1/11 après PR-A).
