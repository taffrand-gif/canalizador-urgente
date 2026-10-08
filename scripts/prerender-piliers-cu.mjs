#!/usr/bin/env node
/** Génération bornée des pages piliers urgence CU. Aucun remplacement de prose générée. */
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DOMAIN = 'https://canalizador-urgente.pt';
const PUBLIC = ROOT;
const PHONE = '+351928484451';
const DISPLAY = '+351 928 484 451';
const pages = [
  {
    file: 'canalizador-urgente-braganca.html', path: '/canalizador-urgente-braganca',
    name: 'Bragança', district: true,
    title: 'Canalizador urgente em Bragança 24h | Norte Reparos',
    description: 'Urgência de canalização em Bragança: fuga de água, entupimento, rotura e esgoto. Disponibilidade 24h/7d. 70 €/hora + 30 € de deslocação de dia; 100 €/hora + 50 € à noite, fins de semana e feriados.',
    intro: 'Para uma fuga, entupimento, rotura ou retorno de esgoto no distrito de Bragança, ligue para confirmar disponibilidade, tipo de intervenção e preço antes da deslocação.',
    local: 'Ponto de orientação para Bragança e concelhos próximos. Indique a localidade, os sintomas e se existe risco de inundação para encaminharmos a urgência correta.',
    areas: ['Bragança', 'Macedo de Cavaleiros', 'Mirandela', 'Vinhais', 'Vila Flor', 'Mogadouro', 'Miranda do Douro'],
    urgent: 'Fugas ativas, sanita ou ralo entupido, retorno de esgoto, rotura visível e fossa ou caixa exterior sem escoamento.'
  },
  {
    file: 'canalizador-urgente-macedo-de-cavaleiros.html', path: '/canalizador-urgente-macedo-de-cavaleiros',
    name: 'Macedo de Cavaleiros',
    title: 'Canalizador urgente em Macedo de Cavaleiros 24h | Norte Reparos',
    description: 'Canalizador urgente em Macedo de Cavaleiros: fuga, entupimento, rotura ou esgoto. Disponibilidade 24h/7d. Preço comunicado antes da deslocação: 70 €/hora + 30 € de dia; 100 €/hora + 50 € à noite e fins de semana.',
    intro: 'Se há água a subir, esgoto a voltar ou um cano partido em Macedo de Cavaleiros, ligue agora. Confirmamos disponibilidade, âmbito e preço antes de sair.',
    local: 'Atendemos a sede e localidades do concelho mediante confirmação por telefone. Diga se o problema está numa casa, apartamento, comércio, fossa ou caixa exterior.',
    areas: ['Macedo de Cavaleiros', 'Morais', 'Lagoa', 'Talhinhas', 'Salsas', 'Macedo do Mato', 'Grijó de Parada', 'Podence'],
    urgent: 'Retorno de esgoto, ralos lentos em vários pontos, sanita entupida, fuga ativa, rotura e fossa sem vazão.'
  },
  {
    file: 'canalizador-urgente-mirandela.html', path: '/canalizador-urgente-mirandela',
    name: 'Mirandela',
    title: 'Canalizador urgente em Mirandela 24h | Norte Reparos',
    description: 'Urgência de canalização em Mirandela: fuga de água, entupimento, rotura e esgoto. Disponibilidade 24h/7d. 70 €/hora + 30 € de dia; 100 €/hora + 50 € à noite, fins de semana e feriados.',
    intro: 'Em Mirandela, descreva o sintoma e a localidade por telefone ou WhatsApp. Confirmamos a disponibilidade e o preço aplicável antes da deslocação.',
    local: 'A página cobre Mirandela e localidades do concelho mediante confirmação. Em caso de retorno de esgoto ou risco de inundação, feche a água quando for seguro e ligue.',
    areas: ['Mirandela', 'Torre de Dona Chama', 'Aguieiras', 'Alvites', 'Carvalhais', 'Mascarenhas', 'Múrias', 'Vale de Gouvinhas', 'Vale de Salgueiro'],
    urgent: 'Fuga ativa, rotura, retorno de esgoto, entupimento de sanita ou cozinha e fossa ou caixa exterior sem escoamento.'
  }
];
function esc(v) { return v.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
function tracking() {
  const seed = execFileSync('git', ['show', 'HEAD:canalizador-urgente-braganca.html'], { cwd: ROOT, encoding: 'utf8' });
  const scripts = seed.match(/<script\b[^>]*>[\s\S]*?<\/script>/gi) || [];
  return scripts.filter(s => !/application\/ld\+json/i.test(s) && /data-rgpd-marker|googletagmanager|G-65XLQV88LM/.test(s)).join('\n');
}
function schema(p) { return JSON.stringify({'@context':'https://schema.org','@graph':[
  {'@type':'WebSite','@id':`${DOMAIN}/#website`,url:`${DOMAIN}/`,name:'Norte Reparos'},
  {'@type':'Organization','@id':`${DOMAIN}/#organization`,name:'Norte Reparos',url:`${DOMAIN}/`,contactPoint:{'@type':'ContactPoint',telephone:PHONE,contactType:'customer service',areaServed:'PT'},sameAs:['https://canalizador-norte-reparos.pt','https://eletricista-norte-reparos.pt','https://eletricista-urgente.pt']},
  {'@type':'Service','@id':`${DOMAIN}${p.path}#service`,name:`Canalizador urgente em ${p.name}`,serviceType:'Canalização de urgência',provider:{'@id':`${DOMAIN}/#organization`},areaServed:{'@type':p.district?'AdministrativeArea':'City',name:p.name},availableChannel:{'@type':'ServiceChannel',servicePhone:{'@type':'ContactPoint',telephone:PHONE,contactType:'customer service'}}},
  {'@type':'FAQPage',mainEntity:[
    {'@type':'Question',name:`Quanto custa a urgência em ${p.name}?`,acceptedAnswer:{'@type':'Answer',text:'Em dias úteis entre as 09:00 e as 17:00: 70 €/hora e 30 € de deslocação. À noite, fins de semana e feriados: 100 €/hora e 50 € de deslocação. Casos fora do padrão ficam sob orçamento, comunicado antes da intervenção.'}},
    {'@type':'Question',name:'Atendem 24h/7d?',acceptedAnswer:{'@type':'Answer',text:'Existe disponibilidade telefónica 24h/7d; a saída é confirmada conforme a situação operacional e a localidade. Não prometemos um tempo de chegada sem confirmação.'}},
    {'@type':'Question',name:'O que devo fazer enquanto aguardo?',acceptedAnswer:{'@type':'Answer',text:'Feche a água quando for seguro, não use soda cáustica ou ácido e explique por telefone quantos pontos estão afetados.'}}
  ]}
]}); }
function render(p, t) {
 const areas=p.areas.map(a=>`<li>${esc(a)}</li>`).join('');
 return `<!doctype html><html lang="pt-PT"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(p.title)}</title><meta name="description" content="${esc(p.description)}"><meta name="robots" content="index,follow"><link rel="canonical" href="${DOMAIN}${p.path}"><meta property="og:title" content="${esc(p.title)}"><meta property="og:description" content="${esc(p.description)}"><meta property="og:url" content="${DOMAIN}${p.path}"><script type="application/ld+json">${schema(p)}</script>${t}</head><body><header><nav><a href="${DOMAIN}/">Norte Reparos</a><a href="tel:${PHONE}">${DISPLAY}</a><a href="https://wa.me/351928484451">WhatsApp</a></nav></header><main><p class="breadcrumb"><a href="${DOMAIN}/">Início</a> / ${esc(p.name)}</p><section class="hero"><p class="eyebrow">URGÊNCIA DE CANALIZAÇÃO · DISPONIBILIDADE 24H/7D</p><h1>Canalizador urgente em ${esc(p.name)}</h1><p>${esc(p.intro)}</p><p><a class="cta phone" href="tel:${PHONE}">Ligar ${DISPLAY}</a><a class="cta whatsapp" href="https://wa.me/351928484451">Enviar WhatsApp</a></p><small>Disponibilidade e preço confirmados antes da deslocação.</small></section><section class="card"><h2>Quando ligar</h2><p>${esc(p.urgent)}</p><p>Se houver retorno de esgoto ou risco de inundação, feche a água quando for seguro e não use produtos corrosivos.</p></section><section class="card"><h2>Preço comunicado antes da deslocação</h2><table><thead><tr><th>Período</th><th>Mão de obra</th><th>Deslocação</th></tr></thead><tbody><tr><td>Dias úteis, 09:00–18:00</td><td>70 €/hora</td><td>30 €</td></tr><tr><td>Noite, fins de semana e feriados</td><td>100 €/hora</td><td>50 €</td></tr></tbody></table><p>O preço final de casos fora do padrão, fossas, raízes ou acesso difícil é explicado antes de avançar.</p></section><section class="card"><h2>Localidades de referência</h2><p>Indique a freguesia ou localidade ao ligar:</p><ul>${areas}</ul></section><section class="card"><h2>Como pedir ajuda</h2><ol><li>Ligue ou envie WhatsApp.</li><li>Explique o sintoma, a localidade e os pontos afetados.</li><li>Confirmamos disponibilidade, âmbito e preço antes da deslocação.</li><li>No local, explicamos o diagnóstico antes de qualquer trabalho adicional.</li></ol></section><section class="card"><h2>Perguntas frequentes</h2><h3>Atendem 24h/7d?</h3><p>Existe disponibilidade telefónica 24h/7d. A saída é confirmada conforme a situação operacional e a localidade; não prometemos um tempo de chegada sem confirmação.</p><h3>Quanto custa?</h3><p>De dia, 70 €/hora e 30 € de deslocação. À noite, fins de semana e feriados, 100 €/hora e 50 € de deslocação. Casos fora do padrão são orçamentados antes de avançar.</p><h3>Que serviço está couvert?</h3><p>Esta página é exclusivamente de canalização urgente: fuga, entupimento, rotura e esgoto.</p></section><section class="cta-bottom"><h2>Precisa de um canalizador agora?</h2><p>Confirme a zona, o sintoma e o preço por telefone.</p><a class="cta phone" href="tel:${PHONE}">Ligar ${DISPLAY}</a><a class="cta whatsapp" href="https://wa.me/351928484451">WhatsApp</a></section></main><footer><p>Norte Reparos — Canalização urgente</p><p><a href="tel:${PHONE}">${DISPLAY}</a> · <a href="https://wa.me/351928484451">WhatsApp</a></p></footer><style>body{margin:0;font:16px/1.6 system-ui,Arial,sans-serif;background:#f5f6f8;color:#20252b}header{background:#222;color:#fff;padding:1rem}header nav{max-width:980px;margin:auto;display:flex;gap:1rem;justify-content:space-between;flex-wrap:wrap}header a{color:#fff;font-weight:700;text-decoration:none}.breadcrumb,main{max-width:980px;margin:auto}.breadcrumb{padding:1rem}.hero{background:#9f2d2d;color:#fff;padding:2.5rem 1rem;text-align:center}.hero h1{font-size:clamp(2rem,5vw,3.2rem);line-height:1.1}.eyebrow{font-weight:800;letter-spacing:.04em}.cta{display:inline-block;border-radius:8px;padding:.8rem 1rem;margin:.25rem;text-decoration:none;font-weight:800}.phone{background:#fff;color:#8b2424}.whatsapp{background:#25d366;color:#062d16}.card,.cta-bottom{max-width:920px;margin:1rem auto;padding:1.25rem;background:#fff;border-radius:12px;box-shadow:0 2px 10px #0001}.cta-bottom{background:#9f2d2d;color:#fff;text-align:center}.cta-bottom .phone{color:#8b2424}table{width:100%;border-collapse:collapse}th,td{border:1px solid #d9dde2;padding:.7rem;text-align:left}th{background:#f0f2f4}footer{text-align:center;background:#222;color:#fff;padding:2rem 1rem;margin-top:2rem}footer a{color:#fff}@media(max-width:640px){header nav{flex-direction:column;align-items:center}.card{margin:.75rem;padding:1rem}}</style></body></html>`;
}
const t=tracking(); for (const p of pages) { fs.writeFileSync(path.join(PUBLIC,p.file),render(p,t)+'\n'); console.log(`WROTE ${p.path}`); }
