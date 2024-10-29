import logging
import requests
import os
import json
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do logging para registrar informações e erros
logging.basicConfig(level=logging.INFO)

class API:
    """Classe para interagir com a API RankMyApp."""

    def __init__(self):
        """Inicializa a classe API com a URL base e o token de autenticação."""
        self.base_url = "https://api.rankmyapp.com/v1/apps"
        self.token = os.getenv("RANKAPI_TOKEN")

    def get_app_details(self, app_id, store, country):
        """
        Obtém os detalhes de um aplicativo.

        Args:
            app_id (str): ID do aplicativo.
            store (str): Nome da loja (ex: 'google' ou 'apple').
            country (str): Código do país (ex: 'BR').

        Returns:
            dict: Detalhes do aplicativo em formato JSON ou None em caso de erro.
        """
        url = f"{self.base_url}/{app_id}/detail?store={store}&country={country}"
        headers = {
            "rankapi-token": self.token
        }

        logging.info(f"URL: {url}")

        try:
            # Faz a requisição GET para a API
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
            return response.json()  # Retorna a resposta em formato JSON
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")  # Log de erro para falhas HTTP
        except Exception as err:
            logging.error(f"An error occurred: {err}")  # Log de erro para outras exceções
        return None  # Retorna None em caso de erro

    def get_changes_log(self, app_id, store, start_date, end_date):
        """
        Obtém o log de alterações de um aplicativo em um intervalo de datas.

        Args:
            app_id (str): ID do aplicativo.
            store (str): Nome da loja (ex: 'google' ou 'apple').
            start_date (str): Data de início no formato 'YYYY-MM-DD'.
            end_date (str): Data de fim no formato 'YYYY-MM-DD'.

        Returns:
            dict: Log de alterações em formato JSON ou None em caso de erro.
        """
        url = f"{self.base_url}/{app_id}/{store}/changes-log?store={store}&startDate={start_date}&endDate={end_date}"
        headers = {
            "rankapi-token": self.token
        }

        logging.info(f"URL: {url}")

        try:
            # Faz a requisição GET para a API
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
            return response.json()  # Retorna a resposta em formato JSON
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")  # Log de erro para falhas HTTP
        except Exception as err:
            logging.error(f"An error occurred: {err}")  # Log de erro para outras exceções
        return None  # Retorna None em caso de erro

# Função para salvar dados em um arquivo JSON
def save_to_json(data, filename):
    """
    Salva os dados em um arquivo JSON.

    Args:
        data (dict): Dados a serem salvos.
        filename (str): Nome do arquivo para salvar os dados.
    """
    # Verifica se o diretório 'data' existe, caso contrário, cria
    if not os.path.exists('data'):
        os.makedirs('data')
    # Salva os dados em um arquivo JSON com indentação
    with open(os.path.join('data', filename), 'w') as file:
        json.dump(data, file, indent=4)

# Exemplo de uso
if __name__ == "__main__":
    api = API()  # Cria uma instância da classe API
    # Obtém detalhes do aplicativo
    app_details = api.get_app_details('com.itau', 'google', 'BR')
    # Obtém o log de alterações do aplicativo
    changes_log = api.get_changes_log('com.itau', 'google', '2024-09-01', '2024-09-30')

    # Salva os detalhes do aplicativo em um arquivo JSON, se obtidos
    if app_details:
        save_to_json(app_details, 'app_details.json')
    # Salva o log de alterações em um arquivo JSON, se obtido
    if changes_log:
        save_to_json(changes_log, 'changesLog.json')
