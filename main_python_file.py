import csv
import json
import os
import re
import sys
import requests

frontpage_url = 'https://www.goodreads.com/shelf/show/fantasy'
downloaded_sites_directory = 'downloaded_sites'

regex = re.compile(
    r'<a title="(?P<title>.*?)\s?(\((?P<series>.*?)?\))?".+?'
    r'<span itemprop="name">(?P<author>.*?)</span>.+?'
    r'\(shelved (?P<shelved>\d+?) times as <em>fantasy</em>\)</a>.+?'
    r'avg rating (?P<avg_rating>\d\.\d\d).+?'
    r'\s*?(?P<ratings>\d.*?\d) ratings.+?'
    r'published (?P<published>.*?)\s',
    flags=re.DOTALL
)
# Creates directory to save files to
def create_directory(dir_name):
    directory = os.path.dirname(dir_name)
    if directory:
        os.makedirs(directory, exist_ok=True)

# Turns html file into string
def read_file_to_str(directory, filename):
    with open(os.path.join(directory, filename), 'r', encoding='utf8') as dat:
        return dat.read()

# Tests wether the code is working or not
def get_data_from_text(text):
    return [separate_data(x) for x in re.finditer(regex, text)]

# Downloads the website from given url and saves it in directory under given name
def download_website(url, directory, filename, force_download=False):
    try:
        print('Saving page {} ...'.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(filename) and not force_download:
            print('Page already saved')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('Page does not exist')
    else:
        with open(os.path.join(directory, filename), 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            print('Page saved')

# Separates page into dictionaries of regex maches
def separate_data(match):
    book_data = match.groupdict()
    return book_data

# Code to be excecuted
download_website(frontpage_url, downloaded_sites_directory, 'goodreads.html')
d = get_data_from_text(read_file_to_str(downloaded_sites_directory, 'goodreads.html'))
