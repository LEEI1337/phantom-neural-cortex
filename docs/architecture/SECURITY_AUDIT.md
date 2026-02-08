# Phase 7: Sandbox Hardening & Security Verification

## 1. Security Manifesto

All skills in the Phantom Neural Cortex must be treated as untrusted code. To protect the host system and user data, we enforce a "Zero-Trust" execution model.

## 2. Theoretical Architecture

The hardening is achieved by wrapping the skill execution in an OCI-compliant container (Docker) with the following constraints:

- **No Persistence**: Containers are transient and destroyed immediately after action completion (`--rm`).
- **Read-Only Root**: The skill cannot modify the container's OS layer.
- **Resource Quotas**: Hard limits on memory and CPU to prevent DoS attacks via infinite loops or memory bombs.
- **Network Gap**: No default internet access. Only white-listed skills get outbound access via explicit policy.

## 3. Test Procedures

We use a specialized `MaliciousSkill` to attempt four types of escapes:

| Test Case | Objective | Pass Criteria |
|-----------|-----------|---------------|
| `test_fs_escape` | Access `/etc/passwd` or host `.env` | `os.path.exists` returns False or Permission Denied |
| `test_network_access` | `connect()` to google.com | `socket.error` or Timeout |
| `test_env_leak` | Read host `API_KEYS` | Values return `NOT_FOUND` |
| `test_resource_exhaustion` | Allocate 1GB RAM | Process killed by OOM Killer or `MemoryError` |

## 4. How to Run Audit

Ensure Docker is running on the host system, then execute:

```bash
# 1. Build the runner image
docker build -t phantom-skill-runner:latest ./skills/docker_runner

# 2. Run the automated security audit
python verify_phase7_security.py
```

## 5. Mitigation Strategies

If an audit fails:

1. **FS Escape**: Check Docker volume mounts in `skills/sandbox.py`. Ensure only `tmpdir` is mapped.
2. **Network Leak**: Verify `network_disabled: True` in the `container_config`.
3. **Resource Leak**: Lower the `mem_limit` and `nano_cpus` in `SkillSandbox` initialization.

---
*Verified for Version 3.5.0*
