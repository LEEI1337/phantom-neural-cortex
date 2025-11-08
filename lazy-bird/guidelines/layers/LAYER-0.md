# 📋 LAYER 0 - Universal Standards

**Gilt für:** ALLE Agents, ALLE Layer, ALLE Projekte
**Vererbung:** Keine (BASIS)
**Zweck:** Grundlegende Standards die IMMER gelten

---

## 🎯 Projekt-Struktur (PFLICHT)

### Standard-Verzeichnis-Layout

```
projekt-name/
├── src/                    # SOURCE CODE (Hauptverzeichnis)
│   ├── __init__.py        # Python Package Init
│   ├── index.ts           # TypeScript Entry Point
│   ├── main.py            # Python Entry Point
│   ├── lib/               # Core Libraries
│   ├── utils/             # Utility Functions
│   └── types/             # Type Definitions (TS)
│
├── tests/                  # TESTS (PFLICHT!)
│   ├── __init__.py        # Python Package
│   ├── unit/              # Unit Tests
│   ├── integration/       # Integration Tests
│   └── e2e/               # End-to-End Tests
│
├── docs/                   # DOKUMENTATION
│   ├── API.md             # API Dokumentation
│   ├── ARCHITECTURE.md    # Architektur
│   └── USAGE.md           # Nutzungs-Anleitung
│
├── .github/                # GITHUB INTEGRATION
│   └── workflows/         # GitHub Actions
│
├── config/                 # KONFIGURATION
│   ├── development.json
│   ├── production.json
│   └── test.json
│
├── scripts/                # UTILITY SCRIPTS
│   ├── setup.sh
│   └── test.sh
│
├── .gitignore              # Git Ignore
├── README.md               # Projekt Doku (PFLICHT!)
├── CHANGELOG.md            # Änderungs-Historie
└── LICENSE                 # MIT License
```

---

## 🚫 VERBOTEN - Anti-Patterns

### ❌ NIEMALS machen:

1. **Code im Root-Verzeichnis**
   ```
   ❌ FALSCH:
   projekt/
   ├── main.py           # Gehört nach src/!
   ├── helper.py         # Gehört nach src/lib/!
   └── utils.py          # Gehört nach src/utils/!
   ```

2. **Tests außerhalb von tests/**
   ```
   ❌ FALSCH:
   projekt/
   ├── src/
   │   └── test_inline.py    # FALSCH!
   └── main_test.py          # FALSCH!
   ```

3. **Flache Struktur ohne Organisation**
   ```
   ❌ FALSCH:
   projekt/
   ├── file1.py
   ├── file2.py
   ├── file3.py
   └── file4.py          # Keine Struktur!
   ```

---

## 📝 Naming Conventions

### Python

```python
# Dateien & Module
my_module.py                    # snake_case
my_package/__init__.py

# Klassen
class UserManager:              # PascalCase
    pass

# Funktionen & Methoden
def calculate_total():          # snake_case
    pass

# Konstanten
MAX_RETRY_COUNT = 3             # UPPER_SNAKE_CASE
API_BASE_URL = "https://..."

# Private
_internal_function()            # Leading underscore
__private_attribute             # Double underscore

# Tests
test_user_creation.py           # test_*.py
tests/test_*.py                 # oder in tests/
```

### TypeScript/JavaScript

```typescript
// Dateien
user-manager.ts                 // kebab-case
UserCard.tsx                    // PascalCase (React Components)

// Klassen & Interfaces
class UserManager {}            // PascalCase
interface User {}               // PascalCase
type UserRole = 'admin' | 'user';  // PascalCase

// Funktionen & Variables
function calculateTotal() {}    // camelCase
const userName = "John";        // camelCase

// Konstanten
const MAX_RETRY_COUNT = 3;      // UPPER_SNAKE_CASE
const API_BASE_URL = "https://";

// React Components
function UserCard() {}          // PascalCase
const UserProfile = () => {};   // PascalCase

// Tests
user-manager.test.ts            // *.test.ts
user-manager.spec.ts            // *.spec.ts
```

---

## ✅ Code Quality Standards

### 1. DRY (Don't Repeat Yourself)

```python
# ✅ RICHTIG
def validate_email(email: str) -> bool:
    return "@" in email and "." in email

def process_user(email: str):
    if not validate_email(email):
        raise ValueError("Invalid email")

def process_admin(email: str):
    if not validate_email(email):        # Wiederverwendung!
        raise ValueError("Invalid email")

# ❌ FALSCH
def process_user(email: str):
    if not ("@" in email and "." in email):  # Duplikation!
        raise ValueError("Invalid email")

def process_admin(email: str):
    if not ("@" in email and "." in email):  # Duplikation!
        raise ValueError("Invalid email")
```

### 2. Single Responsibility

```python
# ✅ RICHTIG: Jede Funktion eine Aufgabe
def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()

def parse_json(content: str) -> dict:
    return json.loads(content)

def validate_data(data: dict) -> bool:
    return "name" in data and "email" in data

# ❌ FALSCH: Alles in einer Funktion
def process_file(path: str) -> bool:
    with open(path) as f:
        content = f.read()
    data = json.loads(content)
    return "name" in data and "email" in data
```

### 3. Aussagekräftige Namen

```typescript
// ✅ RICHTIG
function calculateUserAgeInYears(birthDate: Date): number {
  const now = new Date();
  return now.getFullYear() - birthDate.getFullYear();
}

const isUserAdmin = user.role === 'admin';
const hasValidEmail = validateEmail(user.email);

// ❌ FALSCH
function calc(d: Date): number {  // Unklar!
  const n = new Date();
  return n.getFullYear() - d.getFullYear();
}

const flag = user.role === 'admin';  // Was ist flag?
const x = validateEmail(user.email); // Was ist x?
```

---

## 🔒 Security Basics (PFLICHT)

### 1. Input Validation

```python
# ✅ RICHTIG: IMMER validieren
def process_user_input(data: str) -> str:
    # Type Check
    if not isinstance(data, str):
        raise TypeError("Input must be string")

    # Length Check
    if len(data) > 1000:
        raise ValueError("Input too long")

    # Sanitize
    return html.escape(data)

# ❌ FALSCH: Keine Validation
def process_user_input(data):
    return data  # XSS Vulnerability!
```

### 2. No Secrets in Code

```python
# ✅ RICHTIG: Environment Variables
import os

API_KEY = os.getenv("API_KEY")
DB_PASSWORD = os.getenv("DB_PASSWORD")

if not API_KEY:
    raise ValueError("API_KEY not set")

# ❌ FALSCH: Hardcoded Secrets
API_KEY = "sk-1234567890abcdef"  # NIEMALS!
DB_PASSWORD = "password123"       # NIEMALS!
```

### 3. SQL Injection Prevention

```python
# ✅ RICHTIG: Prepared Statements
def get_user(user_id: int):
    cursor.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    )

# ❌ FALSCH: String Concatenation
def get_user(user_id: int):
    cursor.execute(
        f"SELECT * FROM users WHERE id = {user_id}"  # SQL Injection!
    )
```

---

## 🧪 Testing Basics

### Minimum Requirements

1. **Mindestens 1 Test pro Funktion/Klasse**
2. **Tests in `tests/` Verzeichnis**
3. **Tests müssen ausführbar sein** (`pytest tests/` oder `npm test`)
4. **Keine Tests im Production Code** (nur in `tests/`)

### Test-Naming

```python
# Python
def test_user_creation():           # test_*
def test_invalid_email_raises_error():

# TypeScript
describe('UserManager', () => {
  it('should create user', () => {});
  it('should throw error for invalid email', () => {});
});
```

---

## 📚 Documentation Basics

### README.md (PFLICHT)

Jedes Projekt MUSS haben:

```markdown
# Project Name

One-line description.

## Installation

\`\`\`bash
installation command
\`\`\`

## Usage

\`\`\`python
simple example
\`\`\`

## Testing

\`\`\`bash
pytest tests/
\`\`\`

## License

MIT
```

### Code Comments

```python
# ✅ RICHTIG: Docstrings für öffentliche Funktionen
def calculate_total(items: List[Item]) -> float:
    """
    Calculate total price of items.

    Args:
        items: List of items to sum

    Returns:
        Total price in euros

    Example:
        >>> items = [Item(price=10), Item(price=20)]
        >>> calculate_total(items)
        30.0
    """
    return sum(item.price for item in items)

# ✅ RICHTIG: Inline-Comments für komplexe Logik
# Apply discount based on user tier
if user.tier == "gold":
    discount = 0.20
elif user.tier == "silver":
    discount = 0.10
else:
    discount = 0.05

# ❌ FALSCH: Überflüssige Comments
# Increment counter
counter += 1  # Das sieht man auch so!
```

---

## 📦 Dependencies

### Pinned Versions (PFLICHT)

```txt
# requirements.txt - RICHTIG
fastapi==0.104.1
pydantic==2.5.0
pytest==7.4.3

# requirements.txt - FALSCH
fastapi
pydantic  # Kann brechen!
pytest
```

```json
// package.json - RICHTIG
{
  "dependencies": {
    "express": "4.18.2",
    "typescript": "5.3.3"
  }
}

// package.json - FALSCH
{
  "dependencies": {
    "express": "*",      // Gefährlich!
    "typescript": "latest"  // Kann brechen!
  }
}
```

---

## 🎯 .gitignore (PFLICHT)

Jedes Projekt MUSS ignorieren:

```gitignore
# Build Outputs
dist/
build/
*.pyc
__pycache__/

# Dependencies
node_modules/
venv/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Secrets
.env
*.key
*.pem
secrets.json

# Logs
*.log
logs/
```

---

## ✅ Qualitäts-Checkliste

Jedes Projekt MUSS:

- [ ] Korrekte Verzeichnis-Struktur (`src/`, `tests/`, `docs/`)
- [ ] Code nur in `src/`, NICHT im Root
- [ ] README.md mit vollständiger Doku
- [ ] Mindestens 1 funktionierender Test
- [ ] .gitignore vorhanden
- [ ] Pinned Dependencies
- [ ] Keine Secrets im Code
- [ ] Aussagekräftige Namen
- [ ] Input Validation
- [ ] LICENSE Datei (MIT)

---

## 🚨 Bei Verstößen

Wenn diese Standards NICHT befolgt werden:

1. **Code Review schlägt fehl**
2. **Tests werden nicht akzeptiert**
3. **PR wird abgelehnt**
4. **Nachbesserung erforderlich**

---

**Diese Standards sind NICHT verhandelbar!** 🎯

Sie gelten für:
- ✅ Layer 1 (MCP Servers)
- ✅ Layer 2 (AI CLIs)
- ✅ Layer 3 (Rover)
- ✅ Layer 4 (Lazy Bird)
- ✅ ALLE Agents (Claude, Gemini, Copilot)
- ✅ ALLE Projekt-Typen (Python, TypeScript, React, etc.)

**Nächster Layer:** [LAYER-1.md](LAYER-1.md) - MCP Server Usage
