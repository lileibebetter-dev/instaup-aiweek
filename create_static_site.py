#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import shutil
from pathlib import Path

def create_static_site():
    """创建纯静态网站，适合EdgeOne Pages"""
    print("🏗️  创建纯静态网站...")
    
    # 直接复制到根目录，这样EdgeOne Pages可以直接使用
    files_to_copy = [
        "index.html", "article.html", "styles.css", "script.js",
        "favicon.ico", "favicon.png"
    ]
    
    # 复制静态文件
    for file in files_to_copy:
        if os.path.exists(file):
            print(f"✅ 文件已存在: {file}")
    
    # 确保posts和images目录存在
    if os.path.exists("posts"):
        print("✅ posts目录存在")
    if os.path.exists("images"):
        print("✅ images目录存在")
    
    # 读取文章数据并创建独立的HTML文件
    if os.path.exists("posts/articles.json"):
        with open("posts/articles.json", "r", encoding="utf-8") as f:
            articles = json.load(f)
        
        # 创建articles目录
        articles_dir = Path("articles")
        articles_dir.mkdir(exist_ok=True)
        
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
    
    print(f"\n🎉 纯静态网站创建完成！")
    print(f"📁 根目录包含所有必要文件")
    print(f"📄 生成文章: {len(articles) if 'articles' in locals() else 0} 篇")
    print(f"\n📋 EdgeOne Pages部署说明:")
    print(f"1. 确保根目录包含: index.html, styles.css, script.js")
    print(f"2. 确保 posts/ 和 images/ 目录存在")
    print(f"3. 确保 articles/ 目录包含所有文章HTML文件")
    print(f"4. 如果使用Git集成，设置输出目录为根目录 (/)")

if __name__ == "__main__":
    create_static_site()
