import requests
import schedule
import time
import json
import discord
from bs4 import BeautifulSoup
from datetime import date

URL = "https://www.dictionary.com/e/word-of-the-day/"
RESP = requests.get(URL)
SOUP = BeautifulSoup(RESP.content, "html.parser")

#load config
with open("config.json", "r") as file:
    config = json.load(file)

WEBHOOK = config["webhook_url"]

def get_word_od_msg():
    word = SOUP.find('h1', class_='js-fit-text').text.strip()
    pronun = SOUP.find('span', class_='otd-item-headword__pronunciation__text').text.strip().replace(" ", "")
    qualities = SOUP.find('div', class_='otd-item-headword__pos').text.strip().split("\n\n")
    sentence = SOUP.find('div', class_='wotd-item-origin').findAll('p')[2].text.strip()
    
    msg = "@everyone\nWord of the day for {}\n\n**{}**\n*{}*\n*{}*\n\n**DEFINITION**\n*{}*\n\n*{}*".format(date.today().strftime("%B %d, %Y"), word.upper(), qualities[0].rstrip(), pronun, qualities[1], sentence)
    return msg

def send_word_od_msg():
    msg = get_word_od_msg()
    discord.SyncWebhook.from_url(WEBHOOK).send(msg)

schedule.every().day.at("9:00").do(send_word_od_msg)

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute