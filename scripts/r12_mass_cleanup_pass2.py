#!/usr/bin/env python3
"""R12 Mass Cleanup CU — pass2 (Doctrine §12 R12 INTERDIT)

3 gisements ciblés :
  1. public/canalizador-urgente-{ville}.html (~78 fichiers)
  2. canalizador-{ville}.html racine, SANS préfixe -urgente-/ ni -24-horas- ni -24h- (~1561 fichiers)
  3. blog/public/blog/meta seulement (contenu body pédagogique préservé)
  4. autres statiques (sobre, termos, top-10-*, etc.)
"""
import re, sys, os, json, shutil
from pathlib import Path

ROOT = Path("/Users/admin/work/Sites/canalizador-urgente")

# Patterns longs AVANT les courts (important pour éviter double-substitution)
PATTERNS = [
    # Bloc A : variantes longues hypertrophiées
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

    # Bloc B : motifs courts dérivés
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

    # Bloc C : cas spéciaux
    (r"© 2024(.*?Norte Reparos)", r"© 2026\1"),
    (r"© 2024", "© 2026"),
    (r"地下室", "cave"),
    (r"Sem custo extra noturno em muitas situações", ""),

    # Bloc D : emoji/fa fancy R12
    (r"⚠️ Acréscimos noturnos:\*\* 18h-08h = \+50% hora\. Sábado: \+50%\. Domingo/Feriado = 90€/h\.",
     "Majoração noite (20h-8h), domingo et férié : +50%."),
]


def is_canalizador_root_target(p: Path) -> bool:
    """Match canalizador-<ville>.html racine, excluding urgent/h24/etc"""
    name = p.name
    if not name.startswith("canalizador-"):
        return False
    if not name.endswith(".html"):
        return False
    # Exclure les préfixes déjà traités par pass1 ou qui sont des pages de service templates
    skip_prefixes = (
        "canalizador-urgente-",  # PR #91
        "canalizador-24-horas-",  # generator
        "canalizador-24h-",  # generator
        "canalizador-distrito-",
        "canalizador-ao-domingo-",
        "canalizador-urgente-distrito-",
        # NOTE: NE PAS exclure canalizador-fuga-, -desentupimento-, -fossa-, -esquentador-
        # car ces pages service dédié ont aussi R12
    )
    for sp in skip_prefixes:
        if name.startswith(sp):
            return False
    return True


def main():
    stats = {"files_scanned": 0, "files_modified": 0, "total_replacements": 0,
             "by_pattern": {}}
    targets = []

    # 1. public/canalizador-urgente-*.html
    targets += list((ROOT / "public").glob("canalizador-urgente-*.html"))
    # 2. public/blog/*.html (meta seulement pour éducatif)
    # On traite mais avec flag "skip body" -- simple version: ne pas patcher blog
    # 3. canalizador-{ville}.html racine
    for p in ROOT.glob("canalizador-*.html"):
        if is_canalizador_root_target(p):
            targets.append(p)
    # 4. autres statiques propres (sobre, termos, top-10-*, etc.)
    for static_name in ("sobre.html", "termos-condicoes.html",
                       "zonas-deslocacao.html", "zona-intervencao.html",
                       "calculadora-de-preco.html",
                       "zonas-deslocacao.html"):
        p = ROOT / static_name
        if p.exists():
            targets.append(p)
    for p in ROOT.glob("top-10-*.html"):
        targets.append(p)
    for p in ROOT.glob("sinais-*.html"):
        targets.append(p)
    for p in ROOT.glob("recursos-*.html"):
        targets.append(p)

    targets = list(set(targets))
    print(f"=== TARGETS ===")
    print(f"Total targets: {len(targets)}")

    for p in sorted(targets):
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
