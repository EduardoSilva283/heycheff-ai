from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Configurar conexão com MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["heycheff"]  # Substitua pelo nome do banco
collection = db["receipt"]

# Extrair dados da coleção
documents = list(collection.find({}, {"title": 1, "steps.products.description": 1, "_id": 0}))

# Pré-processar os dados
def preprocess_data(documents):
    data = []
    for doc in documents:
        # Combine título e descrição dos produtos
        text = doc["title"]
        for step in doc.get("steps", []):
            for product in step.get("products", []):
                text += " " + product["description"]
        data.append(text)
    return data

texts = preprocess_data(documents)

# Vetorização com TF-IDF
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(texts)

# Função para recomendar receitas semelhantes
def recommend_recipes(query, tfidf_matrix, texts, top_n=5):
    query_vector = vectorizer.transform([query])  # Vetorize a consulta
    similarity = cosine_similarity(query_vector, tfidf_matrix).flatten()  # Calcule similaridade
    indices = similarity.argsort()[-top_n:][::-1]  # Pegue os índices das mais similares
    recommendations = [(texts[i], similarity[i]) for i in indices]
    return recommendations

# Exemplo de uso
query = "Bolo de Chocolate"
recommendations = recommend_recipes(query, tfidf_matrix, texts)

# Exibir recomendações
for rec, score in recommendations:
    print(f"Receita: {rec}, Similaridade: {score:.2f}")
