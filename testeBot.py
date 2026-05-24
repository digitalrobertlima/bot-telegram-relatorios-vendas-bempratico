import requests

telegram_token = "7070149352:AAE90Igeze2hHZPnGWQ1GORoG6makVdt-MU"

url = f"https://api.telegram.org/bot{telegram_token}/getUpdates"
response = requests.get(url)
print(response.json())

# Retorna o id do bot