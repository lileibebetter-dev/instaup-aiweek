#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re

def get_article_icon(article):
    """根据文章类型返回对应的图标"""
    source = article.get('source', '').lower()
    title = article.get('title', '')
    article_id = article.get('id', '')
    
    # 周报文章：显示周数
    if ('周报' in source or '周报' in title or 
        article_id.startswith('weekly-report') or 
        'AI周报' in source):
        # 从标题中提取周数
        week_match = re.search(r'第(\d+)周', title)
        if week_match:
            week_num = week_match.group(1)
            return f'<span class="week-icon">{week_num}</span>'
        return '<span class="week-icon">周</span>'
    
    # 论文解读文章
    elif ('论文解读' in source or article_id.startswith('pdf-')):
        return '📄'
    
    # 公众号文章：尝试从内容中提取图片
    elif (article_id.startswith('wechat-') or 
          '公众号' in source or 
          source in ['关注前沿科技', '微信公众号', '数字生命卡兹克', '博阳']):
        # 从文章中提取第一张图片作为封面
        content = article.get('content', '')
        # 尝试多种图片匹配模式
        img_patterns = [
            r'<img[^>]+src="([^"]+)"',
            r'data-src="([^"]+)"',
            r'src="([^"]+)"'
        ]
        
        for pattern in img_patterns:
            img_match = re.search(pattern, content)
            if img_match:
                img_src = img_match.group(1)
                # 确保图片路径正确
                if not img_src.startswith('http') and not img_src.startswith('./'):
                    img_src = './' + img_src
                return f'<img src="{img_src}" class="cover-image" alt="封面图">'
        
        # 如果没有找到图片，使用默认公众号图标
        return '📱'
    
    # 默认图标
    return '📰'

def get_card_type_badge(article):
    """获取卡片右上角的类型标识"""
    source = article.get('source', '')
    article_id = article.get('id', '')
    
    # 周报文章
    if ('周报' in source or article_id.startswith('weekly-report') or 'AI周报' in source):
        return '<span class="type-badge weekly">周报</span>'
    
    # 论文解读文章
    elif ('论文解读' in source or article_id.startswith('pdf-')):
        return '<span class="type-badge paper">论文</span>'
    
    # 公众号文章
    elif (article_id.startswith('wechat-') or 
          '公众号' in source or 
          source in ['关注前沿科技', '微信公众号', '数字生命卡兹克', '博阳']):
        return '<span class="type-badge wechat">前沿</span>'
    
    # 默认
    return '<span class="type-badge default">AI</span>'

def build_simple_edgeone_site():
    """为EdgeOne Pages构建简化的白蓝色像素风网站"""
    print("🏗️  为EdgeOne Pages构建白蓝色像素风网站...")
    
    # 读取文章数据 (从项目根目录)
    with open('posts/articles.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    print(f"📚 找到 {len(articles)} 篇文章")
    
    # 1. 创建白蓝色像素风主页
    create_homepage(articles)
    
    # 2. 创建白蓝色像素风样式
    create_styles()
    
    # 3. 创建修复了图片路径的独立文章页面
    create_article_pages(articles)
    
    print("\n🎉 EdgeOne Pages构建完成！")

def create_homepage(articles):
    """创建白蓝色像素风主页"""
    articles_html = ""
    for i, article in enumerate(articles):
            # 获取图标和图片
            icon_content = get_article_icon(article)
            is_image = '<img' in icon_content and 'cover-image' in icon_content
            
            if is_image:
                # 如果有图片，将图片包装在链接中
                articles_html += f"""
                <div class="pixel-card" data-tags='{",".join(article.get("tags", [])[:4])}'>
                    <div class="card-image-container">
                        <a href="articles/{article['id']}.html" class="image-link">
                            {icon_content}
                        </a>
                        <div class="card-type-badge">
                            {get_card_type_badge(article)}
                        </div>
                        <div class="pixel-tags hover-tags">
                            {''.join([f'<span class="pixel-tag" data-href="articles/{article["id"]}.html">{tag}</span>' for tag in article.get('tags', [])[:4]])}
                        </div>
                    </div>
                    <div class="card-content">
                        <h2 class="pixel-title">
                            <a href="articles/{article['id']}.html" class="pixel-link" title="{article['title']}">
                                {article['title']}
                            </a>
                        </h2>
                    </div>
                </div>
                """
            else:
                # 如果没有图片，显示图标
                articles_html += f"""
                <div class="pixel-card" data-tags='{",".join(article.get("tags", [])[:4])}'>
                    <div class="card-image-container">
                        <div class="pixel-icon">
                            {icon_content}
                        </div>
                        <div class="card-type-badge">
                            {get_card_type_badge(article)}
                        </div>
                        <div class="pixel-tags hover-tags">
                            {''.join([f'<span class="pixel-tag" data-href="articles/{article["id"]}.html">{tag}</span>' for tag in article.get('tags', [])[:4]])}
                        </div>
                    </div>
                    <div class="card-content">
                        <h2 class="pixel-title">
                            <a href="articles/{article['id']}.html" class="pixel-link" title="{article['title']}">
                                {article['title']}
                            </a>
                        </h2>
                    </div>
                </div>
                """
    
    homepage_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>云秒搭AI周报 | 秒懂AI，洞见未来</title>
    <meta name="description" content="白蓝色像素风设计的AI资讯周报，每周精选前沿AI技术与应用">
    <link rel="stylesheet" href="styles.css">
    <link rel="icon" type="image/png" href="favicon.png">
    <!-- Ark Pixel 像素字体 -->
    <style>
        @font-face {{
            font-family: 'Ark Pixel';
            src: url('像素字70/ark-pixel-12px-monospaced-zh_cn.woff2') format('woff2'),
                 url('像素字70/ark-pixel-12px-monospaced-zh_cn.ttf') format('truetype');
            font-display: swap;
        }}
        @font-face {{
            font-family: 'Ark Pixel Latin';
            src: url('像素字70/ark-pixel-12px-monospaced-latin.woff2') format('woff2'),
                 url('像素字70/ark-pixel-12px-monospaced-latin.ttf') format('truetype');
            font-display: swap;
        }}
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
</head>
<body>
    <div class="pixel-bg"></div>
    
    <div class="container">
        <header class="pixel-header">
            <div class="header-content">
                <h1 class="pixel-logo">
                    <span class="pixel-text">云秒搭AI周报</span>
                    <span class="pixel-subtitle">秒懂AI，洞见未来</span>
                </h1>
                <div class="pixel-nav">
                    <button class="pixel-btn active">首页</button>
                    <button class="pixel-btn">周报</button>
                    <button class="pixel-btn">AI技术</button>
                    <button class="pixel-btn">关于</button>
                </div>
            </div>
        </header>
        
        <div class="search-section">
            <div class="pixel-search-box">
                <input type="text" placeholder="搜索AI资讯..." class="pixel-input">
                <button class="pixel-search-btn">🔍</button>
            </div>
        </div>
        
        <main class="articles-grid">
            {articles_html}
        </main>
        
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
    
    <div class="pixel-effects">
        <div class="floating-pixel">💻</div>
        <div class="floating-pixel">🤖</div>
        <div class="floating-pixel">⚡</div>
    </div>
    
    <script>
        // 保存原始内容
        let originalContent = null;
        let isAboutPage = false;
        
        // 标签点击事件
        document.addEventListener('click', function(e) {{
            if (e.target.classList.contains('pixel-tag') && e.target.dataset.href) {{
                window.location.href = e.target.dataset.href;
            }}
        }});
        
        // 搜索功能
        document.querySelector('.pixel-input').addEventListener('input', function(e) {{
            if (isAboutPage) return; // 在关于页面时不执行搜索
            
            const searchTerm = e.target.value.toLowerCase();
            const cards = document.querySelectorAll('.pixel-card');
            
            cards.forEach(card => {{
                const title = card.querySelector('.pixel-title').textContent.toLowerCase();
                const tags = card.querySelector('.hover-tags').textContent.toLowerCase();
                
                if (title.includes(searchTerm) || tags.includes(searchTerm)) {{
                    card.style.display = 'block';
                }} else {{
                    card.style.display = searchTerm ? 'none' : 'block';
                }}
            }});
        }});
        
        // 导航切换功能
        document.querySelectorAll('.pixel-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                const buttonText = this.textContent.trim();
                const cards = document.querySelectorAll('.pixel-card');
                const searchSection = document.querySelector('.search-section');
                const articlesGrid = document.querySelector('.articles-grid');
                
                // 移除所有按钮的active状态
                document.querySelectorAll('.pixel-btn').forEach(b => b.classList.remove('active'));
                // 添加当前按钮的active状态
                this.classList.add('active');
                
                if (buttonText === '首页') {{
                    // 恢复原始内容
                    isAboutPage = false;
                    if (searchSection) searchSection.style.display = 'block';
                    if (originalContent && articlesGrid) {{
                        articlesGrid.innerHTML = originalContent;
                    }} else {{
                        location.reload();
                    }}
                }} else if (buttonText === '周报') {{
                    isAboutPage = false;
                    if (searchSection) searchSection.style.display = 'block';
                    
                    // 恢复原始内容
                    if (originalContent && articlesGrid) {{
                        articlesGrid.innerHTML = originalContent;
                        // 重新获取卡片元素
                        const newCards = document.querySelectorAll('.pixel-card');
                        newCards.forEach(card => {{
                            const typeBadge = card.querySelector('.type-badge');
                            if (typeBadge && typeBadge.textContent.includes('周报')) {{
                                card.style.display = 'block';
                            }} else {{
                                card.style.display = 'none';
                            }}
                        }});
                    }} else {{
                        // 如果原始内容不存在，重新加载页面
                        location.reload();
                    }}
                }} else if (buttonText === 'AI技术') {{
                    isAboutPage = false;
                    if (searchSection) searchSection.style.display = 'block';
                    
                    // 恢复原始内容
                    if (originalContent && articlesGrid) {{
                        articlesGrid.innerHTML = originalContent;
                        // 重新获取卡片元素
                        const newCards = document.querySelectorAll('.pixel-card');
                        newCards.forEach(card => {{
                            const typeBadge = card.querySelector('.type-badge');
                            if (typeBadge && typeBadge.textContent.includes('论文')) {{
                                card.style.display = 'block';
                            }} else {{
                                card.style.display = 'none';
                            }}
                        }});
                    }} else {{
                        // 如果原始内容不存在，重新加载页面
                        location.reload();
                    }}
                }} else if (buttonText === '关于') {{
                    isAboutPage = true;
                    
                    // 保存原始内容（如果还没有保存）
                    if (!originalContent && articlesGrid) {{
                        originalContent = articlesGrid.innerHTML;
                    }}
                    
                    // 隐藏所有卡片和搜索框
                    if (searchSection) searchSection.style.display = 'none';
                    
                    // 创建关于页面内容
                    if (articlesGrid) {{
                        articlesGrid.innerHTML = `
                            <div style="text-align: center; padding: 60px 20px; max-width: 800px; margin: 0 auto;">
                                <h2 style="color: var(--pixel-primary); margin-bottom: 30px; font-size: 1.5rem;">关于云秒搭AI周报</h2>
                                <div style="background: var(--pixel-card); padding: 40px; border: 2px solid var(--pixel-border); border-radius: 8px; margin-bottom: 30px;">
                                    <p style="margin-bottom: 20px; line-height: 1.8; color: var(--pixel-text);">
                                        云秒搭AI周报是一个专注于AI技术前沿动态的资讯平台，我们致力于"秒懂AI，洞见未来"的理念。本平台为非商用，专为公司内部使用。
                                    </p>
                                    <p style="margin-bottom: 20px; line-height: 1.8; color: var(--pixel-text);">
                                        我们致力于为读者提供最新、最全面的AI技术资讯，包括：
                                    </p>
                                    <ul style="text-align: left; margin: 20px 0; padding-left: 30px;">
                                        <li style="margin-bottom: 10px; color: var(--pixel-text);">📰 每周AI行业动态分析</li>
                                        <li style="margin-bottom: 10px; color: var(--pixel-text);">📄 前沿论文解读与总结</li>
                                        <li style="margin-bottom: 10px; color: var(--pixel-text);">📱 优质公众号文章精选</li>
                                        <li style="margin-bottom: 10px; color: var(--pixel-text);">🔍 智能搜索与内容推荐</li>
                                    </ul>
                                    <p style="margin-top: 30px; line-height: 1.8; color: var(--pixel-text);">
                                        通过智能化的内容生成和人工编辑相结合，我们确保每一篇内容都具有高质量和时效性，让复杂的AI技术变得易懂易用。
                                    </p>
                                </div>
                                <div style="background: var(--pixel-card); padding: 30px; border: 2px solid var(--pixel-border); border-radius: 8px;">
                                    <h3 style="color: var(--pixel-primary); margin-bottom: 20px;">联系我们</h3>
                                    <p style="color: var(--pixel-text);">📧 邮箱: lilei@instaup.ai</p>
                                </div>
                            </div>
                        `;
                    }}
                }}
            }});
        }});
        
        // 页面加载时保存原始内容
        document.addEventListener('DOMContentLoaded', function() {{
            const articlesGrid = document.querySelector('.articles-grid');
            if (articlesGrid && !originalContent) {{
                originalContent = articlesGrid.innerHTML;
            }}
        }});
    </script>
</body>
</html>"""
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(homepage_content)
    
    print("✅ 创建白蓝色像素风主页")

def create_styles():
    """创建白蓝色像素风样式"""
    styles = """/* 白蓝色像素风AI周报样式 */
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
    --pixel-font: 'Ark Pixel', 'Ark Pixel Latin', 'Press Start 2P', 'Orbitron', 'Courier New', monospace;
    --pixel-font-cn: 'Ark Pixel', 'Press Start 2P', 'Courier New', monospace;
}

/* 面包屑导航样式 */
.breadcrumb {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    background: var(--pixel-card);
    border: 2px solid var(--pixel-border);
    padding: 15px 20px;
    margin: 0;
    font-family: var(--pixel-font);
    font-size: 0.7rem;
    border-radius: 0 0 8px 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.breadcrumb-item {
    display: inline-block;
    color: var(--pixel-muted);
}

.breadcrumb-item:not(:last-child)::after {
    content: " > ";
    margin: 0 8px;
    color: var(--pixel-primary);
    font-weight: bold;
}

.breadcrumb-link {
    color: var(--pixel-primary);
    text-decoration: none;
    transition: color 0.2s;
}

.breadcrumb-link:hover {
    color: var(--pixel-secondary);
    text-decoration: underline;
}

.breadcrumb-current {
    color: var(--pixel-text);
    font-weight: bold;
}

/* 为面包屑预留空间，避免内容被遮挡 */
.article-container {
    padding-top: 80px !important;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: var(--pixel-font);
    background: var(--pixel-bg);
    color: var(--pixel-text);
    line-height: 1.6;
    overflow-x: hidden;
}

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

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    position: relative;
    z-index: 1;
}

.pixel-header {
    text-align: center;
    margin-bottom: 40px;
    padding: 30px 0;
    border: 3px solid var(--pixel-primary);
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
}

.pixel-btn:hover,
.pixel-btn.active {
    background: var(--pixel-primary);
    color: white;
    border-color: var(--pixel-primary);
    transform: translate(-2px, -2px);
    box-shadow: 4px 4px 0px var(--pixel-secondary);
}

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

.articles-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 25px;
    margin-bottom: 60px;
}

.pixel-card {
    background: var(--pixel-card);
    border: 2px solid var(--pixel-border);
    padding: 0;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    height: 280px;
    display: flex;
    flex-direction: column;
    cursor: pointer;
}

.pixel-card:hover {
    border-color: var(--pixel-primary);
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(33, 150, 243, 0.3);
}

/* 新卡片布局样式 */
.card-image-container {
    position: relative;
    height: 220px;
    background: var(--pixel-primary);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}

.card-content {
    padding: 12px 15px;
    height: 60px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.card-type-badge {
    position: absolute;
    top: 8px;
    right: 8px;
    z-index: 20;
}

.type-badge {
    font-family: var(--pixel-font);
    font-size: 0.6rem;
    padding: 4px 8px;
    border-radius: 4px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    background: rgba(255, 255, 255, 0.9);
    color: var(--pixel-primary);
    font-weight: bold;
}

.hover-tags {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    z-index: 10;
    opacity: 0;
    transition: opacity 0.3s ease;
    justify-content: center;
    align-items: center;
    width: 90%;
}

.pixel-card:hover .hover-tags {
    opacity: 1;
}

.hover-tags .pixel-tag {
    background: rgba(255, 255, 255, 0.95);
    color: var(--pixel-primary);
    font-size: 0.7rem;
    padding: 6px 10px;
    border: 1px solid rgba(33, 150, 243, 0.3);
    border-radius: 4px;
    font-family: var(--pixel-font);
    font-weight: bold;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
    margin: 2px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.hover-tags .pixel-tag:hover {
    background: rgba(33, 150, 243, 0.1);
    border-color: var(--pixel-primary);
    transform: scale(1.05);
}

.card-header {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
    gap: 15px;
}

.pixel-icon {
    font-size: 1.5rem;
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.1);
    color: white;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 6px;
    flex-shrink: 0;
    backdrop-filter: blur(10px);
    position: relative;
    z-index: 5;
}

/* 当有封面图片时，隐藏图标背景 */
.card-image-container:has(.cover-image) .pixel-icon {
    background: transparent;
    border: none;
    backdrop-filter: none;
}

/* 周数图标样式 */
.week-icon {
    font-family: var(--pixel-font);
    font-size: 1.8rem;
    font-weight: bold;
    color: white;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

/* 图片链接样式 */
.image-link {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: block;
    z-index: 1;
}

/* 封面图片样式 */
.cover-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 0;
    position: absolute;
    top: 0;
    left: 0;
}

.card-meta {
    flex: 1;
    font-size: 0.65rem;
    color: var(--pixel-muted);
    font-family: var(--pixel-font);
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
    font-size: 0.85rem;
    line-height: 1.4;
    transition: color 0.2s;
    font-family: var(--pixel-font);
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
}

.pixel-title a:hover {
    color: var(--pixel-primary);
    text-shadow: 2px 2px 0px var(--pixel-secondary);
}

.pixel-title a[title]:hover,
.pixel-summary[title]:hover {
    cursor: help;
}

.pixel-summary {
    color: var(--pixel-muted);
    font-size: 0.75rem;
    line-height: 1.5;
    margin-bottom: 15px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    font-family: var(--pixel-font);
    flex: 1;
}

.pixel-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    flex-shrink: 0;
    margin-top: auto;
}

.pixel-tag {
    background: var(--pixel-secondary);
    color: white;
    padding: 5px 10px;
    font-size: 0.55rem;
    border: 1px solid var(--pixel-secondary);
    transition: all 0.2s;
    font-family: var(--pixel-font);
}

.pixel-tag:hover {
    background: var(--pixel-accent);
    border-color: var(--pixel-accent);
    transform: scale(1.05);
}

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

/* 论文解读和周报专用样式 */
.document-overview,
.deep-analysis,
.key-points,
.summary-recommendations,
.key-insights,
.application-guidance,
.weekly-overview,
.hot-topics,
.key-breakthroughs,
.industry-trends,
.deep-analysis,
.trend-outlook,
.recommended-reading {
    background: #ffffff;
    border: 2px solid var(--pixel-primary);
    border-radius: 12px;
    padding: 25px;
    margin: 25px 0;
    box-shadow: 0 4px 12px rgba(33, 150, 243, 0.15);
    position: relative;
}

.document-overview::before,
.deep-analysis::before,
.key-points::before,
.summary-recommendations::before,
.key-insights::before,
.application-guidance::before,
.weekly-overview::before,
.hot-topics::before,
.key-breakthroughs::before,
.industry-trends::before,
.trend-outlook::before,
.recommended-reading::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--pixel-primary), var(--pixel-secondary), var(--pixel-accent));
    border-radius: 12px 12px 0 0;
}

.document-overview h2,
.deep-analysis h2,
.key-points h2,
.summary-recommendations h2,
.key-insights h2,
.application-guidance h2,
.weekly-overview h2,
.hot-topics h2,
.key-breakthroughs h2,
.industry-trends h2,
.trend-outlook h2,
.recommended-reading h2 {
    color: var(--pixel-primary);
    font-size: 1.1rem;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 3px solid var(--pixel-primary);
    font-family: 'Press Start 2P', monospace;
    text-shadow: 1px 1px 2px rgba(33, 150, 243, 0.3);
}

.document-overview h3,
.deep-analysis h3,
.key-points h3,
.summary-recommendations h3,
.key-insights h3,
.application-guidance h3 {
    color: var(--pixel-secondary);
    font-size: 0.9rem;
    margin: 20px 0 15px 0;
    font-family: 'Press Start 2P', monospace;
    padding-left: 15px;
    border-left: 4px solid var(--pixel-secondary);
}

.document-overview p,
.deep-analysis p,
.key-points p,
.summary-recommendations p,
.key-insights p,
.application-guidance p,
.weekly-overview p,
.hot-topics p,
.key-breakthroughs p,
.industry-trends p,
.trend-outlook p,
.recommended-reading p {
    font-size: 0.95rem;
    line-height: 1.8;
    margin-bottom: 16px;
    color: #333;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
    text-align: justify;
}

.document-overview ul,
.deep-analysis ul,
.key-points ul,
.summary-recommendations ul,
.key-insights ul,
.application-guidance ul,
.weekly-overview ul,
.hot-topics ul,
.key-breakthroughs ul,
.industry-trends ul,
.trend-outlook ul,
.recommended-reading ul {
    margin: 16px 0;
    padding-left: 25px;
}

.document-overview li,
.deep-analysis li,
.key-points li,
.summary-recommendations li,
.key-insights li,
.application-guidance li,
.weekly-overview li,
.hot-topics li,
.key-breakthroughs li,
.industry-trends li,
.trend-outlook li,
.recommended-reading li {
    font-size: 0.95rem;
    line-height: 1.7;
    margin-bottom: 12px;
    color: #333;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
    position: relative;
}

.document-overview li::before,
.deep-analysis li::before,
.key-points li::before,
.summary-recommendations li::before,
.key-insights li::before,
.application-guidance li::before,
.weekly-overview li::before,
.hot-topics li::before,
.key-breakthroughs li::before,
.industry-trends li::before,
.trend-outlook li::before,
.recommended-reading li::before {
    content: '▶';
    color: var(--pixel-primary);
    font-weight: bold;
    position: absolute;
    left: -20px;
}

.document-overview strong,
.deep-analysis strong,
.key-points strong,
.summary-recommendations strong,
.key-insights strong,
.application-guidance strong,
.weekly-overview strong,
.hot-topics strong,
.key-breakthroughs strong,
.industry-trends strong,
.trend-outlook strong,
.recommended-reading strong {
    color: var(--pixel-primary);
    font-weight: 600;
    background: #ffffff;
    padding: 2px 6px;
    border-radius: 4px;
}

/* 下载区域样式 */
.download-section {
    background: linear-gradient(135deg, var(--pixel-card) 0%, rgba(33, 150, 243, 0.1) 100%);
    border: 2px solid var(--pixel-primary);
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
    text-align: center;
}

.download-section h3 {
    color: var(--pixel-primary);
    font-size: 0.8rem;
    margin-bottom: 10px;
    font-family: 'Press Start 2P', monospace;
}

.download-section p {
    font-size: 0.6rem;
    color: var(--pixel-text);
    margin-bottom: 15px;
    font-family: 'Press Start 2P', monospace;
}

.download-link {
    display: inline-block;
    padding: 10px 20px;
    background: var(--pixel-primary);
    color: white !important;
    text-decoration: none;
    border-radius: 5px;
    font-size: 0.6rem;
    font-family: 'Press Start 2P', monospace;
    transition: all 0.2s;
}

.download-link:hover {
    background: var(--pixel-secondary);
    transform: translate(-2px, -2px);
    box-shadow: 4px 4px 0px var(--pixel-accent);
}

/* 周报专用样式 */
.weekly-report-content {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
}

.weekly-report-content h1,
.weekly-report-content h2,
.weekly-report-content h3 {
    color: var(--pixel-primary);
    margin: 20px 0 15px 0;
    font-family: 'Press Start 2P', monospace;
}

.weekly-report-content h1 {
    font-size: 1.2rem;
    text-align: center;
    margin-bottom: 30px;
    padding: 20px;
    background: #ffffff;
    border: 2px solid var(--pixel-primary);
    border-radius: 12px;
}

.weekly-report-content h2 {
    font-size: 1.1rem;
}

.weekly-report-content h3 {
    font-size: 0.9rem;
}

.weekly-report-content p {
    font-size: 0.95rem;
    line-height: 1.8;
    margin-bottom: 16px;
    color: #333;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
    text-align: justify;
}

.weekly-report-content ul,
.weekly-report-content ol {
    margin: 16px 0;
    padding-left: 25px;
}

.weekly-report-content li {
    font-size: 0.95rem;
    line-height: 1.7;
    margin-bottom: 12px;
    color: #333;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
    position: relative;
}

.weekly-report-content li::before {
    content: '▶';
    color: var(--pixel-primary);
    font-weight: bold;
    position: absolute;
    left: -20px;
}

.weekly-report-content strong {
    color: var(--pixel-primary);
    font-weight: 600;
    background: #ffffff;
    padding: 2px 6px;
    border-radius: 4px;
}

.weekly-report-content em {
    color: var(--pixel-muted);
    font-style: normal;
}

/* 周报头部样式 */
.weekly-report-header {
    text-align: center;
    margin-bottom: 30px;
    padding: 20px;
    background: #ffffff;
    border: 2px solid var(--pixel-primary);
    border-radius: 12px;
}

.weekly-report-header h1 {
    color: var(--pixel-primary);
    font-size: 1.2rem;
    margin-bottom: 10px;
    font-family: 'Press Start 2P', monospace;
}

.report-subtitle {
    color: var(--pixel-muted);
    font-size: 0.8rem;
    font-family: 'Press Start 2P', monospace;
}"""
    
    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(styles)
    
    print("✅ 创建白蓝色像素风样式")

def create_article_pages(articles):
    """创建修复了图片路径的独立文章页面"""
    os.makedirs('articles', exist_ok=True)
    
    for article in articles:
        article_id = article['id']
        print(f"📝 创建文章页面: {article['title'][:30]}...")
        
        # 使用正则表达式修复图片路径和可见性问题
        content = article['content']
        # 修复转义的换行符和引号
        content = content.replace('\\n', '\n')
        content = content.replace('\\"', '"')
        # 修复 data-src 路径 (匹配 ./images/ 和 images/)
        content = re.sub(r'data-src="\.?/?images/', 'data-src="../images/', content)
        # 修复 src 路径 (匹配 ./images/ 和 images/)
        content = re.sub(r'src="\.?/?images/', 'src="../images/', content)
        # 修复可见性问题：移除 visibility: hidden 和 opacity: 0
        content = re.sub(r'style="[^"]*visibility:\s*hidden[^"]*"', 'style=""', content)
        content = re.sub(r'style="[^"]*opacity:\s*0[^"]*"', 'style=""', content)
        # 修复包含 visibility: hidden; opacity: 0; 的样式
        content = re.sub(r'style="[^"]*visibility:\s*hidden;\s*opacity:\s*0;[^"]*"', 'style=""', content)
        
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
        .article-container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            padding-top: 80px !important; /* 为固定面包屑预留空间 */
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
        <!-- 面包屑导航 -->
        <nav class="breadcrumb">
            <span class="breadcrumb-item">
                <a href="../index.html" class="breadcrumb-link">🏠 首页</a>
            </span>
            <span class="breadcrumb-item">
                <a href="../index.html" class="breadcrumb-link">{"📰 周报" if "周报" in article.get('source', '') else "🤖 AI技术" if article.get('source', '') == "论文解读" else "📱 公众号文章"}</a>
            </span>
            <span class="breadcrumb-item breadcrumb-current">{article['title']}</span>
        </nav>
        
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
            {content}
        </main>
        
        <div class="article-actions">
            <a href="../index.html" class="action-btn">← 返回首页</a>
            <a href="{article['url']}" target="_blank" class="action-btn">查看原文 →</a>
        </div>
    </div>
    
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

if __name__ == "__main__":
    build_simple_edgeone_site()
