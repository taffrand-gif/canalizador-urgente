#!/usr/bin/env python3
"""Generate 70 city HTML pages for canalizador-urgente.pt"""

import os

# 70 localities with zones and prices
LOCALITIES = [
    # Z1 — 0-30km — 80€
    {"name": "Macedo de Cavaleiros", "slug": "macedo-de-cavaleiros", "price": "80"},
    {"name": "Torre de Dona Chama", "slug": "torre-de-dona-chama", "price": "80"},
    {"name": "Mirandela", "slug": "mirandela", "price": "80"},
    # Z2 — 31-41km — 90€
    {"name": "Alfândega da Fé", "slug": "alfandega-da-fe", "price": "90"},
    {"name": "Izeda", "slug": "izada", "price": "90"},
    {"name": "Vila Flor", "slug": "vila-flor", "price": "90"},
    # Z3 — 42-79km — 110€
    {"name": "Bragança", "slug": "braganca", "price": "110"},
    {"name": "Valpaços", "slug": "valpacos", "price": "110"},
    {"name": "Mogadouro", "slug": "mogadouro", "price": "110"},
    {"name": "Vinhais", "slug": "vinhais", "price": "110"},
    {"name": "Carrazeda de Ansiães", "slug": "carrazeda-de-ansiaes", "price": "110"},
    {"name": "Torre de Moncorvo", "slug": "torre-de-moncorvo", "price": "110"},
    {"name": "Murça", "slug": "munca", "price": "110"},
    {"name": "Vilarandelo", "slug": "vilarandelo", "price": "110"},
    {"name": "Vila Nova de Foz Côa", "slug": "vila-nova-de-foz-coa", "price": "110"},
    {"name": "Vimioso", "slug": "vimioso", "price": "110"},
    {"name": "Carrazedo de Montenegro", "slug": "carrazedo-de-montenegro", "price": "110"},
    {"name": "Argozelo", "slug": "argozelo", "price": "110"},
    {"name": "Vilar de Maçada", "slug": "vilar-de-macada", "price": "110"},
    {"name": "Freixo de Numão", "slug": "freixo-de-numao", "price": "110"},
    {"name": "Alijó", "slug": "alijo", "price": "110"},
    {"name": "Chaves", "slug": "chaves", "price": "110"},
    {"name": "Sanfins do Douro", "slug": "sanfins-do-douro", "price": "110"},
    {"name": "Sendim", "slug": "sendim", "price": "110"},
    {"name": "Santo Estêvão", "slug": "santo-estevao", "price": "110"},
    {"name": "Favaios", "slug": "favaios", "price": "110"},
    # Z4 — 80-99km — 120€
    {"name": "Mouçós", "slug": "moucos", "price": "120"},
    {"name": "São João da Pesqueira", "slug": "sao-joao-da-pesqueira", "price": "120"},
    {"name": "Sabrosa", "slug": "sabrosa", "price": "120"},
    {"name": "Almendra", "slug": "almendra", "price": "120"},
    {"name": "Vidago", "slug": "vidago", "price": "120"},
    {"name": "Mêda", "slug": "meda", "price": "120"},
    {"name": "Vila Real", "slug": "vila-real", "price": "120"},
    {"name": "Lordelo", "slug": "lordelo", "price": "120"},
    {"name": "Marialva", "slug": "marialva", "price": "120"},
    {"name": "Cedovim", "slug": "cedovim", "price": "120"},
    {"name": "Vila Pouca de Aguiar", "slug": "vila-pouca-de-aguiar", "price": "120"},
    {"name": "São Martinho de Anta", "slug": "sao-martinho-de-anta", "price": "120"},
    {"name": "Pinhão", "slug": "pinhao", "price": "120"},
    {"name": "Miranda do Douro", "slug": "miranda-do-douro", "price": "120"},
    {"name": "Cumieira", "slug": "cumieira", "price": "120"},
    {"name": "Freixo de Espada à Cinta", "slug": "freixo-de-espada-a-cinta", "price": "120"},
    {"name": "Pedras Salgadas", "slug": "pedras-salgadas", "price": "120"},
    {"name": "Trevões", "slug": "trevoes", "price": "120"},
    {"name": "Penedono", "slug": "penedono", "price": "120"},
    {"name": "Peso da Régua", "slug": "peso-da-regua", "price": "120"},
    {"name": "Boticas", "slug": "boticas", "price": "120"},
    {"name": "Figueira de Castelo Rodrigo", "slug": "figueira-de-castelo-rodrigo", "price": "120"},
    # Z5 — 100-119km — 130€
    {"name": "Valdigem", "slug": "valdigem", "price": "130"},
    {"name": "Santa Marta de Penaguião", "slug": "santa-marta-de-penaguiao", "price": "130"},
    {"name": "Ervedosa do Douro", "slug": "ervadosa-do-douro", "price": "130"},
    {"name": "Cambres", "slug": "cambres", "price": "130"},
    {"name": "Tabuaço", "slug": "tabuaco", "price": "130"},
    {"name": "Pinhel", "slug": "pinhel", "price": "130"},
    {"name": "Britiande", "slug": "britiande", "price": "130"},
    {"name": "Lamego", "slug": "lamego", "price": "130"},
    {"name": "Armamar", "slug": "armamar", "price": "130"},
    {"name": "Montalegre", "slug": "montalegre", "price": "130"},
    {"name": "Mesão Frio", "slug": "mesao-frio", "price": "130"},
    {"name": "Sernancelhe", "slug": "sernancelhe", "price": "130"},
    {"name": "Lalim", "slug": "lalim", "price": "130"},
    {"name": "Vila Franca das Naves", "slug": "vila-franca-das-naves", "price": "130"},
    {"name": "Tarouca", "slug": "tarouca", "price": "130"},
    {"name": "Lazarim", "slug": "lazarim", "price": "130"},
    {"name": "Mondim da Beira", "slug": "mondim-da-beira", "price": "130"},
    {"name": "São Cosmado", "slug": "sao-cosmado", "price": "130"},
    {"name": "Ribeira de Pena", "slug": "ribeira-de-pena", "price": "130"},
    # Z6 — 120km+ — 140€
    {"name": "São João de Tarouca", "slug": "sao-joao-de-tarouca", "price": "140"},
    {"name": "Salzedas", "slug": "salzedas", "price": "140"},
    {"name": "Aguiar da Beira", "slug": "aguiar-da-beira", "price": "140"},
]

SITE = "https://canalizador-urgente.pt"
PHONE_DISPLAY = "928 484 451"
PHONE_LINK = "351928484451"
WHATSAPP_LINK = f"https://wa.me/{PHONE_LINK}"

TEMPLATE = """<!DOCTYPE html>
<html lang="pt-PT">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Canalizador Urgente {city} 💧 24h | {phone}</title>
<meta name="description" content="Canalizador urgente em {city} — resposta rápida 24h. Desentupimentos, fugas de água, esquentadores. Desde {price}€">
<link rel="canonical" href="{site}/canalizador-urgente-{slug}">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Canalizador Urgente {city}",
  "description": "Serviço de canalização urgente em {city}, Trás-os-Montes",
  "telephone": "+351{phone_link}",
  "areaServed": {{"@type": "City", "name": "{city}"}},
  "openingHours": "Mo-Su 00:00-23:59",
  "priceRange": "€€"
}}
</script>
<style>
* {{margin:0;padding:0;box-sizing:border-box}}
body {{font-family:system-ui,-apple-system,sans-serif;background:#f8f9fa;color:#222;line-height:1.6}}
header {{background:linear-gradient(135deg,#2193b0,#1a5276);color:white;padding:2rem 1rem;text-align:center}}
header h1 {{font-size:2rem;margin-bottom:0.5rem}}
header .tel {{font-size:1.4rem;font-weight:bold;margin:0.5rem 0}}
header .tel a {{color:white;text-decoration:none}}
main {{max-width:800px;margin:0 auto;padding:2rem 1rem}}
.price {{background:linear-gradient(135deg,#2193b0,#1a5276);color:white;padding:1.5rem;border-radius:12px;text-align:center;font-size:1.3rem;margin-bottom:2rem}}
.price strong {{font-size:2.5rem;display:block}}
.services {{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:2rem}}
.services li {{background:white;padding:1rem;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.1);list-style:none;font-weight:500}}
.equipment {{background:#e8f4f8;padding:1.5rem;border-radius:12px;margin-bottom:2rem}}
.equipment h2 {{color:#1a5276;margin-bottom:0.5rem}}
.cta {{display:flex;flex-direction:column;gap:1rem;margin-bottom:2rem}}
.cta a {{display:block;padding:1rem;text-decoration:none;border-radius:8px;font-weight:bold;font-size:1.1rem;text-align:center}}
.cta .tel {{background:#2193b0;color:white}}
.cta .wa {{background:#25D366;color:white}}
.faq h2 {{color:#1a5276;margin-bottom:1rem}}
.faqitem {{background:white;padding:1rem;margin-bottom:0.75rem;border-radius:8px;border-left:4px solid #2193b0}}
.faqitem strong {{display:block;margin-bottom:0.25rem;color:#333}}
footer {{background:#1a5276;color:#aac4d6;padding:1.5rem;text-align:center;font-size:0.9rem;margin-top:2rem}}
footer a {{color:#aac4d6}}
</style>
</head>
<body>
<header>
<h1>Canalizador Urgente em {city} 💧 24h</h1>
<p class="tel">📞 <a href="tel:+351{phone_link}">{phone}</a></p>
</header>
<main>
<div class="price">
Orçamento sem compromisso<br>
<strong>Desde {price}€</strong>
</div>
<ul class="services">
<li>🔧 Desentupimentos</li>
<li>💧 Reparação de Fugas de Água</li>
<li>🚿 Esquentadores e Caldeiras</li>
<li>🔨 Canalização Nova</li>
<li>🏠 Instalação Sanitários</li>
<li>⚡ Deteção de Fugas</li>
</ul>
<div class="equipment">
<h2>Equipamento Profissional</h2>
<p>🛠️ Ridgid K-6200 • 📷 Câmara Térmica FLIR • 🎯 Geofone — diagnóstico preciso sem demolições desnecessárias.</p>
</div>
<div class="cta">
<a href="tel:+351{phone_link}" class="tel">📞 Ligar Agora — {phone}</a>
<a href="{whatsapp}" target="_blank" rel="noopener" class="wa">💬 WhatsApp — Resposta Imediata</a>
</div>
<div class="faq">
<h2>Perguntas Frequentes</h2>
<div class="faqitem"><strong>Qual o custo do serviço em {city}?</strong> Desde {price}€ — orçamento gratuito sem compromisso.</div>
<div class="faqitem"><strong>Funciona 24 horas?</strong> Sim, atendimento urgente 24 horas por dia, 7 dias por semana.</div>
<div class="faqitem"><strong>Que zonas cobre em {city}?</strong> Todo o distrito e concelhos vizinhos — resposta rápida garantida.</div>
<div class="faqitem"><strong>Emit fatura?</strong> Sim, emitimos fatura com NIF e garantia escrita de 12 meses.</div>
</div>
</main>
<footer>
<p>⚡另一 site: <a href="https://eletricista-urgente.pt">Eletricista Urgente</a></p>
<p>Canalizador Urgente em {city} | Trás-os-Montes</p>
</footer>
</body>
</html>"""

def generate_pages():
    out_dir = os.path.join(os.path.dirname(__file__), "public")
    os.makedirs(out_dir, exist_ok=True)
    
    for loc in LOCALITIES:
        html = TEMPLATE.format(
            city=loc["name"],
            slug=loc["slug"],
            price=loc["price"],
            phone=PHONE_DISPLAY,
            phone_link=PHONE_LINK,
            whatsapp=WHATSAPP_LINK,
            site=SITE,
        )
        filename = f"canalizador-urgente-{loc['slug']}.html"
        with open(os.path.join(out_dir, filename), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Generated: {filename}")
    
    print(f"\nTotal: {len(LOCALITIES)} pages")

if __name__ == "__main__":
    generate_pages()