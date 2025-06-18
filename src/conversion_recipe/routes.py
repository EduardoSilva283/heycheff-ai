from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

conversion_bp = Blueprint('conversion', __name__)

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI').replace('"', '')
DB_NAME = os.getenv('DB_NAME').replace('"', '')
COLLECTION_NAME = os.getenv('COLLECTION_NAME').replace('"', '')

# Ingredientes de risco para alergias/intolerâncias
ALERGY_MAP = {
    'celiaco': ['trigo', 'farinha de trigo', 'cevada', 'centeio', 'malte', 'gluten'],
    'diabetes': ['açúcar', 'mel', 'xarope', 'glucose', 'leite condensado'],

}
# Sugestões de substituição
SUBSTITUTES = {
    'trigo': 'farinha de arroz',
    'farinha de trigo': 'farinha de arroz',
    'cevada': 'farinha de milho',
    'centeio': 'farinha de milho',
    'malte': 'farinha de milho',
    'gluten': 'farinha sem glúten',
    'açúcar': 'xilitol',
    'mel': 'adoçante',
    'xarope': 'adoçante',
    'glucose': 'adoçante',
    'leite condensado': 'leite condensado diet',

}

# Lista de ingredientes seguros para cada restrição
SAFE_INGREDIENTS = {
    'celiaco': ['farinha de arroz', 'farinha de milho', 'polvilho', 'amido de milho', 'farinha sem glúten'],
    'diabetes': ['xilitol', 'stevia', 'adoçante', 'leite condensado diet', 'frutose', 'erythritol'],
}

# Carrega modelo uma vez
bert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def suggest_substitute(ingredient, restriction):
    # Prioriza substituição direta
    if ingredient.lower() in SUBSTITUTES:
        return SUBSTITUTES[ingredient.lower()]
    safe_list = SAFE_INGREDIENTS.get(restriction, [])
    if not safe_list:
        return ingredient  # fallback
    # Calcula embeddings
    emb_ingredient = bert_model.encode([ingredient])[0]
    emb_safe = bert_model.encode(safe_list)
    # Similaridade
    sims = cosine_similarity([emb_ingredient], emb_safe)[0]
    idx = sims.argmax()
    return safe_list[idx]

def convert_ingredients(products, restriction):
    converted = []
    for prod in products:
        desc = prod['description'].lower()
        # Usa ML para identificar alergênico
        if is_allergen(desc):
            substitute = suggest_substitute(prod['description'], restriction)
            prod = prod.copy()
            prod['description'] = substitute
        converted.append(prod)
    return converted


def train_allergen_classifier():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db['products']

    # Busca usando seqId como inteiro
    df = pd.DataFrame(list(collection.find()))
    X = bert_model.encode(df['product'].tolist())
    y = df['alergenico']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = LogisticRegression()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))
    return clf

# Treina o classificador ao iniciar
allergen_clf = train_allergen_classifier()

def is_allergen(ingredient):
    pred = allergen_clf.predict(bert_model.encode([ingredient]))[0]
    return bool(pred)

# --- Fim do classificador ---

@conversion_bp.route('/convert_recipe', methods=['POST'])
def convert_recipe():
    data = request.json
    restriction = data.get('restriction')  
    recipe_id = data.get('recipe_id')

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    # Busca usando seqId como inteiro
    recipe = collection.find_one({'seqId': int(recipe_id)}) if recipe_id else data.get('recipe')

    if not recipe:
        return jsonify({'error': 'Receita não encontrada'}), 404

    # Converte ObjectId para string
    if '_id' in recipe:
        recipe['_id'] = str(recipe['_id'])

    # Gera novo _id único para a receita convertida
    recipe['_id'] = str(ObjectId())

    for step in recipe.get('steps', []):
        step['products'] = convert_ingredients(step.get('products', []), restriction)

    # Salva receita convertida em nova coleção
    recipe['restriction'] = restriction
    converted_collection = db['converted_recipes']
    insert_result = converted_collection.insert_one(recipe)
    recipe['converted_id'] = str(insert_result.inserted_id)

    return jsonify({'converted_recipe': recipe})

