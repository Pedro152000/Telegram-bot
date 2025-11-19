import time
import requests
import telebot

TOKEN = "8279285665:AAGRi2DQg3Mu3gJmZrKdub_0oHybZKQOSA0"
CHAT_ID = "959511946"
bot = telebot.TeleBot(TOKEN)

SOFASCORE_URL = "https://www.sofascore.com/api/v1/event/live"

def get_live_matches():
    try:
        r = requests.get(SOFASCORE_URL)
        data = r.json()
        return data.get("events", [])
    except:
        return []

def check_signals():
    matches = get_live_matches()

    if not matches:
        print("Sem jogos ao vivo...")
        return

    for game in matches:
        home = game["homeTeam"]["name"]
        away = game["awayTeam"]["name"]
        minute = game["time"]["currentPeriodStartTimestamp"]

        score_home = game["homeScore"]["current"]
        score_away = game["awayScore"]["current"]

        match_name = f"{home} x {away}"

        # 📌 Exemplo de regra para Gol
        if score_home + score_away == 0:
            msg = f"⚽ *Possível Gol*\n📌 {match_name}\n⏱ Minuto: {minute}\n📊 Probabilidade: 78%"
            bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
            print("Enviado sinal de gol")

        # 📌 Escanteios (exemplo simples)
        if game.get("corner", 0) >= 8:
            msg = f"🏳️ *Escanteios*\n📌 {match_name}\n⏱ Minuto: {minute}\n📊 Probabilidade: 85%"
            bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
            print("Enviado sinal de escanteio")

print("BOT INICIADO...")

while True:
    check_signals()
    time.sleep(30)
