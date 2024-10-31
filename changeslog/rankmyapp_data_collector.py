import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import os
from dotenv import load_dotenv
import time
from dataclasses import dataclass

# Configurações da aplicação
@dataclass
class Config:
    MAX_RETRIES: int = 3  # Número máximo de tentativas em caso de falha
    TIMEOUT: int = 10      # Tempo limite para requisições
    RETRY_DELAY: int = 1   # Tempo de espera entre tentativas
    RATE_LIMIT_DELAY: int = 5  # Tempo de espera em caso de limite de taxa
    CACHE_TTL: int = 3600  # Tempo de expiração do cache (1 hora)

class RankAPIException(Exception):
    """Exceção customizada para erros relacionados à API"""
    pass

class APICache:
    """Classe para gerenciamento de cache das respostas da API."""
    def __init__(self):
        self.cache: Dict[str, Dict[str, Any]] = {}
    
    def get(self, key: str) -> Optional[Dict]:
        """Obtém dados do cache se ainda não expiraram."""
        if key in self.cache:
            cache_data = self.cache[key]
            if time.time() < cache_data['expires']:
                return cache_data['value']
            del self.cache[key]  # Remove cache expirado
        return None
    
    def set(self, key: str, value: Dict, ttl: int = Config.CACHE_TTL) -> None:
        """Armazena dados no cache com um tempo de expiração especificado."""
        self.cache[key] = {
            'value': value,
            'expires': time.time() + ttl
        }

class RateLimiter:
    """Classe para controlar a taxa de chamadas à API."""
    def __init__(self, calls_per_second: float = 1.0):
        self.calls_per_second = calls_per_second
        self.last_call = 0
    
    async def wait(self) -> None:
        """Aguarda até que seja possível fazer a próxima chamada."""
        elapsed = time.time() - self.last_call
        if elapsed < 1/self.calls_per_second:
            await asyncio.sleep(1/self.calls_per_second - elapsed)
        self.last_call = time.time()

class RankAPI:
    """Classe para interagir com a API de mudanças de aplicativos."""
    def __init__(self, token: str):
        self.token = token
        self.cache = APICache()
        self.rate_limiter = RateLimiter()
        
        # Configurar logging para registrar erros da API
        logging.basicConfig(
            filename='logs/api_errors.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def _get_cache_key(self, app_id: str, store: str, start_date: str, end_date: str) -> str:
        """Gera uma chave única para o cache baseado nos parâmetros fornecidos."""
        return f"{app_id}:{store}:{start_date}:{end_date}"

    async def get_changes_log(
        self, 
        app_id: str, 
        store: str, 
        start_date: str, 
        end_date: str,
        retries: int = Config.MAX_RETRIES
    ) -> Optional[Dict]:
        """
        Busca logs de mudanças de forma assíncrona para um aplicativo específico.
        
        Parâmetros:
            app_id: ID do aplicativo.
            store: Loja onde o aplicativo está disponível.
            start_date: Data de início para o log.
            end_date: Data de fim para o log.
            retries: Número de tentativas em caso de falha.
        
        Retorna:
            Um dicionário com os logs de mudanças ou None se houver falha.
        """
        cache_key = self._get_cache_key(app_id, store, start_date, end_date)
        
        # Verificar se os dados estão em cache
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data

        url = f"https://api.rankmyapp.com/v1/apps/{app_id}/{store}/changes-log"
        headers = {"rankapi-token": self.token}
        params = {
            "store": store,
            "startDate": start_date,
            "endDate": end_date
        }

        async with aiohttp.ClientSession() as session:
            for attempt in range(retries):
                try:
                    await self.rate_limiter.wait()  # Aguarda para respeitar o limite de taxa
                    
                    async with session.get(
                        url, 
                        headers=headers, 
                        params=params, 
                        timeout=Config.TIMEOUT
                    ) as response:
                        if response.status == 200:
                            data = await response.json()  # Recebe a resposta em formato JSON
                            if self.validate_data(data):  # Valida os dados recebidos
                                self.cache.set(cache_key, data)  # Armazena no cache
                                return data
                        elif response.status == 401:
                            raise RankAPIException(f"Erro de autenticação para {app_id}")
                        elif response.status == 429:
                            self.logger.warning(f"Rate limit atingido para {app_id}")
                            await asyncio.sleep(Config.RATE_LIMIT_DELAY)  # Espera se atingir o limite de taxa
                        else:
                            self.logger.error(
                                f"Erro ao consultar {app_id}: {response.status}"
                            )
                
                except asyncio.TimeoutError:
                    self.logger.warning(f"Timeout ao consultar {app_id}")
                except Exception as e:
                    self.logger.error(f"Erro inesperado ao consultar {app_id}: {str(e)}")
                
                await asyncio.sleep(Config.RETRY_DELAY)  # Espera antes de tentar novamente
            
            self.logger.error(f"Falha ao consultar {app_id} após {retries} tentativas")
            return None

    def validate_data(self, data: Dict) -> bool:
        """Valida se os dados retornados pela API estão no formato esperado.
        
        Parâmetros:
            data: Dados recebidos da API.
        
        Retorna:
            True se os dados estão válidos, False caso contrário.
        """
        try:
            if not isinstance(data, dict):
                raise ValueError("Dados não estão no formato de dicionário")

            content = data.get('content')
            if not content or not isinstance(content, list):
                raise ValueError("Chave 'content' ausente ou não é uma lista")

            for item in content:
                if not isinstance(item, dict):
                    raise ValueError("Item em 'content' não é um dicionário")
                
                changes = item.get('changes')
                if not isinstance(changes, list):
                    raise ValueError("'changes' não é uma lista")

                for change in changes:
                    if not isinstance(change, dict):
                        raise ValueError("Mudança não é um dicionário")
                    
                    required_keys = ['_id', 'date', 'field', 'previousValue', 'currentValue']
                    missing_keys = [key for key in required_keys if key not in change]
                    if missing_keys:
                        raise ValueError(f"Chaves ausentes: {missing_keys}")

            return True
        
        except ValueError as e:
            self.logger.error(f"Erro na validação dos dados: {str(e)}")
            return False

class AppConsultant:
    """Classe para consultar múltiplos aplicativos usando a API."""
    def __init__(self, api: RankAPI):
        self.api = api

    async def consult_apps(
        self, 
        apps: List[str], 
        store: str, 
        start_date: str, 
        end_date: str
    ) -> Dict[str, Any]:
        """Consulta múltiplos aplicativos de forma assíncrona.
        
        Parâmetros:
            apps: Lista de IDs de aplicativos a serem consultados.
            store: Loja onde os aplicativos estão disponíveis.
            start_date: Data de início para a consulta.
            end_date: Data de fim para a consulta.
        
        Retorna:
            Um dicionário com os resultados das consultas.
        """
        tasks = [
            self.api.get_changes_log(app_id, store, start_date, end_date)
            for app_id in apps
        ]
        results = await asyncio.gather(*tasks)
        return {
            app_id: result 
            for app_id, result in zip(apps, results) 
            if result is not None
        }

def save_results(results: Dict[str, Any], filename: str) -> None:
    """Salva os resultados em um arquivo JSON.
    
    Parâmetros:
        results: Dicionário com os resultados a serem salvos.
        filename: Nome do arquivo onde os resultados serão salvos.
    """
    os.makedirs('data', exist_ok=True)  # Cria o diretório se não existir
    with open(f"data/{filename}", 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

async def main():
    # Carregar variáveis de ambiente
    load_dotenv()
    RANKAPI_TOKEN = os.getenv("RANKAPI_TOKEN")

    if not RANKAPI_TOKEN:
        logging.error("Token da API não encontrado")
        return

    # Criar diretório de logs
    os.makedirs('logs', exist_ok=True)

    # IDs dos aplicativos para consulta
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

    # Intervalo de datas para consulta
    start_date = "2024-09-01"
    end_date = "2024-09-30"

    # Inicializar a API e o consultor
    rank_api = RankAPI(RANKAPI_TOKEN)
    consultant = AppConsultant(rank_api)

    # Consultar aplicativos de forma assíncrona
    apple_results = await consultant.consult_apps(
        apps_apple, "apple", start_date, end_date
    )
    google_results = await consultant.consult_apps(
        apps_google, "google", start_date, end_date
    )

    # Salvar resultados em arquivos JSON
    save_results(apple_results, "changeslog_apple_results.json")
    save_results(google_results, "changeslog_google_results.json")

if __name__ == "__main__":
    asyncio.run(main())
