#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guideline Injector - Hierarchical guideline system for all layers

Loads and combines guidelines based on layer and agent.
"""

import sys
import io
from pathlib import Path
from typing import Optional

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class GuidelineInjector:
    """Manages hierarchical guideline loading and injection."""

    def __init__(self, guidelines_root: str = "../layers"):
        """Initialize guideline injector."""
        self.guidelines_root = Path(__file__).parent.parent / "layers"

    def get_guidelines_for_layer(
        self,
        layer: int,
        agent: Optional[str] = None
    ) -> str:
        """
        Load all guidelines for a specific layer.

        Args:
            layer: Layer number (0-4)
            agent: Optional agent name (claude, gemini, copilot)

        Returns:
            Concatenated guidelines with separators
        """
        if layer < 0 or layer > 4:
            raise ValueError(f"Invalid layer: {layer}. Must be 0-4.")

        guidelines = []

        # Layer 0 (always)
        guidelines.append(self._read_layer(0))

        # Layer 1+ (cumulative)
        for i in range(1, layer + 1):
            guidelines.append(self._read_layer(i))

        # Agent-specific (Layer 2 only)
        if layer >= 2 and agent:
            agent_guidelines = self._read_agent_specific(agent)
            if agent_guidelines:
                guidelines.append(agent_guidelines)

        return self._combine_guidelines(guidelines, layer, agent)

    def _read_layer(self, layer: int) -> str:
        """Read a layer guidelines file."""
        file_path = self.guidelines_root / f"LAYER-{layer}.md"

        if not file_path.exists():
            return f"# LAYER {layer} - Not Found\n\nGuidelines missing!"

        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _read_agent_specific(self, agent: str) -> Optional[str]:
        """Read agent-specific guidelines."""
        file_path = self.guidelines_root / f"LAYER-2-{agent.upper()}.md"

        if not file_path.exists():
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _combine_guidelines(
        self,
        guidelines: list,
        layer: int,
        agent: Optional[str]
    ) -> str:
        """Combine guidelines with headers."""
        agent_name = agent.upper() if agent else "GENERAL"

        header = f"""
# 🎯 ACTIVE GUIDELINES - Layer {layer} ({agent_name})

**Hierarchie:**
{"→ ".join([f"Layer {i}" for i in range(layer + 1)])}
{f"→ {agent_name}-Specific" if agent else ""}

**Vererbung:**
Spätere Layer erweitern frühere, überschreiben sie NICHT.
Bei Konflikt hat Layer {layer} Vorrang.

---
"""

        separator = "\n\n" + "=" * 60 + "\n\n"

        combined = header + separator.join(guidelines)

        footer = f"""

---

# ✅ Guidelines Geladen

**Layer:** {layer}
**Agent:** {agent_name}
**Geladene Dateien:** {layer + 1 + (1 if agent else 0)}

**WICHTIG:**
Diese Guidelines sind VERBINDLICH und müssen befolgt werden!
"""

        return combined + footer

    def inject_into_prompt(
        self,
        layer: int,
        agent: str,
        base_prompt: str
    ) -> str:
        """
        Inject guidelines into a base prompt.

        Args:
            layer: Layer number
            agent: Agent name
            base_prompt: Original system prompt

        Returns:
            Enhanced prompt with guidelines
        """
        guidelines = self.get_guidelines_for_layer(layer, agent)

        enhanced = f"""{base_prompt}

---

# HIERARCHICAL GUIDELINES

{guidelines}

---

Du arbeitest jetzt in **Layer {layer}** als **{agent.upper()}** Agent.
Befolge ALLE obigen Guidelines in der angegebenen Hierarchie!
"""

        return enhanced


def main():
    """Demo: Show guidelines for different layers."""
    injector = GuidelineInjector()

    print("=" * 60)
    print("🎯 Guideline Injector Demo")
    print("=" * 60)

    # Example 1: Direct Claude CLI usage (Layer 2)
    print("\n1️⃣ Claude Code CLI (Direct)")
    print("-" * 60)
    guidelines = injector.get_guidelines_for_layer(layer=2, agent="claude")
    print(f"Loaded {len(guidelines)} characters of guidelines")
    print(f"Includes: LAYER-0, LAYER-1, LAYER-2, LAYER-2-CLAUDE")

    # Example 2: Rover calling Gemini (Layer 3)
    print("\n2️⃣ Rover → Gemini")
    print("-" * 60)
    guidelines = injector.get_guidelines_for_layer(layer=3, agent="gemini")
    print(f"Loaded {len(guidelines)} characters of guidelines")
    print(f"Includes: LAYER-0, LAYER-1, LAYER-2, LAYER-2-GEMINI, LAYER-3")

    # Example 3: Lazy Bird → Rover → Copilot (Layer 4)
    print("\n3️⃣ Lazy Bird → Rover → Copilot")
    print("-" * 60)
    guidelines = injector.get_guidelines_for_layer(layer=4, agent="copilot")
    print(f"Loaded {len(guidelines)} characters of guidelines")
    print(f"Includes: LAYER-0, LAYER-1, LAYER-2, LAYER-2-COPILOT, LAYER-3, LAYER-4")

    # Example 4: Show first 500 chars
    print("\n📄 Preview (first 500 chars):")
    print("-" * 60)
    preview = injector.get_guidelines_for_layer(layer=2, agent="claude")
    print(preview[:500] + "...")

    print("\n" + "=" * 60)
    print("✅ Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
