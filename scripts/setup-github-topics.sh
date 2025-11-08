#!/bin/bash
# Script to add GitHub repository topics/tags

REPO="LEEI1337/ai-dev-orchestrator"

# Add topics using GitHub CLI
gh repo edit $REPO --add-topic="ai"
gh repo edit $REPO --add-topic="artificial-intelligence"
gh repo edit $REPO --add-topic="claude"
gh repo edit $REPO --add-topic="gemini"
gh repo edit $REPO --add-topic="github-copilot"
gh repo edit $REPO --add-topic="automation"
gh repo edit $REPO --add-topic="orchestration"
gh repo edit $REPO --add-topic="mcp"
gh repo edit $REPO --add-topic="model-context-protocol"
gh repo edit $REPO --add-topic="developer-tools"
gh repo edit $REPO --add-topic="productivity"
gh repo edit $REPO --add-topic="cost-optimization"
gh repo edit $REPO --add-topic="multi-agent"
gh repo edit $REPO --add-topic="docker"
gh repo edit $REPO --add-topic="cli"

echo "✅ Topics added successfully!"
echo ""
echo "Verify at: https://github.com/$REPO"
