def format_message(
    word: str,
    translation: str,
    examples,
    list_name: str | None = None,
) -> str:
    """
    Build a Telegram message using HTML formatting.
    """
    msg = f"<b>{word}</b> → <span class=\"tg-spoiler\"><i>{translation}</i></span>\n"

    for ex in examples:
        msg += (
            f"\n🇪🇸 <b>{ex['es']}</b>\n"
            f"🇺🇸 <span class=\"tg-spoiler\">{ex['en']}</span>\n"
        )

    msg = msg.strip()

    if list_name:
        msg += f"\n\n#{list_name}"

    return msg


