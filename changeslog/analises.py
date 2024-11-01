
# import json
# import pandas as pd
# import os

# def load_data():
#     # Obtém o diretório atual onde o script está sendo executado
#     current_dir = os.path.dirname(os.path.abspath(__file__))
    
#     print(f"Diretório atual: {current_dir}")
    
#     try:
#         apple_path = os.path.join(current_dir, 'data', 'changeslog_apple_results.json')
#         print(f"Tentando abrir arquivo Apple em: {apple_path}")
        
#         with open(apple_path, 'r', encoding='utf-8') as f:
#             apple_data = json.load(f)
#             print("Dados do Apple carregados com sucesso.")
#     except FileNotFoundError:
#         print(f"Arquivo não encontrado: {apple_path}")
#         apple_data = None
#     except json.JSONDecodeError:
#         print(f"Erro ao decodificar o arquivo JSON do Apple: {apple_path}")
#         apple_data = None
    
#     try:
#         google_path = os.path.join(current_dir, 'data', 'changeslog_google_results.json')
#         print(f"Tentando abrir arquivo Google em: {google_path}")
        
#         with open(google_path, 'r', encoding='utf-8') as f:
#             google_data = json.load(f)
#             print("Dados do Google carregados com sucesso.")
#     except FileNotFoundError:
#         print(f"Arquivo não encontrado: {google_path}")
#         google_data = None
#     except json.JSONDecodeError:
#         print(f"Erro ao decodificar o arquivo JSON do Google: {google_path}")
#         google_data = None
    
#     return apple_data, google_data

# def analyze_data(apple_data, google_data):
#     if apple_data is None and google_data is None:
#         print("Nenhum dado disponível para análise.")
#         return

#     analyses = []

#     # Função auxiliar para extrair informações de forma segura
#     def safe_get(dict_obj, key, default="Não disponível"):
#         return dict_obj.get(key, default)

#     # Análise para dados do Apple
#     if apple_data:
#         print("\nAnálise dos dados da Apple:")
#         print("\nEstrutura dos dados Apple:", apple_data.keys())  # Debug
        
#         for app, details in apple_data.items():
#             try:
#                 num_changes = len(details['content'])
#                 analyses.append(f"\nAplicativo: {app}")
#                 analyses.append(f"Número de alterações: {num_changes}")
                
#                 print(f"\nEstrutura do conteúdo para {app}:")  # Debug
#                 if len(details['content']) > 0:
#                     print(details['content'][0].keys())  # Debug
                
#                 for change in details['content']:
#                     version = safe_get(change, 'version', 'Versão não especificada')
#                     changes_summary = safe_get(change, 'changes', 'Alterações não especificadas')
#                     analyses.append(f"Versão: {version}")
#                     analyses.append(f"Alterações: {changes_summary}")
                    
#             except KeyError as e:
#                 print(f"Erro ao processar dados do app {app}: {str(e)}")
#                 continue

#     # Análise para dados do Google
#     if google_data:
#         print("\nAnálise dos dados do Google:")
#         print("\nEstrutura dos dados Google:", google_data.keys())  # Debug
        
#         for app, details in google_data.items():
#             try:
#                 num_changes = len(details['content'])
#                 analyses.append(f"\nAplicativo: {app}")
#                 analyses.append(f"Número de alterações: {num_changes}")
                
#                 print(f"\nEstrutura do conteúdo para {app}:")  # Debug
#                 if len(details['content']) > 0:
#                     print(details['content'][0].keys())  # Debug
                
#                 for change in details['content']:
#                     version = safe_get(change, 'version', 'Versão não especificada')
#                     changes_summary = safe_get(change, 'changes', 'Alterações não especificadas')
#                     analyses.append(f"Versão: {version}")
#                     analyses.append(f"Alterações: {changes_summary}")
                    
#             except KeyError as e:
#                 print(f"Erro ao processar dados do app {app}: {str(e)}")
#                 continue

#     # Imprimir todas as análises
#     print("\nResultados da análise:")
#     for analysis in analyses:
#         print(analysis)

# def main():
#     print("Iniciando análise de dados...")
#     apple_data, google_data = load_data()
    
#     # Debug: Imprimir estrutura dos dados
#     if apple_data:
#         print("\nEstrutura do arquivo Apple:")
#         for app in apple_data:
#             print(f"App: {app}")
#             if len(apple_data[app]['content']) > 0:
#                 print("Exemplo de conteúdo:", apple_data[app]['content'][0])
    
#     if google_data:
#         print("\nEstrutura do arquivo Google:")
#         for app in google_data:
#             print(f"App: {app}")
#             if len(google_data[app]['content']) > 0:
#                 print("Exemplo de conteúdo:", google_data[app]['content'][0])
    
#     analyze_data(apple_data, google_data)
#     print("\nAnálise concluída.")

# if __name__ == '__main__':
#     main()

import json
import pandas as pd
import os
from datetime import datetime
from collections import Counter

def load_data():
    # Função para carregar os dados
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    try:
        apple_path = os.path.join(current_dir, 'data', 'changeslog_apple_results.json')
        with open(apple_path, 'r', encoding='utf-8') as f:
            apple_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        apple_data = None
    
    try:
        google_path = os.path.join(current_dir, 'data', 'changeslog_google_results.json')
        with open(google_path, 'r', encoding='utf-8') as f:
            google_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        google_data = None
    
    return apple_data, google_data

def analyze_versions(data):
    analyses = []
    frequencies = {}
    history = {}

    for app_id, changes in data.items():
        frequencies[app_id] = len(changes['content'])
        
        # Criar histórico de versões
        history[app_id] = []
        for change in changes['content']:
            # Verifica se 'alteracoes' está presente e é uma lista
            if 'alteracoes' in change and isinstance(change['alteracoes'], list):
                for alteration in change['alteracoes']:
                    # Extrai data e campo, se disponíveis
                    date = alteration.get('date', 'Data não disponível')
                    field = alteration.get('field', 'Campo não especificado')
                    history[app_id].append({"date": date, "field": field})

        # Adiciona informações sobre o aplicativo
        analyses.append(f"### Aplicativo: {app_id}")
        analyses.append(f"Número de atualizações: {frequencies[app_id]}")
        
        # Adiciona linha do tempo
        analyses.append("Histórico de versões:")
        if history[app_id]:  # Verifica se há entradas no histórico
            for entry in history[app_id]:
                analyses.append(f"- **Data**: {entry['date']} | **Campo**: {entry['field']}")
        else:
            analyses.append("- Nenhuma alteração registrada.")
    
    return "\n".join(analyses)




def analyze_changes(data):
    analyses = []
    change_types = {
        'bugs': 0,
        'features': 0,
        'improvements': 0
    }
    total_changes = 0

    for app_id, changes in data.items():
        for change in changes['content']:
            # Supondo que 'changes' é uma lista de dicionários ou strings
            if 'changes' in change:
                # Verifica se 'changes' é uma lista
                if isinstance(change['changes'], list):
                    for change_description in change['changes']:
                        # Se for um dicionário, talvez tenhamos que acessar uma chave específica
                        if isinstance(change_description, dict):
                            # Aqui você deve modificar 'description' para a chave correta que contém o texto
                            description = change_description.get('description', '')
                        else:
                            description = change_description

                        total_changes += 1
                        # Verifica se a descrição menciona 'bug'
                        if 'bug' in description.lower():
                            change_types['bugs'] += 1
                        elif 'feature' in description.lower():
                            change_types['features'] += 1
                        elif 'improvement' in description.lower():
                            change_types['improvements'] += 1

        analyses.append(f"### Aplicativo: {app_id}")
        analyses.append(f"Número total de mudanças: {total_changes}")
        analyses.append("Tipos de mudanças:")
        for change_type, count in change_types.items():
            analyses.append(f"- {change_type.capitalize()}: {count} ({(count / total_changes * 100) if total_changes > 0 else 0:.2f}%)")

    return "\n".join(analyses)


def save_to_markdown(content):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, 'analyses.md')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Resultados da análise salvos em: {output_path}")

def main():
    print("Iniciando análise de dados...")
    apple_data, google_data = load_data()
    
    combined_data = {}
    if apple_data:
        combined_data.update(apple_data)
    if google_data:
        combined_data.update(google_data)

    analysis_results = []
    
    if combined_data:
        analysis_results.append(analyze_versions(combined_data))
        analysis_results.append(analyze_changes(combined_data))
    
    if analysis_results:
        save_to_markdown("\n".join(analysis_results))
    
    print("\nAnálise concluída.")

if __name__ == '__main__':
    main()
