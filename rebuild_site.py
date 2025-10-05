#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import shutil
from pathlib import Path
from datetime import datetime

def rebuild_site():
    """完全重构网站 - 纯静态架构"""
    print("🏗️  开始重构网站架构...")
    
    # 清理旧文件
    cleanup_files = ['public', '_site', 'articles']
    for item in cleanup_files:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item)
            else:
                os.remove(item)
    
    # 读取文章数据
    with open('posts/articles.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    print(f"📚 找到 {len(articles)} 篇文章")
    
    # 1. 创建新的像素风主页
    create_pixel_homepage(articles)
    
    # 2. 创建像素风样式
    create_pixel_styles()
    
    # 3. 创建独立文章页面
    create_article_pages(articles)
    
    # 4. 创建EdgeOne Pages配置
    create_edgeone_config()
    
    print("\n🎉 网站重构完成！")
    print("📁 新的文件结构:")
    print("  - index.html (像素风主页)")
    print("  - styles.css (像素风样式)")
    print("  - articles/ (所有文章独立页面)")
    print("  - posts/ (文章数据)")
    print("  - images/ (图片资源)")

def create_pixel_homepage(articles):
    """创建像素风主页"""
    articles_html = ""
    for i, article in enumerate(articles):
        # 创建像素风格的卡片
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
    <title>云秒搭AI周报 | 像素风AI资讯平台</title>
    <meta name="description" content="像素风设计的AI资讯周报，每周精选前沿AI技术与应用">
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
                    <span class="pixel-subtitle">PIXEL AI DIGEST</span>
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
                <p class="pixel-text">© 2024 云秒搭AI周报 - 像素风设计</p>
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
    
    print("✅ 创建像素风主页")

def create_pixel_styles():
    """创建像素风样式"""
    pixel_styles = """/* 像素风AI周报样式 */
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

:root {
    --pixel-primary: #00ff41;
    --pixel-secondary: #008f11;
    --pixel-accent: #ff6b35;
    --pixel-bg: #0d1117;
    --pixel-card: #161b22;
    --pixel-text: #f0f6fc;
    --pixel-muted: #8b949e;
    --pixel-border: #30363d;
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
        linear-gradient(45deg, transparent 49%, rgba(0, 255, 65, 0.1) 50%, transparent 51%),
        linear-gradient(-45deg, transparent 49%, rgba(0, 255, 65, 0.1) 50%, transparent 51%);
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
    background: rgba(0, 255, 65, 0.05);
}

.pixel-logo {
    margin-bottom: 20px;
}

.pixel-text {
    display: block;
    font-size: 2.5rem;
    color: var(--pixel-primary);
    text-shadow: 3px 3px 0px var(--pixel-secondary);
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
    color: var(--pixel-bg);
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
    box-shadow: 2px 2px 0px #cc5529;
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
    background: linear-gradient(90deg, transparent, rgba(0, 255, 65, 0.2), transparent);
    transition: left 0.5s;
}

.pixel-card:hover::before {
    left: 100%;
}

.pixel-card:hover {
    border-color: var(--pixel-primary);
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0, 255, 65, 0.3);
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
    color: var(--pixel-bg);
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
    color: var(--pixel-bg);
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
        f.write(pixel_styles)
    
    print("✅ 创建像素风样式")

def create_article_pages(articles):
    """创建独立文章页面"""
    os.makedirs('articles', exist_ok=True)
    
    for article in articles:
        article_id = article['id']
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
            background: rgba(0, 255, 65, 0.05);
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
        }}
        
        .article-content img {{
            max-width: 100%;
            height: auto;
            border: 2px solid var(--pixel-border);
            margin: 15px 0;
            display: block;
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
        }}
        
        .action-btn:hover {{
            background: var(--pixel-primary);
            color: var(--pixel-bg);
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
            {article['content']}
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
        
        article_file = f"articles/{article_id}.html"
        with open(article_file, 'w', encoding='utf-8') as f:
            f.write(article_html)
        
        print(f"✅ 创建文章页面: {article['title'][:30]}...")

def create_edgeone_config():
    """创建EdgeOne Pages配置"""
    # 创建简化的配置文件
    edgeone_config = """{
  "name": "云秒搭AI周报",
  "description": "像素风AI资讯平台",
  "build": {
    "command": "python3 rebuild_site.py",
    "output": "/"
  },
  "routes": [
    {
      "src": "/article.html\\?id=(.*)",
      "dest": "/articles/$1.html"
    }
  ]
}"""
    
    with open('edgeone.json', 'w', encoding='utf-8') as f:
        f.write(edgeone_config)
    
    # 创建README
    readme_content = """# 云秒搭AI周报 - 像素风重构版

## 🎮 新特性
- **像素风UI设计** - 复古游戏风格界面
- **纯静态架构** - 完美兼容EdgeOne Pages
- **独立文章页面** - 每篇文章都有独立HTML文件
- **响应式设计** - 支持移动端和桌面端

## 🚀 部署说明

### EdgeOne Pages部署
1. **构建命令**: `python3 rebuild_site.py`
2. **输出目录**: `/` (根目录)
3. **分支**: `main`

### 文件结构
```
/
├── index.html          # 像素风主页
├── styles.css          # 像素风样式
├── articles/           # 独立文章页面
│   ├── article1.html
│   ├── article2.html
│   └── ...
├── posts/              # 文章数据
│   └── articles.json
└── images/             # 图片资源
    └── ...
```

## 🎨 设计特色
- 像素风字体 (Press Start 2P)
- 霓虹绿配色方案
- 复古游戏UI元素
- 动态像素背景
- 浮动特效元素

## 📱 功能特性
- 实时搜索过滤
- 响应式布局
- 独立文章页面
- 像素风动画效果
- 完美兼容EdgeOne Pages

## 🔧 技术栈
- 纯HTML/CSS/JavaScript
- 像素风设计系统
- 静态文件架构
- EdgeOne Pages优化
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ 创建EdgeOne Pages配置")

if __name__ == "__main__":
    rebuild_site()
