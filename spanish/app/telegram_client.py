import requests

from .config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_message(message: str) -> bool:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"Telegram error: {e}")
        return False


def send_telegram_voice(
    audio_bytes: bytes,
    caption: str | None = None,
    filename: str = "word.mp3",
) -> bool:
    """
    Send a voice note, optionally with an HTML caption so the word, translation
    and example sentences arrive as a single message.

    Telegram's sendVoice accepts MP3 (per Bot API docs), so we can forward the
    SpanishDict MP3 directly without transcoding.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVoice"
    data = {"chat_id": TELEGRAM_CHAT_ID}
    if caption:
        data["caption"] = caption
        data["parse_mode"] = "HTML"
    files = {"voice": (filename, audio_bytes, "audio/mpeg")}
    try:
        r = requests.post(url, data=data, files=files, timeout=15)
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"Telegram voice error: {e}")
        return False


