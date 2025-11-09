# Lazy Bird - Cross-Platform Deployment Guide

Complete deployment guide for Windows, Linux (amd64/arm64), macOS, and Kubernetes.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Platform-Specific Instructions](#platform-specific-instructions)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Production Considerations](#production-considerations)
6. [Troubleshooting](#troubleshooting)

## Quick Start

### Prerequisites

- Docker 20.10+ with BuildX support
- Docker Compose 2.0+
- 4GB RAM minimum
- 10GB disk space

### One-Command Deploy

```bash
# Clone repository
git clone https://github.com/your-org/lazy-bird.git
cd lazy-bird

# Deploy with Docker Compose
docker-compose -f docker-compose.multiplatform.yml up -d

# Access
# - Application: http://localhost:8000
# - Grafana: http://localhost:3001 (admin/admin)
# - Prometheus: http://localhost:9090
```

## Platform-Specific Instructions

### Windows (amd64)

#### Using Docker Desktop

1. **Install Docker Desktop**
   ```powershell
   # Download from https://www.docker.com/products/docker-desktop
   # Enable WSL 2 backend
   ```

2. **Enable BuildX**
   ```powershell
   docker buildx install
   docker buildx create --use
   ```

3. **Deploy**
   ```powershell
   cd lazy-bird
   $env:PLATFORM="windows/amd64"
   docker-compose -f docker-compose.multiplatform.yml up -d
   ```

#### Using Windows Containers (Native)

```powershell
# Switch to Windows containers in Docker Desktop
# Build Windows-specific image
docker build -t lazy-bird:windows -f Dockerfile.windows .
```

### Linux (amd64)

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y docker.io docker-compose-plugin

# Enable and start Docker
sudo systemctl enable docker
sudo systemctl start docker

# Deploy
cd lazy-bird
export PLATFORM="linux/amd64"
docker-compose -f docker-compose.multiplatform.yml up -d
```

### Linux (arm64) - Raspberry Pi / ARM Servers

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Enable experimental features for BuildX
sudo mkdir -p /etc/docker
echo '{"experimental": true}' | sudo tee /etc/docker/daemon.json
sudo systemctl restart docker

# Deploy
cd lazy-bird
export PLATFORM="linux/arm64"
docker-compose -f docker-compose.multiplatform.yml up -d
```

### macOS (Apple Silicon M1/M2/M3)

```bash
# Install Docker Desktop for Mac (ARM64)
# Download from https://www.docker.com/products/docker-desktop

# Deploy
cd lazy-bird
export PLATFORM="linux/arm64"
docker-compose -f docker-compose.multiplatform.yml up -d
```

### macOS (Intel)

```bash
# Install Docker Desktop for Mac (Intel)
cd lazy-bird
export PLATFORM="linux/amd64"
docker-compose -f docker-compose.multiplatform.yml up -d
```

## Docker Deployment

### Building Multi-Platform Images

```bash
# Build for all platforms
chmod +x deploy/build-multiplatform.sh
./deploy/build-multiplatform.sh

# Build for specific platforms
export PLATFORMS="linux/amd64,linux/arm64"
export IMAGE_TAG="v2.0.0"
export BUILD_TARGET="production"
./deploy/build-multiplatform.sh
```

### Push to Registry

```bash
# Docker Hub
export DOCKER_REGISTRY="docker.io"
export DOCKER_USERNAME="your-username"
export DOCKER_PASSWORD="your-password"
./deploy/build-multiplatform.sh

# GitHub Container Registry
export DOCKER_REGISTRY="ghcr.io"
export DOCKER_USERNAME="github-username"
export DOCKER_PASSWORD="github-token"
./deploy/build-multiplatform.sh

# AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com
export DOCKER_REGISTRY="123456789.dkr.ecr.us-east-1.amazonaws.com"
./deploy/build-multiplatform.sh
```

### Development Mode

```bash
# Build development image with hot-reload
docker build --target development -t lazy-bird:dev -f Dockerfile.multiplatform .

# Run with volume mounts for live editing
docker run -it --rm \
  -v $(pwd)/lazy-bird:/app/lazy-bird \
  -v $(pwd)/dashboard/backend:/app/dashboard/backend \
  -p 8000:8000 \
  lazy-bird:dev
```

## Kubernetes Deployment

### Prerequisites

- Kubernetes 1.25+
- kubectl configured
- 8GB RAM across cluster
- 50GB storage

### Deploy to Kubernetes

```bash
# Apply all resources
kubectl apply -f deploy/kubernetes/deployment.yaml

# Check deployment status
kubectl get pods -n lazy-bird -w

# Get service URLs
kubectl get svc -n lazy-bird

# Access application
kubectl port-forward -n lazy-bird svc/lazy-bird-service 8000:80
```

### Minikube (Local Testing)

```bash
# Start Minikube
minikube start --cpus=4 --memory=8192

# Build image in Minikube
eval $(minikube docker-env)
docker build -t lazy-bird:latest -f Dockerfile.multiplatform .

# Deploy
kubectl apply -f deploy/kubernetes/deployment.yaml

# Access services
minikube service lazy-bird-service -n lazy-bird
minikube service grafana-service -n lazy-bird
```

### AWS EKS

```bash
# Create EKS cluster
eksctl create cluster --name lazy-bird --region us-east-1 --nodes 3

# Deploy
kubectl apply -f deploy/kubernetes/deployment.yaml

# Get LoadBalancer URL
kubectl get svc lazy-bird-service -n lazy-bird -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```

### Google GKE

```bash
# Create GKE cluster
gcloud container clusters create lazy-bird --num-nodes=3 --machine-type=n1-standard-4

# Get credentials
gcloud container clusters get-credentials lazy-bird

# Deploy
kubectl apply -f deploy/kubernetes/deployment.yaml
```

### Azure AKS

```bash
# Create AKS cluster
az aks create --resource-group lazy-bird-rg --name lazy-bird --node-count 3

# Get credentials
az aks get-credentials --resource-group lazy-bird-rg --name lazy-bird

# Deploy
kubectl apply -f deploy/kubernetes/deployment.yaml
```

## Production Considerations

### Security

1. **Change Default Passwords**
   ```bash
   # Edit docker-compose.multiplatform.yml
   POSTGRES_PASSWORD: <secure-password>
   GRAFANA_PASSWORD: <secure-password>
   ```

2. **Use TLS/SSL**
   ```yaml
   # Add to Ingress
   tls:
     - hosts:
         - lazy-bird.example.com
       secretName: lazy-bird-tls
   ```

3. **Enable Authentication**
   ```python
   # Add to backend/main.py
   from fastapi_jwt_auth import AuthJWT
   ```

### Performance Tuning

1. **Database Optimization**
   ```yaml
   # PostgreSQL config
   POSTGRES_SHARED_BUFFERS: 512MB
   POSTGRES_EFFECTIVE_CACHE_SIZE: 2GB
   POSTGRES_MAX_CONNECTIONS: 200
   ```

2. **Redis Tuning**
   ```yaml
   # Redis config
   maxmemory: 1gb
   maxmemory-policy: allkeys-lru
   ```

3. **Application Scaling**
   ```yaml
   # Horizontal scaling
   replicas: 5
   resources:
     limits:
       cpu: "4"
       memory: "4Gi"
   ```

### Monitoring

1. **Prometheus Retention**
   ```yaml
   --storage.tsdb.retention.time=90d
   --storage.tsdb.retention.size=100GB
   ```

2. **Grafana Alerts**
   - Configure Slack/Email notifications
   - Set up alert rules in `monitoring/alerts.yml`

3. **Logging**
   ```bash
   # ELK Stack integration
   docker run -d \
     --name filebeat \
     -v /var/lib/docker/containers:/var/lib/docker/containers:ro \
     elastic/filebeat:8.11.0
   ```

### Backup Strategy

1. **Database Backup**
   ```bash
   # Automated daily backups
   docker exec lazy-bird-db pg_dump -U lazybird lazybird > backup_$(date +%Y%m%d).sql
   ```

2. **Volume Backup**
   ```bash
   # Backup Docker volumes
   docker run --rm -v lazy-bird_postgres_data:/data -v $(pwd)/backups:/backup ubuntu tar czf /backup/postgres_backup.tar.gz /data
   ```

## Troubleshooting

### Common Issues

#### 1. Platform Mismatch

**Problem**: "exec format error" when running container

**Solution**:
```bash
# Check your platform
uname -m

# Rebuild for correct platform
docker buildx build --platform linux/$(uname -m) -t lazy-bird:latest .
```

#### 2. BuildX Not Available

**Problem**: "buildx: command not found"

**Solution**:
```bash
# Linux
mkdir -p ~/.docker/cli-plugins
wget https://github.com/docker/buildx/releases/download/v0.12.0/buildx-v0.12.0.linux-amd64
mv buildx-v0.12.0.linux-amd64 ~/.docker/cli-plugins/docker-buildx
chmod +x ~/.docker/cli-plugins/docker-buildx
```

#### 3. Memory Issues

**Problem**: Container crashes with OOM

**Solution**:
```bash
# Increase Docker memory limit
# Docker Desktop → Settings → Resources → Memory: 8GB

# Or limit per container
docker-compose up -d --scale lazy-bird-app=1 --memory=2g
```

#### 4. Database Connection Failed

**Problem**: "connection refused" to PostgreSQL

**Solution**:
```bash
# Check database is running
docker-compose ps database

# Check health
docker exec lazy-bird-db pg_isready -U lazybird

# View logs
docker-compose logs database
```

#### 5. Port Already in Use

**Problem**: "bind: address already in use"

**Solution**:
```bash
# Find process using port
lsof -i :8000

# Change port in docker-compose.yml
ports:
  - "8001:8000"
```

### Debug Mode

```bash
# Run with debug logging
docker-compose -f docker-compose.multiplatform.yml up

# Exec into container
docker exec -it lazy-bird-app bash

# Check environment
docker exec lazy-bird-app env

# View application logs
docker logs -f lazy-bird-app
```

### Health Checks

```bash
# Application health
curl http://localhost:8000/api/health

# Metrics endpoint
curl http://localhost:8000/api/metrics

# Database health
docker exec lazy-bird-db pg_isready -U lazybird
```

## Support

- Documentation: `/docs`
- Issues: https://github.com/your-org/lazy-bird/issues
- Discussions: https://github.com/your-org/lazy-bird/discussions
