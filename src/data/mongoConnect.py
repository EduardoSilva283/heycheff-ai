from pymongo import MongoClient

URI = "mongodb://localhost:27017"


def get_database_connection():
    client = MongoClient(URI)
    return client.get_database('heycheff')


def get_recipes():
    return get_database_connection().get_collection('receipt')
