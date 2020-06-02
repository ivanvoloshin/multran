#!/usr/local/bin/python3

"""
script fetches word transcription from online dictionary
and copies it to clipboard
"""

from requests import get
from sys import argv, exit
from os import system
from bs4 import BeautifulSoup

from colortext import *
ct = colortext

if len(argv) == 1 or len(argv) > 2:
    exit(f'{ct.BOLD}usage:{ct.END} multran [word]')

word = argv[1]
if len(word.split()) > 1:
    word = word.replace(' ', '+')

try:
    url = f'https://www.multitran.com/m.exe?l1=1&l2=2&s={word}&langlist=2'
    response = get(url)
except (ConnectionError, Exception) as e:
    exit(f'{ct.RED}Error:{ct.END} {e}')


page = response.content
soup = BeautifulSoup(page, 'html.parser')
data = soup.findAll('span', attrs={'style': 'color:gray'})

if len(data) == 4:
    exit('Word not found')

index = 1
def find_transcription(index):
    transcription = data[index].text

    if transcription.startswith('['):
        system(f'echo "{transcription}" | tr -d "\n" | pbcopy')
        print(transcription)
        exit(0)
    else:
        index += 1
        find_transcription(index)

try:
    find_transcription(index)
except IndexError:
    exit('Transcription not found')
