import os
import re
import requests
from bs4 import BeautifulSoup
import shutil

from multiprocessing.dummy import Pool as ThreadPool

import pathlib
import os

class Constants:
    GUTENBERG_URL = "https://www.gutenberg.org"
    GUTENBERG_SEARCH_URL = f"{GUTENBERG_URL}/ebooks/search/?query={{}}"
    GUTENBERG_DOWNLOAD_URL = f"{GUTENBERG_URL}/cache/epub/{{ID}}/pg{{ID}}.txt"
    GUTENBERG_EBOOK_BASE = f"{GUTENBERG_URL}/ebooks/{{ID}}"
    PROJECT_BASE_PATH = pathlib.Path().resolve()
    DATA_PATH =  os.path.abspath(os.path.join(PROJECT_BASE_PATH ,"dsba6155project", "data"))


    @staticmethod
    def GUTENBERG_rel_to_abs(rel):
        return Constants.GUTENBERG_URL + rel


class GetData:

    def __init__(self,query,refresh=False, downloadLocation=None):
        self.query = query
        self.query_url = Constants.GUTENBERG_SEARCH_URL.format(query)
        self.download_location = downloadLocation if downloadLocation is not None else Constants.DATA_PATH
        print(self.download_location)

        if refresh:
            if os.path.exists(self.download_location):
                shutil.rmtree(self.download_location)

        if not os.path.exists(self.download_location):
            os.makedirs(self.download_location )

        self.pool = ThreadPool(processes=3)


    def _safeName(self,name):
        return "".join([c for c in name if c.isalpha() or c.isdigit() or c==' ']).rstrip()

    def _getBookUrl(self,id):
        return Constants.GUTENBERG_EBOOK_BASE.format(**{"ID" : id})

    def GetIdsAndTitles(self):
        data = requests.get(self.query_url)
        soup = BeautifulSoup(data.text)
        allBooks = soup.select("li.booklink  a")
        titles = [a.select_one("span.title").text.strip("\r\n ") for a in allBooks]
        links = [a["href"] for a in allBooks]
        ids = [ re.findall("\d+" , i)[0] for i in links]
        return ids,titles

    def _getPersistBook(self,id,title):
        text = self.GetBook(id)
        self.PersistBook(title , text)

    def GetBooks(self):
        ids,titles = self.GetIdsAndTitles()
        #
        self.pool.starmap(self._getPersistBook ,[(id,titles[i]) for i,id in enumerate(ids)] )

    def PersistBook(self,title, text):
        name = f"{self.query}_{self._safeName(title)}.txt"
        path = os.path.abspath(os.path.join(self.download_location , name))
        with open(path, "w" , encoding="utf-8") as f:
            f.write(text)

    def GetBook(self,id):
        url = self._getBookUrl(id)
        book_page = requests.get(url)
        soup = BeautifulSoup(book_page.text)
        txt_url = soup.select_one("a[title='Download'][href*='txt']")["href"]
        book_download_url = Constants.GUTENBERG_rel_to_abs(txt_url)
        book = requests.get(book_download_url)
        return book.text




if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("Download Books from Project Gutenberg")
    parser.add_argument("--query" , help="The search query used")
    parser.add_argument("--folder-clean" ,default=False, type=lambda x: (str(x).lower() == 'true'), help="Clean the folder before download?")

    args = parser.parse_args()
    query = args.query
    refresh = args.folder_clean

    #queries = ["hinduism" , "religion" , "bible" , "islam" , "buddhism" , "sikh" , "judaism"]
    GetData(query,refresh).GetBooks()
