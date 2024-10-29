from rake_nltk import Rake
import openai
from text_processing.loader import apps_data
from dotenv import load_dotenv
import os
import nltk
from nltk.corpus import stopwords

# Carregar variáveis do arquivo .env
load_dotenv()

# Recuperar a chave da API do OpenAI do arquivo .env
openai_api_key = os.getenv('OPENAI_API_KEY')

# Baixar stop words do NLTK (se ainda não estiverem baixadas)
nltk.download('stopwords')

# Obter stop words em português
stop_words = set(stopwords.words('portuguese'))

# Função para extrair palavras-chave usando RAKE
def extrair_palavras_chave_rake(descricao):
    r = Rake(language='portuguese')  # Configura o Rake para português
    r.extract_keywords_from_text(descricao)
    
    # Obter as palavras-chave ordenadas por relevância
    palavras_chave = r.get_ranked_phrases()
    
    # Filtrar palavras-chave para remover duplicatas e stop words
    palavras_chave_filtradas = set()
    
    for frase in palavras_chave:
        # Dividir a frase em palavras
        palavras = frase.split()
        # Adicionar palavras que não estão na lista de stop words
        for palavra in palavras:
            if palavra.lower() not in stop_words:
                palavras_chave_filtradas.add(palavra.lower())
    
    return list(palavras_chave_filtradas)

# Processar as descrições de cada aplicativo e extrair palavras-chave
for app, data in apps_data.items():
    descricao = data['descrição']
    
    print(f"App: {app}")
    
    # Extrair palavras-chave usando RAKE
    palavras_chave = extrair_palavras_chave_rake(descricao)
    
    print("Palavras-chave filtradas:")
    print(palavras_chave)
    print()
