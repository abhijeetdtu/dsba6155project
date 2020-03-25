%load_ext autoreload
%autoreload 2

from dsba6155project.constants import Constants

import os
import re
import requests
from bs4 import BeautifulSoup
import shutil

import time

class GetData:

    def __init__(self,query,refresh=False, downloadLocation=None):
        self.query_url = Constants.GUTENBERG_SEARCH_URL.format(query)
        self.download_location = downloadLocation if downloadLocation is not None else Constants.DATA_PATH
        print(self.download_location)
        if os.path.exists(self.download_location):
            shutil.rmtree(self.download_location)
        os.makedirs(self.download_location )

    def _getBookUrl(self,id):
        return Constants.GUTENBERG_EBOOK_BASE.format(**{"ID" : id})

    def GetBooks(self):
        data = requests.get(self.query_url)
        soup = BeautifulSoup(data.text)
        allBooks = soup.select("li.booklink  a")
        titles = [a.select_one("span.title").text.strip("\r\n ") for a in allBooks]
        links = [a["href"] for a in allBooks]
        ids = [ re.findall("\d+" , i)[0] for i in links]
        downloadLocation = Constants.DATA_PATH
        for i,id in enumerate(ids):
            text = self.GetBook(id)
            self.PersistBook(titles[i] , text)

    def PersistBook(self,title, text):
        name = f"{title}.txt"
        path = os.path.abspath(os.path.join(self.download_location , name))
        with open(path, "w" , encoding="utf-8") as f:
            f.write(text)

    def GetBook(self,id):
        id = "61626"
        url = self._getBookUrl(id)
        url = "https://www.gutenberg.org/ebooks/61626"
        book_page = requests.get(url)
        soup = BeautifulSoup(book_page.text)
        txt_url = soup.select_one("a[title='Download'][href*='txt']")["href"]
        book_download_url = Constants.GUTENBERG_rel_to_abs(txt_url)
        book = requests.get(book_download_url)
        return book.text


GetData("religion").GetBooks()
