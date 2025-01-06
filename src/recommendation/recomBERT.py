import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from src.data.mongoConnect import get_recipes
from src.helpers.recom_helper import preprocess_data


def recommend_recipes(query, model, embeddings, texts, top_n=5):
    query_embedding = model.encode([query], convert_to_tensor=True)  # Embedding da consulta
    similarity = cosine_similarity(query_embedding, embeddings)[0]  # Similaridade com todas as receitas
    indices = np.argsort(similarity)[-top_n:][::-1]  # Ordenar por maior similaridade
    recommendations = [(texts[i], similarity[i]) for i in indices]
    return recommendations


def get_bert_recommendations(query):
    collection = get_recipes()
    documents = list(collection.find({}, {"title": 1, "steps.products.description": 1, "_id": 0}))

    texts = preprocess_data(documents)
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # Modelo leve para embeddings de texto
    embeddings = model.encode(texts, convert_to_tensor=True)

    return recommend_recipes(query, model, embeddings, texts)
