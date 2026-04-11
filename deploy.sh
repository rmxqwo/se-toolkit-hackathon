#!/bin/bash

# 🚀 Script for quick deployment of AI Resume Builder
# Run this on your VM: bash deploy.sh

set -e  # Exit on error

echo "====================================="
echo "  AI Resume Builder - Deploy Script"
echo "====================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
echo -n "Checking Docker installation... "
if ! command -v docker &> /dev/null; then
    echo -e "${RED}FAILED${NC}"
    echo "Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/engine/install/"
    exit 1
fi
echo -e "${GREEN}OK${NC}"

# Check if Docker Compose is installed
echo -n "Checking Docker Compose installation... "
if ! command -v docker compose &> /dev/null; then
    echo -e "${RED}FAILED${NC}"
    echo "Docker Compose is not installed."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi
echo -e "${GREEN}OK${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠ .env file not found. Creating from .env.example...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠ Please edit .env file with your settings before running this script${NC}"
    echo -e "${YELLOW}  Required: QWEN_API_KEY and POSTGRES_PASSWORD${NC}"
    exit 1
fi

# Check if QWEN_API_KEY is set
if grep -q "QWEN_API_KEY=" .env && ! grep -q "QWEN_API_KEY=$" .env && ! grep -q "QWEN_API_KEY=your_api_key_here" .env; then
    echo -e "${GREEN}✓ QWEN_API_KEY is set${NC}"
else
    echo -e "${YELLOW}⚠ QWEN_API_KEY is not set or using default value${NC}"
    echo -e "${YELLOW}  Please set it in .env file${NC}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "====================================="
echo "  Starting Deployment..."
echo "====================================="
echo ""

# Stop any running containers
echo "Stopping existing containers (if any)..."
docker compose down 2>/dev/null || true

# Build and start containers
echo ""
echo "Building and starting containers..."
docker compose up -d --build

# Wait for services to start
echo ""
echo "Waiting for services to start..."
sleep 10

# Check if services are running
echo ""
echo "Checking service status..."
docker compose ps

# Wait for database to be ready
echo ""
echo -n "Waiting for database to be ready..."
for i in {1..30}; do
    if docker compose exec -T app curl -s http://localhost:8000/health &> /dev/null; then
        echo -e "${GREEN} OK${NC}"
        break
    fi
    echo -n "."
    sleep 2
done

# Final health check
echo ""
echo "Running final health check..."
if curl -f http://localhost:8000/health 2>/dev/null; then
    echo ""
    echo -e "${GREEN}=====================================${NC}"
    echo -e "${GREEN}  ✓ Deployment Successful!${NC}"
    echo -e "${GREEN}=====================================${NC}"
    echo ""
    echo "Application is running at: http://localhost:8000"
    echo ""
    echo "Useful commands:"
    echo "  View logs:         docker compose logs -f"
    echo "  Stop services:     docker compose down"
    echo "  Restart services:  docker compose restart"
    echo ""
else
    echo ""
    echo -e "${RED}=====================================${NC}"
    echo -e "${RED}  ⚠ Services may not be ready yet${NC}"
    echo -e "${RED}=====================================${NC}"
    echo ""
    echo "Check logs with: docker compose logs -f"
    echo ""
fi
