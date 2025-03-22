@echo off

:: 检查并安装依赖
echo Checking and installing dependencies...
pip install -r requirements.txt

:: 初始化数据库
echo Initializing database...
python scripts/init_db.py

:: 检查模型文件
echo Checking model files...
python scripts/migrate_models.py

:: 启动后端服务
echo Starting backend service...
start cmd /k python backend/app.py

:: 启动前端服务(如果需要)
echo Do you want to start the front-end service?(Y/N)
set /p start_frontend=
if /i "%start_frontend%"=="Y" (
    echo Starting frontend service...
    cd frontend
    start cmd /k npm start
    cd ..
)

echo DONE!
pause
