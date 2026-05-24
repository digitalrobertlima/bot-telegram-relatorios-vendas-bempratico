import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Variáveis de configuração do Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_mensagem_telegram(mensagem):
    """
    Envia uma mensagem para o chat especificado no Telegram.
    
    Parâmetros:
    mensagem (str): Mensagem a ser enviada.
    """
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Erro: TELEGRAM_TOKEN ou TELEGRAM_CHAT_ID não configurados no .env")
        return None

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    return response.json()

def enviar_arquivo_telegram(caminho_arquivo):
    """
    Envia um arquivo PDF para o chat especificado no Telegram.
    
    Parâmetros:
    caminho_arquivo (str): Caminho completo para o arquivo a ser enviado.
    """
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Erro: TELEGRAM_TOKEN ou TELEGRAM_CHAT_ID não configurados no .env")
        return None

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    try:
        with open(caminho_arquivo, 'rb') as f:
            files = {'document': f}
            payload = {"chat_id": CHAT_ID}
            response = requests.post(url, files=files, data=payload)
            return response.json()
    except FileNotFoundError:
        print(f"Erro: Arquivo {caminho_arquivo} não encontrado para envio.")
        return None
