#!/bin/bash
# OpenHands Setup Script
# Runs every time OpenHands begins working with this repository

set -e  # Exit on error

echo "🚀 OpenHands Setup: Starting repository initialization..."

# 1. Environment Setup
echo "📦 Setting up environment..."
if [ -f ".env" ]; then
    echo "✅ .env file found"
    # Load environment variables (don't expose secrets)
    export $(cat .env | grep -v '^#' | grep -v '^$' | xargs)
else
    echo "⚠️  Warning: .env file not found"
fi

# 2. Node.js Dependencies
if [ -f "package.json" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm ci --silent || npm install --silent
    echo "✅ Node.js dependencies installed"
fi

# 3. Python Dependencies (if needed)
if [ -f "requirements.txt" ]; then
    echo "🐍 Installing Python dependencies..."
    pip install -r requirements.txt --quiet
    echo "✅ Python dependencies installed"
fi

# 4. Verify Critical Tools
echo "🔧 Verifying tools..."

# Check Node.js
if command -v node &> /dev/null; then
    echo "✅ Node.js $(node --version)"
else
    echo "❌ Node.js not found"
fi

# Check npm
if command -v npm &> /dev/null; then
    echo "✅ npm $(npm --version)"
else
    echo "❌ npm not found"
fi

# Check git
if command -v git &> /dev/null; then
    echo "✅ Git $(git --version | head -n1)"
else
    echo "❌ Git not found"
fi

# 5. MCP Server Pre-check (optional)
echo "🔌 Checking MCP servers availability..."
if [ -f ".mcp.json" ]; then
    echo "✅ MCP config found (.mcp.json)"
    # Count configured servers
    SERVER_COUNT=$(cat .mcp.json | grep -o '"type": "stdio"' | wc -l)
    echo "   → $SERVER_COUNT MCP servers configured"
else
    echo "⚠️  No MCP config found"
fi

# 6. Setup Memory Bank (if not exists)
if [ ! -d "memory-bank" ]; then
    echo "🧠 Creating memory-bank directory..."
    mkdir -p memory-bank
    echo "✅ Memory bank created"
fi

# 7. Setup Test Environment
if [ -f "playwright.config.ts" ] || [ -f "playwright.config.js" ]; then
    echo "🎭 Playwright detected - installing browsers..."
    npx playwright install --with-deps chromium --quiet || true
    echo "✅ Playwright browsers ready"
fi

# 8. Claude Code Skills Check
if [ -d ".claude/skills" ]; then
    SKILLS_COUNT=$(find .claude/skills -name "SKILL.md" | wc -l)
    echo "✅ Claude Code: $SKILLS_COUNT skills available"
fi

# 9. Custom Agents Check
if [ -f "AGENTS.md" ]; then
    AGENTS_COUNT=$(grep -c "^### " AGENTS.md || echo "0")
    echo "✅ Custom Agents: $AGENTS_COUNT agents defined"
fi

# 10. Verify GitHub Token (for github MCP server)
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  Warning: GITHUB_TOKEN not set (GitHub MCP may not work)"
else
    echo "✅ GITHUB_TOKEN configured"
fi

# 11. Create temp directories if needed
mkdir -p .temp
mkdir -p logs

echo ""
echo "✅ OpenHands Setup Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Repository: $(basename $(pwd))"
echo "Node Version: $(node --version 2>/dev/null || echo 'N/A')"
echo "MCP Servers: $SERVER_COUNT configured"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
