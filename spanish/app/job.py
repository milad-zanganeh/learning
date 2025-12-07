import random
import time

from .config import LIST_URLS, MAX_WORDS_PER_RUN
from .db import init_db, word_exists, insert_word
from .messages import format_message
from .scraper import get_word_translation_pairs, get_examples
from .telegram_client import send_telegram_message


def run_once() -> None:
    """Run a single job: pick a list, send up to MAX_WORDS_PER_RUN new words."""
    init_db()
    added_count = 0

    url = random.choice(LIST_URLS)
    print(f"Fetching list: {url}")
    word_pairs = get_word_translation_pairs(url)

    for spanish, english in word_pairs:
        if added_count >= MAX_WORDS_PER_RUN:
            print(f"Limit reached: {MAX_WORDS_PER_RUN} words.")
            return

        if word_exists(spanish):
            continue

        print(f"Processing: {spanish} → {english}")
        examples = get_examples(spanish)

        if not examples:
            print(f"Skipping: {spanish} → {english} - no examples found")
            continue

        message = format_message(spanish, english, examples)
        success = send_telegram_message(message)

        if success:
            insert_word(spanish, english, examples)
            print(f"Sent and stored: {spanish}")
            added_count += 1
        else:
            print("Skipped DB insert due to Telegram failure.")

        time.sleep(1)  # delay between messages

    print(f"Finished. {added_count} new words sent.")


