@echo off

:: 检查并安装依赖
echo 正在检查并安装依赖...
pip install -r requirements.txt

:: 初始化数据库
echo 正在初始化数据库...
python scripts/init_db.py

:: 检查模型文件
echo 正在检查模型文件...
python scripts/migrate_models.py

:: 启动后端服务
echo 正在启动后端服务...
start cmd /k python backend/app.py

:: 启动前端服务(如果需要)
echo 是否要启动前端服务？(Y/N)
set /p start_frontend=
if /i "%start_frontend%"=="Y" (
    echo 正在启动前端服务...
    cd frontend
    start cmd /k npm start
    cd ..
)

echo 服务已启动！
pause
