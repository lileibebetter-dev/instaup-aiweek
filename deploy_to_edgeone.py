#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import shutil
from pathlib import Path

def build_for_edgeone():
    """为EdgeOne Pages构建静态网站"""
    print("🏗️  为EdgeOne Pages构建静态网站...")
    
    # EdgeOne Pages通常部署到根目录或public目录
    output_dir = Path("public")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir()
    
    # 复制静态文件
    static_files = [
        "index.html", "article.html", "styles.css", "script.js",
        "favicon.ico", "favicon.png"
    ]
    
    for file in static_files:
        if os.path.exists(file):
            shutil.copy2(file, output_dir)
            print(f"✅ 复制文件: {file}")
    
    # 复制目录
    dirs_to_copy = ["posts", "images"]
    for dir_name in dirs_to_copy:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, output_dir / dir_name)
            print(f"✅ 复制目录: {dir_name}")
    
    # 读取文章数据
    with open("posts/articles.json", "r", encoding="utf-8") as f:
        articles = json.load(f)
    
    # 为每个文章创建单独的HTML文件
    articles_dir = output_dir / "articles"
    articles_dir.mkdir()
    
    for article in articles:
        article_id = article['id']
        article_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{article['title']} | 云秒搭AI周报</title>
  <link rel="stylesheet" href="../styles.css">
  <link rel="icon" type="image/png" href="../favicon.png" />
  <link rel="icon" type="image/x-icon" href="../favicon.ico" />
  <meta name="description" content="{article['title']} - 云秒搭AI周报">
</head>
<body>
  <header class="site-header">
    <div class="container">
      <h1><a href="../index.html">云秒搭AI周报</a></h1>
    </div>
  </header>

  <main class="container">
    <article class="article-detail">
      <header class="article-header">
        <h1>{article['title']}</h1>
        <div class="article-meta">
          <span>{article['source']}</span>
          <span>{article['date']}</span>
        </div>
        <div class="article-tags">
          {''.join([f'<span class="article-tag">{tag}</span>' for tag in article['tags']])}
        </div>
      </header>
      
      <div class="article-body">
        {article['content']}
      </div>
      
      <div class="article-actions">
        <a href="../index.html">← 返回首页</a>
        <a href="{article['url']}" target="_blank">查看原文</a>
      </div>
    </article>
  </main>
  
  <footer class="site-footer">
    <div class="container">
      <p>© 2024 云秒搭AI周报 · Weekly AI Digest</p>
    </div>
  </footer>
</body>
</html>'''
        
        # 保存文章HTML文件
        article_file = articles_dir / f"{article_id}.html"
        with open(article_file, "w", encoding="utf-8") as f:
            f.write(article_html)
        
        print(f"✅ 生成文章: {article['title'][:30]}...")
    
    # 创建EdgeOne Pages配置文件
    create_edgeone_config(output_dir)
    
    print(f"\n🎉 EdgeOne Pages构建完成！")
    print(f"📁 输出目录: {output_dir.absolute()}")
    print(f"📄 生成文章: {len(articles)} 篇")
    print(f"\n📋 部署说明:")
    print(f"1. 将 public/ 目录下的所有文件上传到EdgeOne Pages")
    print(f"2. 或者使用EdgeOne Pages的Git集成功能")
    print(f"3. 确保网站根目录包含 index.html")

def create_edgeone_config(output_dir):
    """创建EdgeOne Pages配置文件"""
    
    # 创建.htaccess文件（如果需要）
    htaccess_content = """# EdgeOne Pages 配置
RewriteEngine On

# 处理文章详情页面
RewriteRule ^article/([^/]+)/?$ articles/$1.html [L]

# 处理API请求（如果需要）
RewriteRule ^api/articles$ posts/articles.json [L]

# 缓存设置
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
    ExpiresByType image/png "access plus 1 month"
    ExpiresByType image/jpg "access plus 1 month"
    ExpiresByType image/jpeg "access plus 1 month"
</IfModule>
"""
    
    with open(output_dir / ".htaccess", "w", encoding="utf-8") as f:
        f.write(htaccess_content)
    
    # 创建部署说明文件
    deploy_readme = """# EdgeOne Pages 部署说明

## 部署步骤

### 方法1：手动上传
1. 将 public/ 目录下的所有文件上传到EdgeOne Pages的根目录
2. 确保文件结构如下：
   ```
   /
   ├── index.html
   ├── article.html
   ├── styles.css
   ├── script.js
   ├── posts/
   │   └── articles.json
   ├── images/
   │   └── [各种图片目录]
   └── articles/
       └── [各文章HTML文件]
   ```

### 方法2：Git集成
1. 在EdgeOne Pages控制台启用Git集成
2. 连接到你的GitHub仓库
3. 设置构建命令：`python3 build_static_site.py`
4. 设置输出目录：`public`

## 注意事项
- 确保所有图片文件都已正确上传
- 检查文章链接是否正确
- 测试所有页面是否正常显示

## 更新流程
1. 本地修改文章或添加新文章
2. 运行 `python3 deploy_to_edgeone.py`
3. 将 public/ 目录内容上传到EdgeOne Pages
4. 或者推送代码到Git仓库（如果使用Git集成）
"""
    
    with open(output_dir / "DEPLOY_README.md", "w", encoding="utf-8") as f:
        f.write(deploy_readme)
    
    print("✅ 创建EdgeOne Pages配置文件")

if __name__ == "__main__":
    build_for_edgeone()
