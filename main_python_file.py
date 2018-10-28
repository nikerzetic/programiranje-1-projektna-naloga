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

def get_data_from_text(text):
    return [{x['title'], x['author'], x['shelved'], x['avg_rating'], x['ratings'], x['published'], x['series']} for x in re.finditer(regex, text)]
    
d = get_data_from_text(read_file_to_str(downloaded_sites_directory, 'goodreads.html'))
