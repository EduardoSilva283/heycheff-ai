from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["heycheff"]  # Substitua pelo nome do banco
collection = db["receipt"]

# Extrair os dados da coleção
documents = list(collection.find({}, {"title": 1, "steps.products.description": 1, "_id": 0}))

# Pré-processar os dados
def preprocess_data(documents):
    data = []
    for doc in documents:
        text = doc["title"]
        for step in doc.get("steps", []):
            for product in step.get("products", []):
                text += " " + product["description"]
        data.append(text)
    return data

texts = preprocess_data(documents)

# Carregar o modelo BERT
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # Modelo leve para embeddings de texto

# Gerar embeddings para as receitas
embeddings = model.encode(texts, convert_to_tensor=True)

# Função para recomendar receitas
def recommend_recipes(query, embeddings, texts, top_n=5):
    query_embedding = model.encode([query], convert_to_tensor=True)  # Embedding da consulta
    similarity = cosine_similarity(query_embedding, embeddings)[0]  # Similaridade com todas as receitas
    indices = np.argsort(similarity)[-top_n:][::-1]  # Ordenar por maior similaridade
    recommendations = [(texts[i], similarity[i]) for i in indices]
    print('rodou')
    return recommendations

# Exemplo de uso
query = "Salada"
recommendations = recommend_recipes(query, embeddings, texts)

# Exibir as recomendações
print("Recomendações para:", query)
for rec, score in recommendations:
    print(f"Receita: {rec}, Similaridade: {score:.4f}")
