// Render article detail by id from query

async function fetchPosts() {
  const response = await fetch('posts/posts.json', { cache: 'no-store' });
  if (!response.ok) throw new Error('加载文章失败');
  const data = await response.json();
  return Array.isArray(data) ? data : data.posts || [];
}

function getQueryParam(name) {
  const params = new URLSearchParams(window.location.search);
  return params.get(name);
}

function initFooterYear() {
  const now = new Date().getFullYear();
  const span = document.getElementById('yearNow');
  if (span) span.textContent = now;
}

function renderArticle(post) {
  const el = document.getElementById('article');
  const date = new Date(post.date);
  const dateStr = `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
  const tagsHtml = (post.tags || []).map(t => `<span class="tag">${t}</span>`).join('');
  const linksHtml = (post.links || []).map(l => `<a href="${l.url}" target="_blank" rel="noopener">${l.title || '链接'}</a>`).join(' · ');
  el.innerHTML = `
    <h2 class="article-title">${post.title}</h2>
    <div class="meta">${dateStr} · 第${post.week}周</div>
    <div class="article-content">${post.content || ''}</div>
    <div class="article-links">${linksHtml}</div>
    <div class="tags" style="margin-top:12px;">${tagsHtml}</div>
  `;
}

async function init() {
  initFooterYear();
  const id = getQueryParam('id');
  const posts = await fetchPosts();
  const post = posts.find(p => p.id === id);
  if (!post) {
    const el = document.getElementById('article');
    el.innerHTML = '<p class="empty">未找到该文章，返回首页重试。</p>';
    return;
  }
  renderArticle(post);
}

init().catch(err => {
  console.error(err);
  const el = document.getElementById('article');
  el.innerHTML = '<p class="empty">加载失败，请刷新页面重试。</p>';
});
