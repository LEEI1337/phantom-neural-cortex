#!/bin/bash
# OpenHands Pre-Commit Hook
# Runs before every commit to ensure code quality

set -e  # Exit on error

echo "🔍 OpenHands Pre-Commit: Running quality checks..."

# Track if any checks fail
CHECKS_FAILED=0

# 1. Lint Check
if [ -f "package.json" ] && npm run lint --if-present &> /dev/null; then
    echo "Running ESLint..."
    if npm run lint; then
        echo "✅ Lint check passed"
    else
        echo "❌ Lint check failed"
        CHECKS_FAILED=1
    fi
fi

# 2. TypeScript Type Check
if [ -f "tsconfig.json" ]; then
    echo "Running TypeScript type check..."
    if npm run type-check --if-present || npx tsc --noEmit; then
        echo "✅ Type check passed"
    else
        echo "❌ Type check failed"
        CHECKS_FAILED=1
    fi
fi

# 3. Format Check
if command -v prettier &> /dev/null || npm list prettier &> /dev/null; then
    echo "Checking code formatting..."
    if npm run format:check --if-present || npx prettier --check . &> /dev/null; then
        echo "✅ Format check passed"
    else
        echo "⚠️  Code formatting issues detected"
        echo "   Run 'npm run format' to fix"
        # Don't fail on format issues, just warn
    fi
fi

# 4. Unit Tests (fast tests only)
if [ -f "package.json" ]; then
    echo "Running unit tests..."
    if npm run test:unit --if-present || npm run test -- --passWithNoTests &> /dev/null; then
        echo "✅ Unit tests passed"
    else
        echo "❌ Unit tests failed"
        CHECKS_FAILED=1
    fi
fi

# 5. Security Check (quick scan)
echo "Running security audit..."
if npm audit --audit-level=high --production 2>&1 | grep -q "found 0 vulnerabilities"; then
    echo "✅ No high-severity vulnerabilities found"
else
    echo "⚠️  Security vulnerabilities detected"
    echo "   Run 'npm audit fix' to attempt fixes"
    # Don't fail on vulnerabilities, just warn
fi

# 6. Check for console.log (warn only)
echo "Checking for console.log statements..."
if git diff --cached --name-only | grep -E '\.(js|ts|jsx|tsx)$' | xargs grep -n "console\.log" 2>/dev/null; then
    echo "⚠️  Found console.log statements - consider removing before production"
    # Don't fail, just warn
fi

# 7. Check for TODO/FIXME comments
echo "Checking for TODO/FIXME comments..."
TODO_COUNT=$(git diff --cached | grep -E '^\+.*\b(TODO|FIXME)\b' | wc -l || echo "0")
if [ "$TODO_COUNT" -gt 0 ]; then
    echo "⚠️  Adding $TODO_COUNT new TODO/FIXME comments"
    # Don't fail, just inform
fi

# 8. Check file sizes (prevent large files)
echo "Checking file sizes..."
LARGE_FILES=$(git diff --cached --name-only | xargs -I {} du -k "{}" 2>/dev/null | awk '$1 > 1024 {print $2}' || echo "")
if [ ! -z "$LARGE_FILES" ]; then
    echo "⚠️  Warning: Large files detected (>1MB):"
    echo "$LARGE_FILES"
    # Don't fail, just warn
fi

# 9. Validate JSON files
echo "Validating JSON files..."
for file in $(git diff --cached --name-only | grep '\.json$'); do
    if [ -f "$file" ]; then
        if python -m json.tool "$file" > /dev/null 2>&1 || node -e "JSON.parse(require('fs').readFileSync('$file', 'utf8'))" > /dev/null 2>&1; then
            echo "✅ $file is valid JSON"
        else
            echo "❌ $file is invalid JSON"
            CHECKS_FAILED=1
        fi
    fi
done

# 10. Check for merge conflicts
echo "Checking for merge conflicts..."
if git diff --cached | grep -E '^(<{7}|={7}|>{7})'; then
    echo "❌ Merge conflict markers found"
    CHECKS_FAILED=1
else
    echo "✅ No merge conflicts"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Exit with appropriate code
if [ $CHECKS_FAILED -eq 0 ]; then
    echo "✅ All pre-commit checks passed!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 0
else
    echo "❌ Pre-commit checks failed!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Fix the issues above before committing."
    echo "To bypass (not recommended): git commit --no-verify"
    exit 1
fi
