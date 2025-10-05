#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片路径修复工具
修复文章中的图片路径问题
"""

import json
import os
import re
from pathlib import Path

def fix_image_paths():
    """修复文章中的图片路径"""
    articles_file = 'posts/articles.json'
    
    try:
        with open(articles_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except Exception as e:
        print(f"❌ 读取文章文件失败: {e}")
        return
    
    fixed_count = 0
    
    for i, article in enumerate(articles):
        content = article.get('content', '')
        if not content:
            continue
        
        original_content = content
        
        # 修复图片路径模式
        # 将 aIltul1-Pb8Oz7hrfWC8dA_xxx.jpg 替换为 wechat-aIltul1-Pb8Oz7hrfWC8dA_xxx.jpg
        content = re.sub(
            r'src="images/aIltul1-Pb8Oz7hrfWC8dA/([^"]+)"',
            r'src="images/wechat-aIltul1-Pb8Oz7hrfWC8dA/\1"',
            content
        )
        
        # 将 tV0vAj0pXv04xZkod8H7hw_xxx.jpg 替换为 wechat-tV0vAj0pXv04xZkod8H7hw/xxx.jpg
        content = re.sub(
            r'src="images/tV0vAj0pXv04xZkod8H7hw/([^"]+)"',
            r'src="images/wechat-tV0vAj0pXv04xZkod8H7hw/\1"',
            content
        )
        
        # 将 rADj7tBbJtEecfs18h17BQ_xxx.jpg 替换为 wechat-rADj7tBbJtEecfs18h17BQ/rADj7tBbJtEecfs18h17BQ_xxx.jpg
        content = re.sub(
            r'src="images/rADj7tBbJtEecfs18h17BQ/([^"]+)"',
            r'src="images/wechat-rADj7tBbJtEecfs18h17BQ/rADj7tBbJtEecfs18h17BQ_\1"',
            content
        )
        
        # 修复 &amp; 为 &
        content = content.replace('&amp;', '&')
        
        if content != original_content:
            article['content'] = content
            fixed_count += 1
            print(f"✅ 修复文章 {i+1}: {article.get('title', '无标题')[:50]}...")
    
    if fixed_count > 0:
        try:
            with open(articles_file, 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
            print(f"\n✅ 修复了 {fixed_count} 篇文章的图片路径")
        except Exception as e:
            print(f"❌ 保存修复结果失败: {e}")
    else:
        print("ℹ️  没有需要修复的图片路径")

def check_image_files():
    """检查实际存在的图片文件"""
    images_dir = 'images'
    
    print("🔍 检查实际存在的图片文件:")
    print("-" * 50)
    
    for root, dirs, files in os.walk(images_dir):
        if files:
            print(f"\n📁 目录: {root}")
            for file in files[:5]:  # 只显示前5个文件
                print(f"  📄 {file}")
            if len(files) > 5:
                print(f"  ... 还有 {len(files) - 5} 个文件")

def create_missing_image_placeholders():
    """为缺失的图片创建占位符"""
    articles_file = 'posts/articles.json'
    
    try:
        with open(articles_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except Exception as e:
        print(f"❌ 读取文章文件失败: {e}")
        return
    
    # 创建缺失图片的占位符HTML
    missing_images = []
    
    for article in articles:
        content = article.get('content', '')
        if not content:
            continue
        
        img_pattern = r'src="images/([^"]+\.jpg[^"]*)"'
        img_matches = re.findall(img_pattern, content)
        
        for img_path in img_matches:
            full_path = f"images/{img_path}"
            if not os.path.exists(full_path):
                missing_images.append(full_path)
    
    if missing_images:
        print(f"\n📋 发现 {len(missing_images)} 张缺失图片")
        
        # 创建占位符HTML
        placeholder_html = '''
        <div style="border: 2px dashed #ccc; padding: 20px; text-align: center; background-color: #f9f9f9; margin: 20px 0;">
            <p style="color: #666; margin: 0;">🖼️ 图片加载失败</p>
            <p style="color: #999; font-size: 12px; margin: 5px 0 0 0;">图片路径: {}</p>
        </div>
        '''
        
        # 为每篇文章替换缺失的图片
        for article in articles:
            content = article.get('content', '')
            if not content:
                continue
            
            original_content = content
            
            # 替换缺失的图片
            for missing_img in missing_images:
                if missing_img in content:
                    placeholder = placeholder_html.format(missing_img)
                    content = content.replace(f'src="{missing_img}"', f'data-src="{missing_img}"')
                    # 在图片标签后添加占位符
                    content = re.sub(
                        rf'<img[^>]*data-src="{re.escape(missing_img)}"[^>]*>',
                        lambda m: m.group(0) + placeholder,
                        content
                    )
            
            if content != original_content:
                article['content'] = content
                print(f"✅ 为文章添加图片占位符: {article.get('title', '无标题')[:50]}...")
        
        # 保存修改
        try:
            with open(articles_file, 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
            print(f"✅ 已为缺失图片添加占位符")
        except Exception as e:
            print(f"❌ 保存占位符失败: {e}")
    else:
        print("✅ 所有图片都存在")

def main():
    """主函数"""
    print("🔧 图片路径修复工具")
    print("=" * 50)
    
    # 检查实际存在的图片文件
    check_image_files()
    
    # 修复图片路径
    print("\n🔧 修复图片路径...")
    fix_image_paths()
    
    # 为缺失图片创建占位符
    print("\n🖼️ 为缺失图片创建占位符...")
    create_missing_image_placeholders()
    
    print("\n✅ 修复完成！")

if __name__ == "__main__":
    main()
