# import os
# import json

# # Definir o caminho para o arquivo
# file_path = os.path.join('data', 'stores.json')

# # Carregar o arquivo JSON
# with open(file_path, 'r', encoding='utf-8') as f:
#     apps_data = json.load(f)

# # Exibir os dados carregados
# apps_data

import os
import json
import logging

# Configuração do log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Definir o caminho para o arquivo
file_path = os.path.join('data', 'stores.json')

# Verificar se o arquivo existe
if os.path.exists(file_path):
    logging.info(f"Arquivo encontrado: {file_path}")
else:
    logging.error(f"Arquivo não encontrado: {file_path}")

# Carregar o arquivo JSON
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        apps_data = json.load(f)
        logging.info("Arquivo JSON carregado com sucesso.")
except Exception as e:
    logging.error(f"Erro ao carregar o arquivo JSON: {e}")
else:
    # Exibir os dados carregados
    logging.info(f"Dados carregados: {apps_data}")
    print(apps_data)
