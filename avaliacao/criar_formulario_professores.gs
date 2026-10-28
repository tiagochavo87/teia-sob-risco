/**
 * Teia Sob Risco — formulário anônimo de avaliação pelos professores (Fase 1 da proposta pedagógica).
 *
 * Como usar:
 *   1. Abra script.google.com > Novo projeto, apague o conteúdo e cole este arquivo inteiro.
 *   2. Escolha a função criarFormulario e clique em Executar. Autorize o acesso ao Forms e ao Planilhas.
 *   3. Em Execução > Registro aparecem: o link para os professores, o link de edição e a planilha de respostas.
 *   4. Depois das respostas, execute calcularResultados: ele cria a aba "Resultados" na planilha,
 *      com IVC por item, avaliação por partes da plataforma e pontuação SUS.
 *
 * O formulário não coleta e-mail, não exige login e não limita a uma resposta (o limite exigiria login).
 */

const LINK_SIMULADOR = 'https://tiagochavo87.github.io/teia-sob-risco/?nivel=7';

const PARTES = [
  ['Cena do estuário e fichas', 'Toque nos organismos e leia as fichas.'],
  ['Parâmetros e liberação', 'Escolha poluente, cenário e intensidade e clique em Liberar poluente.'],
  ['Remediação e exposição no tempo', 'Mova a remediação da fonte e use Reproduzir na exposição ao longo do tempo.'],
  ['Leituras e gráficos', 'Leia as leituras (Mais contaminado, Sobe a teia?, No ser humano, Pescados acima do limite) e os dois gráficos.'],
  ['Roteiro de aula guiada', 'Clique em Roteiro de aula e percorra os 5 passos.'],
  ['Montar a teia', 'Descubra ligações com as pistas ligadas e depois desligadas.'],
  ['Quiz', 'Responda às 5 perguntas e corrija.'],
  ['Comparador e tabela de dados', 'Fixe os cenários A e B e abra a Tabela de dados.'],
  ['Catálogo de espécies', 'Na aba Catálogo, filtre por nível e abra algumas fichas.'],
  ['Questionário Antes e depois', 'Responda como aluno (Antes e Depois) e abra a Área da professora.'],
  ['Painel do professor e exportações', 'Registre um resultado e exporte o CSV.'],
  ['Acessibilidade', 'Teste Contraste, A+ (fonte ampliada) e a narração em áudio.'],
];
const CRITERIOS_PARTE = ['Facilidade de uso', 'Clareza das informações', 'Contribuição para a aprendizagem', 'Adequação ao 7º ano'];

// Escala de Usabilidade de Sistema, versão brasileira (Lourenço, Carmona e Lopes, 2022)
const SUS = [
  'Eu acho que gostaria de usar esse sistema frequentemente.',
  'Eu achei esse sistema desnecessariamente complexo.',
  'Eu achei esse sistema fácil de usar.',
  'Eu achei que precisaria de ajuda de uma pessoa técnica para ser capaz de usar esse sistema.',
  'Eu achei que as várias funções desse sistema foram bem integradas.',
  'Eu acho que o sistema apresenta muita inconsistência.',
  'Eu imagino que a maioria das pessoas pode aprender a usar esse sistema rapidamente.',
  'Eu achei esse sistema muito pesado para usar.',
  'Eu me senti muito seguro usando o sistema.',
  'Eu precisei aprender muitas coisas antes que pudesse utilizar esse sistema.',
];
const TITULO_SUS = 'SUS — usabilidade geral';

// Questionário Antes e depois (Apêndice A da proposta); c = índice da alternativa correta
const ITENS_A = [
  { q: 'No manguezal, qual destes seres produz o próprio alimento usando a luz do Sol?', o: ['Caranguejo-uçá', 'Fitoplâncton', 'Tainha', 'Garça-branca-grande'], c: 1 },
  { q: 'Qual frase mostra corretamente quem come quem?', o: ['O fitoplâncton come o zooplâncton, que come a sardinha, que come o boto-cinza.', 'O boto-cinza come o fitoplâncton, e a sardinha come o boto-cinza.', 'O zooplâncton come o fitoplâncton, a sardinha come o zooplâncton e o boto-cinza come a sardinha.', 'O zooplâncton come a sardinha, e o fitoplâncton come o boto-cinza.'], c: 2 },
  { q: 'Uma fábrica lança mercúrio na água do estuário. Depois de algum tempo, em qual destes animais deve haver MAIS mercúrio no corpo?', o: ['Zooplâncton', 'Ostra', 'Tainha', 'Boto-cinza'], c: 3 },
  { q: 'O boto-cinza não bebe a água poluída. Por que ele acaba com mais mercúrio que a sardinha?', o: ['Porque come muitos peixes que já têm mercúrio, e o mercúrio vai se acumulando no corpo dele.', 'Porque mergulha mais fundo, onde a água tem muito mais mercúrio.', 'Porque o mercúrio é atraído pelos animais maiores e mais pesados.', 'Porque vive mais perto da fábrica que lança o mercúrio.'], c: 0 },
  { q: 'Agora o poluente é microplástico. Quais animais ficam com MAIS partículas no corpo?', o: ['Os predadores do topo da teia, como o boto-cinza e a toninha.', 'Os que filtram a água para se alimentar, como a ostra e o mexilhão.', 'As árvores do mangue, que ficam na beira da água.', 'As aves que mergulham para pescar, como o biguá.'], c: 1 },
  { q: 'Qual frase explica a diferença entre o mercúrio e o microplástico na teia alimentar?', o: ['Os dois aumentam a cada elo da teia e ficam maiores no boto-cinza.', 'O microplástico aumenta a cada elo da teia; o mercúrio fica só na água.', 'Nenhum dos dois chega aos animais, porque ficam no fundo do estuário.', 'O mercúrio aumenta a cada elo da teia; o microplástico se concentra em quem filtra a água.'], c: 3 },
  { q: 'Qual é o principal caminho pelo qual o mercúrio lançado no estuário chega até as pessoas?', o: ['Nadando na água poluída do estuário.', 'Respirando o ar perto do mar.', 'Comendo peixes e frutos do mar contaminados.', 'Ele não chega, porque o mar dilui tudo.'], c: 2 },
  { q: 'Qual medida diminui a contaminação de TODA a teia alimentar?', o: ['Tratar o esgoto e os resíduos das fábricas antes que cheguem à água.', 'Pescar só os peixes grandes, que são os mais contaminados.', 'Retirar as ostras e os mexilhões do manguezal.', 'Impedir que as aves comam os peixes do estuário.'], c: 0 },
  { q: 'Para que serve um simulador de computador numa aula de Ciências?', o: ['Para substituir as pesquisas feitas no ambiente real, que são caras.', 'Para representar, de forma simplificada, como algo funciona e testar ideias.', 'Para prever o que vai acontecer no futuro, com certeza.', 'Só para jogar, sem relação com a natureza.'], c: 1 },
  { q: 'Pesquisadores mediram o mercúrio em três seres vivos: alga = 1 unidade; peixe pequeno, que come a alga = 3 unidades; peixe grande, que come o peixe pequeno = 9 unidades. O que esses números sugerem?', o: ['O mercúrio diminui ao subir na teia alimentar.', 'Só o peixe grande tem mercúrio no corpo.', 'O mercúrio aumenta a cada nível da teia alimentar.', 'Não dá para concluir nada com esses números.'], c: 2 },
];
const ITENS_B = [
  'Tenho vontade de aprender mais sobre o mar e os manguezais.',
  'O manguezal é importante para mim e para a minha cidade.',
  'O que vai para o esgoto pode chegar à comida que comemos.',
  'Eu consigo explicar para outra pessoa como um poluente chega até o peixe.',
  'Pretendo evitar jogar plástico em lugares errados.',
  'Pretendo conversar com minha família sobre a poluição no mar.',
];
const CRITERIOS_ITEM = ['Relevância para o objetivo', 'Clareza da redação', 'Adequação ao 7º ano'];

function criarFormulario() {
  const form = FormApp.create('Teia Sob Risco — avaliação por professores');
  form.setDescription(
    'Esta avaliação faz parte do TCC "Corrente de Aprendizagem" (Especialização em Cultura Oceânica e Sustentabilidade na Educação Básica, UFSC/UAB). ' +
    'Você vai explorar o simulador Teia Sob Risco no modo 7º ano e avaliar: (1) cada parte da plataforma, (2) a usabilidade geral e ' +
    '(3) os itens de um questionário de aprendizagem para alunos de 7º ano.\n\n' +
    'Simulador (modo 7º ano): ' + LINK_SIMULADOR + '\n\n' +
    'Tempo estimado: cerca de 30 minutos explorando o simulador e 25 minutos respondendo.\n\n' +
    'A participação é voluntária e anônima: o formulário não pede nome, e-mail nem login, e as respostas são analisadas em conjunto.');
  // configurações que mantêm o anonimato; cada uma protegida, porque nem toda conta aceita todas
  tentar_(function () { form.setCollectEmail(false); });
  tentar_(function () { form.setRequireLogin(false); });
  tentar_(function () { form.setLimitOneResponsePerUser(false); });
  tentar_(function () { form.setAllowResponseEdits(false); });
  tentar_(function () { form.setShowLinkToRespondAgain(false); });
  form.setProgressBar(true);
  form.setConfirmationMessage('Obrigado! Sua avaliação foi registrada de forma anônima.');

  // 1. Consentimento
  const consent = form.addMultipleChoiceItem().setTitle('Li as informações acima e concordo em participar.').setRequired(true);
  consent.setChoices([
    consent.createChoice('Concordo em participar', FormApp.PageNavigationType.CONTINUE),
    consent.createChoice('Não concordo', FormApp.PageNavigationType.SUBMIT),
  ]);

  // 2. Perfil, em faixas, sem dado identificador
  form.addPageBreakItem().setTitle('Perfil').setHelpText('Respostas em faixas, para que ninguém possa ser identificado.');
  form.addMultipleChoiceItem().setTitle('Em que etapa você leciona?').setChoiceValues(['Anos finais do Ensino Fundamental', 'Ensino Médio', 'As duas', 'Outra']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('Componente curricular principal').setChoiceValues(['Ciências', 'Biologia', 'Ciências e Biologia', 'Outro']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('Tempo de docência').setChoiceValues(['Até 5 anos', 'De 6 a 15 anos', 'Mais de 15 anos']).setRequired(true);

  // 3. Plataforma por partes
  form.addPageBreakItem().setTitle('Avaliação da plataforma por partes')
    .setHelpText('Abra o simulador no modo 7º ano: ' + LINK_SIMULADOR + '\nPara cada parte, dê nota de 1 (ruim) a 4 (muito bom) em cada critério, ou marque "Não usei".');
  PARTES.forEach(function (p, i) {
    form.addGridItem().setTitle((i + 1) + '. ' + p[0]).setHelpText('O que fazer: ' + p[1])
      .setRows(CRITERIOS_PARTE).setColumns(['1', '2', '3', '4', 'Não usei']).setRequired(true);
    form.addParagraphTextItem().setTitle('Comentário sobre a parte ' + (i + 1) + ' (opcional)');
  });

  // 4. Usabilidade geral (SUS)
  form.addPageBreakItem().setTitle('Usabilidade geral')
    .setHelpText('Escala de Usabilidade de Sistema, versão brasileira (Lourenço, Carmona e Lopes, 2022). Responda pensando na plataforma inteira.');
  form.addGridItem().setTitle(TITULO_SUS)
    .setRows(SUS.map(function (t, i) { return (i + 1) + '. ' + t; }))
    .setColumns(['1 — Discordo totalmente', '2', '3', '4', '5 — Concordo totalmente']).setRequired(true);

  // 5. Julgamento dos itens do questionário (IVC)
  form.addPageBreakItem().setTitle('Questionário Antes e depois — Parte 1 (conhecimento)')
    .setHelpText('Para cada pergunta, dê nota de 1 a 4 em cada critério: 1 = não, 2 = pouco, 3 = bastante, 4 = muito ' +
      '(relevante para o objetivo; clara; adequada ao 7º ano). A alternativa correta está marcada com ✓.');
  ITENS_A.forEach(function (it, i) {
    const alternativas = it.o.map(function (o, k) { return 'abcd'.charAt(k) + ') ' + o + (k === it.c ? '  ✓' : ''); }).join('\n');
    form.addGridItem().setTitle('A' + (i + 1) + '. ' + it.q).setHelpText(alternativas)
      .setRows(CRITERIOS_ITEM).setColumns(['1', '2', '3', '4']).setRequired(true);
    form.addMultipleChoiceItem().setTitle('A' + (i + 1) + ': o gabarito está correto e há uma só resposta certa?')
      .setChoiceValues(['Sim', 'Não', 'Não sei']).setRequired(true);
  });
  form.addParagraphTextItem().setTitle('Comentários sobre a Parte 1 do questionário (opcional)');

  form.addPageBreakItem().setTitle('Questionário Antes e depois — Parte 2 (interesse, atitudes e intenções)')
    .setHelpText('O aluno responde com: Discordo muito · Discordo · Concordo · Concordo muito. Avalie cada frase nos mesmos três critérios, de 1 a 4.');
  ITENS_B.forEach(function (t, i) {
    form.addGridItem().setTitle('B' + (i + 1) + '. ' + t).setRows(CRITERIOS_ITEM).setColumns(['1', '2', '3', '4']).setRequired(true);
  });
  form.addParagraphTextItem().setTitle('Comentários sobre a Parte 2 do questionário (opcional)');

  // 6. Comentário final
  form.addPageBreakItem().setTitle('Comentário final');
  form.addParagraphTextItem().setTitle('Sugestões gerais (opcional)');

  // planilha de respostas
  const ss = SpreadsheetApp.create('Teia Sob Risco — respostas dos professores');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());
  // contas novas podem criar o formulário "não publicado": publica quando a API oferece isso
  tentar_(function () { if (typeof form.setPublished === 'function') form.setPublished(true); });
  PropertiesService.getScriptProperties().setProperties({ FORM_ID: form.getId(), PLANILHA_ID: ss.getId() });

  Logger.log('Link para os professores: ' + form.getPublishedUrl());
  Logger.log('Editar o formulário: ' + form.getEditUrl());
  Logger.log('Planilha de respostas: ' + ss.getUrl());
}

/** Lê a planilha de respostas e escreve a aba "Resultados" (IVC, partes e SUS). */
function calcularResultados() {
  const id = PropertiesService.getScriptProperties().getProperty('PLANILHA_ID');
  if (!id) throw new Error('Execute criarFormulario antes.');
  const ss = SpreadsheetApp.openById(id);
  const aba = ss.getSheets().filter(function (sh) { return sh.getFormUrl(); })[0];
  if (!aba) throw new Error('A planilha ainda não tem a aba de respostas do formulário.');
  const dados = aba.getDataRange().getDisplayValues();
  const r = analisar(dados[0], dados.slice(1));
  let saida = ss.getSheetByName('Resultados');
  if (!saida) saida = ss.insertSheet('Resultados'); else saida.clear();
  const blocos = [
    [['IVC por item (proporção de notas 3 ou 4)', '', '', '', '', '', '']],
    [['Item', 'Relevância', 'Clareza', 'Adequação ao 7º ano', 'Juízes', 'Gabarito contestado', 'Decisão']].concat(r.ivc),
    [['IVC médio do questionário', r.ivcMedio.relevancia, r.ivcMedio.clareza, r.ivcMedio.adequacao, '', '', '']],
    [['', '', '', '', '', '', '']],
    [['Plataforma por partes (% de notas 3 ou 4 entre quem usou)', '', '', '', '', '', '']],
    [['Parte', 'Facilidade', 'Clareza', 'Aprendizagem', 'Adequação ao 7º ano', 'Usaram', 'Situação']].concat(r.partes),
    [['', '', '', '', '', '', '']],
    [['SUS (0 a 100)', 'Média', 'Mínimo', 'Máximo', 'Respondentes', '', ''],
     ['', r.sus.media, r.sus.min, r.sus.max, r.sus.n, '', '']],
  ];
  let linha = 1;
  blocos.forEach(function (b) { saida.getRange(linha, 1, b.length, 7).setValues(b); linha += b.length; });
  saida.autoResizeColumns(1, 7);
}

/**
 * Cálculo puro (sem Google): recebe o cabeçalho e as linhas da planilha de respostas.
 * IVC = proporção de juízes com nota 3 ou 4 (Alexandre e Coluci, 2011): mínimo 0,78 com 6 ou mais juízes;
 * com 5 ou menos, todos precisam concordar (1,00).
 */
function analisar(cab, linhas) {
  const CRIT = { 'Relevância para o objetivo': 'relevancia', 'Clareza da redação': 'clareza', 'Adequação ao 7º ano': 'adequacao' };
  const CRITP = { 'Facilidade de uso': 0, 'Clareza das informações': 1, 'Contribuição para a aprendizagem': 2, 'Adequação ao 7º ano': 3 };
  const itens = {}, partes = {}, gabarito = {}, susCols = [];
  cab.forEach(function (h, j) {
    let m = /^([AB]\d+)\. [\s\S]*\[(.+)\]$/.exec(h);
    if (m && CRIT[m[2]]) { (itens[m[1]] = itens[m[1]] || {})[CRIT[m[2]]] = j; return; }
    m = /^(A\d+): o gabarito/.exec(h);
    if (m) { gabarito[m[1]] = j; return; }
    m = /^(\d+)\. ([\s\S]*) \[(.+)\]$/.exec(h);
    if (m && CRITP[m[3]] !== undefined) { const p = (partes[m[1]] = partes[m[1]] || { nome: m[2], cols: [] }); p.cols[CRITP[m[3]]] = j; return; }
    m = new RegExp('^' + TITULO_SUS + ' \\[(\\d+)\\.').exec(h);
    if (m) susCols[Number(m[1]) - 1] = j;
  });
  const num = function (v) { const n = parseInt(String(v), 10); return isNaN(n) ? null : n; };
  const r2 = function (x) { return x == null ? '' : Math.round(x * 100) / 100; };
  const prop34 = function (j) {
    const v = linhas.map(function (l) { return num(l[j]); }).filter(function (x) { return x != null; });
    return { p: v.length ? v.filter(function (x) { return x >= 3; }).length / v.length : null, n: v.length };
  };
  const somaMedia = { relevancia: [], clareza: [], adequacao: [] };
  const ivc = Object.keys(itens).sort(ordem_).map(function (k) {
    const c = itens[k], rel = prop34(c.relevancia), cla = prop34(c.clareza), ade = prop34(c.adequacao);
    const n = Math.max(rel.n, cla.n, ade.n), corte = n >= 6 ? 0.78 : 1;
    [['relevancia', rel], ['clareza', cla], ['adequacao', ade]].forEach(function (x) { if (x[1].p != null) somaMedia[x[0]].push(x[1].p); });
    const contest = gabarito[k] === undefined ? 0 : linhas.filter(function (l) { return l[gabarito[k]] === 'Não'; }).length;
    let decisao = 'Mantém';
    if (rel.p != null && rel.p < corte) decisao = 'Excluir (relevância)';
    else if ((cla.p != null && cla.p < corte) || (ade.p != null && ade.p < corte)) decisao = 'Reescrever';
    if (contest >= 2 && decisao === 'Mantém') decisao = 'Rever alternativas';
    return [k, r2(rel.p), r2(cla.p), r2(ade.p), n, gabarito[k] === undefined ? '' : contest, decisao];
  });
  const media = function (a) { return a.length ? a.reduce(function (s, x) { return s + x; }, 0) / a.length : null; };
  const lista = Object.keys(partes).sort(function (a, b) { return a - b; }).map(function (k) {
    const p = partes[k];
    const pc = p.cols.map(function (j) { return prop34(j); });
    const usaram = Math.max.apply(null, pc.map(function (x) { return x.n; }));
    const ajustar = pc.some(function (x) { return x.p != null && x.p < 0.78; });
    return [k + '. ' + p.nome].concat(pc.map(function (x) { return x.p == null ? '' : Math.round(x.p * 100) + '%'; }), [usaram, ajustar ? 'Ajustar' : 'OK']);
  });
  const notas = linhas.map(function (l) {
    const v = susCols.map(function (j) { return num(l[j]); });
    if (v.length !== 10 || v.some(function (x) { return x == null; })) return null;
    return 2.5 * v.reduce(function (s, x, i) { return s + (i % 2 === 0 ? x - 1 : 5 - x); }, 0);
  }).filter(function (x) { return x != null; });
  return {
    ivc: ivc,
    ivcMedio: { relevancia: r2(media(somaMedia.relevancia)), clareza: r2(media(somaMedia.clareza)), adequacao: r2(media(somaMedia.adequacao)) },
    partes: lista,
    sus: { n: notas.length, media: r2(media(notas)), min: notas.length ? Math.min.apply(null, notas) : '', max: notas.length ? Math.max.apply(null, notas) : '' },
  };
}

function ordem_(a, b) { return a.charAt(0) === b.charAt(0) ? Number(a.slice(1)) - Number(b.slice(1)) : (a < b ? -1 : 1); }
function tentar_(f) { try { f(); } catch (e) { Logger.log('Aviso: ' + e.message); } }
