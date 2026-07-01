#!/usr/bin/env python3
"""R12 Blog Safe Cleanup CU — patch UNIQUEMENT les zones safe:
- <title>...</title>
- <meta ... />
- <script type="application/ld+json">...</script>

PAS LE BODY <p>, <li>, <h2>, <a href>
"""
import re, json
from pathlib import Path

ROOT = Path("/Users/admin/work/Sites/canalizador-urgente")
TARGETS = []
TARGETS += list((ROOT / "blog").glob("*.html"))
TARGETS += list((ROOT / "public" / "blog").glob("*.html"))

# Patterns (mêmes que pass2)
PATTERNS = [
    (r"Resposta Resposta mediante confirmação por telefone — ligue 928 484 451, garantimos atendimento mediante confirmação por telefone",
     "Diagnóstico por telefone em poucos minutos, orçamento por escrito antes da deslocação"),
    (r"Resposta mediante confirmação por telefone — ligue 928 484 451, garantimos atendimento mediante confirmação por telefone",
     "Diagnóstico por telefone em poucos minutos, orçamento por escrito antes da deslocação"),
    (r"Atendimento Atendimento mediante confirmação por telefone — ligue 928 484 451, garantimos atendimento mediante confirmação por telefone",
     "Atendimento — ligue 928 484 451, damos orçamento por escrito após auscultação por telefone"),
    (r"Atendimento mediante confirmação por telefone — ligue 928 484 451, garantimos atendimento mediante confirmação por telefone",
     "Atendimento — ligue 928 484 451, damos orçamento por escrito após auscultação por telefone"),
    (r"Atendemos 24h/7 dias, mediante confirmação por telefone — ligue 928 484 451, garantimos atenção mediante confirmação por telefone",
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
    (r"Resposta conforme disponibilidade",
     "Deslocação conforme zona Z"),
    (r"© 2024(.*?Norte Reparos)", r"© 2026\1"),
    (r"© 2024", "© 2026"),
    (r"地下室", "cave"),
    (r"Sem custo extra noturno em muitas situações", ""),
    # FALLBACK GÉNÉRIQUE (doit être en DERNIER pour pas casser les patterns longs)
    (r"mediante confirmação por telefone",
     "orçamento por escrito por telefone"),
]

# Pattern qui matche ce qui est UNIQUE au R12 (pour compter les hits)
R12_DETECT = re.compile(r"(?i)mediante confirmação|Resposta conforme disponibilidade")

def patch_zone(content):
    """Patch les patterns dans la zone safe (meta/title/JSON-LD)."""
    for pat, repl in PATTERNS:
        content = re.sub(pat, repl, content)
    return content


def main():
    stats = {"files_scanned": 0, "files_modified": 0, "total_replacements": 0}
    targets = list(set(TARGETS))
    print(f"Total targets: {len(targets)}")
    for p in sorted(targets):
        stats["files_scanned"] += 1
        content = p.read_text(encoding="utf-8")
        original = content

        # 1. patch <title>...</title>
        content_new = re.sub(r"<title[^>]*>.*?</title>",
                             lambda m: patch_zone(m.group(0)),
                             content, flags=re.DOTALL)
        content = content_new

        # 2. patch <meta ... />
        def meta_repl(m):
            return patch_zone(m.group(0))
        content = re.sub(r"<meta[^>]+>", meta_repl, content)

        # 3. patch JSON-LD scripts
        def jsonld_repl(m):
            return patch_zone(m.group(0))
        content = re.sub(
            r'<script[^>]*type\s*=\s*"application/ld\+json"[^>]*>.*?</script>',
            jsonld_repl, content, flags=re.DOTALL)

        if content != original:
            p.write_text(content, encoding="utf-8")
            stats["files_modified"] += 1
            # Count R12 hits BEFORE - AFTER (only safe zones = approximation)
            # But we want to count what was replaced
            n_before = len(R12_DETECT.findall(original))
            n_after = len(R12_DETECT.findall(content))
            # n_before includes body, n_after also includes body
            # Approximation: replacements = what's gone, body still counted
            # Use a different metric: count R12 patterns that the patcher addresses
            n_replaced = max(0, n_before - n_after)  # at least this many were removed
            stats["total_replacements"] += n_replaced

    print(json.dumps(stats, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

# Patch de patch : ajouter fallback générique (à faire avant)
