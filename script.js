// Load and render weekly posts from JSON
// Chinese-first UI; English comments for maintainability

async function fetchPosts() {
  const response = await fetch('posts/posts.json', { cache: 'no-store' });
  if (!response.ok) throw new Error('加载周报失败');
  const data = await response.json();
  return Array.isArray(data) ? data : data.posts || [];
}

async function fetchArticles() {
  try {
    console.log('开始加载精选文章...');
    const response = await fetch('posts/articles.json', { cache: 'no-store' });
    console.log('响应状态:', response.status, response.statusText);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    const data = await response.json();
    console.log('加载到文章数量:', Array.isArray(data) ? data.length : 0);
    return Array.isArray(data) ? data : [];
  } catch (error) {
    console.error('fetchArticles 错误详情:', error);
    throw error;
  }
}

function renderYearOptions(posts) {
  const yearSelect = document.getElementById('yearSelect');
  const years = Array.from(new Set(posts.map(p => new Date(p.date).getFullYear()))).sort((a,b) => b - a);
  yearSelect.innerHTML = '<option value="all">全部</option>' + years.map(y => `<option value="${y}">${y}</option>`).join('');
}

function createPostCard(post) {
  const card = document.createElement('article');
  card.className = 'post-card';
  const date = new Date(post.date);
  const dateStr = `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
  const linksHtml = (post.links || []).map(l => `<a href="${l.url}" target="_blank" rel="noopener">${l.title || '链接'}</a>`).join('');
  const tagsHtml = (post.tags || []).map(t => `<span class="tag">${t}</span>`).join('');
  const href = `post.html?id=${encodeURIComponent(post.id || '')}`;
  card.innerHTML = `
    <h3><a class="post-link" href="${href}">${post.title}</a></h3>
    <div class="meta">${dateStr} · 第${post.week}周</div>
    <div class="summary">${post.summary || ''}</div>
    <div class="links">${linksHtml}</div>
    <div class="tags">${tagsHtml}</div>
  `;
  // Make whole card clickable except when clicking external links
  card.addEventListener('click', (e) => {
    const withinExternal = e.target.closest && e.target.closest('.links');
    const withinTitleLink = e.target.closest && e.target.closest('.post-link');
    if (withinExternal || withinTitleLink) return;
    if (post.id) window.location.href = href;
  });
  return card;
}

function createArticleCard(article) {
  const card = document.createElement('article');
  card.className = 'article-card';
  const date = new Date(article.date);
  const dateStr = `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
  const tagsHtml = (article.tags || []).map(t => `<span class="article-tag">${t}</span>`).join('');
  
  // Use internal article page if content exists, otherwise use external link
  const hasContent = article.content && article.content.trim().length > 0;
  const articleHref = hasContent ? `articles/${encodeURIComponent(article.id)}.html` : article.url;
  const linkTarget = hasContent ? '_self' : '_blank';
  const linkRel = hasContent ? '' : 'noopener';
  
  card.innerHTML = `
    <h3><a href="${articleHref}" target="${linkTarget}" ${linkRel ? `rel="${linkRel}"` : ''}>${article.title}</a></h3>
    <div class="article-meta">
      <span class="article-source">${article.source}</span>
      <span class="article-date">${dateStr}</span>
    </div>
    <div class="article-summary">${article.summary}</div>
    <div class="article-tags">${tagsHtml}</div>
    <a href="${articleHref}" target="${linkTarget}" ${linkRel ? `rel="${linkRel}"` : ''} class="article-link">${hasContent ? '阅读文章' : '阅读原文'}</a>
  `;
  
  return card;
}

function renderArticles(articles) {
  const container = document.getElementById('articles');
  container.innerHTML = '';
  
  articles
    .sort((a, b) => new Date(b.date) - new Date(a.date))
    .forEach(article => {
      container.appendChild(createArticleCard(article));
    });
}

function renderPosts(posts, { year = 'all', query = '' } = {}) {
  const wrap = document.getElementById('posts');
  const empty = document.getElementById('emptyState');
  const normalizedQuery = query.trim().toLowerCase();

  const filtered = posts.filter(p => {
    const inYear = year === 'all' || new Date(p.date).getFullYear().toString() === String(year);
    const inQuery = !normalizedQuery ||
      (p.title && p.title.toLowerCase().includes(normalizedQuery)) ||
      (p.summary && p.summary.toLowerCase().includes(normalizedQuery)) ||
      (Array.isArray(p.tags) && p.tags.join(' ').toLowerCase().includes(normalizedQuery));
    return inYear && inQuery;
  });

  wrap.innerHTML = '';
  filtered
    .sort((a,b) => new Date(b.date) - new Date(a.date))
    .forEach(post => wrap.appendChild(createPostCard(post)));

  empty.hidden = filtered.length > 0;
}

function initFooterYear() {
  const now = new Date().getFullYear();
  document.getElementById('yearNow').textContent = now;
}

async function init() {
  initFooterYear();
  
  try {
    // Load posts first
    const posts = await fetchPosts();
    renderYearOptions(posts);
    renderPosts(posts);

    const yearSelect = document.getElementById('yearSelect');
    const searchInput = document.getElementById('searchInput');

    function update() { renderPosts(posts, { year: yearSelect.value, query: searchInput.value }); }

    yearSelect.addEventListener('change', update);
    searchInput.addEventListener('input', update);
  } catch (err) {
    console.error('加载周报失败:', err);
    const empty = document.getElementById('emptyState');
    empty.hidden = false;
    empty.innerHTML = '<p>加载周报失败，请刷新页面重试。</p>';
  }

  // Load articles separately to avoid blocking posts
  try {
    const articles = await fetchArticles();
    renderArticles(articles);
  } catch (err) {
    console.error('加载精选文章失败:', err);
    const articlesContainer = document.getElementById('articles');
    if (articlesContainer) {
      articlesContainer.innerHTML = '<p style="text-align: center; color: var(--text-muted); padding: 20px;">精选文章加载失败</p>';
    }
  }
}

init().catch(err => {
  console.error(err);
  const empty = document.getElementById('emptyState');
  empty.hidden = false;
  empty.innerHTML = '<p>加载失败，请刷新页面重试。</p>';
});
