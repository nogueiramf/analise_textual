import json
import os

def load_json(file_path):
    """
    Carrega um arquivo JSON e retorna seu conteúdo como um dicionário.

    Args:
        file_path (str): O caminho do arquivo JSON a ser carregado.

    Returns:
        dict or None: Retorna o conteúdo do arquivo JSON como um dicionário
                      se o carregamento for bem-sucedido, ou None em caso de erro.
    """
    try:
        # Abre o arquivo no modo leitura com codificação UTF-8
        with open(file_path, 'r', encoding='utf-8') as file:
            # Carrega e retorna o conteúdo JSON
            return json.load(file)
    except FileNotFoundError:
        # Trata o erro caso o arquivo não seja encontrado
        print(f"Arquivo não encontrado: {file_path}")
        return None
    except json.JSONDecodeError as e:
        # Trata erros de decodificação JSON
        print(f"Erro de decodificação JSON em {file_path}: {e}")
        return None

# Caminho para os arquivos JSON, ajustado para estar relativo ao local do script
apple_file_path = "data/changeslog_apple_results.json"
google_file_path = "data/changeslog_google_results.json"

# Carregar dados dos arquivos JSON
apple_data = load_json(apple_file_path)
google_data = load_json(google_file_path)

# Exibir conteúdo se os dados forem carregados com sucesso
if apple_data:
    print("\nConteúdo do arquivo Apple:")
    # Imprime os dados formatados em JSON
    print(json.dumps(apple_data, indent=4, ensure_ascii=False))
else:
    print("Falha ao carregar dados do arquivo Apple.")

if google_data:
    print("\nConteúdo do arquivo Google:")
    # Imprime os dados formatados em JSON
    print(json.dumps(google_data, indent=4, ensure_ascii=False))
else:
    print("Falha ao carregar dados do arquivo Google.")
