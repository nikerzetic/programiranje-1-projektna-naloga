import csv
import json
import os
import re
import sys
import requests
from splinter import Browser

sign_in_page = 'https://www.goodreads.com/user/sign_in'
user_email = 'jotopijo1@gmail.com'
user_password = 'geslo123'
frontpage_url = 'https://www.goodreads.com/shelf/show/fantasy'
downloaded_sites_directory = 'downloaded_sites'
edited_data_directory = 'edited_data'

user_regex = re.compile(
    r'<a class="bookTitle" href=".*?">(?P<title>.*?)\s?'
    r'(\((?P<series>.+?)(, #(?P<volume>.+?))?'
    r'(; (?P<alt_series>.+?)(,? #(?P<alt_volume>.+?))?)?\))?</a>.+?'
    r'<span itemprop="name">(?P<author>.*?)</span>.+?'
    r'\(shelved (?P<shelved>\d+?) times as <em>fantasy</em>\)</a>.+?'
    r'avg rating (?P<avg_rating>\d\.\d\d).+?'
    r'\s*?(?P<ratings>\d.*?\d) ratings.+?'
    r'published (?P<published>.*?)\s',
    flags=re.DOTALL
)

class GetAndCleanData:

    def __init__(self, sign_in_page_url, url, email, password, download_dir, edit_dir, page_numbers, regex, force_download=False):
        self.sign_in_page_url = sign_in_page_url
        self.url = url
        self.email = email
        self.password = password
        self.download_dir = download_dir
        self.edit_dir = edit_dir
        self.page_numbers = page_numbers
        self.books = []
        self.regex = regex
        self.force_download = force_download

        self.browser = Browser('firefox')
        self.sign_in()
        self.download_sites()
        self.authors, self.series = self.separate_joint_data()
        self.write_data()

        self.close_browser()

    # Creates Browser object and logs in
    def sign_in(self):
        self.browser.visit(self.sign_in_page_url)

        self.browser.find_by_id('user_email').fill(self.email)
        self.browser.find_by_id('user_password').fill(self.password)
        self.browser.find_by_value('Sign in').first.click()

    # Closes browser
    def close_browser(self):
        self.browser.quit()

    # Creates directory to save files to
    def create_directory(self, directory):
        if not os.path.isdir(directory):
            os.makedirs(directory, exist_ok=True)

    # Turns html file into string
    def read_file_to_str(self, filename):
        with open(os.path.join(self.download_dir, filename), 'r', encoding='utf8') as dat:
            return dat.read()
    
    # Separates page into dictionaries of regex maches
    def separate_data(self, match):
        book_data = match.groupdict()
        return book_data

    # Tests wether the code is working or not
    def get_data_from_text(self, text):
        return [self.separate_data(x) for x in re.finditer(self.regex, text)]

    def download_this_website(self, url, filename):
        self.create_directory(self.download_dir)
        print('Saving page {} ...'.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(os.path.join(self.download_dir, filename)) and not self.force_download:
            print('Page already saved')
            return
        else:
            self.browser.visit(url)
            with open(os.path.join(self.download_dir, filename), 'w', encoding='utf-8') as datoteka:
                datoteka.write(self.browser.html)
                print('Page saved')

    # Creates url from given page number
    def merge_url_and_number(self, num):
        return self.url + '?page={}'.format(num)

    # Writes file to .csv and .json
    def write_to_csv(self, dictionary, fields, directory, filename):
        self.create_directory(directory)
        with open(os.path.join(directory, filename), 'w', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fields, extrasaction='ignore')
            writer.writeheader()
            for dic in dictionary:
                writer.writerow(dic)

    def write_to_json(self, dictionary, directory, filename):
        self.create_directory(directory)
        with open(os.path.join(directory, filename), 'w', encoding='utf-8') as json_file:
            json.dump(dictionary, json_file, indent=4, ensure_ascii=False)

    # Sorts given data
    def sort_data(self, dic):
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
    def separate_joint_data(self):
        authors, series = [], []

        for book in self.books:
            for author in book['author'].split(', '):
                authors.append({'title': book['title'], 'author': author})
            if book['series']:
                series.append({'series': book['series'], 'title': book['title'], 'volume': book['volume']})
            if book['alt_series']:
                series.append({'series': book['alt_series'], 'title': book['title'], 'volume': book['alt_volume']})

        return authors, series

    # Downloads the pages in given range, sorts the data and appends it to books
    def download_sites(self):
        for page_num in self.page_numbers:
            site_name = 'page_{}.html'.format(page_num)
            self.download_this_website(self.merge_url_and_number(page_num), site_name)
            for book in self.get_data_from_text(self.read_file_to_str(site_name)):
                self.sort_data(book)
                if book['published']:
                    self.books.append(book)

    # Writes the data in separate .csv files
    def write_data(self):
        self.write_to_json(self.books, self.edit_dir, 'books.json')
        self.write_to_csv(self.books, ['title', 'shelved', 'avg_rating', 'ratings', 'published'], self.edit_dir, 'books.csv')
        self.write_to_csv(self.authors, ['title', 'author'], self.edit_dir, 'authors.csv')
        self.write_to_csv(self.series, ['series', 'title', 'volume'], self.edit_dir, 'series.csv')


GetAndCleanData(sign_in_page, frontpage_url, user_email, user_password, 
                downloaded_sites_directory, edited_data_directory, range(1, 26), user_regex)