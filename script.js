// Load and render weekly posts from JSON
// Chinese-first UI; English comments for maintainability

async function fetchPosts() {
  const response = await fetch('posts/posts.json', { cache: 'no-store' });
  if (!response.ok) throw new Error('加载周报失败');
  const data = await response.json();
  return Array.isArray(data) ? data : data.posts || [];
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
  card.innerHTML = `
    <h3>${post.title}</h3>
    <div class="meta">${dateStr} · 第${post.week}周</div>
    <div class="summary">${post.summary || ''}</div>
    <div class="links">${linksHtml}</div>
    <div class="tags">${tagsHtml}</div>
  `;
  return card;
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
  const posts = await fetchPosts();
  renderYearOptions(posts);
  renderPosts(posts);

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
