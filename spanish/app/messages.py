def format_message(word: str, translation: str, examples) -> str:
    msg = f"<b>{word}</b> → <i>{translation}</i>\n"
    for ex in examples:
        msg += f"\n🇪🇸 <b>{ex['es']}</b>\n🇺🇸 {ex['en']}\n"
    return msg.strip()


