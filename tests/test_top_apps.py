from pymongo import MongoClient
import os

def test_mongo_connection():
    client_mongo = MongoClient(os.getenv("MONGODB_URL"))
    db = client_mongo['gplaystore']
    collection = db['categoryAppPositions']

    try:
        # Teste uma simples consulta
        sample_doc = collection.find_one()
        if sample_doc:
            print("Conexão bem-sucedida! Documento encontrado:", sample_doc)
        else:
            print("Conexão bem-sucedida, mas nenhum documento encontrado.")
    except Exception as e:
        print("Erro ao acessar a coleção:", e)

if __name__ == "__main__":
    test_mongo_connection()
