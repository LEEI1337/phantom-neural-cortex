#  Claude-Spezifische Guidelines

> ** DEPRECATED:** This file is deprecated. Please use the hierarchical layer system instead:
> - [LAYER-2-CLAUDE.md](layers/LAYER-2-CLAUDE.md) - Claude-specific guidelines
>
> **Migration Date:** 2025-11-09
> **Will be removed in:** Version 3.0.0

**Agent:** Claude (Anthropic)
**Use Case:** Security, Architecture, Complex Problems
**Kosten:** $20/mo
**Stärken:** Code-Qualität, Sicherheit, Best Practices

---

##  Wann Claude verwendet wird

Claude wird automatisch gewählt bei Issues mit Labels:
- `security` - Sicherheitsrelevante Tasks
- `architecture` - Architektur-Design
- `complex` - Komplexe Probleme
- `refactor` - Große Refactorings mit hoher Qualität

---

##  Claude-Spezifische Anforderungen

### 1. Security First

**IMMER** Security Best Practices anwenden:

```python
#  RICHTIG: Input Validation
def process_user_input(data: str) -> str:
    # Sanitize input
    if not isinstance(data, str):
        raise TypeError("Input must be string")
    if len(data) > 1000:
        raise ValueError("Input too long")
    # Escape HTML
    return html.escape(data)

#  FALSCH: Direkte Verwendung
def process_user_input(data):
    return data  # XSS vulnerability!
```

```typescript
//  RICHTIG: SQL Injection Prevention
const getUserById = async (id: number) => {
  return await db.query('SELECT * FROM users WHERE id = $1', [id]);
};

//  FALSCH: SQL Injection möglich
const getUserById = async (id: number) => {
  return await db.query(`SELECT * FROM users WHERE id = ${id}`);
};
```

### 2. Umfassende Error Handling

```python
#  RICHTIG: Proper Error Handling
def fetch_data(url: str) -> dict:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        logger.error(f"Timeout fetching {url}")
        raise
    except requests.HTTPError as e:
        logger.error(f"HTTP error: {e}")
        raise
    except ValueError as e:
        logger.error(f"Invalid JSON response: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

#  FALSCH: Bare except
def fetch_data(url):
    try:
        return requests.get(url).json()
    except:
        pass  # Silent failure!
```

### 3. Type Safety (TypeScript/Python)

```typescript
//  RICHTIG: Strict Types
interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'guest';
}

function getUser(id: number): Promise<User> {
  // Implementation
}

//  FALSCH: Any types
function getUser(id: any): Promise<any> {
  // Type safety lost!
}
```

```python
#  RICHTIG: Type Hints
from typing import List, Optional

def filter_users(
    users: List[User],
    role: Optional[str] = None
) -> List[User]:
    if role:
        return [u for u in users if u.role == role]
    return users

#  FALSCH: No type hints
def filter_users(users, role=None):
    # No type checking
    pass
```

### 4. Comprehensive Testing

Claude MUSS für JEDEN Feature:
- Unit Tests (mind. 80% Coverage)
- Integration Tests
- Edge Cases testen
- Error Cases testen

```python
#  RICHTIG: Comprehensive Tests
def test_user_creation():
    """Test normal user creation."""
    user = create_user("john@example.com", "password123")
    assert user.email == "john@example.com"
    assert user.password_hash != "password123"  # Hashed

def test_user_creation_invalid_email():
    """Test user creation with invalid email."""
    with pytest.raises(ValueError, match="Invalid email"):
        create_user("not-an-email", "password123")

def test_user_creation_weak_password():
    """Test user creation with weak password."""
    with pytest.raises(ValueError, match="Password too weak"):
        create_user("john@example.com", "123")

def test_user_creation_duplicate_email():
    """Test user creation with duplicate email."""
    create_user("john@example.com", "password123")
    with pytest.raises(IntegrityError):
        create_user("john@example.com", "password456")
```

### 5. Ausführliche Dokumentation

```python
#  RICHTIG: Comprehensive Docstring
def authenticate_user(
    username: str,
    password: str,
    *,
    remember_me: bool = False
) -> Optional[AuthToken]:
    """
    Authenticate a user with username and password.

    Args:
        username: User's username or email address
        password: User's password (will be hashed)
        remember_me: If True, token valid for 30 days instead of 1 day

    Returns:
        AuthToken object if authentication successful, None otherwise

    Raises:
        ValidationError: If username or password format invalid
        DatabaseError: If database connection fails

    Example:
        >>> token = authenticate_user("john@example.com", "secure_pass")
        >>> if token:
        ...     print(f"Authenticated: {token.user_id}")

    Security:
        - Password is hashed using bcrypt
        - Rate limiting applied (5 attempts per minute)
        - Failed attempts logged for security monitoring
    """
    # Implementation

#  FALSCH: Minimal Documentation
def auth(u, p):
    # Login user
    pass
```

---

##  Architektur-Prinzipien

Claude folgt diesen Prinzipien:

### 1. SOLID Principles

- **S**ingle Responsibility
- **O**pen/Closed
- **L**iskov Substitution
- **I**nterface Segregation
- **D**ependency Inversion

### 2. Clean Code

- Aussagekräftige Namen
- Kleine Funktionen (< 20 Zeilen)
- DRY (Don't Repeat Yourself)
- Kommentare nur wo nötig

### 3. Security by Design

- Input Validation
- Output Encoding
- Authentication & Authorization
- Secure Dependencies

---

##  Claude Projekt-Struktur Erweiterungen

Zusätzlich zur Standard-Struktur erstellt Claude:

```
projekt/
 src/
    core/              # Core Business Logic
    services/          # External Services
    middleware/        # Middleware Components
    validators/        # Input Validators
    errors/            # Custom Error Classes

 tests/
    unit/
       test_core.py
       test_services.py
    integration/
       test_api.py
    security/
        test_auth.py   # Security Tests!

 docs/
    API.md
    ARCHITECTURE.md
    SECURITY.md        # Security Documentation!
    TESTING.md         # Test Strategy

 .github/
     workflows/
        ci.yml
        security-scan.yml  # Security Scanning!
        dependency-check.yml
     SECURITY.md        # Security Policy
```

---

##  Security Checklist

Claude MUSS diese Punkte prüfen:

- [ ] Input Validation für alle User Inputs
- [ ] SQL Injection Prevention (Prepared Statements)
- [ ] XSS Prevention (Output Encoding)
- [ ] CSRF Protection
- [ ] Authentication & Authorization implementiert
- [ ] Secrets NICHT im Code (Environment Variables)
- [ ] Dependencies aktuell & sicher
- [ ] Error Messages enthalten keine sensitiven Daten
- [ ] Logging von Security Events
- [ ] Rate Limiting implementiert

---

##  Dependencies

Claude verwendet nur:
-  Aktuelle, gepflegte Libraries
-  Libraries mit gutem Security Track Record
-  Minimal Dependencies (weniger Angriffsfläche)

```python
#  RICHTIG: Pinned Versions
# requirements.txt
fastapi==0.104.1
pydantic==2.5.0
sqlalchemy==2.0.23
bcrypt==4.1.1
pytest==7.4.3

#  FALSCH: Unpinned Versions
# requirements.txt
fastapi
pydantic
sqlalchemy  # Could break with updates!
```

---

##  Test Coverage Requirements

Claude MUSS erreichen:
- **Minimum:** 80% Code Coverage
- **Ziel:** 90%+ Coverage
- **Critical Paths:** 100% Coverage

```bash
# Test Coverage prüfen
pytest --cov=src --cov-report=html --cov-report=term

# MINIMUM: 80% erreicht
Name                      Stmts   Miss  Cover
---------------------------------------------
src/__init__.py              12      0   100%
src/core/auth.py             45      3    93%
src/core/users.py            38      2    95%
src/services/email.py        22      6    73%  #  Zu niedrig!
---------------------------------------------
TOTAL                       117     11    91%  #  OK
```

---

##  Code Review Checkliste

Vor PR-Erstellung prüft Claude:

### Security:
- [ ] Alle Inputs validiert
- [ ] Keine SQL Injection möglich
- [ ] Keine XSS möglich
- [ ] Secrets in Environment Variables
- [ ] Dependencies sicher

### Code Quality:
- [ ] SOLID Principles befolgt
- [ ] Clean Code Prinzipien
- [ ] Aussagekräftige Namen
- [ ] Keine Code Duplications

### Testing:
- [ ] 80%+ Test Coverage
- [ ] Alle Edge Cases getestet
- [ ] Security Tests vorhanden
- [ ] Integration Tests vorhanden

### Documentation:
- [ ] README.md aktualisiert
- [ ] API Dokumentation vollständig
- [ ] Security Dokumentation vorhanden
- [ ] Inline Comments wo nötig

---

##  Kosten-Bewusstsein

Da Claude $20/mo kostet, wird er NUR für verwendet:
- Sicherheitskritische Features
- Architektur-Entscheidungen
- Komplexe Refactorings
- Quality-Critical Code

**NICHT für:**
- Einfache CRUD Operations
- Dokumentations-Updates
- Style Fixes
- Kleine Bugfixes

→ Diese gehen an Gemini (FREE) oder Copilot ($10)

---

**Claude steht für höchste Code-Qualität und Sicherheit!** 
