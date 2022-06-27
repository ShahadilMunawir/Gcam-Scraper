import time
import telebot
import requests
import threading
from creds import Telegram
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

bot = telebot.TeleBot(Telegram.TOKEN, parse_mode=None)

@bot.message_handler(commands=["update"])
def update(msg):
    now = datetime.now()
    time_add = now+timedelta(hours=1)
    while True:
        if datetime.now().time().hour == time_add.time().hour:
            r = requests.get("https://www.celsoazevedo.com/files/android/google-camera/").content
            soup = BeautifulSoup(r, "html.parser")
            main_block = soup.find("ul", class_="listapks")
            latest = main_block.find_all("li")[0]
            gcam = latest.a.text
            link = latest.a["href"]
            file1 = open("update.txt", "r")
            if file1.read() != gcam:
                file2 = open("update.txt", "w")
                file2.write(gcam)
                bot.send_message(Telegram.CHAT_ID, f"{gcam}\nLink: {link}")
                file2.close()
                bot.send_message(Telegram.CHAT_ID, "Worked")
            time_add = datetime.now() + timedelta(hours=1)
            bot.send_message(Telegram.CHAT_ID, f"Bot is working, Report time: {datetime.now().strftime('%H:%M:%S')}")

@bot.message_handler(commands=["updates"])
def updates(msg):
    gcamStr = ""
    r = requests.get("https://www.celsoazevedo.com/files/android/google-camera/").content
    soup = BeautifulSoup(r, "html.parser")
    main_block = soup.find("ul", class_="listapks")
    gcam_objs = main_block.find_all("li")
    for i, gcam in enumerate(gcam_objs):
        gcamName = gcam.a.text
        gcamLink = gcam.a["href"]
        # if gcam_objs.index(gcam_objs[-1]) == i:
            # gcamStr += gcamName+gcamLink
        # else:
        gcamStr += gcamName+"\n"+gcamLink+"\n\n"
    print(gcamStr)
    bot.send_message(Telegram.CHAT_ID, gcamStr)

threading.Thread(target=updates)
bot.polling()
while True:
    try:
        bot.polling()
    except:
        time.sleep(15)