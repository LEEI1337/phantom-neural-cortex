# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          | Status                              |
| ------- | ------------------ | ----------------------------------- |
| 3.x.x   | :white_check_mark: | Active (v3.0.0 released Feb 2026)   |
| 2.x.x   | :white_check_mark: | Maintenance (Security patches only) |
| < 2.0   | :x:                | End of Life                         |

## AI-Specific Security (2026 Update)

As an AI-driven orchestration platform, we recognize unique security challenges:

### 1. Prompt Injection Defense

- **Dynamic System Prompts**: We use non-deterministic boundary markers to prevent prompt leakage.
- **Output Sanitization**: All AI-generated code is scanned by our Quality Assessment System before execution.
- **Indirect Injection**: We monitor external data sources (GitHub, web search) for malicious instructions embedded in documents.

### 2. Context Window Security

- **Context Poisoning**: Mitigation strategies against long-range context poisoning are implemented in the `ContextCompactor`.
- **Resource Exhaustion**: The `ContextTracker` prevents context-stuffing attacks that aim to spike execution costs.

### 3. Skill Sandbox Execution

- **Observation Mode**: Skills run in restricted environments with real-time observation.
- **Permission Scoping**: Skills only have access to specific APIs (e.g., `github_api`) requested in their metadata.
- **Resource Limits**: CPU/Memory/Time limits are enforced to prevent crypto-jacking or DoS.

## Reporting a Vulnerability

We take the security of Phantom Neural Cortex seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Please DO NOT

- **Open a public GitHub issue** for security vulnerabilities
- **Discuss the vulnerability publicly** before it has been addressed

### Please DO

**Report security bugs privately via GitHub Security Advisories:**

1. Go to <https://github.com/LEEI1337/phantom-neural-cortex/security/advisories/new>
2. Click "Report a vulnerability"
3. Fill in the details

**OR Email us directly:**

- Create a new GitHub issue with title: "SECURITY: [Brief Description]"
- Mark it as confidential
- We will respond within 48 hours

### What to Include

Please include the following information in your report:

- Type of vulnerability (e.g., RCE, XSS, SQL injection, exposed secrets)
- Full paths of source file(s) related to the manifestation of the issue
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### Our Commitment

- We will acknowledge your email within 48 hours
- We will provide a detailed response within 7 days
- We will keep you informed about our progress
- We will credit you in the security advisory (unless you prefer to remain anonymous)

## Security Best Practices for Users

### API Keys and Secrets

**CRITICAL**: Never commit API keys or secrets to the repository

- Always use `.env` files (already in `.gitignore`)
- Use environment variables for all sensitive data
- Rotate API keys regularly
- Use separate keys for development and production

### MCP Server Security

- Only install MCP servers from trusted sources
- Review server code before installation
- Keep MCP servers updated
- Monitor server logs for suspicious activity

### Docker/Container Security

- Keep Docker Desktop updated
- Review Rover container configurations
- Limit container permissions
- Use official base images only

### Claude Code / AI CLI Security

- Don't share your Claude API keys
- Review AI-generated code before execution
- Use separate accounts for testing
- Enable 2FA on all AI service accounts

## Known Security Considerations

### Current Architecture

This project orchestrates multiple AI systems and MCP servers. Key security considerations:

1. **API Key Management**: Multiple API keys are required (Claude, Gemini, GitHub, Brave Search, Perplexity)
   - ✅ All stored in `.env` (gitignored)
   - ✅ Loaded via environment variables
   - ⚠️ Users must manage key rotation

2. **MCP Server Trust**: 18 MCP servers with varying levels of access
   - ✅ Official @modelcontextprotocol servers are audited
   - ⚠️ Community servers require manual review
   - ✅ All servers run in isolated processes

3. **Rover Isolation**: Git worktrees and Docker containers
   - ✅ Each task runs in isolated environment
   - ✅ No shared state between tasks
   - ⚠️ Host file system access required

4. **Lazy Bird Automation**
   - ⚠️ Will execute AI-generated code automatically
   - ⚠️ Requires robust test validation
   - ⚠️ Needs careful permission management

## Security Updates

We will announce security updates via:

- GitHub Security Advisories
- GitHub Releases with `[SECURITY]` tag
- README.md security notice (for critical issues)

Subscribe to repository notifications to stay informed.

## Disclosure Policy

When we receive a security bug report, we will:

1. Confirm the problem and determine affected versions
2. Audit code to find similar problems
3. Prepare fixes for all supported versions
4. Release patches as soon as possible
5. Publish a security advisory

## Attribution

We thank the following researchers for responsibly disclosing security issues:

- (None yet - be the first!)

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security/getting-started/securing-your-repository)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Anthropic Security Practices](https://docs.anthropic.com/claude/docs/security)

---

**Last Updated**: 2026-02-08

Thank you for helping keep Phantom Neural Cortex and its users safe!
