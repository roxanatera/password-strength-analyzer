import re
import os

KEYBOARD_WALKS = [
    "qwerty", "qwert", "asdf", "asdfg", "zxcv", "zxcvb",
    "12345", "123456", "1234567", "12345678",
    "abcde", "abcdef", "abcd",
]

COMMON_WORDS = [
    "password", "passwd", "pass", "admin", "login", "user",
    "welcome", "letmein", "monkey", "dragon", "master",
    "sunshine", "princess", "football", "shadow", "superman",
    "michael", "jessica", "password1", "iloveyou",
]

LEET_MAP = {
    "@": "a", "4": "a", "3": "e", "1": "i", "!": "i",
    "0": "o", "5": "s", "$": "s", "7": "t", "+": "t",
}


def _load_wordlist() -> set:
    """Load common passwords from data/top10k.txt relative to project root."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base, "data", "top10k.txt")
    try:
        with open(path) as f:
            return {line.strip().lower() for line in f if line.strip()}
    except FileNotFoundError:
        return set()


# Merge hardcoded list + file wordlist
WORDLIST = set(COMMON_WORDS) | _load_wordlist()


def _deleet(password: str) -> str:
    result = password.lower()
    for leet, normal in LEET_MAP.items():
        result = result.replace(leet, normal)
    return result


def detect_patterns(password: str) -> list[dict]:
    warnings = []
    lower = password.lower()
    deleeted = _deleet(password)

    # Keyboard walks
    for walk in KEYBOARD_WALKS:
        if walk in lower:
            warnings.append({
                "type": "keyboard_walk",
                "detail": f'Contains keyboard sequence "{walk}"',
                "penalty": 20,
            })
            break

    # Exact match against full wordlist (highest penalty)
    if lower in WORDLIST or deleeted in WORDLIST:
        warnings.append({
            "type": "common_word",
            "detail": f'"{password}" is in the common passwords list — trivially crackable',
            "penalty": 40,
        })
    else:
        # Partial match — common word contained inside the password
        for word in COMMON_WORDS:
            if len(word) >= 4 and (word in lower or word in deleeted):
                warnings.append({
                    "type": "common_word",
                    "detail": f'Contains common word "{word}"',
                    "penalty": 25,
                })
                break

    # Leet speak substitutions
    if deleeted != lower and any(word in deleeted for word in COMMON_WORDS):
        warnings.append({
            "type": "leet_speak",
            "detail": "Leet substitutions detected on a common word (e.g. p@ssw0rd)",
            "penalty": 10,
        })

    # Repeated characters
    if re.search(r"(.)\1{2,}", password):
        warnings.append({
            "type": "repeated_chars",
            "detail": "Contains 3+ repeated characters in a row (e.g. aaa, 111)",
            "penalty": 15,
        })

    # Year pattern
    if re.search(r"(19|20)\d{2}", password):
        warnings.append({
            "type": "year",
            "detail": "Contains a year (e.g. 1990, 2024) — predictable",
            "penalty": 10,
        })

    # Only digits
    if password.isdigit():
        warnings.append({
            "type": "digits_only",
            "detail": "Password contains only digits",
            "penalty": 20,
        })

    # Too short
    if len(password) < 8:
        warnings.append({
            "type": "too_short",
            "detail": f"Too short ({len(password)} chars) — minimum recommended is 12",
            "penalty": 30,
        })

    return warnings


def get_suggestions(password: str, warnings: list[dict]) -> list[str]:
    tips = []
    types = {w["type"] for w in warnings}

    if len(password) < 12:
        tips.append("Use at least 12 characters — length is the biggest factor")
    if "common_word" in types or "leet_speak" in types:
        tips.append("Avoid dictionary words, even with leet substitutions (@, 3, 0)")
    if "keyboard_walk" in types:
        tips.append("Avoid keyboard sequences like qwerty or 12345")
    if "repeated_chars" in types:
        tips.append("Remove repeated characters (aaa, !!!)")
    if "year" in types:
        tips.append("Don't use years — attackers try them first")
    if "digits_only" in types:
        tips.append("Mix uppercase, lowercase, digits and symbols")
    if not tips:
        tips.append("Looking good! Consider using a passphrase for even better memorability")

    return tips
