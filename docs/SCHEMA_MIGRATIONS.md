# Schema Migrations with Alembic - Production Database Management

**Version:** 1.0.0
**Status:** REQUIRED for Production

Alembic provides **safe, version-controlled database migrations** - track schema changes, rollback safely, deploy confidently.

---

## Why Alembic?

### The Problem Without Migrations:

```python
# Bad: Direct schema changes in models.py
class Task(Base):
    # Added new field - how do you update production DB?
    priority = Column(Integer, default=0)  # 💥 Production DB doesn't have this column!
```

**Risks:**
- Schema drift between environments
- No rollback capability
- Manual SQL scripts (error-prone)
- Lost change history
- Downtime during deployments

### The Solution With Alembic:

```bash
# Generate migration automatically
alembic revision --autogenerate -m "add priority to tasks"

# Review migration file
# Edit: migrations/versions/001_add_priority_to_tasks.py

# Apply to production
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

**Benefits:**
- ✅ Version-controlled schema changes
- ✅ Automatic migration generation
- ✅ Safe rollback capability
- ✅ Environment consistency (dev/staging/prod)
- ✅ Audit trail of all changes
- ✅ Team collaboration (merge migrations in git)

---

## Setup (10 minutes)

### Step 1: Install Alembic

```bash
cd dashboard/backend
pip install alembic==1.13.1
```

### Step 2: Initialize Alembic

```bash
# Initialize Alembic (creates directory structure)
alembic init migrations

# Directory structure created:
# migrations/
#   ├── alembic.ini          # Configuration file
#   ├── env.py               # Migration environment setup
#   ├── script.py.mako       # Migration template
#   └── versions/            # Migration files go here
```

### Step 3: Configure Alembic

Edit `alembic.ini`:

```ini
# alembic.ini

# Set database URL (use async driver)
sqlalchemy.url = postgresql+asyncpg://user:password@localhost:5432/lazy_bird

# Or read from environment variable
# sqlalchemy.url =

# Enable autogenerate features
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d_%%(slug)s
```

Edit `migrations/env.py`:

```python
"""
Alembic Environment Configuration
"""
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import models for autogenerate
from models import Base
from database import DATABASE_URL

# Alembic Config object
config = context.config

# Override sqlalchemy.url from environment variable
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode (generates SQL scripts).

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # Detect column type changes
        compare_server_default=True,  # Detect default value changes
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode (applies to database).

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            # Include schemas if using PostgreSQL schemas
            # include_schemas=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Step 4: Create Initial Migration

```bash
# Generate initial migration from current models
alembic revision --autogenerate -m "initial schema"

# Output:
# Generating migrations/versions/20251110_1200_initial_schema.py ... done
```

Review generated file:

```python
# migrations/versions/20251110_1200_initial_schema.py

"""initial schema

Revision ID: abc123def456
Revises:
Create Date: 2025-11-10 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = 'abc123def456'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Apply migration changes."""
    # Create projects table
    op.create_table(
        'projects',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('project_id', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('assigned_agent', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # ... all 14 tables


def downgrade() -> None:
    """Rollback migration changes."""
    op.drop_table('tasks')
    op.drop_table('projects')
    # ... reverse order
```

### Step 5: Apply Migration

```bash
# Check current migration status
alembic current

# Apply migrations
alembic upgrade head

# Output:
# INFO  [alembic.runtime.migration] Running upgrade  -> abc123def456, initial schema
# ✅ Migration applied successfully!
```

---

## Creating Migrations

### Automatic Generation (Recommended)

```bash
# Make changes to models.py
# Example: Add priority field to Task model

# Generate migration automatically
alembic revision --autogenerate -m "add priority to tasks"

# Review generated file before applying!
cat migrations/versions/20251110_1230_add_priority_to_tasks.py
```

**Example Generated Migration:**

```python
"""add priority to tasks

Revision ID: def456ghi789
Revises: abc123def456
Create Date: 2025-11-10 12:30:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = 'def456ghi789'
down_revision = 'abc123def456'  # Previous migration
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add priority column to tasks table."""
    op.add_column(
        'tasks',
        sa.Column('priority', sa.Integer(), nullable=True, server_default='0')
    )


def downgrade() -> None:
    """Remove priority column from tasks table."""
    op.drop_column('tasks', 'priority')
```

### Manual Migrations (Advanced)

For complex migrations that can't be auto-generated:

```bash
# Create empty migration
alembic revision -m "migrate task data to new format"
```

**Example Manual Migration:**

```python
"""migrate task data to new format

Revision ID: ghi789jkl012
Revises: def456ghi789
Create Date: 2025-11-10 13:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

revision = 'ghi789jkl012'
down_revision = 'def456ghi789'


def upgrade() -> None:
    """Migrate existing task data."""
    connection = op.get_bind()

    # Add new column
    op.add_column('tasks', sa.Column('complexity_score', sa.Float(), nullable=True))

    # Migrate data (calculate complexity from existing fields)
    connection.execute(text("""
        UPDATE tasks
        SET complexity_score =
            CASE
                WHEN current_iteration > 3 THEN 0.8
                WHEN agent_switches > 2 THEN 0.7
                ELSE 0.5
            END
        WHERE complexity_score IS NULL
    """))

    # Make column non-nullable after migration
    op.alter_column('tasks', 'complexity_score', nullable=False)


def downgrade() -> None:
    """Rollback data migration."""
    op.drop_column('tasks', 'complexity_score')
```

---

## Best Practices

### 1. Small, Incremental Changes

**Good:**
```bash
# Migration 1: Add column
alembic revision --autogenerate -m "add priority column"

# Migration 2: Add index
alembic revision --autogenerate -m "add priority index"

# Migration 3: Populate data
alembic revision -m "populate priority from task type"
```

**Bad:**
```bash
# One huge migration with 50 changes
alembic revision --autogenerate -m "refactor entire schema"
```

**Why:** Small migrations are easier to review, test, and rollback.

### 2. Meaningful Migration Names

**Good:**
```bash
alembic revision -m "add_email_verification_to_users"
alembic revision -m "create_audit_log_table"
alembic revision -m "add_index_on_tasks_created_at"
```

**Bad:**
```bash
alembic revision -m "update"
alembic revision -m "fix"
alembic revision -m "changes"
```

### 3. Always Review Auto-Generated Migrations

```bash
# Generate migration
alembic revision --autogenerate -m "add task priority"

# ALWAYS review before applying!
cat migrations/versions/*_add_task_priority.py

# Check for:
# - Unwanted changes (false positives)
# - Missing changes (false negatives)
# - Data loss risks (dropping columns)
# - Performance issues (missing indexes)
```

### 4. Test Migrations Before Production

```bash
# Test on development database
alembic upgrade head

# Test rollback
alembic downgrade -1

# Test upgrade again
alembic upgrade head

# Only deploy to production after testing!
```

### 5. Backup Before Production Migrations

```bash
# PostgreSQL backup
pg_dump lazy_bird > backup_before_migration_$(date +%Y%m%d_%H%M%S).sql

# Apply migration
alembic upgrade head

# If something goes wrong:
# psql lazy_bird < backup_before_migration_20251110_120000.sql
```

### 6. Handle Data Migrations Carefully

**Example: Renaming Column with Data**

```python
def upgrade() -> None:
    """Rename status to task_status with data preservation."""
    # Step 1: Add new column
    op.add_column('tasks', sa.Column('task_status', sa.String(), nullable=True))

    # Step 2: Copy data
    op.execute("UPDATE tasks SET task_status = status")

    # Step 3: Make new column non-nullable
    op.alter_column('tasks', 'task_status', nullable=False)

    # Step 4: Drop old column
    op.drop_column('tasks', 'status')


def downgrade() -> None:
    """Restore original column name."""
    op.add_column('tasks', sa.Column('status', sa.String(), nullable=True))
    op.execute("UPDATE tasks SET status = task_status")
    op.alter_column('tasks', 'status', nullable=False)
    op.drop_column('tasks', 'task_status')
```

### 7. Use Batch Operations for SQLite

SQLite doesn't support `ALTER TABLE` for many operations. Use batch mode:

```python
def upgrade() -> None:
    """Add column using batch operations for SQLite compatibility."""
    with op.batch_alter_table('tasks') as batch_op:
        batch_op.add_column(sa.Column('priority', sa.Integer(), server_default='0'))
        batch_op.create_index('idx_tasks_priority', ['priority'])
```

### 8. Version Control Migration Files

```bash
# Add all migration files to git
git add migrations/versions/*.py

# Commit with descriptive message
git commit -m "feat: add priority field to tasks table"

# Push to remote
git push origin main
```

---

## Common Migration Patterns

### Pattern 1: Add Column

```python
def upgrade() -> None:
    op.add_column('tasks', sa.Column('estimated_tokens', sa.Integer(), nullable=True))

def downgrade() -> None:
    op.drop_column('tasks', 'estimated_tokens')
```

### Pattern 2: Add Index

```python
def upgrade() -> None:
    op.create_index('idx_tasks_created_at', 'tasks', ['created_at'])

def downgrade() -> None:
    op.drop_index('idx_tasks_created_at', table_name='tasks')
```

### Pattern 3: Add Foreign Key

```python
def upgrade() -> None:
    op.create_foreign_key(
        'fk_tasks_agent_id',
        'tasks', 'agents',
        ['assigned_agent'], ['id'],
        ondelete='RESTRICT'
    )

def downgrade() -> None:
    op.drop_constraint('fk_tasks_agent_id', 'tasks', type_='foreignkey')
```

### Pattern 4: Add Enum Type (PostgreSQL)

```python
def upgrade() -> None:
    # Create enum type
    task_status_enum = sa.Enum(
        'pending', 'running', 'completed', 'failed',
        name='task_status_enum'
    )
    task_status_enum.create(op.get_bind())

    # Add column using enum
    op.add_column('tasks', sa.Column('status', task_status_enum, nullable=False))

def downgrade() -> None:
    op.drop_column('tasks', 'status')
    sa.Enum(name='task_status_enum').drop(op.get_bind())
```

### Pattern 5: Add Unique Constraint

```python
def upgrade() -> None:
    op.create_unique_constraint('uq_projects_name', 'projects', ['name'])

def downgrade() -> None:
    op.drop_constraint('uq_projects_name', 'projects', type_='unique')
```

### Pattern 6: Rename Table

```python
def upgrade() -> None:
    op.rename_table('old_table_name', 'new_table_name')

def downgrade() -> None:
    op.rename_table('new_table_name', 'old_table_name')
```

### Pattern 7: Create Table with Relationships

```python
def upgrade() -> None:
    op.create_table(
        'task_dependencies',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('task_id', sa.String(), nullable=False),
        sa.Column('depends_on_task_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['depends_on_task_id'], ['tasks.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('task_id', 'depends_on_task_id', name='uq_task_dependency')
    )
    op.create_index('idx_task_dependencies_task_id', 'task_dependencies', ['task_id'])

def downgrade() -> None:
    op.drop_index('idx_task_dependencies_task_id', table_name='task_dependencies')
    op.drop_table('task_dependencies')
```

---

## Managing Migrations

### Check Current State

```bash
# Show current migration version
alembic current

# Output:
# abc123def456 (head)
```

### View Migration History

```bash
# Show all migrations
alembic history

# Output:
# abc123def456 -> def456ghi789 (head), add priority to tasks
# <base> -> abc123def456, initial schema
```

### Upgrade Database

```bash
# Upgrade to latest
alembic upgrade head

# Upgrade by 1 version
alembic upgrade +1

# Upgrade to specific version
alembic upgrade abc123def456
```

### Downgrade Database

```bash
# Downgrade by 1 version
alembic downgrade -1

# Downgrade to specific version
alembic downgrade abc123def456

# Downgrade to base (remove all migrations)
alembic downgrade base  # ⚠️ DANGEROUS - deletes all tables!
```

### Rollback Workflow

```bash
# Production deployment fails after migration
# Step 1: Check current state
alembic current

# Step 2: Rollback to previous version
alembic downgrade -1

# Step 3: Verify application works
curl http://localhost:1336/api/health

# Step 4: Fix migration file locally
# Step 5: Test in development
# Step 6: Deploy fixed version
```

---

## Production Deployment Workflow

### Development Environment

```bash
# 1. Make model changes
# Edit models.py

# 2. Generate migration
alembic revision --autogenerate -m "add feature X"

# 3. Review migration file
cat migrations/versions/*_add_feature_x.py

# 4. Test upgrade
alembic upgrade head

# 5. Test application
pytest tests/

# 6. Test downgrade
alembic downgrade -1

# 7. Test upgrade again
alembic upgrade head

# 8. Commit to git
git add migrations/versions/*_add_feature_x.py
git commit -m "feat: add feature X"
git push
```

### Staging Environment

```bash
# 1. Pull latest code
git pull origin main

# 2. Check migration status
alembic current

# 3. Apply migrations
alembic upgrade head

# 4. Run integration tests
pytest tests/integration/

# 5. Verify staging works
curl https://staging.example.com/api/health
```

### Production Environment

```bash
# 1. Backup database (CRITICAL!)
pg_dump lazy_bird > backup_$(date +%Y%m%d_%H%M%S).sql

# 2. Enable maintenance mode (optional)
# POST /api/admin/maintenance-mode

# 3. Pull latest code
git pull origin main

# 4. Check what migrations will run
alembic history
alembic current

# 5. Apply migrations
alembic upgrade head

# 6. Verify database state
psql lazy_bird -c "\dt"  # List tables
psql lazy_bird -c "SELECT COUNT(*) FROM tasks"  # Verify data

# 7. Restart application
systemctl restart lazy-bird-backend

# 8. Health check
curl http://localhost:1336/api/health

# 9. Disable maintenance mode
# DELETE /api/admin/maintenance-mode

# 10. Monitor logs
tail -f /var/log/lazy-bird/app.log
```

### Rollback in Production

```bash
# If something goes wrong:

# Option 1: Rollback migration
alembic downgrade -1
systemctl restart lazy-bird-backend

# Option 2: Restore from backup (if migration can't be rolled back)
psql lazy_bird < backup_20251110_120000.sql
systemctl restart lazy-bird-backend
```

---

## Migration Examples for Phantom Neural Cortex

### Example 1: Add Task Priority

```python
"""add priority to tasks

Revision ID: 001_add_priority
Revises: initial_schema
Create Date: 2025-11-10 12:00:00
"""
from alembic import op
import sqlalchemy as sa

revision = '001_add_priority'
down_revision = 'initial_schema'


def upgrade() -> None:
    """Add priority field for task scheduling."""
    op.add_column('tasks', sa.Column('priority', sa.Integer(), server_default='5', nullable=False))
    op.create_index('idx_tasks_priority', 'tasks', ['priority', 'created_at'])


def downgrade() -> None:
    """Remove priority field."""
    op.drop_index('idx_tasks_priority', table_name='tasks')
    op.drop_column('tasks', 'priority')
```

### Example 2: Add Agent Performance Tracking

```python
"""add agent performance tracking

Revision ID: 002_agent_performance
Revises: 001_add_priority
Create Date: 2025-11-10 13:00:00
"""
from alembic import op
import sqlalchemy as sa

revision = '002_agent_performance'
down_revision = '001_add_priority'


def upgrade() -> None:
    """Create agent_performance table for RL training."""
    op.create_table(
        'agent_performance',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('agent', sa.String(), nullable=False),
        sa.Column('task_type', sa.String(), nullable=False),
        sa.Column('success_rate', sa.Float(), nullable=False),
        sa.Column('avg_quality', sa.Float(), nullable=False),
        sa.Column('avg_cost', sa.Float(), nullable=False),
        sa.Column('avg_duration', sa.Float(), nullable=False),
        sa.Column('sample_count', sa.Integer(), nullable=False),
        sa.Column('last_updated', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('agent', 'task_type', name='uq_agent_task_type')
    )
    op.create_index('idx_agent_perf_agent', 'agent_performance', ['agent'])
    op.create_index('idx_agent_perf_task_type', 'agent_performance', ['task_type'])


def downgrade() -> None:
    """Remove agent performance tracking."""
    op.drop_index('idx_agent_perf_task_type', table_name='agent_performance')
    op.drop_index('idx_agent_perf_agent', table_name='agent_performance')
    op.drop_table('agent_performance')
```

### Example 3: Migrate Quality Snapshots to JSON

```python
"""migrate quality snapshots to json format

Revision ID: 003_quality_json
Revises: 002_agent_performance
Create Date: 2025-11-10 14:00:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text
import json

revision = '003_quality_json'
down_revision = '002_agent_performance'


def upgrade() -> None:
    """Migrate quality metrics to structured JSON format."""
    connection = op.get_bind()

    # Add new JSON column
    op.add_column('quality_snapshots', sa.Column('metrics_json', JSONB, nullable=True))

    # Migrate data from individual columns to JSON
    connection.execute(text("""
        UPDATE quality_snapshots
        SET metrics_json = jsonb_build_object(
            'quality', quality,
            'confidence', 0.85,
            'dimensions', jsonb_build_object(
                'correctness', quality * 0.95,
                'completeness', quality * 1.0,
                'efficiency', quality * 0.9,
                'maintainability', quality * 0.85,
                'security', quality * 0.88
            )
        )
    """))

    # Make new column non-nullable
    op.alter_column('quality_snapshots', 'metrics_json', nullable=False)

    # Drop old column (optional - keep for backward compat)
    # op.drop_column('quality_snapshots', 'quality')


def downgrade() -> None:
    """Rollback to individual quality columns."""
    connection = op.get_bind()

    # Restore quality column from JSON
    # op.add_column('quality_snapshots', sa.Column('quality', sa.Float(), nullable=True))
    # connection.execute(text("""
    #     UPDATE quality_snapshots
    #     SET quality = (metrics_json->>'quality')::float
    # """))
    # op.alter_column('quality_snapshots', 'quality', nullable=False)

    # Drop JSON column
    op.drop_column('quality_snapshots', 'metrics_json')
```

### Example 4: Add Composite Indexes for Analytics

```python
"""add composite indexes for analytics queries

Revision ID: 004_analytics_indexes
Revises: 003_quality_json
Create Date: 2025-11-10 15:00:00
"""
from alembic import op

revision = '004_analytics_indexes'
down_revision = '003_quality_json'


def upgrade() -> None:
    """Add composite indexes for common analytics queries."""
    # Tasks by project and status
    op.create_index(
        'idx_tasks_project_status',
        'tasks',
        ['project_id', 'status']
    )

    # Tasks by agent and created date (time-series queries)
    op.create_index(
        'idx_tasks_agent_created',
        'tasks',
        ['assigned_agent', 'created_at']
    )

    # Cost tracking by project and timestamp
    op.create_index(
        'idx_cost_tracking_project_ts',
        'cost_tracking',
        ['project_id', 'timestamp']
    )

    # Quality snapshots by task and iteration
    op.create_index(
        'idx_quality_snapshots_task_iter',
        'quality_snapshots',
        ['task_id', 'iteration']
    )


def downgrade() -> None:
    """Remove analytics indexes."""
    op.drop_index('idx_quality_snapshots_task_iter', table_name='quality_snapshots')
    op.drop_index('idx_cost_tracking_project_ts', table_name='cost_tracking')
    op.drop_index('idx_tasks_agent_created', table_name='tasks')
    op.drop_index('idx_tasks_project_status', table_name='tasks')
```

---

## Troubleshooting

### Issue: Migration Conflicts

**Problem:** Multiple developers create migrations simultaneously

```bash
# Developer A creates migration
alembic revision -m "add feature A"  # Revision: aaa111

# Developer B creates migration
alembic revision -m "add feature B"  # Revision: bbb222

# Both have same down_revision!
```

**Solution:** Merge migrations

```bash
# Create merge migration
alembic merge -m "merge feature A and B" aaa111 bbb222

# Output: Created merge revision ccc333
```

### Issue: Autogenerate Missed Changes

**Problem:** Alembic didn't detect your model changes

**Causes:**
- Alembic can't detect table/column renames
- Type changes may not be detected
- Custom types need manual handling

**Solution:** Create manual migration

```bash
alembic revision -m "rename column manually"
# Edit migration file manually
```

### Issue: SQLite Limitations

**Problem:** SQLite doesn't support many ALTER TABLE operations

**Solution:** Use batch operations

```python
with op.batch_alter_table('tasks') as batch_op:
    batch_op.add_column(sa.Column('new_field', sa.String()))
    batch_op.alter_column('old_field', new_column_name='renamed_field')
```

### Issue: Migration Stuck

**Problem:** `alembic upgrade head` hangs

**Causes:**
- Long-running data migration
- Database lock
- Network timeout

**Solution:**

```bash
# Check database locks (PostgreSQL)
SELECT * FROM pg_locks WHERE granted = false;

# Kill blocking query
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE query LIKE '%alembic%';

# Use transaction timeout
alembic upgrade head --sql  # Generate SQL first
# Review SQL, then apply manually with timeout
```

---

## Best Practices Checklist

Before every migration:

- [ ] Backup production database
- [ ] Test migration in development
- [ ] Test rollback in development
- [ ] Review autogenerated code
- [ ] Check for data loss risks
- [ ] Add appropriate indexes
- [ ] Consider performance impact
- [ ] Document breaking changes
- [ ] Update API docs if schema changes affect endpoints
- [ ] Schedule during maintenance window for large migrations

---

## Integration with FastAPI

### Automatic Migrations on Startup

```python
# dashboard/backend/main.py

from alembic.config import Config
from alembic import command
import logging

logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup_event():
    """Run migrations on startup (development only)."""
    if os.getenv("AUTO_MIGRATE", "false").lower() == "true":
        try:
            alembic_cfg = Config("alembic.ini")
            command.upgrade(alembic_cfg, "head")
            logger.info("Database migrations applied successfully")
        except Exception as e:
            logger.error(f"Migration failed: {e}")
            # Don't crash the application, but log the error

    # Initialize database
    await init_db_async()
```

**`.env`:**
```bash
# Enable auto-migration in development only
AUTO_MIGRATE=true  # Set to false in production!
```

### Migration Status Endpoint

```python
# dashboard/backend/routers/admin.py

from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from sqlalchemy import text

@router.get("/admin/migrations")
async def get_migration_status(db: AsyncSession = Depends(get_async_db)):
    """Get current migration status."""

    # Get current revision from database
    async with db.begin():
        result = await db.execute(text("SELECT version_num FROM alembic_version"))
        current_revision = result.scalar_one_or_none()

    # Get latest revision from migration scripts
    alembic_cfg = Config("alembic.ini")
    script = ScriptDirectory.from_config(alembic_cfg)
    head_revision = script.get_current_head()

    return {
        "current_revision": current_revision,
        "head_revision": head_revision,
        "up_to_date": current_revision == head_revision,
        "migrations_pending": current_revision != head_revision
    }
```

---

## Next Steps

1. ✅ Install Alembic
2. ✅ Initialize migrations directory
3. ✅ Configure `alembic.ini` and `env.py`
4. ✅ Generate initial migration
5. ✅ Test upgrade/downgrade locally
6. ✅ Add to production deployment workflow
7. ✅ Set up automatic backups before migrations

---

**Documentation:** https://alembic.sqlalchemy.org/en/latest/
**Tutorial:** https://alembic.sqlalchemy.org/en/latest/tutorial.html
**Cookbook:** https://alembic.sqlalchemy.org/en/latest/cookbook.html
