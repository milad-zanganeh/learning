import json
import re

import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from urllib.parse import quote, unquote

from .config import HEADERS

_AUDIO_URL_RE = re.compile(r'"audioUrl":"([^"]+)"')


def get_word_translation_pairs(url: str):
    """
    Fetches the word translation pairs from the URL.
    """
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
    """
    encoded_word = quote(word, safe="")
    url = f"https://www.spanishdict.com/examples/{encoded_word}?lang=es"
    print(f"[get_examples] Fetching examples for '{word}' -> {url}")
    r = requests.get(url, headers=HEADERS)
    print(f"[get_examples] HTTP status for '{word}': {r.status_code}")

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
    rows = soup.find_all("tr", {"data-testid": "example-row"})
    print(f"[get_examples] Found {len(rows)} raw example rows for '{word}'")

    for row in rows[:max_examples]:
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


def get_audio_url(word: str, lang: str = "es") -> str | None:
    """
    Fetch the SpanishDict pronunciation URL for a word.

    SpanishDict embeds a `SD_COMPONENT_DATA` JSON blob in the translate page
    that contains one or more `audioUrl` entries pointing at signed MP3s on
    `audio-cdn.sdcdns.com`. The signing `key` is server-generated, so the URL
    must be scraped (it cannot be reconstructed client-side).
    """
    encoded = quote(word, safe="")
    page_url = f"https://www.spanishdict.com/translate/{encoded}"
    print(f"[get_audio_url] Fetching audio for '{word}' -> {page_url}")
    r = requests.get(page_url, headers=HEADERS, timeout=10)
    print(f"[get_audio_url] HTTP status for '{word}': {r.status_code}")
    r.raise_for_status()

    target = word.lower()
    for raw in _AUDIO_URL_RE.findall(r.text):
        # `raw` contains JSON \u002F escapes; decoding it as a JSON string
        # yields the real URL.
        decoded = json.loads(f'"{raw}"')
        if f"lang={lang}" not in decoded:
            continue
        m = re.search(r"text=([^&]+)", decoded)
        if m and unquote(m.group(1)).lower() == target:
            return decoded

    print(f"[get_audio_url] No '{lang}' audio found for '{word}'")
    return None


def download_audio(url: str) -> bytes | None:
    """Download an audio URL; return the raw bytes or None on failure."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        return r.content
    except Exception as e:
        print(f"[download_audio] Failed to download {url}: {e}")
        return None


