import json
import os
from datetime import datetime
import pandas as pd
from collections import Counter, defaultdict
from statistics import mean
from typing import Dict, List, Tuple
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO)

def parse_date(date_str: str) -> datetime:
    """Converte string de data para datetime."""
    return datetime.fromisoformat(date_str.replace("Z", "+00:00"))

class VersionUpdateAnalysis:
    def __init__(self):
        """Inicializa a classe VersionUpdateAnalysis."""
        self.version_updates = {}

    def process(self, app_id: str, change_date: datetime, previous_version: str, current_version: str):
        """Processa uma atualização de versão."""
        self.version_updates[app_id] = (change_date, previous_version, current_version)

    def generate_report(self) -> str:
        """Gera um relatório em Markdown com as atualizações de versão."""
        report = "\n## Análise de Atualizações de Versão\n"
        for app_id, (date, prev_version, curr_version) in self.version_updates.items():
            report += f"- **{app_id}**: Em {date.strftime('%Y-%m-%d')}, de versão {prev_version} para {curr_version}\n"
        return report

class TitleChangeAnalysis:
    def __init__(self):
        """Inicializa a classe TitleChangeAnalysis."""
        self.title_changes = {}

    def process(self, app_id: str, change_date: datetime, previous_title: str, current_title: str):
        """Processa uma mudança de título."""
        self.title_changes[app_id] = (change_date, previous_title, current_title)

    def generate_report(self) -> str:
        """Gera um relatório em Markdown com as mudanças de título."""
        report = "\n## Análise de Mudanças de Título\n"
        for app_id, (date, prev_title, curr_title) in self.title_changes.items():
            report += f"- **{app_id}**: Em {date.strftime('%Y-%m-%d')}, de título '{prev_title}' para '{curr_title}'\n"
        return report

class PromotionalTextChangeAnalysis:
    def __init__(self):
        """Inicializa a classe PromotionalTextChangeAnalysis."""
        self.promo_text_changes = {}

    def process(self, app_id: str, change_date: datetime, previous_promo: str, current_promo: str):
        """Processa uma mudança de texto promocional."""
        self.promo_text_changes[app_id] = (change_date, previous_promo, current_promo)

    def generate_report(self) -> str:
        """Gera um relatório em Markdown com as mudanças de texto promocional."""
        report = "\n## Análise de Mudanças em Texto Promocional\n"
        for app_id, (date, prev_promo, curr_promo) in self.promo_text_changes.items():
            report += f"- **{app_id}**: Em {date.strftime('%Y-%m-%d')}, de texto promocional '{prev_promo}' para '{curr_promo}'\n"
        return report

class IconChangeAnalysis:
    def __init__(self):
        """Inicializa a classe IconChangeAnalysis."""
        self.icon_changes = defaultdict(list)

    def process(self, app_id: str, change_date: datetime, previous_icon: str, current_icon: str):
        """Processa uma mudança de ícone."""
        self.icon_changes[app_id].append((change_date, previous_icon, current_icon))

    def generate_report(self) -> str:
        """Gera um relatório em Markdown com as mudanças de ícone."""
        report = "\n## Análise de Mudanças de Ícone\n"
        for app_id, changes in self.icon_changes.items():
            report += f"\n### {app_id}:\n"
            for date, prev_icon, curr_icon in changes:
                report += f"- **Data**: {date.strftime('%Y-%m-%d')}\n"
        return report

class UpdateFrequencyAnalysis:
    def __init__(self):
        """Inicializa a classe UpdateFrequencyAnalysis."""
        self.update_frequency = defaultdict(list)

    def process(self, app_id: str, change_date: datetime):
        """Processa uma atualização de frequência."""
        self.update_frequency[app_id].append(change_date)

    def calculate_intervals(self, dates: List[datetime]) -> Tuple[float, List[float]]:
        """Calcula os intervalos entre as datas de atualização."""
        dates.sort()
        intervals = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))]
        avg_interval = mean(intervals) if intervals else 0
        return avg_interval, intervals

    def generate_report(self) -> str:
        """Gera um relatório em Markdown com a frequência de atualizações."""
        report = "\n## Frequência de Atualizações\n"
        for app_id, dates in self.update_frequency.items():
            avg_interval, intervals = self.calculate_intervals(dates)
            report += f"\n### {app_id}:\n"
            report += f"- **Intervalo médio entre atualizações**: {avg_interval:.2f} dias\n"
            for date, count in Counter([d.date() for d in dates]).items():
                report += f"- **Data**: {date}, **Atualizações**: {count}\n"
        return report

def load_data(file_path: str) -> Dict:
    """Carrega dados do arquivo JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"Arquivo não encontrado: {file_path}")
        return {}
    except json.JSONDecodeError:
        logging.error(f"Erro ao decodificar JSON: {file_path}")
        return {}

def count_change_types(data: Dict) -> Counter:
    """Conta a frequência de cada tipo de mudança."""
    change_counter = Counter()
    for app_id, app_data in data.items():
        for entry in app_data.get('content', []):
            for change in entry.get('changes', []):
                change_counter[change['field']] += 1
    return change_counter

def get_update_frequency(data: Dict) -> pd.DataFrame:
    """Obtém a frequência de atualizações usando Pandas."""
    update_dates = defaultdict(list)
    for app_id, app_data in data.items():
        for entry in app_data.get('content', []):
            for change in entry.get('changes', []):
                date_obj = datetime.strptime(change['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
                update_dates[app_id].append(date_obj.date())
    # Construir DataFrame para série temporal
    freq_df = pd.DataFrame([(app_id, date) for app_id, dates in update_dates.items() for date in dates],
                           columns=['App ID', 'Date'])
    freq_df['Date'] = pd.to_datetime(freq_df['Date'])
    return freq_df.groupby(['App ID', 'Date']).size().unstack(fill_value=0)

def generate_markdown_report(analyses: List[str], output_path: str):
    """Gera um relatório em Markdown com as análises."""
    report = "# Relatório de Análise de Changeslog de Aplicativos Bancários\n"
    report += "## Visão Geral\n"
    report += "Este relatório apresenta uma análise detalhada das mudanças nos aplicativos bancários, abordando atualizações de versão, mudanças de título, textos promocionais e ícones.\n"

    for analysis in analyses:
        report += analysis

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(report)

def main():
    # Caminhos dos arquivos
    current_dir = os.path.dirname(os.path.abspath(__file__))
    apple_path = os.path.join(current_dir, 'data', 'changeslog_apple_results.json')
    google_path = os.path.join(current_dir, 'data', 'changeslog_google_results.json')
    output_path = os.path.join(current_dir, 'data', 'relatorio_analise_changeslog.md')

    # Carregar dados
    apple_data = load_data(apple_path)
    google_data = load_data(google_path)
    all_data = {**apple_data, **google_data}

    # Instanciar classes de análise
    version_analysis = VersionUpdateAnalysis()
    title_analysis = TitleChangeAnalysis()
    promo_text_analysis = PromotionalTextChangeAnalysis()
    icon_analysis = IconChangeAnalysis()
    frequency_analysis = UpdateFrequencyAnalysis()

    # Processar dados
    for app_id, app_data in all_data.items():
        for entry in app_data.get('content', []):
            for change in entry.get('changes', []):
                change_date = parse_date(change['date'])
                field = change['field']

                if field == 'version':
                    version_analysis.process(app_id, change_date, change.get('previousValue'), change.get('currentValue'))
                elif field == 'title':
                    title_analysis.process(app_id, change_date, change.get('previousValue'), change.get('currentValue'))
                elif field == 'promotionalText':
                    promo_text_analysis.process(app_id, change_date, change.get('previousValue'), change.get('currentValue'))
                elif field == 'icon':
                    icon_analysis.process(app_id, change_date, change.get('previousValue', ''), change.get('currentValue', ''))

                frequency_analysis.process(app_id, change_date)

    # Contagem de tipos de mudanças
    apple_change_types = count_change_types(apple_data)
    google_change_types = count_change_types(google_data)

    # Frequência de atualizações com Pandas
    apple_update_freq = get_update_frequency(apple_data)
    google_update_freq = get_update_frequency(google_data)

    # Salvar as tabelas de frequência em CSV
    apple_update_freq.to_csv(os.path.join(current_dir, 'data', 'apple_update_freq.csv'))
    google_update_freq.to_csv(os.path.join(current_dir, 'data', 'google_update_freq.csv'))

    # Gerar e salvar relatório
    generate_markdown_report(
        [
            icon_analysis.generate_report(),
            version_analysis.generate_report(),
            title_analysis.generate_report(),
            promo_text_analysis.generate_report(),
            frequency_analysis.generate_report(),
            f"\n## 2. Impacto no Posicionamento nas Lojas de Apps\n",
            f"### Mudanças mais comuns por tipo\n",
            f"#### Apple Store:\n",
            "\n".join([f"- {field}: {count} mudanças" for field, count in apple_change_types.items()]),
            f"\n#### Google Play:\n",
            "\n".join([f"- {field}: {count} mudanças" for field, count in google_change_types.items()]),
            f"\n## 3. Frequência de Atualizações\n",
            f"### Apple Store\n",
            apple_update_freq.to_markdown(),
            f"\n### Google Play\n",
            google_update_freq.to_markdown(),
            f"\n## 4. Conclusão\n",
            f"As análises sugerem que mudanças frequentes em ícones e descrições podem ter impacto nas lojas de apps.\n"
        ],
        output_path
    )

    logging.info(f"Relatório gerado com sucesso em: {output_path}")

if __name__ == '__main__':
    main()
