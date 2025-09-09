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
    const article = articles.find(a => a.id === articleId);
    console.log('找到的文章:', article ? article.title : '未找到');
    
    if (article) {
      console.log('开始渲染文章...');
      renderArticle(article);
      console.log('文章渲染完成');
    } else {
      console.log('未找到指定文章');
      const articleBody = document.getElementById('articleBody');
      if (articleBody) {
        articleBody.innerHTML = '<p>未找到指定文章</p>';
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
