#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复文章内容可见性问题
移除 visibility: hidden; opacity: 0; 样式
"""

import json
import re

def fix_visibility():
    """修复文章内容的可见性问题"""
    
    # 读取文章数据
    with open('posts/articles.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    updated_count = 0
    
    for article in articles:
        content = article.get('content', '')
        
        if not content:
            continue
        
        # 修复 visibility: hidden; opacity: 0; 问题
        old_pattern = 'style="visibility: hidden; opacity: 0; "'
        new_pattern = 'style="visibility: visible; opacity: 1; "'
        
        if old_pattern in content:
            new_content = content.replace(old_pattern, new_pattern)
            article['content'] = new_content
            updated_count += 1
            print(f"📝 修复文章可见性: {article.get('title', 'Unknown')}")
    
    # 保存更新后的文章数据
    with open('posts/articles.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 修复了 {updated_count} 篇文章的可见性问题")

if __name__ == '__main__':
    try:
        fix_visibility()
        print("🎉 可见性修复完成!")
    except Exception as e:
        print(f"❌ 修复失败: {e}")
