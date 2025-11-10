#!/usr/bin/env python3
"""Remove all emojis from files"""
import re
from pathlib import Path

def remove_emojis(text):
    """Remove all emojis from text"""
    # Unicode emoji ranges
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002600-\U000026FF"  # Miscellaneous Symbols
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)

files_to_clean = [
    "lazy-bird/guidelines/claude-guidelines.md",
    "lazy-bird/guidelines/layers/LAYER-2-CLAUDE.md",
    "lazy-bird/guidelines/gemini-guidelines.md",
    "lazy-bird/guidelines/copilot-guidelines.md",
]

for file_path in files_to_clean:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        cleaned = remove_emojis(content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned)

        print(f"[CLEANED] {file_path}")
    except Exception as e:
        print(f"[ERROR] {file_path}: {e}")

print("\n[DONE] All emojis removed")
