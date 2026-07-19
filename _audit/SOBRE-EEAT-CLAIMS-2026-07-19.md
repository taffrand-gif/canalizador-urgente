# Gate E-E-A-T `/sobre` — claims et sources

Date : 2026-07-19
Branche : `feat/sobre-eeat`
Source unique contrôlée : `AGENTS.md` du repo.

## Tableau claim → ligne source

| Claim ajouté à `sobre.html` | Source `AGENTS.md` | Vérification |
|---|---:|---|
| Norte Reparos est l'identité organisationnelle commune, présentée comme une PME professionnelle multi-sites au Portugal | 206-211 | Marque, pays et organisation multi-sites explicitement verrouillés |
| Quatre sites actifs Norte Reparos | 210-211 | Les quatre domaines actifs sont énumérés |
| Téléphone canalisation `+351 928 484 451` | 211 | Même numéro pour les deux sites canalisation |
| Zone servie : Trás-os-Montes | 60, 212 | Région explicitement citée ; aucune adresse de rue ajoutée |
| Main-d'œuvre canalisation : 65 €/h | 109-110 | Grille R12 verrouillée |
| Déplacement Z1-Z6 : 15/25/35/45/55/65 € | 109-111 | Grille R12 verrouillée |
| Majoration nuit, week-end et jour férié : +50 % | 109-112 | Majoration R12 verrouillée |
| Orçamento por escrito avant intervention, sans surprises | 113, 153-154 | Formule R12 obligatoire ; aucune formulation « de conformidade » |
| Contact direct, pas de call center | 114-116 | Formule R12 obligatoire |
| Diagnostic expliqué avant intervention | 117 | Honnêteté et diagnostic transparent |
| Fatura avec NIF et seguro RC | 118 | Traçabilité explicitement autorisée |
| Atendimento 24h/7 dias | 124-125, 165-166 | Disponibilité autorisée sans délai de trajet chiffré |
| Aucune adresse postale ajoutée ; `areaServed` régional seulement | 18, 127, 167 | R5 géo-neutre, contrôlé dans le HTML et le JSON-LD |
| Rédaction PT-PT et pronom organisationnel « nous » | 215, 217-220 | Langue et règle de communication client |
| `sameAs` vers les quatre domaines actifs | 210-211 | Les quatre domaines proviennent de la liste verrouillée |

## Claims proposés mais non écrits faute de source locale

- `Alto Douro` : 0 occurrence dans `AGENTS.md` au moment du gate. La page conserve uniquement `Trás-os-Montes`.
- Histoire datée, ancienneté, date de création : aucune valeur ajoutée.
- Nom de personne, adresse de rue, photo, avis client : aucun ajout.
- Certification, DGEG, certificat, fiche ou document de conformité : aucun ajout.

## Interprétation « mediante confirmação »

`AGENTS.md:125` et `AGENTS.md:166` autorisent `24h/7 dias` mais interdisent la promesse « resposta mediante confirmação por telefone ». La page n'emploie donc pas cette promesse. Elle indique seulement la disponibilité 24h/7 et invite le client à confirmer la disponibilité et la zone, sans délai de réponse ni délai d'arrivée.
