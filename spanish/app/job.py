import random
import time

from .config import LIST_URLS, MAX_WORDS_PER_RUN
from .db import init_db, word_exists, insert_word
from .messages import format_message
from .scraper import (
    download_audio,
    get_audio_url,
    get_examples,
    get_word_translation_pairs,
)
from .telegram_client import send_telegram_message, send_telegram_voice


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

        # Try to fetch audio first so we can ship voice + caption as a
        # single Telegram message. If anything in the audio path fails (or
        # the caption wouldn't fit Telegram's 1024-char media-caption limit),
        # we fall back to a plain text message.
        audio_bytes = None
        try:
            audio_url = get_audio_url(spanish)
            if audio_url:
                audio_bytes = download_audio(audio_url)
            else:
                print(f"No pronunciation available for: {spanish}")
        except Exception as e:
            print(f"Audio lookup failed for '{spanish}': {e}")

        TELEGRAM_CAPTION_MAX = 1024
        success = False
        if audio_bytes and len(message) <= TELEGRAM_CAPTION_MAX:
            success = send_telegram_voice(audio_bytes, caption=message)
            if success:
                print(f"Sent voice + caption for: {spanish}")
            else:
                print(f"Voice send failed for '{spanish}', falling back to text")
        elif audio_bytes:
            print(
                f"Caption too long ({len(message)} chars) for '{spanish}', "
                "falling back to text-only"
            )

        if not success:
            success = send_telegram_message(message)

        if success:
            insert_word(spanish, english, examples)
            print(f"Sent and stored: {spanish}")
            added_count += 1
        else:
            print("Skipped DB insert due to Telegram failure.")

        time.sleep(1)  # delay between messages

    print(f"Finished. {added_count} new words sent.")


