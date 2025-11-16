import time
import requests

TOKEN = "8279285665:AAEyYlOpniGDYM0KZyDk_D1L7FypANb3uqs"
CHAT_ID = "959511946"
URL = f"https://api.telegram.org/bot{TOKEN}/"

def send_message(text):
    try:
        requests.post(URL + "sendMessage", data={"chat_id": CHAT_ID, "text": text})
    except Exception as e:
        print("Erro ao enviar mensagem:", e)

def get_updates(offset=None):
    try:
        params = {"timeout": 100, "offset": offset}
        response = requests.get(URL + "getUpdates", params=params).json()
        return response
    except:
        return {"result": []}

def handle_message(text):
    text = text.lower()

    if text == "/start":
        send_message("🔥 Bot ativo! Envie: gol, escanteio, canto, alerta")
    elif text == "gol":
        send_message("⚽ *ALERTA DE GOL* enviado!")
    elif text == "escanteio":
        send_message("🏁 *ALERTA DE ESCANTEIO* enviado!")
    elif text == "canto":
        send_message("⬆️ *ALERTA DE CANTOS* enviado!")
    else:
        send_message("🤖 Não entendi. Tente /start")

def main():
    print("Bot iniciado...")
    last_update_id = None

    while True:
        updates = get_updates(last_update_id)

        for update in updates["result"]:
            last_update_id = update["update_id"] + 1
            message = update["message"]["text"]
            handle_message(message)

        time.sleep(1)

main()
