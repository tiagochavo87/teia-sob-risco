/**
 * Teia Sob Risco — recebe as respostas do questionário Antes e depois (versão 7º ano)
 * e grava numa planilha do Google Drive do professor.
 *
 * Como publicar (uma vez):
 *  1. script.google.com → Novo projeto → cole este arquivo.
 *  2. Execute a função configurar() e autorize. Ela cria a planilha
 *     "Teia Sob Risco – Respostas do questionário" no seu Drive (abas Respostas e Resumo).
 *  3. Implantar → Nova implantação → App da Web; Executar como: Eu; Quem pode acessar: Qualquer pessoa.
 *  4. Copie o URL do app da web (termina em /exec) e abra o simulador com ele no endereço:
 *     .../7ano.html?planilha=URL_DO_APP  (sem o parâmetro, nada é enviado).
 *
 * O link só recebe respostas: quem abre o endereço não vê nenhum dado da planilha.
 */

const NOME_PLANILHA = 'Teia Sob Risco – Respostas do questionário';
// versão curta do Apêndice A: Q1–Q5 conhecimento (3 alternativas) + Q6 atitude (1 a 4)
const GABARITO = ['b', 'c', 'a', 'b', 'c'];
const N_ATITUDE = 1;
const L = 'abcd';
const CAB = ['Recebido em', 'ID', 'Data', 'Hora', 'Fase', 'Código', 'Nível', 'Acertos (de ' + GABARITO.length + ')']
  .concat(GABARITO.map((_, i) => 'Q' + (i + 1)))
  .concat(Array.from({ length: N_ATITUDE }, (_, i) => 'Q' + (GABARITO.length + i + 1) + ' (1 a 4)'))
  .concat(['C1 (aprendeu)', 'C2 (dificuldade)']);

/** Rode uma vez: cria a planilha e guarda o ID. Rodar de novo só mostra o link. */
function configurar() {
  const props = PropertiesService.getScriptProperties();
  let id = props.getProperty('PLANILHA_ID');
  if (!id) {
    const ss = SpreadsheetApp.create(NOME_PLANILHA);
    const sh = ss.getSheets()[0];
    sh.setName('Respostas');
    sh.appendRow(CAB);
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, CAB.length).setFontWeight('bold').setBackground('#d9e7e4');
    montarResumo_(ss);
    id = ss.getId();
    props.setProperty('PLANILHA_ID', id);
  }
  Logger.log('Planilha: https://docs.google.com/spreadsheets/d/' + id);
}

/** Aba Resumo: percentual de acerto por pergunta, Antes x Depois, e média de acertos. */
function montarResumo_(ss) {
  const r = ss.insertSheet('Resumo');
  r.getRange('A1:E1').setValues([['Pergunta', 'Resposta certa', 'Acerto no Antes', 'Acerto no Depois', 'Diferença']])
    .setFontWeight('bold').setBackground('#d9e7e4');
  // planilha em português usa ";" como separador de argumentos; em inglês, ","
  const sep = /^en/.test(ss.getSpreadsheetLocale()) ? ',' : ';';
  const f = x => x.replace(/,/g, sep);
  GABARITO.forEach((g, i) => {
    const col = colLetra_(9 + i); // Q1 está na coluna I
    const lin = i + 2;
    r.getRange(lin, 1, 1, 2).setValues([['Q' + (i + 1), g]]);
    r.getRange(lin, 3, 1, 3).setFormulas([[
      f(`=IFERROR(COUNTIFS(Respostas!E:E,"Antes",Respostas!${col}:${col},B${lin})/COUNTIF(Respostas!E:E,"Antes"),"")`),
      f(`=IFERROR(COUNTIFS(Respostas!E:E,"Depois",Respostas!${col}:${col},B${lin})/COUNTIF(Respostas!E:E,"Depois"),"")`),
      f(`=IF(OR(C${lin}="",D${lin}=""),"",D${lin}-C${lin})`)]]);
  });
  r.getRange('C2:E11').setNumberFormat('0%');
  r.getRange('A13:A15').setValues([['Respostas no Antes'], ['Respostas no Depois'], ['Média de acertos no Antes']]);
  r.getRange('A16').setValue('Média de acertos no Depois');
  r.getRange('B13:B16').setFormulas([
    [f('=COUNTIF(Respostas!E:E,"Antes")')],
    [f('=COUNTIF(Respostas!E:E,"Depois")')],
    [f('=IFERROR(AVERAGEIF(Respostas!E:E,"Antes",Respostas!H:H),"")')],
    [f('=IFERROR(AVERAGEIF(Respostas!E:E,"Depois",Respostas!H:H),"")')]]);
  r.getRange('B15:B16').setNumberFormat('0.0');
  r.getRange('A13:A16').setFontWeight('bold');
  r.autoResizeColumns(1, 5);
}

/** Refaz a aba Resumo (use se ela for apagada ou mostrar erro). */
function refazerResumo() {
  const ss = planilha_().getParent();
  const velha = ss.getSheetByName('Resumo');
  if (velha) ss.deleteSheet(velha);
  montarResumo_(ss);
}

/** Reescreve o cabeçalho da aba Respostas (depois de mudar o questionário) e refaz o Resumo. */
function ajustarCabecalho() {
  const sh = planilha_();
  const ult = sh.getLastColumn();
  if (ult > CAB.length) sh.getRange(1, CAB.length + 1, sh.getMaxRows(), ult - CAB.length).clearContent().clearFormat();
  sh.getRange(1, 1, 1, CAB.length).setValues([CAB]).setFontWeight('bold').setBackground('#d9e7e4');
  refazerResumo();
}

/** Apaga as linhas de teste (código TESTE) da aba Respostas. */
function limparTestes() {
  const sh = planilha_();
  const n = sh.getLastRow() - 1;
  if (n < 1) return;
  const cod = sh.getRange(2, 6, n, 1).getValues();
  for (let i = n - 1; i >= 0; i--) if (cod[i][0] === 'TESTE') sh.deleteRow(i + 2);
}

function colLetra_(n) { let s = ''; while (n > 0) { const m = (n - 1) % 26; s = String.fromCharCode(65 + m) + s; n = Math.floor((n - 1) / 26); } return s; }

function planilha_() {
  const id = PropertiesService.getScriptProperties().getProperty('PLANILHA_ID');
  if (!id) throw new Error('Rode configurar() antes de publicar.');
  return SpreadsheetApp.openById(id).getSheetByName('Respostas');
}

/** Texto seguro para célula: corta o tamanho e impede que vire fórmula. */
function txt_(v, max) {
  let s = String(v == null ? '' : v).slice(0, max);
  if (/^[=+\-@]/.test(s)) s = "'" + s;
  return s;
}

function saida_(msg) { return ContentService.createTextOutput(msg).setMimeType(ContentService.MimeType.TEXT); }

function doPost(e) {
  let r;
  try { r = JSON.parse(e.postData.contents); } catch (err) { return saida_('erro: corpo inválido'); }
  if (!r || typeof r.id !== 'string' || !/^[a-z0-9]{6,24}$/.test(r.id)) return saida_('erro: id');
  if (r.fase !== 'antes' && r.fase !== 'depois') return saida_('erro: fase');
  const a = Array.isArray(r.a) ? r.a : [], b = Array.isArray(r.b) ? r.b : [], c = Array.isArray(r.c) ? r.c : [];
  const letras = GABARITO.map((_, i) => (Number.isInteger(a[i]) && a[i] >= 0 && a[i] < 3) ? L[a[i]] : '');
  const acertos = letras.reduce((s, x, i) => s + (x === GABARITO[i] ? 1 : 0), 0); // recalculado aqui, não confia no aparelho
  const escala = Array.from({ length: N_ATITUDE }, (_, i) => (Number.isInteger(b[i]) && b[i] >= 1 && b[i] <= 4) ? b[i] : '');
  const abertas = [0, 1].map(i => txt_(c[i], 400));

  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const sh = planilha_();
    const n = sh.getLastRow() - 1;
    if (n > 0) {
      const ids = sh.getRange(2, 2, n, 1).getValues().map(x => x[0]);
      if (ids.indexOf(r.id) >= 0) return saida_('ok: já recebida'); // reenvio da fila
    }
    sh.appendRow([new Date(), r.id, txt_(r.d, 10), txt_(r.h, 5), r.fase === 'depois' ? 'Depois' : 'Antes',
      txt_(r.cod, 10), r.nivel === '7' ? '7º ano' : 'Ensino Médio', acertos]
      .concat(letras, escala, abertas));
  } finally {
    lock.releaseLock();
  }
  return saida_('ok');
}

function doGet() { return saida_('Teia Sob Risco: este endereço só recebe respostas do questionário.'); }
