#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图形化启动器
提供简单的GUI界面来启动管理后台
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import webbrowser
import subprocess
import sys
import os
import time
import requests
from pathlib import Path

class AdminLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("云秒搭AI周报 - 管理后台启动器")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # 设置窗口图标和样式
        self.root.configure(bg='#f0f0f0')
        
        # 服务器进程
        self.server_process = None
        self.server_running = False
        
        self.create_widgets()
        self.check_dependencies()
    
    def create_widgets(self):
        """创建界面组件"""
        # 标题
        title_frame = tk.Frame(self.root, bg='#f0f0f0')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame, 
            text="🚀 云秒搭AI周报管理后台", 
            font=("Microsoft YaHei", 20, "bold"),
            fg='#2c3e50',
            bg='#f0f0f0'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="文章管理后台启动器",
            font=("Microsoft YaHei", 12),
            fg='#7f8c8d',
            bg='#f0f0f0'
        )
        subtitle_label.pack()
        
        # 状态显示
        status_frame = tk.LabelFrame(
            self.root, 
            text="系统状态", 
            font=("Microsoft YaHei", 10, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        status_frame.pack(pady=20, padx=20, fill='x')
        
        self.status_text = scrolledtext.ScrolledText(
            status_frame, 
            height=8, 
            font=("Consolas", 9),
            bg='#2c3e50',
            fg='#ecf0f1',
            insertbackground='#ecf0f1'
        )
        self.status_text.pack(pady=10, padx=10, fill='both', expand=True)
        
        # 按钮区域
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        self.start_btn = tk.Button(
            button_frame,
            text="🚀 启动管理后台",
            font=("Microsoft YaHei", 12, "bold"),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=10,
            command=self.start_server,
            cursor='hand2'
        )
        self.start_btn.pack(side='left', padx=10)
        
        self.stop_btn = tk.Button(
            button_frame,
            text="⏹️ 停止服务器",
            font=("Microsoft YaHei", 12, "bold"),
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=10,
            command=self.stop_server,
            state='disabled',
            cursor='hand2'
        )
        self.stop_btn.pack(side='left', padx=10)
        
        self.open_btn = tk.Button(
            button_frame,
            text="📝 打开管理界面",
            font=("Microsoft YaHei", 12, "bold"),
            bg='#27ae60',
            fg='white',
            padx=20,
            pady=10,
            command=self.open_admin,
            state='disabled',
            cursor='hand2'
        )
        self.open_btn.pack(side='left', padx=10)
        
        # 进度条
        self.progress = ttk.Progressbar(
            self.root, 
            mode='indeterminate',
            length=400
        )
        self.progress.pack(pady=10)
        
        # 状态标签
        self.status_label = tk.Label(
            self.root,
            text="准备就绪",
            font=("Microsoft YaHei", 10),
            fg='#27ae60',
            bg='#f0f0f0'
        )
        self.status_label.pack(pady=5)
    
    def log(self, message):
        """添加日志信息"""
        self.status_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.status_text.see(tk.END)
        self.root.update()
    
    def check_dependencies(self):
        """检查依赖"""
        self.log("检查Python环境...")
        self.log(f"Python版本: {sys.version}")
        
        self.log("检查依赖包...")
        required_packages = ['flask', 'flask_cors', 'requests', 'beautifulsoup4', 'lxml']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                self.log(f"✅ {package}")
            except ImportError:
                missing_packages.append(package)
                self.log(f"❌ {package}")
        
        if missing_packages:
            self.log(f"缺少依赖包: {', '.join(missing_packages)}")
            self.log("正在安装依赖包...")
            self.install_dependencies(missing_packages)
        else:
            self.log("✅ 所有依赖包已安装")
            self.status_label.config(text="依赖检查完成", fg='#27ae60')
    
    def install_dependencies(self, packages):
        """安装依赖包"""
        try:
            for package in packages:
                self.log(f"安装 {package}...")
                subprocess.run([
                    sys.executable, "-m", "pip", "install", package
                ], check=True, capture_output=True)
                self.log(f"✅ {package} 安装成功")
            
            self.log("✅ 所有依赖包安装完成")
            self.status_label.config(text="依赖安装完成", fg='#27ae60')
        except subprocess.CalledProcessError as e:
            self.log(f"❌ 依赖安装失败: {e}")
            self.status_label.config(text="依赖安装失败", fg='#e74c3c')
    
    def start_server(self):
        """启动服务器"""
        if self.server_running:
            return
        
        self.log("正在启动服务器...")
        self.status_label.config(text="正在启动服务器...", fg='#f39c12')
        self.progress.start()
        self.start_btn.config(state='disabled')
        
        # 在新线程中启动服务器
        thread = threading.Thread(target=self._start_server_thread)
        thread.daemon = True
        thread.start()
    
    def _start_server_thread(self):
        """启动服务器线程"""
        try:
            # 启动Flask服务器
            self.server_process = subprocess.Popen([
                sys.executable, "server.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # 等待服务器启动
            time.sleep(3)
            
            # 检查服务器是否启动成功
            if self.check_server_status():
                self.server_running = True
                self.root.after(0, self._server_started)
            else:
                self.root.after(0, self._server_failed)
                
        except Exception as e:
            self.root.after(0, lambda: self._server_error(str(e)))
    
    def check_server_status(self):
        """检查服务器状态"""
        try:
            response = requests.get('http://localhost:8080/api/articles', timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _server_started(self):
        """服务器启动成功"""
        self.log("✅ 服务器启动成功")
        self.log("📝 管理界面: http://localhost:8080")
        self.status_label.config(text="服务器运行中", fg='#27ae60')
        self.progress.stop()
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.open_btn.config(state='normal')
        
        # 自动打开浏览器
        self.open_admin()
    
    def _server_failed(self):
        """服务器启动失败"""
        self.log("❌ 服务器启动失败")
        self.status_label.config(text="服务器启动失败", fg='#e74c3c')
        self.progress.stop()
        self.start_btn.config(state='normal')
        messagebox.showerror("错误", "服务器启动失败，请检查端口是否被占用")
    
    def _server_error(self, error):
        """服务器启动错误"""
        self.log(f"❌ 服务器启动错误: {error}")
        self.status_label.config(text="服务器启动错误", fg='#e74c3c')
        self.progress.stop()
        self.start_btn.config(state='normal')
        messagebox.showerror("错误", f"服务器启动错误: {error}")
    
    def stop_server(self):
        """停止服务器"""
        if not self.server_running:
            return
        
        self.log("正在停止服务器...")
        self.status_label.config(text="正在停止服务器...", fg='#f39c12')
        
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None
        
        self.server_running = False
        self.log("✅ 服务器已停止")
        self.status_label.config(text="服务器已停止", fg='#e74c3c')
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.open_btn.config(state='disabled')
    
    def open_admin(self):
        """打开管理界面"""
        try:
            webbrowser.open('http://localhost:8080')
            self.log("📝 已打开管理界面")
        except Exception as e:
            self.log(f"❌ 打开管理界面失败: {e}")
            messagebox.showerror("错误", f"打开管理界面失败: {e}")
    
    def on_closing(self):
        """关闭窗口时的处理"""
        if self.server_running:
            self.stop_server()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = AdminLauncher(root)
    
    # 设置关闭事件
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # 启动GUI
    root.mainloop()

if __name__ == "__main__":
    main()
