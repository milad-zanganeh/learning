def format_message(word: str, translation: str, examples) -> str:
    """
    Build a Telegram message using HTML formatting.
    """
    msg = f"<b>{word}</b> → <span class=\"tg-spoiler\"><i>{translation}</i></span>\n"

    for ex in examples:
        msg += (
            f"\n🇪🇸 <b>{ex['es']}</b>\n"
            f"🇺🇸 <span class=\"tg-spoiler\">{ex['en']}</span>\n"
        )

    return msg.strip()


