##Analisa os dados coletados do mongodb

# -*- coding: utf-8 -*-
import json
import pandas as pd
import os

class AppAnalysis:
    """
    Classe para análise de dados de aplicativos, extraindo informações de um arquivo JSON,
    realizando análises competitivas e salvando relatórios.

    Attributes:
        json_file (str): Caminho do arquivo JSON contendo os dados.
        data_folder (str): Pasta onde o relatório gerado será salvo.
        app_data (list): Dados carregados do arquivo JSON.
        df (DataFrame): DataFrame Pandas com os dados preparados para análise.
    """
    
    def __init__(self, json_file, data_folder='data'):
        """
        Inicializa a classe AppAnalysis com o caminho do arquivo JSON e a pasta de saída.

        Args:
            json_file (str): Caminho para o arquivo JSON.
            data_folder (str): Pasta para salvar os relatórios gerados. Default é 'data'.
        """
        self.json_file = json_file
        self.data_folder = data_folder
        self.app_data = []
        self.df = None
        self.create_folders()

    def create_folders(self):
        """Cria a pasta de saída (data) caso não exista."""
        os.makedirs(self.data_folder, exist_ok=True)

    def load_data(self):
        """Carrega o conteúdo do arquivo JSON especificado no atributo json_file."""
        with open(self.json_file, 'r', encoding='utf-8') as file:
            self.app_data = json.load(file)

    def prepare_data(self):
        """
        Extrai dados relevantes do JSON e cria um DataFrame Pandas.

        Filtra dados de aplicativos específicos, com informações de score,
        posição, data, categoria e outras características relevantes.
        """
        results = []
        app_id_itau = 'com.itau'
        concorrentes = ['com.nu.production', 'com.picpay', 'com.bradesco', 'com.mercadopago.wallet', 'br.com.intermedium']

        for item in self.app_data:
            for position in item.get('positions', []):
                app_id = position.get('appId')
                if app_id in [app_id_itau] + concorrentes:
                    results.append({
                        'app_id': app_id,
                        'score': position['score'],
                        'position': position['position'],
                        'date': item['date']['$date'],
                        'category': item['category'],
                        'country': item['country'],
                        'lang': item['lang'],
                        'store': item['store'],
                    })

        # Criar um DataFrame com os dados relevantes
        self.df = pd.DataFrame(results)

    def analyze_competition(self):
        """
        Realiza análise de concorrência, calculando pontuação média, melhor e pior posição de cada app.

        Returns:
            DataFrame: DataFrame com resultados agregados por app_id.
        """
        return self.df.groupby('app_id').agg(
            pontuacao_media=('score', 'mean'),
            melhor_posicao=('position', 'min'),
            pior_posicao=('position', 'max')
        ).reset_index()

    def position_variation(self):
        """
        Calcula a variação de posição dos aplicativos ao longo de setembro de 2024.

        Returns:
            DataFrame: DataFrame com a variação de posição inicial e final de cada aplicativo.
        """
        # Filtra os dados para o mês de setembro
        df_setembro = self.df[pd.to_datetime(self.df['date']).dt.month == 9]
        return df_setembro.groupby('app_id').agg(
            posicao_inicial=('position', 'first'),
            posicao_final=('position', 'last'),
            variacao_posicao=('position', lambda x: x.iloc[-1] - x.iloc[0])
        ).reset_index()

    def save_report(self, analise_concorrencia, variacao_posicao):
        """
        Salva um relatório em markdown com os resultados da análise.

        Args:
            analise_concorrencia (DataFrame): Dados de análise de concorrência.
            variacao_posicao (DataFrame): Dados de variação de posição.
        """
        report_path = os.path.join(self.data_folder, 'relatorio_analise.md')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Relatório de Análise de Aplicativos\n")
            f.write("## Análise de Concorrência\n")
            f.write(analise_concorrencia.to_markdown(index=False))
            f.write("\n\n## Variação de Posição\n")
            f.write(variacao_posicao.to_markdown(index=False))

    def run_analysis(self):
        """
        Executa o fluxo completo de análise de dados, incluindo a carga de dados,
        preparação, análise e salvamento do relatório.
        """
        self.load_data()
        self.prepare_data()
        analise_concorrencia = self.analyze_competition()
        variacao_posicao = self.position_variation()
        self.save_report(analise_concorrencia, variacao_posicao)
        print("Análise concluída. Relatório salvo.")

# Executar a análise
if __name__ == "__main__":
    # Caminho do arquivo JSON contendo os dados dos aplicativos
    analysis = AppAnalysis('../data/gplaystore.categoryAppPositionsAllbanks.json')
    analysis.run_analysis()