#!/bin/bash

# ProjectGen - Verification Script
# This script verifies that all components are working correctly

echo "🔍 ProjectGen Verification Script"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Docker
echo "1. Checking Docker..."
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker is installed"
    docker --version
else
    echo -e "${RED}✗${NC} Docker is not installed"
    exit 1
fi

echo ""

# Check Docker Compose
echo "2. Checking Docker Compose..."
if command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker Compose is installed"
    docker-compose --version
else
    echo -e "${RED}✗${NC} Docker Compose is not installed"
    exit 1
fi

echo ""

# Check if services are running
echo "3. Checking running services..."

services=("projectgen-postgres" "projectgen-redis" "projectgen-minio" "projectgen-backend" "projectgen-celery" "projectgen-frontend")

for service in "${services[@]}"; do
    if docker ps | grep -q $service; then
        echo -e "${GREEN}✓${NC} $service is running"
    else
        echo -e "${YELLOW}⚠${NC} $service is not running"
    fi
done

echo ""

# Check ports
echo "4. Checking port availability..."

ports=(3000 5432 6379 8000 9000 9001)
port_names=("Frontend" "PostgreSQL" "Redis" "Backend API" "MinIO" "MinIO Console")

for i in "${!ports[@]}"; do
    port=${ports[$i]}
    name=${port_names[$i]}
    
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 || netstat -an | grep -q ":$port.*LISTEN" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Port $port ($name) is in use"
    else
        echo -e "${YELLOW}⚠${NC} Port $port ($name) is not in use"
    fi
done

echo ""

# Check backend health
echo "5. Checking backend health..."
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo -e "${GREEN}✓${NC} Backend API is healthy"
else
    echo -e "${RED}✗${NC} Backend API is not responding"
fi

echo ""

# Check frontend
echo "6. Checking frontend..."
if curl -s http://localhost:3000 > /dev/null; then
    echo -e "${GREEN}✓${NC} Frontend is accessible"
else
    echo -e "${RED}✗${NC} Frontend is not accessible"
fi

echo ""

# Check environment file
echo "7. Checking environment configuration..."
if [ -f ".env" ]; then
    echo -e "${GREEN}✓${NC} .env file exists"
    
    # Check for required variables
    required_vars=("GROQ_API_KEY" "JWT_SECRET_KEY" "DATABASE_URL")
    
    for var in "${required_vars[@]}"; do
        if grep -q "^$var=" .env; then
            echo -e "${GREEN}✓${NC} $var is configured"
        else
            echo -e "${YELLOW}⚠${NC} $var is not configured"
        fi
    done
else
    echo -e "${RED}✗${NC} .env file not found. Copy .env.example to .env"
fi

echo ""

# Summary
echo "=================================="
echo "Verification Complete!"
echo ""
echo "Next steps:"
echo "1. If services are not running: docker-compose up --build"
echo "2. Access frontend: http://localhost:3000"
echo "3. Access API docs: http://localhost:8000/docs"
echo "4. Access MinIO console: http://localhost:9001"
echo ""
echo "For detailed instructions, see QUICKSTART.md"
