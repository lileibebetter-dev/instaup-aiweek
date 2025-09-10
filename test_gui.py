#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的GUI测试
"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import threading
import time

class SimpleLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("云秒搭AI周报 - 简单启动器")
        self.root.geometry("400x300")
        
        # 创建界面
        self.create_widgets()
        
        # 服务器状态
        self.server_running = False
        self.server_process = None
    
    def create_widgets(self):
        """创建界面组件"""
        # 标题
        title = tk.Label(
            self.root, 
            text="🚀 云秒搭AI周报管理后台", 
            font=("Arial", 16, "bold")
        )
        title.pack(pady=20)
        
        # 状态显示
        self.status_label = tk.Label(
            self.root,
            text="准备就绪",
            font=("Arial", 12),
            fg="green"
        )
        self.status_label.pack(pady=10)
        
        # 日志显示
        self.log_text = tk.Text(self.root, height=8, width=50)
        self.log_text.pack(pady=10, padx=20, fill='both', expand=True)
        
        # 按钮
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        self.start_btn = tk.Button(
            button_frame,
            text="🚀 启动服务器",
            font=("Arial", 12, "bold"),
            bg="blue",
            fg="white",
            padx=20,
            pady=10,
            command=self.start_server
        )
        self.start_btn.pack(side='left', padx=10)
        
        self.stop_btn = tk.Button(
            button_frame,
            text="⏹️ 停止服务器",
            font=("Arial", 12, "bold"),
            bg="red",
            fg="white",
            padx=20,
            pady=10,
            command=self.stop_server,
            state='disabled'
        )
        self.stop_btn.pack(side='left', padx=10)
        
        self.open_btn = tk.Button(
            button_frame,
            text="📝 打开管理界面",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            padx=20,
            pady=10,
            command=self.open_admin,
            state='disabled'
        )
        self.open_btn.pack(side='left', padx=10)
    
    def log(self, message):
        """添加日志"""
        self.log_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def start_server(self):
        """启动服务器"""
        self.log("🔘 启动按钮被点击")
        
        if self.server_running:
            self.log("⚠️ 服务器已在运行")
            return
        
        self.log("正在启动服务器...")
        self.status_label.config(text="正在启动服务器...", fg="orange")
        self.start_btn.config(state='disabled')
        
        # 在新线程中启动
        thread = threading.Thread(target=self._start_thread)
        thread.daemon = True
        thread.start()
    
    def _start_thread(self):
        """启动线程"""
        try:
            self.log("启动Flask服务器...")
            self.server_process = subprocess.Popen([
                sys.executable, "server.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            self.log("等待服务器启动...")
            time.sleep(3)
            
            # 检查服务器状态
            try:
                import requests
                response = requests.get('http://localhost:8080/api/articles', timeout=5)
                if response.status_code == 200:
                    self.server_running = True
                    self.root.after(0, self._server_started)
                else:
                    self.root.after(0, self._server_failed)
            except ImportError:
                self.log("安装requests库...")
                subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
                import requests
                response = requests.get('http://localhost:8080/api/articles', timeout=5)
                if response.status_code == 200:
                    self.server_running = True
                    self.root.after(0, self._server_started)
                else:
                    self.root.after(0, self._server_failed)
            except Exception as e:
                self.log(f"检查服务器状态失败: {e}")
                self.root.after(0, self._server_failed)
                
        except Exception as e:
            self.log(f"启动服务器失败: {e}")
            self.root.after(0, self._server_error)
    
    def _server_started(self):
        """服务器启动成功"""
        self.log("✅ 服务器启动成功")
        self.status_label.config(text="服务器运行中", fg="green")
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.open_btn.config(state='normal')
    
    def _server_failed(self):
        """服务器启动失败"""
        self.log("❌ 服务器启动失败")
        self.status_label.config(text="服务器启动失败", fg="red")
        self.start_btn.config(state='normal')
        messagebox.showerror("错误", "服务器启动失败")
    
    def _server_error(self):
        """服务器启动错误"""
        self.log("❌ 服务器启动错误")
        self.status_label.config(text="服务器启动错误", fg="red")
        self.start_btn.config(state='normal')
        messagebox.showerror("错误", "服务器启动错误")
    
    def stop_server(self):
        """停止服务器"""
        self.log("停止服务器...")
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None
        
        self.server_running = False
        self.log("✅ 服务器已停止")
        self.status_label.config(text="服务器已停止", fg="red")
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.open_btn.config(state='disabled')
    
    def open_admin(self):
        """打开管理界面"""
        try:
            import webbrowser
            webbrowser.open('http://localhost:8080')
            self.log("📝 已打开管理界面")
        except Exception as e:
            self.log(f"❌ 打开管理界面失败: {e}")
            messagebox.showerror("错误", f"打开管理界面失败: {e}")

def main():
    root = tk.Tk()
    app = SimpleLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()
