@echo off
chcp 65001 >nul
echo ===== Docker Network Check Tool =====

REM 确认Docker运行状态
echo Checking Docker status...
docker info >nul 2>&1
if %errorlevel% neq 0 (
  echo Error: Docker is not running!
  exit /b 1
)

REM 检查容器运行状态
echo.
echo 1. Checking container status
docker-compose ps
if %errorlevel% neq 0 (
  echo Error: Unable to get container status, docker-compose may not be installed or project not started
  exit /b 1
)

REM 检查网络配置，先确认现有网络
echo.
echo 2. Checking Docker networks
docker network ls 
echo.

REM 检查parking-network是否存在
echo Checking for parking-network...
docker network ls | findstr parking-network
if %errorlevel% neq 0 (
  echo Warning: parking-network not found!
  echo Creating network...
  
  REM 先删除可能存在的同名网络以避免冲突
  docker network rm parking-network >nul 2>nul
  
  REM 创建网络
  docker network create parking-network
  if %errorlevel% neq 0 (
    echo Error: Failed to create network! Check Docker permissions.
    echo Continuing with checks...
  ) else (
    echo Network created successfully.
    
    REM 重新连接容器到网络
    for %%c in (parking-db parking-backend parking-frontend) do (
      docker ps --format "{{.Names}}" | findstr %%c >nul
      if !errorlevel! equ 0 (
        echo Connecting %%c to network...
        docker network connect parking-network %%c >nul 2>nul
      )
    )
  )
)

REM 检查所有容器的网络连接
echo.
echo 3. Checking network connections
echo Running: docker network inspect parking-network
set "INSPECT_OUTPUT="
for /f "delims=" %%i in ('docker network inspect parking-network 2^>nul') do (
  set "INSPECT_OUTPUT=!INSPECT_OUTPUT!%%i"
)

if "%INSPECT_OUTPUT%"=="[]" (
  echo Network exists but has no connected containers!
  echo Attempting to connect running containers...
  
  REM 连接正在运行的容器到网络
  for %%c in (parking-db parking-backend parking-frontend) do (
    docker ps --format "{{.Names}}" | findstr %%c >nul
    if !errorlevel! equ 0 (
      echo Connecting %%c to network...
      docker network connect parking-network %%c >nul 2>nul
    )
  )
  
  REM 重新检查网络
  echo Rechecking network...
  docker network inspect parking-network
) else (
  docker network inspect parking-network >nul 2>nul || echo Network not found or not accessible.
  if %errorlevel% equ 0 (
    echo Network exists and accessible.
    echo Connected containers:
    docker network inspect -f "{{range .Containers}}{{.Name}} {{end}}" parking-network
  )
)

REM 检查是否有容器正在运行
echo.
echo 4. Testing container connectivity
docker ps --format "{{.Names}}" | findstr parking-backend >nul
if %errorlevel% neq 0 (
  echo Error: Backend container not running!
) else (
  echo Testing backend to database connection...
  docker exec parking-backend ping -c 2 mysql
  if %errorlevel% neq 0 (
    echo Error: Backend cannot connect to database!
    echo Attempting to repair...
    
    REM 确保容器在同一网络
    for %%c in (parking-db parking-backend) do (
      docker network connect parking-network %%c >nul 2>nul
    )
    
    REM 重试连接
    echo Retrying connection...
    docker exec parking-backend ping -c 2 mysql
    if %errorlevel% neq 0 (
      echo Error: Connection repair failed. DNS resolution may be broken.
      echo Container networking IPs:
      docker inspect -f "{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" parking-db parking-backend
    ) else (
      echo Success: Connection repaired!
    )
  ) else (
    echo Success: Backend can connect to database
  )
)

REM 检查前端到后端的连接
echo.
echo 5. Testing frontend to backend connection
docker ps --format "{{.Names}}" | findstr parking-frontend >nul
if %errorlevel% neq 0 (
  echo Error: Frontend container not running!
) else (
  echo Running: docker exec parking-frontend curl -s -o /dev/null -w "%%{http_code}" http://parking-backend:5000/api/health
  docker exec parking-frontend curl -s -o /dev/null -w "%%{http_code}" http://parking-backend:5000/api/health || echo Backend health check API not responding
)

REM 检查环境变量
echo.
echo 6. Checking environment variables
echo Backend environment:
docker ps --format "{{.Names}}" | findstr parking-backend >nul
if %errorlevel% neq 0 (
  echo Error: Backend container not running!
) else (
  docker exec parking-backend env | findstr /C:"DB_" /C:"PORT" /C:"IS_DOCKER"
)

echo.
echo Frontend environment:
docker ps --format "{{.Names}}" | findstr parking-frontend >nul
if %errorlevel% neq 0 (
  echo Error: Frontend container not running!
) else (
  docker exec parking-frontend env | findstr /C:"VUE_APP_API" /C:"NODE_ENV"
)

REM 检查端口映射
echo.
echo 7. Checking port mappings
docker-compose ps

echo.
echo ===== Check Complete =====
echo If problems persist, try:
echo 1. Run 'docker-compose down' then 'docker-deploy.bat'
echo 2. Check environment variables and Docker config files
echo 3. View container logs: docker logs parking-backend
echo 4. Restart Docker service

pause
