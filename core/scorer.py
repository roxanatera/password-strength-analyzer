from core.entropy import calculate_entropy, estimate_crack_time
from core.patterns import detect_patterns, get_suggestions


def score_password(password: str) -> dict:
    entropy = calculate_entropy(password)
    warnings = detect_patterns(password)
    suggestions = get_suggestions(password, warnings)

    # Base score from entropy (0–70 points)
    if entropy < 28:
        base = 10
    elif entropy < 36:
        base = 25
    elif entropy < 50:
        base = 45
    elif entropy < 60:
        base = 60
    elif entropy < 80:
        base = 70
    else:
        base = 80

    # Bonus points for diversity
    import string
    bonus = 0
    if any(c in string.ascii_uppercase for c in password):
        bonus += 5
    if any(c in string.digits for c in password):
        bonus += 5
    if any(c in string.punctuation for c in password):
        bonus += 10

    # Apply penalties from patterns
    total_penalty = sum(w["penalty"] for w in warnings)

    final_score = max(0, min(100, base + bonus - total_penalty))

    # Label
    if final_score < 20:
        label = "VERY WEAK"
        color = "red"
    elif final_score < 40:
        label = "WEAK"
        color = "orange1"
    elif final_score < 60:
        label = "FAIR"
        color = "yellow"
    elif final_score < 80:
        label = "STRONG"
        color = "green"
    else:
        label = "VERY STRONG"
        color = "bright_green"

    return {
        "password": password,
        "score": final_score,
        "label": label,
        "color": color,
        "entropy": round(entropy, 1),
        "crack_time": estimate_crack_time(entropy),
        "warnings": warnings,
        "suggestions": suggestions,
    }
