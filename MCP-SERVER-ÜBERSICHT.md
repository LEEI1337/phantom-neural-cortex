# MCP Server Komplett-Übersicht

**Stand:** 2025-11-08
**Total:** 18 MCP-Server (davon 13 kostenlos & lokal)

---

## 🆓 Kostenlose & Lokale Server (13)

### Core Infrastruktur
1. **filesystem** - Dateisystem-Zugriff
2. **memory** - Persistenter Wissens-Graph
3. **sequential-thinking** - Reflektives Reasoning
4. **brave-search** - Web-Suche (2000 req/Monat gratis)

### Development Tools
5. **playwright** - Browser-Automatisierung (Chromium)
6. **browser-tools** - Browser Control Extension
7. **studentofjs** - Testing Framework (Jest/Cypress)
8. **mcp-inspector** - Live Debugging & Monitoring

### Neu hinzugefügt (5)
9. **docs** - Durchsuchbare Dokumentation (1000+ Frameworks)
10. **postmancer** - API Testing (Postman Alternative)
11. **time** - Timezone & Datum-Handling
12. **sqlite** - Lokale SQLite Datenbank
13. **postgres** - PostgreSQL Integration (optional, needs DB)

---

## 💰 API-basierte Server (5)

14. **github** - GitHub Integration
    - Kosten: $0 (mit GitHub Account)
    - Token: GITHUB_TOKEN

15. **gemini-cli** - Google Gemini AI
    - Kosten: $0 (Free Tier: 100 req/Tag)
    - Token: GOOGLE_API_KEY

16. **perplexity** - Perplexity AI Search
    - Kosten: ~$5-10/Monat
    - Token: PERPLEXITY_API_KEY

17. **copilot-cli** - GitHub Copilot
    - Kosten: Included in Copilot Subscription
    - Auth: Copilot Account

18. **Rover** - Multi-Agent Manager
    - Kosten: $0 (Open Source)
    - Benötigt: Docker Desktop

---

## 📊 Kategorien-Übersicht

| Kategorie | Server | Kosten |
|-----------|--------|--------|
| **Dateisystem** | filesystem | $0 |
| **Memory** | memory | $0 |
| **Reasoning** | sequential-thinking | $0 |
| **Web Search** | brave-search, perplexity | $0 + $5-10 |
| **Documentation** | docs | $0 |
| **API Testing** | postmancer | $0 |
| **Browser** | playwright, browser-tools | $0 |
| **Testing** | studentofjs | $0 |
| **Debugging** | mcp-inspector | $0 |
| **Database** | sqlite, postgres | $0 |
| **Time** | time | $0 |
| **Version Control** | github | $0 |
| **AI Assistants** | gemini-cli, copilot-cli, perplexity | $5-10 |
| **Orchestration** | Rover | $0 |

---

## 🎯 Use Cases

### 1. Code-Entwicklung
- **copilot-cli** - Code-Vorschläge
- **docs** - Framework-Dokumentation
- **github** - Repo-Integration
- **sequential-thinking** - Komplexe Logik

### 2. Testing
- **studentofjs** - Unit/E2E Tests
- **playwright** - Browser-Tests
- **postmancer** - API Testing

### 3. Recherche
- **brave-search** - Schnelle Web-Suche
- **perplexity** - Deep Research
- **docs** - Technische Dokumentation

### 4. Datenbank
- **sqlite** - Lokale Persistence
- **postgres** - Production DB Access
- **memory** - Kontext-Speicher

### 5. Debugging
- **mcp-inspector** - Server Debugging
- **browser-tools** - Browser DevTools
- **time** - Timezone-Probleme

---

## ⚡ Quick Start Commands

### Docs Server nutzen
```bash
# In Claude:
"Suche React 18 useEffect Dokumentation"
"Zeige Next.js 14 App Router Docs"
```

### API Testing
```bash
# In Claude:
"Teste GET https://api.github.com/users/octocat"
"POST Request an https://api.example.com mit JSON {name: 'test'}"
```

### Zeit-Handling
```bash
# In Claude:
"Aktuelle Zeit in Tokyo?"
"Konvertiere 14:00 UTC zu Berlin Zeit"
```

### SQLite
```bash
# In Claude:
"Erstelle Tabelle 'users' mit id, name, email"
"SELECT * FROM users WHERE email LIKE '%@gmail.com'"
```

---

## 🔧 Konfiguration

### Alle Server in .mcp.json
```json
{
  "mcpServers": {
    "docs": {...},
    "postmancer": {...},
    "time": {...},
    "sqlite": {...},
    "postgres": {...}
  }
}
```

### Environment Variables (.env)
```env
GITHUB_TOKEN=ghp_xxx
GOOGLE_API_KEY=AIza_xxx
PERPLEXITY_API_KEY=pplx_xxx
BRAVE_API_KEY=BSA_xxx
DATABASE_URL=postgresql://... (optional)
```

---

## 💡 Pro-Tips

### 1. Kosten sparen
- Brave für einfache Suchen
- Perplexity nur für komplexe Research
- Gemini Free Tier nutzen (100/Tag)

### 2. Performance
- SQLite für lokale Daten (schneller als Remote DB)
- Docs Server cached Dokumentation lokal
- Postmancer speichert Collections

### 3. Workflows
- **Copilot** für Code-Generierung
- **Docs** für Syntax-Lookup
- **Postmancer** für API-Integration-Tests
- **Playwright** für E2E-Tests

---

## 📈 Statistik

**Total Server:** 18
**Kostenlos:** 13 (72%)
**API-basiert:** 5 (28%)
**Monatliche Kosten:** ~$5-10 (nur Perplexity)

**Neue Features:**
- ✅ Dokumentations-Suche
- ✅ API Testing
- ✅ Timezone-Handling
- ✅ Lokale Datenbank
- ✅ PostgreSQL Support

---

**Alles bereit für professionelle Entwicklung! 🚀**
