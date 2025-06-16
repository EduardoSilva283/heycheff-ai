from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from datetime import datetime, timedelta
import pytz
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

recommendation_bp = Blueprint('recommendation', __name__)

# Config MongoDB Atlas
MONGO_URI = "mongodb+srv://eduardolrs1998:Zk69JSLU3ZE3NEfa@cluster0.ftrgyiy.mongodb.net/"
DB_NAME = "heycheff"
COLLECTION_NAME = "recipe"

# Datas comemorativas exemplo (adicione mais conforme necessário)
HOLIDAYS = {
    '01-01': 'Ano Novo',
    '12-25': 'Natal',
    '06-12': 'Dia dos Namorados',
    '04-21': 'Tiradentes',
    '07-30': 'Festa Junina',
    # ...
}

def get_next_holiday():
    today = datetime.now(pytz.timezone('America/Sao_Paulo'))
    year = today.year
    holidays = []
    tz = today.tzinfo
    for date_str, name in HOLIDAYS.items():
        holiday_date = datetime.strptime(f"{year}-{date_str}", "%Y-%m-%d")
        holiday_date = tz.localize(holiday_date)
        if holiday_date >= today:
            holidays.append((holiday_date, name))
    if holidays:
        holidays.sort()
        return holidays[0]  # (date, name)
    return None

def preprocess_data(documents):
    data = []
    for doc in documents:
        text = doc.get("title", "")
        for step in doc.get("steps", []):
            for product in step.get("products", []):
                text += ", " + product.get("description", "")
        data.append(text)
    return data

def bert_recommendation(query, texts):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings = model.encode(texts, convert_to_tensor=True)
    query_embedding = model.encode([query], convert_to_tensor=True)
    similarity = cosine_similarity(query_embedding, embeddings)[0]
    indices = similarity.argsort()[-5:][::-1]
    return indices, similarity

@recommendation_bp.route('/', methods=['GET'])
def recommend():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    now = datetime.now(pytz.timezone('America/Sao_Paulo'))
    next_holiday = get_next_holiday()
    recipes = list(collection.find())
    texts = preprocess_data(recipes)
    reason = None
    query = None

    if next_holiday:
        query = next_holiday[1]
        reason = f'Receitas para {query}'
    else:
        hour = now.hour
        if 12 <= hour < 16:
            query = 'almoço'
            reason = 'Horário de almoço'
        elif 16 <= hour < 19:
            query = 'café da tarde'
            reason = 'Horário de café da tarde'
        else:
            query = 'receita popular'
            reason = 'Receitas populares/recentes'

    indices, similarity = bert_recommendation(query, texts)
    recommended = []
    for i in indices:
        r = recipes[i]
        recommended.append({
            '_id': str(r.get('_id')),
            'seqId': r.get('seqId'),
            'title': r.get('title'),
            'similarity': float(similarity[i])
        })

    return jsonify({
        'now': now.strftime('%Y-%m-%d %H:%M:%S'),
        'next_holiday': next_holiday[1] if next_holiday else None,
        'reason': reason,
        'recipes': recommended
    })
