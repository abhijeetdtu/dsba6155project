
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
