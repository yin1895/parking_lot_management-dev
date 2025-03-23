#!/bin/bash
set -e

echo "===== Docker Network Check Tool ====="

# 确认Docker运行状态
echo "Checking Docker status..."
docker info >/dev/null 2>&1 || { echo "Error: Docker is not running!"; exit 1; }

# 检查容器运行状态
echo -e "\n1. Checking container status"
docker-compose ps
if [ $? -ne 0 ]; then
  echo "Error: Unable to get container status, docker-compose may not be installed or project not started"
  exit 1
fi

# 检查网络配置
echo -e "\n2. Checking Docker networks"
docker network ls
echo -e "\nChecking for parking-network..."
docker network ls | grep parking-network
if [ $? -ne 0 ]; then
  echo "Warning: parking-network not found!"
  echo "Creating network..."
  docker network create parking-network
  if [ $? -ne 0 ]; then
    echo "Error: Failed to create network! Check Docker permissions."
  else
    echo "Network created successfully."
  fi
fi

# 检查所有容器的网络连接
echo -e "\n3. Checking network connections"
echo "Running: docker network inspect parking-network"
docker network inspect parking-network 2>/dev/null || echo "Network not found or not accessible."

# 检查是否有容器正在运行
echo -e "\n4. Testing container connectivity"
docker ps --format "{{.Names}}" | grep parking-backend >/dev/null
if [ $? -ne 0 ]; then
  echo "Error: Backend container not running!"
else
  echo "Testing backend to database connection..."
  docker exec parking-backend ping -c 2 mysql
  if [ $? -ne 0 ]; then
    echo "Error: Backend cannot connect to database!"
  else
    echo "Success: Backend can connect to database"
  fi
fi

# 检查前端到后端的连接
echo -e "\n5. Testing frontend to backend connection"
docker ps --format "{{.Names}}" | grep parking-frontend >/dev/null
if [ $? -ne 0 ]; then
  echo "Error: Frontend container not running!"
else
  echo "Running: docker exec parking-frontend curl -s -o /dev/null -w '%{http_code}' http://parking-backend:5000/api/health"
  docker exec parking-frontend curl -s -o /dev/null -w "%{http_code}" http://parking-backend:5000/api/health || echo "Backend health check API not responding"
fi

# 检查环境变量
echo -e "\n6. Checking environment variables"
echo "Backend environment:"
docker ps --format "{{.Names}}" | grep parking-backend >/dev/null
if [ $? -ne 0 ]; then
  echo "Error: Backend container not running!"
else
  docker exec parking-backend env | grep -E 'DB_|PORT|IS_DOCKER'
fi

echo -e "\nFrontend environment:"
docker ps --format "{{.Names}}" | grep parking-frontend >/dev/null
if [ $? -ne 0 ]; then
  echo "Error: Frontend container not running!"
else
  docker exec parking-frontend env | grep -E 'VUE_APP_API|NODE_ENV'
fi

# 检查端口映射
echo -e "\n7. Checking port mappings"
docker-compose ps

echo -e "\n===== Check Complete ====="
echo "If problems persist, try:"
echo "1. Restart Docker service"
echo "2. Run 'docker-compose down' then 'docker-compose up -d'"
echo "3. Check environment variables and Docker config files"
echo "4. View container logs: docker logs parking-backend"
