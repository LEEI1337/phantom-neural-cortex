FROM python:3.12-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl && \
    rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Gateway port
EXPOSE 18789

CMD ["python", "-m", "uvicorn", "gateway.server:app", "--host", "0.0.0.0", "--port", "18789"]
