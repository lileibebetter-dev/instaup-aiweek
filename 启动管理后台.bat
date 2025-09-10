@echo off
chcp 65001 >nul
title 云秒搭AI周报 - 文章管理后台

echo.
echo ========================================
echo    云秒搭AI周报 - 文章管理后台
echo ========================================
echo.

echo [1/3] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python环境正常

echo.
echo [2/3] 安装依赖包...
pip install flask flask-cors requests beautifulsoup4 lxml >nul 2>&1
if errorlevel 1 (
    echo ⚠️  依赖包安装可能有问题，但继续尝试启动...
) else (
    echo ✅ 依赖包检查完成
)

echo.
echo [3/3] 启动服务器...
echo.
echo 🚀 正在启动文章管理后台...
echo 📝 管理界面: http://localhost:8080
echo 🔧 按 Ctrl+C 停止服务器
echo.
echo ⏳ 请稍候，正在启动服务器...
echo.

REM 启动Flask服务器
python server.py

echo.
echo 👋 服务器已停止
pause
