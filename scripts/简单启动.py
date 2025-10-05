#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最简单的启动方式
"""

import subprocess
import sys
import time
import webbrowser
import os

def main():
    print("🚀 云秒搭AI周报管理后台")
    print("=" * 40)
    
    # 检查依赖
    print("检查依赖包...")
    try:
        import flask
        import requests
        import bs4
        print("✅ 依赖包已安装")
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        print("正在安装依赖包...")
        subprocess.run([sys.executable, "-m", "pip", "install", "flask", "flask-cors", "requests", "beautifulsoup4", "lxml"])
        print("✅ 依赖包安装完成")
    
    # 启动服务器
    print("\n启动服务器...")
    print("📝 管理界面: http://localhost:8888")
    print("🔧 按 Ctrl+C 停止服务器")
    print("-" * 40)
    
    try:
        # 启动Flask服务器
        process = subprocess.Popen([sys.executable, "server.py"])
        
        # 等待服务器启动
        time.sleep(3)
        
        # 打开浏览器
        print("🌐 正在打开浏览器...")
        webbrowser.open('http://localhost:8888')
        
        # 等待用户中断
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n👋 正在停止服务器...")
            process.terminate()
            process.wait()
            print("✅ 服务器已停止")
            
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main()
