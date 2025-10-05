#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import os
from bs4 import BeautifulSoup

ARTICLES_FILE = 'posts/articles.json'

def load_articles():
    """加载文章数据"""
    if not os.path.exists(ARTICLES_FILE):
        return []
    with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_articles(articles):
    """保存文章数据"""
    with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

def fix_article_visibility(articles):
    """修复文章内容被隐藏的问题"""
    print("🔧 修复文章可见性问题...")
    fixed_count = 0
    
    for i, article in enumerate(articles):
        content = article.get('content', '')
        if not content:
            continue
            
        # 检查是否有visibility: hidden的问题
        if 'visibility: hidden' in content or 'opacity: 0' in content:
            print(f"📖 发现隐藏文章: {article.get('title', '未知标题')[:30]}...")
            
            # 使用正则表达式替换隐藏样式
            # 替换 visibility: hidden 为 visibility: visible
            content = re.sub(r'visibility:\s*hidden', 'visibility: visible', content)
            # 替换 opacity: 0 为 opacity: 1
            content = re.sub(r'opacity:\s*0', 'opacity: 1', content)
            
            # 如果还有style="visibility: hidden; opacity: 0;"这种完整的情况
            content = re.sub(r'style="([^"]*?)visibility:\s*hidden([^"]*?)"', 
                           lambda m: f'style="{m.group(1)}visibility: visible{m.group(2)}"', 
                           content)
            content = re.sub(r'style="([^"]*?)opacity:\s*0([^"]*?)"', 
                           lambda m: f'style="{m.group(1)}opacity: 1{m.group(2)}"', 
                           content)
            
            article['content'] = content
            fixed_count += 1
            print(f"  ✅ 已修复可见性")
    
    if fixed_count > 0:
        save_articles(articles)
        print(f"✅ 修复了 {fixed_count} 篇文章的可见性问题")
    else:
        print("ℹ️  没有发现可见性问题")
    
    return fixed_count

def main():
    print("🔧 文章可见性修复工具")
    print("=" * 50)
    
    import os
    articles = load_articles()
    print(f"📚 总共找到 {len(articles)} 篇文章")
    
    fixed_count = fix_article_visibility(articles)
    
    print(f"\n✅ 修复完成！共修复 {fixed_count} 篇文章")

if __name__ == "__main__":
    main()
