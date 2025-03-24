import os
import sys
import requests 

def migrate_models():
    """下载或检查权重文件"""
    # 目标文件路径
    dst_dir = r"D:\parking_lot_management-dev\backend\weights"
    
    # 在Docker环境中修改路径
    if os.path.exists('/app/backend/weights'):
        dst_dir = '/app/backend/weights'
    
    # 确保目标目录存在
    os.makedirs(dst_dir, exist_ok=True)
    
    # 需要的权重文件
    weights_files = ['plate_detect.onnx', 'plate_rec_color.onnx']
    for file in weights_files:
        dst_file = os.path.join(dst_dir, file)
        
        # 检查文件是否已存在
        if os.path.exists(dst_file):
            print(f"权重文件 {file} 已存在")
        else:
            print(f"警告: 未找到权重文件 {dst_file}")
            print(f"请从官方仓库下载并放入 {dst_dir} 目录")

if __name__ == "__main__":
    migrate_models()
