#Esse segundo script lê os dados do relatório gerado e visualiza gráficos de frequência de atualização e tipos de mudança.

import pandas as pd
import matplotlib.pyplot as plt
import os

# Função para plotar gráficos com base nos dados carregados
def plot_frequency_chart(update_freq, title):
    plt.figure(figsize=(12, 6))
    update_freq.T.plot(ax=plt.gca(), title=title)
    plt.xlabel('Data')
    plt.ylabel('Frequência de Atualizações')
    plt.legend(title='App ID', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Caminho do diretório onde os arquivos CSV foram salvos
current_dir = os.path.dirname(os.path.abspath(__file__))
apple_update_freq = pd.read_csv(os.path.join(current_dir, 'data', 'apple_update_freq.csv'), index_col=0, parse_dates=True)
google_update_freq = pd.read_csv(os.path.join(current_dir, 'data', 'google_update_freq.csv'), index_col=0, parse_dates=True)

# Plotar gráficos de frequência
plot_frequency_chart(apple_update_freq, title='Frequência de Atualizações - Apple Store')
plot_frequency_chart(google_update_freq, title='Frequência de Atualizações - Google Play')
