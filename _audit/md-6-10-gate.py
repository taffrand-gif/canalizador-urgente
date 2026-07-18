#!/usr/bin/env python3
"""Gate reproductible pour les cinq articles de la tranche MD 6–10."""

from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SLUGS = [
    "tubo-pvc-vs-cobre",
    "banheira-entupida-desentupir",
    "desentupir-ralo-chuveiro",
    "duche-entupido-limpar",
    "instalar-banheira",
]
SITE = "https://canalizador-urgente.pt/blog/"


class VisibleText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.skip = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self.skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self.skip:
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


FORBIDDEN = {
    "R145 réponse mediante": r"resposta\s+mediante\s+confirmação\s+por\s+telefone",
    "R145 réponse immédiate": r"resposta\s+(?:imediata|prioritária)",
    "claim certification": r"(?:emitimos|fazemos)\s+certifica",
    "document émis": r"(?:certificado|relatório|ficha)\s+(?:emitido|emitida|formal)",
    "chantier inventé": r"(?:trabalhos|intervenções)\s+(?:realizados|recentes)",
    "ancienneté chiffrée": r"experiência\s+(?:de\s+)?\d+\s+anos",
}


def check(slug: str) -> dict[str, object]:
    path = ROOT / "blog" / f"{slug}.html"
    text = path.read_text(encoding="utf-8")
    parser = VisibleText()
    parser.feed(text)
    words = re.findall(r"[\wÀ-ÿ]+(?:['’][\wÀ-ÿ]+)?", " ".join(parser.parts))
    canonical = re.findall(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', text, re.I
    )
    scripts = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', text, re.I | re.S
    )
    schemas = [json.loads(raw) for raw in scripts]
    types = [schema.get("@type") for schema in schemas]
    missing = [
        marker
        for marker in (
            "65 €/h", "Z1", "15 €", "Z2", "25 €", "Z3", "35 €",
            "Z4", "45 €", "Z5", "55 €", "Z6", "65 €", "+50 %",
            "mediante confirmação por telefone",
            "orçamento por escrito antes de qualquer intervenção, sem surpresas",
            "fala sempre com a mesma pessoa, não um call center",
            "+351 928 484 451",
        )
        if marker not in text
    ]
    forbidden = [name for name, pattern in FORBIDDEN.items() if re.search(pattern, text, re.I)]
    return {
        "slug": slug,
        "visible_words": len(words),
        "canonical_ok": canonical == [f"{SITE}{slug}"],
        "schema_types": types,
        "faq_count": types.count("FAQPage"),
        "missing_markers": missing,
        "forbidden": forbidden,
        "pass": (
            len(words) >= 800
            and canonical == [f"{SITE}{slug}"]
            and types.count("FAQPage") == 1
            and {"BlogPosting", "Service", "FAQPage"}.issubset(set(types))
            and not missing
            and not forbidden
        ),
    }


def main() -> int:
    results = [check(slug) for slug in SLUGS]
    print(json.dumps(results, ensure_ascii=False, indent=2))
    passed = sum(bool(result["pass"]) for result in results)
    print(f"DoD: {passed}/5 articles PASS")
    return 0 if passed == 5 else 1


if __name__ == "__main__":
    sys.exit(main())
