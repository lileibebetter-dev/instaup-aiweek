#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将文章管理后台打包成exe文件
使用PyInstaller将整个应用打包成可执行文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        print("✅ PyInstaller已安装")
        return True
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            print("✅ PyInstaller安装成功")
            return True
        except subprocess.CalledProcessError:
            print("❌ PyInstaller安装失败")
            return False

def create_spec_file():
    """创建PyInstaller配置文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['server.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('admin.html', '.'),
        ('launcher.html', '.'),
        ('posts', 'posts'),
        ('images', 'images'),
        ('styles.css', '.'),
        ('script.js', '.'),
        ('article.html', '.'),
        ('article.js', '.'),
        ('crawler.py', '.'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'flask',
        'flask_cors',
        'requests',
        'beautifulsoup4',
        'lxml',
        'json',
        'os',
        'subprocess',
        'datetime',
        'pathlib',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='云秒搭AI周报管理后台',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
    
    with open('云秒搭AI周报.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("✅ 创建PyInstaller配置文件")

def build_exe():
    """构建exe文件"""
    print("🚀 开始构建exe文件...")
    
    try:
        # 运行PyInstaller
        subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm",
            "云秒搭AI周报.spec"
        ], check=True)
        
        print("✅ exe文件构建成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return False

def create_installer():
    """创建安装包"""
    print("📦 创建安装包...")
    
    # 创建发布目录
    release_dir = Path("release")
    release_dir.mkdir(exist_ok=True)
    
    # 复制exe文件
    exe_path = Path("dist/云秒搭AI周报管理后台.exe")
    if exe_path.exists():
        shutil.copy2(exe_path, release_dir / "云秒搭AI周报管理后台.exe")
        print("✅ exe文件已复制到release目录")
    
    # 创建启动脚本
    start_script = release_dir / "启动管理后台.bat"
    with open(start_script, 'w', encoding='utf-8') as f:
        f.write('''@echo off
chcp 65001 >nul
title 云秒搭AI周报 - 文章管理后台

echo.
echo ========================================
echo    云秒搭AI周报 - 文章管理后台
echo ========================================
echo.

echo 🚀 正在启动文章管理后台...
echo 📝 管理界面: http://localhost:8080
echo 🔧 按 Ctrl+C 停止服务器
echo.

REM 启动exe文件
"云秒搭AI周报管理后台.exe"

echo.
echo 👋 服务器已停止
pause
''')
    
    # 创建README
    readme_content = '''# 云秒搭AI周报管理后台

## 使用方法

1. 双击"启动管理后台.bat"启动服务器
2. 浏览器会自动打开管理界面
3. 输入微信公众号文章链接进行抓取

## 功能特性

- 一键抓取微信公众号文章
- 自动下载图片到本地
- 自动同步到Git仓库
- 文章管理和搜索功能

## 系统要求

- Windows 10/11
- 无需安装Python环境
- 需要网络连接

## 注意事项

- 首次使用需要配置Git仓库
- 确保有足够的磁盘空间存储图片
- 建议在稳定的网络环境下使用

## 技术支持

如有问题，请检查：
1. 网络连接是否正常
2. 磁盘空间是否充足
3. 防火墙是否阻止了程序运行
'''
    
    with open(release_dir / "README.txt", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ 安装包创建完成")
    print(f"📁 发布文件位置: {release_dir.absolute()}")

def main():
    print("🔧 云秒搭AI周报管理后台 - 打包工具")
    print("=" * 50)
    
    # 检查PyInstaller
    if not check_pyinstaller():
        return
    
    # 创建配置文件
    create_spec_file()
    
    # 构建exe
    if build_exe():
        create_installer()
        print("\n🎉 打包完成！")
        print("📁 请查看release目录中的文件")
    else:
        print("\n❌ 打包失败")

if __name__ == "__main__":
    main()
