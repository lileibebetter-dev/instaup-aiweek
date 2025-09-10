#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片重新组织脚本
将现有图片按文章ID分文件夹存储
"""

import os
import json
import shutil
import re
from pathlib import Path

def reorganize_images():
    """重新组织图片存储结构"""
    
    # 读取文章数据
    with open('posts/articles.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    # 创建新的图片目录结构
    images_dir = Path('images')
    if not images_dir.exists():
        print("❌ images目录不存在")
        return
    
    # 统计信息
    moved_count = 0
    article_dirs_created = set()
    
    print("🔄 开始重新组织图片结构...")
    
    # 遍历所有文章
    for article in articles:
        article_id = article.get('id')
        if not article_id:
            continue
            
        # 为每篇文章创建单独的文件夹
        article_dir = images_dir / article_id
        if not article_dir.exists():
            article_dir.mkdir(parents=True, exist_ok=True)
            article_dirs_created.add(article_id)
            print(f"📁 创建文件夹: {article_id}")
        
        # 查找属于这篇文章的图片
        pattern = f"^{article_id}_"
        for image_file in images_dir.glob(f"{article_id}_*"):
            if image_file.is_file():
                # 移动图片到对应的文章文件夹
                new_path = article_dir / image_file.name
                if not new_path.exists():
                    shutil.move(str(image_file), str(new_path))
                    moved_count += 1
                    print(f"📷 移动图片: {image_file.name} -> {article_id}/")
    
    print(f"\n✅ 重新组织完成!")
    print(f"📊 统计信息:")
    print(f"   - 创建了 {len(article_dirs_created)} 个文章文件夹")
    print(f"   - 移动了 {moved_count} 张图片")
    
    # 更新文章内容中的图片路径
    update_article_paths(articles)
    
    return moved_count, len(article_dirs_created)

def update_article_paths(articles):
    """更新文章内容中的图片路径"""
    
    print("\n🔄 更新文章内容中的图片路径...")
    
    updated_articles = []
    updated_count = 0
    
    for article in articles:
        article_id = article.get('id')
        content = article.get('content', '')
        
        if not article_id or not content:
            updated_articles.append(article)
            continue
        
        # 更新图片路径
        old_pattern = f'./images/{article_id}_'
        new_pattern = f'./images/{article_id}/'
        
        if old_pattern in content:
            new_content = content.replace(old_pattern, new_pattern)
            article['content'] = new_content
            updated_count += 1
            print(f"📝 更新文章路径: {article_id}")
        
        updated_articles.append(article)
    
    # 保存更新后的文章数据
    with open('posts/articles.json', 'w', encoding='utf-8') as f:
        json.dump(updated_articles, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 更新了 {updated_count} 篇文章的图片路径")

def cleanup_empty_images_dir():
    """清理空的images目录中的文件"""
    
    images_dir = Path('images')
    if not images_dir.exists():
        return
    
    print("\n🧹 清理根目录下的图片文件...")
    
    # 查找根目录下剩余的图片文件
    remaining_files = []
    for file in images_dir.iterdir():
        if file.is_file() and file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            remaining_files.append(file)
    
    if remaining_files:
        print(f"⚠️  发现 {len(remaining_files)} 个未分类的图片文件:")
        for file in remaining_files:
            print(f"   - {file.name}")
        
        # 询问是否删除
        response = input("\n是否删除这些未分类的图片文件? (y/N): ").strip().lower()
        if response == 'y':
            for file in remaining_files:
                file.unlink()
                print(f"🗑️  删除: {file.name}")
            print("✅ 清理完成")
        else:
            print("⏭️  跳过清理")
    else:
        print("✅ 没有发现未分类的图片文件")

if __name__ == '__main__':
    try:
        moved_count, dirs_created = reorganize_images()
        cleanup_empty_images_dir()
        
        print(f"\n🎉 图片重新组织完成!")
        print(f"📁 新的目录结构:")
        print(f"   images/")
        print(f"   ├── wechat-tV0vAj0pXv04xZkod8H7hw/")
        print(f"   ├── wechat-aIltul1-Pb8Oz7hrfWC8dA/")
        print(f"   ├── wechat-rADj7tBbJtEecfs18h17BQ/")
        print(f"   └── ...")
        
    except Exception as e:
        print(f"❌ 重新组织失败: {e}")
