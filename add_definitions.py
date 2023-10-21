# this script can fetch words definitions from the web
import json
import os
import time

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


def main():
    words = fetch_words()
    write_down(words)


def fetch_words():
    load_dotenv()
    endpoint = str(os.getenv("API_URL"))
    response = requests.get(endpoint)
    data = json.loads(response.text)
    return data


def write_down(words):
    for item in words:
        word = item["English"]
        definition = fetch_definition(word)
        with open("definitions.txt", "a") as file:
            file.write(f"{definition}\n")
        time.sleep(1)


def fetch_definition(word: str):
    url = f"https://dictionary.cambridge.org/dictionary/english/{word}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        message = f"Failed to retrieve the page: {response.status_code}"
        print(message)
        return message

    soup = BeautifulSoup(response.text, "html.parser")
    definition_div = soup.find("div", class_="def ddef_d db")
    if definition_div:
        definition = definition_div.text.strip()
        print(definition)
        return definition
    else:
        print(f"No definition found: {word}")
        return "-"


if __name__ == "__main__":
    main()
