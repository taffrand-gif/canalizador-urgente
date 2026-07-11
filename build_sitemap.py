#!/usr/bin/env python3
"""
Génère public/sitemap.xml (et sitemap.xml racine) pour canalizador-urgente.pt.

Cible : inclure les pages money/service SERVIE et INDEXABLES :
- 33 piliers info (sans noindex, sans _archive)
- 77 urgentes money (≥18KB = top villes avec contenu)
- 77 desentupimento money (qualité gold, ≥18KB)
- 539 services money (7 services × 77 villes, ≥18KB)
- 33 concelhos/
- 6 distritos/
- 27 blog/ (html)

Exclut :
- 3 fichiers noindex (glossario-eletricidade, guia-eletricidade, top-10-razoes-contratar-eletricista)
- 166 doublons md5 (versions avec diacritiques)
- _archive/*
- Pages <18KB (boilerplates courts)

Format URL : https://canalizador-urgente.pt/<slug> (sans .html, conforme canonical)
"""
import os, re, hashlib, sys
from collections import defaultdict
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_URL = 'https://canalizador-urgente.pt'
TODAY = date.today().isoformat()  # 2026-07-11
SIZE_THRESHOLD = 18000

NOINDEX_PAGES = {
    'glossario-eletricidade.html',
    'guia-eletricidade.html',
    'top-10-razoes-contratar-eletricista.html',
}

SERVICE_PREFIXES = (
    'autoclismo-', 'fuga-agua-', 'fossa-septica-', 'esquentador-',
    'canalizacao-nova-', 'canalizacao-', 'torneira-', 'pressao-agua-',
)


def has_diacritics(s):
    return bool(re.search(r'[áéíóúàâêôãõçÁÉÍÓÚÀÂÊÔÃÕÇ]', s))


def collect_html_files(directory):
    """Liste tous les .html d'un dossier (non récursif)."""
    out = []
    for f in os.listdir(directory):
        full = os.path.join(directory, f)
        if os.path.isfile(full) and f.endswith('.html'):
            out.append(f)
    return out


def dedup_md5(files, root_dir):
    """Dédup par md5, garde la version sans diacritiques (préférée pour URL)."""
    md5_groups = defaultdict(list)
    for f in files:
        full = os.path.join(root_dir, f)
        with open(full, 'rb') as fp:
            data = fp.read()
        h = hashlib.md5(data).hexdigest()
        md5_groups[h].append(f)
    keep = set()
    for h, lst in md5_groups.items():
        sorted_lst = sorted(lst, key=lambda x: (has_diacritics(x), x))
        keep.add(sorted_lst[0])
    return keep


def categorize(unique_files, root_dir):
    """Catégorise les fichiers .html en (pilier, urgente, desentupimento, service, ville_seule, noindex)."""
    pillars = set()
    urgentes = set()
    desents = set()
    services = set()
    ville_seule = set()
    noindex = set()

    for f in unique_files:
        if f in NOINDEX_PAGES:
            noindex.add(f)
            continue
        if not f.startswith('canalizador-'):
            # pages info piliers (contactos, precos, sobre, etc.)
            pillars.add(f)
            continue
        if f == 'index.html':
            pillars.add(f)
            continue
        if f.startswith('canalizador-desentupimento-'):
            desents.add(f)
            continue
        if f.startswith('canalizador-urgente-'):
            urgentes.add(f)
            continue
        is_service = False
        for sp in SERVICE_PREFIXES:
            if f.startswith(f'canalizador-{sp}'):
                services.add(f)
                is_service = True
                break
        if is_service:
            continue
        ville_seule.add(f)

    return pillars, urgentes, desents, services, ville_seule, noindex


def file_to_url(f):
    """Convertit un nom de fichier en URL canonique (sans .html)."""
    slug = f[:-5]  # retire .html
    return f'{BASE_URL}/{slug}'


def build_sitemap_xml(urls_with_priority):
    """Génère le XML sitemap.0.9 formaté avec lastmod et priority."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url, priority in urls_with_priority:
        lines.append(f'<url><loc>{url}</loc><lastmod>{TODAY}</lastmod><priority>{priority}</priority></url>')
    lines.append('</urlset>')
    lines.append('')
    return '\n'.join(lines)


def main():
    # 1) Racine
    root_files = collect_html_files(ROOT)
    unique_root = dedup_md5(root_files, ROOT)
    pillars, urgentes_all, desents_all, services_all, ville_seule, noindex = categorize(unique_root, ROOT)

    # 2) Filtre money : seuil 18KB
    def by_size(file_set):
        return {f for f in file_set if os.path.getsize(os.path.join(ROOT, f)) >= SIZE_THRESHOLD}

    urgentes_money = by_size(urgentes_all)
    desents_money = by_size(desents_all)
    services_money = by_size(services_all)

    # 3) Sous-dossiers
    concelhos_dir = os.path.join(ROOT, 'concelhos')
    distritos_dir = os.path.join(ROOT, 'distritos')
    blog_dir = os.path.join(ROOT, 'blog')

    concelhos = sorted(os.listdir(concelhos_dir))
    distritos = sorted(os.listdir(distritos_dir))
    blog_html = sorted([f for f in os.listdir(blog_dir) if f.endswith('.html')])

    # 4) Construction de la liste ordonnée
    urls = []  # (url, priority)

    # Piliers : index = 1.0, autres = 0.7
    for f in sorted(pillars):
        url = file_to_url(f) if f != 'index.html' else f'{BASE_URL}/'
        priority = '1.0' if f == 'index.html' else '0.7'
        urls.append((url, priority))

    # Concelhos : 0.8
    for f in concelhos:
        slug = f[:-5]  # .html
        urls.append((f'{BASE_URL}/concelhos/{slug}', '0.8'))

    # Distritos : 0.7
    for f in distritos:
        slug = f[:-5]
        urls.append((f'{BASE_URL}/distritos/{slug}', '0.7'))

    # Blog : 0.6
    for f in blog_html:
        slug = f[:-5]
        urls.append((f'{BASE_URL}/blog/{slug}', '0.6'))

    # Urgentes money : 0.9 (pages gold)
    for f in sorted(urgentes_money):
        urls.append((file_to_url(f), '0.9'))

    # Desentupimento money : 0.9 (gold)
    for f in sorted(desents_money):
        urls.append((file_to_url(f), '0.9'))

    # Services money : 0.8
    for f in sorted(services_money):
        urls.append((file_to_url(f), '0.8'))

    # Stats
    print(f"=== INVENTAIRE FINAL ===")
    print(f"  Piliers info        : {len(pillars)}")
    print(f"  Urgentes money      : {len(urgentes_money)} (sur {len(urgentes_all)} total)")
    print(f"  Desentupimento money: {len(desents_money)} (sur {len(desents_all)} total)")
    print(f"  Service money       : {len(services_money)} (sur {len(services_all)} total)")
    print(f"  Concelhos           : {len(concelhos)}")
    print(f"  Distritos           : {len(distritos)}")
    print(f"  Blog (html)         : {len(blog_html)}")
    print(f"  TOTAL URLs sitemap  : {len(urls)}")
    print(f"  Exclus noindex      : {len(noindex)}")
    print(f"  Exclus <18KB urgente: {len(urgentes_all) - len(urgentes_money)}")
    print(f"  Exclus ville_seule  : {len(ville_seule)} (doublon avec urgente/service)")

    # 5) Génération XML
    xml = build_sitemap_xml(urls)

    # 6) Écriture : sitemap.xml (racine) ET public/sitemap.xml
    out_paths = [
        os.path.join(ROOT, 'sitemap.xml'),
        os.path.join(ROOT, 'public', 'sitemap.xml'),
    ]
    for p in out_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8') as fp:
            fp.write(xml)
        print(f"  Written: {p}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
