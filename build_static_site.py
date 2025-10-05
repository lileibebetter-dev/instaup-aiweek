#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import shutil
from pathlib import Path

def build_static_site():
    """构建静态网站"""
    print("🏗️  开始构建静态网站...")
    
    # 创建输出目录
    output_dir = Path("_site")
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
    
    # 更新index.html中的链接
    update_index_links(output_dir / "index.html", articles)
    
    print(f"\n🎉 静态网站构建完成！")
    print(f"📁 输出目录: {output_dir.absolute()}")
    print(f"📄 生成文章: {len(articles)} 篇")

def update_index_links(index_file, articles):
    """更新首页中的文章链接"""
    with open(index_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 这里可以添加JavaScript代码来更新链接
    # 或者直接修改HTML内容
    print("✅ 更新首页链接")

if __name__ == "__main__":
    build_static_site()
