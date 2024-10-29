# Análise de Aplicativos

Este projeto realiza a análise de dados de aplicativos a partir de um arquivo JSON. Ele extrai informações relevantes, realiza análises competitivas e gera relatórios e gráficos para facilitar a visualização dos resultados.

## Estrutura do Projeto

- `AppAnalysis.py`: Classe principal que contém toda a lógica para carregar, processar e analisar os dados.
- `data/`: Pasta onde os relatórios gerados são salvos.
- `assets/`: Pasta onde os gráficos gerados são salvos.
- `gplaystore.categoryAppPositionsAllbanks.json`: Arquivo JSON com os dados dos aplicativos.

## Instalação

Para executar o projeto, você precisará ter o Python 3.x e as seguintes bibliotecas instaladas:

- `pandas`
- `matplotlib`
- `seaborn`

Você pode instalar as dependências usando pip:

```bash
pip install pandas matplotlib seaborn
```
## Uso
Para realizar a análise, você deve alterar o caminho do arquivo JSON no final do código da classe `AppAnalysis`.
```bash
if __name__ == "__main__":
    analysis = AppAnalysis('../data/gplaystore.categoryAppPositionsAllbanks.json')
    analysis.run_analysis()
```
Após executar o script, os seguintes arquivos serão gerados:

- Gráficos em `assets/`:
    - `pontuacao_media.png`: Gráfico da pontuação média dos aplicativos.
    - `variacao_posicao.png`: Gráfico da variação de posição dos aplicativos.

- Relatório em `data/`:
    - `relatorio_analise.md`: Relatório em formato Markdown com os resultados da análise.

## Funcionalidades

- `Carregamento de Dados`: Lê dados de um arquivo JSON.
- `Preparação de Dados`: Filtra e organiza dados relevantes em um DataFrame.
- `Análise de Concorrência`: Calcula a pontuação média e as melhores/piores posições dos aplicativos.
- `Variação de Posição`: Analisa a variação de posição dos aplicativos ao longo de um período específico.
- `Geração de Gráficos`: Cria e salva gráficos para visualização dos dados.
- `Relatório em Markdown`: Gera um relatório detalhado com os resultados da análise.