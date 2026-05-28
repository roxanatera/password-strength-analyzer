import math
import string


def get_charset_size(password: str) -> int:
    size = 0
    if any(c in string.ascii_lowercase for c in password):
        size += 26
    if any(c in string.ascii_uppercase for c in password):
        size += 26
    if any(c in string.digits for c in password):
        size += 10
    if any(c in string.punctuation for c in password):
        size += 32
    return size or 1


def calculate_entropy(password: str) -> float:
    charset = get_charset_size(password)
    return len(password) * math.log2(charset)


def estimate_crack_time(entropy: float) -> str:
    # Assumes 10 billion guesses/sec (offline, fast hash)
    guesses_per_sec = 1e10
    combinations = 2 ** entropy
    seconds = combinations / guesses_per_sec / 2  # average case

    if seconds < 1:
        return "instantly"
    elif seconds < 60:
        return f"~{int(seconds)} seconds"
    elif seconds < 3600:
        return f"~{int(seconds/60)} minutes"
    elif seconds < 86400:
        return f"~{int(seconds/3600)} hours"
    elif seconds < 31536000:
        return f"~{int(seconds/86400)} days"
    elif seconds < 3.154e9:
        return f"~{int(seconds/31536000)} years"
    else:
        return "centuries"
