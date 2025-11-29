#!/bin/bash

# 激活虚拟环境（如果存在）
if [ -d "venv" ]; then
    echo "激活虚拟环境..."
    source venv/bin/activate
fi

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 数据库迁移
echo "执行数据库迁移..."
python manage.py migrate

# 创建超级用户（如果需要）
echo "检查是否需要创建超级用户..."
python manage.py createsuperuser --noinput || echo "超级用户已存在或无法创建"

# 启动服务器
echo "启动开发服务器..."
python manage.py runserver 0.0.0.0:8000