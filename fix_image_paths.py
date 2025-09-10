#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复图片路径脚本
将文章内容中的图片路径更新为新的子文件夹结构
"""

import json
import re

def fix_image_paths():
    """修复文章内容中的图片路径"""
    
    # 读取文章数据
    with open('posts/articles.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    updated_count = 0
    
    for article in articles:
        article_id = article.get('id')
        content = article.get('content', '')
        
        if not article_id or not content:
            continue
        
        # 更新图片路径
        old_pattern = f'./images/{article_id}_'
        new_pattern = f'./images/{article_id}/'
        
        if old_pattern in content:
            new_content = content.replace(old_pattern, new_pattern)
            article['content'] = new_content
            updated_count += 1
            print(f"📝 更新文章路径: {article_id}")
    
    # 保存更新后的文章数据
    with open('posts/articles.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 更新了 {updated_count} 篇文章的图片路径")

if __name__ == '__main__':
    try:
        fix_image_paths()
        print("🎉 图片路径修复完成!")
    except Exception as e:
        print(f"❌ 修复失败: {e}")
