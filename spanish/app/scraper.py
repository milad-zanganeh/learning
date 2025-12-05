import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from urllib.parse import quote

from .config import HEADERS


def get_word_translation_pairs(url: str):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    word_blocks = soup.find_all("div", class_="M51vAoht")
    results = []
    for block in word_blocks:
        word_div = block.find("div", class_="UO6pWUJR")
        trans_div = block.find("div", class_="xLusdC9B")
        if word_div and trans_div:
            spanish = word_div.get_text(strip=True)
            english = trans_div.get_text(strip=True)
            results.append((spanish, english))
    return results


def get_examples(word: str, max_examples: int = 3):
    """
    Fetch example sentences for a word or phrase.

    We URL-encode the full phrase so that multi-word expressions like
    "dar un paseo" are looked up as a single unit instead of only the
    first word being used in the /examples/ URL.
    """
    encoded_word = quote(word, safe="")
    url = f"https://www.spanishdict.com/examples/{encoded_word}?lang=es"
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    def get_clean_text(div):
        parts = []
        for elem in div.children:
            if isinstance(elem, NavigableString):
                parts.append(str(elem))
            elif isinstance(elem, Tag):
                parts.append(" " + elem.get_text(strip=True) + " ")
        return " ".join("".join(parts).split())

    examples = []
    for row in soup.find_all("tr", {"data-testid": "example-row"})[:max_examples]:
        es = row.find("div", lang="es")
        en = row.find("div", lang="en")
        if es and en:
            examples.append(
                {
                    "es": get_clean_text(es),
                    "en": get_clean_text(en),
                }
            )
    return examples


