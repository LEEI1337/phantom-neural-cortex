"""
CLI-First Multi-Agent Orchestrator
Hub-and-Spoke Pattern with Async Coordination

Based on 2025 Best Practices:
- Subprocess execution for Claude & Gemini CLI
- Real-time WebSocket streaming
- Redis for state management
- asyncio.gather for parallel execution
- Cost optimization (prefer FREE Gemini)
"""

import asyncio
import subprocess
import json
import uuid
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime
import logging
import os
import platform

from .circuit_breaker import CircuitBreaker, CircuitState
from .langfuse_integration import get_langfuse_observer

logger = logging.getLogger(__name__)


class AgentType(Enum):
    """Available CLI agents"""
    CLAUDE = "claude"
    GEMINI = "gemini"
    COPILOT = "copilot"


class TaskType(Enum):
    """Task categories for smart routing"""
    SECURITY = "security"
    ARCHITECTURE = "architecture"
    BULK_ANALYSIS = "bulk_analysis"
    GITHUB_WORKFLOW = "github_workflow"
    CODE_GENERATION = "code_generation"
    DEBUGGING = "debugging"


class Task:
    """Task definition"""
    def __init__(
        self,
        id: str,
        prompt: str,
        task_type: TaskType = TaskType.CODE_GENERATION,
        files: List[str] = None,
        workspace: str = ".",
        context_size: int = 0,
        requires_security: bool = False,
        complexity: float = 0.5
    ):
        self.id = id
        self.prompt = prompt
        self.task_type = task_type
        self.files = files or []
        self.workspace = workspace
        self.context_size = context_size
        self.requires_security = requires_security
        self.complexity = complexity


class AgentResponse:
    """Unified response from any agent"""
    def __init__(
        self,
        agent: AgentType,
        content: str,
        tokens: int,
        cost: float,
        duration: float,
        session_id: Optional[str] = None,
        metadata: Dict[str, Any] = None
    ):
        self.agent = agent
        self.content = content
        self.tokens = tokens
        self.cost = cost
        self.duration = duration
        self.session_id = session_id
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow()


class CLIOrchestrator:
    """
    Hub-and-Spoke Multi-Agent Orchestrator

    Coordinates multiple CLI-based AI agents via subprocess:
    - Claude CLI (--print mode): Security, architecture, complex reasoning
    - Gemini CLI (-o json): Bulk operations, large context (FREE)

    Features:
    - Smart agent selection (RL-based reward model)
    - Real-time WebSocket streaming
    - Cost optimization (prefer Gemini when possible)
    - Parallel agent execution via asyncio.gather
    """

    def __init__(
        self,
        redis_manager=None,
        websocket_manager=None
    ):
        # State Management
        self.redis = redis_manager
        self.websocket = websocket_manager

        # Reward Model (RL-based agent selection)
        self.reward_model = {
            "claude": 0.8,   # High quality, expensive
            "gemini": 0.75,  # Good quality, FREE
        }

        self.last_selection_reason = ""

        # Circuit Breakers for resilience
        self.claude_breaker = CircuitBreaker(
            failure_threshold=5,
            timeout_duration=60,
            expected_exception=RuntimeError
        )
        self.gemini_breaker = CircuitBreaker(
            failure_threshold=5,
            timeout_duration=60,
            expected_exception=RuntimeError
        )

        # Langfuse observability (optional)
        self.langfuse = get_langfuse_observer()

        logger.info("CLIOrchestrator initialized (Hub-and-Spoke, subprocess-based)")

    async def execute_task(self, task: Task) -> AgentResponse:
        """
        Execute task with optimal agent selection.

        Smart Selection Logic:
        1. Check task requirements (security, complexity, context size)
        2. Query RL-based reward model for agent performance history
        3. Consider cost optimization (prefer Gemini when possible)
        4. Route to selected agent via subprocess
        5. Stream progress via WebSocket
        6. Track cost and performance metrics

        Args:
            task: Task definition

        Returns:
            AgentResponse with result, cost, and metadata
        """
        logger.info(f"Executing task {task.id} (type: {task.task_type.value})")

        # Smart Agent Selection
        agent = await self._select_agent(task)
        logger.info(f"Selected agent: {agent.value} ({self.last_selection_reason})")

        # Track agent selection in Langfuse
        self.langfuse.track_agent_selection(
            task_id=task.id,
            selected_agent=agent.value,
            reason=self.last_selection_reason,
            all_rewards=self.reward_model
        )

        # Broadcast agent selection
        if self.websocket:
            await self.websocket.broadcast({
                "type": "agent_selected",
                "task_id": task.id,
                "agent": agent.value,
                "reason": self.last_selection_reason
            }, f"task_{task.id}")

        # Route to agent with Langfuse tracing
        start_time = datetime.utcnow()

        async with self.langfuse.trace_agent_execution(
            task_id=task.id,
            agent=agent.value,
            prompt=task.prompt,
            metadata={
                "task_type": task.task_type.value,
                "files_count": len(task.files),
                "workspace": task.workspace
            }
        ) as trace:
            try:
                if agent == AgentType.CLAUDE:
                    response = await self._execute_claude(task)
                elif agent == AgentType.GEMINI:
                    response = await self._execute_gemini(task)
                else:
                    raise ValueError(f"Unknown agent: {agent}")

                # Calculate duration
                duration = (datetime.utcnow() - start_time).total_seconds()
                response.duration = duration

                # Update Langfuse trace
                trace.update(
                    output=response.content,
                    tokens=response.tokens,
                    cost=response.cost,
                    metadata={"duration": duration}
                )

                # Update reward model
                await self._update_reward(agent, task, response)

                # Broadcast completion
                if self.websocket:
                    await self.websocket.broadcast({
                        "type": "task_completed",
                        "task_id": task.id,
                        "agent": agent.value,
                        "cost": response.cost,
                        "tokens": response.tokens,
                        "duration": duration
                    }, f"task_{task.id}")

                return response

            except Exception as e:
                logger.error(f"Task {task.id} failed: {e}")

                # Update trace with error
                trace.update(metadata={"error": str(e)})

                # Broadcast error
                if self.websocket:
                    await self.websocket.broadcast({
                        "type": "task_failed",
                        "task_id": task.id,
                        "agent": agent.value,
                        "error": str(e)
                    }, f"task_{task.id}")

                raise

    async def _select_agent(self, task: Task) -> AgentType:
        """
        Select optimal agent for task (RL-based + rules).

        Decision Logic:
        1. SECURITY tasks -> Claude (best reasoning)
        2. LARGE CONTEXT (>100k tokens) -> Gemini (2M tokens FREE)
        3. DEFAULT -> Gemini (FREE!)

        With RL Refinement:
        - Query reward model for agent performance history
        - Adjust based on recent success rates
        """
        # Load reward model from Redis
        if self.redis:
            stored_rewards = await self.redis.hgetall("agent_rewards")
            if stored_rewards:
                self.reward_model = {k: float(v) for k, v in stored_rewards.items()}

        # Rule-based selection (override RL for critical tasks)
        if task.requires_security or task.task_type == TaskType.SECURITY:
            self.last_selection_reason = "Security-critical task requires Claude"
            return AgentType.CLAUDE

        if task.context_size > 100_000 or len(task.files) > 50:
            self.last_selection_reason = f"Large context ({task.context_size} tokens) -> Gemini (2M FREE)"
            return AgentType.GEMINI

        # RL-based selection
        claude_reward = self.reward_model.get("claude", 0.8)
        gemini_reward = self.reward_model.get("gemini", 0.75)

        # Cost-weighted rewards (Gemini is FREE!)
        claude_score = claude_reward * 0.7  # Penalize cost
        gemini_score = gemini_reward * 1.2  # Boost FREE agent

        # Select highest score
        if gemini_score >= claude_score:
            self.last_selection_reason = f"Gemini has highest reward ({gemini_reward:.2f}) and is FREE"
            return AgentType.GEMINI
        else:
            self.last_selection_reason = f"Claude selected for quality (reward: {claude_reward:.2f})"
            return AgentType.CLAUDE

    async def _execute_claude(self, task: Task) -> AgentResponse:
        """
        Execute via Claude CLI subprocess with circuit breaker protection.

        Command:
            claude --print -o json "prompt"

        Features:
        - Non-interactive output (--print)
        - JSON format for parsing
        - Session continuity via --continue flag
        - Circuit breaker for resilience
        """
        async def _claude_subprocess():
            """Inner function for circuit breaker wrapping"""
            # Get or create session ID
            session_id = await self._get_session(task.id)

            # Build command (use .cmd extension on Windows)
            claude_bin = "claude.cmd" if platform.system() == "Windows" else "claude"
            cmd = [claude_bin, "--print", "--output-format", "json"]

            # Add session continuity
            if session_id:
                cmd.extend(["--resume", session_id])

            # Add prompt
            cmd.append(task.prompt)

            logger.info(f"Executing Claude CLI: {' '.join(cmd[:3])}...")

            # Execute subprocess
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=task.workspace
            )

            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=120.0  # 2 min timeout
            )

            if process.returncode != 0:
                raise RuntimeError(f"Claude CLI failed: {stderr.decode()}")

            # Parse JSON output
            result = json.loads(stdout.decode())

            # Extract content and tokens
            content = result.get("content", "")
            tokens = result.get("usage", {}).get("total_tokens", 0)

            # Calculate cost ($3/1M input, $15/1M output)
            input_tokens = result.get("usage", {}).get("input_tokens", 0)
            output_tokens = result.get("usage", {}).get("output_tokens", 0)
            cost = (input_tokens / 1_000_000) * 3.0 + (output_tokens / 1_000_000) * 15.0

            # Store session
            new_session_id = result.get("session_id", session_id)
            if new_session_id:
                await self._store_session(task.id, new_session_id)

            logger.info(f"Claude response: {tokens} tokens, ${cost:.4f}")

            return AgentResponse(
                agent=AgentType.CLAUDE,
                content=content,
                tokens=tokens,
                cost=cost,
                duration=0,  # Set by caller
                session_id=new_session_id
            )

        # Execute with circuit breaker protection
        try:
            return await self.claude_breaker.call_async(_claude_subprocess)

        except asyncio.TimeoutError:
            logger.error("Claude CLI timeout (120s)")
            raise RuntimeError("Claude CLI timeout")

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude output: {e}")
            # Return fallback response
            return AgentResponse(
                agent=AgentType.CLAUDE,
                content="",
                tokens=0,
                cost=0.0,
                duration=0
            )

    async def _execute_gemini(self, task: Task) -> AgentResponse:
        """
        Execute via Gemini CLI subprocess with circuit breaker protection.

        Command:
            gemini -o json "prompt"

        Features:
        - JSON output format
        - Real-time streaming
        - Glob pattern file context
        - FREE (no cost)
        - Circuit breaker for resilience
        """
        async def _gemini_subprocess():
            """Inner function for circuit breaker wrapping"""
            # Build command (use .cmd extension on Windows)
            gemini_bin = "gemini.cmd" if platform.system() == "Windows" else "gemini"
            cmd = [gemini_bin, "-o", "json"]

            # Add yolo mode for auto-approval (optional)
            # cmd.append("--yolo")

            # Add file context
            if task.files:
                for file_pattern in task.files:
                    cmd.extend(["--include-directories", file_pattern])

            # Add prompt
            cmd.append(task.prompt)

            logger.info(f"Executing Gemini CLI: {' '.join(cmd[:3])}...")

            # Execute subprocess with streaming
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=task.workspace
            )

            # Stream output line by line
            output_lines = []

            while True:
                line = await process.stdout.readline()

                if not line:
                    break

                line_str = line.decode().strip()
                output_lines.append(line_str)

                # Stream to WebSocket
                if self.websocket and line_str:
                    await self.websocket.broadcast({
                        "type": "agent_progress",
                        "task_id": task.id,
                        "line": line_str
                    }, f"task_{task.id}")

            # Wait for completion
            await process.wait()

            if process.returncode != 0:
                stderr_output = await process.stderr.read()
                raise RuntimeError(f"Gemini CLI failed: {stderr_output.decode()}")

            # Parse JSON output
            full_output = "".join(output_lines)

            try:
                result = json.loads(full_output)
                content = result.get("response", full_output)
                tokens = result.get("usage", {}).get("total_tokens", 0)
            except json.JSONDecodeError:
                # Use raw output if not JSON
                content = full_output
                tokens = len(full_output.split()) * 1.3  # Rough estimate

            logger.info(f"Gemini response: {tokens} tokens, $0.00 (FREE)")

            return AgentResponse(
                agent=AgentType.GEMINI,
                content=content,
                tokens=int(tokens),
                cost=0.0,  # FREE!
                duration=0,
                metadata={"raw_output": full_output}
            )

        # Execute with circuit breaker protection
        try:
            return await self.gemini_breaker.call_async(_gemini_subprocess)

        except Exception as e:
            logger.error(f"Gemini CLI failed: {e}")
            raise

    async def _get_session(self, task_id: str) -> Optional[str]:
        """Get session ID from Redis"""
        if not self.redis:
            return None

        session_id = await self.redis.get_state(f"session:{task_id}")
        return session_id

    async def _store_session(self, task_id: str, session_id: str):
        """Store session ID in Redis"""
        if not self.redis:
            return

        # Store with 24h TTL
        await self.redis.set_state(f"session:{task_id}", session_id, ttl=86400)

    async def _update_reward(
        self,
        agent: AgentType,
        task: Task,
        response: AgentResponse
    ):
        """
        Update reward model based on task outcome.

        Reward Calculation:
        - Speed: tokens/second
        - Cost: Inverse (FREE = 1.0)
        - Quality: Placeholder (would use real feedback)
        """
        # Calculate reward signal
        tokens_per_sec = response.tokens / max(response.duration, 0.1)
        speed_score = min(tokens_per_sec / 100, 1.0)

        # Cost score (inverse, FREE = 1.0)
        if response.cost == 0:
            cost_score = 1.0
        else:
            cost_score = max(1.0 - response.cost / 0.1, 0.0)

        # Quality score (placeholder)
        quality_score = 0.8

        # Weighted average
        reward = (
            0.3 * speed_score +
            0.3 * cost_score +
            0.4 * quality_score
        )

        # Update reward model (exponential moving average)
        agent_key = agent.value
        current_reward = self.reward_model.get(agent_key, 0.5)
        learning_rate = 0.1
        new_reward = (1 - learning_rate) * current_reward + learning_rate * reward

        self.reward_model[agent_key] = new_reward

        # Store in Redis
        if self.redis:
            await self.redis.hset("agent_rewards", agent_key, new_reward)

        logger.info(f"Updated {agent_key} reward: {current_reward:.2f} -> {new_reward:.2f}")

    async def execute_parallel(self, tasks: List[Task]) -> List[AgentResponse]:
        """
        Execute multiple tasks in parallel via asyncio.gather.

        Use Cases:
        - Bulk code analysis
        - Parallel security audits
        - Multi-file refactoring

        Example:
            tasks = [
                Task("1", "Audit file1.py", TaskType.SECURITY),
                Task("2", "Audit file2.py", TaskType.SECURITY),
                Task("3", "Audit file3.py", TaskType.SECURITY)
            ]
            responses = await orchestrator.execute_parallel(tasks)
        """
        logger.info(f"Executing {len(tasks)} tasks in parallel")

        # Execute all tasks concurrently
        responses = await asyncio.gather(
            *[self.execute_task(task) for task in tasks],
            return_exceptions=True
        )

        # Filter out exceptions
        valid_responses = [
            r for r in responses
            if isinstance(r, AgentResponse)
        ]

        logger.info(f"Completed {len(valid_responses)}/{len(tasks)} tasks")

        return valid_responses

    async def get_reward_model(self) -> Dict[str, float]:
        """Get current reward model"""
        if self.redis:
            stored_rewards = await self.redis.hgetall("agent_rewards")
            if stored_rewards:
                return {k: float(v) for k, v in stored_rewards.items()}

        return self.reward_model

    def get_circuit_breaker_status(self) -> Dict[str, Any]:
        """Get circuit breaker status for all agents"""
        return {
            "claude": {
                "state": self.claude_breaker.state.value,
                "failure_count": self.claude_breaker.failure_count,
                "last_failure": self.claude_breaker.last_failure_time.isoformat() if self.claude_breaker.last_failure_time else None
            },
            "gemini": {
                "state": self.gemini_breaker.state.value,
                "failure_count": self.gemini_breaker.failure_count,
                "last_failure": self.gemini_breaker.last_failure_time.isoformat() if self.gemini_breaker.last_failure_time else None
            }
        }
