from pymongo import MongoClient
from datetime import datetime
import logging
import pandas as pd
from dotenv import load_dotenv
import os
import json

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração de logs para capturar informações e possíveis erros
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MongoDBConnector:
    """
    Classe para gerenciar a conexão e operações com um banco de dados MongoDB.

    Attributes:
        mongo_uri (str): URI de conexão com o MongoDB.
        db_name (str): Nome do banco de dados no MongoDB.
        client (MongoClient): Cliente MongoDB.
        db (Database): Instância do banco de dados.
    """
    
    def __init__(self, mongo_uri, db_name):
        """
        Inicializa a conexão MongoDB com os parâmetros de URI e nome do banco de dados.
        
        Args:
            mongo_uri (str): URI de conexão com o MongoDB.
            db_name (str): Nome do banco de dados.
        """
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        """Estabelece uma conexão com o MongoDB e inicializa o banco de dados."""
        try:
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client[self.db_name]
            logging.info("Conexão com MongoDB estabelecida com sucesso")
        except Exception as e:
            logging.error(f"Erro ao conectar ao MongoDB: {e}")

    def close(self):
        """Fecha a conexão com o MongoDB."""
        try:
            self.client.close()
            logging.info("Conexão com MongoDB fechada.")
        except Exception as e:
            logging.error(f"Erro ao fechar conexão com MongoDB: {e}")

    def query_data(self, collection_name, query):
        """
        Consulta uma coleção específica no MongoDB com uma query fornecida.
        
        Args:
            collection_name (str): Nome da coleção MongoDB.
            query (dict): Query para filtrar os dados.
        
        Returns:
            list: Lista de documentos retornados pela consulta ou uma lista vazia se nenhum dado for encontrado.
        """
        try:
            collection = self.db[collection_name]
            data = list(collection.find(query))
            if data:
                logging.info("Dados recuperados do MongoDB")
                return data
            else:
                logging.warning("Nenhum resultado encontrado para a query.")
                return []
        except Exception as e:
            logging.error(f"Erro ao consultar o MongoDB: {e}")
            return []

def save_to_json(data, file_path):
    """
    Salva os dados fornecidos em um arquivo JSON.

    Args:
        data (list): Dados a serem salvos.
        file_path (str): Caminho do arquivo JSON onde os dados serão salvos.
    """
    try:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, default=str)
        logging.info(f"Dados salvos em {file_path}")
    except Exception as e:
        logging.error(f"Erro ao salvar dados em JSON: {e}")

if __name__ == "__main__":
    # Carrega as variáveis de ambiente para acessar o MongoDB
    mongo_uri_google = os.getenv("MONGO_URI_GOOGLE")
    db_name_google = 'gplaystore'
    collection_name_google = 'categoryAppPositions'

    # Define a query para buscar dados com base no appId e no intervalo de datas
    query = {
        "positions.appId": {"$in": ["com.nu.production", "com.picpay", "com.bradesco", "com.itau"]},
        "date": {
            "$gte": datetime(2024, 9, 1, 0, 0),
            "$lt": datetime(2024, 10, 1, 0, 0)
        },
        "lang": "pt-BR"
    }

    # Cria uma instância do conector MongoDB, conecta e consulta dados
    connector = MongoDBConnector(mongo_uri_google, db_name_google)
    connector.connect()
    result = connector.query_data(collection_name_google, query)
    connector.close()

    # Salva os resultados em um arquivo JSON na pasta 'data'
    output_file_path = '../data/google_play_data.json'
    save_to_json(result, output_file_path)

    # Caso queira visualizar os resultados diretamente no console, descomente a linha abaixo
    # print(result)
