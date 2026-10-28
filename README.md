# 🌊 Teia Sob Risco

**Laboratório trófico-ecotoxicológico de um estuário catarinense — da raiz do mangue ao seu prato.**

![versão](https://img.shields.io/badge/versão-7.0-2BB3A3)
![offline](https://img.shields.io/badge/funciona-offline-155A63)
![sem dependências](https://img.shields.io/badge/dependências-nenhuma-0C3A44)
![licença](https://img.shields.io/badge/licença-REA%20(CC%20BY--SA)-E0902F)

> _"Por que um poluente lançado no mar hoje pode terminar concentrado no peixe que chega ao nosso prato?"_

O **Teia Sob Risco** é uma aplicação educativa interativa que reconstrói a teia alimentar de um estuário/manguezal de Santa Catarina — do fitoplâncton e dos mangues até o boto-cinza, as aves e o ser humano — e mostra, **em tempo real**, como um poluente sobe os níveis tróficos até chegar à maricultura, à pesca e à mesa.

É um produto técnico-pedagógico voltado à aula de Biologia no Ensino Médio, no campo da **Cultura Oceânica** e do **ODS 14 (Vida na Água)**, alinhado à BNCC.

## 🔗 Acesso

- **Aplicação (online):** https://tiagochavo87.github.io/teia-sob-risco/
- **Direto no modo 7º ano:** https://tiagochavo87.github.io/teia-sob-risco/?nivel=7
- **Offline:** baixe o arquivo `.html` e abra em qualquer navegador — **não precisa de internet nem instalação.**

## ✨ Recursos

- **Simulador em corte** do estuário com 31 táxons reais (fauna e flora locais, mais o ser humano) e o folhiço/detrito, com destaque de dieta ao passar o cursor e ficha por organismo.
- **Dois poluentes contrastantes:** mercúrio (metilmercúrio), que **biomagnifica**, e microplástico, que **acumula sem biomagnificar**.
- **Fator de Magnificação Trófica (TMF):** métrica de campo (inclinação de `log10(C)` × nível trófico) que resume, num número, se o poluente sobe a teia. O gráfico tem uma opção de **escala log** que mostra a própria reta do TMF.
- **Remediação da fonte** e **exposição ao longo do tempo** (animação da contaminação subindo a teia).
- **Roteiro de aula guiada:** guia de 5 passos que configura o app automaticamente a cada etapa.
- **Dois níveis:** _Ensino Médio_ (com o TMF) e _7º ano_ do Ensino Fundamental, com leituras e roteiro em linguagem simples, sem TMF nem escala log. O nível fica guardado no aparelho e pode vir no link (`?nivel=7`).
- **Quatro modos:** _Explorar_ (livre), _Montar a teia_ (jogo de quem-come-quem, com pistas opcionais), _Quiz_ (5 perguntas geradas da própria simulação) e _Antes e depois_ (questionário de aprendizagem aplicado no início e no fim da sequência).
- **Comparador de cenários A/B** e **tabela de dados acessível** (leitor de tela).
- **Exportações:** CSV, PNG, impressão e **link de cenário** (reproduz poluente + intensidade + remediação; aberto do pen drive, oferece o endereço da versão online e a configuração para refazer à mão).
- **Painel do professor:** registra resultados no aparelho (localStorage), com data, turma e estação; no modo Explorar, guarda o cenário, o TMF e o organismo mais contaminado. Permite **exportar/importar JSON** para consolidar turmas (registros repetidos são ignorados).
- **Acessibilidade:** narração em áudio (TTS, offline), Libras via VLibras (requer internet), alto contraste, fonte ampliada e navegação por teclado.

## 🚀 Como usar

Não há build nem instalação — é um único arquivo HTML.

```bash
# clonar
git clone https://github.com/tiagochavo87/teia-sob-risco.git
cd teia-sob-risco

# abrir localmente (basta um duplo-clique no arquivo .html)
# ou servir por HTTP, se preferir:
python3 -m http.server 8000
# depois acesse http://localhost:8000
```

Em sala, distribua o mesmo arquivo entre as estações (pen drive, e-mail ou nuvem) — cada aparelho roda de forma independente.

## 🧪 Como o modelo funciona

O simulador percorre a teia de baixo para cima, nível por nível. Para cada consumidor:

```
C(organismo) = média[ C(presas) ] × fator de amplificação + ( água × filtragem direta )
```

Os **produtores** absorvem o poluente direto da água; cada consumidor herda a concentração das presas e soma o que filtra. O **mercúrio** tem fator > 1 (biomagnifica, máximo no topo); o **microplástico** tem fator < 1 e entra pela filtragem (máximo nos filtradores).

No cálculo do TMF entram só os organismos ligados à teia: o ser humano (ponto de consumo) e os produtores que nenhum consumidor do modelo come (mangues, marisma e alface-do-mar) ficam de fora. Com isso, o TMF fica em torno de **1,6** para o mercúrio e **0,9** para o microplástico, em qualquer intensidade (o modelo é linear).

> ⚠️ **Aviso importante:** os valores são **relativos e ilustrativos, com fins didáticos** — não são medições. Reproduzem *padrões* reais (biomagnificação do mercúrio, acúmulo em filtradores, a linha de 0,5 mg/kg da ANVISA), mas **não devem ser citados como dados de campo**.

## 📁 Estrutura do repositório

```
teia-sob-risco/
├── index.html                                # a aplicação (arquivo único, offline)
├── Manual_do_Professor_Teia_Sob_Risco_v6.pdf # manual do professor
├── manual/gerar_manual.py                    # texto e diagramação do manual (gera o PDF)
├── avaliacao/criar_formulario_professores.gs # Google Apps Script: formulário anônimo dos professores + cálculo de IVC e SUS
├── teia_icon.ico
└── README.md
```

O GitHub Pages serve o `index.html` da raiz. Para distribuir offline, o mesmo `index.html` pode ser renomeado à vontade (por exemplo, `Teia_Sob_Risco.html`).

## 👩‍🏫 Para o professor

O **Manual do Professor** (PDF) cobre instalação, tour da interface, o TMF, o roteiro de aula passo a passo, um plano de 4 encontros alinhado à BNCC, FAQ e os limites do modelo.

Para atualizar o manual, edite o texto em `manual/gerar_manual.py` e rode `python3 manual/gerar_manual.py` (requer `pip install reportlab`); o sumário recalcula as páginas sozinho.

Sequência sugerida (Corrente de Aprendizagem):

| Aula | Foco | No app |
|------|------|--------|
| 1 | Quem come quem: a teia | Catálogo + _Montar a teia_ |
| 2 | Bioacumulação × biomagnificação | Roteiro guiado (mercúrio, TMF) |
| 3 | Tipos de poluente e destino | Comparador + exportar CSV |
| 4 | Da teia ao prato: saúde pública | Limite ANVISA + Remediação + Quiz |

## 🆕 Novidades da v7.0

- **Modo 7º ano:** seletor _Ensino Médio | 7º ano_ na barra de modos (ou o link com `?nivel=7`). No 7º ano, a leitura do TMF vira **Sobe a teia?** (Sim/Não, com uma comparação como "boto-cinza: 7× o fitoplâncton"), as unidades ganham explicação, o gráfico perde a escala log, o cartão Dados reais fica oculto e o **Roteiro de aula** tem 5 passos próprios, terminando na remediação da fonte.
- **Questionário Antes e depois:** 10 perguntas de conhecimento e 6 frases de concordância, com o simulador escondido enquanto o aluno responde. O aluno usa um código sem nome; ao enviar o Depois, vê quantas acertou antes e depois e as respostas certas comentadas. Cada pergunta tem botão **Ouvir**. A **Área da professora** mostra o acerto por pergunta, exporta JSON/CSV, importa sem duplicar, imprime a versão em papel e apaga tudo. As respostas ficam só no aparelho.
- **Painel do professor:** registra também o modo Antes e depois (contagem de respostas e médias).
- **Atalhos:** as teclas 1, 2 e R ficam desligadas no jogo e no questionário, para não rodar a simulação por trás.
- **Formulário dos professores:** `avaliacao/criar_formulario_professores.gs` cria, num Google Forms anônimo, a avaliação da plataforma por partes, a escala SUS e o julgamento dos itens do questionário; `calcularResultados` calcula o IVC por item, a avaliação por partes e a pontuação SUS.
- **Manual do Professor:** nova seção sobre o modo 7º ano e o questionário, e perguntas frequentes novas.

## Novidades da v6.3

- **Cena completa no Simulador:** o céu, o degradê da água e a pluma de poluição voltaram a aparecer. Os degradês da tela de Início e do Simulador tinham o mesmo nome, e o Simulador acabava usando os da tela de Início, que fica escondida.
- **Dados reais:** os campos aceitam vírgula ou ponto (`0,12` = `0.12`). Antes, num navegador configurado em inglês, `0,12` virava `12`. Valor que não é número fica marcado e aparece um aviso.
- **Celular:** nenhuma parte da página fica mais larga que a tela (cabeçalhos, botões dos gráficos, jogo e tabela do painel quebram linha ou rolam dentro do cartão); a barra do roteiro cabe inteira.
- **Remediação em 100%:** as leituras e o texto explicam que a teia ficou limpa, em vez de apontar um "mais contaminado" com 0,00.
- **Toque nos organismos:** cada organismo responde ao clique em toda a área do círculo de destaque (antes, o meio do camarão e do ser humano não respondia).
- **Rótulos sem sobreposição:** ostra × alface-do-mar, caranguejo-uçá × chama-maré, mangue-vermelho × mangue-preto e os rótulos com fonte ampliada.
- **Textos:** rodapé atualizado para o TCC 2; aba Modelo informa em que intensidade os bivalves ficam na faixa de 12–16 partículas/g; Manual do Professor revisto para a versão atual.

## Novidades da v6.2

- **Montar a teia com pistas:** as ligações ainda não descobertas aparecem como linhas tracejadas e apagadas; ao escolher um organismo (ou passar o mouse), as linhas dele ficam mais fortes. O botão **Pistas** liga e desliga esse apoio, e o painel do professor registra se o jogo foi feito com ou sem pistas.

## Novidades da v6.1

- **Montar a teia:** passar o mouse não revela mais as ligações; o jogo também funciona pelo teclado (Tab + Enter).
- **Quiz:** depois de corrigir, as respostas ficam travadas; a nota registrada é a da primeira correção.
- **Roteiro de aula:** "Voltar" não bagunça mais o comparador; o passo 5 usa intensidade média (60%), em que os bivalves ficam abaixo do limite e os peixes, acima.
- **Sincronia:** trocar cenário ou intensidade refaz a simulação; CSV, comparador e link usam sempre o cenário que está na tela.
- **TMF:** exclui os produtores sem ligação com a teia; nova opção de escala log no gráfico.
- **Exportações:** CSV abre com acentos no Excel e traz poluente, intensidade e remediação; o PNG mantém a linha da ANVISA.
- **Comparador:** mesma unidade → escala comum (diferenças de intensidade aparecem).
- **Celular:** a cena rola na horizontal, com rótulos legíveis; "Contraste" também realça os organismos.
- **Link:** aberto do pen drive, oferece o endereço da versão online e a configuração para refazer à mão.
- **Painel:** data, estação, resumo da exploração e importação sem duplicatas.

## ♿ Acessibilidade

Narração em áudio, alto contraste, fonte ampliada, `aria-label` nos organismos e tabela de dados navegável por leitor de tela funcionam **offline**. Apenas o intérprete de **Libras (VLibras)** depende de internet.

## 🌐 Publicação (GitHub Pages)

1. Faça commit do `index.html` na branch de publicação (geralmente `main`).
2. Em **Settings → Pages**, selecione a branch e a pasta de origem.
3. Aguarde a propagação (segundos a ~10 min) e recarregue com `Ctrl+Shift+R` para furar o cache.

## 📚 Referências

- KEHRIG, H. A. et al. *Bioconcentração e biomagnificação de metilmercúrio na baía de Guanabara.* Química Nova, v. 34, n. 3, 2011.
- SANTORO, F. et al. *Cultura oceânica para todos: kit pedagógico.* COI-UNESCO, 2020.
- ONU. *Agenda 2030 para o Desenvolvimento Sustentável.* 2015.
- BRASIL/MEC. *Base Nacional Comum Curricular: Ensino Médio.* 2018.

## 📄 Licença

Recurso Educacional Aberto (REA). Sugerido: **Creative Commons Atribuição-CompartilhaIgual (CC BY-SA 4.0)** — livre para uso e adaptação por professores, com atribuição. Adicione um arquivo `LICENSE` para formalizar.

## 🙌 Créditos

Produto técnico-pedagógico da **Corrente de Aprendizagem** — Pós-Graduação em **Cultura Oceânica e Sustentabilidade na Educação Básica** (UFSC/UAB).

---

<sub>Feito para rodar em qualquer dispositivo, sem servidor. Contribuições e adaptações são bem-vindas.</sub>
