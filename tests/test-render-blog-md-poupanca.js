// Garde : une économie chiffrée en fourchette (« Poupança: 40-65 € ») est un prix professionnel implicite non sourcé.
const assert = require('assert');
const { auditConformity } = require('../scripts/render-blog-md.js');
const labels = (s) => auditConformity(s).map((f) => f.label);
for (const bad of ['**Poupança:** 40-65€', 'Poupança face ao profissional: 40-65 €', 'trocar vedante poupa cerca de 40-65 €']) {
  assert.ok(labels(bad).includes('poupança chiffrée'), 'non refusé : ' + bad);
}
for (const ok of ['Poupança: a deslocação e a primeira hora de um profissional.', 'vedante novo (2-5 €)', 'excepto quando a poupança é grande (acima de 200 €)']) {
  assert.ok(!labels(ok).includes('poupança chiffrée'), 'refusé à tort : ' + ok);
}
console.log('ok');
