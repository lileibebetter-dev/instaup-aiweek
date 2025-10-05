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
  // Update page title
  document.title = `${article.title} | 云秒搭AI周报`;
  
  // Update breadcrumb title
  const breadcrumbTitle = document.getElementById('breadcrumbTitle');
  if (breadcrumbTitle) {
    breadcrumbTitle.textContent = article.title;
  }
  
  // Update article title
  const articleTitle = document.getElementById('articleTitle');
  if (articleTitle) {
    articleTitle.textContent = article.title;
  }
  
  // Update article source
  const articleSource = document.getElementById('articleSource');
  if (articleSource) {
    articleSource.textContent = article.source;
  }
  
  // Update article date
  const articleDate = document.getElementById('articleDate');
  if (articleDate) {
    const date = new Date(article.date);
    const dateStr = `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`;
    articleDate.textContent = dateStr;
  }
  
  // Update article tags
  const articleTags = document.getElementById('articleTags');
  if (articleTags) {
    const tagsHtml = (article.tags || []).map(t => `<span class="article-tag">${t}</span>`).join('');
    articleTags.innerHTML = tagsHtml;
  }

  // Update article body
  const articleBody = document.getElementById('articleBody');
  if (articleBody) {
    articleBody.innerHTML = article.content || '<p>文章内容加载中...</p>';
  }
  
  // Update original link
  const originalLink = document.getElementById('originalLink');
  if (originalLink) {
    originalLink.href = article.url;
  }
}

async function init() {
  console.log('开始初始化文章页面...');
  initFooterYear();
  
  // Get article ID from URL parameters
  const urlParams = new URLSearchParams(window.location.search);
  const articleId = urlParams.get('id');
  console.log('文章ID:', articleId);
  console.log('当前URL:', window.location.href);
  
  if (!articleId) {
    console.log('未找到文章ID');
    const articleBody = document.getElementById('articleBody');
    if (articleBody) {
      articleBody.innerHTML = '<p>未找到文章ID</p>';
    }
    return;
  }
  
  try {
    console.log('开始获取文章数据...');
    const articles = await fetchArticles();
    console.log('获取到文章数量:', articles.length);
    console.log('所有文章ID:', articles.map(a => a.id));
    
    const article = articles.find(a => a.id === articleId);
    console.log('找到的文章:', article ? article.title : '未找到');
    
    if (article) {
      console.log('开始渲染文章...');
      console.log('文章内容长度:', article.content ? article.content.length : '无内容');
      renderArticle(article);
      console.log('文章渲染完成');
    } else {
      console.log('未找到指定文章');
      console.log('尝试查找包含该ID的文章...');
      const partialMatch = articles.find(a => a.id.includes(articleId) || articleId.includes(a.id));
      console.log('部分匹配的文章:', partialMatch ? partialMatch.title : '无');
      
      const articleBody = document.getElementById('articleBody');
      if (articleBody) {
        articleBody.innerHTML = `
          <p>未找到指定文章</p>
          <p>查找的ID: ${articleId}</p>
          <p>可用文章:</p>
          <ul>
            ${articles.map(a => `<li>${a.id}: ${a.title}</li>`).join('')}
          </ul>
        `;
      }
    }
  } catch (error) {
    console.error('加载文章失败:', error);
    const articleBody = document.getElementById('articleBody');
    if (articleBody) {
      articleBody.innerHTML = '<p>加载文章失败，请刷新页面重试。</p>';
    }
  }
}

init();
