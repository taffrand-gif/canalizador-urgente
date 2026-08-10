#!/usr/bin/env python3
"""R12 Mass Cleanup CU — hubs concelhos/ + distritos/ (39 fichiers)

Cible uniquement les 2 dossiers d'information municipales qui avaient été
ratés par pass1 #91 et pass2 #92. Patterns identiques au script pass2.
"""
import re, sys, json
from pathlib import Path

ROOT = Path("/Users/admin/work/Sites/canalizador-urgente")

# Patterns IDENTIQUES au script pass2 (ne pas inventer)
PATTERNS = [
    (r"Resposta Resposta mediante confirmação por telefone — ligue 928 484 451, garantimos atendimento mediante confirmação por telefone",
     "Diagnóstico por telefone em poucos minutos, orçamento por escrito antes da deslocação"),
    (r"Resposta mediante confirmação por telefone — ligue 928 484 451, garantimos atendimento mediante confirmação por telefone",
     "Diagnóstico por telefone em poucos minutos, orçamento por escrito antes da deslocação"),
    (r"Atendimento mediante confirmação por telefone — ligue 928 484 451, garantimos atendimento mediante confirmação por telefone",
     "Atendimento — ligue 928 484 451, damos orçamento por escrito após auscultação por telefone"),
    (r"Atendimento Atendimento mediante confirmação por telefone — ligue 928 484 451, garantimos atendimento mediante confirmação por telefone",
     "Atendimento — ligue 928 484 451, damos orçamento por escrito após auscultação por telefone"),
    (r"Atendemos 24h/7 dias, mediante confirmação por telefone — ligue 928 484 451, atenção dedicada mediante confirmação por telefone",
     "Atendemos 24h/7d (orçamento por escrito em poucos minutos)"),
    (r"o atendimento é mediante confirmação por telefone — ligue 928 484 451, garantimos atendimento mediante confirmação por telefone",
     "o atendimento começa por orçamento escrito — ligue 928 484 451"),
    (r"Atendemos 24h/7 dias, mediante confirmação por telefone, 7 dias por semana",
     "Atendemos 24h/7d, 7 dias por semana"),
    (r"Atendemos 24h/7 dias, mediante confirmação por telefone",
     "Atendemos 24h/7d"),
    (r"Atendimento mediante confirmação por telefone/7d, 7 dias por semana\. Para emergências, atendemos sempre\.",
     "Atendimento 24h/7d, 7 dias por semana. Para emergências, atendemos sempre."),
    (r"Atendimento mediante confirmação por telefone/7d",
     "Atendimento 24h/7d"),
    (r"Atendimento mediante confirmação por telefone, sem surpresas",
     "Atendimento 24h/7d, sem surpresas"),
    (r"Atendimento mediante confirmação por telefone\. orçamento por escrito",
     "Atendimento. orçamento por escrito"),
    (r"Atendimento mediante confirmação por telefone",
     "Atendimento — ligue 928 484 451"),
    (r"atendimento é mediante confirmação por telefone",
     "atendimento é por telefone"),
    (r"atendimento mediante confirmação por telefone",
     "orçamento por escrito após auscultação por telefone"),
    (r"Resposta Resposta mediante confirmação por telefone",
     "Diagnóstico por telefone em poucos minutos"),
    (r"Resposta mediante confirmação por telefone",
     "Diagnóstico por telefone em poucos minutos"),
    (r"mediante confirmação por telefone\. Em emergências, prioridade absoluta\.",
     "por telefone. Em emergências, prioridade absoluta."),
    (r"Resposta conforme disponibilidade",
     "Deslocação conforme zona Z"),
    (r"© 2024(.*?Norte Reparos)", r"© 2026\1"),
    (r"© 2024", "© 2026"),
    (r"地下室", "cave"),
    (r"Sem custo extra noturno em muitas situações", ""),
    (r"⚠️ Acréscimos noturnos:\*\* 18h-08h = \+50% hora\. Sábado: \+50%\. Domingo/Feriado = 90€/h\.",
     "Majoração noite (20h-8h), domingo et férié : +50%."),
]


def main():
    stats = {"files_scanned": 0, "files_modified": 0, "total_replacements": 0,
             "by_pattern": {}}

    targets = []
    targets += sorted((ROOT / "concelhos").glob("*.html"))
    targets += sorted((ROOT / "distritos").glob("*.html"))
    targets = list(set(targets))
    print(f"Total targets: {len(targets)} (concelhos + distritos)")

    for p in targets:
        stats["files_scanned"] += 1
        try:
            content = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        original = content
        file_replacements = 0
        for pattern, replacement in PATTERNS:
            count = len(re.findall(pattern, content))
            if count > 0:
                content = re.sub(pattern, replacement, content)
                stats["by_pattern"][pattern[:60]] = stats["by_pattern"].get(pattern[:60], 0) + count
                file_replacements += count

        if content != original:
            p.write_text(content, encoding="utf-8")
            stats["files_modified"] += 1
            stats["total_replacements"] += file_replacements

    print(json.dumps(stats, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
