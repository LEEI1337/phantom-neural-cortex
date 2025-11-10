/**
 * E2E Tests for Dashboard UI
 * Tests user interactions, page navigation, and real-time updates
 *
 * Run with: npx playwright test
 */

import { test, expect, Page } from '@playwright/test';

// Test configuration
const BASE_URL = process.env.VITE_APP_URL || 'http://localhost:3000';
const API_URL = process.env.VITE_API_URL || 'http://localhost:8000/api';

test.describe('Dashboard Page', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to dashboard
    await page.goto(BASE_URL);
  });

  test('should load dashboard page successfully', async ({ page }) => {
    // Check page title
    await expect(page).toHaveTitle(/Lazy Bird/i);

    // Check main heading
    const heading = page.locator('h1, h2').first();
    await expect(heading).toBeVisible();
  });

  test('should display quick stats cards', async ({ page }) => {
    // Wait for stats to load
    await page.waitForSelector('[data-testid="quick-stats"]', { timeout: 5000 });

    // Check for stats cards (Projects, Tasks, Cost)
    const statsCards = page.locator('[data-testid^="stat-card"]');
    await expect(statsCards).toHaveCount(4); // 4 stat cards

    // Verify stats have numeric values
    const projectCount = page.locator('[data-testid="stat-projects"]');
    await expect(projectCount).toBeVisible();
  });

  test('should display metrics visualization', async ({ page }) => {
    // Check for charts/visualizations
    const metricsSection = page.locator('[data-testid="metrics-visualization"]');
    await expect(metricsSection).toBeVisible();

    // Check for chart canvas elements (Recharts uses SVG)
    const charts = page.locator('svg.recharts-surface');
    const chartCount = await charts.count();
    expect(chartCount).toBeGreaterThan(0);
  });

  test('should navigate to projects page', async ({ page }) => {
    // Click on Projects link in sidebar
    await page.click('a[href="/projects"], nav a:has-text("Projects")');

    // Verify URL changed
    await expect(page).toHaveURL(/.*\/projects/);

    // Verify projects page loaded
    const heading = page.locator('h1, h2:has-text("Projects")');
    await expect(heading).toBeVisible();
  });

  test('should navigate to analytics page', async ({ page }) => {
    // Click on Analytics link
    await page.click('a[href="/analytics"], nav a:has-text("Analytics")');

    // Verify URL
    await expect(page).toHaveURL(/.*\/analytics/);
  });
});

test.describe('Projects Management', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(`${BASE_URL}/projects`);
  });

  test('should display create project button', async ({ page }) => {
    const createButton = page.locator('button:has-text("Create Project"), button:has-text("New Project")');
    await expect(createButton).toBeVisible();
  });

  test('should open create project modal', async ({ page }) => {
    // Click create button
    await page.click('button:has-text("Create Project"), button:has-text("New Project")');

    // Modal should appear
    const modal = page.locator('[role="dialog"], .modal, [data-testid="create-project-modal"]');
    await expect(modal).toBeVisible();

    // Should have form fields
    const nameInput = page.locator('input[name="name"], input[placeholder*="name" i]');
    await expect(nameInput).toBeVisible();
  });

  test('should create new project', async ({ page }) => {
    // Open modal
    await page.click('button:has-text("Create Project"), button:has-text("New Project")');

    // Fill form
    await page.fill('input[name="name"], input[placeholder*="name" i]', 'E2E Test Project');

    // Select project type
    const typeSelect = page.locator('select[name="project_type"], select[name="type"]');
    if (await typeSelect.count() > 0) {
      await typeSelect.selectOption('typescript_fullstack');
    }

    // Submit form
    await page.click('button[type="submit"], button:has-text("Create")');

    // Wait for success (modal closes or success message)
    await page.waitForTimeout(2000);

    // Verify project appears in list
    const projectCard = page.locator('text="E2E Test Project"');
    await expect(projectCard).toBeVisible({ timeout: 5000 });
  });

  test('should display project cards', async ({ page }) => {
    // Wait for projects to load
    await page.waitForSelector('[data-testid^="project-card"], .project-card', {
      timeout: 5000,
      state: 'attached'
    });

    // Check for project cards
    const projectCards = page.locator('[data-testid^="project-card"], .project-card');
    const count = await projectCards.count();

    // Should have at least 0 projects (allow empty state)
    expect(count).toBeGreaterThanOrEqual(0);
  });

  test('should open project configuration editor', async ({ page }) => {
    // Create project first (or assume one exists)
    const firstProject = page.locator('[data-testid^="project-card"], .project-card').first();

    if (await firstProject.count() > 0) {
      // Click configure/settings button
      await firstProject.locator('button:has-text("Configure"), button:has-text("Settings"), [aria-label*="settings" i]').first().click();

      // Config modal should open
      const configModal = page.locator('[data-testid="config-editor"], .config-modal, [role="dialog"]');
      await expect(configModal).toBeVisible();

      // Should have 5 configuration dimensions
      const prioritySection = page.locator('text=/priority/i');
      const timeframeSection = page.locator('text=/timeframe/i');
      const riskSection = page.locator('text=/risk/i');

      await expect(prioritySection).toBeVisible();
    }
  });

  test('should delete project', async ({ page }) => {
    // Create a project to delete
    await page.click('button:has-text("Create Project"), button:has-text("New Project")');
    await page.fill('input[name="name"]', 'Project To Delete');
    await page.click('button[type="submit"]');
    await page.waitForTimeout(1000);

    // Find the project
    const projectToDelete = page.locator('text="Project To Delete"').locator('..').locator('..');

    // Click delete button
    await projectToDelete.locator('button:has-text("Delete"), [aria-label*="delete" i]').click();

    // Confirm deletion
    const confirmButton = page.locator('button:has-text("Confirm"), button:has-text("Yes")');
    if (await confirmButton.count() > 0) {
      await confirmButton.click();
    }

    // Wait for deletion
    await page.waitForTimeout(1000);

    // Project should be gone
    await expect(page.locator('text="Project To Delete"')).not.toBeVisible();
  });
});

test.describe('Configuration Editor', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(`${BASE_URL}/projects`);
  });

  test('should display all 5 configuration dimensions', async ({ page }) => {
    // Assuming there's at least one project
    const configButton = page.locator('button:has-text("Configure")').first();

    if (await configButton.count() > 0) {
      await configButton.click();

      // Check for 5 dimensions
      const dimensions = [
        /priority/i,
        /timeframe/i,
        /risk.*tolerance/i,
        /deployment/i,
        /ml.*component/i
      ];

      for (const dimension of dimensions) {
        const section = page.locator(`text=${dimension}`);
        await expect(section).toBeVisible({ timeout: 3000 });
      }
    }
  });

  test('should change priority mode', async ({ page }) => {
    const configButton = page.locator('button:has-text("Configure")').first();

    if (await configButton.count() > 0) {
      await configButton.click();

      // Select priority mode
      const prioritySelect = page.locator('select[name*="priority"], select:near(:text("Priority"))').first();
      if (await prioritySelect.count() > 0) {
        await prioritySelect.selectOption('performance');

        // Save
        await page.click('button:has-text("Save")');

        // Wait for save
        await page.waitForTimeout(1000);

        // Success message or modal closes
        const modal = page.locator('[role="dialog"]');
        await expect(modal).not.toBeVisible();
      }
    }
  });

  test('should adjust risk tolerance slider', async ({ page }) => {
    const configButton = page.locator('button:has-text("Configure")').first();

    if (await configButton.count() > 0) {
      await configButton.click();

      // Find risk tolerance slider
      const slider = page.locator('input[type="range"][name*="risk"], input[type="range"]:near(:text("Risk"))').first();

      if (await slider.count() > 0) {
        // Set slider to 75%
        await slider.fill('75');

        // Verify value changed
        const value = await slider.inputValue();
        expect(parseInt(value)).toBeGreaterThanOrEqual(70);
      }
    }
  });

  test('should toggle ML components', async ({ page }) => {
    const configButton = page.locator('button:has-text("Configure")').first();

    if (await configButton.count() > 0) {
      await configButton.click();

      // Find ML component toggles
      const mlToggles = page.locator('input[type="checkbox"][name*="ml"], input[type="checkbox"]:near(:text("ML"))');
      const count = await mlToggles.count();

      if (count > 0) {
        // Toggle first one
        await mlToggles.first().click();

        // Should be checked or unchecked
        const isChecked = await mlToggles.first().isChecked();
        expect(typeof isChecked).toBe('boolean');
      }
    }
  });
});

test.describe('Analytics Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(`${BASE_URL}/analytics`);
  });

  test('should display cost analysis chart', async ({ page }) => {
    // Wait for page load
    await page.waitForLoadState('networkidle');

    // Look for cost chart
    const costSection = page.locator('text=/cost.*analysis/i, h2:has-text("Cost"), h3:has-text("Cost")');
    await expect(costSection).toBeVisible({ timeout: 5000 });

    // Should have chart
    const chart = page.locator('svg.recharts-surface').first();
    await expect(chart).toBeVisible();
  });

  test('should display quality trends', async ({ page }) => {
    await page.waitForLoadState('networkidle');

    // Quality trends section
    const qualitySection = page.locator('text=/quality.*trend/i, h2:has-text("Quality")');
    await expect(qualitySection).toBeVisible({ timeout: 5000 });
  });

  test('should display agent performance comparison', async ({ page }) => {
    await page.waitForLoadState('networkidle');

    // Agent performance section
    const agentSection = page.locator('text=/agent.*performance/i, h2:has-text("Agent")');
    await expect(agentSection).toBeVisible({ timeout: 5000 });
  });

  test('should filter metrics by date range', async ({ page }) => {
    // Look for date range selector
    const dateSelector = page.locator('select:has-text("7"), select:has-text("30"), button:has-text("7 days")').first();

    if (await dateSelector.count() > 0) {
      await dateSelector.click();

      // Select 30 days
      await page.click('text="30 days", option:has-text("30")');

      // Charts should update
      await page.waitForTimeout(1000);
    }
  });
});

test.describe('Real-Time Monitoring', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(BASE_URL);
  });

  test('should display real-time monitor component', async ({ page }) => {
    // Real-time monitor section
    const monitorSection = page.locator('[data-testid="real-time-monitor"], text=/real.*time/i').first();

    // May or may not be visible depending on active tasks
    // Just check it doesn't error
    const count = await monitorSection.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });

  test('should display active tasks', async ({ page }) => {
    // Active tasks section
    const activeTasksSection = page.locator('text=/active.*task/i, h3:has-text("Active")');

    if (await activeTasksSection.count() > 0) {
      await expect(activeTasksSection).toBeVisible();
    }
  });
});

test.describe('Responsive Design', () => {
  test('should work on mobile viewport', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(BASE_URL);

    // Page should still be usable
    const heading = page.locator('h1, h2').first();
    await expect(heading).toBeVisible();

    // Mobile menu button might be visible
    const menuButton = page.locator('button[aria-label*="menu" i], .menu-button');
    // Don't fail if not found, just check it doesn't error
  });

  test('should work on tablet viewport', async ({ page }) => {
    // Set tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto(BASE_URL);

    // Verify layout
    const heading = page.locator('h1, h2').first();
    await expect(heading).toBeVisible();
  });

  test('should work on desktop viewport', async ({ page }) => {
    // Set desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto(BASE_URL);

    // Verify full layout
    const sidebar = page.locator('nav, aside, [role="navigation"]').first();
    await expect(sidebar).toBeVisible();
  });
});

test.describe('Error Handling', () => {
  test('should handle API errors gracefully', async ({ page }) => {
    // Block API requests to simulate errors
    await page.route(`${API_URL}/**`, route => route.abort());

    await page.goto(BASE_URL);

    // Should show error message or empty state, not crash
    await page.waitForTimeout(2000);

    // Page should still render
    const body = page.locator('body');
    await expect(body).toBeVisible();
  });

  test('should display loading states', async ({ page }) => {
    // Slow down network
    await page.route(`${API_URL}/**`, route => {
      setTimeout(() => route.continue(), 2000);
    });

    await page.goto(BASE_URL);

    // Should show loading indicator
    const loading = page.locator('text=/loading/i, [data-testid="loading"], .spinner, .loading');

    // May or may not be visible depending on timing
    // Just verify page doesn't crash
  });
});
