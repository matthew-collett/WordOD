import requests
import schedule
import time
import json
import discord
from bs4 import BeautifulSoup
from datetime import date

#load config
with open("config.json", "r") as file:
    config = json.load(file)

WEBHOOK = config["webhook_url"]

URL = "https://www.dictionary.com/e/word-of-the-day/"

def get_word_od_msg():
    resp = requests.get(URL)
    soup = BeautifulSoup(resp.content, "html.parser")

    word = soup.find('h1', class_='js-fit-text').text.strip()
    pronun = soup.find('span', class_='otd-item-headword__pronunciation__text').text.strip().replace(" ", "")
    qualities = soup.find('div', class_='otd-item-headword__pos').text.strip().split("\n\n")
    sentence = soup.find('div', class_='wotd-item-origin').findAll('p')[2].text.strip()
    
    msg = "@everyone\nWord of the day for {}\n\n**{}**\n*{}*\n*{}*\n\n**DEFINITION**\n*{}*\n\n*{}*".format(date.today().strftime("%B %d, %Y"), word.upper(), qualities[0].rstrip(), pronun, qualities[1], sentence)
    return msg

def send_word_od_msg():
    msg = get_word_od_msg()
    discord.SyncWebhook.from_url(WEBHOOK).send(msg)

schedule.every().day.at("08:00").do(send_word_od_msg)

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute