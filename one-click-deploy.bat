@echo off

echo ===== Parking Lot Management System - One-click Deployment Tool =====

REM Set Docker Hub username (input yinth)
echo Please enter your Docker Hub username:
set /p dockerhub_username=Username:

REM Check if Docker is installed
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Docker is not installed! Please install Docker Desktop or Docker Engine first.
    exit /b 1
)

REM Check if docker-compose is installed
where docker-compose >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: docker-compose is not installed! Please install docker-compose first.
    exit /b 1
)

echo Creating Docker network...
docker network create parking-network >nul 2>nul

echo Creating docker-compose.yml file...
(
echo version: '3.8'
echo.
echo services:
echo   mysql:
echo     image: mysql:5.7
echo     container_name: parking-db
echo     restart: always
echo     environment:
echo       MYSQL_DATABASE: parking_management
echo       MYSQL_USER: root
echo       MYSQL_ROOT_PASSWORD: 123456
echo       TZ: Asia/Shanghai
echo     ports:
echo       - "3307:3306"
echo     volumes:
echo       - mysql-data:/var/lib/mysql
echo       - ./mysql-init:/docker-entrypoint-initdb.d
echo     healthcheck:
echo       test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-p123456"]
echo       interval: 5s
echo       timeout: 5s
echo       retries: 5
echo     networks:
echo       - parking-network
echo.
echo   backend:
echo     image: %dockerhub_username%/parking-backend:latest
echo     container_name: parking-backend
echo     restart: always
echo     depends_on:
echo       mysql:
echo         condition: service_healthy
echo     environment:
echo       - DB_HOST=mysql
echo       - DB_PORT=3306
echo       - DB_NAME=parking_management
echo       - DB_USER=root
echo       - DB_PASSWORD=123456
echo       - JWT_SECRET_KEY=parkingsecretkey12345
echo       - IS_DOCKER=1
echo     ports:
echo       - "5001:5000"
echo     networks:
echo       - parking-network
echo.
echo   frontend:
echo     image: %dockerhub_username%/parking-frontend:latest
echo     container_name: parking-frontend
echo     restart: always
echo     depends_on:
echo       - backend
echo     ports:
echo       - "8080:80"
echo     networks:
echo       - parking-network
echo.
echo networks:
echo   parking-network:
echo     driver: bridge
echo.
echo volumes:
echo   mysql-data:
) > docker-compose.yml

echo Starting services...
docker-compose up -d

echo.
echo Deployment completed! The system will be running at:
echo Frontend: http://localhost:8080
echo Backend API: http://localhost:5001/api

pause
