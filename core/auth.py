import requests
import logging
import os
from dotenv import load_dotenv

from datetime import datetime, timedelta

load_dotenv()

class Auth:
    _token = None
    _token_expiry = None

    @staticmethod
    def get_token():
        # 🔹 Verifica se já existe um token válido
        if Auth._token and Auth._token_expiry and datetime.now() < Auth._token_expiry:
            return Auth._token

        url_login = os.getenv("API_LOGIN_URL")
        login_payload = {
            "email": os.getenv("API_EMAIL"),
            "senha": os.getenv("API_PASSWORD")
        }


        try:
            response_login = requests.post(url_login, json=login_payload, timeout=10)
            response_login.raise_for_status()  # Levanta exceção se a resposta for erro
        except requests.RequestException as e:
            raise RuntimeError(f"Falha na autenticação: {e}")

        token_data = response_login.json() # Converte a resposta para um dicionário
        Auth._token = token_data.get("token") # Extrai o token usando .get("token")

        # 🔹 Define uma expiração fictícia de 30 minutos (simula comportamento padrão de tokens JWT)
        Auth._token_expiry = datetime.now() + timedelta(minutes=30)

        if not Auth._token:
            raise RuntimeError(f"Falha na autenticação: {response_login.text}")

        logging.info("🔹 Token gerado com sucesso")

        return Auth._token

    @staticmethod
    def get_headers(extra_headers=None):
        headers = {"Authorization": f"JWT {Auth.get_token()}"}
        if extra_headers:
            headers.update(extra_headers)
        return headers
