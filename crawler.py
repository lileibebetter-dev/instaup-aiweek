#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章爬虫
用于抓取微信公众号文章内容并重新排版到网站
"""

import requests
import json
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import html
import os
import hashlib

class WeChatArticleCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # 创建图片目录
        self.images_dir = 'images'
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
    
    def extract_article_id(self, url):
        """从微信公众号URL中提取文章ID"""
        try:
            parsed = urlparse(url)
            if 'mp.weixin.qq.com' in parsed.netloc:
                # 提取URL中的文章ID
                path_parts = parsed.path.split('/')
                if len(path_parts) >= 2:
                    return path_parts[-1]
            return None
        except Exception as e:
            print(f"提取文章ID失败: {e}")
            return None
    
    def fetch_article_content(self, url):
        """抓取文章内容"""
        try:
            print(f"正在抓取文章: {url}")
            
            # 尝试直接访问
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # 检查是否被重定向到验证页面
            if "环境异常" in response.text or "完成验证" in response.text:
                print("⚠️  文章需要验证，尝试使用备用方法...")
                return self.fetch_with_alternative_method(url)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取文章信息
            article_data = self.parse_article_content(soup, url)
            return article_data
            
        except requests.RequestException as e:
            print(f"❌ 网络请求失败: {e}")
            return None
        except Exception as e:
            print(f"❌ 抓取失败: {e}")
            return None
    
    def fetch_with_alternative_method(self, url):
        """备用抓取方法"""
        try:
            # 尝试使用不同的User-Agent
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9',
            }
            
            response = self.session.get(url, headers=headers, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 如果还是需要验证，返回模拟数据
            if "环境异常" in response.text:
                print("⚠️  文章需要验证，生成模拟内容...")
                return self.generate_mock_content(url)
            
            return self.parse_article_content(soup, url)
            
        except Exception as e:
            print(f"❌ 备用方法也失败: {e}")
            return self.generate_mock_content(url)
    
    def generate_mock_content(self, url):
        """生成模拟内容（当无法抓取时）"""
        article_id = self.extract_article_id(url) or "unknown"
        
        return {
            'id': f'wechat-{article_id}',
            'title': '微信公众号文章',
            'source': '微信公众号',
            'summary': '这是一篇来自微信公众号的文章，由于访问限制，无法获取完整内容。请点击"阅读原文"查看完整内容。',
            'url': url,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'tags': ['微信公众号', 'AI技术'],
            'content': '''
                <h2>微信公众号文章</h2>
                <p>由于微信公众号的访问限制，我们无法直接获取这篇文章的完整内容。</p>
                <p>请点击下方的"阅读原文"按钮，在新窗口中查看完整的文章内容。</p>
                <blockquote>
                    <p><strong>提示：</strong>如果遇到"环境异常"提示，请按照页面指引完成验证后即可正常访问。</p>
                </blockquote>
                <p>我们正在努力改进抓取技术，以便为您提供更好的阅读体验。</p>
            '''
        }
    
    def parse_article_content(self, soup, url):
        """解析文章内容"""
        try:
            # 生成文章ID
            article_id = self.extract_article_id(url) or f"article-{int(time.time())}"
            
            # 提取标题
            title = self.extract_title(soup)
            
            # 提取作者/来源
            source = self.extract_source(soup)
            
            # 提取正文内容
            content = self.extract_content(soup)
            
            # 处理图片下载
            content = self.process_article_images(content, article_id)
            
            # 生成摘要
            summary = self.generate_summary(content)
            
            # 提取标签
            tags = self.extract_tags(content, title)
            
            return {
                'id': f'wechat-{article_id}',
                'title': title,
                'source': source,
                'summary': summary,
                'url': url,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'tags': tags,
                'content': content
            }
            
        except Exception as e:
            print(f"❌ 解析内容失败: {e}")
            return None
    
    def extract_title(self, soup):
        """提取文章标题"""
        # 尝试多种选择器
        title_selectors = [
            'h1#activity-name',
            'h1.rich_media_title',
            'h1',
            'title'
        ]
        
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = title_elem.get_text().strip()
                if title and len(title) > 3:
                    return title
        
        return "微信公众号文章"
    
    def extract_source(self, soup):
        """提取文章来源"""
        # 尝试提取公众号名称
        source_selectors = [
            '.profile_nickname',
            '.rich_media_meta_text',
            '.author'
        ]
        
        for selector in source_selectors:
            source_elem = soup.select_one(selector)
            if source_elem:
                source = source_elem.get_text().strip()
                if source:
                    return source
        
        return "微信公众号"
    
    def extract_content(self, soup):
        """提取文章正文内容"""
        # 尝试多种内容选择器
        content_selectors = [
            '#js_content',
            '.rich_media_content',
            '.content',
            'article'
        ]
        
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                # 清理内容
                content = self.clean_content(content_elem)
                if content and len(content) > 100:
                    return content
        
        return "<p>无法提取文章内容，请点击原文链接查看。</p>"
    
    def clean_content(self, content_elem):
        """清理和重新格式化内容"""
        # 移除不需要的元素
        for elem in content_elem.find_all(['script', 'style', 'noscript']):
            elem.decompose()
        
        # 移除隐藏样式
        for elem in content_elem.find_all(attrs={'style': True}):
            style = elem.get('style', '')
            # 移除visibility: hidden和opacity: 0等隐藏样式
            if 'visibility: hidden' in style or 'opacity: 0' in style:
                # 保留其他样式，只移除隐藏相关的
                new_style = re.sub(r'visibility\s*:\s*hidden[^;]*;?', '', style)
                new_style = re.sub(r'opacity\s*:\s*0[^;]*;?', '', style)
                new_style = re.sub(r';\s*;', ';', new_style)  # 清理多余的分号
                new_style = new_style.strip('; ')
                if new_style:
                    elem['style'] = new_style
                else:
                    del elem['style']
        
        # 处理图片
        for img in content_elem.find_all('img'):
            src = img.get('data-src') or img.get('src')
            if src:
                img['src'] = src
                img['alt'] = img.get('alt', '图片')
                # 添加响应式样式
                img['style'] = 'max-width: 100%; height: auto; display: block; margin: 16px auto;'
        
        # 处理链接
        for link in content_elem.find_all('a'):
            href = link.get('href')
            if href and not href.startswith('http'):
                link['href'] = f"https://mp.weixin.qq.com{href}"
            link['target'] = '_blank'
            link['rel'] = 'noopener'
        
        # 转换为HTML字符串
        content_html = str(content_elem)
        
        # 清理HTML
        content_html = re.sub(r'\s+', ' ', content_html)
        content_html = re.sub(r'>\s+<', '><', content_html)
        
        return content_html
    
    def generate_summary(self, content):
        """生成文章摘要"""
        try:
            # 移除HTML标签
            text_content = re.sub(r'<[^>]+>', '', content)
            text_content = re.sub(r'\s+', ' ', text_content).strip()
            
            # 取前200个字符作为摘要
            if len(text_content) > 200:
                summary = text_content[:200] + "..."
            else:
                summary = text_content
            
            return summary
        except:
            return "这是一篇来自微信公众号的文章，内容精彩，值得一读。"
    
    def extract_tags(self, content, title):
        """提取文章标签"""
        tags = []
        
        # 从标题和内容中提取关键词
        text = f"{title} {content}".lower()
        
        # AI相关关键词
        ai_keywords = ['ai', '人工智能', '机器学习', '深度学习', '大模型', 'chatgpt', 'gpt', 'llm', '神经网络']
        tech_keywords = ['技术', '算法', '编程', '开发', '代码', '软件', '系统', '平台']
        trend_keywords = ['趋势', '发展', '未来', '创新', '突破', '应用', '实践']
        
        for keyword in ai_keywords + tech_keywords + trend_keywords:
            if keyword in text:
                tags.append(keyword)
        
        # 去重并限制数量
        tags = list(set(tags))[:5]
        
        if not tags:
            tags = ['技术', 'AI', '文章']
        
        return tags
    
    def download_image(self, image_url, article_id):
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
    
    def update_articles_json(self, new_article):
        """更新articles.json文件"""
        try:
            json_file = 'posts/articles.json'
            
            # 读取现有文章
            if os.path.exists(json_file):
                with open(json_file, 'r', encoding='utf-8') as f:
                    articles = json.load(f)
            else:
                articles = []
            
            # 检查是否已存在相同ID的文章
            existing_ids = [article.get('id') for article in articles]
            if new_article['id'] in existing_ids:
                # 更新现有文章
                for i, article in enumerate(articles):
                    if article.get('id') == new_article['id']:
                        articles[i] = new_article
                        print(f"✅ 更新了现有文章: {new_article['title']}")
                        break
            else:
                # 添加新文章到开头
                articles.insert(0, new_article)
                print(f"✅ 添加了新文章: {new_article['title']}")
            
            # 保存文件
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
            
            print(f"📝 已更新 {json_file}")
            return True
            
        except Exception as e:
            print(f"❌ 更新JSON文件失败: {e}")
            return False

def main():
    """主函数"""
    print("🚀 微信公众号文章爬虫启动")
    print("=" * 50)
    
    # 获取用户输入
    url = input("请输入微信公众号文章链接: ").strip()
    
    if not url:
        print("❌ 请输入有效的URL")
        return
    
    if 'mp.weixin.qq.com' not in url:
        print("❌ 请输入有效的微信公众号文章链接")
        return
    
    # 创建爬虫实例
    crawler = WeChatArticleCrawler()
    
    # 抓取文章
    article_data = crawler.fetch_article_content(url)
    
    if article_data:
        print("\n📄 文章信息:")
        print(f"标题: {article_data['title']}")
        print(f"来源: {article_data['source']}")
        print(f"日期: {article_data['date']}")
        print(f"标签: {', '.join(article_data['tags'])}")
        print(f"摘要: {article_data['summary'][:100]}...")
        
        # 询问是否更新到网站
        confirm = input("\n是否将此文章添加到网站? (y/n): ").strip().lower()
        
        if confirm in ['y', 'yes', '是', '确定']:
            if crawler.update_articles_json(article_data):
                print("\n🎉 文章已成功添加到网站!")
                print("请刷新浏览器查看更新后的内容。")
            else:
                print("\n❌ 添加文章失败")
        else:
            print("\n❌ 已取消添加")
    else:
        print("\n❌ 抓取文章失败")

if __name__ == "__main__":
    main()
