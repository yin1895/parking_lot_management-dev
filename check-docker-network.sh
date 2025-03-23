#!/bin/bash
set -e

echo "===== 检查Docker网络通信 ====="

echo "1. 检查各容器状态"
docker-compose ps

echo -e "\n2. 检查网络列表"
docker network ls

echo -e "\n3. 检查parking-network网络连接情况"
docker network inspect parking-network

echo -e "\n4. 检查后端访问数据库连接"
docker exec parking-backend curl -m 2 -s mysql:3306 || echo "正常 - 数据库端口不支持HTTP连接"

echo -e "\n5. 检查后端容器与数据库连通性"
docker exec parking-backend ping -c 2 mysql

echo -e "\n6. 测试前端API环境变量"
docker exec parking-frontend env | grep VUE_APP_API

echo -e "\n7. 测试从前端容器访问后端"
docker exec parking-frontend curl -m 2 -s backend:5000/api/health || echo "后端健康检查接口可能不存在"

echo -e "\n8. 检查后端环境变量"
docker exec parking-backend env | grep -E 'DB_|PORT|IS_DOCKER'

echo -e "\n9. 检查后端日志"
docker logs --tail 50 parking-backend

echo -e "\n===== 检查完成 ====="
exit 0
