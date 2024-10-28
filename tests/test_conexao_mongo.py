import logging
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Configurar o logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connect_to_mongo():
    load_dotenv()  # Carregar as variáveis de ambiente do arquivo .env

    # Obtendo a URI do MongoDB
    mongo_uri = os.getenv('MONGO_URI_GOOGLE')  # Altere para MONGO_URI_APPLE se necessário

    logger.info("Conectando ao MongoDB...")
    try:
        client = MongoClient(mongo_uri)
        db = client['gplaystore']  # Nome do seu banco de dados
        logger.info("Conexão estabelecida com sucesso!")
        return db
    except Exception as e:
        logger.error(f"Erro ao conectar ao MongoDB: {e}")
        return None

def check_permissions(db):
    try:
        status = db.command("connectionStatus")
        user_info = status['authInfo']['authenticatedUsers']
        
        logger.info("Informações do usuário autenticado:")
        for user in user_info:
            logger.info(f"Usuário: {user['user']}, Database: {user['db']}, Funções: {user['roles']}")
    except Exception as e:
        logger.error(f"Erro ao verificar permissões: {e}")

# Defina essa função se precisar listar permissões
# def list_permissions(db):
#     pass  # Implementação da função para listar permissões

def main():
    db = connect_to_mongo()  # Conectar ao MongoDB

    if db is not None:
        logger.info("Conexão com o banco de dados é bem-sucedida!")
        check_permissions(db)  # Verificar permissões
        # list_permissions(db)  # Descomente se a função for definida
    else:
        logger.error("Falha ao conectar ao banco de dados.")

if __name__ == "__main__":
    main()
