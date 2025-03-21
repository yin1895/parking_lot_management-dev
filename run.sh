#!/bin/bash

# 激活虚拟环境(如果使用)
# source venv/bin/activate

# 检查并安装依赖
echo "正在检查并安装依赖..."
pip install -r requirements.txt

# 初始化数据库
echo "正在初始化数据库..."
python scripts/init_db.py

# 检查模型文件
echo "正在检查模型文件..."
python scripts/migrate_models.py

# 启动后端服务
echo "正在启动后端服务..."
python backend/app.py &
BACKEND_PID=$!

# 询问是否启动前端
read -p "是否要启动前端服务？(y/n) " start_frontend
if [[ $start_frontend == "y" || $start_frontend == "Y" ]]; then
    echo "正在启动前端服务..."
    cd frontend
    npm start &
    FRONTEND_PID=$!
    cd ..
fi

echo "按 Ctrl+C 停止服务"
wait $BACKEND_PID
