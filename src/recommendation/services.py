from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.data.mongoConnect import get_recipes
from src.helpers.recom_helper import preprocess_data


def recommend_recipes(query, vectorizer, tfidf_matrix, texts, top_n=5):
    query_vector = vectorizer.transform([query])  # Vetoriza a consulta
    similarity = cosine_similarity(query_vector, tfidf_matrix).flatten()  # Calcula a  similaridade
    indices = similarity.argsort()[-top_n:][::-1]  # Otbem os índices dos mais semelhantes
    recommendations = [(texts[i], similarity[i]) for i in indices]
    return recommendations


def get_recommendations(query):
    collection = get_recipes()
    documents = list(collection.find({}, {"title": 1, "steps.products.description": 1, "_id": 0}))

    texts = preprocess_data(documents)
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(texts)

    return recommend_recipes(query, vectorizer, tfidf_matrix, texts)
