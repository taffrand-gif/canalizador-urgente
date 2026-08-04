#!/usr/bin/env python3
"""Gate ciblé pour la PR #229 — page money `canalizador urgente`."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "blog" / "canalizador-24-horas-guia-completo.html"
SITEMAP = ROOT / "sitemap-blog.xml"
TARGET_URL = "https://canalizador-urgente.pt/blog/canalizador-24-horas-guia-completo"


class HTMLGateParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.h1_count = 0
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag.lower() == "h1":
            self.h1_count += 1
        if tag.lower() == "a" and values.get("href"):
            self.links.append(values["href"] or "")


def extract(pattern: str, text: str, label: str) -> str:
    match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        raise AssertionError(f"{label}: absent")
    return re.sub(r"<[^>]+>", "", match.group(1)).strip()


def assert_count(pattern: str, text: str, expected: int, label: str) -> None:
    count = len(re.findall(pattern, text, flags=re.IGNORECASE | re.DOTALL))
    assert count == expected, f"{label}: attendu {expected}, obtenu {count}"


def main() -> int:
    page = PAGE.read_text(encoding="utf-8")
    parser = HTMLGateParser()
    parser.feed(page)

    title = extract(r"<title>(.*?)</title>", page, "title")
    description = extract(
        r'<meta\s+name="description"\s+content="(.*?)">', page, "meta description"
    )
    h1 = extract(r"<h1\b[^>]*>(.*?)</h1>", page, "h1")
    canonical = extract(
        r'<link\s+rel="canonical"\s+href="(.*?)">', page, "canonical"
    )
    og_url = extract(r'<meta\s+property="og:url"\s+content="(.*?)">', page, "og:url")

    assert 45 <= len(title) <= 60, f"title: {len(title)} caractères"
    assert 130 <= len(description) <= 160, f"description: {len(description)} caractères"
    assert re.search(r"canalizador\s+urgente", title, re.IGNORECASE), "query absente du title"
    assert re.search(r"canalizador\s+urgente", description, re.IGNORECASE), "query absente de la description"
    assert re.search(r"canalizador\s+urgente", h1, re.IGNORECASE), "query absente du h1"
    assert parser.h1_count == 1, f"h1: attendu 1, obtenu {parser.h1_count}"
    assert canonical == TARGET_URL == og_url, "canonical / og:url non alignés"
    assert_count(r'<link\s+rel="canonical"', page, 1, "canonical")

    json_blocks = re.findall(
        r'<script\s+type="application/ld\+json">(.*?)</script>',
        page,
        flags=re.IGNORECASE | re.DOTALL,
    )
    parsed = [json.loads(block) for block in json_blocks]
    types = [item.get("@type") for item in parsed]
    assert types == ["BlogPosting", "Service", "FAQPage"], f"JSON-LD types: {types}"
    faq = parsed[2].get("mainEntity", [])
    assert 5 <= len(faq) <= 9, f"FAQ JSON-LD: {len(faq)} questions"
    assert_count(r'class="faq-item"', page, len(faq), "FAQ visible")

    required_literals = {
        "canalizador urgente": 1,
        "65 €/h": 1,
        "Z1": 1,
        "Z2": 1,
        "Z3": 1,
        "Z4": 1,
        "Z5": 1,
        "Z6": 1,
        "+50 %": 1,
        "preço é confirmado antes de qualquer intervenção, sem surpresas": 1,
        "fala sempre com a mesma pessoa, não um call center": 1,
        "+351 928 484 451": 1,
        'telephone":"+351928484451': 1,
        "tel:+351928484451": 1,
        "wa.me/351928484451": 1,
    }
    folded = page.casefold()
    for literal, minimum in required_literals.items():
        count = folded.count(literal.casefold())
        assert count >= minimum, f"{literal!r}: attendu ≥{minimum}, obtenu {count}"

    forbidden_patterns = {
        "orçamento por escrito": r"orçamento\s+por\s+escrito",
        "document/certification claim": (
            r"(?:emitimos|fazemos)\s+(?:certificação|certificados?)|"
            r"emissão\s+de\s+certificado|instalações\s+certificadas|"
            r"ficha\s+eletrot[eé]cnica|relatório\s+emitido|trabalho\s+profissional"
        ),
        "electric-domain contamination": r"\b(?:DGEG|TRIESP|wallbox|carregador\s+VE)\b",
        "banned response wording": r"resposta\s+(?:prioritária|imediata|mediante confirmação por telefone)",
        "precise-address schema": r"streetAddress|postalCode|addressLocality",
        "review schema": r'"@type"\s*:\s*"(?:Review|AggregateRating)"',
        "solo wording": r"\b(?:sozinho|contacto pessoal|falar comigo|eu sou|eu faço|quem fala comigo)\b",
    }
    for label, pattern in forbidden_patterns.items():
        assert not re.search(pattern, page, flags=re.IGNORECASE), f"{label}: motif interdit"

    visible = re.sub(r"<script\b[^>]*>.*?</script>", " ", page, flags=re.IGNORECASE | re.DOTALL)
    visible = re.sub(r"<style\b[^>]*>.*?</style>", " ", visible, flags=re.IGNORECASE | re.DOTALL)
    visible = re.sub(r"<[^>]+>", " ", visible)
    assert not re.search(
        r"\b(?:em|dentro de|até|cheg(?:amos|ada)|resposta)[^.!?]{0,35}"
        r"\b\d+\s*(?:min(?:uto)?s?|h(?:oras?)?)\b",
        visible,
        flags=re.IGNORECASE,
    ), "délai chiffré détecté"
    assert not re.search(
        r"\b(?:cliente|obra|intervenção)\s+(?:em|de)\s+"
        r"(?:Bragança|Chaves|Mirandela|Macedo(?: de Cavaleiros)?|Vila Real|Lamego)\b",
        visible,
        flags=re.IGNORECASE,
    ), "chantier/localité spécifique potentiellement inventé"

    for path in ("/precos", "/zona-intervencao", "/contactos"):
        assert path in parser.links, f"lien pilier absent: {path}"
    for href in parser.links:
        if not href.startswith("/") or href.startswith("//"):
            continue
        route = urlparse(href).path.strip("/")
        if not route:
            continue
        candidates = [ROOT / f"{route}.html", ROOT / route / "index.html", ROOT / route]
        assert any(candidate.exists() for candidate in candidates), f"lien interne sans cible: {href}"

    tree = ET.parse(SITEMAP)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    entries = []
    for node in tree.findall("sm:url", ns):
        loc = node.findtext("sm:loc", default="", namespaces=ns)
        if loc == TARGET_URL:
            entries.append(
                (
                    node.findtext("sm:lastmod", default="", namespaces=ns),
                    node.findtext("sm:priority", default="", namespaces=ns),
                )
            )
    assert entries == [("2026-08-04", "0.7")], f"entrée sitemap cible: {entries}"

    print("PASS verify_t_ec555aaf")
    print(f"title={len(title)} chars | description={len(description)} chars | h1={parser.h1_count}")
    print(f"jsonld={types} | faq={len(faq)} | internal_links={len(parser.links)}")
    print("forbidden=0 | NAP=928 484 451 | sitemap lastmod=2026-08-04 priority=0.7")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, json.JSONDecodeError, ET.ParseError) as error:
        print(f"FAIL verify_t_ec555aaf: {error}", file=sys.stderr)
        raise SystemExit(1)
