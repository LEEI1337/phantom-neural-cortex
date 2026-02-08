# Phantom Neural Cortex - Isolated Skill Runner
FROM python:3.11-slim

# Security: Create non-root user
RUN groupadd -r phantom && useradd -r -g phantom phantom

WORKDIR /app

# Install base dependencies for skills
# (In production, this would be more extensive or dynamic)
COPY requirements-base.txt .
RUN pip install --no-cache-dir -r requirements-base.txt || true

# Copy bridge script and core base classes
COPY bridge.py .
COPY core/ /app/core/
COPY skills/base.py /app/skills/base.py

# Set permissions
RUN chown -r phantom:phantom /app
USER phantom

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Entrypoint will be provided by the Host Sandbox Manager
ENTRYPOINT ["python", "bridge.py"]
