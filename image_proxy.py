#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片代理脚本
用于下载微信公众号图片并保存到本地，避免防盗链问题
"""

import requests
import os
import re
import hashlib
from urllib.parse import urlparse
import json
from datetime import datetime

class ImageProxy:
    def __init__(self, images_dir='images'):
        self.images_dir = images_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://mp.weixin.qq.com/',
        })
        
        # 创建图片目录
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
    
    def download_image(self, image_url, article_id=None):
        """下载图片并返回本地路径"""
        try:
            # 生成文件名
            parsed_url = urlparse(image_url)
            filename = os.path.basename(parsed_url.path)
            
            # 如果没有文件名，使用URL的hash
            if not filename or '.' not in filename:
                url_hash = hashlib.md5(image_url.encode()).hexdigest()
                filename = f"{url_hash}.jpg"
            
            # 添加文章ID前缀避免冲突
            if article_id:
                filename = f"{article_id}_{filename}"
            
            local_path = os.path.join(self.images_dir, filename)
            
            # 如果文件已存在，直接返回
            if os.path.exists(local_path):
                return f"./{self.images_dir}/{filename}"
            
            # 下载图片
            print(f"正在下载图片: {image_url}")
            response = self.session.get(image_url, timeout=30)
            response.raise_for_status()
            
            # 保存图片
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            print(f"图片已保存: {local_path}")
            return f"./{self.images_dir}/{filename}"
            
        except Exception as e:
            print(f"下载图片失败 {image_url}: {e}")
            return image_url  # 返回原URL作为备用
    
    def process_article_images(self, article_content, article_id):
        """处理文章中的所有图片"""
        if not article_content:
            return article_content
        
        # 查找所有图片标签
        img_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
        img_matches = re.findall(img_pattern, article_content)
        
        for img_url in img_matches:
            if 'mmbiz.qpic.cn' in img_url or 'res.wx.qq.com' in img_url:
                # 下载图片
                local_path = self.download_image(img_url, article_id)
                
                # 替换URL
                article_content = article_content.replace(img_url, local_path)
        
        return article_content

def main():
    """主函数 - 处理现有文章中的图片"""
    proxy = ImageProxy()
    
    # 读取文章数据
    try:
        with open('posts/articles.json', 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except Exception as e:
        print(f"读取文章数据失败: {e}")
        return
    
    updated_count = 0
    
    for article in articles:
        if article.get('content') and ('mmbiz.qpic.cn' in article['content'] or 'res.wx.qq.com' in article['content']):
            print(f"\n处理文章: {article['title']}")
            
            # 处理图片
            original_content = article['content']
            article['content'] = proxy.process_article_images(article['content'], article['id'])
            
            if original_content != article['content']:
                updated_count += 1
                print(f"已更新文章图片: {article['title']}")
    
    if updated_count > 0:
        # 保存更新后的文章数据
        try:
            with open('posts/articles.json', 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
            print(f"\n✅ 已更新 {updated_count} 篇文章的图片")
        except Exception as e:
            print(f"保存文章数据失败: {e}")
    else:
        print("\n没有需要处理的图片")

if __name__ == "__main__":
    main()
