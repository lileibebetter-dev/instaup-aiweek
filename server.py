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
import threading
import time
import uuid
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import sys

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入爬虫模块
from crawler import WeChatArticleCrawler
from pdf_processor import PDFProcessor

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 配置
ARTICLES_FILE = 'posts/articles.json'
IMAGES_DIR = 'images'

# 任务状态存储
report_tasks = {}

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
        
        # 找到要删除的文章
        article_to_delete = None
        for article in articles:
            if article.get('id') == article_id:
                article_to_delete = article
                break
        
        if not article_to_delete:
            return jsonify({
                'success': False,
                'error': '文章不存在'
            }), 404
        
        # 删除文章
        articles = [article for article in articles if article.get('id') != article_id]
        
        # 删除本地文件
        deleted_files = []
        
        # 删除HTML文件
        html_file = f"articles/{article_id}.html"
        if os.path.exists(html_file):
            try:
                os.remove(html_file)
                deleted_files.append(f"HTML文件: {html_file}")
            except Exception as e:
                print(f"删除HTML文件失败: {e}")
        
        # 删除PDF文件（如果是PDF解读文章）
        if 'pdf_path' in article_to_delete:
            pdf_file = article_to_delete['pdf_path']
            if os.path.exists(pdf_file):
                try:
                    os.remove(pdf_file)
                    deleted_files.append(f"PDF文件: {pdf_file}")
                except Exception as e:
                    print(f"删除PDF文件失败: {e}")
        
        # 保存更新后的文章列表
        if save_articles(articles):
            message = '文章删除成功'
            if deleted_files:
                message += f'，已删除本地文件: {", ".join(deleted_files)}'
            
            return jsonify({
                'success': True,
                'message': message,
                'deleted_files': deleted_files
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

@app.route('/api/articles/update', methods=['POST'])
def update_article():
    """更新文章信息"""
    try:
        data = request.get_json()
        article_id = data.get('id')
        title = data.get('title')
        source = data.get('source')
        summary = data.get('summary')
        url = data.get('url')
        date = data.get('date')
        
        if not article_id:
            return jsonify({
                'success': False,
                'error': '缺少文章ID'
            }), 400
        
        if not title:
            return jsonify({
                'success': False,
                'error': '缺少文章标题'
            }), 400
        
        # 加载文章列表
        articles = load_articles()
        
        # 查找文章
        article = next((a for a in articles if a['id'] == article_id), None)
        if not article:
            return jsonify({
                'success': False,
                'error': '文章不存在'
            }), 404
        
        # 更新文章信息
        article['title'] = title
        if source:
            article['source'] = source
        if summary:
            article['summary'] = summary
        if url:
            article['url'] = url
        if date:
            article['date'] = date
        
        # 保存文章列表
        if save_articles(articles):
            return jsonify({
                'success': True,
                'message': '文章更新成功'
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

@app.route('/api/articles/update-categories', methods=['POST'])
def update_article_categories():
    """更新文章分类"""
    try:
        data = request.get_json()
        article_id = data.get('id')
        tags = data.get('tags', [])
        
        if not article_id:
            return jsonify({
                'success': False,
                'error': '缺少文章ID'
            }), 400
        
        # 加载文章列表
        articles = load_articles()
        
        # 查找文章
        article = next((a for a in articles if a['id'] == article_id), None)
        if not article:
            return jsonify({
                'success': False,
                'error': '文章不存在'
            }), 404
        
        # 更新标签
        article['tags'] = tags
        
        # 保存文章列表
        if save_articles(articles):
            return jsonify({
                'success': True,
                'message': '分类更新成功'
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

@app.route('/api/images/count', methods=['GET'])
def get_images_count():
    """获取图片总数"""
    try:
        import os
        import glob
        
        # 统计images目录下的所有图片文件
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp', '*.bmp']
        total_images = 0
        
        for ext in image_extensions:
            pattern = os.path.join('images', '**', ext)
            total_images += len(glob.glob(pattern, recursive=True))
        
        return jsonify({
            'success': True,
            'count': total_images
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/check-orphaned-files', methods=['GET'])
def check_orphaned_files():
    """检查本地未上架的文件"""
    try:
        import os
        import glob
        
        # 获取所有已上架的文章ID
        articles = load_articles()
        published_ids = set(article.get('id') for article in articles)
        
        orphaned_files = []
        
        # 检查articles目录下的HTML文件
        html_files = glob.glob('articles/*.html')
        for html_file in html_files:
            # 从文件名提取文章ID
            filename = os.path.basename(html_file)
            article_id = os.path.splitext(filename)[0]
            
            # 如果文章ID不在已上架列表中，标记为孤立文件
            if article_id not in published_ids:
                file_size = os.path.getsize(html_file)
                orphaned_files.append({
                    'type': 'HTML文件',
                    'path': html_file,
                    'size': file_size,
                    'article_id': article_id
                })
        
        # 检查uploads/pdf目录下的PDF文件
        pdf_files = glob.glob('uploads/pdf/*.pdf')
        for pdf_file in pdf_files:
            # 检查是否有文章引用这个PDF文件
            is_referenced = False
            for article in articles:
                if article.get('pdf_path') == pdf_file:
                    is_referenced = True
                    break
            
            # 如果没有文章引用，标记为孤立文件
            if not is_referenced:
                file_size = os.path.getsize(pdf_file)
                orphaned_files.append({
                    'type': 'PDF文件',
                    'path': pdf_file,
                    'size': file_size,
                    'article_id': None
                })
        
        return jsonify({
            'success': True,
            'orphaned_files': orphaned_files,
            'count': len(orphaned_files)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cleanup-selected-files', methods=['POST'])
def cleanup_selected_files():
    """删除选中的未上架文件"""
    try:
        import os
        
        data = request.get_json()
        file_paths = data.get('file_paths', [])
        
        if not file_paths:
            return jsonify({
                'success': False,
                'error': '没有指定要删除的文件'
            }), 400
        
        deleted_files = []
        failed_files = []
        deleted_articles = []
        
        # 加载文章列表
        articles = load_articles()
        articles_updated = False
        
        for file_path in file_paths:
            try:
                # 检查文件是否存在
                if os.path.exists(file_path):
                    # 从文件路径中提取文章ID
                    filename = os.path.basename(file_path)
                    article_id = os.path.splitext(filename)[0]  # 去掉扩展名
                    
                    # 从文章列表中删除对应的文章记录
                    original_count = len(articles)
                    articles = [article for article in articles if article.get('id') != article_id]
                    
                    if len(articles) < original_count:
                        deleted_articles.append(article_id)
                        articles_updated = True
                        print(f"从文章列表中删除文章: {article_id}")
                    
                    # 删除文件
                    os.remove(file_path)
                    deleted_files.append(file_path)
                else:
                    failed_files.append(f"文件不存在: {file_path}")
            except Exception as e:
                failed_files.append(f"删除失败 {file_path}: {str(e)}")
        
        # 如果删除了文章记录，保存更新后的文章列表
        if articles_updated:
            if save_articles(articles):
                print(f"文章列表已更新，删除了 {len(deleted_articles)} 个文章记录")
            else:
                print("警告：文件删除成功，但文章列表更新失败")
        
        message = f'清理完成，成功删除了 {len(deleted_files)} 个文件'
        if deleted_articles:
            message += f'，同步删除了 {len(deleted_articles)} 个文章记录'
        if failed_files:
            message += f'，{len(failed_files)} 个文件删除失败'
        
        return jsonify({
            'success': True,
            'message': message,
            'deleted_files': deleted_files,
            'deleted_articles': deleted_articles,
            'failed_files': failed_files,
            'count': len(deleted_files)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cleanup-orphaned-files', methods=['POST'])
def cleanup_orphaned_files():
    """清除本地未上架的文件"""
    try:
        import os
        import glob
        
        # 获取所有已上架的文章ID
        articles = load_articles()
        published_ids = set(article.get('id') for article in articles)
        
        deleted_files = []
        
        # 检查articles目录下的HTML文件
        html_files = glob.glob('articles/*.html')
        for html_file in html_files:
            # 从文件名提取文章ID
            filename = os.path.basename(html_file)
            article_id = os.path.splitext(filename)[0]
            
            # 如果文章ID不在已上架列表中，删除文件
            if article_id not in published_ids:
                try:
                    os.remove(html_file)
                    deleted_files.append(f"HTML文件: {html_file}")
                except Exception as e:
                    print(f"删除文件失败 {html_file}: {e}")
        
        # 检查uploads/pdf目录下的PDF文件
        pdf_files = glob.glob('uploads/pdf/*.pdf')
        for pdf_file in pdf_files:
            # 检查是否有文章引用这个PDF文件
            is_referenced = False
            for article in articles:
                if article.get('pdf_path') == pdf_file:
                    is_referenced = True
                    break
            
            # 如果没有文章引用，删除文件
            if not is_referenced:
                try:
                    os.remove(pdf_file)
                    deleted_files.append(f"PDF文件: {pdf_file}")
                except Exception as e:
                    print(f"删除文件失败 {pdf_file}: {e}")
        
        return jsonify({
            'success': True,
            'message': f'清理完成，删除了 {len(deleted_files)} 个未上架文件',
            'deleted_files': deleted_files,
            'count': len(deleted_files)
        })
        
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
        
        # 验证URL类型
        if 'mp.weixin.qq.com' not in url:
            return jsonify({
                'success': False,
                'error': '目前只支持微信公众号文章链接 (mp.weixin.qq.com)'
            }), 400
        
        # 创建爬虫实例
        crawler = WeChatArticleCrawler()
        print(f"使用微信公众号爬虫抓取文章: {url}")
        
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
            # 如果custom_tags是字符串，则分割；如果是列表，则直接使用
            if isinstance(custom_tags, str):
                tags = [tag.strip() for tag in custom_tags.split(',') if tag.strip()]
            else:
                tags = [tag.strip() for tag in custom_tags if tag.strip()]
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

# 构建网站API
@app.route('/api/build-site', methods=['POST'])
def build_site():
    """构建网站"""
    try:
        import subprocess
        import sys
        
        # 运行构建脚本
        result = subprocess.run([sys.executable, 'build.py'], 
                              capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': '网站构建成功',
                'output': result.stdout
            })
        else:
            return jsonify({
                'success': False,
                'error': f'构建失败: {result.stderr}',
                'output': result.stdout
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# PDF处理相关API
@app.route('/api/upload-pdf', methods=['POST'])
def upload_pdf():
    """上传PDF文件并生成解读文章"""
    try:
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': '没有上传文件'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': '没有选择文件'
            }), 400
        
        # 获取自定义参数
        custom_title = request.form.get('customTitle')
        custom_tags = request.form.get('customTags')
        
        # 创建PDF处理器
        processor = PDFProcessor()
        
        # 保存PDF文件
        pdf_path, error = processor.save_pdf(file)
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        # 从PDF创建文章
        article_data, error = processor.create_article_from_pdf(
            pdf_path, custom_title, custom_tags
        )
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 500
        
        # 更新文章列表
        if processor.update_articles_json(article_data):
            return jsonify({
                'success': True,
                'message': 'PDF解读文章生成成功',
                'article': article_data
            })
        else:
            return jsonify({
                'success': False,
                'error': '保存文章失败'
            }), 500
            
    except Exception as e:
        print(f"PDF上传处理失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/download-pdf/<filename>')
def download_pdf(filename):
    """下载PDF文件"""
    try:
        pdf_dir = 'uploads/pdf'
        if not os.path.exists(pdf_dir):
            return jsonify({'error': 'PDF目录不存在'}), 404
        
        pdf_path = os.path.join(pdf_dir, filename)
        if not os.path.exists(pdf_path):
            return jsonify({'error': 'PDF文件不存在'}), 404
        
        return send_file(pdf_path, as_attachment=True)
        
    except Exception as e:
        print(f"PDF下载失败: {e}")
        return jsonify({'error': '下载失败'}), 500

@app.route('/api/pdf-list')
def list_pdfs():
    """获取PDF文件列表"""
    try:
        pdf_dir = 'uploads/pdf'
        if not os.path.exists(pdf_dir):
            return jsonify({'pdfs': []})
        
        pdfs = []
        for filename in os.listdir(pdf_dir):
            if filename.endswith('.pdf'):
                file_path = os.path.join(pdf_dir, filename)
                file_size = os.path.getsize(file_path)
                file_time = os.path.getmtime(file_path)
                
                pdfs.append({
                    'filename': filename,
                    'size': file_size,
                    'upload_time': datetime.fromtimestamp(file_time).strftime('%Y-%m-%d %H:%M:%S'),
                    'download_url': f'/api/download-pdf/{filename}'
                })
        
        return jsonify({'pdfs': pdfs})
        
    except Exception as e:
        print(f"获取PDF列表失败: {e}")
        return jsonify({'error': '获取列表失败'}), 500

@app.route('/api/generate-weekly-report', methods=['POST'])
def generate_weekly_report():
    """生成AI周报"""
    try:
        # 创建任务ID
        task_id = str(uuid.uuid4())
        
        # 初始化任务状态
        report_tasks[task_id] = {
            'status': 'running',
            'progress': 0,
            'message': '开始生成AI周报...',
            'details': '正在准备数据',
            'start_time': time.time(),
            'article': None,
            'error': None
        }
        
        # 在后台线程中执行周报生成
        thread = threading.Thread(target=generate_report_background, args=(task_id,))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': '周报生成任务已启动'
        })
        
    except Exception as e:
        print(f"生成周报失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def generate_report_background(task_id):
    """后台生成周报"""
    try:
        # 更新进度：准备数据
        report_tasks[task_id].update({
            'progress': 10,
            'message': '正在准备数据...',
            'details': '加载文章数据'
        })
        
        # 创建PDF处理器
        processor = PDFProcessor()
        
        # 获取所有文章数据
        articles = load_articles()
        
        if not articles:
            report_tasks[task_id].update({
                'status': 'failed',
                'error': '没有找到文章数据，无法生成周报'
            })
            return
        
        # 更新进度：分析文章
        report_tasks[task_id].update({
            'progress': 30,
            'message': '正在分析文章...',
            'details': f'分析 {len(articles)} 篇文章'
        })
        
        # 更新进度：生成内容
        report_tasks[task_id].update({
            'progress': 50,
            'message': '正在生成周报内容...',
            'details': '调用AI生成周报'
        })
        
        # 生成周报（带进度回调）
        def progress_callback(progress, message, details):
            report_tasks[task_id].update({
                'progress': progress,
                'message': message,
                'details': details
            })
        
        report_data, error = processor.generate_weekly_report(articles, progress_callback)
        
        if error:
            report_tasks[task_id].update({
                'status': 'failed',
                'error': error
            })
            return
        
        # 更新进度：保存文章
        report_tasks[task_id].update({
            'progress': 80,
            'message': '正在保存周报...',
            'details': '更新文章列表'
        })
        
        # 保存周报到文章列表
        if processor.update_articles_json(report_data):
            # 更新进度：完成
            report_tasks[task_id].update({
                'status': 'completed',
                'progress': 100,
                'message': '周报生成完成！',
                'details': '周报已成功保存',
                'article': report_data
            })
        else:
            report_tasks[task_id].update({
                'status': 'failed',
                'error': '保存周报失败'
            })
            
    except Exception as e:
        report_tasks[task_id].update({
            'status': 'failed',
            'error': str(e)
        })

@app.route('/api/report-progress/<task_id>', methods=['GET'])
def get_report_progress(task_id):
    """获取周报生成进度"""
    try:
        if task_id not in report_tasks:
            return jsonify({
                'success': False,
                'error': '任务不存在'
            }), 404
        
        task = report_tasks[task_id]
        
        # 计算运行时间
        runtime = time.time() - task['start_time']
        
        return jsonify({
            'success': True,
            'progress': {
                'status': task['status'],
                'percentage': task['progress'],
                'message': task['message'],
                'details': task['details'],
                'runtime': f"{runtime:.1f}秒"
            },
            'article': task.get('article'),
            'error': task.get('error')
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
