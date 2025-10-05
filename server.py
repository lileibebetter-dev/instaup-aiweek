#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章管理后台API服务器
提供RESTful API接口用于文章抓取、管理和Git同步
"""

import os
import json
import subprocess
import asyncio
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入爬虫模块
from crawler import WeChatArticleCrawler

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 配置
ARTICLES_FILE = 'posts/articles.json'
IMAGES_DIR = 'images'

def load_articles():
    """加载文章数据"""
    try:
        if os.path.exists(ARTICLES_FILE):
            with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"加载文章失败: {e}")
        return []

def save_articles(articles):
    """保存文章数据"""
    try:
        os.makedirs(os.path.dirname(ARTICLES_FILE), exist_ok=True)
        with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存文章失败: {e}")
        return False

def run_git_command(command):
    """执行Git命令"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

@app.route('/')
def index():
    """返回主页"""
    return send_from_directory('.', 'index.html')

@app.route('/admin')
def admin():
    """管理后台"""
    return send_from_directory('.', 'admin.html')

@app.route('/api/articles', methods=['GET'])
def get_articles():
    """获取文章列表"""
    try:
        articles = load_articles()
        return jsonify({
            'success': True,
            'articles': articles,
            'count': len(articles)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/articles/<article_id>', methods=['DELETE'])
def delete_article(article_id):
    """删除文章"""
    try:
        articles = load_articles()
        original_count = len(articles)
        
        # 删除文章
        articles = [article for article in articles if article.get('id') != article_id]
        
        if len(articles) == original_count:
            return jsonify({
                'success': False,
                'error': '文章不存在'
            }), 404
        
        # 保存更新后的文章列表
        if save_articles(articles):
            return jsonify({
                'success': True,
                'message': '文章删除成功'
            })
        else:
            return jsonify({
                'success': False,
                'error': '保存失败'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/crawl', methods=['POST'])
def crawl_article():
    """抓取文章"""
    try:
        data = request.get_json()
        url = data.get('url')
        custom_title = data.get('customTitle')
        custom_tags = data.get('customTags')
        
        if not url:
            return jsonify({
                'success': False,
                'error': '缺少文章链接'
            }), 400
        
        # 创建爬虫实例
        crawler = WeChatArticleCrawler()
        
        # 抓取文章
        print(f"开始抓取文章: {url}")
        article_data = crawler.fetch_article_content(url)
        
        if not article_data:
            return jsonify({
                'success': False,
                'error': '抓取文章失败'
            }), 500
        
        # 应用自定义设置
        if custom_title:
            article_data['title'] = custom_title
        
        if custom_tags:
            tags = [tag.strip() for tag in custom_tags.split(',') if tag.strip()]
            if tags:
                article_data['tags'] = tags
        
        # 加载现有文章
        articles = load_articles()
        
        # 检查是否已存在
        existing_ids = [article.get('id') for article in articles]
        if article_data.get('id') in existing_ids:
            # 更新现有文章
            for i, article in enumerate(articles):
                if article.get('id') == article_data.get('id'):
                    articles[i] = article_data
                    break
            message = "文章已更新"
        else:
            # 添加新文章
            articles.insert(0, article_data)  # 插入到开头
            message = "文章添加成功"
        
        # 保存文章
        if save_articles(articles):
            return jsonify({
                'success': True,
                'message': message,
                'article': article_data
            })
        else:
            return jsonify({
                'success': False,
                'error': '保存文章失败'
            }), 500
            
    except Exception as e:
        print(f"抓取文章错误: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/git-status', methods=['GET'])
def get_git_status():
    """获取Git状态"""
    try:
        # 检查是否有未提交的更改
        success, stdout, stderr = run_git_command('git status --porcelain')
        has_changes = bool(stdout.strip()) if success else False
        
        # 检查是否需要推送
        success, stdout, stderr = run_git_command('git status -sb')
        needs_push = 'ahead' in stdout if success else False
        
        return jsonify({
            'success': True,
            'status': {
                'has_changes': has_changes,
                'needs_push': needs_push,
                'working_tree_clean': not has_changes,
                'up_to_date': not needs_push
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sync', methods=['POST'])
def sync_to_git():
    """同步到Git"""
    try:
        # 检查是否有未提交的更改
        success, stdout, stderr = run_git_command('git status --porcelain')
        if not success:
            return jsonify({
                'success': False,
                'error': f'检查Git状态失败: {stderr}'
            }), 500
        
        # 如果有未提交的更改，则添加并提交
        if stdout.strip():
            # 添加所有更改
            success, stdout, stderr = run_git_command('git add .')
            if not success:
                return jsonify({
                    'success': False,
                    'error': f'Git add 失败: {stderr}'
                }), 500
            
            # 提交更改
            commit_message = f"通过管理后台添加文章 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            success, stdout, stderr = run_git_command(f'git commit -m "{commit_message}"')
            if not success:
                return jsonify({
                    'success': False,
                    'error': f'Git commit 失败: {stderr}'
                }), 500
            
            commit_msg = f'已提交更改: {commit_message}'
        else:
            commit_msg = '没有新的更改需要提交'
        
        # 检查是否需要推送
        success, stdout, stderr = run_git_command('git status -sb')
        if not success:
            return jsonify({
                'success': False,
                'error': f'检查推送状态失败: {stderr}'
            }), 500
        
        # 如果有未推送的提交，则推送
        if 'ahead' in stdout:
            success, stdout, stderr = run_git_command('git push origin main')
            if not success:
                return jsonify({
                    'success': False,
                    'error': f'Git push 失败: {stderr}'
                }), 500
            push_msg = '已推送到远程仓库'
        else:
            push_msg = '没有需要推送的提交'
        
        return jsonify({
            'success': True,
            'message': f'Git同步完成 - {commit_msg}, {push_msg}',
            'details': {
                'commit': commit_msg,
                'push': push_msg
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/clear-cache', methods=['POST'])
def clear_cache():
    """清除缓存"""
    try:
        # 这里可以添加清除缓存的逻辑
        # 比如清除临时文件、重置某些状态等
        
        return jsonify({
            'success': True,
            'message': '缓存清除成功'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    try:
        articles = load_articles()
        
        # 计算今日新增文章
        today = datetime.now().strftime('%Y-%m-%d')
        today_articles = [article for article in articles if article.get('date') == today]
        
        # 计算图片总数
        total_images = 0
        for article in articles:
            content = article.get('content', '')
            # 简单计算img标签数量
            total_images += content.count('<img')
        
        return jsonify({
            'success': True,
            'stats': {
                'total_articles': len(articles),
                'today_articles': len(today_articles),
                'total_images': total_images
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# 简单邮件发送API
@app.route('/api/send-email', methods=['POST'])
def send_email():
    """发送邮件"""
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        data = request.get_json()
        to_emails = data.get('to_emails', [])
        subject = data.get('subject', '')
        content = data.get('content', '')
        
        if not to_emails or not subject or not content:
            return jsonify({
                'success': False,
                'error': '缺少必要参数：to_emails, subject, content'
            }), 400
        
        # 简单的邮件发送功能（需要配置SMTP）
        # 这里只是一个示例，实际使用时需要配置SMTP服务器
        
        return jsonify({
            'success': True,
            'message': f'邮件发送成功，收件人：{", ".join(to_emails)}',
            'note': '这是模拟发送，请配置SMTP服务器以实际发送邮件'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# 静态文件服务
@app.route('/<path:filename>')
def serve_static(filename):
    """提供静态文件服务"""
    response = send_from_directory('.', filename)
    # 禁用缓存，确保文件更新后立即生效
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    print("🚀 启动文章管理后台服务器...")
    print("📝 管理界面: http://localhost:8888")
    print("📚 文章列表: http://localhost:8888/api/articles")
    print("🔧 按 Ctrl+C 停止服务器")
    
    app.run(host='0.0.0.0', port=8888, debug=True)
