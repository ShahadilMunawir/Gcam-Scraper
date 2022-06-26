from ast import parse
import time
import telebot
import requests
from creds import Telegram
from bs4 import BeautifulSoup

bot = telebot.TeleBot(Telegram.TOKEN, parse_mode=None)

@bot.message_handler(commands=["update"])
def update(msg):
    r = requests.get("https://www.celsoazevedo.com/files/android/google-camera/").content
    soup = BeautifulSoup(r, "html.parser")
    main_block = soup.find("ul", class_="listapks")
    latest = main_block.find_all("li")[0]
    gcam = latest.a.text
    link = latest.a["href"]
    with open("update.txt", "w+") as f:
        if f.read() != gcam:
            f.write(gcam)
            bot.send_message(Telegram.CHAT_ID, f"{gcam}\nLink: {link}")

bot.polling()
while True:
    try:
        bot.polling()
    except:
        time.sleep(15)