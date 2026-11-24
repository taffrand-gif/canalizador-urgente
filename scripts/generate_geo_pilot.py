#!/usr/bin/env python3
"""Prototype GEO CU borné à deux pages money existantes.

La sortie reste volontairement limitée à Mogadouro et Chaves. Les faits locaux
non sourcés ne sont pas générés : la valeur locale vient de l'intention,
du concelho ciblé et de la confirmation opérationnelle par téléphone.
"""
from __future__ import annotations

from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://canalizador-urgente.pt"
PHONE = "+351928484451"
DISPLAY_PHONE = "+351 928 484 451"
PAGES = {
    "mogadouro": {"name": "Mogadouro", "district": "Bragança"},
    "chaves": {"name": "Chaves", "district": "Vila Real"},
}


def tracking_prefix() -> str:
    source = (ROOT / "canalizador-desentupimento-braganca.html").read_text(encoding="utf-8")
    head = source.split("<head>", 1)[-1]
    match = re.search(r"^([\s\S]*?)(?=<meta charset=)", head, re.I)
    if not match:
        raise RuntimeError("tracking prefix not found")
    return match.group(1)


def faq(name: str) -> list[dict[str, str]]:
    return [
        {
            "q": f"Que preço se aplica a um desentupimento urgente em {name}?",
            "a": "Em dias úteis entre as 09:00 e as 18:00: 70 €/hora e 30 € de deslocação. À noite, fins de semana e feriados: 100 €/hora e 50 € de deslocação. Valores TTC, comunicados por escrito antes da intervenção.",
        },
        {
            "q": f"Atendem urgências de canalização em {name} 24h/7d?",
            "a": "Existe disponibilidade telefónica 24h/7d. A disponibilidade e a janela de chegada são confirmadas por telefone conforme a situação operacional e a localidade.",
        },
        {
            "q": f"Que problemas urgentes resolvem em {name}?",
            "a": "Fugas de água, entupimentos de sanita, ralo ou esgoto, roturas e refluxos. O diagnóstico e o âmbito do trabalho são explicados antes de qualquer intervenção adicional.",
        },
        {
            "q": f"Como peço ajuda em {name}?",
            "a": f"Ligue {DISPLAY_PHONE} ou envie WhatsApp. Indique a freguesia ou localidade, o sintoma e os pontos afetados. Confirmamos a disponibilidade, o preço aplicável e a janela de chegada antes da deslocação.",
        },
    ]


def jsonld(name: str, slug: str, district: str) -> str:
    questions = [
        {"@type": "Question", "name": x["q"], "acceptedAnswer": {"@type": "Answer", "text": x["a"]}}
        for x in faq(name)
    ]
    graph = [
        {"@type": "WebSite", "@id": f"{DOMAIN}/#website", "url": f"{DOMAIN}/", "name": "Norte Reparos", "inLanguage": "pt-PT"},
        {"@type": "Organization", "@id": f"{DOMAIN}/#organization", "name": "Norte Reparos", "url": f"{DOMAIN}/", "telephone": DISPLAY_PHONE, "sameAs": ["https://canalizador-norte-reparos.pt", "https://eletricista-norte-reparos.pt", "https://eletricista-urgente.pt"]},
        {"@type": "Plumber", "@id": f"{DOMAIN}/#plumber", "name": "Norte Reparos — Canalização urgente", "url": f"{DOMAIN}/", "telephone": DISPLAY_PHONE, "areaServed": {"@type": "AdministrativeArea", "name": f"Concelho de {name}"}, "knowsLanguage": "pt-PT"},
        {"@type": "Service", "@id": f"{DOMAIN}/canalizador-desentupimento-{slug}#service", "name": f"Desentupimento urgente em {name}", "serviceType": "Canalização urgente", "provider": {"@id": f"{DOMAIN}/#plumber"}, "areaServed": {"@type": "AdministrativeArea", "name": f"Concelho de {name}"}, "availableChannel": {"@type": "ServiceChannel", "servicePhone": {"@type": "ContactPoint", "telephone": DISPLAY_PHONE, "contactType": "customer service", "areaServed": "PT"}}},
        {"@type": "FAQPage", "@id": f"{DOMAIN}/canalizador-desentupimento-{slug}#faq", "mainEntity": questions},
        {"@type": "BreadcrumbList", "@id": f"{DOMAIN}/canalizador-desentupimento-{slug}#breadcrumb", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Início", "item": f"{DOMAIN}/"}, {"@type": "ListItem", "position": 2, "name": f"Canalização urgente em {name}", "item": f"{DOMAIN}/canalizador-desentupimento-{slug}"}]},
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")


def render(slug: str, data: dict[str, str]) -> str:
    name, district = data["name"], data["district"]
    canonical = f"{DOMAIN}/canalizador-desentupimento-{slug}"
    title = f"Desentupimento urgente em {name} 24h/7d | Norte Reparos"
    description = f"Desentupimento urgente em {name}, distrito de {district}: sanita, ralo, esgoto, fuga e rotura. Preço comunicado antes da deslocação. Ligue {DISPLAY_PHONE}."
    faq_html = "\n".join(f"<details><summary>{escape(x['q'])}</summary><p>{escape(x['a'])}</p></details>" for x in faq(name))
    return f'''<!doctype html>
<html lang="pt-PT">
<head>
{tracking_prefix()}<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="pt_PT">
<meta property="og:site_name" content="Norte Reparos">
<script type="application/ld+json">{jsonld(name, slug, district)}</script>
<style>
:root{{font-family:system-ui,-apple-system,Segoe UI,sans-serif;color:#20252b;background:#f5f7f8;line-height:1.6}}
*{{box-sizing:border-box}}body{{margin:0}}header{{background:#0a4d68;color:#fff;padding:1rem}}header nav,main,footer{{max-width:980px;margin:auto}}header nav{{display:flex;gap:1rem;justify-content:space-between;flex-wrap:wrap}}header a,footer a{{color:#fff;font-weight:700}}main{{padding:0 1rem 2rem}}.breadcrumb{{padding:1rem 0;font-size:.9rem}}.hero{{background:#0a4d68;color:#fff;margin:0 -1rem;padding:2.5rem 1rem;text-align:center}}h1{{font-size:clamp(2rem,5vw,3rem);line-height:1.1;margin:.5rem auto 1rem;max-width:22ch}}h2{{color:#0a4d68;line-height:1.2}}.hero h2{{color:#fff;font-size:1.15rem;font-weight:500;max-width:60ch;margin:0 auto 1.5rem}}.cta{{display:inline-block;padding:.8rem 1rem;margin:.25rem;border-radius:8px;text-decoration:none;font-weight:800}}.phone{{background:#fff;color:#0a4d68}}.whatsapp{{background:#25d366;color:#062d16}}.card{{background:#fff;border:1px solid #dfe5e8;border-radius:12px;padding:1.25rem;margin:1rem 0}}.price{{display:grid;grid-template-columns:1fr 1fr;gap:.75rem}}.price div{{background:#eef6f8;padding:1rem;border-radius:8px}}.price strong{{display:block;font-size:1.25rem;color:#0a4d68}}details{{border-top:1px solid #dfe5e8;padding:.8rem 0}}summary{{cursor:pointer;font-weight:700;color:#0a4d68}}.local{{background:#f0f8ff;border-left:4px solid #0a4d68}}footer{{background:#073b51;color:#fff;max-width:none;padding:1.5rem;text-align:center}}@media(max-width:640px){{.price{{grid-template-columns:1fr}}header nav{{flex-direction:column;align-items:center}}}}
</style>
</head>
<body>
<header><nav><a href="/">Norte Reparos — Canalização urgente</a><a data-track="phone_click" href="tel:{PHONE}">{DISPLAY_PHONE}</a><a data-track="whatsapp_click" href="https://wa.me/351928484451">WhatsApp</a></nav></header>
<main>
<nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Início</a> / Canalização urgente em {escape(name)}</nav>
<section class="hero"><p>URGÊNCIA DE CANALIZAÇÃO · DISPONIBILIDADE TELEFÓNICA 24H/7D</p><h1>Desentupimento urgente em {escape(name)}</h1><h2>Fuga, entupimento, rotura ou refluxo? Explique a situação e receba o preço por escrito antes da intervenção.</h2><a class="cta phone" data-track="phone_click" href="tel:{PHONE}">Ligar {DISPLAY_PHONE}</a><a class="cta whatsapp" data-track="whatsapp_click" href="https://wa.me/351928484451?text=Ol%C3%A1%2C%20preciso%20de%20canalizador%20urgente%20em%20{slug}">Enviar WhatsApp</a></section>
<section class="card local"><h2>Canalizador urgente no concelho de {escape(name)}</h2><p>Esta página é dedicada a pedidos urgentes de canalização em {escape(name)}, no distrito de {escape(district)}. A cobertura da localidade e a janela de chegada são confirmadas por telefone conforme a situação operacional.</p><p>Indique a freguesia, o sintoma e se há risco de inundação ou retorno de esgoto.</p></section>
<section class="card"><h2>Preço comunicado antes da deslocação</h2><div class="price"><div><strong>70 €/hora + 30 €</strong>Dias úteis, das 09:00 às 18:00.</div><div><strong>100 €/hora + 50 €</strong>Noite, fins de semana e feriados.</div></div><p>Valores TTC, IVA incluído. Cada hora iniciada é devida. O orçamento escrito é apresentado antes de qualquer intervenção; situações fora do padrão dependem do diagnóstico.</p></section>
<section class="card"><h2>Quando pedir ajuda</h2><ul><li>Sanita, ralo ou esgoto entupido.</li><li>Fuga de água ou cano rebentado.</li><li>Retorno de esgoto ou água a subir.</li><li>Problema que afeta vários pontos da instalação.</li></ul><p>Se for seguro, feche a água e não deite soda cáustica, ácido ou outros químicos agressivos.</p></section>
<section class="card"><h2>Como funciona</h2><ol><li>Ligue ou envie WhatsApp.</li><li>Descreva a localidade, o sintoma e os pontos afetados.</li><li>Confirmamos disponibilidade, âmbito e preço.</li><li>A intervenção só começa depois da sua confirmação e do orçamento escrito.</li></ol></section>
<section class="card"><h2>Perguntas frequentes sobre canalização urgente em {escape(name)}</h2>{faq_html}</section>
<section class="card" style="text-align:center"><h2>Precisa de ajuda agora?</h2><a class="cta phone" data-track="phone_click" href="tel:{PHONE}">Ligar {DISPLAY_PHONE}</a><a class="cta whatsapp" data-track="whatsapp_click" href="https://wa.me/351928484451">WhatsApp</a></section>
</main><footer><p>Norte Reparos — Canalização urgente</p><p><a data-track="phone_click" href="tel:{PHONE}">{DISPLAY_PHONE}</a></p></footer>
<script src="/call-tracking.js" defer></script>
</body></html>
'''


def main() -> None:
    for slug, data in PAGES.items():
        path = ROOT / f"canalizador-desentupimento-{slug}.html"
        path.write_text(render(slug, data), encoding="utf-8")
        print(f"generated {path.name}")


if __name__ == "__main__":
    main()
