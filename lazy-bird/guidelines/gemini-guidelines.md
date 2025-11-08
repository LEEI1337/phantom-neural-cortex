# 🤖 Gemini-Spezifische Guidelines

**Agent:** Gemini (Google)
**Use Case:** Dokumentation, Bulk Tasks, General Development
**Kosten:** KOSTENLOS (1000 requests/day)
**Stärken:** Schnell, Effizient, Große Datenmengen

---

## 🎯 Wann Gemini verwendet wird

Gemini ist der DEFAULT Agent und wird verwendet für:
- `documentation` - Dokumentations-Erstellung
- `bulk-refactor` - Große Refactorings
- `large-scale` - Features mit vielen Dateien
- Issues OHNE spezielle Labels (Fallback)

**Ziel:** 60-70% aller Tasks durch Gemini (KOSTENLOS!)

---

## 📋 Gemini-Spezifische Anforderungen

### 1. Effizienz & Geschwindigkeit

Gemini optimiert für:
- ✅ Schnelle Implementierung
- ✅ Wenig Iterations
- ✅ Pragmatische Lösungen
- ✅ DRY Code

```python
# ✅ RICHTIG: Effiziente Implementierung
def generate_api_docs(endpoints: List[Endpoint]) -> str:
    """Generate API documentation from endpoints."""
    docs = ["# API Documentation\n"]

    for endpoint in endpoints:
        docs.extend([
            f"## {endpoint.method} {endpoint.path}",
            endpoint.description,
            "",
            "**Parameters:**",
            *[f"- `{p.name}` ({p.type}): {p.description}"
              for p in endpoint.parameters],
            "",
            "**Response:**",
            f"```json\n{endpoint.response_example}\n```",
            "---",
            ""
        ])

    return "\n".join(docs)

# ❌ FALSCH: Over-engineered
class DocumentationGenerator:
    def __init__(self, config):
        self.config = config
        self.renderer = Renderer(config)
        self.formatter = Formatter(config)

    # 100 lines of abstraction for simple task...
```

### 2. Standard Patterns bevorzugen

Nutze bewährte Patterns statt Custom Solutions:

```typescript
// ✅ RICHTIG: Standard Express Pattern
app.get('/api/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  res.json(user);
});

// ❌ FALSCH: Custom abstraction
class EndpointHandler {
  constructor(private endpoint: Endpoint) {}
  async handle(req: Request, res: Response) {
    // Unnecessary abstraction
  }
}
```

### 3. Template-basierte Generierung

Für Bulk-Tasks verwende Templates:

```python
# ✅ RICHTIG: Template für CRUD
CRUD_TEMPLATE = '''
def create_{model}(data: dict) -> {Model}:
    """Create new {model}."""
    return {Model}.create(**data)

def get_{model}(id: int) -> Optional[{Model}]:
    """Get {model} by ID."""
    return {Model}.get_by_id(id)

def update_{model}(id: int, data: dict) -> {Model}:
    """Update {model}."""
    return {Model}.update(id, **data)

def delete_{model}(id: int) -> bool:
    """Delete {model}."""
    return {Model}.delete(id)
'''

# Generate for multiple models
for model in ['User', 'Product', 'Order']:
    code = CRUD_TEMPLATE.format(model=model, Model=model)
    # Write to file
```

### 4. Dokumentation First

Gemini's Stärke: EXZELLENTE Dokumentation!

```markdown
# ✅ RICHTIG: Comprehensive README

## Installation

\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Quick Start

\`\`\`python
from mylib import Client

client = Client(api_key="your_key")
result = client.fetch_data()
\`\`\`

## Examples

### Basic Usage
\`\`\`python
# Example 1: Simple query
data = client.query("SELECT * FROM users")
\`\`\`

### Advanced Usage
\`\`\`python
# Example 2: With filters
data = client.query("users", filters={"age__gt": 18})
\`\`\`

## API Reference

### Client
- `__init__(api_key: str)` - Initialize client
- `query(table: str, **kwargs)` - Query data

## Testing

\`\`\`bash
pytest tests/
\`\`\`

## License
MIT
```

---

## 📁 Gemini Projekt-Struktur

Gemini hält sich an die Standard-Struktur, OHNE zusätzliche Komplexität:

```
projekt/
├── src/
│   ├── main.py            # Simple entry point
│   ├── lib/               # Core functionality
│   └── utils/             # Utilities
│
├── tests/
│   ├── test_main.py       # Basic tests (60-70% coverage OK)
│   └── test_lib.py
│
├── docs/
│   ├── README.md          # Excellent documentation!
│   ├── API.md
│   └── EXAMPLES.md        # Lots of examples!
│
├── requirements.txt       # Minimal dependencies
└── .gitignore
```

**Fokus:** Einfachheit, Klarheit, Dokumentation

---

## 🚀 Bulk Operations Best Practices

### Dokumentation für 200 API Endpoints:

```python
def generate_all_api_docs(endpoints: List[Endpoint]) -> None:
    """Generate documentation for all API endpoints."""

    # Group by category
    by_category = {}
    for ep in endpoints:
        by_category.setdefault(ep.category, []).append(ep)

    # Generate per category
    for category, eps in by_category.items():
        filename = f"docs/api/{category.lower()}.md"
        content = generate_category_docs(category, eps)

        with open(filename, 'w') as f:
            f.write(content)

        print(f"✅ Generated: {filename} ({len(eps)} endpoints)")

# Generate for all
generate_all_api_docs(endpoints)

# Output:
# ✅ Generated: docs/api/users.md (45 endpoints)
# ✅ Generated: docs/api/products.md (67 endpoints)
# ✅ Generated: docs/api/orders.md (88 endpoints)
```

### Code-Generierung aus Schema:

```python
def generate_models_from_schema(schema: dict) -> None:
    """Generate SQLAlchemy models from JSON schema."""

    for table_name, fields in schema['tables'].items():
        model_code = generate_model(table_name, fields)

        filename = f"src/models/{table_name}.py"
        with open(filename, 'w') as f:
            f.write(model_code)

        print(f"✅ Generated: {filename}")

# One command generates all models!
```

---

## 🎯 Optimierung für Free Tier

Da Gemini FREE ist, optimieren wir anders:

### 1. Batch Processing

```python
# ✅ RICHTIG: Process in batches
def process_all_files(files: List[str]) -> None:
    """Process multiple files efficiently."""
    for i in range(0, len(files), 10):
        batch = files[i:i+10]
        process_batch(batch)

# ❌ FALSCH: Individual processing (slow)
for file in files:
    process_one_file(file)  # 1000 einzelne Calls
```

### 2. Template Reuse

Nutze Templates mehrfach:

```python
# Template einmal definieren
TEST_TEMPLATE = '''
def test_{function}():
    """Test {function} with valid input."""
    result = {function}({valid_input})
    assert result == {expected}

def test_{function}_invalid():
    """Test {function} with invalid input."""
    with pytest.raises({error_type}):
        {function}({invalid_input})
'''

# Für 100 Functions generieren
for func in functions:
    generate_test(func, TEST_TEMPLATE)
```

### 3. Smart Caching

```python
# ✅ RICHTIG: Cache results
cache = {}

def get_or_generate(key: str) -> str:
    if key in cache:
        return cache[key]

    result = generate_expensive_operation(key)
    cache[key] = result
    return result
```

---

## 📊 Test Coverage Expectations

Gemini Ziel: **60-70% Coverage**

- Unit Tests für Haupt-Funktionen
- Happy Path Tests
- Basic Error Handling
- KEINE exhaustive Edge Cases (das macht Claude)

```python
# ✅ RICHTIG: Pragmatic Testing
def test_create_user():
    """Test user creation."""
    user = create_user("john@example.com", "password123")
    assert user.email == "john@example.com"

def test_create_user_invalid_email():
    """Test with invalid email."""
    with pytest.raises(ValueError):
        create_user("not-an-email", "password123")

# Das reicht für Gemini! (keine 20 Edge Cases)
```

---

## 📚 Dokumentations-Standards

Gemini's Superkraft: BESTE Dokumentation!

### README.md Struktur:

```markdown
# Project Name

One-line description.

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

\`\`\`bash
installation command
\`\`\`

## Quick Start

\`\`\`python
simple example
\`\`\`

## Usage

### Example 1
\`\`\`python
code example
\`\`\`

### Example 2
\`\`\`python
another example
\`\`\`

## API Reference

Brief API docs or link to full docs.

## Configuration

Environment variables and config options.

## Testing

\`\`\`bash
test command
\`\`\`

## Contributing

How to contribute.

## License

MIT
```

### Code Comments:

```python
# ✅ RICHTIG: Clear, concise comments
def calculate_discount(price: float, code: str) -> float:
    """
    Calculate discounted price.

    Args:
        price: Original price
        code: Discount code (e.g., "SUMMER20")

    Returns:
        Discounted price

    Example:
        >>> calculate_discount(100, "SUMMER20")
        80.0
    """
    # Get discount percentage from code
    discount_pct = DISCOUNT_CODES.get(code, 0)

    # Apply discount
    return price * (1 - discount_pct / 100)
```

---

## 💡 Pragmatic Patterns

### 1. KISS (Keep It Simple, Stupid)

```python
# ✅ RICHTIG: Simple & Clear
def format_date(date):
    return date.strftime("%Y-%m-%d")

# ❌ FALSCH: Over-engineered
class DateFormatter:
    def __init__(self, format_string="%Y-%m-%d"):
        self.format = format_string

    def format(self, date):
        return date.strftime(self.format)

formatter = DateFormatter()
# Unnecessary complexity!
```

### 2. Prefer Built-ins

```python
# ✅ RICHTIG: Use standard library
from collections import Counter

def count_items(items):
    return Counter(items)

# ❌ FALSCH: Reinvent the wheel
def count_items(items):
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts
```

---

## 🎯 Gemini Checkliste

- [ ] Code ist einfach & klar
- [ ] Standard Patterns verwendet
- [ ] Excellent Dokumentation (README, API docs, Examples)
- [ ] 60-70% Test Coverage
- [ ] Minimale Dependencies
- [ ] DRY Prinzipien befolgt
- [ ] No over-engineering
- [ ] Bulk operations optimiert (wenn applicable)

---

## 💰 Cost Efficiency

Gemini ist FREE → Nutzen wir maximal aus!

**Perfekt für:**
- ✅ Dokumentation (Unlimitiert!)
- ✅ Code Generation (Templates)
- ✅ Bulk Refactorings
- ✅ Standard CRUD Operations
- ✅ API Endpoint Creation
- ✅ Test Generation

**Sparen wir Claude ($20) für:**
- Sicherheit
- Komplexe Architektur
- Critical Business Logic

---

**Gemini = Geschwindigkeit + Effizienz + FREE!** 🚀
