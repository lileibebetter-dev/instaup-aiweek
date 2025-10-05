#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF文档处理模块
用于上传PDF文件并通过LLM生成解读文章
"""

import os
import json
import hashlib
import time
from datetime import datetime
from pathlib import Path
import PyPDF2
import requests
from werkzeug.utils import secure_filename
from openai import OpenAI

class PDFProcessor:
    def __init__(self):
        # 创建上传目录
        self.upload_dir = 'uploads'
        self.pdf_dir = os.path.join(self.upload_dir, 'pdf')
        self.articles_dir = os.path.join(self.upload_dir, 'articles')
        
        for dir_path in [self.upload_dir, self.pdf_dir, self.articles_dir]:
            os.makedirs(dir_path, exist_ok=True)
        
        # 初始化火山方舟客户端
        self.client = OpenAI(
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            api_key=os.environ.get("ARK_API_KEY", "86b2b17f-8b5a-4cde-ba7a-b9bd3ec93da3"),
        )
        self.model = "doubao-seed-1-6-thinking-250715"
    
    def allowed_file(self, filename):
        """检查文件类型是否允许"""
        ALLOWED_EXTENSIONS = {'pdf'}
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    def save_pdf(self, file):
        """保存PDF文件"""
        if not self.allowed_file(file.filename):
            return None, "不支持的文件类型，请上传PDF文件"
        
        # 生成安全的文件名
        filename = secure_filename(file.filename)
        timestamp = int(time.time())
        name, ext = os.path.splitext(filename)
        
        # 创建唯一文件名
        unique_filename = f"{name}_{timestamp}{ext}"
        file_path = os.path.join(self.pdf_dir, unique_filename)
        
        try:
            file.save(file_path)
            return file_path, None
        except Exception as e:
            return None, f"保存文件失败: {str(e)}"
    
    def extract_text_from_pdf(self, pdf_path):
        """从PDF中提取文本"""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
            
            return text.strip(), None
        except Exception as e:
            return None, f"提取PDF文本失败: {str(e)}"
    
    def call_llm_api(self, text, title="PDF文档解读"):
        """调用火山方舟LLM API生成解读文章"""
        try:
            # 构建提示词
            prompt = f"""
请对以下PDF文档内容进行专业解读，生成一篇结构化的解读文章。

文档标题：{title}

文档内容：
{text[:8000]}  # 限制文本长度避免超出API限制

请按照以下格式生成解读文章：

## 📄 文档概述
简要概述文档的主要内容和核心观点

## 🔍 深度分析  
对文档内容进行深入分析，包括：
- 主要观点和论述
- 支撑论据和案例
- 逻辑结构和论证方式

## 📋 核心要点
提取文档的3-5个核心要点，每个要点用一句话概括

## 💡 总结与建议
基于文档内容，提供实用的总结和建议

## 🎯 关键洞察
从文档中提炼出的独特见解和启发

请用HTML格式输出，使用合适的标签如<h2>、<p>、<ul>、<li>等。语言要专业、准确、易读。
"""
            
            # 调用火山方舟API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=4000,
                temperature=0.7
            )
            
            # 获取生成的内容
            llm_content = response.choices[0].message.content
            
            # 添加下载链接部分
            content = llm_content + """
            
            <div class="download-section" style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px;">
                <h3>📥 原始文档下载</h3>
                <p>如需查看完整内容，请下载原始PDF文档：</p>
                <a href="#" class="download-link" style="display: inline-block; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px;">下载PDF文档</a>
            </div>
            """
            
            return content, None
            
        except Exception as e:
            print(f"LLM API调用失败: {e}")
            # 如果API调用失败，使用备用方法
            return self.generate_fallback_content(text, title)
    
    def generate_fallback_content(self, text, title):
        """当LLM API失败时生成备用内容"""
        summary = self.generate_summary(text)
        analysis = self.generate_analysis(text)
        key_points = self.extract_key_points(text)
        
        content = f"""
        <h2>📄 文档概述</h2>
        <p>{summary}</p>
        
        <h2>🔍 深度分析</h2>
        <p>{analysis}</p>
        
        <h2>📋 核心要点</h2>
        <ul>
            {''.join([f'<li>{point}</li>' for point in key_points])}
        </ul>
        
        <h2>💡 总结与建议</h2>
        <p>本文档内容丰富，涵盖了多个重要方面。建议读者重点关注核心要点部分，并结合实际情况进行应用。</p>
        
        <div class="download-section" style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px;">
            <h3>📥 原始文档下载</h3>
            <p>如需查看完整内容，请下载原始PDF文档：</p>
            <a href="#" class="download-link" style="display: inline-block; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px;">下载PDF文档</a>
        </div>
        """
        
        return content, None
    
    def generate_summary(self, text):
        """生成文档摘要"""
        # 简单的摘要生成逻辑
        sentences = text.split('。')
        if len(sentences) > 3:
            summary = '。'.join(sentences[:3]) + '。'
        else:
            summary = text[:200] + "..." if len(text) > 200 else text
        
        return summary
    
    def generate_analysis(self, text):
        """生成分析内容"""
        # 简单的分析生成逻辑
        word_count = len(text)
        sentence_count = len(text.split('。'))
        
        analysis = f"""
        本文档共包含约{word_count}个字符，{sentence_count}个句子。
        文档内容结构清晰，信息密度较高，适合进行深入学习和研究。
        建议读者按照章节顺序阅读，重点关注核心概念和关键数据。
        """
        
        return analysis.strip()
    
    def extract_key_points(self, text):
        """提取关键要点"""
        # 简单的关键点提取逻辑
        sentences = text.split('。')
        key_points = []
        
        for sentence in sentences[:10]:  # 取前10个句子作为关键点
            if len(sentence.strip()) > 20:  # 过滤太短的句子
                key_points.append(sentence.strip())
        
        return key_points[:5]  # 返回前5个关键点
    
    def create_article_from_pdf(self, pdf_path, custom_title=None, custom_tags=None):
        """从PDF创建文章"""
        try:
            # 提取PDF文本
            text, error = self.extract_text_from_pdf(pdf_path)
            if error:
                return None, error
            
            # 调用LLM生成解读内容
            content, error = self.call_llm_api(text, custom_title)
            if error:
                return None, error
            
            # 生成文章ID
            pdf_name = os.path.basename(pdf_path)
            article_id = f"pdf-{hashlib.md5(pdf_name.encode()).hexdigest()[:12]}"
            
            # 生成标题
            title = custom_title or f"PDF文档解读 - {os.path.splitext(pdf_name)[0]}"
            
            # 生成标签
            tags = custom_tags or ["PDF解读", "文档分析", "AI解读"]
            if isinstance(tags, str):
                tags = [tag.strip() for tag in tags.split(',') if tag.strip()]
            
            # 生成摘要
            summary = self.generate_summary(text)
            
            # 创建文章数据
            article_data = {
                'id': article_id,
                'title': title,
                'source': 'PDF文档解读',
                'summary': summary,
                'url': f"/uploads/pdf/{os.path.basename(pdf_path)}",  # PDF下载链接
                'date': datetime.now().strftime('%Y-%m-%d'),
                'tags': tags,
                'content': content,
                'pdf_path': pdf_path,  # 保存PDF路径用于下载
                'original_filename': os.path.basename(pdf_path)
            }
            
            return article_data, None
            
        except Exception as e:
            return None, f"创建文章失败: {str(e)}"
    
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
    
    def generate_weekly_report(self, articles_data):
        """生成周报"""
        try:
            # 构建周报提示词
            articles_summary = []
            for article in articles_data[:10]:  # 取最近10篇文章
                articles_summary.append(f"""
标题：{article.get('title', '未知标题')}
来源：{article.get('source', '未知来源')}
日期：{article.get('date', '未知日期')}
摘要：{article.get('summary', '无摘要')[:200]}
""")
            
            articles_text = "\n".join(articles_summary)
            
            prompt = f"""
请基于以下AI相关文章内容，生成一份专业的AI周报。

文章列表：
{articles_text}

请按照以下格式生成周报：

# 🤖 AI周报 - {datetime.now().strftime('%Y年%m月第%U周')}

## 📊 本周概览
简要概述本周AI领域的主要动态和趋势

## 🔥 热门话题
总结本周最受关注的AI话题和讨论热点

## 💡 重要突破
列举本周AI技术的重要突破和创新

## 📈 行业动态
分析AI行业的重要动态和发展趋势

## 🎯 深度解读
选择1-2篇重要文章进行深度解读

## 🔮 趋势展望
基于本周动态，预测未来AI发展趋势

## 📚 推荐阅读
推荐本周值得深入阅读的文章

请用HTML格式输出，使用合适的标签。语言要专业、客观、有洞察力。
"""
            
            # 调用火山方舟API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=4000,
                temperature=0.7
            )
            
            # 获取生成的内容
            report_content = response.choices[0].message.content
            
            # 创建周报文章数据
            report_data = {
                'id': f"weekly-report-{int(time.time())}",
                'title': f"AI周报 - {datetime.now().strftime('%Y年%m月第%U周')}",
                'source': 'AI周报生成器',
                'summary': '基于本周AI相关文章自动生成的周报，涵盖热门话题、重要突破和趋势分析。',
                'url': '#',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'tags': ['AI周报', '趋势分析', '行业动态', '自动生成'],
                'content': report_content
            }
            
            return report_data, None
            
        except Exception as e:
            print(f"生成周报失败: {e}")
            return None, f"生成周报失败: {str(e)}"

def main():
    """主函数"""
    print("🚀 PDF文档处理模块")
    print("=" * 50)
    
    processor = PDFProcessor()
    
    # 测试PDF处理
    test_pdf = input("请输入PDF文件路径: ").strip()
    
    if not test_pdf or not os.path.exists(test_pdf):
        print("❌ 请输入有效的PDF文件路径")
        return
    
    # 处理PDF
    article_data, error = processor.create_article_from_pdf(test_pdf)
    
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
            if processor.update_articles_json(article_data):
                print("\n🎉 文章已成功添加到网站!")
                print("请刷新浏览器查看更新后的内容。")
            else:
                print("\n❌ 添加文章失败")
        else:
            print("\n❌ 已取消添加")
    else:
        print(f"\n❌ 处理PDF失败: {error}")

if __name__ == "__main__":
    main()
