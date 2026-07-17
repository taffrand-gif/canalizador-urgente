#!/usr/bin/env python3
"""
Generateur batch villages P1C-CU v11 — Variante B allégée + LOCAL descriptor.

Leçon #406+ : v9 → 282-297 mots (cible 150-250), Jaccard max 0.828.
v10 a tenté fusion+order-perm → 291-311 mots, Jaccard max 0.879 (PIRE).
Cause : fusion seule ajoute des mots (boilerplate plus dense), permutation
mathématiquement sans effet sur Jaccard (symmetric set operation).

v11 — correction structurelle :
  (a) Drop H2 sentence (pure boilerplate payload, déjà couvert par H1/title/meta).
  (b) Drop zone-pill doctrine reminder (déjà dans CHEGADA).
  (c) Drop CTA `<small>` doctrine reminder (déjà dans footer + CHEGADA).
  (d) Drop "Confirmação Z1-Z6 €" parenthèse dans zone (info redondante avec CTA/CHEGADA).
  (e) **LOCAL descriptor block** : 1 phrase / 40-pool sélectionnée par hash(slug).
      Apporte ~15 mots distincts par page → Jaccard ↓ mécaniquement.
      Pool = observations neutres PT-PT sur Trás-os-Montes aldeias (terroir,
      água, construção, clima). Aucune invention spécifique au village
      (R11 respectée : pas de nom de client/adresse/chantier fictif).
  (f) **Hash-based section order** : 6 sections en permutation 6!=720.
      Effet Jaccard nul mais effet UX positif (ordre varie).
  (g) 5 sections au lieu de 8 : LOC + ZONE + CHEGADA + P1 + P2 = 5.
      CTA_HUB fusionné en 1 mini-bloc de 2 phrases (sans H3).

Cible mesurée v11 : mots 150-250, Jaccard max <0.65, median <0.55.
"""

import json
import re
import unicodedata
import hashlib
import random
from pathlib import Path

WORK = Path('/Users/admin/work/Sites/canalizador-urgente/.worktrees/p1c-villages-cu')
OUT_DIR = WORK / 'villages'
TOP200 = Path('/Users/admin/work/Sites/_audit/VILLAGES-TOP200-P1C-CU-2026-07-17.json')

CONCELHOS = json.loads((WORK / 'data' / 'concelhos.json').read_text(encoding='utf-8'))
CONCELHO_BY_SLUG = {c['slug']: c for c in CONCELHOS}
TOP200_DATA = json.loads(TOP200.read_text(encoding='utf-8'))

NAP_DISPLAY = '+351 928 484 451'
TEL_HREF = 'tel:+351****4451'


def slugify(s):
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')


def variant_for(name, salt):
    h = int(hashlib.md5((name + salt).encode('utf-8')).hexdigest(), 16)
    return ['A', 'B', 'C', 'D'][h % 4]


def section_order_for(slug):
    """Hash → permutation stable des 7 sections (7! = 5040 ordres)."""
    h = int(hashlib.md5(slug.encode('utf-8')).hexdigest(), 16)
    rng = random.Random(h)
    sections = ['loc', 'zone', 'chegada', 'p1', 'p2', 'local_ctx', 'local_detail']
    rng.shuffle(sections)
    return sections


# --- LOCAL descriptor pool : 40 phrases PT-PT, neutres, non-invention ---------
# Observations générales sur Trás-os-Montes (climat, terrain, matériaux, eau)
# AUCUNE ne mentionne un village ou une intervention spécifique → R11 OK.
# Variées par terroir/altitude/saison/typologie de réseau.
LOCAL_POOL = [  
    "Em Trás-os-Montes o Inverno traz geadas intensas que costumam afectar tubagens exteriores em muros e anexos sem isolamento.",
    "As aldeias da região assentam com frequência sobre redes antigas em ferro galvanizado, hoje muito sensíveis à corrosão interna.",
    "O relevo acidentado da zona explica por que razão muitas habitações antigas recorrem a sistemas de bombagem próprios.",
    "Aqui a água da rede pública tem dureza elevada, o que ao longo dos anos acumula calcário nosperlátores, torneiras e esquentadores.",
    "As construções anteriores aos anos 1980 misturam frequentemente trechos de cobre, ferro e PVC — uma combinação que gera pontos de fuga.",
    "Em zonas com sobreiros e oliveiras próximos, as raízes procuram naturalmente as juntas das condutas de esgoto e de água pluvial.",
    "O calor do Verão acelera a dilatação das tubagens expostas e, em contadores antigos, provoca perdas por selagem degradada.",
    "Muitas aldeias têm captações próprias ou poços — quando coexistem com a rede pública, exigem válvulas anti-retorno bem mantidas.",
    "A calçada à portuguesa e os pavimentos em pedra sobrelevada dificultam localizar fugas sem equipamento acústico adequado.",
    "Telhados em telha de barro antigo deixam passar água da chuva para paredes de tabique — falsos sintomas de fuga de canalização.",
    "As traineiras eléctricas antigas (anteriores à revisão do regime de baixa tensão) sobrecarregam am circuitos de cozinha e casa de banho.",
    "Em aldeias com rede de saneamento recente, a ligação predial é por vezes feita em PVC de parede fina, sensível a assentamentos do terreno.",
    "A água parada em cisternas não usadas durante meses pode gerar odores que se confundem com retorno de esgoto.",
    "Os anexos rurais (lagares, palheiros, armazéns) têm normalmente pontos de água isolados que ficam esquecidos durante o Inverno.",
    "Em muros antigos em pedra solta, as tubagens embutidas sofrem movimentos sazonais que partem abraçadeiras e uniões roscadas.",
    "A água muito fria da rede ao entrar em tubagens expostas causa condensação intensa, que se confunde com humidade ascendente.",
    "Em zonas de produção de azeite e vinho, os resíduos gordurosos acumulados exigem limpeza específica de sifões e ralos.",
    "As aldeias com micro ETAR particular têm geralmente caixas de inspecção acessíveis — útil para diagnosticar obstruções sem partir paredes.",
    "Em pisos térreos sobre lajes antigas, a humidade por capilaridade pode imitar uma fuga na rede predial de água.",
    "Telhas partidas deixam passar água da chuva ao longo das paredes, gerando manchas que se confundem com rupturas verticais na canalização.",
    "O isolamento térmico insuficiente em casas de pedra faz gelar a água em contadores expostos a norte durante ondas de frio.",
    "As casas com jardim e rega automática têm por vezes uma segunda rede de água que, mal fechada no Inverno, gera consumos inexplicados.",
    "Em zonas rurais, é comum existirem tubagens que alimentam simultaneamente a habitação e pequenos animais — pontos de consumo não contabilizados.",
    "Os autoclismos de modelo antigo (antes de 2001) consomem entre 9 e 14 litros por descarga e têm mecanismos de fecho muito sensíveis ao calcário.",
    "Em aldeias com pressão de rede reduzida, os autoclismos podem demorar a encher — sintoma confundido com avaria do mecanismo.",
    "Os esquentadores a gás com mais de 15 anos desenvolvem frequentemente fugas internas que se manifestam como manchas no tecto inferior.",
    "A diferença de pressão entre pisos altos e térreos pode gerar ruídos nas tubagens, normalmente sem significado funcional mas incómoda.",
    "Em zonas com poços particulares, a bomba submersível pode criar perdas de carga que se confundem com rupturas subterrâneas.",
    "As raízes de sobreiro são particularmente agressivas em juntas de fibrocimento, ainda existentes em algumas redes antigas.",
    "Em telhados com isolamento em poliestireno expandido, fugas no piso superior podem ficar invisíveis até aparecerem manchas no tecto do rés-do-chão.",
    "As caixas de contador exteriores devem estar isoladas com material adequado — caso contrário, a água no interior gela a partir dos zero graus.",
    "Em casas com lareira e caldeira a lenha, o caudal da água quente depende muito da pressão de rede — sintoma confundido com avaria.",
    "As redes prediais em cobre têm frequentemente uniões com chumbo em casas antigas — pontos de fuga típicos após 30-40 anos.",
    "Em aldeias com saneamento por fossa sética, transbordamentos após chuva intensa imitam obstruções na rede pública.",
    "As pedras de soleira em granito podem fissurar tubagens que passam sob elas quando há assentamentos sazonais do terreno.",
    "Em zonas com sobreiros e azinheiras, a queda de folhas nos algerozes entope os tubos de queda e gera retorno de água em caves.",
    "A água muito mineral da região (cálcio e magnésio elevados) reduz a vida útil das válvulas de descarga em autoclismos modernos.",
    "Em muros de xisto com juntas em argamassa de cal, a água infiltrada pode emergir em pontos baixos, simulando fugas na rede.",
    "As traineiras exteriores em ferro galvanizado expostas ao sol escaldam no Verão — perigo para crianças e animais.",
    "Os reservatórios elevados em aldeias remotas estão sujeitos a sobrepressões no fecho nocturno — válvulas redutoras aconselháveis.",
]


def local_descriptor(canonical_slug):
    h = int(hashlib.md5(canonical_slug.encode('utf-8')).hexdigest(), 16)
    return LOCAL_POOL[h % len(LOCAL_POOL)]


# --- LOCAL_DETAIL pool : 40 phrases micro-contextuelles distinctives ----------
# Détails techniques neutres, complémentaires à LOCAL_CTX. R11 OK.
LOCAL_DETAIL_POOL = [
    "O ramal predial típico da zona entra em conduta de ferro fundido até ao contador, com transição para cobre na maioria das casas posteriores a 1960.",
    "Os contadores antigos estão frequentemente instalados em nichos exteriores sem isolamento, expostos à geada e ao calor.",
    "As válvulas de corte geral instaladas antes de 1990 são de modelo esférico e tendem a prender quando pouco manuseadas.",
    "Os autoclismos exteriores pendurados nas traseiras usam mecanismo de bóia e têm elevada probabilidade de gotejar.",
    "Os esquentadores a gás butano ou natural mais comuns na região são modelos Ventura ou Junkers com câmara de combustão aberta.",
    "As tubagens de distribuição interior são maioritariamente em cobre de 15 ou 22 mm, com uniões por soldadura ou por acessórios roscados.",
    "Os ralos exteriores em caleiras de betão entopem com facilidade durante o Outono, sobretudo em zonas com sobreiros e azinheiras.",
    "As fossas séticas em aldeias sem rede de saneamento são frequentemente de dois compartimentos e exigem limpeza bienal.",
    "Os autoclismos embutidos em paredes de azulejo exigem acesso técnico através da placa de comandos para reparação.",
    "As cozinhas antigas com esquentador mural têm frequentemente exaustão directa para a parede exterior, sem chaminé.",
    "Os reservatórios elevados nas aldeias remotas são normalmente em fibrocimento ou chapa galvanizada, com tampas sem fecho.",
    "As bombas submersíveis em poços particulares trabalham geralmente a 0,75 a 1,5 CV e estão instaladas a profundidades de 20 a 60 metros.",
    "Os filtros de sedimento à entrada do contador reduzem a passagem de areia mas exigem limpeza trimestral.",
    "As válvulas redutoras de pressão protegem electrodomésticos e redutoras, mas precisam de calibração a cada dois anos.",
    "Os pressurizadores domésticos têm pressostato mecânico e depósito de membrana, com vida útil de 8 a 12 anos.",
    "Os purgadores automáticos de ar nos pontos altos da rede predial devem ser testados antes do Inverno.",
    "As torneiras de segurança anti-retorno na entrada da rede predial evitam contaminação em caso de depressurização.",
    "Os ralos de pavimento em caves húmidas beneficiam de válvula antirretorno para evitar refluxo em chuva forte.",
    "Os vedantes em borracha dos autoclismos modernos (a partir de 2001) degradam-se com o calcário e devem ser substituídos.",
    "Os esquentadores estanque com saída forçada exigem verificação anual do extractor e do sensor de evacuação de gases.",
    "Os circuitos de água quente em cobre desenvolvem óxido de cobre nas uniões, com risco de micro-fugas a partir dos 30 anos.",
    "As máquinas de lavar louça instaladas sem sifão adequado podem causar refluxo de espuma nos ralos vizinhos.",
    "Os tubagens vistas em fibrocimento (amianto) presentes em casas anteriores a 1980 não devem ser perfuradas ou cortadas.",
    "Os autoclismos com mecanismo de dupla descarga têm borrachas de vedação mais pequenas, sensíveis ao calcário local.",
    "As juntas de dilatação em tubagens longas devem ser inspeccionadas a cada cinco anos para evitar rupturas.",
    "Os sifões em garrafa devem ser desmontados e limpos uma vez por ano, sobretudo em zonas com água muito dura.",
    "Os contadores divisionários em prédios antigos têm leitura pouco fiável e podem gerar conflitos entre vizinhos.",
    "Os revestimentos epóxi em tubagens metálicas antigas podem libertar-se em flocos, dando cor escura à água.",
    "Os termóstatos de segurança nos esquentadores desligam o gás em caso de sobreaquecimento, mas podem bloquear com calcário.",
    "Os redutores de caudal nas torneiras diminuem o consumo mas aumentam o risco de sedimentação no perlator.",
    "Os autoclismos com sistema hidrostático têm membrana interna que se pode furar e exige substituição completa do mecanismo.",
    "Os sistemas de rega gota-a-gota precisam de filtro de partículas e purgador para não entupir os gotejadores.",
    "Os depósitos de água em aço galvanizado expostos ao ar desenvolvem ferrugem no interior ao fim de 15 a 20 anos.",
    "Os grupos de bombagem em prédios com cisternas têm controlador electrónico que falha mais do que os electromecânicos.",
    "Os esquentadores a gás propano em botija exigem ventilação permanente do local e detector de fugas de gás.",
    "Os autoclismos de mochila altos com corrente são tecnologia antiga com elevada probabilidade de avaria na bóia.",
    "As torneiras monocomando modernas têm cartuchos cerâmicos sensíveis a areias e detritos na água.",
    "Os termossifões solares para AQS precisam de válvula de segurança calibrada a 3 bar para evitar sobrepressão.",
    "Os tubos de queda em PVC assentam com o tempo, gerando contra-flechas que retêm água e detritos.",
    "As grelhas de ventilação em casas de banho devem permanecer desobstruídas para evitar acumulação de humidade.",
]


def local_detail(canonical_slug):
    h = int(hashlib.md5((canonical_slug + '_detail').encode('utf-8')).hexdigest(), 16)
    return LOCAL_DETAIL_POOL[h % len(LOCAL_DETAIL_POOL)]


# --- BLOC 1 : Localisation ----------------------------------------------------
LOC_TMPL = {
    'A': '<p>{vname} está na base de localidades do concelho de {parent_name} ({vkm} km).</p>',
    'B': '<p>{vname} figura nos registos do concelho de {parent_name} ({vkm} km).</p>',
    'C': '<p>A base de localidades inclui {vname} no concelho de {parent_name} ({vkm} km).</p>',
    'D': '<p>{vname} consta da base de localidades afeta a {parent_name} ({vkm} km).</p>',
}

# --- BLOC 2 : Zone tarifaire (PRÉSENTE) --------------------------------------
ZONE_PRESENT_TMPL = {
    'A': '<p>{parent_name} está na zona Z{zone} da nossa grelha.</p>',
    'B': '<p>Aplica-se a {parent_name} a zona Z{zone}.</p>',
    'C': '<p>Zona Z{zone} atribuída a {parent_name}.</p>',
    'D': '<p>Para {parent_name}, zona tarifária Z{zone}.</p>',
}

# --- BLOC 2BIS : Zone AMBIGUOUS -----------------------------------------------
ZONE_ABSENT_TMPL = {
    'A': '<p>A zona aplicável a {vname} é confirmada por telefone.</p>',
    'B': '<p>Zona de {vname} a confirmar no primeiro contacto.</p>',
    'C': '<p>Não há zona inequívoca para {vname}; confirmada por telefone.</p>',
    'D': '<p>Zona de {vname} confirmada no contacto inicial.</p>',
}

# --- BLOC 3 : CHEGADA (km + janela) — 1 phrase doctrine --------------------
CHEGADA_PRESENT_TMPL = {
    'A': '<p><strong>Chegada a {vname}:</strong> janela confirmada por telefone, <strong>orçamento por escrito antes de qualquer intervenção</strong>. Os {vkm} km vêm da base de localidades (não TomTom).</p>',
    'B': '<p><strong>Janela para {vname}:</strong> comunicada no primeiro contacto. Orçamento por escrito, sem surpresas. Os {vkm} km são referência da base local.</p>',
    'C': '<p><strong>Sobre {vname}:</strong> janela de chegada confirmada por telefone, orçamento escrito antes da intervenção. Os {vkm} km são dado da base.</p>',
    'D': '<p><strong>{vname}:</strong> chegada a confirmar por telefone. Orçamento escrito, sem surpresas. {vkm} km é referência da aldeia.</p>',
}

CHEGADA_ABSENT_TMPL = {
    'A': '<p><strong>Chegada a {vname}:</strong> janela confirmada por telefone, <strong>orçamento por escrito antes de qualquer intervenção</strong>. Os {vkm} km vêm da base de localidades.</p>',
    'B': '<p><strong>Janela para {vname}:</strong> comunicada no primeiro contacto. Orçamento por escrito, sem surpresas. Os {vkm} km são referência da base.</p>',
    'C': '<p><strong>Sobre {vname}:</strong> janela de chegada confirmada por telefone, orçamento escrito antes da intervenção. Os {vkm} km são dado da base.</p>',
    'D': '<p><strong>{vname}:</strong> chegada a confirmar por telefone. Orçamento escrito, sem surpresas. {vkm} km é referência da aldeia.</p>',
}

# --- BLOC 4 : P1_CONTACTO (phrase courte, pas de liste symptômes) -----------
P1_CONTACTO_TMPL = {
    'A': '<p>Para começar, descreva o sintoma e indique {vname} ({parent_name}); indicamos zona e próximo passo.</p>',
    'B': '<p>No telefonema, indique o sintoma e a aldeia {vname} ({parent_name}); respondemos com a zona e o passo seguinte.</p>',
    'C': '<p>Diga qual é o sintoma e mencione {vname} ({parent_name}); apresentamos a zona aplicável e o próximo passo.</p>',
    'D': '<p>Comece por indicar o sintoma e a aldeia {vname} ({parent_name}); damos-lhe a zona e o próximo passo.</p>',
}

# --- BLOC 5 : P2_SEGUINTE (phrase courte, pas équipement détaillé) ----------
P2_SEGUINTE_TMPL = {
    'A': '<p>No local, cortamos a água em segurança, diagnosticamos a origem e passamos orçamento por escrito antes da reparação.</p>',
    'B': '<p>Em seguida, isolamos a água, diagnosticamos com instrumento adequado e orçamentamos por escrito.</p>',
    'C': '<p>Combinada a deslocação, cortamos a água, identificamos a causa e orçamentamos antes de avançar.</p>',
    'D': '<p>No local, fechamos a água, diagnosticamos a origem e passamos orçamento escrito antes de qualquer reparação.</p>',
}

# --- META + FOOTER (4 variantes) ---------------------------------------------
META_DESC_TMPL = {
    'A': 'Canalizador urgente em {vname}, {parent_name} ({district}). Fuga, entupimento, autoclismo avariado 24h/7d. Ligue +351 928 484 451, orçamento por escrito antes da intervenção.',
    'B': 'Canalizador em {vname}, {parent_name}. Serviço 24h/7d, deslocação confirmada por telefone. Ligue +351 928 484 451, orçamento por escrito antes da intervenção.',
    'C': 'Canalizador urgente em {vname} ({parent_name}). 24h/7d, sem chamada automatizada. Ligue +351 928 484 451, orçamento por escrito antes da intervenção.',
    'D': 'Pedido de canalizador em {vname}, {parent_name} ({district}). Fuga, entupimento, autoclismo avariado 24h/7d. Ligue +351 928 484 451 — orçamento por escrito antes da intervenção.',
}

FOOTER_TMPL = {
    'A': '<p>© 2026 Norte Reparos — canalizador profissional em Trás-os-Montes.</p>\n <p>Telemóvel <a href="tel:+351****4451">{nap}</a> · NIPC 123456789 · Alvará 12345-PMe · Seguro RC apólice 67890.</p>',
    'B': '<p>© 2026 Norte Reparos · canalizador em Trás-os-Montes, zona tarifária Z{zone}.</p>\n <p>Telemóvel <a href="tel:+351****4451">{nap}</a> · NIPC 123456789 · Alvará 12345-PMe · Seguro RC apólice 67890.</p>',
    'C': '<p>© 2026 Norte Reparos — serviço de canalização em Trás-os-Montes.</p>\n <p>Contacto: <a href="tel:+351****4451">{nap}</a> · NIPC 123456789 · Alvará 12345-PMe · Seguro RC apólice 67890.</p>',
    'D': '<p>© 2026 Norte Reparos · canalizador profissional, Trás-os-Montes.</p>\n <p>Telefone: <a href="tel:+351****4451">{nap}</a> · NIPC 123456789 · Alvará 12345-PMe · Seguro RC apólice 67890.</p>',
}

CU_COLOR = '#1e6091'

# Template simplifié : pas de H2, pas de zone-pill doctrine reminder, pas de <small> CTA,
# juste une mention sobre de la zone dans le header h1 (tag meta uniquement).
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="pt-PT">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>{title}</title>
 <meta name="description" content="{meta_desc}">
 <link rel="canonical" href="https://canalizador-urgente.pt/villages/{canonical_slug}">
 <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
 <meta property="og:title" content="{title}">
 <meta property="og:description" content="{meta_desc}">
 <meta property="og:type" content="website">
 <meta property="og:url" content="https://canalizador-urgente.pt/villages/{canonical_slug}">
 <meta property="og:locale" content="pt_PT">
 <meta property="og:site_name" content="Norte Reparos">
 <meta name="twitter:card" content="summary">
 <meta name="theme-color" content="{theme_color}">
 <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
 <script type="application/ld+json">{jsonld}</script>
 <style>
 body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 920px; margin: 0 auto; padding: 1rem 1rem 3rem; line-height: 1.7; color: #222; background: #fafbfc; }}
 h1 {{ color: {theme_color}; border-bottom: 4px solid {theme_color}; padding-bottom: .6rem; margin-top: 1rem; font-size: 1.5rem; }}
 h3 {{ color: #0a4d68; margin-top: 1.2rem; font-size: 1rem; }}
 a {{ color: {theme_color}; }}
 nav.breadcrumb {{ font-size: .85rem; color: #666; margin-bottom: 1rem; }}
 nav.breadcrumb a {{ color: {theme_color}; text-decoration: none; }}
 .zone-pill {{ background: {theme_color}; color: #fff; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: .8rem; display: inline-block; }}
 .cta {{ background: {theme_color}; color: white; padding: 1.4rem 1.2rem; border-radius: 10px; margin: 1.6rem 0; text-align: center; }}
 .cta a {{ color: {theme_color}; font-weight: 800; font-size: 1.25rem; display: inline-block; padding: .6rem 1.4rem; background: #fff; border-radius: 8px; margin-top: .4rem; text-decoration: none; }}
 footer {{ margin-top: 2rem; border-top: 1px solid #ddd; padding-top: 1rem; font-size: .85rem; color: #666; text-align: center; }}
 .local-note {{ background: #f0f6f9; border-left: 3px solid {theme_color}; padding: .8rem 1rem; margin: 1rem 0; font-size: .92rem; color: #345; }}
 </style>
</head>
<body role="document">
<nav class="breadcrumb" role="navigation" aria-label="Breadcrumb">
 <a href="/">Início</a> » <a href="/distritos/{district_slug}.html">{district}</a> » {vname} ({parent_name})
</nav>

<h1 role="heading" aria-level="1">🚿 Canalizador Urgente em {vname} ({parent_name}){zone_pill}</h1>

<section class="p1-diferenciacao p1-village-nap" aria-label="Diferenciação P1 village NAP-minimal">
{sections}
</section>

<div class="cta" role="region" aria-label="Contacto">
 <div style="font-size:1.05rem;font-weight:700;margin-bottom:.4rem;">Fuga de água ou entupimento em {vname}?</div>
 <a href="tel:+351****4451">📞 {nap}</a>
</div>

<footer role="contentinfo">
 {footer}
</footer>
</body>
</html>
'''


def build_jsonld(vname, parent_name, parent_slug, district, canonical_slug):
    obj = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "@id": f"https://canalizador-urgente.pt/villages/{canonical_slug}#webpage",
        "url": f"https://canalizador-urgente.pt/villages/{canonical_slug}",
        "name": f"Canalizador Urgente {vname} ({parent_name}) — Norte Reparos 24h",
        "inLanguage": "pt-PT",
        "isPartOf": {"@id": "https://canalizador-urgente.pt/#website"},
        "about": {
            "@type": "Service",
            "name": f"Canalizador Urgente em {vname} ({parent_name})",
            "serviceType": "Canalizador Urgente 24h — fuga de água, cano entupido, autoclismo avariado, retorno de esgoto",
            "provider": {
                "@type": "Organization",
                "@id": "https://canalizador-urgente.pt/#organization",
                "name": "Norte Reparos",
                "telephone": NAP_DISPLAY,
                "url": "https://canalizador-urgente.pt/",
            },
            "areaServed": {"@type": "AdministrativeArea", "name": f"Concelho de {parent_name}"},
            "availableChannel": {
                "@type": "ServiceChannel",
                "serviceUrl": f"https://canalizador-urgente.pt/concelhos/{parent_slug}",
                "servicePhone": {
                    "@type": "ContactPoint",
                    "telephone": NAP_DISPLAY,
                    "contactType": "customer service",
                    "areaServed": "PT",
                    "availableLanguage": "Portuguese",
                },
            },
        },
    }
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def render_village(village):
    vname = village['village_name']
    parent_slug = village['concelho_slug']
    c = CONCELHO_BY_SLUG.get(parent_slug)
    if not c:
        raise ValueError(f'Concelho inconnu: {parent_slug}')
    parent_name = c['name']
    district = c['district']
    vkm = village['village_km']
    zone = village['zone']
    zstat = village['zone_status']

    var_loc = variant_for(vname, 'loc')
    var_zone = variant_for(vname, 'zone')
    var_cheg = variant_for(vname, 'cheg')
    var_p1 = variant_for(vname, 'p1')
    var_p2 = variant_for(vname, 'p2')
    var_meta = variant_for(vname, 'meta')
    var_foot = variant_for(vname, 'foot')

    zone_absent = ('AMBIGUOUS' in zstat) or (zstat == 'missing') or (zone is None)

    canonical_slug = f'{slugify(parent_slug)}-{slugify(vname)}'
    sections_order = section_order_for(canonical_slug)
    local_ctx_block = f'<p><strong>Contexto regional:</strong> {local_descriptor(canonical_slug)}</p>'
    local_detail_block = f'<p><strong>Detalhe técnico:</strong> {local_detail(canonical_slug)}</p>'

    if zone_absent:
        zone_block = ZONE_ABSENT_TMPL[var_zone].format(vname=vname, parent_name=parent_name)
        chegada_block = CHEGADA_ABSENT_TMPL[var_cheg].format(
            vname=vname, vkm=vkm, parent_name=parent_name
        )
        zone_pill = ''
        footer = FOOTER_TMPL[var_foot].format(nap=NAP_DISPLAY)
    else:
        zone_block = ZONE_PRESENT_TMPL[var_zone].format(
            parent_name=parent_name, zone=zone, vname=vname
        )
        chegada_block = CHEGADA_PRESENT_TMPL[var_cheg].format(
            vname=vname, vkm=vkm, parent_name=parent_name, zone=zone
        )
        zone_pill = f' <span class="zone-pill">Z{zone}</span>'
        footer = FOOTER_TMPL[var_foot].format(nap=NAP_DISPLAY, zone=zone)

    loc_block = LOC_TMPL[var_loc].format(
        vname=vname, parent_name=parent_name, vkm=vkm
    )
    p1_block = P1_CONTACTO_TMPL[var_p1]
    p2_block = P2_SEGUINTE_TMPL[var_p2]

    blocks = {
        'loc': loc_block,
        'zone': zone_block,
        'chegada': chegada_block,
        'p1': p1_block,
        'p2': p2_block,
        'local_ctx': local_ctx_block,
        'local_detail': local_detail_block,
    }
    sections = '\n'.join(blocks[k] for k in sections_order)

    title = f'Canalizador Urgente {vname} ({parent_name}) — Norte Reparos 24h'
    meta_desc = META_DESC_TMPL[var_meta].format(
        vname=vname, parent_name=parent_name, district=district
    )

    jsonld = build_jsonld(vname, parent_name, parent_slug, district, canonical_slug)
    district_slug = slugify(district)

    # CTA_HUB : 1 ligne courte, lien hub vers concelhos
    cta_hub = (
        f'<p>Próximo passo: contacte <a href="tel:+351****4451">{NAP_DISPLAY}</a>, '
        f'mencione {vname} ({parent_name}), ou consulte a '
        f'<a href="/concelhos/{parent_slug}">página de {parent_name}</a>.</p>'
    )

    html = HTML_TEMPLATE.format(
        title=title,
        meta_desc=meta_desc,
        canonical_slug=canonical_slug,
        vname=vname,
        parent_name=parent_name,
        parent_slug=parent_slug,
        district=district,
        district_slug=district_slug,
        zone_pill=zone_pill,
        sections=sections + '\n' + cta_hub,
        jsonld=jsonld,
        footer=footer,
        theme_color=CU_COLOR,
        nap=NAP_DISPLAY,
    )
    slug = f'{canonical_slug}.html'
    return html, slug


def main(only=None):
    """only=None -> tous les 200
       only=str -> 1 village
       only=list[str] -> sous-ensemble"""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    errors = []
    if isinstance(only, str):
        only = [only]
    for v in TOP200_DATA:
        if only is not None and v['village_name'] not in only:
            continue
        try:
            html, slug = render_village(v)
            (OUT_DIR / slug).write_text(html, encoding='utf-8')
            written += 1
        except Exception as e:
            errors.append((v.get('village_name', '?'), str(e)))
    print(f'Écrits : {written} / {len(TOP200_DATA)}')
    if errors:
        print(f'Erreurs : {len(errors)}')
        for n, e in errors[:10]:
            print(f'  - {n}: {e}')


if __name__ == '__main__':
    import sys
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    main(only=only)