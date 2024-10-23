import os
import json

# Definir o caminho para o arquivo
file_path = os.path.join('data', 'stores.json')

# Carregar o arquivo JSON
with open(file_path, 'r', encoding='utf-8') as f:
    apps_data = json.load(f)

# Exibir os dados carregados
apps_data