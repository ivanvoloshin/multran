#!/usr/bin/env python3

"""
script fetches word transcription from online dictionary
and copies it to clipboard
"""

import pyperclip
from requests import get
from sys import argv, exit
from bs4 import BeautifulSoup

if len(argv) == 1 or len(argv) > 2:
    exit('usage: multran [word]')

word = argv[1]
if len(word.split()) > 1:
    word = word.replace(' ', '+')

url = f'https://www.multitran.com/m.exe?l1=1&l2=2&s={word}&langlist=2'

try:
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
        pyperclip.copy(transcription)
        exit(transcription)
    else:
        index += 1
        find_transcription(index)

try:
    find_transcription()
except IndexError:
    exit('Transcription not found')
