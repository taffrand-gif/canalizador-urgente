#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""enrich_cu_desentup.py — diffêrencier 30 pages /canalizador-desentupimento-{slug}.html du site CU.

Cible: casser le signal CRAWLED_NOT_INDEXED + cannibalisation "templatées identiques"
sur les pages cibles (30 villes cœur). Pas toucher au HTML existant : on INJECTE
des briques GEO uniques + on MODIFIE lead/JSON-LD/zone-badge pour casser le duplicate.

Doctrine (Filipe 2026-07-15):
  - intent URGENCE (desentupir canos agora, entupimento 24h)
  - data locale UNIQUE/ville (zone+grille prix+temps réponse depuis PRICING.md + precos-zonas.json + TomTom real)
  - briques GEO: answer-first (H2=question kw, lead 40-60 mots),
    FAQPage, HowTo, Speakable, LocalBusiness @id unique, tables first-party
  - 3+ liens internes / page
  - transp box interpolée (PRICING canonique, pas de regex literal Z[1-6]=\\d+)
  - R12 voix "equipa" (jamais "mesma pessoa")
  - R145 zero délai chiffré ("mediante confirmação")
"""

from __future__ import annotations
import json
import re
import sys
from pathlib import Path
import argparse
from collections import OrderedDict

ROOT = Path(__file__).resolve().parent.parent

# Source 1 (TomTom real) — chemin vers l'audit unifié
TOMTOM_SOURCE = Path.home() / "work/Sites/_audit/zonas-distances-concelhos.json"

# Source 2 (PRICING canonique CU) — mapping localité -> zone depuis precos-zonas.json
PRECOS_CU = ROOT / "precos-zonas.json"

# Grille officielle verrouillée (doctrine tarifs PRICING.md)
GRILLE_PRECOS = OrderedDict([(1, 15), (2, 25), (3, 35), (4, 45), (5, 55), (6, 65)])

TARIF_HORA = 65
MAJORACAO = "+50% noite (20h-8h) / domingo / feriado"
TELEFONE_PUBLIC = "928 484 451"
TELEFONE_E164 = "+351****4451"

# Fallback centroïde district pour lat/lon si non trouvé
DISTRICT_COORDS = {
    "Bragança": (41.806, -6.768),
    "Vila Real": (41.296, -7.746),
    "Viseu": (40.661, -7.911),
    "Guarda": (40.537, -7.271),
}


def km_to_zone(km: float) -> int:
    """Déduction zone depuis km (fallback si precos-zonas.json absent)."""
    if km <= 15: return 1
    if km <= 30: return 2
    if km <= 50: return 3
    if km <= 75: return 4
    if km <= 100: return 5
    return 6


def slugify(name: str) -> str:
    """Reproduit la convention observée dans canalizador-desentupimento-{slug}.html."""
    s = name.strip()
    repl = {
        "ã": "a", "á": "a", "â": "a", "à": "a",
        "ê": "e", "é": "e",
        "í": "i",
        "ô": "o", "ó": "o", "õ": "o", "ò": "o",
        "ú": "u", "ü": "u",
        "ç": "c",
        "'": "-", "’": "-",
        "(": "", ")": "",
    }
    for k, v in repl.items():
        s = s.replace(k, v)
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s


def load_sources():
    """Charge les 2 sources en mémoire et merge en dict {slug: info}.

    Stratégie: 1) TomTom pour km/min/lat (33 concelhos); 2) precos-zonas.json pour
    zone+grille (toutes localités = mapping localité→zone, ~960 entrées).
    Pour les concelhos absents du TomTom mais présents dans precos-zonas.json (cas
    de Tarouca, etc.), on prend precos-zonas.json + centroïde district pour km/min.
    """
    tomtom = json.load(open(TOMTOM_SOURCE))["concelhos"]
    precos = json.load(open(PRECOS_CU))
    merged = {}

    # Étape 1 — depuis TomTom
    for name, v in tomtom.items():
        slug = v["slug"]
        zone_raw = precos.get(name)
        if isinstance(zone_raw, int):
            zone = zone_raw
        else:
            zone = km_to_zone(v["km"])
        desloc = GRILLE_PRECOS[zone]
        merged[slug] = {
            "name": name,
            "slug": slug,
            "district": v.get("distrito", "Trás-os-Montes"),
            "km": v["km"],
            "min": v["temps_min"],
            "zone": zone,
            "desloc": desloc,
        }

    # Étape 2 — fallback: localités de precos-zonas.json qui ne sont PAS dans TomTom
    # mais qui sont aussi noms de concelhos (heuristic: pas de paroisse ending)
    for locality, zone_raw in precos.items():
        if not isinstance(zone_raw, int):
            continue
        slug_cand = slugify(locality)
        if slug_cand in merged:
            continue
        # Heuristic: nom de concelho = sans préfixe comme "Santa" - mais ici on accepte tout.
        # On l'enregistre comme concelhos potentiel. (lat/lon = centroïde district Viseu
        # par défaut — c'est l'hypothèse la plus probable pour Tarouca.)
        merged[slug_cand] = {
            "name": locality,
            "slug": slug_cand,
            "district": "Viseu",  # La plupart des non-TomTom sont Viseu (Tarouca, Lamego, etc.)
            "km": 0,  # inconnu sans TomTom
            "min": 0,
            "zone": zone_raw,
            "desloc": GRILLE_PRECOS[zone_raw],
        }
    return merged


def intro_unique(c: dict) -> str:
    """Lead answer-first (40-60 mots) — GEO best practice."""
    name = c["name"]
    zone = c["zone"]
    desloc = c["desloc"]
    km = c["km"]
    minutos = c["min"]
    if km == 0:
        dist_str = "imediatamente (base operacional em Macedo de Cavaleiros, resposta 24h mais rápida da região)"
    else:
        dist_str = f"em {km:.0f} km (~{minutos} min de viagem desde a base em Macedo de Cavaleiros)"
    return (
        f"Sim, atendemos desentupimento urgente em {name} 24h/7d. "
        f"Desentupir canos, entupimento de sanita, ralo ou esgoto com refluxo: "
        f"chegamos {dist_str}, zona tarifária Z{zone} com deslocação "
        f"de {desloc}€ já incluída no orçamento. "
        f"Diagnóstico com Ridgid K9-102 + câmara 30 m antes de reparar. "
        f"Orçamento por escrito antes de tocar na instalação, sem surpresas — "
        f"majorações {MAJORACAO} comunicadas ao telefone."
    )


def answer_first_h2(c: dict) -> str:
    """Question keyword en H2 (answer-first) — intent desentupir 24h."""
    name = c["name"]
    return f"Quanto custa um desentupimento urgente em {name} e como pedir ajuda 24h?"


def faq_entries(c: dict) -> list[dict]:
    """5 FAQ dur — intent urgência dinheiro, cite la vraie grille (R12 verrouillée)."""
    name = c["name"]
    zone = c["zone"]
    desloc = c["desloc"]
    km = c["km"]
    minutos = c["min"]
    return [
        {
            "q": f"Quanto tempo demora a chegar a {name}?",
            "a": (
                f"Em condições normais, a vinda desde Macedo de Cavaleiros é de "
                f"~{minutos} minutos ({km:.0f} km). Em horário noturno, feriado ou "
                f"condições atmosféricas adversas, este tempo pode aumentar. "
                f"Confirmamos a janela de chegada ao telefone antes da deslocação."
            ),
        },
        {
            "q": f"Quanto custa a deslocação de desentupimento a {name}?",
            "a": (
                f"Zona tarifária Z{zone}: deslocação {desloc}€ já incluída no orçamento "
                f"por escrito. {TARIF_HORA}€/hora de mão de obra. "
                f"Majoração noite/domingo/feriado: +50% (sempre anunciada antes)."
            ),
        },
        {
            "q": f"Atendem entupimentos urgentes em {name} 24h?",
            "a": (
                f"Sim — desentupimento de sanita, ralo, esgoto, fossa ou coluna: "
                f"atendemos 24 horas, 7 dias por semana, incluindo fins de semana e feriados. "
                f"Ligue +351 928 484 451 — atendimento mediante confirmação por chamada."
            ),
        },
        {
            "q": f"Fazem orçamento por escrito em {name} antes de começar?",
            "a": (
                f"Sim — orçamento por escrito sem surpresas, com discriminação de "
                f"deslocação Z{zone}, mão de obra ({TARIF_HORA}€/h) e material. "
                f"Só arrancamos depois da sua confirmação oral ou escrita."
            ),
        },
        {
            "q": f"Emitem fatura com NIF para {name}?",
            "a": (
                f"Sim. Fatura com NIF, discriminada por deslocação Z{zone} ({desloc}€), "
                f"hora de trabalho ({TARIF_HORA}€/h) e material. Pagamento MB Way, "
                f"cartão ou numerário. Garantia 2 anos sobre mão de obra e peças."
            ),
        },
    ]


def service_items(c: dict) -> list[str]:
    """Items de services différenciés — urgence plomberie."""
    name = c["name"]
    return [
        f"Desentupimento de sanita em {name} — diagnóstico com câmara 30 m, máquina Ridgid K9-102 sem partir louça",
        f"Desentupimento de ralo e escoamento em {name} — cabelo, gordura ou sabão acumulado, limpeza completa",
        f"Desentupimento de esgoto e coluna em {name} — refluxo, retorno de água suja, hidrojato profissional",
        f"Desentupimento de fossa sética em {name} — limpeza, desentupimento e verificação de nível",
        f"Desentupimento de banheira/polibã em {name} — acumulação de cabelos e sabão, restabelecimento do escoamento",
        f"Avaria urgente em {name} (noite, fim de semana, feriado) — atendimento 24h/7d com majoração transparente",
    ]


def howto_schema(c: dict) -> dict:
    """HowTo schema — protocole entupimento urgent (intent urgência)."""
    name = c["name"]
    return {
        "@type": "HowTo",
        "name": f"Como agir num entupimento urgente em {name}",
        "description": (
            "Procedimento de emergência imediata, antes da chegada do canalizador, "
            "para minimizar danos e acelerar o diagnóstico do entupimento."
        ),
        "totalTime": "PT5M",
        "step": [
            {"@type": "HowToStep", "position": 1, "name": "Não deitar químicos agressivos",
             "text": "Não reforçar com lixívia pura, ácido ou soda cáustica — corroem juntas e danificam canos antigos. Em ferro galvanizado antigo, podem partir a tubagem."},
            {"@type": "HowToStep", "position": 2, "name": "Fechar a válvula geral da água",
             "text": "Se há refluxo, vire a válvula do contador no sentido horário. Minimize o uso de água até à chegada do técnico."},
            {"@type": "HowToStep", "position": 3, "name": "Colocar baldes e toalhas",
             "text": "Sob o ralo ou junto à sanita. Proteja pavimentos em madeira e alcatifa da água que possa sair durante a contenção."},
            {"@type": "HowToStep", "position": 4, "name": "Ligar para a Norte Reparos",
             "text": f"Ligue +351 928 484 451. Indicamos a hora prevista de chegada em {name} e passamos orçamento por escrito."},
            {"@type": "HowToStep", "position": 5, "name": "Aguardar o canalizador em segurança",
             "text": "Mantenha a válvula fechada até à chegada. Não force a bomba de borracha se sentir resistência forte — pode compactar o bloqueio."},
        ],
    }


def faq_schema(c: dict) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q["q"],
                "acceptedAnswer": {"@type": "Answer", "text": q["a"]},
                "speakable": True,
            }
            for q in faq_entries(c)
        ],
    }


def local_business_schema(c: dict) -> dict:
    """LocalBusiness @id unique par concelhos — verrouillage R5 (géo-neutre centroïde district)."""
    name = c["name"]
    district = c.get("district", "Trás-os-Montes")
    # Use centroïde district (géo-neutre, jamais adresse précise — R5)
    lat, lon = DISTRICT_COORDS.get(district, (41.5, -6.9))
    zone = c["zone"]
    desloc = c["desloc"]
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": f"https://canalizador-urgente.pt/#localbusiness-{c['slug']}",
        "name": f"Norte Reparos — Desentupimento Urgente {name}",
        "alternateName": f"Desentupimento Urgente {name} 24h",
        "telephone": "+351 928 484 451",
        "priceRange": "€€",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": name,
            "addressRegion": district,
            "addressCountry": "PT",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lon},
        "areaServed": {"@type": "AdministrativeArea", "name": f"Concelho de {name}"},
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00",
            "closes": "23:59",
        },
        "serviceArea": {
            "@type": "GeoCircle",
            "geoMidpoint": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lon},
            "geoRadius": "80000",
        },
        "makesOffer": [
            {"@type": "Offer", "name": f"Desentupimento urgente 24h em {name}",
             "priceCurrency": "EUR", "price": str(desloc)},
        ],
        "sameAs": [
            "https://canalizador-norte-reparos.pt",
            "https://eletricista-norte-reparos.pt",
            "https://eletricista-urgente.pt",
        ],
    }


def service_schema(c: dict) -> dict:
    name = c["name"]
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "@id": f"https://canalizador-urgente.pt/canalizador-desentupimento-{c['slug']}#service",
        "name": f"Desentupimento Urgente em {name}",
        "serviceType": "Desentupimento Urgente 24h — canos, sanita, ralo, esgoto, fossa",
        "provider": {"@id": "https://canalizador-urgente.pt/#organization"},
        "areaServed": {"@type": "AdministrativeArea", "name": f"Concelho de {name}"},
        "availableChannel": {
            "@type": "ServiceChannel",
            "serviceUrl": f"https://canalizador-urgente.pt/canalizador-desentupimento-{c['slug']}",
            "servicePhone": {
                "@type": "ContactPoint",
                "telephone": "+351 928 484 451",
                "contactType": "customer service",
                "areaServed": "PT",
                "availableLanguage": "Portuguese",
            },
        },
    }


def speakable_schema(c: dict) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": f"Desentupimento Urgente {c['name']} 24h — Norte Reparos",
        "url": f"https://canalizador-urgente.pt/canalizador-desentupimento-{c['slug']}",
        "speakable": {
            "@type": "SpeakableSpecification",
            "xpath": [
                "/html/body/main/h1",
                "/html/body/main/p[1]",
                "/html/body/main/section[@class='faq']/h2",
            ],
        },
        "inLanguage": "pt-PT",
    }


def website_org_graph() -> list[dict]:
    """WebSite + Organization — partagé (référencé par @id depuis LocalBusiness)."""
    return [
        {
            "@type": "WebSite",
            "@id": "https://canalizador-urgente.pt/#website",
            "url": "https://canalizador-urgente.pt/",
            "name": "Norte Reparos",
        },
        {
            "@type": "Organization",
            "@id": "https://canalizador-urgente.pt/#organization",
            "name": "Norte Reparos",
            "url": "https://canalizador-urgente.pt/",
            "logo": {"@type": "ImageObject", "url": "https://canalizador-urgente.pt/og-image.png", "width": 1200, "height": 630},
            "contactPoint": {
                "@type": "ContactPoint",
                "telephone": "+351 928 484 451",
                "contactType": "customer service",
                "areaServed": "PT",
                "availableLanguage": "Portuguese",
            },
            "address": {"@type": "PostalAddress", "addressRegion": "Trás-os-Montes", "addressCountry": "PT"},
            "sameAs": [
                "https://canalizador-norte-reparos.pt",
                "https://eletricista-norte-reparos.pt",
                "https://eletricista-urgente.pt",
            ],
        },
    ]


def briques_geo(c: dict, neighbors: list[str]) -> str:
    """Renvoie le bloc HTML à injecter en bas de page: H2 question + zoneBadge + FAQ dur + Speakable + grids services."""
    name = c["name"]
    zone = c["zone"]
    desloc = c["desloc"]
    km = c["km"]
    minutos = c["min"]
    district = c["district"]
    intro = intro_unique(c)
    h2q = answer_first_h2(c)
    faq = faq_entries(c)
    services = service_items(c)

    # km_str — chaîne lisible pour la cellule tableau (cas km=0 = sans TomTom)
    if km > 0:
        km_str = f"{km:.0f} km (~{minutos} min)"
    else:
        km_str = "conforme TomTom (sob confirmação)"

    # next_zone, next_dist, next_preco — pour la 3ème ligne du tableau (zone adjacente)
    next_zone = zone + 1 if zone < 6 else 6
    if zone < 6:
        next_dist = f"{int((zone)*15+5)}-{int((zone+1)*15)} km"
    else:
        next_dist = "100+ km"
    next_preco = GRILLE_PRECOS.get(next_zone, 65)

    # Liens internes (≥4)
    district_slug = district.lower().replace(" ", "-")
    district_slug = re.sub(r"[^a-z0-9-]", "", district_slug)
    internal_links = []
    # sister page canalizador
    internal_links.append((f"https://canalizador-urgente.pt/canalizador-{c['slug']}", f"💧 Página dedicada Canalizador {name}"))
    # distritos hub
    internal_links.append((f"https://canalizador-urgente.pt/distritos/{district_slug}.html", f"📍 Distrito de {district}"))
    # neighbors (max 2)
    for ns in neighbors[:2]:
        nm_lookup = next((x["name"] for x in all_concelhos_lookup if x["slug"] == ns), ns.replace("-", " ").title())
        internal_links.append((f"https://canalizador-urgente.pt/canalizador-desentupimento-{ns}", f"➡️ Concelho vizinho: Desentupimento {nm_lookup}"))
    # blog
    internal_links.append((f"https://canalizador-urgente.pt/blog/entupimento-grave-urgencia.html", f"📖 Entupimento grave: o que fazer"))

    faq_html = "\n".join(
        f'<div class="faq"><strong>{q["q"]}</strong><p>{q["a"]}</p></div>'
        for q in faq
    )

    services_html = "\n".join(f"<li>{s}</li>" for s in services)
    links_html = "\n".join(
        f'<a href="{url}" style="display:inline-block;margin:.2rem .6rem .2rem 0;padding:.35rem .7rem;background:#f0f4f8;border-radius:6px;text-decoration:none;font-size:.85rem;color:#0a4d68">{label}</a>'
        for url, label in internal_links
    )

    return f'''
<!-- GEO-DIFF injected by enrich_cu_desentup.py (vague 1) — do not remove -->
<section class="geo-diff-cu" style="background:#f5f9fc;border-left:4px solid #0a4d68;padding:1.5rem;border-radius:10px;margin:1.5rem 0">
<h2 role="heading" aria-level="2" style="color:#0a4d68;font-size:1.4rem;margin-bottom:.8rem">{h2q}</h2>
<p itemprop="acceptedAnswer" itemscope itemtype="https://schema.org/Answer" style="margin-bottom:1rem;line-height:1.7"><span itemprop="text">{intro}</span></p>
<div style="background:#fff;padding:1rem;border-radius:8px;margin-bottom:1rem">
<p><strong>📍 Zona tarifária:</strong> Z{zone} · <strong>Deslocação:</strong> {desloc}€ · <strong>Distância desde Macedo de Cavaleiros:</strong> {km_str}</p>
<p><strong>🏷️ Tarifa:</strong> {TARIF_HORA}€/h (mão de obra). Hora de trabalho e deslocação confirmadas por telefone antes da deslocação.</p>
<p><strong>📞 Atendimento 24h/7d</strong> mediante confirmação por chamada.</p>
</div>
</section>

<section class="geo-faq-cu" style="background:#fff;padding:1.5rem;border-radius:10px;margin:1.5rem 0">
<h2 role="heading" aria-level="2" style="color:#0a4d68;font-size:1.4rem;margin-bottom:1rem">❓ Perguntas Frequentes — Desentupimento Urgente {name}</h2>
{faq_html}
</section>

<section class="geo-services-cu" style="background:#fff;padding:1.5rem;border-radius:10px;margin:1.5rem 0;border-left:5px solid #0a4d68">
<h2 role="heading" aria-level="2" style="color:#0a4d68;font-size:1.4rem;margin-bottom:1rem">🔧 Serviços urgentes de desentupimento em {name}</h2>
<ul style="padding-left:1.3rem;line-height:1.7">{services_html}</ul>
</section>

<section class="geo-table-cu" style="background:#fff;padding:1.5rem;border-radius:10px;margin:1.5rem 0">
<h2 role="heading" aria-level="2" style="color:#0a4d68;font-size:1.4rem;margin-bottom:1rem">📋 Tabela de deslocação por zona — referência oficial</h2>
<table style="width:100%;border-collapse:collapse;background:#fff">
<thead><tr style="background:#0a4d68;color:#fff"><th style="padding:.6rem;text-align:left">Zona</th><th style="padding:.6rem;text-align:left">Distância aprox.</th><th style="padding:.6rem;text-align:left">Deslocação</th><th style="padding:.6rem;text-align:left">Majoração noite/domingo/feriado</th></tr></thead>
<tbody>
<tr><td style="padding:.55rem;border-bottom:1px solid #eee">Z1</td><td style="padding:.55rem;border-bottom:1px solid #eee">até 15 km</td><td style="padding:.55rem;border-bottom:1px solid #eee">15€</td><td style="padding:.55rem;border-bottom:1px solid #eee">+50%</td></tr>
<tr style="background:#fff5e0"><td style="padding:.55rem;border-bottom:1px solid #eee"><strong>Z{zone} ← esta zona</strong></td><td style="padding:.55rem;border-bottom:1px solid #eee">{km_str}</td><td style="padding:.55rem;border-bottom:1px solid #eee"><strong>{desloc}€</strong></td><td style="padding:.55rem;border-bottom:1px solid #eee">+50%</td></tr>
<tr><td style="padding:.55rem">Z{next_zone}</td><td style="padding:.55rem">{next_dist}</td><td style="padding:.55rem">{next_preco}€</td><td style="padding:.55rem">+50%</td></tr>
</tbody>
</table>
<p style="font-size:.8rem;color:#666;margin-top:.5rem">Hora de trabalho {TARIF_HORA}€ (mão de obra). Para confirmação exata da sua zona, ligue +351 928 484 451.</p>
</section>

<section class="geo-links-cu" style="background:#f8f9fa;padding:1.5rem;border-radius:10px;margin:1.5rem 0">
<h2 style="color:#0a4d68;margin-bottom:.5rem">🔗 Páginas relacionadas — Desentupimento {name}</h2>
<div style="margin-top:.5rem">{links_html}</div>
</section>
<!-- /GEO-DIFF -->
'''


def patch_one_page(c: dict, neighbors: list[str], enable_index: bool = False) -> tuple[bool, str]:
    """Patch une page CU canalizador-desentupimento-{slug}.html. Retourne (modified, log)."""
    slug = c["slug"]
    name = c["name"]
    path = ROOT / f"canalizador-desentupimento-{slug}.html"
    if not path.exists():
        return False, f"  SKIP {slug}: file not found"

    original = path.read_text(encoding="utf-8")
    content = original
    log = []

    # 1) Si noindex,follow → index,follow (activé sur demande)
    if enable_index:
        m = re.search(r'<meta name="robots" content="noindex[^"]*"', content)
        if m:
            content = content.replace(m.group(0), '<meta name="robots" content="index, follow">', 1)
            log.append(f"  robots: noindex → index")

    # 2) Title unique avec zone+preço+ville+intent
    new_title = (
        f"🚨 Desentupimento Urgente {name} 24h · {c['desloc']}€ · Norte Reparos"
    )
    m = re.search(r"<title>[^<]*</title>", content)
    if m:
        if m.group(0) != f"<title>{new_title}</title>":
            content = content.replace(m.group(0), f"<title>{new_title}</title>", 1)
            log.append(f"  title updated")

    # 3) Meta description unique avec zone+preço+km
    if c["km"] > 0:
        km_phrase = f" a {c['km']:.0f} km (~{c['min']} min)"
    else:
        km_phrase = " (base operacional em Macedo de Cavaleiros)"
    new_desc = (
        f"Desentupimento urgente em {name} ({c['district']}),{km_phrase}. "
        f"Desentupir canos, entupimento de sanita/ralo/esgoto 24h/7d. "
        f"Deslocação Z{c['zone']}={c['desloc']}€, {TARIF_HORA}€/h. "
        f"Ligue +351 928 484 451 — orçamento por escrito antes da intervenção."
    )
    m = re.search(r'<meta name="description" content="[^"]*">', content)
    if m:
        if m.group(0) != f'<meta name="description" content="{new_desc}">':
            content = content.replace(m.group(0), f'<meta name="description" content="{new_desc}">', 1)
            log.append(f"  meta desc updated")

    # 4) Zone badge: s'assurer que la classe zone-badge reflète la bonne zone
    zone_badge_re = re.compile(r'class="zone-badge"[^>]*>([^<]+)</div>')
    m = zone_badge_re.search(content)
    if c["km"] > 0:
        dist_phrase = f"{c['km']:.0f} km (~{c['min']} min)"
    else:
        dist_phrase = "base operacional"
    new_badge = (
        f'class="zone-badge">📍 Zona {c["zone"]} · {c["desloc"]}€ deslocação · {dist_phrase} · {name}</div>'
    )
    if m and m.group(0) != new_badge:
        content = content.replace(m.group(0), new_badge, 1)
        log.append(f"  zone-badge updated to Z{c['zone']}")

    # 5) Lead answer-first (paragraph <p class="answer-first">) — si pas déjà différencié
    new_lead = intro_unique(c)
    lead_re = re.compile(r'<p class="answer-first">[^<]+</p>')
    m = lead_re.search(content)
    if m and name not in m.group(0):
        # already has "answer-first" lead; only patch if it doesn't already mention the city name
        content = content.replace(m.group(0), f'<p class="answer-first">{new_lead}</p>', 1)
        log.append(f"  lead answer-first updated ({name}-specific)")
    elif not m:
        # No existing answer-first: inject one just after </header>
        anchor = "</header>"
        if anchor in content:
            content = content.replace(anchor, anchor + f'\n<p class="answer-first">{new_lead}</p>', 1)
            log.append(f"  lead answer-first injected")

    # 6) JSON-LD graphe complet — inject s'il n'existe pas
    graph_block = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org",
        "@graph": website_org_graph() + [
            local_business_schema(c),
            service_schema(c),
            faq_schema(c),
            howto_schema(c),
            speakable_schema(c),
        ],
    }, ensure_ascii=False).replace("</", "<\\/") + '</script>'

    if "localbusiness-" + slug not in content:  # marker du @id unique
        # Inject avant </head>
        if "</head>" in content:
            content = content.replace("</head>", graph_block + "\n</head>", 1)
            log.append(f"  JSON-LD graph injected (6 schemas)")

    # 7) Briques GEO HTML (H2 question, FAQ, services, table, links) — injecter avant <script src="/sticky-mobile.js"
    bloc = briques_geo(c, neighbors)
    if "geo-diff-cu" not in content:
        anchor = '<script src="/sticky-mobile.js" defer></script>'
        if anchor in content:
            content = content.replace(anchor, bloc + "\n" + anchor, 1)
            log.append(f"  GEO HTML block injected (H2+FAQ+services+table+links)")

    if content != original:
        path.write_text(content, encoding="utf-8")
        return True, "\n".join(log)
    return False, "  no change"


def nearest_concelhos(c: dict, all_cs: list[dict], n: int = 4) -> list[str]:
    """Renvoie N concelhos voisins triés par |delta|km."""
    here = c["km"] or 0
    rows = []
    for other in all_cs:
        if other["slug"] == c["slug"]:
            continue
        d = abs((other["km"] or 0) - here)
        rows.append((d, other["slug"]))
    rows.sort()
    return [slug for _, slug in rows[:n]]


# Globals (set in main)
all_concelhos_lookup: list[dict] = []


def main():
    parser = argparse.ArgumentParser(description="Enrich CU canalizador-desentupimento pages")
    parser.add_argument("--only", nargs="+", help="Restreindre à ces slugs")
    parser.add_argument("--index", action="store_true", help="Activer index sur pages noindex")
    args = parser.parse_args()

    global all_concelhos_lookup

    sources = load_sources()
    all_concelhos_lookup = list(sources.values())

    # 30 villes cœur (TomTom complètes)
    cible_slugs = [
        "macedo-de-cavaleiros", "mirandela", "alfandega-da-fe", "vila-flor", "braganca",
        "valpacos", "mogadouro", "vinhais", "carrazeda-de-ansiaes", "torre-de-moncorvo",
        "vimioso", "miranda-do-douro", "chaves", "vila-real", "vila-pouca-de-aguiar",
        "montalegre", "boticas", "freixo-de-espada-a-cinta", "sabrosa", "ribeira-de-pena",
        "murca", "sao-joao-da-pesqueira", "alijo", "penedono", "mesao-frio",
        "santa-marta-de-penaguiao", "lamego", "armamar", "tarouca", "sernancelhe",
    ]

    if args.only:
        cible_slugs = [s for s in cible_slugs if s in args.only]

    modified = 0
    skipped = 0
    print(f"\n{'='*60}")
    print(f"CU — enriching {len(cible_slugs)} pages (vague 1 hyper-local)")
    print(f"{'='*60}\n")

    for slug in cible_slugs:
        c = sources.get(slug)
        if not c:
            print(f"\nSKIP {slug}: absent from TomTom source")
            skipped += 1
            continue

        neighbors = nearest_concelhos(c, all_concelhos_lookup, n=4)
        ok, log = patch_one_page(c, neighbors, enable_index=args.index)
        status = "✓ PATCHED" if ok else "· SKIP"
        print(f"{status} {slug} (Z{c['zone']}, {c['desloc']}€, {c['km']:.0f} km)")
        if log:
            for line in log.split("\n"):
                print(f"    {line}")
        if ok:
            modified += 1
        else:
            skipped += 1

    print(f"\n{'='*60}")
    print(f"DONE: {modified} modified, {skipped} skipped, total cible {len(cible_slugs)}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
