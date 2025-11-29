@echo off

REM 检查并激活虚拟环境
if exist "venv\Scripts\activate" (
    echo 激活虚拟环境...
    call venv\Scripts\activate
)

REM 安装依赖
echo 安装依赖...
pip install -r requirements.txt

REM 数据库迁移
echo 执行数据库迁移...
python manage.py migrate

REM 启动服务器
echo 启动开发服务器...
python manage.py runserver 0.0.0.0:8000