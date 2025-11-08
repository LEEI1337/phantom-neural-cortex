# GitHub Copilot Custom Instructions

## Project Context
This is a Claude Code configuration repository optimized for professional development.

## Code Style & Standards

### TypeScript/JavaScript
- Use TypeScript with strict mode enabled
- Prefer functional components with hooks (React)
- Use async/await over promises
- Explicit return types for functions
- No `any` types - use `unknown` if necessary

### Python
- Follow PEP 8 style guide
- Type hints for all function signatures
- Use dataclasses or Pydantic models
- Async/await for I/O operations

### General
- Maximum line length: 100 characters
- Use meaningful variable names
- Single responsibility principle
- Comment complex logic only
- No dead code or commented-out code

## Security Requirements
- **Never** hardcode secrets, API keys, or passwords
- Always validate and sanitize user inputs
- Use parameterized queries (prevent SQL injection)
- Implement proper authentication/authorization
- Follow OWASP Top 10 guidelines
- Use HTTPS only for production APIs

## Testing Requirements
- Minimum 80% code coverage for critical paths
- Unit tests for all public functions
- Integration tests for API endpoints
- E2E tests for critical user flows
- Test edge cases and error conditions

## Documentation
- JSDoc/PyDoc for all public APIs
- README for each module/package
- Inline comments for complex algorithms
- ADRs (Architecture Decision Records) for major changes

## Performance Guidelines
- Optimize database queries (use EXPLAIN)
- Lazy load components where possible
- Minimize bundle size (code splitting)
- Use memoization for expensive computations
- Monitor and optimize rendering performance

## Error Handling
- Use try/catch for all async operations
- Provide meaningful error messages
- Log errors with context
- Never silently catch errors
- Implement proper error boundaries (React)

## Git Commit Messages
Format: `<type>(<scope>): <subject>`

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Adding tests
- chore: Maintenance

Example: `feat(auth): add OAuth2 integration`

## MCP Servers Available
- filesystem - File operations
- memory - Context retention
- github - Repository access
- brave-search - Web research
- docs - Framework documentation
- postmancer - API testing
- playwright - Browser automation
- time - Timezone handling
- sqlite - Local database
- sequential-thinking - Complex reasoning

## Frameworks & Libraries

### Preferred Stack
- **Frontend:** React 18+, Next.js 14+, TypeScript
- **Styling:** Tailwind CSS, CSS Modules
- **State:** Context API, Zustand, or Jotai
- **Data Fetching:** React Query or SWR
- **Forms:** React Hook Form + Zod
- **Testing:** Jest + React Testing Library
- **E2E:** Playwright

### Backend
- **Node.js:** Express or Fastify
- **Python:** FastAPI or Django
- **Database:** PostgreSQL or SQLite
- **ORM:** Prisma (Node.js) or SQLAlchemy (Python)
- **API:** REST or GraphQL (Apollo)

## File Structure
```
src/
├── components/       # Reusable UI components
├── pages/           # Next.js pages or routes
├── hooks/           # Custom React hooks
├── utils/           # Utility functions
├── services/        # API services
├── types/           # TypeScript types
├── styles/          # Global styles
└── tests/           # Test files
```

## Code Review Checklist
Before submitting code, ensure:
- [ ] All tests pass
- [ ] No TypeScript errors
- [ ] No console.log statements
- [ ] No hardcoded values
- [ ] Proper error handling
- [ ] Documentation updated
- [ ] No unused imports
- [ ] Follows project conventions

## Environment Variables
Always use environment variables for:
- API keys
- Database URLs
- API endpoints
- Feature flags
- Third-party service credentials

Use `.env.example` to document required variables.

## Accessibility
- Use semantic HTML
- ARIA labels where needed
- Keyboard navigation support
- Screen reader compatibility
- Color contrast ratios (WCAG AA)

## Localization
- Externalize all user-facing strings
- Use i18n libraries (react-i18next, next-i18next)
- Support RTL languages
- Format dates/numbers per locale

---

**Last Updated:** 2025-11-08
**For:** GitHub Copilot, Claude Code, all AI assistants
