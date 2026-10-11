#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""refonte_v2_canalizador.py — WAVE-2 CU : refonte 5 sections data-driven + variantes linguistiques.

Inspiré du pattern EU (commit f6aef43d sur eletricista-urgente).
Adapté vocabulaire canalização (Ridgid K9-102 — seul équipement plomberie confirmé, décision Filipe 2026-10-10).
Sections refondues : info-box (Z + prix), paragraphe intro, services list, FAQ, "Sobre" block.

Stratégie V2 (variation linguistique) :
  - 4 VARIANTES par section (transp, intro, servicos, faq, sobre)
  - Choix variante = hash(slug) modulo len(variantes) → déterministe + dispersé
  - Chaque variante utilise des synonymes et tournures différentes, pas juste name/rkm
  - District context (VISEU/GUARDA: 'serra da Estrela' etc.) — JAMAIS d'invention sur habitat/climat

Contraintes (R11/R12/SPEC §1/§5) :
  - Tarif verrouillé (_governance/20-BUSINESS-FACTS.json) : 70 €/h + 30 € (09h–18h) ; 100 €/h + 50 € (nuit/week-end/férié), TTC, heure commencée due
  - Pas d'invention : pas de "ferro galvanizado" non vérifié, pas de "construções antigas" non source
  - Équipement confirmé : Ridgid K9-102 uniquement (ni ROLeak, ni caméra 30 m, ni FLIR/Fluke : électricité = ENR/EU)

Usage :
  python3 scripts/p1/refonte_v2_canalizador.py --slug macedo-de-cavaleiros --dry-run
  python3 scripts/p1/refonte_v2_canalizador.py --slug macedo-de-cavaleiros --apply
  python3 scripts/p1/refonte_v2_canalizador.py --all --apply
"""
import argparse, json, re, sys, unicodedata, hashlib, shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]

TELEPHONE = '+351 928 484 451'
CANAL_RATE = 70
CANAL_STR = '70 €/h'
MAJORATION = '100 €/h + deslocação 50 € à noite, fins de semana e feriados'

ZONE_TABLE = [(9999, 1, 30)]


def norm(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return s.lower()


def grille(km):
    if km is None:
        return None, None
    for sup, z, p in ZONE_TABLE:
        if km < sup:
            return z, p
    return None, None


def pick(slug, options):
    if not options:
        return ''
    h = int(hashlib.sha1(slug.encode()).hexdigest(), 16)
    return options[h % len(options)]


def district_context_cu(district):
    """Contexte géographique public, vérifiable selon district — JAMAIS d'invention locale.
    On donne UNIQUEMENT des éléments qui sont des connaissances publiques évidentes
    (district existe, pas de 'construções antigas' inventé)."""
    if district == 'Bragança':
        return ('terras transmontanas', 'planalto')
    elif district == 'Vila Real':
        return ('terras do Douro', 'encostas')
    elif district == 'Viseu':
        return ('terras do Viseu', 'encosta beirã')
    elif district == 'Guarda':
        return ('terras da Guarda', 'planalto beirão')
    return ('interior norte', 'encosta')


# === VARIANTES INFO-BOX (remplace Zone + prix dans <div class="info-box"> initial) ===

INFOBOX_TEMPLATES = [
    # V0 — sobre, direct
    '''<div class="info-box">
 <p><strong>Concelho:</strong> {name}</p>
 <p><strong>Distrito:</strong> {district}</p>
 <p><strong>Distância desde Macedo de Cavaleiros:</strong> {rkm} km por estrada</p>
 <p><strong>Deslocação:</strong> 30 € em dias úteis (9h–18h) e 50 € à noite, fins de semana e feriados</p>
</div>''',
    # V1 — focus zone contexte
    '''<div class="info-box">
 <p><strong>Concelho:</strong> {name}</p>
 <p><strong>Distrito:</strong> {district}</p>
 <p><strong>Distância desde Macedo de Cavaleiros:</strong> {rkm} km por estrada</p>
 <p><strong>Deslocação:</strong> 30 € em dias úteis (9h–18h) e 50 € à noite, fins de semana e feriados</p>
</div>''',
    # V2 — focus tableau
    '''<div class="info-box">
 <p><strong>Local:</strong> {name} ({district})</p>
 <p><strong>Distância operacional:</strong> {rkm} km (estrada municipal + nacional)</p>
 <p><strong>Deslocação:</strong> 30 € em dias úteis (9h–18h) e 50 € à noite, fins de semana e feriados</p>
 <p style="font-size:.85rem;color:#666;margin-top:.5rem">A deslocação é um forfait único por horário.</p>
</div>''',
    # V3 (NO_ROUTE) — Moimenta
    '''<div class="info-box">
 <p><strong>Concelho:</strong> {name}</p>
 <p><strong>Distrito:</strong> {district}</p>
 <p><strong>Cobertura:</strong> confirmada por telefone</p>
 <p><strong>Deslocação:</strong> 30 € em dias úteis (9h–18h) e 50 € à noite, fins de semana e feriados</p>
</div>''',
]


def render_infobox(c, slug):
    name = c['name']
    district = c['district']
    rkm = c.get('route_km')

    if rkm is None:
        t = INFOBOX_TEMPLATES[3]
        return t.format(name=name, district=district)

    rkm_str = f'{rkm:g}'
    t = pick(slug, INFOBOX_TEMPLATES[:3])
    return t.format(name=name, district=district, rkm=rkm_str)


# === VARIANTES PARAGRAPHE INTRO ===

INTRO_TEMPLATES = [
    '''<p>A {rkm} km de Macedo de Cavaleiros (base operacional Norte Reparos). Deslocamo-nos a todo o concelho de {name}.</p>''',
    '''<p>Distância operacional {rkm} km por estrada desde a base em Macedo de Cavaleiros. Cobertura completa do concelho de {name}.</p>''',
    '''<p>Localizado a {rkm} km de Macedo de Cavaleiros, o concelho de {name} é servido a partir da nossa base operacional transmontana.</p>''',
    '''<p>O concelho de {name} ({district}) dista {rkm} km por estrada da nossa base em Macedo de Cavaleiros. Operamos em todo o perímetro administrativo.</p>''',
    # V4 — base operacional (route_km=0)
    '''<p>{name} é a nossa base operacional em Trás-os-Montes. A partir daqui servimos todo o perímetro administrativo do concelho.</p>''',
    # V5 NO_ROUTE
    '''<p>Cobertura mediante contacto telefónico para o concelho de {name}.</p>''',
]


def render_intro(c, slug):
    name = c['name']
    district = c['district']
    rkm = c.get('route_km')
    if rkm is None:
        t = INTRO_TEMPLATES[5]
        return t.format(name=name)
    if rkm == 0:
        t = INTRO_TEMPLATES[4]
        return t.format(name=name)
    rkm_str = f'{rkm:g}'
    t = pick(slug, INTRO_TEMPLATES[:4])
    return t.format(name=name, rkm=rkm_str, district=district)


# === VARIANTES SERVIÇOS (refonte ul) ===

SERVICOS_TEMPLATES = [
    # V0 — défaut (liste canonique)
    '''<h2>Serviços de canalizador em {name}</h2>
 <ul>
 <li>Desentupimentos de canos, esgotos e ralos</li>
 <li>Fugas de água: diagnóstico prévio e reparação</li>
 <li>Autoclismos, torneiras e misturadoras</li>
 <li>Esquentadores, termoacumuladores e caldeiras</li>
 <li>Substituição de tubagens e canalização</li>
 <li>Urgência 24h em todo o concelho de {name}</li>
 </ul>''',
    # V1 — focus equipamento
    '''<h2>Serviços de canalizador em {name}</h2>
 <ul>
 <li>Desentupimentos mecânicos com máquina Ridgid K9-102</li>
 <li>Diagnóstico prévio de fugas e reparação localizada</li>
 <li>Reparação e substituição de autoclismos, torneiras, misturadoras</li>
 <li>Esquentadores, termoacumuladores, caldeiras — diagnóstico e reparação</li>
 <li>Substituição total ou parcial de tubagens</li>
 <li>Resposta urgente 24h por dia, 7 dias por semana, em {name} e arredores</li>
 </ul>''',
    # V2 — focus síntomas típicos
    '''<h2>O que intervencionamos em {name}</h2>
 <ul>
 <li>«Cano entupido» — desentupimento mecânico profissional</li>
 <li>«Fuga de água sem ver onde» — diagnóstico prévio no local</li>
 <li>«Autoclismo não para» — substituição mecanismo ou caixa completa</li>
 <li>«Esquentador avariado» — diagnóstico e reparação</li>
 <li>«Pressão de água fraca» — inspeção da rede interna</li>
 <li>«Cheiro a gás/esgoto» — deteção e isolamento</li>
 <li>«Inundação» — resposta urgente 24h em {name}</li>
 </ul>''',
    # V3 — focus contexte aldeias
    '''<h2>Cobertura técnica em {name}</h2>
 <ul>
 <li>Desentupimento por máquina mecânica (Ridgid K9-102)</li>
 <li>Diagnóstico prévio de fugas e reparação localizada</li>
 <li>Reparação de autoclismo, torneira ou misturadora</li>
 <li>Diagnóstico e reparação de esquentador / termoacumulador</li>
 <li>Renovação de canalização em PVC, cobre ou PEX</li>
 <li>Urgência fora-de-horas em todo o perímetro de {name} ({n_villages} aldeias)</li>
 </ul>''',
]


def render_servicos(c, slug, loc_data):
    name = c['name']
    n_villages = len(loc_data.get(slug, []))
    t = pick(slug, SERVICOS_TEMPLATES)
    return t.format(name=name, n_villages=n_villages)


# === VARIANTES FAQ ===

FAQ_TEMPLATES = [
    # V0 — défaut perguntas habituais
    '''<h2>Perguntas frequentes — Canalizador em {name}</h2>
 <p><strong>Quanto custa a deslocação a {name}?</strong><br>{preco_phrase}</p>
 <p style="margin-top:1rem"><strong>Quanto tempo demora a chegar?</strong><br>{chegar}</p>
 <p style="margin-top:1rem"><strong>Atendem de noite, fins de semana e feriados?</strong><br>Sim, 24h por dia, 7 dias por semana. Majoração {majo} anunciada antes.</p>
 <p style="margin-top:1rem"><strong>Emitem fatura?</strong><br>Sim, fatura detalhada com NIF e garantia escrita.</p>
 <p style="margin-top:1rem"><strong>Quantas aldeias servem no concelho de {name}?</strong><br>{aldeias}</p>''',
    # V1 — focus confiança
    '''<h2>Dúvidas frequentes — Canalizador em {name}</h2>
 <p><strong>Quanto custa em {name}?</strong><br>{preco_phrase}</p>
 <p style="margin-top:1rem"><strong>Como sei que o orçamento é justo?</strong><br>Publicamos a tabela tarifária no início da página; o orçamento por escrito nunca muda após acordo.</p>
 <p style="margin-top:1rem"><strong>Chegam rápido a {name}?</strong><br>{chegar}</p>
 <p style="margin-top:1rem"><strong>Fazem orçamento antes de trabalhar?</strong><br>Sim — orçamento por escrito antes de qualquer intervenção.</p>
 <p style="margin-top:1rem"><strong>Equipamento profissional em {name}?</strong><br>Ridgid K9-102 (desentupimento mecânico).</p>''',
    # V2 — focus pratique
    '''<h2>FAQ Canalizador urgente {name}</h2>
 <p><strong>Quanto vou pagar pela deslocação em {name}?</strong><br>{preco_phrase}</p>
 <p style="margin-top:1rem"><strong>Trabalham à noite e ao fim de semana?</strong><br>Sim, 24h/7d incluindo feriados. Majoração {majo} anunciada com antecedência.</p>
 <p style="margin-top:1rem"><strong>Quanto tempo até chegar?</strong><br>{chegar}</p>
 <p style="margin-top:1rem"><strong>Pago deslocação mesmo sem trabalho?</strong><br>Sim — a deslocação é fixa, anunciada antes. Se houver trabalho, é integrada no orçamento.</p>
 <p style="margin-top:1rem"><strong>Fatura discriminada?</strong><br>Sim, mão-de-obra + deslocação + peças detalhadas, NIF incluído.</p>''',
    # V3 — focus transparência
    '''<h2>Transparência e perguntas — {name}</h2>
 <p><strong>Tarifa publicada para {name}?</strong><br>{preco_phrase}</p>
 <p style="margin-top:1rem"><strong>Há orçamento antes de intervir?</strong><br>Sim, orçamento por escrito antes de qualquer intervenção. A deslocação é faturada sempre que há deslocação.</p>
 <p style="margin-top:1rem"><strong>Qual é a janela de chegada em {name}?</strong><br>{chegar}</p>
 <p style="margin-top:1rem"><strong>Como localizam uma fuga?</strong><br>Diagnóstico prévio no local; quando necessário, abertura pontual limitada ao estritamente necessário.</p>
 <p style="margin-top:1rem"><strong>Cobertura no concelho?</strong><br>{aldeias}</p>''',
]


def render_faq(c, slug, loc_data):
    name = c['name']
    rkm = c.get('route_km')
    rmin = c.get('route_min')
    n_villages = len(loc_data.get(slug, []))

    if rkm is None:
        preco_phrase = 'Dias úteis (09h–18h): 70 €/h + 30 € de deslocação; noite, fins de semana e feriados: 100 €/h + 50 €. Montantes TTC; orçamento por escrito antes de qualquer intervenção.'
        chegar = 'A janela de chegada é confirmada por telefone antes da deslocação.'
    elif rkm == 0:
        preco_phrase = 'Dias úteis (09h–18h): 70 €/h + 30 € de deslocação; noite, fins de semana e feriados: 100 €/h + 50 €. Montantes TTC; orçamento por escrito antes de qualquer intervenção.'
        chegar = 'A janela de atendimento é confirmada por telefone conforme a disponibilidade operacional.'
    else:
        preco_phrase = f'A deslocação custa 30 € em dias úteis (9h–18h) e 50 € à noite, fins de semana e feriados; o orçamento é apresentado por escrito.'
        if rmin is not None:
            chegar = 'A janela de atendimento é confirmada por telefone conforme a disponibilidade operacional.'
        else:
            chegar = f'A distância operacional é de {rkm:g} km por estrada; a janela exata é confirmada por telefone antes da deslocação.'

    if n_villages == 0:
        aldeias = f'A base não publica lista de aldeias nesta versão; confirmamos a distância exata por telefone antes do orçamento.'
    else:
        aldeias = f'Base cobre {n_villages} aldeias listadas para o concelho de {name}.'

    t = pick(slug, FAQ_TEMPLATES)
    return t.format(name=name, preco_phrase=preco_phrase, chegar=chegar,
                    aldeias=aldeias, majo=MAJORATION)


# === VARIANTES BLOC PREÇOS (remplace l'<h2>Preços em X</h2><div class="info-box">) ===

PRECOS_BLOCK_TEMPLATES = [
    # V0 — défaut
    '''<h2>Preços em {name}</h2>
 <div class="info-box">
 <p><strong>Deslocação:</strong> 30 € em dias úteis e 50 € à noite, fins de semana e feriados</p>
 <p><strong>Dias úteis, 1h + deslocação:</strong> {h1} € TTC</p>
 <p><strong>Dias úteis, 2h + deslocação:</strong> {h2} € TTC</p>
 <p style="font-size:.85rem;color:#666;margin-top:.8rem">70 €/h em dias úteis (9h–18h) + deslocação 30 €. À noite, fins de semana e feriados: 100 €/h + deslocação 50 €. Cada hora começada é devida.</p>
 </div>''',
    # V1 — focus zone
    '''<h2>Preços em {name}</h2>
 <div class="info-box">
 <p><strong>Deslocação:</strong> 30 € em dias úteis; 50 € à noite, fins de semana e feriados</p>
 <p><strong>Tarifa horária:</strong> 70 €/h em dias úteis; 100 €/h à noite, fins de semana e feriados.</p>
 <p><strong>Deslocação:</strong> 30 € em horário útil; 50 € à noite, fins de semana e feriados.</p>
 <p style="font-size:.85rem;color:#666;margin-top:.8rem">Orçamento escrito comunicado antes da deslocação</p>
 </div>''',
    # V2 — focus tableaux
    '''<h2>Tabela de preços em {name}</h2>
 <div class="info-box">
 <table style="width:100%;border-collapse:collapse">
 <tr><td><strong>Deslocação</strong></td><td>30 € / 50 €</td></tr>
 <tr><td><strong>Mão de obra em horário útil</strong></td><td>70 €/h</td></tr>
 <tr><td><strong>Noite, fim de semana e feriado</strong></td><td>100 €/h + 50 €</td></tr>
 <tr><td><strong>Deslocação em horário útil</strong></td><td>30 €</td></tr>
 </table>
 <p style="font-size:.85rem;color:#666;margin-top:.8rem">Montantes TTC. Cada hora começada é devida.</p>
 </div>''',
    # V3 NO_ROUTE
    '''<h2>Preços em {name}</h2>
 <div class="info-box">
 <p><strong>Deslocação:</strong> 30 € em dias úteis e 50 € à noite, fins de semana e feriados</p>
 <p><strong>Mão de obra:</strong> 70 €/h em horário útil; 100 €/h à noite, fins de semana e feriados</p>
 <p><strong>Cada hora começada:</strong> é devida</p>
 <p style="font-size:.85rem;color:#666;margin-top:.8rem">70 €/h em horário útil + deslocação 30 €; 100 €/h + deslocação 50 € à noite, fins de semana e feriados · Orçamento por escrito</p>
 </div>''',
]


# Mapping grille Filipe pour h1/h2 — par défaut h1=80, h2=145 (Macedo Z1)
# H1/H2 = 70 €/h × heures + 30 € de déplacement (dias úteis), TTC
H1_BASE = 100   # 1ʳᵉ heure (base)
H2_BASE = 170  # 2h cumul


def render_precos_block(c, slug):
    name = c['name']
    rkm = c.get('route_km')

    if rkm is None:
        t = PRECOS_BLOCK_TEMPLATES[3]
        return t.format(name=name, h1=H1_BASE, h2=H2_BASE)

    t = pick(slug, PRECOS_BLOCK_TEMPLATES[:3])
    return t.format(name=name, h1=H1_BASE, h2=H2_BASE)


# === VARIANTES SOBRE (Equipe / fonte) — ne pas toucher canonical ===

SOBRE_TEMPLATES = [
    '''<h2>Sobre a Norte Reparos</h2>
 <p>A Norte Reparos é uma equipa de canalizadores com base em Macedo de Cavaleiros, ao serviço do concelho de {name} e da região transmontana. Diagnóstico por telefone em poucos minutos — ligue {tel}, garantimos atenção mediante confirmação por telefone 24 horas por dia, 7 dias por semana, incluindo fins de semana e feriados. Fatura com NIF e garantia sobre os trabalhos realizados.</p>''',
    '''<h2>Quem somos</h2>
 <p>Norte Reparos opera a partir de Macedo de Cavaleiros, cobrindo {name} e a região circundante. Contacto directo por telefone — {tel} — com marcação após confirmação. Fatura com NIF discriminada, garantia escrita sobre mão-de-obra e peças, seguro de responsabilidade civil.</p>''',
    '''<h2>A nossa equipa</h2>
 <p>Base operacional em Macedo de Cavaleiros, a Norte Reparos é uma PME profissional de canalização ao serviço de {name}. Resposta 24h por dia, 7 dias por semana, mediante confirmação por telefone ao {tel}. Documentos: fatura com NIF, garantia escrita, seguro RC.</p>''',
    '''<h2>Quem atende {name}</h2>
 <p>A Norte Reparos, equipa de canalizadores profissional com base em Macedo de Cavaleiros, cobre {name} e toda a região transmontana. Chamada directa ao {tel}, garantia de resposta mediante confirmação por telefone 24/7 (incluindo feriados). Fatura NIF, garantia escrita, seguro responsabilidade civil.</p>''',
]


def render_sobre(c, slug):
    name = c['name']
    t = pick(slug, SOBRE_TEMPLATES)
    return t.format(name=name, tel=TELEPHONE)


# === APPLICATION ===

def apply_section(html, section_html, anchor_open_re, anchor_close_re=None):
    """Remplace la zone correspondant à anchor_open_re (+ éventuelle extension) par section_html.

    Comportement:
    - Si anchor_close_re est None, le pattern complet est juste anchor_open_re (substitution directe).
    - Si anchor_close_re est fourni, on étend avec r'.*?' + anchor_close_re uniquement si anchor_open_re
      ne se termine PAS déjà par anchor_close_re (évite double fermeture qui mange trop).
    """
    if anchor_close_re is None:
        pat_re = anchor_open_re
    elif anchor_close_re in anchor_open_re:
        # anchor_close_re est déjà inclus dans anchor_open_re, ne pas l'ajouter
        pat_re = anchor_open_re
    else:
        pat_re = anchor_open_re + r'.*?' + anchor_close_re
    pat = re.compile(pat_re, flags=re.S)
    new_html, n = pat.subn(lambda m: section_html, html, count=1)
    if n != 1:
        return html, False
    return new_html, True


def apply_refonte(target_path, c, loc_data):
    """Refonte 5 sections pré-existantes SANS toucher bloc P1 Variante A."""
    html = Path(target_path).read_text()
    orig_len = len(html)
    applied = []

    # (a) Info-box initiale (1ʳᵉ <div class="info-box">) — pattern complet incluant </div>
    infobox = render_infobox(c, c['slug'])
    new_html, ok = apply_section(html, infobox,
        r'<div class="info-box">\s*<p><strong>Concelho:</strong>.*?</p>\s*<p><strong>Distrito:</strong>.*?</p>\s*<p><strong>Distância desde.*?</p>\s*<p><strong>Zona tarifária:.*?</p>\s*</div>',
    )  # anchor_close_re=None → pattern entier
    if ok:
        applied.append('infobox'); html = new_html

    # (b) Paragraphe intro ("A X km de Macedo...")
    intro = render_intro(c, c['slug'])
    new_html, ok = apply_section(html, intro,
        r'<p>A\s+\d+\s*km[^<]*Macedo[^<]*</p>',
        r'</p>')
    if not ok:
        # Variante "Distância operacional X km..."
        new_html, ok = apply_section(html, intro,
            r'<p>Distância operacional\s+\d+\s*km[^<]*</p>',
            r'</p>')
    if ok:
        applied.append('intro'); html = new_html

    # (c) Serviços (h2 + ul) — NE PAS toucher si ça a "Serviços de canalizador"
    servicos = render_servicos(c, c['slug'], loc_data)
    # On touche "Serviços de canalizador em X" et "O que intervencionamos em X" et "Cobertura técnica em X"
    new_html, ok = apply_section(html, servicos,
        r'<h2[^>]*>(?:Serviços de canalizador|O que intervencionamos|Casos habituais|Cobertura técnica)[^<]*</h2>\s*<ul[^>]*>.*?</ul>',
        r'</ul>')
    if ok:
        applied.append('servicos'); html = new_html

    # (d) Preços (h2 + info-box)
    precos = render_precos_block(c, c['slug'])
    new_html, ok = apply_section(html, precos,
        r'<h2[^>]*>Preços em[^<]*</h2>\s*<div class="info-box">.*?</div>',
        r'</div>')
    if ok:
        applied.append('precos'); html = new_html

    # (e) FAQ (h2 + p)
    faq = render_faq(c, c['slug'], loc_data)
    new_html, ok = apply_section(html, faq,
        r'<h2[^>]*>Perguntas frequentes[^<]*</h2>(.*?)(?:<div class="cta"|<h2[^>]*>Veja também)',
        r'(?:<div class="cta"|<h2[^>]*>Veja também)')
    if ok:
        applied.append('faq'); html = new_html

    # (f) Sobre la Norte Reparos (h2 + p, entre </ul> et <h2>Perguntas)
    # Plus sûr : cibler le h2 Sobre/Quem/Equipa suivi d'1 p
    sobre = render_sobre(c, c['slug'])
    new_html, ok = apply_section(html, sobre,
        r'<h2[^>]*>(?:Sobre a Norte Reparos|Quem somos|A nossa equipa|Quem atende)[^<]*</h2>\s*<p>[^<]*</p>',
        r'</p>')
    if ok:
        applied.append('sobre'); html = new_html

    if applied:
        Path(target_path).write_text(html)

    return applied, len(html) - orig_len


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--slug', default='macedo-de-cavaleiros')
    p.add_argument('--all', action='store_true')
    p.add_argument('--apply', action='store_true')
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()

    concelhos = json.load(open(REPO / 'data' / 'concelhos.json'))
    loc = json.load(open(REPO / 'data' / 'localidades.json'))

    if args.dry_run and not args.apply:
        slug = args.slug
        c = next((x for x in concelhos if x['slug'] == slug), None)
        if not c:
            sys.exit(f"slug {slug} introuvable")
        print(f"--- DRY-RUN {slug} ---\n")
        print(f"## INFOBOX:\n{render_infobox(c, slug)}\n")
        print(f"## INTRO:\n{render_intro(c, slug)}\n")
        print(f"## SERVIÇOS:\n{render_servicos(c, slug, loc)}\n")
        print(f"## PREÇOS:\n{render_precos_block(c, slug)}\n")
        print(f"## FAQ:\n{render_faq(c, slug, loc)}\n")
        print(f"## SOBRE:\n{render_sobre(c, slug)}\n")
        return

    targets = [c['slug'] for c in concelhos] if args.all else [args.slug]
    summary = []
    for slug in targets:
        c = next((x for x in concelhos if x['slug'] == slug), None)
        if not c:
            print(f"  SKIP {slug}: not in concelhos.json")
            continue
        target = REPO / 'concelhos' / f'{slug}.html'
        if not target.exists():
            print(f"  SKIP {slug}: no file")
            continue
        applied, delta = apply_refonte(target, c, loc)
        summary.append((slug, applied, delta))
        print(f"  {slug:30s} | applied: {applied} | Δlen: {delta:+d}")
    print(f"\n=== REFONTE V2 on {len(summary)} files ===")


if __name__ == '__main__':
    main()
