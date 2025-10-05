#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

def build_edgeone_site():
    """为EdgeOne Pages构建完整的白蓝色像素风网站"""
    print("🏗️  为EdgeOne Pages构建白蓝色像素风网站...")
    
    # 读取文章数据
    with open('posts/articles.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    print(f"📚 找到 {len(articles)} 篇文章")
    
    # 1. 创建白蓝色像素风主页
    create_blue_white_homepage(articles)
    
    # 2. 创建白蓝色像素风样式
    create_blue_white_styles()
    
    # 3. 创建修复了图片路径的独立文章页面
    create_fixed_article_pages(articles)
    
    print("\n🎉 EdgeOne Pages构建完成！")
    print("📁 文件结构:")
    print("  - index.html (白蓝色像素风主页)")
    print("  - styles.css (白蓝色像素风样式)")
    print("  - articles/ (修复图片路径的文章页面)")
    print("  - posts/ (文章数据)")
    print("  - images/ (图片资源)")

def create_blue_white_homepage(articles):
    """创建白蓝色像素风主页"""
    articles_html = ""
    for i, article in enumerate(articles):
        articles_html += f"""
        <div class="pixel-card" data-aos="fade-up" data-aos-delay="{i * 100}">
            <div class="card-header">
                <div class="pixel-icon">📰</div>
                <div class="card-meta">
                    <span class="source">{article.get('source', '来源')}</span>
                    <span class="date">{article.get('date', '')}</span>
                </div>
            </div>
            <h2 class="pixel-title">
                <a href="articles/{article['id']}.html" class="pixel-link">
                    {article['title']}
                </a>
            </h2>
            <div class="pixel-tags">
                {''.join([f'<span class="pixel-tag">{tag}</span>' for tag in article.get('tags', [])])}
            </div>
        </div>
        """
    
    homepage_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>云秒搭AI周报 | 白蓝色像素风AI资讯平台</title>
    <meta name="description" content="白蓝色像素风设计的AI资讯周报，每周精选前沿AI技术与应用">
    <link rel="stylesheet" href="styles.css">
    <link rel="icon" type="image/png" href="favicon.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
</head>
<body>
    <!-- 像素风背景 -->
    <div class="pixel-bg"></div>
    
    <!-- 主容器 -->
    <div class="container">
        <!-- 像素风头部 -->
        <header class="pixel-header">
            <div class="header-content">
                <h1 class="pixel-logo">
                    <span class="pixel-text">云秒搭AI周报</span>
                    <span class="pixel-subtitle">BLUE WHITE PIXEL AI DIGEST</span>
                </h1>
                <div class="pixel-nav">
                    <button class="pixel-btn active">首页</button>
                    <button class="pixel-btn">周报</button>
                    <button class="pixel-btn">AI技术</button>
                    <button class="pixel-btn">关于</button>
                </div>
            </div>
        </header>
        
        <!-- 像素风搜索栏 -->
        <div class="search-section">
            <div class="pixel-search-box">
                <input type="text" placeholder="搜索AI资讯..." class="pixel-input">
                <button class="pixel-search-btn">🔍</button>
            </div>
        </div>
        
        <!-- 文章网格 -->
        <main class="articles-grid">
            {articles_html}
        </main>
        
        <!-- 像素风页脚 -->
        <footer class="pixel-footer">
            <div class="footer-content">
                <p class="pixel-text">© 2024 云秒搭AI周报 - 白蓝色像素风设计</p>
                <div class="footer-links">
                    <a href="#" class="pixel-link">GitHub</a>
                    <a href="#" class="pixel-link">联系</a>
                    <a href="#" class="pixel-link">RSS</a>
                </div>
            </div>
        </footer>
    </div>
    
    <!-- 像素风特效 -->
    <div class="pixel-effects">
        <div class="floating-pixel">💻</div>
        <div class="floating-pixel">🤖</div>
        <div class="floating-pixel">⚡</div>
    </div>
    
    <script>
        // 简单的搜索功能
        document.querySelector('.pixel-input').addEventListener('input', function(e) {{
            const searchTerm = e.target.value.toLowerCase();
            const cards = document.querySelectorAll('.pixel-card');
            
            cards.forEach(card => {{
                const title = card.querySelector('.pixel-title').textContent.toLowerCase();
                const tags = card.querySelector('.pixel-tags').textContent.toLowerCase();
                
                if (title.includes(searchTerm) || tags.includes(searchTerm)) {{
                    card.style.display = 'block';
                }} else {{
                    card.style.display = searchTerm ? 'none' : 'block';
                }}
            }});
        }});
        
        // 像素风按钮点击效果
        document.querySelectorAll('.pixel-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                document.querySelectorAll('.pixel-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
            }});
        }});
    </script>
</body>
</html>"""
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(homepage_content)
    
    print("✅ 创建白蓝色像素风主页")

def create_blue_white_styles():
    """创建白蓝色像素风样式"""
    blue_white_styles = """/* 白蓝色像素风AI周报样式 */
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

:root {
    --pixel-primary: #2196f3;
    --pixel-secondary: #1976d2;
    --pixel-accent: #64b5f6;
    --pixel-bg: #ffffff;
    --pixel-card: #f8f9fa;
    --pixel-text: #212529;
    --pixel-muted: #6c757d;
    --pixel-border: #dee2e6;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Press Start 2P', monospace;
    background: var(--pixel-bg);
    color: var(--pixel-text);
    line-height: 1.6;
    overflow-x: hidden;
}

/* 像素风背景 */
.pixel-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        linear-gradient(45deg, transparent 49%, rgba(33, 150, 243, 0.1) 50%, transparent 51%),
        linear-gradient(-45deg, transparent 49%, rgba(33, 150, 243, 0.1) 50%, transparent 51%);
    background-size: 20px 20px;
    z-index: -1;
    animation: pixelMove 20s linear infinite;
}

@keyframes pixelMove {
    0% { transform: translate(0, 0); }
    100% { transform: translate(20px, 20px); }
}

/* 容器 */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    position: relative;
    z-index: 1;
}

/* 像素风头部 */
.pixel-header {
    text-align: center;
    margin-bottom: 40px;
    padding: 30px 0;
    border: 3px solid var(--pixel-primary);
    border-image: repeating-linear-gradient(45deg, var(--pixel-primary), var(--pixel-primary) 10px, transparent 10px, transparent 20px) 1;
    background: rgba(33, 150, 243, 0.05);
}

.pixel-logo {
    margin-bottom: 20px;
}

.pixel-text {
    display: block;
    font-size: 2.5rem;
    color: var(--pixel-primary);
    text-shadow: 2px 2px 0px var(--pixel-secondary);
    margin-bottom: 10px;
}

.pixel-subtitle {
    display: block;
    font-size: 0.8rem;
    color: var(--pixel-muted);
    letter-spacing: 3px;
}

.pixel-nav {
    display: flex;
    justify-content: center;
    gap: 15px;
    flex-wrap: wrap;
}

.pixel-btn {
    background: var(--pixel-card);
    border: 2px solid var(--pixel-border);
    color: var(--pixel-text);
    padding: 10px 20px;
    font-family: inherit;
    font-size: 0.7rem;
    cursor: pointer;
    transition: all 0.2s;
    position: relative;
}

.pixel-btn:hover,
.pixel-btn.active {
    background: var(--pixel-primary);
    color: white;
    border-color: var(--pixel-primary);
    transform: translate(-2px, -2px);
    box-shadow: 4px 4px 0px var(--pixel-secondary);
}

.pixel-btn:active {
    transform: translate(0, 0);
    box-shadow: 2px 2px 0px var(--pixel-secondary);
}

/* 搜索区域 */
.search-section {
    margin-bottom: 40px;
    display: flex;
    justify-content: center;
}

.pixel-search-box {
    display: flex;
    align-items: center;
    background: var(--pixel-card);
    border: 2px solid var(--pixel-border);
    padding: 5px;
    max-width: 500px;
    width: 100%;
}

.pixel-input {
    flex: 1;
    background: transparent;
    border: none;
    color: var(--pixel-text);
    padding: 15px;
    font-family: inherit;
    font-size: 0.7rem;
    outline: none;
}

.pixel-input::placeholder {
    color: var(--pixel-muted);
}

.pixel-search-btn {
    background: var(--pixel-accent);
    border: 2px solid var(--pixel-accent);
    color: var(--pixel-bg);
    padding: 10px 15px;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.2s;
}

.pixel-search-btn:hover {
    transform: translate(-1px, -1px);
    box-shadow: 2px 2px 0px #1976d2;
}

/* 文章网格 */
.articles-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 25px;
    margin-bottom: 60px;
}

.pixel-card {
    background: var(--pixel-card);
    border: 2px solid var(--pixel-border);
    padding: 25px;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.pixel-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(33, 150, 243, 0.2), transparent);
    transition: left 0.5s;
}

.pixel-card:hover::before {
    left: 100%;
}

.pixel-card:hover {
    border-color: var(--pixel-primary);
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(33, 150, 243, 0.3);
}

.card-header {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
    gap: 15px;
}

.pixel-icon {
    font-size: 1.5rem;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--pixel-primary);
    color: white;
    border: 2px solid var(--pixel-primary);
}

.card-meta {
    flex: 1;
    font-size: 0.6rem;
    color: var(--pixel-muted);
}

.card-meta span {
    display: block;
    margin-bottom: 5px;
}

.pixel-title {
    margin-bottom: 15px;
}

.pixel-title a {
    color: var(--pixel-text);
    text-decoration: none;
    font-size: 1rem;
    line-height: 1.4;
    transition: color 0.2s;
}

.pixel-title a:hover {
    color: var(--pixel-primary);
    text-shadow: 2px 2px 0px var(--pixel-secondary);
}

.pixel-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.pixel-tag {
    background: var(--pixel-secondary);
    color: white;
    padding: 5px 10px;
    font-size: 0.5rem;
    border: 1px solid var(--pixel-secondary);
    transition: all 0.2s;
}

.pixel-tag:hover {
    background: var(--pixel-accent);
    border-color: var(--pixel-accent);
    transform: scale(1.05);
}

/* 像素风页脚 */
.pixel-footer {
    border-top: 2px solid var(--pixel-border);
    padding: 30px 0;
    text-align: center;
}

.footer-content p {
    font-size: 0.6rem;
    color: var(--pixel-muted);
    margin-bottom: 15px;
}

.footer-links {
    display: flex;
    justify-content: center;
    gap: 20px;
}

.pixel-link {
    color: var(--pixel-primary);
    text-decoration: none;
    font-size: 0.6rem;
    transition: all 0.2s;
}

.pixel-link:hover {
    color: var(--pixel-accent);
    text-shadow: 1px 1px 0px var(--pixel-secondary);
}

/* 浮动像素特效 */
.pixel-effects {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
}

.floating-pixel {
    position: absolute;
    font-size: 1.5rem;
    opacity: 0.3;
    animation: float 6s ease-in-out infinite;
}

.floating-pixel:nth-child(1) {
    top: 20%;
    left: 10%;
    animation-delay: 0s;
}

.floating-pixel:nth-child(2) {
    top: 60%;
    right: 15%;
    animation-delay: 2s;
}

.floating-pixel:nth-child(3) {
    bottom: 30%;
    left: 20%;
    animation-delay: 4s;
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(180deg); }
}

/* 响应式设计 */
@media (max-width: 768px) {
    .container {
        padding: 15px;
    }
    
    .pixel-text {
        font-size: 1.8rem;
    }
    
    .pixel-nav {
        gap: 10px;
    }
    
    .pixel-btn {
        font-size: 0.6rem;
        padding: 8px 15px;
    }
    
    .articles-grid {
        grid-template-columns: 1fr;
        gap: 20px;
    }
    
    .pixel-card {
        padding: 20px;
    }
    
    .pixel-title a {
        font-size: 0.9rem;
    }
}

/* 加载动画 */
@keyframes pixelLoad {
    0% { opacity: 0; transform: scale(0.8); }
    100% { opacity: 1; transform: scale(1); }
}

.pixel-card {
    animation: pixelLoad 0.5s ease-out;
}

/* 滚动条样式 */
::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    background: var(--pixel-bg);
    border: 1px solid var(--pixel-border);
}

::-webkit-scrollbar-thumb {
    background: var(--pixel-primary);
    border: 1px solid var(--pixel-secondary);
}

::-webkit-scrollbar-thumb:hover {
    background: var(--pixel-accent);
}"""
    
    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(blue_white_styles)
    
    print("✅ 创建白蓝色像素风样式")

def create_fixed_article_pages(articles):
    """创建修复了图片路径的独立文章页面"""
    os.makedirs('articles', exist_ok=True)
    
    for article in articles:
        article_id = article['id']
        print(f"📝 创建文章页面: {article['title'][:30]}...")
        
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
        
        # 生成文章页面
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
        
        # 保存文章页面
        article_file = f"articles/{article_id}.html"
        with open(article_file, 'w', encoding='utf-8') as f:
            f.write(article_html)

if __name__ == "__main__":
    build_edgeone_site()
