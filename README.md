# 🌊 Teia Sob Risco

**Laboratório trófico-ecotoxicológico de um estuário catarinense — da raiz do mangue ao seu prato.**

![versão](https://img.shields.io/badge/versão-6.0-2BB3A3)
![offline](https://img.shields.io/badge/funciona-offline-155A63)
![sem dependências](https://img.shields.io/badge/dependências-nenhuma-0C3A44)
![licença](https://img.shields.io/badge/licença-REA%20(CC%20BY--SA)-E0902F)

> _"Por que um poluente lançado no mar hoje pode terminar concentrado no peixe que chega ao nosso prato?"_

O **Teia Sob Risco** é uma aplicação educativa interativa que reconstrói a teia alimentar de um estuário/manguezal de Santa Catarina — do fitoplâncton e dos mangues até o boto-cinza, as aves e o ser humano — e mostra, **em tempo real**, como um poluente sobe os níveis tróficos até chegar à maricultura, à pesca e à mesa.

É um produto técnico-pedagógico voltado à aula de Biologia no Ensino Médio, no campo da **Cultura Oceânica** e do **ODS 14 (Vida na Água)**, alinhado à BNCC.

## 🔗 Acesso

- **Aplicação (online):** https://tiagochavo87.github.io/teia-sob-risco/
- **Offline:** baixe o arquivo `.html` e abra em qualquer navegador — **não precisa de internet nem instalação.**

## ✨ Recursos

- **Simulador em corte** do estuário com 32 táxons reais (fauna e flora locais), com destaque de dieta ao passar o cursor e ficha por organismo.
- **Dois poluentes contrastantes:** mercúrio (metilmercúrio), que **biomagnifica**, e microplástico, que **acumula sem biomagnificar**.
- **Fator de Magnificação Trófica (TMF):** métrica de campo (inclinação de `log10(C)` × nível trófico) que resume, num número, se o poluente sobe a teia.
- **Remediação da fonte** e **exposição ao longo do tempo** (animação da contaminação subindo a teia).
- **Roteiro de aula guiada:** guia de 5 passos que configura o app automaticamente a cada etapa.
- **Três modos:** _Explorar_ (livre), _Montar a teia_ (jogo de quem-come-quem) e _Quiz_ (5 perguntas geradas da própria simulação).
- **Comparador de cenários A/B** e **tabela de dados acessível** (leitor de tela).
- **Exportações:** CSV, PNG, impressão e **link de cenário** (reproduz poluente + intensidade + remediação, offline).
- **Painel do professor:** registra resultados no aparelho (localStorage) e permite **exportar/importar JSON** para consolidar turmas.
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

> ⚠️ **Aviso importante:** os valores são **relativos e ilustrativos, com fins didáticos** — não são medições. Reproduzem *padrões* reais (biomagnificação do mercúrio, acúmulo em filtradores, a linha de 0,5 mg/kg da ANVISA), mas **não devem ser citados como dados de campo**.

## 📁 Estrutura do repositório

```
teia-sob-risco/
├── index.html          # a aplicação (arquivo único, offline)
├── docs/
│   └── Manual_do_Professor_Teia_Sob_Risco_v6.pdf
└── README.md
```

> Ajuste os nomes conforme o seu repositório. O GitHub Pages serve o `index.html` da raiz (ou a pasta configurada em *Settings → Pages*).

## 👩‍🏫 Para o professor

O **Manual do Professor** (PDF) cobre instalação, tour da interface, o TMF, o roteiro de aula passo a passo, um plano de 4 encontros alinhado à BNCC, FAQ e os limites do modelo.

Sequência sugerida (Corrente de Aprendizagem):

| Aula | Foco | No app |
|------|------|--------|
| 1 | Quem come quem: a teia | Catálogo + _Montar a teia_ |
| 2 | Bioacumulação × biomagnificação | Roteiro guiado (mercúrio, TMF) |
| 3 | Tipos de poluente e destino | Comparador + exportar CSV |
| 4 | Da teia ao prato: saúde pública | Limite ANVISA + Remediação + Quiz |

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
