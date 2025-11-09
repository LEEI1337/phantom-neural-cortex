#!/bin/bash
# Multi-Platform Docker Build Script for Lazy Bird
# Builds images for linux/amd64, linux/arm64

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="lazy-bird"
IMAGE_TAG="${IMAGE_TAG:-latest}"
REGISTRY="${DOCKER_REGISTRY:-docker.io}"
PLATFORMS="linux/amd64,linux/arm64"
BUILD_TARGET="${BUILD_TARGET:-production}"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Lazy Bird Multi-Platform Build${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Image: ${YELLOW}${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}${NC}"
echo -e "Platforms: ${YELLOW}${PLATFORMS}${NC}"
echo -e "Target: ${YELLOW}${BUILD_TARGET}${NC}"
echo ""

# Step 1: Check prerequisites
echo -e "${GREEN}[1/5] Checking prerequisites...${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: docker is not installed${NC}"
    exit 1
fi

if ! docker buildx version &> /dev/null; then
    echo -e "${RED}Error: docker buildx is not available${NC}"
    echo "Please install buildx: https://docs.docker.com/buildx/working-with-buildx/"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites satisfied${NC}"
echo ""

# Step 2: Create buildx builder
echo -e "${GREEN}[2/5] Creating buildx builder...${NC}"

BUILDER_NAME="lazy-bird-builder"

if docker buildx inspect ${BUILDER_NAME} &> /dev/null; then
    echo "Builder ${BUILDER_NAME} already exists"
else
    docker buildx create --name ${BUILDER_NAME} --driver docker-container --bootstrap
    echo -e "${GREEN}✓ Created builder: ${BUILDER_NAME}${NC}"
fi

docker buildx use ${BUILDER_NAME}
echo ""

# Step 3: Login to registry (if credentials provided)
if [ -n "${DOCKER_USERNAME}" ] && [ -n "${DOCKER_PASSWORD}" ]; then
    echo -e "${GREEN}[3/5] Logging into registry...${NC}"
    echo "${DOCKER_PASSWORD}" | docker login ${REGISTRY} -u "${DOCKER_USERNAME}" --password-stdin
    echo -e "${GREEN}✓ Logged in to ${REGISTRY}${NC}"
else
    echo -e "${YELLOW}[3/5] Skipping registry login (no credentials provided)${NC}"
fi
echo ""

# Step 4: Build multi-platform image
echo -e "${GREEN}[4/5] Building multi-platform image...${NC}"
echo "This may take several minutes..."
echo ""

docker buildx build \
    --platform ${PLATFORMS} \
    --target ${BUILD_TARGET} \
    --tag ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} \
    --tag ${REGISTRY}/${IMAGE_NAME}:latest \
    --file Dockerfile.multiplatform \
    --push \
    --progress=plain \
    .

echo ""
echo -e "${GREEN}✓ Build completed successfully${NC}"
echo ""

# Step 5: Verify images
echo -e "${GREEN}[5/5] Verifying images...${NC}"

docker buildx imagetools inspect ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Build Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Images built for:"
echo "  - linux/amd64"
echo "  - linux/arm64"
echo ""
echo "Image: ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
echo ""
echo "To deploy:"
echo "  docker-compose -f docker-compose.multiplatform.yml up -d"
echo "  OR"
echo "  kubectl apply -f deploy/kubernetes/deployment.yaml"
echo ""
