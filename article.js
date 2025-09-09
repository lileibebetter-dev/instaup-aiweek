// Article detail page functionality
// Load and display article content from JSON

async function fetchArticles() {
  const response = await fetch('posts/articles.json', { cache: 'no-store' });
  if (!response.ok) throw new Error('加载文章失败');
  const data = await response.json();
  return Array.isArray(data) ? data : [];
}

function initFooterYear() {
  const now = new Date().getFullYear();
  document.getElementById('yearNow').textContent = now;
}

function renderArticle(article) {
  const articleContent = document.getElementById('articleContent');
  const articleTitle = document.getElementById('articleTitle');
  const originalLink = document.getElementById('originalLink');
  
  // Update page title
  document.title = `${article.title} | 云秒搭AI周报`;
  
  // Update breadcrumb
  articleTitle.textContent = article.title;
  
  // Update original link
  originalLink.href = article.url;
  
  // Format date
  const date = new Date(article.date);
  const dateStr = `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`;
  
  // Create article HTML
  const tagsHtml = (article.tags || []).map(t => `<span class="article-tag">${t}</span>`).join('');
  
  articleContent.innerHTML = `
    <header class="article-header">
      <h1 class="article-title">${article.title}</h1>
      <div class="article-meta">
        <span class="article-source">${article.source}</span>
        <span class="article-date">${dateStr}</span>
      </div>
      <div class="article-tags">${tagsHtml}</div>
    </header>
    <div class="article-body">
      ${article.content || '<p>文章内容加载中...</p>'}
    </div>
  `;
}

async function init() {
  initFooterYear();
  
  // Get article ID from URL parameters
  const urlParams = new URLSearchParams(window.location.search);
  const articleId = urlParams.get('id');
  
  if (!articleId) {
    document.getElementById('articleContent').innerHTML = '<p>未找到文章ID</p>';
    return;
  }
  
  try {
    const articles = await fetchArticles();
    const article = articles.find(a => a.id === articleId);
    
    if (article) {
      renderArticle(article);
    } else {
      document.getElementById('articleContent').innerHTML = '<p>未找到指定文章</p>';
    }
  } catch (error) {
    console.error('加载文章失败:', error);
    document.getElementById('articleContent').innerHTML = '<p>加载文章失败，请刷新页面重试。</p>';
  }
}

init();
