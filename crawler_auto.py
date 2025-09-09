#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章爬虫 - 自动化版本
直接通过命令行参数传入URL，无需交互
"""

import sys
import json
import os
from crawler import WeChatArticleCrawler

def main():
    """主函数 - 自动化版本"""
    if len(sys.argv) != 2:
        print("使用方法: python3 crawler_auto.py <微信公众号文章链接>")
        print("示例: python3 crawler_auto.py https://mp.weixin.qq.com/s/aIltul1-Pb8Oz7hrfWC8dA")
        sys.exit(1)
    
    url = sys.argv[1].strip()
    
    if 'mp.weixin.qq.com' not in url:
        print("❌ 请输入有效的微信公众号文章链接")
        sys.exit(1)
    
    print(f"🚀 开始抓取文章: {url}")
    
    # 创建爬虫实例
    crawler = WeChatArticleCrawler()
    
    # 抓取文章
    article_data = crawler.fetch_article_content(url)
    
    if article_data:
        print(f"\n📄 成功抓取文章:")
        print(f"标题: {article_data['title']}")
        print(f"来源: {article_data['source']}")
        print(f"日期: {article_data['date']}")
        print(f"标签: {', '.join(article_data['tags'])}")
        print(f"摘要: {article_data['summary'][:100]}...")
        
        # 自动更新到网站
        if crawler.update_articles_json(article_data):
            print(f"\n🎉 文章已成功添加到网站!")
            print("请刷新浏览器查看更新后的内容。")
        else:
            print(f"\n❌ 添加文章失败")
            sys.exit(1)
    else:
        print(f"\n❌ 抓取文章失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
