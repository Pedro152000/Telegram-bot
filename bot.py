
import requests
import time
import telebot
from bs4 import BeautifulSoup

# ---------------------------------------
# CONFIGURAÇÃO (SEU TOKEN + SEU ID)
# ---------------------------------------
BOT_TOKEN = "8279285665:AAGRi2DQg3Mu3gJmZrKdub_0oHybZKQOSA0"
CHAT_ID = "959511946"

bot = telebot.TeleBot(BOT_TOKEN)

# Página de jogos ao vivo do Sofascore
SOFASCORE_URL = "https://www.sofascore.com/pt/partidas/ao-vivo"

# Guarda últimos eventos detectados para evitar duplicados
ultimos_eventos = set()


def buscar_jogos():
    """Faz scraping básico da página de jogos ao vivo do Sofascore."""
    try:
        html = requests.get(SOFASCORE_URL, timeout=10).text
        soup = BeautifulSoup(html, "lxml")

        jogos = []
        for bloco in soup.find_all("div", class_="s-event"):
            try:
                time_a = bloco.find("div", class_="home").text.strip()
                time_b = bloco.find("div", class_="away").text.strip()
                placar = bloco.find("div", class_="score").text.strip()
                minuto = bloco.find("div", class_="event-round").text.strip()

                jogos.append({
                    "jogo": f"{time_a} vs {time_b}",
                    "placar": placar,
                    "minuto": minuto
                })
            except:
                continue

        return jogos

    except Exception as e:
        print("Erro ao buscar Sofascore:", e)
        return []


def detectar_eventos(jogos):
    """Gera sinais com base em alterações no placar ou minuto."""
    sinais = []

    for j in jogos:
        chave = f"{j['jogo']} - {j['placar']} - {j['minuto']}"

        # Evita sinais duplicados
        if chave in ultimos_eventos:
            continue

        ultimos_eventos.add(chave)

        # Detectar GOL
        if "-" in j["placar"]:
            gols = j["placar"].split("-")
            if len(gols) == 2:
                try:
                    g1 = int(gols[0])
                    g2 = int(gols[1])
                    total = g1 + g2
                    if total >= 1:
                        sinais.append(
                            f"⚽ *GOL DETECTADO!*\n📌 {j['jogo']}\n⏱ Minuto: {j['minuto']}\n📊 Placar: {j['placar']}"
                        )
                except:
                    pass

        # Detectar ESCANTEIO (modo básico)
        if "+" in j["minuto"]:
            sinais.append(
                f"🏳️ *POSSÍVEL ESCANTEIO!*\n📌 {j['jogo']}\n⏱ Minuto: {j['minuto']}\n📊 Placar: {j['placar']}"
            )

    return sinais


def enviar_sinais():
    """Busca, detecta e envia sinais."""
    jogos = buscar_jogos()

    if not jogos:
        print("Nenhum jogo encontrado")
        return

    sinais = detectar_eventos(jogos)

    for s in sinais:
        try:
            bot.send_message(CHAT_ID, s, parse_mode="Markdown")
            print("Sinal enviado:", s)
        except Exception as e:
            print("Erro ao enviar:", e)


print("BOT INICIADO — analisando Sofascore...")

while True:
    enviar_sinais()
    time.sleep(60)