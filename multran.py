#!/usr/bin/env python3

"""
script fetches word transcription from online dictionary
and copies it to clipboard
"""

from requests import get
from sys import argv, exit
from os import system
from bs4 import BeautifulSoup

if len(argv) == 1 or len(argv) > 2:
    exit(f'usage: multran [word]')

word = argv[1]
if len(word.split()) > 1:
    word = word.replace(' ', '+')

try:
    url = f'https://www.multitran.com/m.exe?l1=1&l2=2&s={word}&langlist=2'
    response = get(url)
except (ConnectionError, Exception) as e:
    exit(e)

page = response.content
soup = BeautifulSoup(page, 'html.parser')
data = soup.findAll('span', attrs={'style': 'color:gray'})

if len(data) == 4:
    exit('Word not found')

def find_transcription(index = 1):
    transcription = data[index].text

    if transcription.startswith('['):
        system(f'echo "{transcription}" | tr -d "\n" | pbcopy')
        print(transcription)
        exit(0)
    else:
        index += 1
        find_transcription(index)

try:
    find_transcription()
except IndexError:
    exit('Transcription not found')
