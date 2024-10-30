import requests
from dotenv import load_dotenv
import os
import time
import json
from datetime import datetime

class RankAPI:
    def __init__(self, token, log_file):
        self.token = token
        self.log_file = log_file

    def log_error(self, message):
        """Registra mensagens de erro em um arquivo de log."""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now()} - {message}\n")

    def get_changes_log(self, app_id, store, start_date, end_date, retries=3):
        url = f"https://api.rankmyapp.com/v1/apps/{app_id}/{store}/changes-log"
        headers = {
            "rankapi-token": self.token
        }
        params = {
            "store": store,
            "startDate": start_date,
            "endDate": end_date
        }
        
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=headers, params=params, timeout=10)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    self.log_error(f"Erro de autenticação para {app_id}. Verifique o token.")
                    return None
                elif response.status_code == 429:
                    self.log_error(f"Limite de taxa atingido para {app_id}. Tentando novamente...")
                    time.sleep(5)
                else:
                    self.log_error(f"Erro ao consultar {app_id}: {response.status_code} - {response.text}")
                    return None
            
            except requests.exceptions.Timeout:
                self.log_error(f"Timeout ao tentar acessar {app_id}. Tentando novamente...")
            except requests.exceptions.RequestException as e:
                self.log_error(f"Erro de rede ao consultar {app_id}: {e}")
            
            time.sleep(1)
        
        self.log_error(f"Falha ao consultar {app_id} após {retries} tentativas.")
        return None

    def validate_data(self, data):
        """Valida se os dados retornados pela API estão no formato esperado."""
        if not isinstance(data, dict):
            self.log_error("Dados retornados não estão no formato esperado (dicionário).")
            return False

        # Verifica se a chave 'content' está presente e é uma lista
        content = data.get('content')
        if not content or not isinstance(content, list):
            self.log_error("Chave 'content' ausente ou não é uma lista.")
            return False

        # Validar cada item em 'content'
        for item in content:
            if not isinstance(item, dict):
                self.log_error("Um dos itens em 'content' não está no formato esperado (dicionário).")
                return False
            
            changes = item.get('changes')
            if changes is None:
                self.log_error("Chave 'changes' ausente em um item de 'content'.")
                return False
            elif not isinstance(changes, list):
                self.log_error("O valor da chave 'changes' deve ser uma lista.")
                return False

            for change in changes:
                if not isinstance(change, dict):
                    self.log_error("Uma das mudanças não está no formato esperado (dicionário).")
                    return False
                
                expected_keys = ['_id', 'date', 'field', 'previousValue', 'currentValue']
                for key in expected_keys:
                    if key not in change or change[key] is None:
                        self.log_error(f"Chave inválida ou nula encontrada em uma mudança: {key}")
                        return False

        return True

class AppConsultant:
    def __init__(self, api):
        self.api = api

    def consult_apps(self, apps, store, start_date, end_date):
        results = {}
        for app_id in apps:
            data = self.api.get_changes_log(app_id, store, start_date, end_date)
            if data and self.api.validate_data(data):
                results[app_id] = data
        return results

def save_results(results, filename):
    """Salva os resultados em um arquivo JSON."""
    os.makedirs('data', exist_ok=True)
    with open(f"data/{filename}", 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    # Carregar variáveis de ambiente do arquivo .env
    load_dotenv()
    RANKAPI_TOKEN = os.getenv("RANKAPI_TOKEN")

    if not RANKAPI_TOKEN:
        print("Token da API não encontrado. Verifique suas variáveis de ambiente.")
        exit(1)

    # Definir o arquivo de log e verificar/criar a pasta de logs
    os.makedirs('logs', exist_ok=True)
    log_file = 'logs/api_errors.log'

    # IDs dos aplicativos
    apps_apple = [
        "br.com.bradescora.app",
        "com.itau.iphone.varejo",
        "br.com.Neon",
        "com.bb.bbapp",
        "com.nu.iphone"
    ]
    apps_google = [
        "com.itau",
        "com.bradesco",
        "com.nu.production",
        "br.com.neon",
        "br.com.bb.android"
    ]

    # Intervalo de datas
    start_date = "2023-08-01"
    end_date = "2023-08-07"

    # Inicializa a API e o consultor de aplicativos
    rank_api = RankAPI(RANKAPI_TOKEN, log_file)
    consultant = AppConsultant(rank_api)

    # Consultar e salvar resultados para aplicativos da Apple
    apple_results = consultant.consult_apps(apps_apple, "apple", start_date, end_date)
    save_results(apple_results, "changeslog_apple_results.json")

    # Consultar e salvar resultados para aplicativos do Google
    google_results = consultant.consult_apps(apps_google, "google", start_date, end_date)
    save_results(google_results, "changeslog_google_results.json")
