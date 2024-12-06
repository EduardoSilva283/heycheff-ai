from pymongo import MongoClient
import pandas as pd

# Configuração de conexão com o MongoDB
uri = "mongodb://localhost:27017" 
client = MongoClient(uri)

# Seleciona o banco de dados
db = client['heycheff']  # Substitua pelo nome do seu banco

# Seleciona a coleção
collection = db['receipt']

# Extrai todos os documentos da coleção
documents = list(collection.find())


# Converte os dados para um DataFrame pandas (opcional)
df = pd.DataFrame(documents)

# Exibe os dados (ou manipula conforme necessário)
print(df.columns)

# Fecha a conexão
client.close()
