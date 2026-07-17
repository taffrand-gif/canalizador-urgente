#!/usr/bin/env python3
"""
p1_hub_render_v2 — Réinjection des blocs P1 Variante A SANS le paragraphe halluciné
("ferro galvanizado"), avec zone+prix corrigés depuis data/concelhos.json (post-fix
fix/data-zones-tomtom).

Usage : python3 .hermes-p1-hub-prototype/p1_hub_render_v2.py
"""

import json, os, re, shutil
from pathlib import Path

REPO = Path('/Users/admin/work/Sites/canalizador-urgente')
concelhos = json.load(open(REPO / 'data' / 'concelhos.json'))
locs = json.load(open(REPO / 'data' / 'localidades.json'))

village_pages = sorted(f for f in os.listdir(REPO)
                       if f.startswith('canalizador-') and f.endswith('.html')
                       and not f.startswith('canalizador-desentupimento'))


def find_village_page(name):
    n = name.lower()
    simple = (n.replace(' ', '-').replace("'", '')
              .replace('ã','a').replace('ç','c').replace('é','e').replace('ê','e')
              .replace('á','a').replace('í','i').replace('ó','o').replace('ô','o').replace('ú','u'))
    cand = f'canalizador-{simple}.html'
    if (REPO / cand).exists():
        return cand
    name_lower = name.lower().replace(' ', '-')
    for f in village_pages:
        if name_lower in f:
            return f
    return None


def get_village_links(slug, n=6):
    if slug not in locs:
        return []
    vl = []
    for v in locs[slug]:
        fn = find_village_page(v['name'])
        if fn and len(vl) < n:
            vl.append((v['name'], fn))
    return vl


ZONE_CTX = {
    1: "Z1 — base de operações, deslocação mínima",
    2: "Z2 — concelho próximo, deslocação curta",
    3: "Z3 — percurso intermédio",
    4: "Z4 — área de montanha, acesso por vezes lento",
    5: "Z5 — distância grande, orçamento dedicado",
    6: "Z6 — área distante, orçamento específico",
}


def render_p1_v3(c, village_links):
    """Sans adjectif régional inventé. Tout dérivé des champs réels uniquement."""
    slug = c['slug']
    name = c['name']
    district = c['district']
    route_km = c.get('route_km')
    zone = c.get('zone')
    price_desloc = c.get('price', {}).get('desloc') if c.get('price') else None
    indexable = c.get('indexable', False)
    village_count = len(locs.get(slug, []))
    village_names = [v['name'] for v in locs.get(slug, [])]
    route_km_str = "0 km (base de operações)" if route_km is None or route_km == 0 else f"{route_km:g} km"
    my_desloc = price_desloc if price_desloc is not None else 15

    pilier = f'canalizador-desentupimento-{slug}'
    pilier_label = f'Desentupimento em {name}'

    price_block = f'''<div class="price-transparency">
<p><strong>Transparência tarifária — Canalizador</strong></p>
<p>Aplicável em {name} ({ZONE_CTX.get(zone, f"Z{zone}")}):</p>
<ul style="margin:.6rem 0 0 1.2rem;line-height:1.7">
<li><strong>65 €/h</strong> — mão de obra canalizador (tarifa horária).</li>
<li>Deslocação Z{zone} = <strong>{my_desloc} €</strong>.</li>
<li>Demais zonas: Z1 = 15 € · Z2 = 25 € · Z3 = 35 € · Z4 = 45 € · Z5 = 55 € · Z6 = 65 €.</li>
<li>Noite (20h–7h), fim de semana e feriado: <strong>+50 %</strong>.</li>
<li><strong>Orçamento por escrito antes de qualquer intervenção</strong>, sem surpresas.</li>
</ul>
</div>'''

    village_links_html = '\n'.join(
        [f'   <li><a href="/{fn[:-5]}">{n}</a></li>' for n, fn in village_links]
    )

    if route_km is None or route_km == 0:
        context_phrase = f"a base operacional fica no próprio centro de {name} (distância 0 km) e cobre as {village_count} localidades listadas na base atual"
    else:
        context_phrase = f"a base operacional fica a {route_km_str} do centro de {name} e cobre as {village_count} localidades listadas na base atual"

    villages_listed = ', '.join(village_names[:15])
    last_villages = ', '.join(village_names[15:30]) if len(village_names) > 15 else ''
    extra = max(0, len(village_names) - 30)

    specific = f'''<p>Em {name} ({district}), {context_phrase}. A ficha rodoviária regista este valor como dado da rota {district} → {name} — não é uma promessa de tempo. A lista atual inclui {villages_listed}{', ' + last_villages if last_villages else ''}{f' (e outras {extra} entradas não detalhadas aqui)' if extra > 0 else ''}.</p>'''

    if not indexable:
        specific += f'\n<p><em>Cobertura:</em> {name} aparece na base sem distância rodoviária validada; mantemos a página honesta até confirmação por fonte TomTom ou equivalente.</p>'

    bloc = f'''<section class="p1-diferenciacao p1-hub-concelho" data-p1-slug="{slug}">
 <h2>Canalizador em {name}: informação clara antes do contacto</h2>
{specific}
{price_block}
 <p>Explicamos o diagnóstico e o trabalho necessário antes de qualquer intervenção. Utilizamos equipamento profissional — entre outros, máquina Ridgid K9-102 para desobstrução mecânica, câmara de inspeção 30 m e deteção acústica ROLeak Aqua 3Plus para localizar fugas sem destruir paredes. Não apresentamos moradas privadas, testemunhos, obras ou pontos comerciais que não estejam confirmados por uma fonte pública.</p>
 <p>O nosso padrão de fala é direto: a nossa equipa, e não um call center — fala sempre com a mesma pessoa. Contacte-nos pelo <strong>+351 928 484 451</strong> para descrever os sintomas em {name}. Respondemos com linguagem simples, preço transparente e fatura com NIF, seguro de responsabilidade civil e garantia escrita.</p>
 <nav aria-label="Ligação local — {name}">
  <p><strong>Localidades próximas (maillage interno):</strong></p>
  <ul style="columns:2;column-gap:1rem;padding-left:1.2rem;line-height:1.6">
{village_links_html}
  </ul>
  <p style="margin-top:.6rem"><strong>Página serviço connexa:</strong> <a href="/{pilier}">{pilier_label}</a>.</p>
 </nav>
</section>
<!-- /p1-diferenciacao -->'''
    return bloc


def re_inject(slug):
    """Remplace l'éventuel bloc P1 existant par le nouveau (idempotent)."""
    hub_path = REPO / 'concelhos' / f'{slug}.html'
    if not hub_path.exists():
        return None, 'NO_HUB'

    c = next(c for c in concelhos if c['slug'] == slug)
    village_links = get_village_links(slug)
    bloc = render_p1_v3(c, village_links)
    html = hub_path.read_text(encoding='utf-8')

    # 1. Retirer tout bloc P1 existant (du précédent batch ou du fix)
    pattern_old = re.compile(
        r'<section class="p1-diferenciacao p1-hub-concelho".*?</section>\s*<!--\s*/p1-diferenciacao\s*-->\s*',
        re.S,
    )
    html_clean = pattern_old.sub('', html)

    # 2. Aussi supprimer le paragraphe halluciné (au cas où)
    pattern_hallu = re.compile(
        r'<p>O contexto regional[^<]*gel[^<]*\.</p>\s*',
        re.S,
    )
    html_clean = pattern_hallu.sub('', html_clean)

    # 3. Réinjecter le nouveau bloc après </div> qui ferme info-box, avant <h2>
    pattern_inj = re.compile(r'(<div class="info-box">.*?</div>)(\s*<h2)', re.S | re.M)
    new_html, n_sub = pattern_inj.subn(r'\1\n\n' + bloc + r'\n\n\2', html_clean, count=1)
    if n_sub == 0:
        return None, 'NO_INJECT_PATTERN'

    hub_path.write_text(new_html, encoding='utf-8')
    return new_html, 'OK'


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--slug', default=None, help='Si fourni, traiter uniquement ce slug')
    ap.add_argument('--backup-dir', default='_archive-p1-fix-2026-07-16')
    args = ap.parse_args()

    backup_dir = REPO / args.backup_dir
    backup_dir.mkdir(exist_ok=True)

    slugs = [args.slug] if args.slug else sorted(c['slug'] for c in concelhos if c.get('indexable'))
    ok = 0
    fail = []
    for s in slugs:
        hub = REPO / 'concelhos' / f'{s}.html'
        if hub.exists():
            shutil.copy2(hub, backup_dir / f'{s}.html.PRE-fix')
        result, status = re_inject(s)
        if status == 'OK':
            ok += 1
        else:
            fail.append((s, status))

    print(f"=== p1_hub_render_v2 ===")
    print(f"OK: {ok}/{len(slugs)}")
    for s, e in fail:
        print(f"  ❌ {s}: {e}")
