"""Gera o Manual do Professor do Teia Sob Risco em PDF (A4).

Uso:  python3 manual/gerar_manual.py
Saída: Manual_do_Professor_Teia_Sob_Risco_v6.pdf na raiz do repositório.
Requer: reportlab (pip install reportlab).

O texto do manual fica todo neste arquivo, em CONTEUDO: para atualizar o manual,
edite o texto e rode o script de novo. O sumário é calculado sozinho (duas passagens),
então os números de página sempre batem.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
                                TableStyle, KeepTogether, PageBreak, NextPageTemplate, CondPageBreak)

VERSAO = '6.3'
DATA = 'outubro de 2026'
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, 'Manual_do_Professor_Teia_Sob_Risco_v6.pdf')

# ---------- paleta (a mesma do app) ----------
ABYSS = HexColor('#082A31'); COVER = HexColor('#0A2C32'); W3 = HexColor('#0C3A44'); W2 = HexColor('#155A63')
TIDE = HexColor('#2BB3A3'); INK = HexColor('#11201E'); MUTED = HexColor('#56625E'); LINE = HexColor('#D7E0DB')
PANEL2 = HexColor('#F2F6F3'); HAZ1 = HexColor('#E0902F'); WARN = HexColor('#9C1F12')
TL = [HexColor(c) for c in ('#6E9A3C', '#2E8C9B', '#1C6470', '#2B5C86', '#6E3B7E')]

PW, PH = A4
ML, MR, MT, MB = 56, 56, 74, 62
LARG = PW - ML - MR

# ---------- estilos ----------
corpo = ParagraphStyle('corpo', fontName='Helvetica', fontSize=9.5, leading=14.2, textColor=INK,
                       alignment=TA_JUSTIFY, spaceAfter=6, allowWidows=0)
corpo_esq = ParagraphStyle('corpo_esq', parent=corpo, alignment=TA_LEFT)
h1 = ParagraphStyle('h1', fontName='Times-Bold', fontSize=20, leading=24, textColor=W3, spaceBefore=12, spaceAfter=7, keepWithNext=1)
h2 = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=W2, spaceBefore=9, spaceAfter=4, keepWithNext=1)
faq_q = ParagraphStyle('faq_q', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=W2, spaceBefore=6, spaceAfter=1)
bullet = ParagraphStyle('bullet', parent=corpo_esq, leftIndent=13, bulletIndent=2, bulletFontName='Helvetica-Bold',
                        bulletFontSize=9, bulletColor=TIDE, spaceAfter=4)
cel = ParagraphStyle('cel', fontName='Helvetica', fontSize=8.3, leading=11.5, textColor=INK)
cel_b = ParagraphStyle('cel_b', parent=cel, fontName='Helvetica-Bold')
cel_h = ParagraphStyle('cel_h', parent=cel, fontName='Helvetica-Bold', textColor=white)
cel_hl = ParagraphStyle('cel_hl', parent=cel, fontName='Helvetica-Bold', textColor=W3)
call = ParagraphStyle('call', parent=corpo_esq, fontSize=9, leading=13, spaceAfter=0)
eq = ParagraphStyle('eq', fontName='Courier', fontSize=8.2, leading=11.5, textColor=W3)
ref = ParagraphStyle('ref', parent=corpo_esq, fontSize=8.6, leading=12, spaceAfter=4)
fecho = ParagraphStyle('fecho', parent=corpo_esq, fontName='Helvetica-Oblique', fontSize=8.2, leading=11.5, textColor=MUTED)
toc_n = ParagraphStyle('toc_n', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=W2)
toc_t = ParagraphStyle('toc_t', fontName='Helvetica', fontSize=9.5, leading=13, textColor=INK)
toc_p = ParagraphStyle('toc_p', fontName='Helvetica', fontSize=9, leading=13, textColor=MUTED, alignment=2)


# ---------- blocos ----------
class Titulo(Paragraph):
    """Título de seção que registra a própria página para o sumário."""
    def __init__(self, num, texto):
        self.num, self.texto_toc = num, texto
        super().__init__(f'{num} · {texto}', h1)


def P(t, s=corpo): return Paragraph(t, s)
def B(itens): return [Paragraph(t, bullet, bulletText='•') for t in itens]


def H1(num, texto): return [CondPageBreak(170), Titulo(num, texto)]


def H2(t): return Paragraph(t, h2)


def caixa(texto, cor=TIDE):
    t = Table([[Paragraph(texto, call)]], colWidths=[LARG])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), PANEL2), ('BOX', (0, 0), (-1, -1), .5, LINE),
                           ('LINEBEFORE', (0, 0), (0, -1), 3, cor), ('LEFTPADDING', (0, 0), (-1, -1), 11),
                           ('RIGHTPADDING', (0, 0), (-1, -1), 10), ('TOPPADDING', (0, 0), (-1, -1), 8),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 9)]))
    t.spaceBefore, t.spaceAfter = 4, 8  # Table (não KeepTogether): assim o título anterior consegue ficar junto
    return t


def passos(itens):
    dados = [[Paragraph(str(i), ParagraphStyle('n', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=TIDE)),
              Paragraph(t, corpo_esq)] for i, t in enumerate(itens, 1)]
    t = Table(dados, colWidths=[18, LARG - 18])
    t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                           ('RIGHTPADDING', (0, 0), (-1, -1), 0), ('TOPPADDING', (0, 0), (-1, -1), 1),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 1)]))
    return t


def tabela(cab, linhas, larg, escuro=False, primeira_negrito=False):
    hs = cel_h if escuro else cel_hl
    dados = [[Paragraph(c, hs) for c in cab]] + [
        [Paragraph(c, cel_b if (primeira_negrito and j == 0) else cel) for j, c in enumerate(l)] for l in linhas]
    t = Table(dados, colWidths=[LARG * f for f in larg], repeatRows=1)
    st = [('GRID', (0, 0), (-1, -1), .5, LINE), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
          ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
          ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
          ('BACKGROUND', (0, 0), (-1, 0), W3 if escuro else PANEL2)]
    t.setStyle(TableStyle(st))
    t.spaceBefore, t.spaceAfter = 3, 9
    return t


def roteiro(itens):
    dados = [[Paragraph(f'<font color="#155A63"><b>{t}</b></font><br/>{d}', cel)] for t, d in itens]
    t = Table(dados, colWidths=[LARG])
    t.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), .5, LINE), ('LINEBELOW', (0, 0), (-1, -2), .5, LINE),
                           ('BACKGROUND', (0, 0), (-1, -1), HexColor('#FBFCFB')),
                           ('LEFTPADDING', (0, 0), (-1, -1), 10), ('TOPPADDING', (0, 0), (-1, -1), 6),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 7)]))
    t.spaceBefore, t.spaceAfter = 2, 6
    return t


def equacao(t):
    tb = Table([[Paragraph(t, eq)]], colWidths=[LARG])
    tb.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), PANEL2), ('BOX', (0, 0), (-1, -1), .5, LINE),
                            ('LEFTPADDING', (0, 0), (-1, -1), 11), ('TOPPADDING', (0, 0), (-1, -1), 9),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 9)]))
    tb.spaceBefore, tb.spaceAfter = 2, 8
    return tb


def faq(q, r): return KeepTogether([Paragraph(q, faq_q), Paragraph(r, corpo_esq)])


# ---------- conteúdo ----------
def CONTEUDO():
    s = []
    s += H1(1, 'O que é o Teia Sob Risco')
    s.append(P('O <b>Teia Sob Risco</b> é um laboratório interativo que reconstrói a teia alimentar de um estuário de Santa '
               'Catarina — do fitoplâncton e dos mangues até o boto-cinza, as aves e o ser humano — e mostra, em tempo '
               'real, como um poluente lançado na água <b>sobe os níveis tróficos</b> até chegar à maricultura, à pesca e '
               'à mesa. É um produto técnico-pedagógico voltado à aula de Biologia no Ensino Médio, dentro do campo da '
               'Cultura Oceânica e do <b>ODS 14 (Vida na Água)</b>.'))
    s.append(H2('Por que usar em sala'))
    s += B(['Conecta um conceito abstrato (bioacumulação e biomagnificação) a espécies <b>reais e locais</b>, com nome '
            'científico e papel ecológico.',
            'Liga ecologia à <b>saúde pública</b>: mostra quantos pescados ultrapassariam o limite da ANVISA para mercúrio.',
            'Funciona <b>offline</b>, em um único arquivo <font face="Courier">.html</font> — abre em qualquer celular, '
            'tablet ou computador, sem instalação e sem internet.',
            'Traz modos de <b>gamificação</b> (montar a teia, quiz) e um <b>painel do professor</b> para registrar resultados.'])
    s.append(caixa('Os valores de concentração são <b>relativos e ilustrativos</b>, com fins didáticos: não são medições. '
                   'Eles reproduzem <i>padrões</i> reais (ver seção 12), mas não devem ser citados como dados de campo.', WARN))

    s += H1(2, 'Antes de começar: abrir e projetar')
    s.append(passos([
        'Baixe o arquivo <font face="Courier">index.html</font> do repositório do projeto no GitHub e copie-o para o '
        'computador, tablet ou celular (pen drive, e-mail ou nuvem servem). Pode renomeá-lo à vontade, por exemplo, '
        'para <font face="Courier">Teia_Sob_Risco.html</font>.',
        'Toque/clique duas vezes no arquivo: ele abre no navegador (Chrome, Firefox, Edge ou Safari). <b>Não precisa de '
        'internet.</b> Com internet, o app também abre direto em <font face="Courier">tiagochavo87.github.io/teia-sob-risco</font>.',
        'Para projetar, conecte o aparelho ao projetor/TV e use tela cheia (tecla <font face="Courier">F11</font> no computador).',
        'Para atividade individual ou em duplas, distribua o mesmo arquivo entre as estações — cada aparelho roda de '
        'forma independente.']))
    s.append(Spacer(1, 6))
    s.append(H2('O que precisa e o que não precisa de internet'))
    s.append(tabela(['Funciona sempre (offline)', 'Só com internet'],
                    [['Simulador, gráficos, catálogo, quiz, montar a teia, narração em áudio (TTS), exportar '
                      'CSV/PNG/JSON, salvar registros no aparelho.',
                      'O intérprete de Libras (<b>VLibras</b>), que é um serviço externo do governo, e o endereço online '
                      'que o botão <b>Link</b> oferece quando o app é aberto do pen drive. Todo o restante é offline.']],
                    [.5, .5]))
    s.append(caixa('<b>No celular:</b> a cena do estuário mantém uma largura mínima para os nomes ficarem legíveis. '
                   'Arraste-a para os lados para ver todo o estuário.'))

    s += H1(3, 'A interface em um relance')
    s.append(P('O app tem quatro abas no topo:'))
    s.append(tabela(['Aba', 'O que tem'],
                    [['Início', 'Abertura com a pergunta motivadora e três dados de contexto.'],
                     ['Simulador', 'O coração do app: o estuário em corte, os parâmetros, os gráficos e todos os modos.'],
                     ['Catálogo', 'Guia de campo com 32 fichas (31 táxons e o folhiço/detrito), com filtro por nível '
                                  'trófico e ficha detalhada.'],
                     ['Modelo', 'Documentação: a equação, a diferença mercúrio × microplástico, o TMF e as referências.']],
                    [.18, .82], primeira_negrito=True))
    s.append(H2('Dentro do Simulador'))
    s += B(['<b>Estuário em corte:</b> cena ilustrada, com céu, coluna d’água, sedimento, maricultura e o emissário de '
            'onde sai a pluma de poluição. Passe o dedo/mouse sobre um organismo para destacar quem ele come e quem o '
            'come; toque para abrir a ficha.',
            '<b>Parâmetros:</b> escolha o <b>poluente</b> (mercúrio ou microplástico), um <b>cenário/fonte</b> pronto e a '
            '<b>intensidade</b> de liberação. Depois toque em <b>Liberar poluente</b>.',
            '<b>Remediação da fonte:</b> simula o tratamento do efluente — reduz a carga e recalcula a teia. Em 100%, '
            'nada entra na água e o app avisa que a teia ficou limpa.',
            '<b>Exposição ao longo do tempo:</b> anima a contaminação se acumulando (produtores primeiro, topo por último).',
            '<b>Leituras:</b> mais contaminado, magnificação trófica (TMF), valor no ser humano e nº de pescados acima do limite.',
            '<b>Gráficos:</b> concentração por organismo e concentração × nível trófico (com a reta de tendência e a '
            'opção <b>escala log</b>).',
            '<b>Abaixo dos gráficos:</b> tabela de dados, comparador de cenários, dados reais, painel do professor e '
            'acessibilidade (seções 7 a 9).'])
    s.append(tabela(['Atalho', 'Ação'],
                    [['1 / 2', 'Alterna entre mercúrio e microplástico'],
                     ['R', 'Libera o poluente (roda a simulação)'],
                     ['Botões da cena', 'Rótulos on/off · Alto contraste · Fonte ampliada (A+)']],
                    [.25, .75], primeira_negrito=True))

    s += H1(4, 'O modelo científico e o TMF')
    s.append(P('O simulador percorre a teia de baixo para cima, nível por nível. Para cada consumidor:'))
    s.append(equacao('C(organismo) = média[ C(presas) ] × fator de amplificação<br/>'
                     '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ ( água × filtragem direta )'))
    s.append(P('Os <b>produtores</b> (fitoplâncton, folhiço do mangue) absorvem o poluente direto da água. Cada consumidor '
               'herda a concentração das presas e soma o que filtra da água.'))
    s.append(H2('Mercúrio × microplástico'))
    s.append(tabela(['', 'Mercúrio (metilmercúrio)', 'Microplástico'],
                    [['Comportamento', 'Fator de amplificação maior que 1: <b>biomagnifica</b>, cresce a cada elo.',
                      'Fator menor que 1: <b>acumula, mas não biomagnifica</b>.'],
                     ['Onde fica o máximo', 'Predadores de topo e ser humano.', 'Filtradores (ostra, mexilhão, vieira).'],
                     ['No gráfico', 'Reta com <b>inclinação positiva</b>.', 'Nuvem de pontos <b>achatada</b>.'],
                     ['Limite legal', '0,5 mg/kg (ANVISA, pescado não predador). Por simplicidade, o app aplica essa linha '
                                      'a todos os pescados; para peixes predadores, a norma admite 1,0 mg/kg.',
                      'Sem limite definido no app.']],
                    [.2, .45, .35], escuro=True, primeira_negrito=True))
    s.append(H2('A leitura “Magnificação trófica (TMF)”'))
    s.append(P('O <b>TMF</b> (Fator de Magnificação Trófica) resume em um número se o poluente sobe a teia. Ele é a '
               'inclinação da reta de <b>log<sub>10</sub>(concentração)</b> contra o <b>nível trófico</b>, convertida em '
               'fator por nível: TMF = 10<super>inclinação</super>. É a mesma métrica usada em estudos de campo. Como o '
               'modelo é linear, o TMF não muda com a intensidade nem com a remediação.'))
    s += B(['<b>TMF maior que 1</b> — o poluente biomagnifica. No modelo, o mercúrio dá cerca de <b>1,6× por nível</b>.',
            '<b>TMF perto de 1 ou menor</b> — acumula sem biomagnificar. No modelo, o microplástico dá cerca de <b>0,9</b>.',
            'Ficam <b>de fora do cálculo</b> o ser humano (um ponto de consumo, escolha do que comer, e não um elo trófico '
            'fixo) e os produtores que nenhum consumidor do modelo come (mangues, marisma e alface-do-mar). No gráfico, '
            'eles aparecem como pontos vazados.',
            'O botão <b>escala log</b> do gráfico concentração × nível trófico mostra exatamente a reta cuja inclinação dá o TMF.'])
    s.append(caixa('<b>Pergunta para a turma:</b> por que o boto-cinza, que nunca “toca” no poluente diretamente, termina como '
                   'o mais contaminado no cenário de mercúrio? (Resposta: cada refeição concentra o que já estava '
                   'concentrado na presa — é a biomagnificação, e o TMF maior que 1 a mede.)'))

    s += H1(5, 'Roteiro de aula guiada (passo a passo)')
    s.append(P('No Simulador, o botão <b>“Roteiro de aula”</b> abre um guia de 5 passos que <b>configura o app '
               'automaticamente</b> a cada etapa. Uma barra aparece na base da tela com o texto do passo e os botões '
               '<i>Voltar</i> / <i>Avançar</i>. É a forma mais rápida de conduzir a turma pelos conceitos-chave.'))
    s.append(roteiro([
        ('Passo 1 — Liberar mercúrio', 'Libera mercúrio em intensidade alta (100%). Peça que observem <b>até onde</b> a '
                                       'contaminação chega na cena.'),
        ('Passo 2 — Ler o TMF', 'Aponte a leitura <b>Magnificação trófica</b> (1,6, maior que 1) e a reta subindo no '
                                'gráfico; ative a <b>escala log</b> para ver a reta do TMF. O cenário é fixado como <b>A</b>.'),
        ('Passo 3 — Trocar o poluente', 'Troca para microplástico na mesma intensidade e libera de novo. Para onde a '
                                        'contaminação vai desta vez?'),
        ('Passo 4 — Comparar padrões', 'O <b>TMF cai para menos de 1</b> (0,9) e quem lidera são os filtradores (ostra, '
                                       'mexilhão). Fixa como <b>B</b> e mostra o comparador lado a lado.'),
        ('Passo 5 — Da teia ao prato', 'Volta ao mercúrio em intensidade <b>média (60%)</b> e abre a <b>Tabela de dados</b>: '
                                       '10 dos 15 pescados passam de 0,5 mg/kg. Os bivalves (ostra, mexilhão, vieira, '
                                       'berbigão) ficam abaixo e os peixes, acima: quanto mais alto na teia, mais mercúrio. '
                                       'É o fecho, ligando ecologia e saúde pública.')]))
    s.append(caixa('Você pode sair do roteiro a qualquer momento (botão X ou tecla Esc) e continuar explorando manualmente. '
                   'Cada passo monta o cenário inteiro de que precisa (zera a remediação e ajusta poluente e intensidade), '
                   'então <i>Voltar</i> funciona igual a <i>Avançar</i>.'))

    s += H1(6, 'Os três modos: Explorar, Montar a teia e Quiz')
    s.append(P('Logo abaixo do título do Simulador há uma barra de modos:'))
    s += B(['<b>Explorar</b> (padrão): libere poluentes, toque nos organismos, compare cenários. O modo livre de investigação.',
            '<b>Montar a teia:</b> jogo com <b>86 ligações</b>. O aluno clica em <b>dois organismos</b> (ou usa Tab + Enter) '
            'para testar se um come o outro; acertos acendem a ligação em verde e contam pontos. Com <b>Pistas: ligadas</b> '
            '(padrão), as ligações ainda não descobertas aparecem tracejadas e apagadas, e as do organismo escolhido ficam '
            'mais fortes. Desligue as pistas para um desafio maior: sem pistas, passar o mouse não revela nada. '
            '<i>Revelar restantes</i> mostra o que falta; <i>Recomeçar</i> zera o placar.',
            '<b>Quiz:</b> cinco perguntas geradas a partir da própria simulação (quem acumula mais mercúrio, o que é '
            'produtor, o que a tainha come etc.). É preciso responder todas para corrigir; depois da correção as '
            'respostas ficam travadas, e a nota que vai para o painel é a da primeira correção. '
            '<i>Novas perguntas</i> sorteia outro conjunto.'])
    s.append(caixa('<b>Sugestão de dinâmica:</b> comece por <i>Montar a teia</i> (constrói o vocabulário de quem-come-quem), '
                   'passe ao <i>Explorar</i> com o roteiro guiado (introduz a contaminação) e feche com o <i>Quiz</i> como '
                   'avaliação rápida — registrando a pontuação no Painel do professor.'))

    s += H1(7, 'Comparador, tabela de dados, dados reais e exportações')
    s.append(H2('Comparador de cenários'))
    s.append(P('Depois de rodar uma simulação, use <b>Fixar como cenário A</b> e <b>Fixar como cenário B</b> para congelar '
               'dois cenários e vê-los lado a lado nos organismos-chave. É o recurso ideal para contrastar mercúrio × '
               'microplástico ou duas intensidades diferentes. Com a <b>mesma unidade</b> (por exemplo, mercúrio a 100% e a '
               '40%), as barras usam escala comum e a diferença de intensidade aparece. Com <b>unidades diferentes</b> '
               '(mg/kg × partículas/g), cada cenário é normalizado pelo próprio máximo: compare o padrão, não a altura '
               'das barras.'))
    s.append(H2('Tabela de dados (acessível)'))
    s.append(P('Abaixo dos gráficos, a <b>Tabela de dados</b> lista cada organismo com nível trófico, papel, concentração e se '
               'está acima do limite. Serve tanto para leitores de tela quanto para o momento “mostre-me os números” — ótima '
               'para copiar valores para o caderno ou para a lousa.'))
    s.append(H2('Dados reais: comparar o padrão'))
    s.append(P('O cartão <b>Dados reais</b> recebe valores medidos (de artigos ou de coleta local) para ostra, tainha, robalo, '
               'boto-cinza e ser humano, na unidade do poluente ativo, e os desenha ao lado dos simulados. Aceita vírgula ou '
               'ponto decimal (<font face="Courier">0,12</font> ou <font face="Courier">0.12</font>); um valor que não é '
               'número fica marcado e aparece um aviso. Como os valores simulados são ilustrativos, compare o '
               '<b>padrão</b> (quem tem mais, quem tem menos, a ordem de grandeza), não os números exatos.'))
    s.append(H2('Exportar e compartilhar'))
    s.append(tabela(['Botão', 'O que faz'],
                    [['CSV', 'Baixa a concentração por organismo, com o poluente, a intensidade e a remediação em cada linha '
                             '(abre no Excel/Planilhas, com acentos corretos).'],
                     ['PNG', 'Salva o gráfico de barras como imagem, com a linha de 0,5 mg/kg.'],
                     ['Imprimir', 'Gera uma versão para papel/PDF (esconde botões e menus).'],
                     ['Link', 'Copia um endereço que <b>reproduz o cenário exato</b> (poluente + intensidade + remediação). Na '
                              'versão online, basta colar no navegador de outra estação. Aberto do pen drive, o botão mostra '
                              'o endereço da versão online (que precisa de internet) e a configuração para refazer à mão.']],
                    [.16, .84], primeira_negrito=True))
    s.append(caixa('O botão <b>Link</b> é a forma mais simples de todos os alunos partirem do mesmo ponto: prepare o cenário na '
                   'versão online, copie o link e envie pelo mural/WhatsApp da turma. Sem internet, dite a configuração que '
                   'o botão mostra (poluente, intensidade e remediação).'))

    s += H1(8, 'Painel do professor: registrar e consolidar turmas')
    s.append(P('O <b>Painel do professor</b> (no fim do Simulador) registra os resultados da sessão <b>neste aparelho</b>. Os '
               'registros ficam salvos mesmo se você fechar o navegador.'))
    s.append(passos([
        'Digite a turma/atividade (ex.: “2º A — manhã”) e a estação/dupla (ex.: “dupla 3”, sem nomes).',
        'Clique em <b>Registrar resultado atual</b>. Ele grava data, hora, turma, estação, o modo e o resultado: no '
        '<i>Explorar</i>, o cenário, o TMF e o organismo mais contaminado; no <i>Montar a teia</i>, as ligações descobertas '
        'e se foi com ou sem pistas; no <i>Quiz</i>, a nota da primeira correção.',
        'Ao final, use <b>Exportar JSON</b> em cada estação e <b>Importar</b> num único aparelho para <b>consolidar a turma '
        'toda</b>. Registros repetidos são ignorados, então importar o mesmo arquivo duas vezes não duplica nada.',
        '<b>CSV</b> gera a mesma tabela para planilha; <b>Apagar</b> limpa os registros do aparelho (pede confirmação).']))
    s.append(Spacer(1, 4))
    s.append(caixa('A junção <i>em tempo real</i> entre vários aparelhos exigiria um servidor. Aqui a consolidação é feita '
                   'depois, via exportação/importação de JSON — simples, offline e sem depender de infraestrutura da escola.',
                   HAZ1))
    s.append(caixa('<b>Privacidade:</b> os dados nunca saem do aparelho por conta própria — só quando você exporta o arquivo. '
                   'Evite registrar nomes de alunos; prefira identificar por turma ou por número.', WARN))

    s += H1(9, 'Acessibilidade e inclusão')
    s += B(['<b>Narração em áudio (TTS):</b> o botão <i>Ouvir</i>, na ficha do organismo, e o <i>Narrar seleção</i>, no '
            'cartão Acessibilidade, leem a ficha em português; <i>Parar áudio</i> interrompe. Funciona offline (usa a voz '
            'do próprio aparelho).',
            '<b>Libras (VLibras):</b> <i>Ativar Libras</i> carrega o intérprete oficial do governo. Aparece um botão azul na '
            'lateral direita da tela: toque nele e selecione um texto para traduzir. <b>Requer internet</b> — é o único '
            'recurso que não funciona offline.',
            '<b>Alto contraste</b> e <b>fonte ampliada (A+)</b>: botões na cena, úteis para baixa visão e para projeção em '
            'salas claras.',
            '<b>Tabela de dados</b> e rótulos de organismos com <i>aria-label</i>: leitores de tela conseguem navegar pela teia.',
            '<b>Navegação por teclado:</b> é possível dar foco aos organismos com Tab e ativar com Enter/Espaço, inclusive '
            'no jogo <i>Montar a teia</i>.'])

    s += H1(10, 'Plano de aula sugerido')
    s.append(P('Sequência de quatro encontros, na lógica da Corrente de Aprendizagem. Ajuste ao seu contexto.'))
    s.append(tabela(['Aula', 'Foco', 'No app', 'Produto'],
                    [['1', 'Quem come quem: teia alimentar do estuário', 'Catálogo + modo <i>Montar a teia</i>',
                      'Teia reconstruída; vocabulário de níveis tróficos'],
                     ['2', 'Bioacumulação × biomagnificação', '<i>Roteiro guiado</i>, passos 1–2 (mercúrio, TMF)',
                      'Registro do TMF e do organismo mais contaminado'],
                     ['3', 'Tipos de poluente e destino na teia', 'Roteiro, passos 3–4; <i>Comparador</i>; exportar CSV',
                      'Tabela/CSV comparando mercúrio × microplástico'],
                     ['4', 'Da teia ao prato: saúde pública e ação', 'Passo 5 (limite ANVISA); <i>Remediação</i>; <i>Quiz</i>',
                      'Proposta de mitigação; quiz avaliativo']],
                    [.08, .28, .32, .32], escuro=True))
    s.append(H2('Ganchos com a BNCC e a Cultura Oceânica'))
    s += B(['Transferência de matéria e energia nos ecossistemas; cadeias e teias alimentares.',
            'Impactos ambientais e ações de sustentabilidade (ODS 14) no litoral catarinense.',
            'Interpretação de gráficos e de dados quantitativos; noção de limite legal e risco.',
            'Princípio da Cultura Oceânica: “o oceano e o ser humano estão profundamente interligados”.'])

    s += H1(11, 'Perguntas frequentes e solução de problemas')
    s += [faq('O app não abre / abre em branco.',
              'Confirme que o arquivo tem a extensão <font face="Courier">.html</font> e abra-o com um navegador atual '
              '(Chrome, Firefox, Edge, Safari). Evite abrir dentro de apps de mensagem; salve primeiro no aparelho.'),
          faq('A cena não cabe na tela do celular.',
              'É de propósito: a cena mantém uma largura mínima para os nomes ficarem legíveis. Arraste-a para os lados. '
              'O restante da página se ajusta à largura da tela.'),
          faq('Não sai som na narração.',
              'Verifique o volume e se o navegador tem voz em português instalada. Em alguns celulares a primeira narração '
              'só sai após um toque na tela. O botão “Parar áudio” interrompe.'),
          faq('O Libras não ativa.',
              'O VLibras precisa de internet — é o único recurso online. Sem conexão, o app avisa e a narração em áudio '
              'continua funcionando offline.'),
          faq('Com a remediação em 100%, tudo zerou.',
              'Está certo: o efluente foi todo tratado e nada entra na água, então a teia fica limpa. Reduza a remediação '
              'para ver a contaminação voltar a subir a teia.'),
          faq('Um valor em Dados reais ficou marcado em vermelho.',
              'O campo aceita só números, com vírgula ou ponto decimal (<font face="Courier">0,12</font> ou '
              '<font face="Courier">0.12</font>). Apague letras, unidades e outros símbolos.'),
          faq('Os registros do painel sumiram.',
              'Eles ficam salvos por aparelho e por navegador. Trocar de navegador, usar aba anônima ou limpar os dados do '
              'site apaga os registros. Exporte em JSON antes de encerrar para não perder.'),
          faq('O link do cenário não copiou.',
              'Se o navegador bloquear a cópia automática, aparece uma caixa com o link para copiar à mão. Aberto do pen '
              'drive, a caixa traz o endereço da versão online e a configuração para refazer o cenário sem internet.'),
          faq('Quero comparar duas intensidades do mesmo poluente.',
              'Rode a 1ª, fixe como A; mude a intensidade, rode de novo e fixe como B. Como a unidade é a mesma, o '
              'comparador usa escala comum e a diferença aparece na altura das barras.'),
          faq('Posso adaptar o app?',
              'Sim. É um Recurso Educacional Aberto: pode ser usado e adaptado por professores. Espécies, poluentes e '
              'textos ficam no próprio arquivo, nas listas de espécies e de poluentes do código.')]

    s += H1(12, 'Limites do modelo e referências')
    s.append(P('O Teia Sob Risco é um <b>modelo didático simplificado</b>. Ele assume um estado estacionário (a teia “já se '
               'equilibrou” com a fonte), usa a média das presas e trata a filtragem de forma linear. Ele não modela idade, '
               'tamanho, sazonalidade, migração, taxa de depuração real nem toxicocinética individual. Os valores são '
               '<b>relativos e ilustrativos</b> — servem para revelar <i>padrões</i> (biomagnificação do mercúrio, acúmulo em '
               'filtradores do microplástico, a linha de 0,5 mg/kg), não para estimar risco real de consumo. Para isso, '
               'remeta os alunos a órgãos oficiais e à literatura.'))
    s.append(P('A <i>magnitude</i> também é didática: no modelo, o boto-cinza fica cerca de 7 vezes acima do fitoplâncton, bem '
               'menos que os ~36× medidos na Baía de Guanabara, porque cada consumidor come uma mistura de presas de níveis '
               'diferentes, o que dilui o ganho a cada elo. Ostras e mexilhões chegam à faixa de 12–16 partículas por grama '
               'observada em bivalves do litoral com intensidade entre 70% e 90%.'))
    s.append(H2('Referências'))
    s += [P(t, ref) for t in [
        'KEHRIG, H. A.; MALM, O.; PALERMO, E. F. A.; SEIXAS, T. G.; BAÊTA, A. P.; MOREIRA, I. Bioconcentração e '
        'biomagnificação de metilmercúrio na baía de Guanabara, Rio de Janeiro. <i>Química Nova</i>, v. 34, n. 3, '
        'p. 377–384, 2011.',
        'SANTORO, F. et al. <i>Cultura oceânica para todos: kit pedagógico</i>. Paris/Veneza: COI-UNESCO, 2020.',
        'ORGANIZAÇÃO DAS NAÇÕES UNIDAS. <i>Agenda 2030 para o Desenvolvimento Sustentável</i>. ONU, 2015.',
        'BRASIL. Ministério da Educação. <i>Base Nacional Comum Curricular: Ensino Médio</i>. Brasília: MEC, 2018.']]
    s.append(Spacer(1, 10))
    linha = Table([['']], colWidths=[LARG], rowHeights=[1])
    linha.setStyle(TableStyle([('LINEABOVE', (0, 0), (-1, -1), .5, LINE)]))
    s += [linha, Spacer(1, 6),
          P('Teia Sob Risco · produto técnico-pedagógico da Corrente de Aprendizagem — Pós-Graduação em Cultura Oceânica e '
            'Sustentabilidade na Educação Básica (UFSC/UAB). Aplicação de arquivo único, sem servidor, funciona offline. '
            'Recurso educacional aberto para uso e adaptação por professores.', fecho)]
    return s


# ---------- páginas ----------
def capa(c, doc):
    c.saveState()
    c.setFillColor(COVER); c.rect(0, 0, PW, PH, stroke=0, fill=1)
    # marca: arco e três pontos (níveis tróficos)
    x0, y0 = ML + 4, PH - 120
    c.setStrokeColor(HAZ1); c.setLineWidth(3.2); c.setLineCap(1)
    p = c.beginPath(); p.arc(x0 + 10, y0 - 6, x0 + 52, y0 + 22, 30, 120); c.drawPath(p, stroke=1, fill=0)
    for (dx, dy, cor) in [(0, -42, TL[0]), (12, -26, TL[1]), (26, -12, TL[2])]:
        c.setFillColor(cor); c.circle(x0 + dx, y0 + dy, 4.2, stroke=0, fill=1)
    # ondas
    c.setStrokeColor(HexColor('#1B4A52')); c.setLineWidth(.8)
    import math
    for k, yb in enumerate((150, 132, 114)):
        p = c.beginPath(); p.moveTo(0, yb)
        for xi in range(0, int(PW) + 6, 6):
            p.lineTo(xi, yb + 4 * math.sin(xi / 38 + k))
        c.drawPath(p, stroke=1, fill=0)
    # faixa dos níveis tróficos
    wb = PW / 5
    for i, cor in enumerate(TL):
        c.setFillColor(cor); c.rect(i * wb, 0, wb + .5, 22, stroke=0, fill=1)
    # textos
    y = PH * .5 + 30
    c.setFillColor(TIDE); c.setFont('Helvetica-Bold', 8.5); c.drawString(ML, y + 52, 'MANUAL DO PROFESSOR')
    c.setFillColor(white); c.setFont('Times-Bold', 38); c.drawString(ML, y + 10, 'Teia Sob Risco')
    c.setFillColor(HexColor('#CFE7E1')); c.setFont('Times-Italic', 12.5)
    c.drawString(ML, y - 12, 'Laboratório trófico-ecotoxicológico de um estuário catarinense')
    c.drawString(ML, y - 28, '— da raiz do mangue ao seu prato.')
    c.setFillColor(HexColor('#9FC2BE')); c.setFont('Helvetica', 8.5)
    for i, t in enumerate(['Aplicação de arquivo único · funciona offline · Ensino Médio',
                           'Cultura Oceânica · ODS 14 · alinhado à BNCC',
                           f'Versão {VERSAO} · {DATA}']):
        c.drawString(ML, y - 76 - i * 13, t)
    c.restoreState()


def miolo(c, doc):
    c.saveState()
    yh = PH - 46
    c.setFont('Helvetica-Bold', 7.5); c.setFillColor(W2); c.drawString(ML, yh, 'TEIA SOB RISCO')
    c.setFont('Helvetica', 7.5); c.setFillColor(MUTED); c.drawRightString(PW - MR, yh, f'Manual do Professor · v{VERSAO}')
    c.setStrokeColor(LINE); c.setLineWidth(.6); c.line(ML, yh - 6, PW - MR, yh - 6)
    yf = 36
    c.line(ML, yf + 12, PW - MR, yf + 12)
    c.setFont('Helvetica', 7.5); c.setFillColor(MUTED)
    c.drawString(ML, yf, 'Recurso Educacional Aberto · Cultura Oceânica e Sustentabilidade (UFSC/UAB)')
    c.setFont('Helvetica-Bold', 8); c.setFillColor(INK); c.drawRightString(PW - MR, yf, str(doc.page))
    c.restoreState()


class Manual(BaseDocTemplate):
    def __init__(self, fn, paginas):
        super().__init__(fn, pagesize=A4, leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB,
                         title=f'Manual do Professor — Teia Sob Risco v{VERSAO}', author='Teia Sob Risco',
                         subject='Manual do professor usuário', lang='pt-BR')
        fr = Frame(ML, MB, LARG, PH - MT - MB, id='f', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate('capa', [Frame(0, 0, PW, PH, id='c')], onPage=capa),
                               PageTemplate('miolo', [fr], onPage=miolo)])
        self.paginas_ant, self.paginas = paginas, {}

    def afterFlowable(self, f):
        if isinstance(f, Titulo):
            self.paginas[f.num] = self.page


def sumario(paginas):
    secoes = [(1, 'O que é o Teia Sob Risco'), (2, 'Antes de começar: abrir e projetar'), (3, 'A interface em um relance'),
              (4, 'O modelo científico e o TMF'), (5, 'Roteiro de aula guiada (passo a passo)'),
              (6, 'Os três modos: Explorar, Montar a teia e Quiz'), (7, 'Comparador, tabela de dados, dados reais e exportações'),
              (8, 'Painel do professor: registrar e consolidar turmas'), (9, 'Acessibilidade e inclusão'),
              (10, 'Plano de aula sugerido (Corrente de Aprendizagem)'), (11, 'Perguntas frequentes e solução de problemas'),
              (12, 'Limites do modelo e referências')]
    dados = [[Paragraph(str(n), toc_n), Paragraph(t, toc_t), Paragraph(str(paginas.get(n, '00')), toc_p)] for n, t in secoes]
    tb = Table(dados, colWidths=[28, LARG - 60, 32])
    tb.setStyle(TableStyle([('LINEBELOW', (0, 0), (-1, -1), .5, LINE), ('TOPPADDING', (0, 0), (-1, -1), 5),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 6), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 0)]))
    return [Paragraph('Sumário', h1), Spacer(1, 4), tb, Spacer(1, 14),
            caixa(f'<b>Dica rápida:</b> este manual descreve a versão {VERSAO} (o número aparece na barra de status, no fim do '
                  'Simulador). Em versões anteriores, recursos como as <i>Pistas</i> do jogo, o campo <i>estação</i> do painel '
                  'e as correções de exibição no celular podem não estar presentes.'),
            PageBreak()]


def gerar():
    paginas = {}
    for _ in range(2):  # 1ª passagem descobre as páginas; 2ª escreve o sumário com elas
        doc = Manual(SAIDA, paginas)
        # página 1 = capa (desenhada no onPage); o miolo começa no sumário
        doc.build([Spacer(1, 1), NextPageTemplate('miolo'), PageBreak()] + sumario(paginas) + CONTEUDO())
        paginas = doc.paginas
    print('ok:', SAIDA, paginas)


if __name__ == '__main__':
    gerar()
