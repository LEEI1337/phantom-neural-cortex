# Branch Protection Setup Guide

This guide will help you configure branch protection rules for the `master` branch on GitHub to ensure code quality, security, and collaboration standards.

## Why Branch Protection?

Branch protection rules enforce quality standards by:
- Requiring code reviews before merging
- Ensuring all CI/CD checks pass
- Preventing accidental force pushes or branch deletion
- Maintaining a clean, linear commit history
- Applying the same standards to all contributors (including maintainers)

## Prerequisites

Before enabling branch protection, ensure:

1. **GitHub Secrets are configured** (Settings → Secrets and variables → Actions):
   - `ANTHROPIC_API_KEY` - For OpenHands AI auto-fix functionality (optional)

2. **Workflows run successfully**:
   ```bash
   # Push a test commit to verify all workflows pass
   git push origin master
   ```

   Check GitHub Actions tab to ensure all jobs complete successfully:
   - ✅ Markdown Lint - Validates Markdown formatting
   - ✅ Check Links - Verifies all links in documentation
   - ✅ Validate Repository Structure - Checks required files exist

## Step-by-Step Configuration

### 1. Navigate to Branch Protection Settings

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Click **Branches** in the left sidebar
4. Under "Branch protection rules", click **Add rule** or **Add branch protection rule**

### 2. Configure Branch Name Pattern

- **Branch name pattern**: `master`

  This will apply the rules specifically to your master branch.

### 3. Enable Required Settings

#### ✅ Require a pull request before merging

- **Enable**: ✓ Require a pull request before merging
  - ✓ Require approvals: **1** (or **2** for higher security)
  - ✓ Dismiss stale pull request approvals when new commits are pushed
  - ☐ Require review from Code Owners (optional - only if you add a CODEOWNERS file)

**Why**: Ensures all changes are reviewed by at least one other person before merging.

#### ✅ Require status checks to pass before merging

- **Enable**: ✓ Require status checks to pass before merging
  - ✓ Require branches to be up to date before merging

- **Add required status checks** (click the search box and add these):
  - `Markdown Lint` - Validates Markdown formatting
  - `Check Links` - Verifies all documentation links work
  - `Validate Repository Structure` - Ensures required files exist

**Note**: These status checks will only appear in the list after they've run at least once. Push a commit to trigger the workflows first.

**Why**: Ensures documentation quality and prevents broken links from being merged.

#### ✅ Require conversation resolution before merging

- **Enable**: ✓ Require conversation resolution before merging

**Why**: Ensures all review comments are addressed before merging.

#### ✅ Require linear history

- **Enable**: ✓ Require linear history

**Why**: Prevents merge commits, keeping your git history clean and easy to follow. Forces use of squash or rebase merging.

#### ✅ Include administrators

- **Enable**: ✓ Include administrators

**Why**: Applies quality standards to everyone, including repository admins. No shortcuts!

#### ⚠️ Do not allow bypassing the above settings

- **Enable**: ✓ Do not allow bypassing the above settings

**Why**: Ensures no one can override these protections, even in emergencies.

### 4. Restrict Who Can Push (Optional but Recommended)

#### ✅ Restrict pushes that create matching branches

- **Enable**: ✓ Restrict pushes that create matching branches
  - Select specific people, teams, or apps that can push to this branch
  - Typically: Repository maintainers only

**Why**: Ensures only trusted contributors can push directly (though they still need PRs due to earlier settings).

### 5. Rules Applied to Everyone

#### ✅ Block force pushes

- **Enable**: ✓ Block force pushes

**Why**: Prevents rewriting commit history, which can cause problems for other contributors.

#### ✅ Allow deletions

- **Disable**: ☐ Allow deletions

**Why**: Prevents accidental deletion of the master branch.

### 6. Save Your Configuration

Click **Create** or **Save changes** at the bottom of the page.

## Verification

After enabling branch protection:

1. **Test a direct push** (should fail):
   ```bash
   # This should be rejected
   git push origin master
   ```

   Expected message: `remote: error: GH006: Protected branch update failed`

2. **Create a test PR**:
   ```bash
   git checkout -b test/branch-protection
   echo "# Test" >> README.md
   git add README.md
   git commit -m "test: verify branch protection"
   git push origin test/branch-protection
   ```

   Then create a PR on GitHub and verify:
   - All status checks run automatically
   - Merge button is disabled until checks pass
   - Review approval is required
   - Merge options show "Squash and merge" or "Rebase and merge" (not "Create a merge commit")

## Recommended GitHub Settings

### Repository Settings → General

1. **Pull Requests**:
   - ✓ Allow squash merging (recommended default)
   - ☐ Allow merge commits (disabled for linear history)
   - ✓ Allow rebase merging (alternative option)
   - ✓ Automatically delete head branches (cleans up after merging)

2. **Security**:
   - ✓ Enable Dependabot alerts
   - ✓ Enable Dependabot security updates
   - ✓ Enable secret scanning

## Optional Enhancements

### Add CODEOWNERS File

Create `.github/CODEOWNERS` to automatically request reviews from specific people:

```
# Global owners
* @your-username

# Specific areas
/.github/ @your-username @security-team
/src/security/ @security-team
/docs/ @docs-team
```

### Add Dependabot Configuration

Create `.github/dependabot.yml` for automated dependency updates:

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "your-username"
    labels:
      - "dependencies"
      - "automated"
```

### Enable GitHub Advanced Security (for public repos)

1. Go to Settings → Code security and analysis
2. Enable:
   - ✓ Dependency graph
   - ✓ Dependabot alerts
   - ✓ Dependabot security updates
   - ✓ Code scanning (CodeQL)
   - ✓ Secret scanning

## Troubleshooting

### Status checks don't appear in the list

**Problem**: You can't find the required status checks when configuring branch protection.

**Solution**:
1. Push a commit to the master branch (before protection is enabled)
2. Wait for all workflows to complete
3. The status check names will now appear in the branch protection settings

### Workflows fail with "Resource not accessible by integration"

**Problem**: GitHub Actions can't create releases or access certain APIs.

**Solution**:
1. Go to Settings → Actions → General
2. Under "Workflow permissions", select:
   - ✓ Read and write permissions
   - ✓ Allow GitHub Actions to create and approve pull requests

### Merge button is disabled even after reviews

**Problem**: Can't merge PR even with approvals and passing checks.

**Solution**:
- Ensure the branch is up to date with master (enable "Update branch" button in PR)
- Check that ALL required status checks have passed
- Verify no unresolved conversations remain

### Can't push to master in emergency

**Problem**: Need to hotfix production but branch protection blocks it.

**Solution**:
1. Create a hotfix branch
2. Make your fix
3. Create a PR
4. Use "Squash and merge" as soon as checks pass
5. This is actually SAFER than bypassing protection!

For true emergencies (site down, security breach):
1. Temporarily disable branch protection (requires admin)
2. Push fix
3. Re-enable protection immediately
4. Create a post-mortem PR with proper review

## Workflow with Branch Protection

### Standard Feature Development

```bash
# 1. Create feature branch
git checkout -b feature/your-feature-name

# 2. Make changes and commit
git add .
git commit -m "feat: add your feature"

# 3. Push to GitHub
git push origin feature/your-feature-name

# 4. Create Pull Request on GitHub
# - Fill out PR template
# - Wait for CI/CD checks to pass
# - Request review from team member
# - Address review comments
# - Squash and merge when approved
```

### Handling Review Feedback

```bash
# Make requested changes
git add .
git commit -m "fix: address review feedback"
git push origin feature/your-feature-name

# Checks will run automatically
# Get re-approval if needed
# Merge when ready
```

### Emergency Hotfix

```bash
# 1. Create hotfix branch
git checkout -b hotfix/critical-bug

# 2. Fix the issue
git add .
git commit -m "fix: critical bug in production"

# 3. Push and create PR
git push origin hotfix/critical-bug

# 4. Mark as urgent, request immediate review
# 5. Merge as soon as checks pass (1 approval minimum)
```

## Summary

With branch protection enabled, your workflow becomes:

1. ✅ **All changes require pull requests**
2. ✅ **All PRs require at least 1 approval**
3. ✅ **All tests must pass before merging**
4. ✅ **Security scans must complete**
5. ✅ **No force pushes or branch deletions**
6. ✅ **Clean, linear git history**
7. ✅ **Same rules apply to everyone**

This ensures high code quality, reduces bugs in production, and maintains a professional development workflow.

## Questions?

- GitHub Branch Protection Documentation: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches
- GitHub Rulesets (newer alternative): https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets

For project-specific questions, open an issue or discussion on the repository.
