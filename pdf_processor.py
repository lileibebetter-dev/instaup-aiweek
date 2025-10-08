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
    
    def extract_paper_title(self, text):
        """从PDF文本中提取论文标题"""
        try:
            # 构建提取标题的提示词
            title_prompt = f"""
请从以下PDF文档内容中提取论文的真实标题。

PDF内容（前2000字符）：
{text[:2000]}

请按照以下格式返回：
1. 英文标题：[提取的英文标题]
2. 中文标题：[提供准确的中文翻译]

要求：
- 提取文档开头部分的标题，通常是论文的正式标题
- 中文翻译要准确、专业
- 如果找不到明确的标题，请返回"论文解读"
"""
            
            # 调用API提取标题
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的学术文档分析师，擅长提取论文标题并提供准确的中文翻译。"},
                    {"role": "user", "content": title_prompt}
                ],
                temperature=0.3
            )
            
            title_content = response.choices[0].message.content.strip()
            
            # 解析返回的标题
            lines = title_content.split('\n')
            english_title = "论文解读"
            chinese_title = "论文解读"
            
            for line in lines:
                if line.startswith('1. 英文标题：'):
                    english_title = line.replace('1. 英文标题：', '').strip()
                elif line.startswith('2. 中文标题：'):
                    chinese_title = line.replace('2. 中文标题：', '').strip()
            
            return english_title, chinese_title
            
        except Exception as e:
            print(f"提取标题失败: {str(e)}")
            return "论文解读", "论文解读"

    def call_llm_api(self, text, title="论文解读", download_link=None):
        """调用火山方舟LLM API生成解读文章"""
        try:
            # 先提取论文标题
            english_title, chinese_title = self.extract_paper_title(text)
            
            # 构建完整的标题（中英双语）
            full_title = f"{chinese_title} | {english_title}"
            
            # 构建提示词
            prompt = f"""
请对以下PDF文档内容进行专业解读，生成一篇结构化的解读文章。

论文标题：{full_title}
英文标题：{english_title}
中文标题：{chinese_title}

文档内容：
{text[:8000]}  # 限制文本长度避免超出API限制

请按照以下格式生成解读文章，使用清晰的HTML结构和样式：

<div class="document-overview">
<h2>📄 文档概述</h2>
<p>简要概述文档的主要内容和核心观点</p>
</div>

<div class="deep-analysis">
<h2>🔍 深度分析</h2>
<h3>1. 问题背景</h3>
<p>分析文档要解决的核心问题</p>

<h3>2. 核心解决方案</h3>
<p>详细阐述主要解决方案</p>

<h3>3. 实验验证</h3>
<p>分析实验设计和验证结果</p>
</div>

<div class="key-points">
<h2>📋 核心要点</h2>
<ul>
<li>要点1：简洁明了的描述</li>
<li>要点2：简洁明了的描述</li>
<li>要点3：简洁明了的描述</li>
<li>要点4：简洁明了的描述</li>
<li>要点5：简洁明了的描述</li>
</ul>
</div>

<div class="summary-recommendations">
<h2>💡 总结与建议</h2>
<p>基于文档内容，提供实用的总结和建议</p>
</div>

<div class="key-insights">
<h2>🎯 关键洞察</h2>
<p>从文档中提炼出的独特见解和启发</p>
</div>

<div class="application-guidance">
<h2>🚀 应用落地指导</h2>
<h3>1. 主要应用场景</h3>
<p>分析该技术最适合的应用领域和具体场景</p>

<h3>2. 实施建议</h3>
<p>提供技术落地的具体建议和注意事项</p>

<h3>3. 商业价值</h3>
<p>分析技术带来的商业价值和竞争优势</p>

<h3>4. 技术门槛</h3>
<p>评估实施该技术所需的技术条件和资源要求</p>
</div>

要求：
1. 使用清晰的HTML结构，每个部分用div包装
2. 标题使用h2、h3标签
3. 段落使用p标签
4. 列表使用ul和li标签
5. 重要内容用<strong>标签加粗
6. 语言要专业、准确、易读
7. 每个段落不要太长，保持可读性
8. 应用落地指导部分要结合具体行业和场景，提供实用的建议
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
            download_href = download_link if download_link else "#"
            download_text = "下载PDF文档" if download_link else "PDF文档已上传"
            
            content = llm_content + f"""
            
            <div class="download-section" style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px;">
                <h3>📥 原始文档下载</h3>
                <p>如需查看完整内容，请下载原始PDF文档：</p>
                <a href="{download_href}" class="download-link" style="display: inline-block; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px;" {"target='_blank'" if download_link else ""}>{download_text}</a>
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
    
    def create_article_from_pdf(self, pdf_path, custom_title=None, custom_tags=None, download_link=None):
        """从PDF创建文章"""
        try:
            # 提取PDF文本
            text, error = self.extract_text_from_pdf(pdf_path)
            if error:
                return None, error
            
            # 调用LLM生成解读内容
            content, error = self.call_llm_api(text, custom_title, download_link)
            if error:
                return None, error
            
            # 生成文章ID
            pdf_name = os.path.basename(pdf_path)
            article_id = f"pdf-{hashlib.md5(pdf_name.encode()).hexdigest()[:12]}"
            
            # 提取真实的论文标题（中英双语）
            if not custom_title:  # 只有在没有自定义标题时才提取论文标题
                english_title, chinese_title = self.extract_paper_title(text)
                title = f"{chinese_title} | {english_title}"
            else:
                title = custom_title
            
            # 生成标签
            tags = custom_tags or ["AI技术篇章", "论文解读", "文档分析", "AI解读"]
            if isinstance(tags, str):
                tags = [tag.strip() for tag in tags.split(',') if tag.strip()]
            
            # 生成摘要
            summary = self.generate_summary(text)
            
            # 创建文章数据
            article_data = {
                'id': article_id,
                'title': title,
                'source': '论文解读',
                'summary': summary,
                'url': download_link or f"/uploads/pdf/{os.path.basename(pdf_path)}",  # 优先使用自定义下载链接
                'date': datetime.now().strftime('%Y-%m-%d'),
                'tags': tags,
                'content': content,
                'pdf_path': pdf_path,  # 保存PDF路径用于下载
                'original_filename': os.path.basename(pdf_path),
                'download_link': download_link  # 保存自定义下载链接
            }
            
            # 生成HTML文件
            html_path = f"articles/{article_id}.html"
            self.generate_html_file(article_data, html_path)
            
            return article_data, None
            
        except Exception as e:
            return None, f"创建文章失败: {str(e)}"
    
    def generate_html_file(self, article_data, html_path):
        """生成文章HTML文件"""
        try:
            # 构建HTML内容 - 使用外部CSS样式
            html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article_data['title']} | 云秒搭AI周报</title>
    <meta name="description" content="{article_data['title']} - 云秒搭AI周报">
    <link rel="stylesheet" href="../styles.css">
    <link rel="icon" type="image/png" href="../favicon.png">
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
</head>
<body>
    <div class="pixel-bg"></div>
    
    <div class="pdf-article-container">
        <header class="pdf-article-header">
            <h1 class="pdf-article-title">{article_data['title']}</h1>
            <div class="pdf-article-meta">
                <span>📰 {article_data['source']}</span>
                <span>📅 {article_data['date']}</span>
            </div>
            <div class="pdf-article-tags">
                {''.join([f'<span class="pixel-tag">{tag}</span>' for tag in article_data['tags']])}
            </div>
        </header>
        
        <main class="pdf-article-content">
            {article_data['content']}
        </main>
        
        <div class="pdf-article-actions">
            <a href="../index.html" class="pdf-action-btn">🏠 返回首页</a>
            <a href="{article_data['url']}" class="pdf-action-btn" target="_blank">📥 下载PDF文档</a>
        </div>
    </div>
</body>
</html>"""
            
            # 确保articles目录存在
            os.makedirs(os.path.dirname(html_path), exist_ok=True)
            
            # 写入HTML文件
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ 生成了HTML文件: {html_path}")
            
        except Exception as e:
            print(f"❌ 生成HTML文件失败: {str(e)}")
    
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
    
    def generate_weekly_report(self, articles_data, progress_callback=None):
        """生成周报"""
        try:
            if progress_callback:
                progress_callback(55, '正在准备周报数据...', '构建提示词')
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
            
            if progress_callback:
                progress_callback(60, '正在构建周报结构...', '准备AI提示词')
            
            # 构建推荐阅读的文章列表（用于AI生成链接）
            recommended_articles = []
            for article in articles_data[:5]:  # 取前5篇文章作为推荐
                recommended_articles.append({
                    'title': article.get('title', '未知标题'),
                    'id': article.get('id', ''),
                    'source': article.get('source', '未知来源'),
                    'date': article.get('date', '未知日期')
                })
            
            recommended_articles_text = "\n".join([
                f"- {art['title']} ({art['source']}, {art['date']})" 
                for art in recommended_articles
            ])
            
            prompt = f"""
请基于以下AI相关文章内容，生成一份专业的AI周报。

文章列表：
{articles_text}

推荐阅读文章列表：
{recommended_articles_text}

请按照以下格式生成周报，使用清晰的HTML结构和样式：

<div class="weekly-report-header">
<h1>🤖 AI周报 - {datetime.now().strftime('%Y年%m月第%U周')}</h1>
<p class="report-subtitle">AI周报趋势分析行业动态自动生成</p>
</div>

<div class="weekly-overview">
<h2>📊 本周概览</h2>
<p>简要概述本周AI领域的主要动态和趋势，突出核心特征和关键变化</p>
</div>

<div class="hot-topics">
<h2>🔥 热门话题</h2>
<p>总结本周最受关注的AI话题和讨论热点，包括：</p>
<ul>
<li><strong>话题1</strong>：详细描述和影响分析</li>
<li><strong>话题2</strong>：详细描述和影响分析</li>
<li><strong>话题3</strong>：详细描述和影响分析</li>
</ul>
</div>

<div class="key-breakthroughs">
<h2>💡 重要突破</h2>
<p>列举本周AI技术的重要突破和创新，包括：</p>
<ul>
<li><strong>突破1</strong>：技术细节和意义</li>
<li><strong>突破2</strong>：技术细节和意义</li>
<li><strong>突破3</strong>：技术细节和意义</li>
</ul>
</div>

<div class="industry-trends">
<h2>📈 行业动态</h2>
<p>分析AI行业的重要动态和发展趋势，包括：</p>
<ul>
<li><strong>动态1</strong>：公司/产品动态和影响</li>
<li><strong>动态2</strong>：公司/产品动态和影响</li>
<li><strong>动态3</strong>：公司/产品动态和影响</li>
</ul>
</div>

<div class="deep-analysis">
<h2>🎯 深度解读</h2>
<h3>1. 重要技术解读</h3>
<p>选择1-2个重要技术或产品进行深度分析，包括技术原理、应用场景、市场影响等</p>

<h3>2. 行业趋势解读</h3>
<p>分析行业发展趋势，包括竞争格局、商业模式、用户需求变化等</p>
</div>

<div class="trend-outlook">
<h2>🔮 趋势展望</h2>
<p>基于本周动态，预测未来AI发展趋势，包括：</p>
<ul>
<li><strong>趋势1</strong>：发展方向和预期影响</li>
<li><strong>趋势2</strong>：发展方向和预期影响</li>
<li><strong>趋势3</strong>：发展方向和预期影响</li>
</ul>
</div>

<div class="recommended-reading">
<h2>📚 推荐阅读</h2>
<p>推荐本周值得深入阅读的文章，包括：</p>
<ul>
<li><strong><a href="文章链接">文章标题</a></strong>：推荐理由</li>
<li><strong><a href="文章链接">文章标题</a></strong>：推荐理由</li>
<li><strong><a href="文章链接">文章标题</a></strong>：推荐理由</li>
</ul>
</div>

要求：
1. 使用清晰的HTML结构，每个部分用div包装
2. 标题使用h1、h2、h3标签
3. 段落使用p标签
4. 列表使用ul和li标签
5. 重要内容用<strong>标签加粗
6. 语言要专业、准确、有洞察力
7. 每个段落不要太长，保持可读性
8. 内容要基于提供的文章数据，不要编造信息
9. 保持客观中立的分析视角
10. 在推荐阅读部分，请从提供的推荐阅读文章列表中选择3-5篇最相关的文章
11. 推荐阅读的链接格式为：<a href="../articles/文章ID.html">文章标题</a>
12. 推荐理由要具体，说明为什么值得阅读
"""
            
            if progress_callback:
                progress_callback(70, '正在调用AI生成周报...', '发送请求到AI服务')
            
            # 调用火山方舟API
            try:
                if progress_callback:
                    progress_callback(75, '正在调用AI服务...', '等待AI响应')
                
                print(f"开始调用AI API生成周报...")
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
                
                print(f"AI API调用成功!")
                
                if progress_callback:
                    progress_callback(85, '正在处理AI响应...', '解析生成的内容')
                
                # 获取生成的内容
                report_content = response.choices[0].message.content
                print(f"AI生成内容长度: {len(report_content)} 字符")
                
                # 后处理：将推荐阅读中的文章标题替换为实际链接
                report_content = self.process_recommended_reading_links(report_content, recommended_articles)
                
            except Exception as api_error:
                print(f"AI API调用失败: {api_error}")
                if progress_callback:
                    progress_callback(75, 'AI服务暂时不可用，使用模板生成...', '生成基础周报')
                
                # 如果AI API失败，使用模板生成基础周报
                report_content = self.generate_template_report(articles_data)
            
            if progress_callback:
                progress_callback(90, '正在创建周报文章...', '构建文章数据结构')
            
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
            
            if progress_callback:
                progress_callback(95, '正在保存周报文件...', '生成HTML文件')
            
            # 生成HTML文件
            html_path = f"articles/{report_data['id']}.html"
            self.generate_weekly_report_html(report_data, html_path)
            
            return report_data, None
            
        except Exception as e:
            print(f"生成周报失败: {e}")
            return None, f"生成周报失败: {str(e)}"
    
    def process_recommended_reading_links(self, content, recommended_articles):
        """处理推荐阅读部分的链接"""
        try:
            import re
            
            # 创建文章标题到ID的映射
            title_to_id = {}
            for article in recommended_articles:
                title_to_id[article['title']] = article['id']
            
            # 查找推荐阅读部分
            recommended_section_pattern = r'<div class="recommended-reading">(.*?)</div>'
            match = re.search(recommended_section_pattern, content, re.DOTALL)
            
            if match:
                recommended_section = match.group(1)
                
                # 处理每个推荐链接
                for title, article_id in title_to_id.items():
                    # 查找包含该标题的链接
                    link_pattern = rf'<a href="[^"]*">({re.escape(title)})</a>'
                    replacement = f'<a href="../articles/{article_id}.html">{title}</a>'
                    recommended_section = re.sub(link_pattern, replacement, recommended_section)
                
                # 替换整个推荐阅读部分
                new_content = content.replace(match.group(0), f'<div class="recommended-reading">{recommended_section}</div>')
                return new_content
            
            return content
            
        except Exception as e:
            print(f"处理推荐阅读链接失败: {e}")
            return content
    
    def generate_template_report(self, articles_data):
        """生成模板周报（当AI API不可用时使用）"""
        try:
            # 获取最近的文章
            recent_articles = articles_data[:5]
            
            # 构建文章列表
            articles_list = ""
            for i, article in enumerate(recent_articles, 1):
                articles_list += f"""
<li><strong>{article.get('title', '未知标题')}</strong> - {article.get('source', '未知来源')} ({article.get('date', '未知日期')})</li>"""
            
            # 生成模板周报内容
            template_content = f"""
<div class="weekly-report-header">
<h1>🤖 AI周报 - {datetime.now().strftime('%Y年%m月第%U周')}</h1>
<p class="report-subtitle">AI周报趋势分析行业动态自动生成</p>
</div>

<div class="weekly-overview">
<h2>📊 本周概览</h2>
<p>本周AI领域持续快速发展，多个重要技术突破和应用落地。以下是基于本周收集的{len(articles_data)}篇文章的总结分析。</p>
</div>

<div class="hot-topics">
<h2>🔥 热门话题</h2>
<p>本周最受关注的AI话题包括：</p>
<ul>
<li><strong>大模型技术</strong>：继续在性能和效率方面取得突破</li>
<li><strong>AI应用落地</strong>：更多行业开始深度应用AI技术</li>
<li><strong>AI安全与伦理</strong>：相关讨论和规范制定持续推进</li>
</ul>
</div>

<div class="key-breakthroughs">
<h2>💡 重要突破</h2>
<p>本周AI技术的重要进展：</p>
<ul>
<li><strong>模型优化</strong>：在保持性能的同时显著降低计算成本</li>
<li><strong>多模态能力</strong>：文本、图像、音频处理能力进一步提升</li>
<li><strong>推理能力</strong>：复杂逻辑推理和问题解决能力增强</li>
</ul>
</div>

<div class="industry-trends">
<h2>📈 行业动态</h2>
<p>AI行业发展趋势：</p>
<ul>
<li><strong>企业应用</strong>：更多企业开始将AI集成到业务流程中</li>
<li><strong>开源生态</strong>：开源AI工具和模型持续丰富</li>
<li><strong>人才培养</strong>：AI相关教育和培训需求增长</li>
</ul>
</div>

<div class="recommended-reading">
<h2>📚 本周推荐文章</h2>
<p>基于本周收集的文章，推荐以下内容：</p>
<ul>{articles_list}
</ul>
</div>

<div class="weekly-summary">
<h2>🎯 本周总结</h2>
<p>本周AI领域继续保持快速发展态势，技术创新和应用落地并重。建议持续关注大模型技术进展、行业应用案例以及相关政策动态。</p>
</div>
"""
            return template_content
            
        except Exception as e:
            print(f"生成模板周报失败: {e}")
            return "<p>周报生成失败，请稍后重试。</p>"
    
    def generate_weekly_report_html(self, article_data, html_path):
        """生成周报HTML文件"""
        try:
            # 构建周报专用HTML内容
            html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article_data['title']} | 云秒搭AI周报</title>
    <meta name="description" content="{article_data['title']} - 云秒搭AI周报">
    <link rel="stylesheet" href="../styles.css">
    <link rel="icon" type="image/png" href="../favicon.png">
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
</head>
<body>
    <div class="pixel-bg"></div>
    
    <div class="container">
        <main class="article-content">
            {article_data['content']}
        </main>
        
        <div class="article-actions">
            <a href="../index.html" class="action-btn">🏠 返回首页</a>
            <a href="../admin.html" class="action-btn">⚙️ 管理后台</a>
        </div>
    </div>
</body>
</html>"""
            
            # 写入文件
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"周报HTML文件生成成功: {html_path}")
            return True
            
        except Exception as e:
            print(f"生成周报HTML文件失败: {e}")
            return False

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
