# 📁 Standard Projekt-Struktur - Für ALLE AI-Agenten

**Gültig für:** Claude, Gemini, Copilot, OpenHands
**Gilt für:** Layer 2 (AI CLIs), Layer 3 (Rover), Layer 4 (Lazy Bird)

---

## 🎯 Ziel

ALLE AI-Agenten müssen diese Standard-Struktur befolgen, unabhängig vom Layer!

---

## 📁 Universal Projekt-Struktur

```
projekt-name/
├── src/                    # SOURCE CODE (Hauptverzeichnis)
│   ├── __init__.py        # Python: Package Init
│   ├── index.ts           # TypeScript/JavaScript: Entry Point
│   ├── main.py            # Python: Entry Point
│   ├── components/        # React/Frontend: Komponenten
│   ├── lib/               # Gemeinsame Libraries
│   ├── utils/             # Utility Functions
│   └── types/             # TypeScript: Type Definitions
│
├── tests/                  # TESTS (PFLICHT!)
│   ├── __init__.py        # Python Package
│   ├── unit/              # Unit Tests
│   ├── integration/       # Integration Tests
│   └── e2e/               # End-to-End Tests
│
├── docs/                   # DOKUMENTATION
│   ├── API.md             # API Dokumentation
│   ├── ARCHITECTURE.md    # Architektur-Übersicht
│   └── USAGE.md           # Nutzungs-Anleitung
│
├── .github/                # GITHUB INTEGRATION
│   └── workflows/         # GitHub Actions
│       ├── ci.yml         # CI/CD Pipeline
│       └── tests.yml      # Test Workflow
│
├── config/                 # KONFIGURATION
│   ├── development.json   # Dev Config
│   ├── production.json    # Prod Config
│   └── test.json          # Test Config
│
├── scripts/                # UTILITY SCRIPTS
│   ├── setup.sh           # Setup Script
│   ├── deploy.sh          # Deployment Script
│   └── test.sh            # Test Runner
│
├── .gitignore              # Git Ignore Rules
├── README.md               # Projekt Dokumentation
├── CHANGELOG.md            # Änderungs-Historie
├── LICENSE                 # Lizenz (MIT)
│
# PROJEKT-TYP SPEZIFISCH:
│
├── requirements.txt        # Python: Dependencies
├── setup.py                # Python: Package Setup
├── pyproject.toml          # Python: Modern Config
│
├── package.json            # Node/TypeScript: Dependencies
├── tsconfig.json           # TypeScript: Compiler Config
├── jest.config.js          # JavaScript/TypeScript: Test Config
│
└── Cargo.toml              # Rust: Package Config
```

---

## 🚫 VERBOTEN - Was NICHT gemacht werden darf

### ❌ NIEMALS diese Anti-Patterns verwenden:

1. **Keine flachen Strukturen**
   ```
   ❌ FALSCH:
   projekt/
   ├── file1.py
   ├── file2.py
   ├── test_file1.py
   └── utils.py
   ```

2. **Kein Code im Root-Verzeichnis**
   ```
   ❌ FALSCH:
   projekt/
   ├── main.py          # Gehört nach src/
   ├── helper.py        # Gehört nach src/lib/
   └── constants.py     # Gehört nach src/
   ```

3. **Keine gemischten Test-Locations**
   ```
   ❌ FALSCH:
   projekt/
   ├── src/
   │   └── test_inline.py    # Tests gehören NICHT in src/
   └── tests/
       └── test_actual.py
   ```

4. **Keine unorganisierten Configs**
   ```
   ❌ FALSCH:
   projekt/
   ├── config.json
   ├── settings.yaml
   ├── .env              # OK im Root
   └── dev_config.json
   ```

---

## ✅ PFLICHT-ANFORDERUNGEN

### Für JEDEN Projekt-Typ:

1. **README.md** MUSS enthalten:
   - Project Titel & Beschreibung
   - Installation & Setup
   - Usage Examples
   - Test Commands
   - License Info

2. **tests/** MUSS existieren mit:
   - Mindestens 1 Test-Datei
   - Test für Hauptfunktionalität
   - Test Command dokumentiert in README

3. **.gitignore** MUSS enthalten:
   - Build Outputs (`dist/`, `build/`)
   - Dependencies (`node_modules/`, `venv/`)
   - IDE Files (`.vscode/`, `.idea/`)
   - OS Files (`.DS_Store`, `Thumbs.db`)

4. **src/** MUSS verwendet werden für:
   - ALLE Source Code Dateien
   - KEINE Tests
   - KEINE Configs (außer Code-Configs)

---

## 📋 Projekt-Typ Spezifische Strukturen

### Python Projekt

```
python-projekt/
├── src/
│   ├── __init__.py
│   ├── main.py            # Entry Point
│   ├── lib/
│   │   └── helpers.py
│   └── utils/
│       └── logging.py
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_helpers.py
├── requirements.txt        # PFLICHT
├── setup.py                # PFLICHT
├── pyproject.toml          # Empfohlen (modern)
└── .gitignore
```

**PFLICHT Dependencies:**
```txt
# requirements.txt
pytest>=7.0.0
ruff>=0.1.0              # Linting
black>=23.0.0            # Formatting
```

### TypeScript/Node.js Projekt

```
typescript-projekt/
├── src/
│   ├── index.ts           # Entry Point
│   ├── lib/
│   │   └── helpers.ts
│   └── types/
│       └── index.ts
├── tests/
│   └── index.test.ts
├── dist/                  # Build Output (in .gitignore)
├── package.json           # PFLICHT
├── tsconfig.json          # PFLICHT
├── jest.config.js         # Für Tests
└── .gitignore
```

**PFLICHT package.json Scripts:**
```json
{
  "scripts": {
    "build": "tsc",
    "test": "jest",
    "lint": "eslint src/**/*.ts",
    "start": "node dist/index.js"
  }
}
```

### React Projekt

```
react-projekt/
├── src/
│   ├── index.tsx          # Entry Point
│   ├── App.tsx            # Main Component
│   ├── components/
│   │   ├── Header.tsx
│   │   └── Footer.tsx
│   ├── hooks/
│   │   └── useAuth.ts
│   ├── lib/
│   │   └── api.ts
│   └── styles/
│       └── global.css
├── public/
│   └── index.html
├── tests/
│   └── App.test.tsx
├── package.json
├── tsconfig.json
└── .gitignore
```

---

## 🔧 Build & Test Commands

### Jedes Projekt MUSS diese Commands unterstützen:

```bash
# INSTALLATION
npm install          # Node/TypeScript/React
pip install -r requirements.txt  # Python

# TESTS AUSFÜHREN (PFLICHT!)
npm test             # Node/TypeScript/React
pytest tests/        # Python

# BUILD (wenn applicable)
npm run build        # Node/TypeScript/React
python -m build      # Python

# LINTING (PFLICHT!)
npm run lint         # Node/TypeScript/React
ruff check .         # Python
```

---

## 📝 Datei-Naming Conventions

### Python:
- Dateien: `snake_case.py`
- Klassen: `PascalCase`
- Funktionen: `snake_case`
- Konstanten: `UPPER_SNAKE_CASE`
- Tests: `test_*.py` oder `*_test.py`

### TypeScript/JavaScript:
- Dateien: `kebab-case.ts` oder `PascalCase.tsx` (React Components)
- Klassen/Interfaces: `PascalCase`
- Funktionen: `camelCase`
- Konstanten: `UPPER_SNAKE_CASE`
- Tests: `*.test.ts` oder `*.spec.ts`

---

## 🎯 Qualitäts-Checkliste

Jedes erstellte Projekt MUSS diese Punkte erfüllen:

- [ ] Korrekte Verzeichnis-Struktur (`src/`, `tests/`, `docs/`)
- [ ] README.md mit vollständiger Dokumentation
- [ ] Mindestens 1 funktionierender Test
- [ ] .gitignore mit allen relevanten Einträgen
- [ ] Kein Code im Root-Verzeichnis (außer Configs)
- [ ] Package Manager Config vorhanden (requirements.txt / package.json)
- [ ] Build Command funktioniert
- [ ] Test Command funktioniert
- [ ] Linting Command funktioniert
- [ ] CHANGELOG.md initialisiert
- [ ] LICENSE Datei vorhanden (MIT)

---

## 🤖 Agent-Spezifische Guidelines

Jeder AI-Agent hat zusätzlich seine eigenen Guidelines:

- **Claude:** [claude-guidelines.md](claude-guidelines.md)
- **Gemini:** [gemini-guidelines.md](gemini-guidelines.md)
- **Copilot:** [copilot-guidelines.md](copilot-guidelines.md)
- **OpenHands:** [openhands-guidelines.md](openhands-guidelines.md)

Diese Guidelines ergänzen (nicht ersetzen!) diese Standard-Struktur.

---

## 🚨 Bei Abweichungen

Wenn die Standard-Struktur NICHT passt (z.B. externes Tool-Format):

1. **Dokumentiere** in README.md WARUM abgewichen wird
2. **Behalte** so viel Standard-Struktur wie möglich
3. **Erstelle** `STRUCTURE.md` mit Erklärung der abweichenden Struktur

---

**Diese Struktur ist VERBINDLICH für alle Layers!** 🎯
