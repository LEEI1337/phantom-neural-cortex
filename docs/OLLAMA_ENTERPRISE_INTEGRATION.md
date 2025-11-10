# Ollama Enterprise Integration - Local AI with MCP

**Version:** 1.0.0
**Status:** ENTERPRISE GRADE - NO COMPROMISES

Complete Enterprise-Grade Ollama integration with MCP servers, skills, subagents, and Claude Code-like CLI experience.

---

## Why Ollama?

### Benefits

```
✅ 100% Local - Complete data privacy
✅ Zero API Costs - Run unlimited tasks
✅ No Rate Limits - Full control
✅ Offline Capable - Work anywhere
✅ Custom Models - Fine-tune freely
✅ Enterprise Control - Your infrastructure
```

### Use Cases

- **Security-Critical Projects** - Keep code completely local
- **Cost Optimization** - Zero inference costs
- **High-Volume Workloads** - No rate limits
- **Offline Development** - No internet required
- **Custom Fine-Tuning** - Train domain-specific models

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    PHANTOM NEURAL CORTEX                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────┐       │
│  │              ORCHESTRATION LAYER                      │       │
│  │  (Selects: Claude, Gemini, Copilot, or Ollama)       │       │
│  └──────────────────────────────────────────────────────┘       │
│                           ↓                                       │
│  ┌──────────────────────────────────────────────────────┐       │
│  │              OLLAMA INTEGRATION                       │       │
│  ├──────────────────────────────────────────────────────┤       │
│  │                                                        │       │
│  │  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐ │       │
│  │  │  ollama-code│  │   ollmcp     │  │ MCP Servers │ │       │
│  │  │  (CLI Tool) │→ │  (MCP Client)│→ │  (Skills)   │ │       │
│  │  └─────────────┘  └──────────────┘  └─────────────┘ │       │
│  │        ↓                  ↓                  ↓        │       │
│  │  ┌────────────────────────────────────────────────┐ │       │
│  │  │          OLLAMA ENGINE (Local)                  │ │       │
│  │  │  Models: qwen2.5-coder, deepseek-coder, etc.  │ │       │
│  │  └────────────────────────────────────────────────┘ │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                   │
│  ┌──────────────────────────────────────────────────────┐       │
│  │              GUIDELINE LAYER-2                        │       │
│  │  Optimized prompts for Ollama models                 │       │
│  └──────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Selection

### Best CLI Tools for Ollama

#### 1. **ollama-code** (Primary Choice)

**GitHub:** https://github.com/Foadsf/ollama-code

**Features:**
- Terminal-based AI coding assistant
- FLOSS (Free/Libre Open Source Software)
- Mimics Claude Code's REPL-style experience
- Lightweight wrapper around Ollama
- Local execution only

**Why Choose:**
- ✅ Most similar to Claude Code
- ✅ Actively maintained (2025)
- ✅ Simple, focused on coding tasks
- ✅ Works out-of-the-box

#### 2. **OpenCode** (Alternative)

**GitHub:** https://github.com/xichen1997/opencode

**Features:**
- Open-source Claude Code alternative
- Provider-agnostic (Ollama, OpenAI, etc.)
- Full Ollama integration
- Growing community

**Why Choose:**
- ✅ More flexible (multiple providers)
- ✅ Active community
- ✅ Extensible architecture

#### 3. **ollmcp** (MCP Client)

**GitHub:** https://github.com/jonigl/mcp-client-for-ollama

**Features:**
- Text-based UI (TUI) for MCP servers
- Multi-server support
- Dynamic model switching
- Streaming responses
- Tool management
- Human-in-the-loop
- Thinking mode
- Full model parameter configuration
- Custom system prompts
- Saved preferences

**Why Choose:**
- ✅ Enterprise-grade MCP support
- ✅ Skills and tool integration
- ✅ Subagent coordination
- ✅ Built for developers

#### 4. **Aider** (Git-Aware Assistant)

**GitHub:** https://github.com/paul-gauthier/aider

**Features:**
- Terminal-first pair programmer
- Git-aware (commits, diffs)
- Supports local & cloud models
- Refactoring workflows

**Why Choose:**
- ✅ Best for Git workflows
- ✅ Excellent code editing
- ✅ Works with any model

---

## Recommended Stack

### Enterprise Configuration

```yaml
# Ollama Integration Stack

Primary CLI:
  - ollama-code (Claude Code experience)
  OR
  - OpenCode (multi-provider flexibility)

MCP Integration:
  - ollmcp (skills, tools, subagents)

Git Integration:
  - Aider (optional, for Git-heavy workflows)

Model:
  - qwen2.5-coder:32b (best coding model)
  - deepseek-coder-v2:236b (enterprise)
  - codellama:70b (alternative)
```

---

## Installation & Setup

### Step 1: Install Ollama

```bash
# Windows (PowerShell)
winget install Ollama.Ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# macOS
brew install ollama

# Verify installation
ollama --version
```

### Step 2: Pull Recommended Models

```bash
# Best coding model (32B, runs on 24GB VRAM)
ollama pull qwen2.5-coder:32b

# Alternative: Smaller model (7B, runs on 8GB VRAM)
ollama pull qwen2.5-coder:7b

# Alternative: DeepSeek Coder (best for complex tasks)
ollama pull deepseek-coder-v2:16b

# Alternative: CodeLlama (solid general purpose)
ollama pull codellama:34b

# Alternative: Phi-3.5 (tiny but capable, 3.8B)
ollama pull phi3.5:latest
```

### Step 3: Install ollama-code

```bash
# Clone repository
git clone https://github.com/Foadsf/ollama-code.git
cd ollama-code

# Install dependencies (Node.js required)
npm install

# Make globally available
npm link

# Test installation
ollama-code --version
```

### Step 4: Install ollmcp (MCP Client)

```bash
# Using pipx (recommended)
pipx install ollmcp

# Or using pip
pip install ollmcp

# Verify installation
ollmcp --version
```

### Step 5: Install Aider (Optional)

```bash
# Using pipx
pipx install aider-chat

# Or using pip
pip install aider-chat

# Verify installation
aider --version
```

---

## Configuration

### Ollama Configuration

```bash
# ~/.ollama/config.json
{
  "models_dir": "/path/to/models",
  "gpu_layers": -1,
  "context_length": 32768,
  "num_threads": 8,
  "num_gpu": 1,
  "host": "127.0.0.1:11434"
}
```

### ollama-code Configuration

```bash
# ~/.ollama-code/config.json
{
  "model": "qwen2.5-coder:32b",
  "temperature": 0.7,
  "max_tokens": 4096,
  "system_prompt": "You are an expert software engineer assistant.",
  "stream": true,
  "auto_commit": false,
  "git_integration": true
}
```

### ollmcp Configuration

```bash
# ~/.ollmcp/config.yaml
default_model: qwen2.5-coder:32b
ollama_host: http://localhost:11434

mcp_servers:
  - name: filesystem
    command: mcp-server-filesystem
    args: ["/path/to/project"]

  - name: git
    command: mcp-server-git
    args: ["/path/to/repo"]

  - name: search
    command: mcp-server-brave-search
    env:
      BRAVE_API_KEY: your-key-here

thinking_mode: true
human_in_the_loop: true
stream_responses: true
```

---

## Usage Examples

### Example 1: Basic Coding with ollama-code

```bash
# Start interactive session
ollama-code

# In session:
> Write a Python function to calculate fibonacci numbers

# With context
ollama-code --files src/**/*.py --prompt "Refactor authentication logic"

# With specific model
ollama-code --model deepseek-coder-v2:16b --prompt "Add error handling"
```

### Example 2: MCP Skills with ollmcp

```bash
# Start ollmcp with MCP servers
ollmcp

# In session:
> Use filesystem tool to read main.py
> Search codebase for authentication logic
> Use git tool to show recent commits
```

### Example 3: Git Workflows with Aider

```bash
# Start aider in project
cd /path/to/project
aider --model ollama/qwen2.5-coder:32b

# In session:
> Refactor user authentication to use JWT
> Add comprehensive error handling
> /commit
```

---

## Integration with Orchestrator

### Ollama Agent Wrapper

```python
# dashboard/backend/orchestration/ollama_agent.py

import httpx
import asyncio
from typing import Optional, Dict, List
import subprocess
import logging

logger = logging.getLogger(__name__)


class OllamaAgent:
    """
    Enterprise-grade Ollama agent wrapper.

    Supports:
    - ollama-code CLI
    - OpenCode CLI
    - Direct Ollama API
    - MCP integration via ollmcp
    """

    def __init__(
        self,
        model: str = "qwen2.5-coder:32b",
        cli_tool: str = "ollama-code",  # or "opencode" or "aider"
        ollama_host: str = "http://localhost:11434",
        use_mcp: bool = True,
        mcp_servers: Optional[List[str]] = None
    ):
        self.model = model
        self.cli_tool = cli_tool
        self.ollama_host = ollama_host
        self.use_mcp = use_mcp
        self.mcp_servers = mcp_servers or ["filesystem", "git"]

    async def execute(
        self,
        prompt: str,
        context_files: Optional[List[str]] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> Dict:
        """
        Execute task with Ollama agent.

        Args:
            prompt: Task prompt
            context_files: Optional list of file paths for context
            system_prompt: Optional system prompt override
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Dict with content, tokens, cost (0.0 for local)
        """
        if self.cli_tool == "ollama-code":
            return await self._execute_ollama_code(
                prompt, context_files, system_prompt, temperature, max_tokens
            )
        elif self.cli_tool == "opencode":
            return await self._execute_opencode(
                prompt, context_files, system_prompt, temperature, max_tokens
            )
        elif self.cli_tool == "aider":
            return await self._execute_aider(
                prompt, context_files, system_prompt
            )
        else:
            # Fallback: Direct Ollama API
            return await self._execute_ollama_api(
                prompt, context_files, system_prompt, temperature, max_tokens
            )

    async def _execute_ollama_code(
        self,
        prompt: str,
        context_files: Optional[List[str]],
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> Dict:
        """Execute using ollama-code CLI."""
        cmd = ["ollama-code", "--model", self.model]

        # Add context files
        if context_files:
            cmd.extend(["--files", ",".join(context_files)])

        # Add system prompt
        if system_prompt:
            cmd.extend(["--system", system_prompt])

        # Add temperature
        cmd.extend(["--temperature", str(temperature)])

        # Add prompt
        cmd.extend(["--prompt", prompt])

        # Execute
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                raise Exception(f"ollama-code failed: {stderr.decode()}")

            output = stdout.decode()

            return {
                "content": output,
                "tokens": len(output.split()),  # Rough estimate
                "cost": 0.0,  # Local is free!
                "model": self.model,
                "provider": "ollama"
            }

        except Exception as e:
            logger.error(f"ollama-code execution failed: {e}")
            raise

    async def _execute_opencode(
        self,
        prompt: str,
        context_files: Optional[List[str]],
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> Dict:
        """Execute using OpenCode CLI."""
        # Similar to ollama-code
        cmd = ["opencode", "--provider", "ollama", "--model", self.model]

        if context_files:
            cmd.extend(["--files"] + context_files)

        if system_prompt:
            cmd.extend(["--system-prompt", system_prompt])

        cmd.extend(["--prompt", prompt])

        # Execute subprocess
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise Exception(f"OpenCode failed: {stderr.decode()}")

        return {
            "content": stdout.decode(),
            "tokens": len(stdout.decode().split()),
            "cost": 0.0,
            "model": self.model,
            "provider": "ollama"
        }

    async def _execute_aider(
        self,
        prompt: str,
        context_files: Optional[List[str]],
        system_prompt: Optional[str]
    ) -> Dict:
        """Execute using Aider CLI."""
        cmd = [
            "aider",
            "--model", f"ollama/{self.model}",
            "--yes",  # Auto-confirm
            "--message", prompt
        ]

        if context_files:
            cmd.extend(context_files)

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=context_files[0].rsplit('/', 1)[0] if context_files else "."
        )

        stdout, stderr = await process.communicate()

        return {
            "content": stdout.decode(),
            "tokens": len(stdout.decode().split()),
            "cost": 0.0,
            "model": self.model,
            "provider": "ollama"
        }

    async def _execute_ollama_api(
        self,
        prompt: str,
        context_files: Optional[List[str]],
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> Dict:
        """Execute using direct Ollama API."""
        # Build messages
        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        # Add context files
        if context_files:
            context = await self._read_context_files(context_files)
            messages.append({
                "role": "system",
                "content": f"Context files:\n\n{context}"
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        # Call Ollama API
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                f"{self.ollama_host}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                }
            )

            if response.status_code != 200:
                raise Exception(f"Ollama API failed: {response.text}")

            result = response.json()

            return {
                "content": result["message"]["content"],
                "tokens": result.get("eval_count", 0) + result.get("prompt_eval_count", 0),
                "cost": 0.0,
                "model": self.model,
                "provider": "ollama"
            }

    async def _read_context_files(self, file_paths: List[str]) -> str:
        """Read context files."""
        context_parts = []

        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    context_parts.append(f"File: {file_path}\n```\n{content}\n```\n")
            except Exception as e:
                logger.warning(f"Failed to read {file_path}: {e}")

        return "\n\n".join(context_parts)

    async def check_health(self) -> Dict:
        """Check Ollama health."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.ollama_host}/api/tags")

                if response.status_code == 200:
                    models = response.json().get("models", [])
                    model_names = [m["name"] for m in models]

                    return {
                        "status": "healthy",
                        "available_models": model_names,
                        "model_loaded": self.model in model_names
                    }
                else:
                    return {"status": "unhealthy", "error": "API not responding"}

        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
```

---

## MCP Server Integration

### Filesystem MCP Server

```bash
# Install
npm install -g @modelcontextprotocol/server-filesystem

# Run
mcp-server-filesystem /path/to/project
```

### Git MCP Server

```bash
# Install
npm install -g @modelcontextprotocol/server-git

# Run
mcp-server-git /path/to/repo
```

### Custom MCP Server

```python
# custom_mcp_server.py

from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("custom-skills")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="analyze_code",
            description="Analyze code quality and suggest improvements",
            input_schema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "check_type": {"type": "string", "enum": ["security", "performance", "style"]}
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "analyze_code":
        # Implement code analysis
        return [TextContent(
            type="text",
            text=f"Analysis complete for {arguments['file_path']}"
        )]

if __name__ == "__main__":
    server.run()
```

---

## Model Recommendations

### By Use Case

**Coding Tasks (Primary):**
- `qwen2.5-coder:32b` - Best overall (24GB VRAM)
- `deepseek-coder-v2:16b` - Complex reasoning (16GB VRAM)
- `qwen2.5-coder:7b` - Resource-constrained (8GB VRAM)

**General Purpose:**
- `llama3.3:70b` - Best general model
- `mistral-nemo:12b` - Good balance

**Tiny/Fast:**
- `phi3.5:3.8b` - Surprisingly capable
- `gemma2:9b` - Google's efficient model

**Enterprise/Maximum Quality:**
- `deepseek-coder-v2:236b` - Largest coding model (requires 8x A100)
- `qwen2.5:72b` - Excellent reasoning

### Performance Comparison

```
Model               | Size | VRAM  | Speed | Quality | Use Case
--------------------|------|-------|-------|---------|------------------
qwen2.5-coder:32b  | 32B  | 24GB  | ⚡⚡  | ⭐⭐⭐⭐⭐ | Primary choice
deepseek-coder:16b | 16B  | 16GB  | ⚡⚡⚡ | ⭐⭐⭐⭐  | Complex tasks
qwen2.5-coder:7b   | 7B   | 8GB   | ⚡⚡⚡⚡| ⭐⭐⭐   | Dev machines
phi3.5             | 3.8B | 4GB   | ⚡⚡⚡⚡⚡| ⭐⭐⭐   | Fast iteration
```

---

## Layer-2 Guidelines for Ollama

```markdown
# LAYER-2 GUIDELINES: OLLAMA AGENT

## Model Characteristics

You are running on **{model_name}** locally via Ollama.

**Strengths:**
- Complete privacy (100% local)
- No API costs
- No rate limits
- Offline capable

**Limitations:**
- Smaller context than Claude/GPT-4
- May need more explicit instructions
- Slower than cloud APIs

## Instructions

### Code Generation
- Be concise and focused
- Use clear, well-structured code
- Add inline comments for complex logic
- Test code before responding

### Context Management
- Context window: {context_length} tokens
- Prioritize most recent/relevant info
- Summarize when needed

### Error Handling
- Always validate inputs
- Handle edge cases explicitly
- Provide clear error messages

### Security
- Follow secure coding practices
- No hardcoded credentials
- Validate user input
- Use parameterized queries

## Examples

### Good Response:
```python
def calculate_fibonacci(n: int) -> int:
    """Calculate nth Fibonacci number using dynamic programming."""
    if n <= 1:
        return n

    # Use memoization for efficiency
    fib = [0] * (n + 1)
    fib[1] = 1

    for i in range(2, n + 1):
        fib[i] = fib[i-1] + fib[i-2]

    return fib[n]
```

### Bad Response:
```python
def fib(n):
    # Inefficient recursive approach
    if n <= 1: return n
    return fib(n-1) + fib(n-2)
```

## Quality Standards

- Code must be production-ready
- Follow language conventions
- Include error handling
- Add docstrings/comments
- Test edge cases

---

**Agent:** Ollama
**Version:** 1.0.0
**Model:** {model_name}
```

---

## Troubleshooting

### Ollama Not Starting

```bash
# Check if running
ollama list

# Restart Ollama
# Windows
Stop-Service Ollama
Start-Service Ollama

# Linux/macOS
sudo systemctl restart ollama
```

### Model Not Loading

```bash
# Check available models
ollama list

# Re-pull model
ollama pull qwen2.5-coder:32b

# Check VRAM
nvidia-smi  # NVIDIA
rocm-smi   # AMD
```

### CLI Tool Not Found

```bash
# Check installation
which ollama-code
which ollmcp
which aider

# Reinstall
npm link ollama-code
pipx reinstall ollmcp
```

### Performance Issues

```bash
# Increase GPU layers
export OLLAMA_NUM_GPU_LAYERS=-1

# Increase context
export OLLAMA_CONTEXT_LENGTH=32768

# Use smaller model
ollama pull qwen2.5-coder:7b
```

---

## Next Steps

1. ✅ Install Ollama
2. ✅ Pull recommended models
3. ✅ Install ollama-code and ollmcp
4. ✅ Configure MCP servers
5. ✅ Test with sample task
6. ✅ Integrate with orchestrator
7. ✅ Deploy Layer-2 guidelines

---

**Documentation:**
- Ollama: https://ollama.com/docs
- ollama-code: https://github.com/Foadsf/ollama-code
- ollmcp: https://github.com/jonigl/mcp-client-for-ollama
- MCP Servers: https://modelcontextprotocol.io/servers
- Aider: https://aider.chat/docs/
