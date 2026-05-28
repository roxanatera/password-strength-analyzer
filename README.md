# 🔐 Password Strength Analyzer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![OWASP](https://img.shields.io/badge/OWASP-Compliant-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

**A real-time password strength analyzer with entropy scoring, pattern detection, and breach database lookup.**

[Features](#-features) · [Demo](#-demo) · [Installation](#-installation) · [Usage](#-usage) · [How it works](#-how-it-works) · [Roadmap](#-roadmap)

</div>

---

## 📸 Demo

<div align="center">

<!-- Replace with your own GIF recorded with asciinema or peek -->
![demo](assets/demo.png)

> *Real-time analysis as you type — entropy score, breach check and actionable feedback*

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧮 **Entropy Score** | Calculates bits of entropy using character set and length |
| 🔍 **Pattern Detection** | Identifies keyboard walks, dates, repeated chars, common words |
| 💥 **Breach Check** | Checks against Have I Been Pwned API (k-anonymity, no plaintext sent) |
| 📖 **Dictionary Attack Sim** | Tests against top 10k passwords from RockYou dataset |
| 🎨 **Rich CLI Output** | Color-coded feedback using `rich` library |
| 🌐 **Web UI** | Optional Flask interface with live strength meter |
| 📊 **Scoring Report** | Detailed breakdown exportable as JSON |

---

## 🚀 Installation

### Prerequisites

- Python 3.10+
- pip

### Clone & install

```bash
git clone https://github.com/yourusername/password-strength-analyzer.git
cd password-strength-analyzer
pip install -r requirements.txt
```

### Dependencies

```
rich>=13.0
requests>=2.28
zxcvbn>=4.4.28
flask>=2.3          # optional, for web UI
pytest>=7.0         # optional, for tests
```

---

## 🖥️ Usage

### CLI — single password

```bash
python analyzer.py --password "MyP@ssw0rd!"
```

**Output:**

```
┌─────────────────────────────────────────┐
│        Password Strength Report         │
├─────────────────────────────────────────┤
│ Score       ████████░░  72/100  STRONG  │
│ Entropy     43.2 bits                   │
│ Crack time  ~3 years (offline, fast)    │
│ HaveIBeenPwned  ✅ Not found            │
├─────────────────────────────────────────┤
│ ⚠️  Warnings                            │
│  • Contains dictionary word: "password" │
│  • Predictable leet substitution: @→a   │
├─────────────────────────────────────────┤
│ 💡 Suggestions                          │
│  • Add 2+ more random characters        │
│  • Avoid common substitutions           │
└─────────────────────────────────────────┘
```

### CLI — interactive mode

```bash
python analyzer.py --interactive
```

### Web UI (Flask)

```bash
python web/app.py
# Open http://localhost:5000
```

### Batch mode (for auditing)

```bash
python analyzer.py --batch passwords.txt --output report.json
```

---

## 🧠 How It Works

```
Input Password
      │
      ▼
┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Entropy    │    │ Pattern          │    │  Breach         │
│  Calculator │    │ Detector         │    │  Lookup (HIBP)  │
│             │    │                  │    │                 │
│ • charset   │    │ • keyboard walks │    │ • SHA-1 prefix  │
│ • length    │    │ • leet speak     │    │ • k-anonymity   │
│ • uniqueness│    │ • dates/years    │    │ • pwned count   │
└──────┬──────┘    └───────┬──────────┘    └────────┬────────┘
       │                   │                        │
       └───────────────────┴────────────────────────┘
                           │
                           ▼
                   ┌───────────────┐
                   │  Score Engine │
                   │  0 – 100 pts  │
                   └───────┬───────┘
                           │
                           ▼
                   ┌───────────────┐
                   │  Rich Report  │
                   │  CLI / JSON   │
                   └───────────────┘
```

### Entropy formula

```
Entropy (bits) = log₂(charset_size ^ length)
```

| Charset | Size |
|---|---|
| Lowercase only | 26 |
| + Uppercase | 52 |
| + Numbers | 62 |
| + Symbols | 95 |

A password with **>60 bits** of entropy is considered strong against offline attacks.

---

## 📂 Project Structure

```
password-strength-analyzer/
│
├── analyzer.py          # Main CLI entrypoint
├── core/
│   ├── entropy.py       # Entropy calculation
│   ├── patterns.py      # Pattern detection engine
│   ├── hibp.py          # Have I Been Pwned API client
│   └── scorer.py        # Final score aggregation
│
├── web/
│   ├── app.py           # Flask app
│   └── templates/
│       └── index.html   # Live strength meter UI
│
├── data/
│   └── top10k.txt       # Common passwords wordlist
│
├── tests/
│   ├── test_entropy.py
│   ├── test_patterns.py
│   └── test_scorer.py
│
├── assets/
│   └── demo.gif         # Demo GIF for README
│
├── requirements.txt
└── README.md
```

---

## 🧪 Tests

```bash
pytest tests/ -v
```

```
PASSED tests/test_entropy.py::test_lowercase_only
PASSED tests/test_entropy.py::test_mixed_charset
PASSED tests/test_patterns.py::test_keyboard_walk_detected
PASSED tests/test_patterns.py::test_leet_substitution
PASSED tests/test_scorer.py::test_strong_password_score
PASSED tests/test_scorer.py::test_breached_password_penalty

6 passed in 0.42s
```

---

## 🔒 Privacy & Ethics

- **HIBP check uses k-anonymity**: only the first 5 characters of the SHA-1 hash are sent over the network. Your password is **never transmitted**.
- This tool is intended for **educational and defensive** purposes only.
- Do not use it to audit passwords you don't own.

---

## 📈 Roadmap

- [x] CLI with entropy scoring
- [x] Pattern detection engine
- [x] HIBP breach lookup
- [ ] Browser extension version
- [ ] Password generator based on score feedback
- [ ] Support for passphrases (NIST SP 800-63B)
- [ ] Docker image

---

## 📚 References & Learning

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [NIST SP 800-63B — Digital Identity Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [Have I Been Pwned API](https://haveibeenpwned.com/API/v3)
- [zxcvbn — Realistic password strength estimation](https://github.com/dropbox/zxcvbn)

---

## 🙋 Author

**Your Name** · [LinkedIn](https://www.linkedin.com/in/julia-roxana-natera-917b62172/) · [Portfolio](https://yoursite.com)

> Built as part of my cybersecurity learning journey. Feedback and PRs welcome!

---

<div align="center">
<sub>⭐ Star this repo if you found it useful</sub>
</div>
