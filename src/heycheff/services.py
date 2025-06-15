import requests
import os
from dotenv import load_dotenv


load_dotenv()

HEYCHEFF_URL = os.getenv('HEYCHEFF_URL')
HEYCHEFF_USER = os.getenv('HEYCHEFF_USER')
HEYCHEFF_PASSWORD = os.getenv('HEYCHEFF_PASSWORD')


def authenticate_heycheff():
    url = f"{HEYCHEFF_URL}/auth"
    payload = {
        "username": HEYCHEFF_USER,
        "password": HEYCHEFF_PASSWORD
    }
    print(payload)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


def get_heycheff_receitas():
    url = f"{HEYCHEFF_URL}/receitas/all"
    token = authenticate_heycheff().get('token')
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    try:
        return response.json()
    except Exception:
        print(f"Resposta inválida ou vazia: {response.text}")
        return None


