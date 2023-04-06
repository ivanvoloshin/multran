#!/usr/bin/env python3

import pyperclip
import argparse
from requests import get
from sys import exit
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(
    description="English word transcription fetching tool", usage="%(prog)s"
)

parser.add_argument(
    "word", metavar="WORD", type=str, help="Specify word", action="store", nargs="?"
)

args = parser.parse_args()


class Multran:
    def __init__(self, word=None) -> None:
        self.word = word

    def process(self, word):
        if len(word.split()) > 1:
            word = word.replace(" ", "+")

        url = f"https://www.multitran.com/m.exe?l1=1&l2=2&s={word}&langlist=2"

        try:
            response = get(url)
        except (ConnectionError, Exception) as e:
            exit(e)

        page = response.content
        soup = BeautifulSoup(page, "html.parser")
        data = soup.findAll("span", attrs={"style": "color:gray"})

        if len(data) == 7:
            exit("Word not found")

        try:
            self.find_transcription(1, data)
        except IndexError:
            exit("Transcription not found")

    def find_transcription(self, index, lst):
        transcription = lst[index].text

        if transcription.startswith("["):
            pyperclip.copy(transcription)
            print(transcription)
        else:
            index += 1
            self.find_transcription(index, lst)


if args.word:
    word = args.word
    Multran().process(word)
else:
    try:
        while 1:
            word = input("Enter word: ")
            Multran().process(word)
            print()
    except KeyboardInterrupt as e:
        print(e)
        exit(1)
