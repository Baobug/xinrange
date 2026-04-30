@echo off
chcp 65001 > nul
title XinRange - 信创渗透靶场
cd /d "%~dp0"

echo.
echo  ██████╗  █████╗ ███╗   ██╗██╗  ██╗
echo  ██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝
echo  ██║  ██║███████║██╔██╗ ██║█████╔╝
echo  ██║  ██║██╔══██║██║╚██╗██║██╔═██╗
echo  ██████╔╝██║  ██║██║ ╚████║██║  ██╗
echo  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝
echo  信创渗透学习靶场
echo.
echo [INFO] 启动 XinRange 开发服务器...
echo [INFO] 访问地址: http://localhost:8000
echo [INFO] 按 Ctrl+C 停止服务
echo.

set USE_SQLITE_DEV=True
python manage.py runserver 0.0.0.0:8000
