#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
from bs4 import BeautifulSoup

def fix_ui_colors():
    """修改UI颜色为白蓝色主题"""
    print("🎨 修改UI颜色为白蓝色主题...")
    
    # 读取当前样式文件
    with open('styles.css', 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # 替换颜色变量为白蓝色主题
    color_replacements = {
        '--pixel-primary: #00ff41;': '--pixel-primary: #2196f3;',      # 蓝色
        '--pixel-secondary: #008f11;': '--pixel-secondary: #1976d2;',   # 深蓝色
        '--pixel-accent: #ff6b35;': '--pixel-accent: #64b5f6;',        # 浅蓝色
        '--pixel-bg: #0d1117;': '--pixel-bg: #ffffff;',                # 白色背景
        '--pixel-card: #161b22;': '--pixel-card: #f8f9fa;',            # 浅灰色卡片
        '--pixel-text: #f0f6fc;': '--pixel-text: #212529;',            # 深色文字
        '--pixel-muted: #8b949e;': '--pixel-muted: #6c757d;',          # 灰色文字
        '--pixel-border: #30363d;': '--pixel-border: #dee2e6;',        # 浅灰色边框
    }
    
    for old_color, new_color in color_replacements.items():
        css_content = css_content.replace(old_color, new_color)
    
    # 修改特定的颜色值
    css_content = css_content.replace('rgba(0, 255, 65, 0.1)', 'rgba(33, 150, 243, 0.1)')  # 蓝色透明背景
    css_content = css_content.replace('rgba(0, 255, 65, 0.05)', 'rgba(33, 150, 243, 0.05)')  # 浅蓝色透明背景
    css_content = css_content.replace('rgba(0, 255, 65, 0.3)', 'rgba(33, 150, 243, 0.3)')    # 蓝色阴影
    css_content = css_content.replace('rgba(0, 255, 65, 0.2)', 'rgba(33, 150, 243, 0.2)')    # 蓝色悬停效果
    
    # 修改背景渐变
    css_content = css_content.replace(
        'linear-gradient(45deg, transparent 49%, rgba(0, 255, 65, 0.1) 50%, transparent 51%)',
        'linear-gradient(45deg, transparent 49%, rgba(33, 150, 243, 0.1) 50%, transparent 51%)'
    )
    css_content = css_content.replace(
        'linear-gradient(-45deg, transparent 49%, rgba(0, 255, 65, 0.1) 50%, transparent 51%)',
        'linear-gradient(-45deg, transparent 49%, rgba(33, 150, 243, 0.1) 50%, transparent 51%)'
    )
    
    # 修改文字阴影
    css_content = css_content.replace('3px 3px 0px var(--pixel-secondary)', '2px 2px 0px var(--pixel-secondary)')
    css_content = css_content.replace('2px 2px 0px var(--pixel-secondary)', '1px 1px 0px var(--pixel-secondary)')
    css_content = css_content.replace('1px 1px 0px var(--pixel-secondary)', '1px 1px 2px rgba(33, 150, 243, 0.3)')
    
    # 保存修改后的样式
    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    print("✅ UI颜色已修改为白蓝色主题")

def fix_article_images():
    """修复文章详情页图片路径问题"""
    print("🖼️  修复文章详情页图片路径...")
    
    # 读取文章数据
    with open('posts/articles.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    # 重新生成文章页面，修复图片路径
    for article in articles:
        article_id = article['id']
        article_file = f"articles/{article_id}.html"
        
        if not os.path.exists(article_file):
            continue
        
        print(f"📝 修复文章: {article['title'][:30]}...")
        
        # 使用BeautifulSoup处理文章内容，修复图片路径
        soup = BeautifulSoup(article['content'], 'html.parser')
        
        # 查找所有图片标签
        images = soup.find_all('img')
        for img in images:
            # 获取原始src和data-src
            src = img.get('src')
            data_src = img.get('data-src')
            
            # 优先使用data-src，如果没有则使用src
            image_path = data_src if data_src else src
            
            if image_path and image_path.startswith('images/'):
                # 修复路径：从 images/xxx 改为 ../images/xxx
                fixed_path = f"../{image_path}"
                img['src'] = fixed_path
                if data_src:
                    img['data-src'] = fixed_path
        
        # 获取修复后的内容
        fixed_content = str(soup)
        
        # 重新生成文章页面
        article_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']} | 云秒搭AI周报</title>
    <meta name="description" content="{article['title']} - 云秒搭AI周报">
    <link rel="stylesheet" href="../styles.css">
    <link rel="icon" type="image/png" href="../favicon.png">
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    <style>
        /* 文章页面特定样式 */
        .article-container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .article-header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            border: 3px solid var(--pixel-primary);
            background: rgba(33, 150, 243, 0.05);
        }}
        
        .article-title {{
            font-size: 1.2rem;
            color: var(--pixel-primary);
            margin-bottom: 20px;
            line-height: 1.4;
        }}
        
        .article-meta {{
            font-size: 0.6rem;
            color: var(--pixel-muted);
            margin-bottom: 15px;
        }}
        
        .article-meta span {{
            display: inline-block;
            margin: 0 10px;
        }}
        
        .article-tags {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 8px;
        }}
        
        .article-content {{
            background: var(--pixel-card);
            border: 2px solid var(--pixel-border);
            padding: 30px;
            margin-bottom: 30px;
            line-height: 1.8;
        }}
        
        .article-content h1,
        .article-content h2,
        .article-content h3 {{
            color: var(--pixel-primary);
            margin: 20px 0 15px 0;
        }}
        
        .article-content p {{
            margin-bottom: 15px;
            font-size: 0.7rem;
            color: var(--pixel-text);
        }}
        
        .article-content img {{
            max-width: 100%;
            height: auto;
            border: 2px solid var(--pixel-border);
            margin: 15px 0;
            display: block;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .article-actions {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 30px;
        }}
        
        .action-btn {{
            background: var(--pixel-card);
            border: 2px solid var(--pixel-border);
            color: var(--pixel-text);
            padding: 15px 25px;
            font-family: inherit;
            font-size: 0.6rem;
            text-decoration: none;
            transition: all 0.2s;
            cursor: pointer;
            border-radius: 4px;
        }}
        
        .action-btn:hover {{
            background: var(--pixel-primary);
            color: white;
            border-color: var(--pixel-primary);
            transform: translate(-2px, -2px);
            box-shadow: 4px 4px 0px var(--pixel-secondary);
        }}
        
        @media (max-width: 768px) {{
            .article-container {{
                padding: 15px;
            }}
            
            .article-title {{
                font-size: 1rem;
            }}
            
            .article-content {{
                padding: 20px;
            }}
            
            .article-actions {{
                flex-direction: column;
                align-items: center;
            }}
        }}
    </style>
</head>
<body>
    <div class="pixel-bg"></div>
    
    <div class="article-container">
        <header class="article-header">
            <h1 class="article-title">{article['title']}</h1>
            <div class="article-meta">
                <span>📰 {article.get('source', '来源')}</span>
                <span>📅 {article.get('date', '')}</span>
            </div>
            <div class="article-tags">
                {''.join([f'<span class="pixel-tag">{tag}</span>' for tag in article.get('tags', [])])}
            </div>
        </header>
        
        <main class="article-content">
            {fixed_content}
        </main>
        
        <div class="article-actions">
            <a href="../index.html" class="action-btn">← 返回首页</a>
            <a href="{article['url']}" target="_blank" class="action-btn">查看原文 →</a>
        </div>
    </div>
    
    <!-- 浮动像素特效 -->
    <div class="pixel-effects">
        <div class="floating-pixel">📰</div>
        <div class="floating-pixel">🤖</div>
        <div class="floating-pixel">⚡</div>
    </div>
</body>
</html>"""
        
        # 保存修复后的文章页面
        with open(article_file, 'w', encoding='utf-8') as f:
            f.write(article_html)
    
    print("✅ 文章详情页图片路径已修复")

def main():
    """主函数"""
    print("🔧 开始修复UI颜色和图片加载问题...")
    
    # 修复UI颜色
    fix_ui_colors()
    
    # 修复文章图片
    fix_article_images()
    
    print("\n🎉 修复完成！")
    print("✅ UI颜色已改为白蓝色主题")
    print("✅ 文章详情页图片路径已修复")

if __name__ == "__main__":
    main()
