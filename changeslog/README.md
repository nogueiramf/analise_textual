# Análise de Aplicativos com AppAnalysis

Este projeto realiza a análise de dados de aplicativos extraindo informações de um arquivo JSON, realizando análises competitivas e salvando relatórios e gráficos.

## Requisitos

Certifique-se de ter as seguintes bibliotecas instaladas:

- pandas
- matplotlib
- seaborn

Você pode instalar as dependências necessárias com o seguinte comando:

```bash
pip install pandas matplotlib seaborn
```
## Estrutura do Código

### Classe **AppAnalysis**
A classe **AppAnalysis** contém métodos para:

- Carregar dados de um arquivo JSON.
- Preparar os dados para análise.
- Analisar a concorrência entre aplicativos, calculando pontuação média, melhor e pior posição.
- Calcular a variação de posição dos aplicativos ao longo de setembro de 2024.
- Salvar gráficos que ilustram as análises.
- Salvar um relatório em formato Markdown com os resultados das análises.

## Atributos
- **json_file**: Caminho do arquivo JSON contendo os dados.
- **assets_folder**: Pasta onde os gráficos gerados serão salvos.
- **data_folder**: Pasta onde o relatório gerado será salvo.
- **app_data**: Dados carregados do arquivo JSON.
- **df**: DataFrame Pandas com os dados preparados para análise.

## Como Usar
1. Prepare um arquivo JSON com os dados dos aplicativos no formato esperado.
2. Atualize o caminho do arquivo JSON na linha onde a instância de **AppAnalysis** é criada.
3. Execute o script.
```bash
if __name__ == "__main__":
    analysis = AppAnalysis('../data/gplaystore.categoryAppPositionsAllbanks.json')
    analysis.run_analysis()
```
## Resultados

Após a execução, os resultados da análise serão salvos:

    . Gráficos em formato PNG na pasta **assets**.
    . Relatório em formato Markdown na pasta **data**.
```bash
AppAnalysis/
│
├── data/
│   └── gplaystore.categoryAppPositionsAllbanks.json  # Arquivo JSON com os dados dos aplicativos
│
├── assets/  # Pasta para salvar gráficos gerados
│
├── reports/  # Pasta para salvar relatórios gerados
│
├── app_analysis.py  # Código fonte da classe AppAnalysis
├── RankMyAppClient.py y # Script para interagir com a API ou coletar dados
│
├── README.md  # Documentação do projeto
```

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