# MongoDB Data Retrieval and JSON Export

## Descrição

Este projeto Python é uma aplicação para conectar-se a um banco de dados MongoDB, realizar consultas em uma coleção específica e salvar os resultados em um arquivo JSON. O código utiliza as bibliotecas `pymongo`, `datetime`, `logging`, `pandas`, `dotenv` e `json`. A configuração de logging permite monitorar o processo e capturar possíveis erros.

## Funcionalidades

- Conexão com o MongoDB utilizando uma URI definida em variáveis de ambiente.
- Consulta a uma coleção específica com base em critérios definidos.
- Exportação dos dados recuperados para um arquivo JSON.
- Tratamento de erros e logging de informações relevantes durante o processo.

## Estrutura do Código

### Classes e Métodos

#### `MongoDBConnector`

A classe `MongoDBConnector` é responsável por gerenciar a conexão com o banco de dados MongoDB. Ela possui os seguintes métodos:

- `__init__(self, mongo_uri, db_name)`: Inicializa a classe com a URI de conexão e o nome do banco de dados.
- `connect(self)`: Estabelece a conexão com o MongoDB e inicializa a instância do banco de dados.
- `close(self)`: Fecha a conexão com o banco de dados.
- `query_data(self, collection_name, query)`: Realiza uma consulta na coleção especificada usando a query fornecida. Retorna uma lista de documentos ou uma lista vazia se não encontrar dados.

### Funções

#### `save_to_json(data, file_path)`

Esta função recebe uma lista de dados e um caminho de arquivo, salvando os dados em um arquivo JSON. Ela utiliza `json.dump` para realizar a exportação.

## Uso

1. **Instalação das Dependências**

   Certifique-se de ter as bibliotecas necessárias instaladas. Você pode instalar as dependências usando `pip`:

   ```bash
   pip install pymongo pandas python-dotenv
```
2. **Configuração do Ambiente**

Crie um arquivo `.env`na raiz do seu projeto e adicione sua URI do MongoDB:
```bash
MONGO_URI_GOOGLE='sua_uri_do_mongodb'
```
3. **Execução do Script**
Execute o script para conectar ao MongoDB, consultar dados e salvar os resultados em um arquivo JSON:
```bash
python mongoJsonExporter.py
```
Observação: O caminho do arquivo de saída para os dados JSON está configurado como **../data/google_play_data.json**. Certifique-se de que a pasta **data** exista ou ajuste o caminho conforme necessário.

## Exemplo de Query
O código realiza uma consulta na coleção **categoryAppPositions** com os seguintes critérios:

    - appId: Busca apps específicos (por exemplo, "com.nu.production", "com.picpay", "com.bradesco", "com.itau").
    - date: Filtra dados entre 1º de setembro de 2024 e 1º de outubro de 2024.
    - lang: Define o idioma como "pt-BR".

## Logs

Durante a execução do código, logs serão gerados para informar sobre o status da conexão, consultas e quaisquer erros que possam ocorrer.