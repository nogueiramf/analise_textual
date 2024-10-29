# Analisador de Palavras-chave para Descrições de Aplicativos

Este projeto consiste em dois scripts Python: `RakeKeywordExtractor` e `AppDescriptionOptimizer`, que têm como objetivo analisar e otimizar as descrições de aplicativos para melhorar a visibilidade e a descoberta nas lojas de aplicativos.

## Conteúdo do Projeto

- `RakeKeywordExtractor.py`: Script para extrair palavras-chave relevantes de descrições de aplicativos utilizando o algoritmo RAKE (Rapid Automatic Keyword Extraction).
- `AppDescriptionOptimizer.py`: Script que analisa a densidade de palavras, extrai palavras-chave e fornece recomendações para otimização das descrições de aplicativos.

## Requisitos

Certifique-se de que você tenha as seguintes bibliotecas instaladas:

```bash
pip install nltk rake-nltk python-dotenv
```
## Configuração
1- **Configuração da API do OpenAI**: Certifique-se de ter uma chave de API do OpenAI e armazene-a em um arquivo `.env` na raiz do seu projeto:
```bash
OPENAI_API_KEY=your_api_key_here
```
2- **Estrutura de Dados**: Os scripts assumem que você possui um arquivo JSON com os dados dos aplicativos no seguinte formato:
```bash
{
    "app_name": {
        "titulo": "Título do App",
        "descrição": "Descrição do App",
        "store": "google"  // ou "apple"
    },
    ...
}
```
## Descrição dos Scripts
**RakeKeywordExtractor**
Este script utiliza a biblioteca `rake-nltk` para extrair palavras-chave de descrições de aplicativos. A seguir estão as principais funcionalidades:

- Extrair Palavras-Chave: Utiliza o algoritmo RAKE para identificar as frases mais relevantes na descrição do aplicativo.
- Filtragem de Stop Words: Remove palavras comuns (stop words) e duplicatas das palavras-chave extraídas.
- Uso de NLTK: Carrega as stop words em português do NLTK para garantir a precisão na extração.

### Exemplo de uso:
```bash
for app, data in apps_data.items():
    descricao = data['descrição']
    palavras_chave = extrair_palavras_chave_rake(descricao)
    print(palavras_chave)
```
## AppDescriptionOptimizer
Este script analisa a descrição e o título de aplicativos, focando em otimizações para lojas de aplicativos (ASO). As principais funcionalidades incluem:

- Análise de Densidade de Palavras: Calcula a densidade de palavras, excluindo stop words, e gera um relatório.
- Extração de Palavras-Chave e Bigramas: Extrai palavras-chave e bigramas da descrição e do título.
- Geração de Recomendações: Fornece recomendações sobre o comprimento do título e da descrição, além de alertar sobre palavras repetidas em alta densidade.
Exemplo de uso:
```bash
analyzer = ASOKeywordAnalyzer()
app_data = analyzer.load_data()
results = {app_name: analyzer.analyze_app(app_name, data) for app_name, data in app_data.items()}
analyzer.save_analysis_to_markdown(results)
```
## Execução
Para executar os scripts, utilize o seguinte comando:
```bash
python RakeKeywordExtractor.py
python AppDescriptionOptimizer.py
```
## Logs
Os logs de execução do `AppDescriptionOptimizer` serão salvos em um arquivo chamado app.log na pasta `logs`.