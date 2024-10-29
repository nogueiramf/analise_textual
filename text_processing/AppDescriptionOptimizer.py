#!/usr/bin/env python3
import json
import os
import logging
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("logs/app.log", encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class ASOKeywordAnalyzer:
    """Classe responsável por analisar palavras-chave e densidade em descrições de aplicativos para ASO."""
    
    def __init__(self):
        """Inicializa o ASOKeywordAnalyzer, configura NLTK e define caminhos para arquivos de dados."""
        logger.info("Iniciando ASOKeywordAnalyzer")
        try:
            # Verifica se os pacotes NLTK necessários estão disponíveis, senão os baixa
            nltk.data.find('corpora/stopwords')
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            logger.info("Baixando recursos do NLTK...")
            nltk.download('stopwords')
            nltk.download('punkt')

        # Carregar stopwords em português
        self.stop_words = set(stopwords.words('portuguese'))

        # Caminhos dos arquivos
        self.data_path = os.path.join('data', 'stores.json')  # Arquivo JSON com dados dos aplicativos
        self.report_path = os.path.join('data', 'report_aso.md')  # Arquivo de saída em markdown

        logger.info("ASOKeywordAnalyzer inicializado com sucesso")

    def analyze_word_density(self, text):
        """Analisa a densidade de todas as palavras no texto, excluindo stopwords."""
        logger.info("Iniciando análise de densidade de palavras")

        # Tokenização do texto
        tokens = word_tokenize(text.lower())

        # Remove pontuação e números
        words = [word for word in tokens if word.isalnum()]

        # Conta total de palavras
        total_words = len(words)
        logger.info(f"Total de palavras encontradas: {total_words}")

        # Conta frequência de cada palavra
        word_counts = Counter(words)

        # Calcula densidade para cada palavra
        densities = {
            word: {
                'contagem': count,
                'densidade': (count / total_words) * 100
            }
            for word, count in word_counts.items()
            if word not in self.stop_words
        }

        # Ordena por densidade (mais frequentes primeiro)
        sorted_densities = dict(sorted(
            densities.items(),
            key=lambda x: x[1]['densidade'],
            reverse=True
        ))

        logger.info(f"Análise de densidade concluída. Encontradas {len(sorted_densities)} palavras únicas")
        return {
            'total_palavras': total_words,
            'densidades': sorted_densities
        }

    def load_data(self):
        """Carrega os dados dos aplicativos de um arquivo JSON."""
        logger.info(f"Tentando carregar dados de: {self.data_path}")
        try:
            # Carregar dados do arquivo JSON
            with open(self.data_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                logger.info(f"Dados carregados com sucesso. {len(data)} apps encontrados")
                return data
        except FileNotFoundError:
            logger.error(f"Arquivo não encontrado: {self.data_path}")
            raise FileNotFoundError(f"Arquivo não encontrado: {self.data_path}")
        except json.JSONDecodeError:
            logger.error("Erro ao decodificar o arquivo JSON")
            raise ValueError("Erro ao decodificar o arquivo JSON")

    def extract_keywords(self, text):
        """Extrai palavras-chave e bigramas de um texto."""
        logger.info("Iniciando extração de palavras-chave")

        # Tokenização do texto
        tokens = word_tokenize(text.lower())

        # Remove stopwords e palavras curtas
        keywords = [word for word in tokens if word.isalnum() and word not in self.stop_words and len(word) > 3]

        # Encontra bigramas
        bigram_measures = BigramAssocMeasures()
        finder = BigramCollocationFinder.from_words(tokens)
        finder.apply_freq_filter(2)
        bigrams = finder.nbest(bigram_measures.pmi, 5)

        logger.info(f"Extração concluída. Encontradas {len(keywords)} palavras-chave e {len(bigrams)} bigramas")
        return {
            'keywords': list(set(keywords)),  # Remove duplicatas
            'bigrams': [' '.join(bigram) for bigram in bigrams]
        }

    def analyze_app(self, app_name, data):
        """Analisa título e descrição de um aplicativo, gerando recomendações baseadas em limites e densidade."""
        logger.info(f"Iniciando análise do app: {app_name}")

        # Análise de densidade de palavras na descrição do aplicativo
        densidade_palavras = self.analyze_word_density(data["descrição"])

        # Estrutura para armazenar a análise
        analysis = {
            "título": {
                "texto": data["titulo"],
                "caracteres": len(data["titulo"]),
                "análise_keywords": self.extract_keywords(data["titulo"])
            },
            "descrição": {
                "caracteres": len(data["descrição"]),
                "análise_keywords": self.extract_keywords(data["descrição"]),
                "análise_densidade": densidade_palavras
            },
            "recomendações": []
        }

        # Limitar o número de palavras-chave na descrição a 10
        analysis["descrição"]["análise_keywords"]["keywords"] = analysis["descrição"]["análise_keywords"]["keywords"][:10]

        # Verificações de limites para cada loja (Apple/Google)
        store = data.get("store", "google")  # Loja padrão é Google
        if store == "apple":
            max_title_length = 30
            max_subtitle_length = 30
        else:  # google
            max_title_length = 50
            max_subtitle_length = 80

        # Recomendações sobre o comprimento do título e descrição
        if analysis["título"]["caracteres"] > max_title_length:
            analysis["recomendações"].append(f"O título excede o limite de {max_title_length} caracteres.")
        if analysis["descrição"]["caracteres"] > 4000 and store == "google":
            analysis["recomendações"].append("A descrição excede o limite de 4000 caracteres para a Google Play Store.")

        # Gera recomendações baseadas na densidade das palavras
        self.generate_density_recommendations(analysis)

        logger.info(f"Análise do app {app_name} concluída")
        return analysis

    def generate_density_recommendations(self, analysis):
        """Gera recomendações com base na densidade de palavras repetidas."""
        logger.info("Gerando recomendações baseadas na densidade")

        densidades = analysis["descrição"]["análise_densidade"]["densidades"]
        total_palavras = analysis["descrição"]["análise_densidade"]["total_palavras"]

        # Verifica palavras que aparecem com muita frequência (>3% de repetição)
        palavras_alta_densidade = [
            palavra for palavra, info in densidades.items()
            if info['densidade'] > 3.0
        ]

        if palavras_alta_densidade:
            analysis["recomendações"].append(
                f"Palavras com alta repetição: {', '.join(palavras_alta_densidade)}"
            )

        logger.info(f"Geradas {len(analysis['recomendações'])} recomendações")

    def save_analysis_to_markdown(self, results):
        """Salva a análise em um arquivo markdown."""
        with open(self.report_path, 'w', encoding='utf-8') as file:
            for app_name, analysis in results.items():
                file.write(f"\n{'=' * 50}\n")
                file.write(f"Análise do App: {app_name}\n")
                file.write(f"{'=' * 50}\n")

                file.write("\n### Análise do Título:\n")
                file.write(f"- Caracteres: {analysis['título']['caracteres']}\n")
                file.write(f"- Palavras-chave: {', '.join(analysis['título']['análise_keywords']['keywords'])}\n")

                file.write("\n### Análise da Descrição:\n")
                file.write(f"- Caracteres: {analysis['descrição']['caracteres']}\n")
                file.write(f"- Total de palavras: {analysis['descrição']['análise_densidade']['total_palavras']}\n")

                file.write("\n### Densidade de Palavras (Top 10):\n")
                densidade_items = list(analysis['descrição']['análise_densidade']['densidades'].items())
                for palavra, info in densidade_items[:10]:
                    file.write(f"- {palavra}: {info['contagem']} ocorrências ({info['densidade']:.2f}%)\n")

                if analysis['recomendações']:
                    file.write("\n### Recomendações:\n")
                    for rec in analysis['recomendações']:
                        file.write(f"- {rec}\n")

def main():
    """Função principal que coordena o processo de análise dos aplicativos."""
    logger.info("Iniciando programa principal")
    try:
        analyzer = ASOKeywordAnalyzer()  # Inicializa o analisador
        app_data = analyzer.load_data()  # Carrega dados dos aplicativos

        # Analisar dados dos apps
        results = {app_name: analyzer.analyze_app(app_name, data)
                   for app_name, data in app_data.items()}

        # Salvar os resultados no arquivo markdown
        analyzer.save_analysis_to_markdown(results)
        logger.info("Programa concluído com sucesso")
    except Exception as e:
        logger.error(f"Erro durante a execução: {str(e)}")
        raise

if __name__ == "__main__":
    main()
