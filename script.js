// Load and render weekly posts from JSON
// Chinese-first UI; English comments for maintainability

async function fetchPosts() {
  const response = await fetch('posts/posts.json', { cache: 'no-store' });
  if (!response.ok) throw new Error('加载周报失败');
  const data = await response.json();
  return Array.isArray(data) ? data : data.posts || [];
}

async function fetchArticles() {
  const response = await fetch('posts/articles.json', { cache: 'no-store' });
  if (!response.ok) throw new Error('加载精选文章失败');
  const data = await response.json();
  return Array.isArray(data) ? data : [];
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
  
  card.innerHTML = `
    <h3><a href="${article.url}" target="_blank" rel="noopener">${article.title}</a></h3>
    <div class="article-meta">
      <span class="article-source">${article.source}</span>
      <span class="article-date">${dateStr}</span>
    </div>
    <div class="article-summary">${article.summary}</div>
    <div class="article-tags">${tagsHtml}</div>
    <a href="${article.url}" target="_blank" rel="noopener" class="article-link">阅读原文</a>
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
  
  // Load and render both posts and articles
  const [posts, articles] = await Promise.all([
    fetchPosts(),
    fetchArticles()
  ]);
  
  renderYearOptions(posts);
  renderPosts(posts);
  renderArticles(articles);

  const yearSelect = document.getElementById('yearSelect');
  const searchInput = document.getElementById('searchInput');

  function update() { renderPosts(posts, { year: yearSelect.value, query: searchInput.value }); }

  yearSelect.addEventListener('change', update);
  searchInput.addEventListener('input', update);
}

init().catch(err => {
  console.error(err);
  const empty = document.getElementById('emptyState');
  empty.hidden = false;
  empty.innerHTML = '<p>加载失败，请刷新页面重试。</p>';
});
