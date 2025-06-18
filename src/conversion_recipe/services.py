import requests
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI').replace('"', '')
DB_NAME = os.getenv('DB_NAME').replace('"', '')

# Exemplo de lista de alergênicos e substitutos (pode ser expandida)
ALLERGENS = [
    {"alergenico": "trigo", "substitutos": ["farinha de arroz", "farinha de milho"]},
    {"alergenico": "leite", "substitutos": ["bebida vegetal", "leite de amêndoas"]},
    {"alergenico": "ovo", "substitutos": ["linhaça", "chia"]},
    {"alergenico": "soja", "substitutos": ["ervilha", "grão-de-bico"]},
    {"alergenico": "amendoim", "substitutos": ["sementes de girassol"]},
    {"alergenico": "castanhas", "substitutos": ["sementes de abóbora"]},
    {"alergenico": "peixe", "substitutos": ["tofu", "proteína de soja"]},
    {"alergenico": "crustáceos", "substitutos": ["proteína de soja"]},
    {"alergenico": "açúcar", "substitutos": ["xilitol", "stevia", "erythritol"]},
    # ...
]

def save_allergens_to_mongo():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db['products']
    # Remove todos antes de inserir (opcional)
    collection.delete_many({})
    collection.insert_many(ALLERGENS)
    print(f"{len(ALLERGENS)} produtos alergênicos e substitutos salvos na collection 'products'.")

# Exemplo de uso:
# save_allergens_to_mongo()
