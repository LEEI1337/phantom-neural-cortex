# Code Quality Microagent

This microagent defines code quality standards and best practices for OpenHands when working with this repository.

## Language-Specific Standards

### TypeScript/JavaScript
- **Always** use TypeScript over JavaScript
- Enable `strict` mode in tsconfig.json
- Explicit return types for all functions
- No `any` types - use `unknown` if type is truly unknown
- Prefer functional components with hooks (React)
- Use async/await over raw promises

### Python
- Follow PEP 8 style guide
- Type hints for all function signatures
- Use dataclasses or Pydantic models for data structures
- Prefer async/await for I/O operations

## Code Organization

### File Structure
```
src/
├── components/      # UI components (React)
├── pages/          # Next.js pages or routes
├── hooks/          # Custom React hooks
├── utils/          # Pure utility functions
├── services/       # API services & external integrations
├── types/          # TypeScript type definitions
├── styles/         # Global styles & theme
└── tests/          # Test files
```

### Naming Conventions
- **Files**: kebab-case (`user-profile.tsx`)
- **Components**: PascalCase (`UserProfile`)
- **Functions**: camelCase (`getUserData`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_RETRY_COUNT`)
- **Types/Interfaces**: PascalCase with `I` prefix for interfaces (`IUserData`)

## Security Requirements

### Never Allow
- ❌ Hardcoded API keys or secrets
- ❌ SQL injection vulnerabilities (always use parameterized queries)
- ❌ XSS vulnerabilities (sanitize all user inputs)
- ❌ Exposed sensitive data in logs
- ❌ Insecure dependencies (check with `npm audit`)

### Always Require
- ✅ Input validation & sanitization
- ✅ Proper error handling
- ✅ HTTPS for all external API calls
- ✅ Authentication/Authorization checks
- ✅ CSRF protection for state-changing operations

## Testing Requirements

### Coverage Targets
- **Critical paths**: 100% coverage
- **Business logic**: 90%+ coverage
- **UI components**: 80%+ coverage
- **Utilities**: 100% coverage

### Test Types
1. **Unit Tests** (Jest)
   - Test individual functions/components
   - Mock external dependencies
   - Fast execution (<1s per test)

2. **Integration Tests** (Playwright)
   - Test API endpoints
   - Test component interactions
   - Test data flow

3. **E2E Tests** (Playwright)
   - Test critical user flows
   - Test across browsers (Chromium, Firefox, WebKit)
   - Run in CI/CD pipeline

## Performance Guidelines

### React/Frontend
- Lazy load routes & heavy components
- Memoize expensive computations (`useMemo`, `useCallback`)
- Optimize images (WebP, lazy loading)
- Code splitting for large bundles
- Target bundle size: <200KB initial load

### Backend/API
- Database query optimization (use EXPLAIN)
- Implement caching (Redis, in-memory)
- Connection pooling for databases
- Rate limiting for public endpoints
- Response time target: <200ms (p95)

### General
- Avoid N+1 queries
- Use pagination for large datasets
- Implement request debouncing
- Monitor and optimize rendering

## Error Handling

### Principles
1. **Never silent failures** - Always log errors
2. **Meaningful messages** - User-friendly error descriptions
3. **Error boundaries** - Catch React component errors
4. **Fallbacks** - Graceful degradation

### Implementation
```typescript
// Good
try {
  const data = await fetchUserData(id);
  return data;
} catch (error) {
  logger.error('Failed to fetch user data', { userId: id, error });
  throw new AppError('Unable to load user profile', { cause: error });
}

// Bad
try {
  const data = await fetchUserData(id);
  return data;
} catch (error) {
  // Silent failure
}
```

## Documentation Requirements

### Code Comments
- **JSDoc** for all public APIs
- **Inline comments** only for complex logic
- **No commented-out code** (use git history)

### README Files
- Each module should have a README
- Include usage examples
- Document configuration options
- List dependencies

### Architecture Decisions
- Document major decisions in ADR format
- Store in `docs/architecture/decisions/`
- Use markdown template

## Git Commit Standards

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting (no code change)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

### Examples
```
feat(auth): add OAuth2 integration

Implement OAuth2 authentication flow using Authorization Code grant type.
Supports Google and GitHub providers.

Closes #123
```

## Code Review Checklist

Before submitting code for review:
- [ ] All tests pass locally
- [ ] No TypeScript/ESLint errors
- [ ] No console.log statements
- [ ] Proper error handling implemented
- [ ] Security vulnerabilities addressed
- [ ] Performance considered
- [ ] Documentation updated
- [ ] No unused imports or variables

## Accessibility Standards

- ✅ Semantic HTML elements
- ✅ ARIA labels where appropriate
- ✅ Keyboard navigation support
- ✅ Screen reader compatibility
- ✅ Color contrast ratios (WCAG AA minimum)
- ✅ Focus indicators visible

## Environment Variables

### Naming Convention
```
NEXT_PUBLIC_*  # Client-side (Next.js)
VITE_*         # Client-side (Vite)
API_*          # Server-side API configs
DB_*           # Database configs
```

### Required in .env
- API keys
- Database URLs
- Third-party service credentials
- Feature flags
- Environment identifiers (dev/staging/prod)

### Never Commit
- Actual API keys or secrets
- Production credentials
- Personal access tokens

Use `.env.example` to document required variables.

---

**When OpenHands generates code, it should automatically follow these standards.**
