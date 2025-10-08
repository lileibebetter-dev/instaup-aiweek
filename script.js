/**
 * 云秒搭AI周报 - 前端架构
 * 采用模块化设计，便于维护和扩展
 */

// 全局状态管理
const AppState = {
    currentFilter: 'all', // all, weekly, ai-tech, about
    articles: [],
    isLoading: false
};

// 配置常量
const CONFIG = {
    API_ENDPOINTS: {
        ARTICLES: 'posts/articles.json',
        POSTS: 'posts/posts.json'
    },
    FILTERS: {
        ALL: 'all',
        WEEKLY: 'weekly', 
        AI_TECH: 'ai-tech',
        ABOUT: 'about'
    },
    SELECTORS: {
        ARTICLES_GRID: '.articles-grid',
        NAV_BUTTONS: '.pixel-nav .pixel-btn',
        SEARCH_INPUT: '.pixel-input'
    }
};

/**
 * API模块 - 数据获取
 */
const ApiService = {
    async fetchArticles() {
  try {
    console.log('开始加载精选文章...');
            console.log('请求URL:', CONFIG.API_ENDPOINTS.ARTICLES);
            
            const response = await fetch(CONFIG.API_ENDPOINTS.ARTICLES, { 
                cache: 'no-store',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            });
            
    console.log('响应状态:', response.status, response.statusText);
            console.log('响应头:', response.headers);
            
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
            
    const data = await response.json();
            console.log('JSON解析成功，数据类型:', typeof data);
    console.log('加载到文章数量:', Array.isArray(data) ? data.length : 0);
            
            if (Array.isArray(data)) {
                return data;
            } else {
                console.warn('数据不是数组格式:', data);
                return [];
            }
  } catch (error) {
    console.error('fetchArticles 错误详情:', error);
            console.error('错误堆栈:', error.stack);
            throw error;
        }
    },

    async fetchPosts() {
        try {
            const response = await fetch(CONFIG.API_ENDPOINTS.POSTS, { 
                cache: 'no-store' 
            });
            if (!response.ok) throw new Error('加载周报失败');
            const data = await response.json();
            return Array.isArray(data) ? data : data.posts || [];
        } catch (error) {
            console.error('fetchPosts 错误详情:', error);
    throw error;
  }
}
};

/**
 * UI模块 - 界面渲染
 */
const UIService = {
    // 创建文章卡片
    createArticleCard(article) {
  const card = document.createElement('article');
        card.className = 'pixel-card';
        
  const date = new Date(article.date);
  const dateStr = `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
        
        // 根据来源选择图标
        const icon = this.getIconBySource(article.source);
        
        // 生成标签HTML
        const tagsHtml = (article.tags || []).map(tag => 
            `<span class="pixel-tag">${tag}</span>`
        ).join('');
        
        // 处理标题截断 - 允许两行显示，增加字符限制
        const truncatedTitle = this.truncateText(article.title, 80); // 限制80个字符，允许两行显示
        
        // 处理简介截断
        const truncatedSummary = this.truncateText(article.summary || '', 150); // 限制150个字符
  
  card.innerHTML = `
            <div class="card-header">
                <div class="pixel-icon">${icon}</div>
                <div class="card-meta">
                    <span class="source">${article.source}</span>
                    <span class="date">${dateStr}</span>
                </div>
            </div>
            <h2 class="pixel-title">
                <a href="articles/${article.id}.html" class="pixel-link">
                    ${truncatedTitle}
                </a>
            </h2>
            <div class="pixel-summary">
                ${truncatedSummary}
            </div>
            <div class="article-tags">
                ${tagsHtml}
    </div>
        `;
        
        // 设置title属性 - 在innerHTML之后设置，避免HTML解析问题
        const titleLink = card.querySelector('.pixel-link');
        const summaryDiv = card.querySelector('.pixel-summary');
        
        if (titleLink) {
            titleLink.title = article.title;
        }
        if (summaryDiv) {
            summaryDiv.title = article.summary || '';
        }
  
  return card;
    },

    // 文本截断工具函数
    truncateText(text, maxLength) {
        if (!text) return '';
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    },

    // HTML转义函数
    escapeHtml(text) {
        if (!text) return '';
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    },

    // 根据来源获取图标
    getIconBySource(source) {
        const iconMap = {
            '论文解读': '📄',
            'AI周报生成器': '📊'
        };
        
        if (iconMap[source]) return iconMap[source];
        if (source.includes('周报')) return '📊';
        return '📰';
    },

    // 渲染文章列表
    renderArticles(articles, filter = CONFIG.FILTERS.ALL) {
        const container = document.querySelector(CONFIG.SELECTORS.ARTICLES_GRID);
        if (!container) {
            console.error('找不到文章容器');
            return;
        }
        
        // 显示搜索框（非关于页面）
        this.toggleSearchBox(true);
        
        let filteredArticles = articles;
        
        // 根据筛选条件过滤文章
        if (filter === CONFIG.FILTERS.WEEKLY) {
            filteredArticles = articles.filter(article => 
                article.source === 'AI周报生成器' || 
                article.source.includes('周报') ||
                article.tags.some(tag => tag.includes('周报') || tag.includes('AI周报'))
            );
        } else if (filter === CONFIG.FILTERS.AI_TECH) {
            filteredArticles = articles.filter(article => 
                article.source === '论文解读' ||
                article.tags.some(tag => tag.includes('论文解读') || tag.includes('AI解读'))
            );
        }
        
        // 清空容器
  container.innerHTML = '';
  
        // 渲染文章卡片
        filteredArticles.forEach(article => {
            container.appendChild(this.createArticleCard(article));
        });
        
        // 更新导航按钮状态
        this.updateNavigationState(filter);
        
        console.log(`渲染了 ${filteredArticles.length} 篇文章，筛选条件: ${filter}`);
    },

    // 更新导航按钮状态
    updateNavigationState(activeFilter) {
        const buttons = document.querySelectorAll(CONFIG.SELECTORS.NAV_BUTTONS);
        buttons.forEach(btn => {
            btn.classList.remove('active');
        });
        
        const buttonTexts = ['首页', '周报', 'AI技术', '关于'];
        const buttonIndex = buttonTexts.findIndex(text => {
            if (text === '首页' && activeFilter === CONFIG.FILTERS.ALL) return true;
            if (text === '周报' && activeFilter === CONFIG.FILTERS.WEEKLY) return true;
            if (text === 'AI技术' && activeFilter === CONFIG.FILTERS.AI_TECH) return true;
            if (text === '关于' && activeFilter === CONFIG.FILTERS.ABOUT) return true;
            return false;
        });
        
        if (buttonIndex !== -1) {
            buttons[buttonIndex].classList.add('active');
        }
    },

    // 显示关于页面
    showAboutPage() {
        const container = document.querySelector(CONFIG.SELECTORS.ARTICLES_GRID);
        if (!container) return;
        
        // 隐藏搜索框
        this.toggleSearchBox(false);
        
        container.innerHTML = `
            <div class="about-content" style="grid-column: 1 / -1; text-align: center; padding: 40px;">
                <h2 style="color: var(--pixel-primary); font-family: 'Press Start 2P', monospace; margin-bottom: 30px;">关于云秒搭AI周报</h2>
                <div style="background: white; border: 2px solid var(--pixel-primary); border-radius: 12px; padding: 30px; margin: 20px auto; max-width: 800px;">
                    <p style="font-size: 16px; line-height: 1.8; color: #333; margin-bottom: 20px;">
                        云秒搭AI周报是一个专注于AI技术与应用的白蓝色像素风资讯平台。
                    </p>
                    <p style="font-size: 16px; line-height: 1.8; color: #333; margin-bottom: 20px;">
                        我们每周精选最新的AI技术动态、行业趋势分析、学术论文解读等内容，
                        为AI从业者和爱好者提供有价值的信息服务。
                    </p>
                    <div style="margin-top: 30px;">
                        <h3 style="color: var(--pixel-primary); font-family: 'Press Start 2P', monospace; font-size: 14px; margin-bottom: 15px;">内容特色</h3>
                        <ul style="text-align: left; max-width: 600px; margin: 0 auto;">
                            <li style="margin-bottom: 10px; color: #333;">📊 AI周报：每周AI行业动态汇总</li>
                            <li style="margin-bottom: 10px; color: #333;">📄 论文解读：深度解析前沿AI学术成果</li>
                            <li style="margin-bottom: 10px; color: #333;">📰 技术资讯：最新AI产品与技术动态</li>
                            <li style="margin-bottom: 10px; color: #333;">🎯 趋势分析：AI行业发展方向洞察</li>
                        </ul>
                    </div>
                </div>
            </div>
        `;
    },

    // 切换搜索框显示状态
    toggleSearchBox(show = true) {
        const searchSection = document.querySelector('.search-section');
        if (searchSection) {
            searchSection.style.display = show ? 'block' : 'none';
        }
    },

    // 显示加载状态
    showLoading() {
        const container = document.querySelector(CONFIG.SELECTORS.ARTICLES_GRID);
        if (container) {
            container.innerHTML = '<p style="text-align: center; color: var(--pixel-primary);">加载中...</p>';
        }
    },

    // 显示错误状态
    showError(message, details = '') {
        const container = document.querySelector(CONFIG.SELECTORS.ARTICLES_GRID);
        if (container) {
            container.innerHTML = `
                <div style="text-align: center; padding: 40px; color: #666;">
                    <h3 style="color: #e74c3c; margin-bottom: 20px;">⚠️ 加载遇到问题</h3>
                    <p style="margin-bottom: 10px;">${message}</p>
                    ${details ? `<p style="font-size: 0.9rem; color: #999;">${details}</p>` : ''}
                    <button onclick="location.reload()" style="
                        margin-top: 20px; 
                        padding: 10px 20px; 
                        background: #2196f3; 
                        color: white; 
                        border: none; 
                        border-radius: 5px; 
                        cursor: pointer;
                        font-family: var(--pixel-font);
                    ">🔄 刷新页面</button>
                </div>
            `;
        }
    }
};

/**
 * 事件处理模块
 */
const EventService = {
    // 初始化导航功能
    initNavigation() {
        const buttons = document.querySelectorAll(CONFIG.SELECTORS.NAV_BUTTONS);
        
        buttons.forEach(btn => {
            btn.addEventListener('click', () => {
                const text = btn.textContent.trim();
                
                if (text === '首页') {
                    AppState.currentFilter = CONFIG.FILTERS.ALL;
                    AppController.loadAndRenderArticles();
                } else if (text === '周报') {
                    AppState.currentFilter = CONFIG.FILTERS.WEEKLY;
                    AppController.loadAndRenderArticles();
                } else if (text === 'AI技术') {
                    AppState.currentFilter = CONFIG.FILTERS.AI_TECH;
                    AppController.loadAndRenderArticles();
                } else if (text === '关于') {
                    AppState.currentFilter = CONFIG.FILTERS.ABOUT;
                    UIService.showAboutPage();
                    UIService.updateNavigationState(CONFIG.FILTERS.ABOUT);
                }
            });
        });
    },

    // 初始化搜索功能
    initSearch() {
        const searchInput = document.querySelector(CONFIG.SELECTORS.SEARCH_INPUT);
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                const searchTerm = e.target.value.toLowerCase();
                const cards = document.querySelectorAll('.pixel-card');
                
                cards.forEach(card => {
                    const title = card.querySelector('.pixel-title')?.textContent.toLowerCase() || '';
                    const tags = card.querySelector('.article-tags')?.textContent.toLowerCase() || '';
                    
                    if (title.includes(searchTerm) || tags.includes(searchTerm)) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = searchTerm ? 'none' : 'block';
                    }
                });
            });
        }
    }
};

/**
 * 应用控制器 - 主要业务逻辑
 */
const AppController = {
    // 加载并渲染文章
    async loadAndRenderArticles() {
        try {
            AppState.isLoading = true;
            UIService.showLoading();
            
            const articles = await ApiService.fetchArticles();
            AppState.articles = articles;
            
            if (AppState.currentFilter === CONFIG.FILTERS.ABOUT) {
                UIService.showAboutPage();
            } else {
                UIService.renderArticles(articles, AppState.currentFilter);
            }
        } catch (error) {
            console.error('加载文章失败:', error);
            const errorMessage = error.message || '未知错误';
            UIService.showError('文章数据加载失败', `错误信息: ${errorMessage}`);
        } finally {
            AppState.isLoading = false;
        }
    },

    // 初始化应用
    async init() {
        try {
            console.log('🚀 初始化云秒搭AI周报应用...');
            
            // 初始化事件监听
            EventService.initNavigation();
            EventService.initSearch();
            
            // 加载文章数据
            await this.loadAndRenderArticles();
            
            console.log('✅ 应用初始化完成');
        } catch (error) {
            console.error('❌ 应用初始化失败:', error);
            UIService.showError('应用初始化失败，请刷新页面重试。');
        }
    }
};

/**
 * 应用启动
 */
document.addEventListener('DOMContentLoaded', () => {
    AppController.init();
});