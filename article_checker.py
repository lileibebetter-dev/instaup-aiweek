#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章检查和修复工具
检查文章数据完整性和图片路径问题
"""

import json
import os
import re
from pathlib import Path

def check_articles():
    """检查文章数据"""
    articles_file = 'posts/articles.json'
    
    if not os.path.exists(articles_file):
        print("❌ 文章文件不存在")
        return
    
    try:
        with open(articles_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except Exception as e:
        print(f"❌ 读取文章文件失败: {e}")
        return
    
    print(f"📚 总共找到 {len(articles)} 篇文章")
    print("=" * 50)
    
    issues = []
    
    for i, article in enumerate(articles):
        print(f"\n📖 检查文章 {i+1}: {article.get('title', '无标题')[:50]}...")
        
        # 检查基本字段
        required_fields = ['id', 'title', 'content', 'source', 'date']
        for field in required_fields:
            if field not in article:
                issues.append(f"文章 {i+1} 缺少字段: {field}")
                print(f"  ❌ 缺少字段: {field}")
            elif not article[field]:
                issues.append(f"文章 {i+1} 字段为空: {field}")
                print(f"  ❌ 字段为空: {field}")
        
        # 检查内容长度
        content = article.get('content', '')
        if len(content) < 100:
            issues.append(f"文章 {i+1} 内容过短: {len(content)} 字符")
            print(f"  ⚠️  内容过短: {len(content)} 字符")
        
        # 检查图片路径
        if content:
            img_pattern = r'src=["\']([^"\']*\.jpg[^"\']*)["\']'
            img_matches = re.findall(img_pattern, content)
            
            if img_matches:
                print(f"  🖼️  找到 {len(img_matches)} 张图片")
                
                for img_path in img_matches[:3]:  # 只检查前3张
                    # 清理路径
                    clean_path = img_path.replace('&amp;', '&')
                    if clean_path.startswith('./'):
                        clean_path = clean_path[2:]
                    
                    if not os.path.exists(clean_path):
                        issues.append(f"文章 {i+1} 图片不存在: {clean_path}")
                        print(f"    ❌ 图片不存在: {clean_path}")
                    else:
                        print(f"    ✅ 图片存在: {clean_path}")
            else:
                print(f"  📝 无图片内容")
    
    print("\n" + "=" * 50)
    print("🔍 检查结果汇总:")
    
    if issues:
        print(f"❌ 发现 {len(issues)} 个问题:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✅ 所有文章检查通过！")
    
    return issues

def fix_image_paths():
    """修复图片路径"""
    articles_file = 'posts/articles.json'
    
    try:
        with open(articles_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except Exception as e:
        print(f"❌ 读取文章文件失败: {e}")
        return
    
    fixed_count = 0
    
    for article in articles:
        content = article.get('content', '')
        if not content:
            continue
        
        # 修复图片路径
        original_content = content
        
        # 替换 ./images/ 为 images/
        content = content.replace('src="./images/', 'src="images/')
        
        # 替换 &amp; 为 &
        content = content.replace('&amp;', '&')
        
        if content != original_content:
            article['content'] = content
            fixed_count += 1
    
    if fixed_count > 0:
        try:
            with open(articles_file, 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
            print(f"✅ 修复了 {fixed_count} 篇文章的图片路径")
        except Exception as e:
            print(f"❌ 保存修复结果失败: {e}")
    else:
        print("ℹ️  没有需要修复的图片路径")

def generate_missing_images_report():
    """生成缺失图片报告"""
    articles_file = 'posts/articles.json'
    
    try:
        with open(articles_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except Exception as e:
        print(f"❌ 读取文章文件失败: {e}")
        return
    
    missing_images = []
    
    for i, article in enumerate(articles):
        content = article.get('content', '')
        if not content:
            continue
        
        img_pattern = r'src=["\']([^"\']*\.jpg[^"\']*)["\']'
        img_matches = re.findall(img_pattern, content)
        
        for img_path in img_matches:
            clean_path = img_path.replace('&amp;', '&').replace('./', '')
            if not os.path.exists(clean_path):
                missing_images.append({
                    'article_id': article.get('id'),
                    'article_title': article.get('title', '无标题'),
                    'image_path': clean_path,
                    'original_path': img_path
                })
    
    if missing_images:
        print(f"\n📋 缺失图片报告 ({len(missing_images)} 张):")
        print("-" * 80)
        for img in missing_images:
            print(f"文章: {img['article_title'][:30]}...")
            print(f"路径: {img['image_path']}")
            print("-" * 40)
    else:
        print("✅ 所有图片都存在")

def main():
    """主函数"""
    print("🔍 文章检查工具")
    print("=" * 50)
    
    # 检查文章
    issues = check_articles()
    
    # 修复图片路径
    print("\n🔧 修复图片路径...")
    fix_image_paths()
    
    # 生成缺失图片报告
    print("\n📋 生成缺失图片报告...")
    generate_missing_images_report()
    
    print("\n✅ 检查完成！")

if __name__ == "__main__":
    main()
