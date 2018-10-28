import csv
import json
import os
import re
import sys
import requests

frontpage_url = 'https://www.goodreads.com/shelf/show/fantasy'
downloaded_sites_directory = 'prenesene_strani'

regex = re.compile(
    r'<a title="(?P<title>.*?)\s?(\((?P<series>.*?)?\))?".+?'
    r'<span itemprop="name">(?P<author>.*?)</span>.+?'
    r'\(shelved (?P<shelved>\d+?) times as <em>fantasy</em>\)</a>.+?'
    r'avg rating (?P<avg_rating>\d\.\d\d).+?'
    r'\s*?(?P<ratings>\d.*?\d) ratings.+?'
    r'published (?P<published>.*?)\s',
    re.DOTALL
)

def read_file_to_str(directory, filename):
    with open(os.path.join(directory, filename), 'r', encoding='utf8') as dat:
        return dat.read()

# test of wether the code is working
def get_data_from_text(text):
    return [{x['title'], x['author'], x['shelved'], x['avg_rating'], x['ratings'], x['published'], x['series']} for x in re.finditer(regex, text)]
    
def download_website(url, directory, filename, force_download=False):
    try:
        print('Shranjujem stran {} ...'.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(filename) and not force_download:
            print('Stran že shranjena')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('Stran ne obstaja')
    else:
        with open(os.path.join(directory, filename), 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            print('Shranjena')

download_website(frontpage_url, downloaded_sites_directory, 'goodreads.html', True)
d = get_data_from_text(read_file_to_str(downloaded_sites_directory, 'goodreads.html'))
