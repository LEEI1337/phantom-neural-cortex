# Sandbox Hardening Architecture (Phase 7 Initial)

## Overview

The goal is to transition from raw asynchronous execution within the main process to strictly isolated, containerized execution. This prevents skills (which may contain dynamic code) from accessing the host filesystem, environment variables, or other neural cortex components without explicit permission.

## Proposed Components

### 1. Unified Skill Runner (Dockerfile)

A base image optimized for skill execution.

- **Base**: `python:3.11-slim`
- **Security**:
  - Non-root user `phantom`.
  - Minimal packages installed.
  - Entrypoint: A Python bridge that serializes output to JSON.

### 2. DockerSandbox Implementation

The evolution of `skills/sandbox.py`.

- **Logic**:
  - Uses the `docker` Python SDK.
  - Dynamically builds/pulls skill-specific layers if extra requirements (pip) are needed.
  - Mounts a temporary `workdir`.
  - Enforces hard resource quotas.

### 3. Resource Policy

Defines what a skill can do:

- **Default**: No network, 256MB RAM, 0.5 CPU.
- **elevated-network**: Allows access to specific domains (e.g., GitHub API).
- **elevated-compute**: Higher memory/CPU for heavy processing.

## Implementation Steps

1. **Step 1**: Create `skills/docker_runner/` containing the base Dockerfile and execution bridge.
2. **Step 2**: Refactor `sandbox.py` to support dual-mode (Local vs. Docker).
3. **Step 3**: Implement Skill Context virtualization (passing API keys securely into containers).
4. **Step 4**: Stress test isolation with "malicious" skills.

## Security Manifesto

- "Skills shall not know they are running on a host."
- "All data entering/leaving the container must be strictly schema-validated."
- "Persistent storage for skills must be explicitly requested and mapped."

---
*Drafted: Feb 2026*
