# Password Strength Analyzer & Secure Vault

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![OWASP](https://img.shields.io/badge/OWASP-Compliant-red?style=for-the-badge)](https://owasp.org/)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)]()

**A real-time password strength analyzer with entropy scoring, pattern detection, breach database lookup, and a secure local vault for password storage.**

**Un analizador de fortaleza de contraseñas en tiempo real con puntuación de entropía, detección de patrones, consulta a bases de datos de filtraciones, y un vault local seguro para almacenamiento de contraseñas.**

[Features](#-features-características) · [Demo](#-demo) · [Installation](#-installation-instalación) · [Usage](#-usage-uso) · [How It Works](#-how-it-works-cómo-funciona) · [Roadmap](#-roadmap-hoja-de-ruta)

---

## Demo

![demo](assets/demo.png)

> *Real-time analysis as you type — entropy score, breach check and actionable feedback*
> 
> *Análisis en tiempo real mientras escribes — puntuación de entropía, verificación de filtraciones y comentarios accionables*

---

## Features / Características

### Password Analysis / Análisis de Contraseñas

| Feature | Description | Descripción |
|---------|-------------|-------------|
| **Entropy Score** | Calculates bits of entropy using character set and length | Calcula bits de entropía usando conjunto de caracteres y longitud |
| **Pattern Detection** | Identifies keyboard walks, dates, repeated chars, common words | Identifica patrones de teclado, fechas, caracteres repetidos, palabras comunes |
| **Breach Check** | Checks against Have I Been Pwned API (k-anonymity, no plaintext sent) | Consulta la API de Have I Been Pwned (k-anonimidad, no se envía texto plano) |
| **Dictionary Attack Sim** | Tests against top 10k passwords from RockYou dataset | Prueba contra las 10k contraseñas más comunes del dataset RockYou |
| **Rich CLI Output** | Color-coded feedback using `rich` library | Comentarios con códigos de colores usando la librería `rich` |
| **Web UI** | Optional Flask interface with live strength meter | Interfaz Flask opcional con medidor de fortaleza en vivo |
| **Scoring Report** | Detailed breakdown exportable as JSON | Desglose detallado exportable como JSON |

### Secure Vault / Vault Seguro

| Feature | Description | Descripción |
|---------|-------------|-------------|
| **Master Key Derivation** | PBKDF2-HMAC-SHA256 with 600k iterations and unique salt | Derivación de clave maestra con PBKDF2-HMAC-SHA256, 600k iteraciones y salt único |
| **AES-256-GCM Encryption** | Authenticated encryption that detects tampering | Cifrado autenticado que detecta manipulaciones |
| **Local JSON Vault** | All data stays on your machine, encrypted at rest | Todos los datos permanecen en tu máquina, cifrados en reposo |
| **CRUD Operations** | Add, retrieve, update, and delete stored entries | Añadir, recuperar, actualizar y borrar entradas almacenadas |

---

## Installation / Instalación

### Prerequisites / Prerrequisitos

- Python 3.10+
- pip

### Clone & install / Clonar e instalar

```bash
git clone https://github.com/roxanatera/password-strength-analyzer.git
cd password-strength-analyzer
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Dependencies / Dependencias

```
rich>=13.0
requests>=2.28
zxcvbn>=4.4.28
cryptography>=41.0
flask>=2.3          # optional, for web UI / opcional, para interfaz web
pytest>=7.0         # optional, for tests / opcional, para pruebas
```

---

## Usage / Uso

### CLI — single password / contraseña única

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
│ HaveIBeenPwned  Not found               │
├─────────────────────────────────────────┤
│  Warnings                               │
│  - Contains dictionary word: "password" │
│  - Predictable leet substitution: @->a  │
├─────────────────────────────────────────┤
│  Suggestions                            │
│  - Add 2+ more random characters        │
│  - Avoid common substitutions           │
└─────────────────────────────────────────┘
```

### CLI — interactive mode / modo interactivo

```bash
python analyzer.py --interactive
```

### Web UI (Flask)

```bash
python web/app.py
# Open http://localhost:5000
# Abrir http://localhost:5000
```

### Batch mode (for auditing) / Modo por lotes (para auditoría)

```bash
python analyzer.py --batch passwords.txt --output report.json
```

### Vault Operations / Operaciones del Vault

**Initialize vault / Inicializar vault:**

```python
from core import vault

vault.init_vault('your_master_password')
# Creates vault.json with encrypted empty storage
# Crea vault.json con almacenamiento vacío cifrado
```

**Unlock vault / Desbloquear vault:**

```python
from core import vault

entries = vault.unlock_vault('your_master_password')
# Returns list of stored entries
# Devuelve lista de entradas almacenadas
```

**Save entries / Guardar entradas:**

```python
from core import vault

entries = vault.unlock_vault('your_master_password')
entries.append({
    'site': 'github.com',
    'username': 'your_username',
    'password': 'your_password'
})
vault.save_vault('your_master_password', entries)
```

---

## How It Works / Cómo Funciona

### Password analysis flow / Flujo de análisis de contraseñas

```
Input Password / Contraseña de entrada
      |
      v
+-------------+    +------------------+    +-----------------+
|  Entropy    |    | Pattern          |    |  Breach         |
|  Calculator |    | Detector         |    |  Lookup (HIBP)  |
|             |    |                  |    |                 |
| - charset   |    | - keyboard walks |    | - SHA-1 prefix  |
| - length    |    | - leet speak     |    | - k-anonymity   |
| - uniqueness|    | - dates/years    |    | - pwned count   |
+------+------+    +-------+----------+    +--------+--------+
       |                   |                        |
       +-------------------+------------------------+
                           |
                           v
                   +---------------+
                   |  Score Engine |
                   |  0 - 100 pts  |
                   +-------+-------+
                           |
                           v
                   +---------------+
                   |  Rich Report  |
                   |  CLI / JSON   |
                   +---------------+
```

### Entropy formula / Fórmula de entropía

```
Entropy (bits) = log2(charset_size ^ length)
```

| Charset / Conjunto | Size / Tamaño |
|--------------------|---------------|
| Lowercase only / Solo minúsculas | 26 |
| + Uppercase / + Mayúsculas | 52 |
| + Numbers / + Números | 62 |
| + Symbols / + Símbolos | 95 |

A password with **>60 bits** of entropy is considered strong against offline attacks.

Una contraseña con **>60 bits** de entropía se considera fuerte contra ataques offline.

### Vault cryptography / Criptografía del Vault

```
Master Password / Contraseña Maestra
       |
       v
+---------------------------+
| PBKDF2-HMAC-SHA256        |
| iterations = 600000       |
| salt = os.urandom(16)     |
+-------------+-------------+
              |
              v
       256-bit key / clave de 256 bits
              |
              v
+---------------------------+
| AES-256-GCM               |
| nonce = os.urandom(12)    |
| encrypt(plaintext)        |
| -> nonce + ciphertext     |
|    + auth tag             |
+---------------------------+
              |
              v
      vault.json (at rest / en reposo)
```

**English:**
- **PBKDF2** turns the master password into a 256-bit key, applying 600,000 iterations to slow down brute force attacks.
- **AES-GCM** provides authenticated encryption: it encrypts the data and generates a tag that detects any modification.
- **Salt and nonce** are stored in plaintext next to the ciphertext. They are not secrets — they guarantee uniqueness.

**Español:**
- **PBKDF2** convierte la contraseña maestra en una clave de 256 bits, aplicando 600,000 iteraciones para ralentizar ataques de fuerza bruta.
- **AES-GCM** proporciona cifrado autenticado: cifra los datos y genera un tag que detecta cualquier modificación.
- **Salt y nonce** se almacenan en texto plano junto al texto cifrado. No son secretos — garantizan unicidad.

### Crypto module implementation / Implementación del módulo crypto

**English:**

The `core/crypto.py` module provides four core functions:

1. **`generate_salt()`** - Generates 16 random bytes using `os.urandom()`
2. **`derive_key(master_password, salt, iterations=600000)`** - Derives a 256-bit key using PBKDF2-HMAC-SHA256
3. **`encrypt(data, key)`** - Encrypts data using AES-256-GCM with a 12-byte random nonce
4. **`decrypt(encrypted_data, key)`** - Decrypts and verifies data integrity

```python
from core.crypto import generate_salt, derive_key, encrypt, decrypt

# Generate salt and derive key
salt = generate_salt()
key = derive_key('master_password', salt)

# Encrypt
encrypted = encrypt('sensitive data', key)
# Returns: {'nonce': 'hex...', 'ciphertext': 'hex...'}

# Decrypt
decrypted = decrypt(encrypted, key)
# Returns: 'sensitive data'
```

**Español:**

El módulo `core/crypto.py` proporciona cuatro funciones principales:

1. **`generate_salt()`** - Genera 16 bytes aleatorios usando `os.urandom()`
2. **`derive_key(master_password, salt, iterations=600000)`** - Deriva una clave de 256 bits usando PBKDF2-HMAC-SHA256
3. **`encrypt(data, key)`** - Cifra datos usando AES-256-GCM con un nonce aleatorio de 12 bytes
4. **`decrypt(encrypted_data, key)`** - Descifra y verifica la integridad de los datos

```python
from core.crypto import generate_salt, derive_key, encrypt, decrypt

# Generar salt y derivar clave
salt = generate_salt()
key = derive_key('contraseña_maestra', salt)

# Cifrar
encrypted = encrypt('datos sensibles', key)
# Devuelve: {'nonce': 'hex...', 'ciphertext': 'hex...'}

# Descifrar
decrypted = decrypt(encrypted, key)
# Devuelve: 'datos sensibles'
```

### Vault module implementation / Implementación del módulo vault

**English:**

The `core/vault.py` module manages encrypted password storage:

1. **`init_vault(master_password)`** - Creates a new vault with encrypted empty storage
2. **`unlock_vault(master_password)`** - Decrypts and returns the list of stored entries
3. **`save_vault(master_password, entries)`** - Encrypts and saves entries to disk

The vault uses a JSON file (`vault.json`) with this structure:

```json
{
  "salt": "hex_string",
  "nonce": "hex_string",
  "ciphertext": "hex_string"
}
```

**Español:**

El módulo `core/vault.py` gestiona el almacenamiento cifrado de contraseñas:

1. **`init_vault(master_password)`** - Crea un nuevo vault con almacenamiento vacío cifrado
2. **`unlock_vault(master_password)`** - Descifra y devuelve la lista de entradas almacenadas
3. **`save_vault(master_password, entries)`** - Cifra y guarda las entradas en disco

El vault usa un archivo JSON (`vault.json`) con esta estructura:

```json
{
  "salt": "cadena_hex",
  "nonce": "cadena_hex",
  "ciphertext": "cadena_hex"
}
```

---

## Project Structure / Estructura del Proyecto

```
password-strength-analyzer/
|
+-- analyzer.py          # Main CLI entrypoint / Punto de entrada CLI principal
+-- core/
|   +-- __init__.py      # Package initialization / Inicialización del paquete
|   +-- entropy.py       # Entropy calculation / Cálculo de entropía
|   +-- patterns.py      # Pattern detection engine / Motor de detección de patrones
|   +-- hibp.py          # Have I Been Pwned API client / Cliente API HIBP
|   +-- scorer.py        # Final score aggregation / Agregación de puntuación final
|   +-- crypto.py        # PBKDF2, AES-GCM encrypt/decrypt / Cifrado/descifrado
|   +-- vault.py         # Vault CRUD operations / Operaciones CRUD del vault
|
+-- web/
|   +-- app.py           # Flask app / Aplicación Flask
|   +-- templates/
|       +-- index.html   # Live strength meter UI / UI de medidor en vivo
|
+-- data/
|   +-- top10k.txt       # Common passwords wordlist / Lista de contraseñas comunes
|
+-- tests/
|   +-- test_entropy.py
|   +-- test_patterns.py
|   +-- test_scorer.py
|   +-- test_crypto.py   # (WIP) Crypto round-trip tests / (En progreso) Pruebas de cifrado
|
+-- assets/
|   +-- demo.png         # Demo screenshot / Captura de demostración
|
+-- vault.json           # Encrypted vault (created at runtime) / Vault cifrado (creado en ejecución)
+-- requirements.txt
+-- .gitignore
+-- README.md
```

---

## Tests / Pruebas

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

## Privacy & Ethics / Privacidad y Ética

**English:**
- **HIBP check uses k-anonymity**: only the first 5 characters of the SHA-1 hash are sent over the network. Your password is **never transmitted**.
- **Vault data never leaves your machine**: everything is encrypted locally with AES-256-GCM before being written to disk.
- This tool is intended for **educational and defensive** purposes only.
- Do not use it to audit passwords you don't own.

**Español:**
- **La verificación HIBP usa k-anonimidad**: solo los primeros 5 caracteres del hash SHA-1 se envían por la red. Tu contraseña **nunca se transmite**.
- **Los datos del vault nunca salen de tu máquina**: todo se cifra localmente con AES-256-GCM antes de escribirse en disco.
- Esta herramienta está destinada únicamente a fines **educativos y defensivos**.
- No la uses para auditar contraseñas que no te pertenecen.

---

## Roadmap / Hoja de Ruta

- [x] CLI with entropy scoring / CLI con puntuación de entropía
- [x] Pattern detection engine / Motor de detección de patrones
- [x] HIBP breach lookup / Consulta de filtraciones HIBP
- [x] Crypto primitives (PBKDF2, AES-GCM) / Primitivas criptográficas (PBKDF2, AES-GCM)
- [x] Basic vault operations (init, unlock, save) / Operaciones básicas del vault (inicializar, desbloquear, guardar)
- [ ] Complete vault CRUD operations / Completar operaciones CRUD del vault
- [ ] Password generator with strength feedback / Generador de contraseñas con retroalimentación de fortaleza
- [ ] Tests for crypto and vault modules / Pruebas para módulos de crypto y vault
- [ ] CLI commands for vault management / Comandos CLI para gestión del vault
- [ ] Integration: score passwords on add/update / Integración: puntuar contraseñas al añadir/actualizar
- [ ] Browser extension version / Versión de extensión de navegador
- [ ] Support for passphrases (NIST SP 800-63B) / Soporte para frases de contraseña (NIST SP 800-63B)
- [ ] Docker image / Imagen Docker

---

## References & Learning / Referencias y Aprendizaje

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [NIST SP 800-63B -- Digital Identity Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [Have I Been Pwned API](https://haveibeenpwned.com/API/v3)
- [zxcvbn -- Realistic password strength estimation](https://github.com/dropbox/zxcvbn)
- [cryptography.io -- Python crypto library](https://cryptography.io/)

---

## Author / Autora

**Julia Roxana Natera**

[LinkedIn](https://www.linkedin.com/in/julia-roxana-natera-917b62172/)

> Built as part of my cybersecurity learning journey. Feedback and PRs welcome!
> 
> Construido como parte de mi camino de aprendizaje en ciberseguridad. ¡Comentarios y PRs son bienvenidos!
