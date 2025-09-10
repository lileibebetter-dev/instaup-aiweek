#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动文章管理后台
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """检查依赖包"""
    required_packages = ['flask', 'flask_cors', 'requests', 'beautifulsoup4']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ 缺少以下依赖包:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n请运行以下命令安装依赖:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def start_server():
    """启动服务器"""
    print("🚀 正在启动文章管理后台...")
    
    # 检查依赖
    if not check_dependencies():
        return False
    
    # 启动服务器
    try:
        print("📝 管理界面: http://localhost:5000")
        print("🔧 按 Ctrl+C 停止服务器")
        print("-" * 50)
        
        # 延迟打开浏览器
        def open_browser():
            time.sleep(2)
            webbrowser.open('http://localhost:5000')
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # 启动Flask服务器
        subprocess.run([sys.executable, 'server.py'])
        
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False
    
    return True

if __name__ == '__main__':
    start_server()
