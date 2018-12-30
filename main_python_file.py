import csv
import json
import os
import re
import sys
import requests

frontpage_url = 'https://www.goodreads.com/shelf/show/fantasy'
downloaded_sites_directory = 'downloaded_sites'
edited_data_directory = 'edited_data'

regex = re.compile(
    r'<a class="bookTitle" href=".*?">(?P<title>.*?)\s?'
    r'(\((?P<series>.+?)(, #(?P<volume>.+?))?'
    r'(; (?P<alt_series>.+?) #(?P<alt_volume>.+?))?\))?</a>.+?'
    r'<span itemprop="name">(?P<author>.*?)</span>.+?'
    r'\(shelved (?P<shelved>\d+?) times as <em>fantasy</em>\)</a>.+?'
    r'avg rating (?P<avg_rating>\d\.\d\d).+?'
    r'\s*?(?P<ratings>\d.*?\d) ratings.+?'
    r'published (?P<published>.*?)\s',
    flags=re.DOTALL
)
# Creates directory to save files to
def create_directory(dir_name):
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name, exist_ok=True)

# Turns html file into string
def read_file_to_str(directory, filename):
    with open(os.path.join(directory, filename), 'r', encoding='utf8') as dat:
        return dat.read()

# Tests wether the code is working or not
def get_data_from_text(text):
    return [separate_data(x) for x in re.finditer(regex, text)]

# Downloads the website from given url and saves it in directory under given name
def download_website(url, directory, filename, force_download=False):
    create_directory(directory)
    try:
        print('Saving page {} ...'.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(os.path.join(directory, filename)) and not force_download:
            print('Page already saved')
            return
        r = requests.get(url, allow_redirects=True)
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


# Creates url from given page number
def merge_url_and_number(url, num):
    return url + '?page={}'.format(num)

# Writes file to .csv and .json
def write_to_csv(dictionary, fields, directory, filename):
    create_directory(directory)
    with open(os.path.join(directory, filename), 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        for dic in dictionary:
            writer.writerow(dic)

def write_to_json(dictionary, directory, filename):
    create_directory(directory)
    with open(os.path.join(directory, filename), 'w', encoding='utf-8') as json_file:
        json.dump(dictionary, json_file, indent=4, ensure_ascii=False)

# Sorts given data
def sort_data(dic):
    dic['shelved'] = int(dic['shelved'])
    dic['avg_rating'] = float(dic['avg_rating'])
    dic['ratings'] = int(dic['ratings'].replace(',', ''))
    try:
        dic['published'] = int(dic['published'])
    except (TypeError, ValueError):
        dic['published'] = None
    try:
        dic['volume'] = int(dic['volume'])
    except (TypeError, ValueError):
        dic['volume'] = None
    if not dic['volume']:
        dic['series'] = None

# Separates data about authors and series
def separate_joint_data(books):
    authors, series = [], []

    for book in books:
        for author in book['author'].split(', '):
            authors.append({'title': book['title'], 'author': author})
        if book['series']:
            series.append({'series': book['series'], 'title': book['title'], 'volume': book['volume']})
        if book['alt_series']:
            series.append({'series': book['alt_series'], 'title': book['title'], 'volume': book['alt_volume']})

    return authors, series

# Downloads the pages in given range, sorts the data and appends it to books
books = []

for page_num in range(1, 26):
    site_name = 'page_{}.html'.format(page_num)
    download_website(merge_url_and_number(frontpage_url, page_num), downloaded_sites_directory, site_name)
    for book in get_data_from_text(read_file_to_str(downloaded_sites_directory, site_name)):
        sort_data(book)
        if book['published']:
            books.append(book)

# Writes the data in separate .csv files
authors, series = separate_joint_data(books)
write_to_json(books, edited_data_directory, 'books.json')
write_to_csv(books, ['title', 'shelved', 'avg_rating', 'ratings', 'published'], edited_data_directory, 'books.csv')
write_to_csv(authors, ['title', 'author'], edited_data_directory, 'authors.csv')
write_to_csv(series, ['series', 'title', 'volume'], edited_data_directory, 'series.csv')
