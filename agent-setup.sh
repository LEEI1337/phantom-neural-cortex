#!/usr/bin/env bash
# agent-setup.sh — Interactive setup for a new Phantom Agent
# Creates AGENT.yaml from template and prepares deployment
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$SCRIPT_DIR/config/templates"

echo "============================================"
echo "  Phantom Agent System — Agent Setup"
echo "============================================"
echo ""

# 1. Agent Name
read -rp "Agent Name (e.g., lisa01): " AGENT_NAME
if [[ -z "$AGENT_NAME" ]]; then
    echo "Error: Agent name is required."
    exit 1
fi

# 2. Role
echo ""
echo "Available roles:"
echo "  1) Infrastructure Specialist (Docker, Server, Monitoring)"
echo "  2) Web & DevOps Specialist (Web, API, CI/CD, Git)"
echo "  3) Research Specialist (Browser, Research, Analysis)"
echo "  4) Custom"
read -rp "Select role [1-4]: " ROLE_CHOICE

case "$ROLE_CHOICE" in
    1) ROLE="Infrastructure Specialist"; TEMPLATE="lisa01.yaml" ;;
    2) ROLE="Web & DevOps Specialist"; TEMPLATE="jim01.yaml" ;;
    3) ROLE="Research Specialist"; TEMPLATE="john01.yaml" ;;
    4) read -rp "Custom role: " ROLE; TEMPLATE="lisa01.yaml" ;;
    *) echo "Invalid choice."; exit 1 ;;
esac

# 3. LLM Configuration
echo ""
echo "LLM Configuration:"
echo "  Planner (Cloud): opus-4.6 (default)"
echo "  Executor (Local): mistral-small3.2 (default)"
read -rp "Use defaults? [Y/n]: " LLM_DEFAULT
LLM_DEFAULT="${LLM_DEFAULT:-Y}"

PLANNER="opus-4.6"
EXECUTOR="mistral-small3.2"
if [[ "${LLM_DEFAULT,,}" == "n" ]]; then
    read -rp "Planner model: " PLANNER
    read -rp "Executor model: " EXECUTOR
fi

# 4. Mattermost Token
echo ""
read -rp "Mattermost Vault Path (e.g., ${AGENT_NAME}/mattermost/MM_TOKEN): " MM_VAULT
MM_VAULT="${MM_VAULT:-${AGENT_NAME}/mattermost/MM_TOKEN}"

read -rp "Home Channel ID: " HOME_CHANNEL

# 5. Killswitch owners
echo ""
read -rp "Killswitch authorized users (comma-separated, default: joe): " KS_OWNERS
KS_OWNERS="${KS_OWNERS:-joe}"

# 6. Create config
AGENT_DIR="$SCRIPT_DIR/agents/$AGENT_NAME"
mkdir -p "$AGENT_DIR"

AGENT_YAML="$AGENT_DIR/AGENT.yaml"

# Use template as base and customize
if [[ -f "$TEMPLATES_DIR/$TEMPLATE" ]]; then
    cp "$TEMPLATES_DIR/$TEMPLATE" "$AGENT_YAML"
else
    cp "$TEMPLATES_DIR/lisa01.yaml" "$AGENT_YAML"
fi

# Replace values using sed
sed -i "s/name: \".*\"/name: \"$AGENT_NAME\"/" "$AGENT_YAML"
sed -i "s/role: \".*\"/role: \"$ROLE\"/" "$AGENT_YAML"
sed -i "s/planner: \".*\"/planner: \"$PLANNER\"/" "$AGENT_YAML"
sed -i "s/executor: \".*\"/executor: \"$EXECUTOR\"/" "$AGENT_YAML"
sed -i "s|token_vault_path: \".*\"|token_vault_path: \"$MM_VAULT\"|" "$AGENT_YAML"
sed -i "s/home_channel: \".*\"/home_channel: \"$HOME_CHANNEL\"/" "$AGENT_YAML"

# Create rules and skills directories
mkdir -p "$AGENT_DIR/rules" "$AGENT_DIR/skills"

echo ""
echo "============================================"
echo "  Agent '$AGENT_NAME' created successfully!"
echo "============================================"
echo ""
echo "Config:  $AGENT_YAML"
echo "Rules:   $AGENT_DIR/rules/"
echo "Skills:  $AGENT_DIR/skills/"
echo ""
echo "Next steps:"
echo "  1. Review config:    cat $AGENT_YAML"
echo "  2. Set MM token:     python vault.py set $AGENT_NAME mattermost MM_TOKEN <token>"
echo "  3. Start agent:      python run_agent.py --config $AGENT_YAML"
echo "  4. Or via Docker:    docker compose up -d pnc-gateway"
echo ""
