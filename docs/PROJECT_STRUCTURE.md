# 云秒搭AI周报 - 项目结构说明

## 📁 目录结构

```
云秒搭AI周报/
├── 📄 核心文件
│   ├── index.html          # 网站主页
│   ├── article.html        # 文章详情页模板
│   ├── styles.css          # 网站样式
│   ├── script.js           # 前端JavaScript
│   ├── article.js          # 文章页面JavaScript
│   ├── server.py           # Flask后端服务器
│   ├── crawler.py          # 文章爬虫
│   ├── admin.html          # 管理后台界面
│   ├── launcher.html       # 启动页面
│   └── requirements.txt    # Python依赖
│
├── 📚 docs/                # 文档目录
│   ├── README.md           # 项目说明
│   ├── ADMIN_README.md     # 管理后台说明
│   ├── CRAWLER_README.md   # 爬虫使用说明
│   ├── FINAL_DEPLOY.md     # 最终部署说明
│   ├── 启动说明.md         # 启动说明
│   └── PROJECT_STRUCTURE.md # 本文档
│
├── 🔧 scripts/             # 脚本目录
│   ├── build_simple.py     # 网站构建脚本
│   ├── start_gui.py        # GUI启动脚本
│   └── 简单启动.py         # 简单启动脚本
│
├── ⚙️ config/              # 配置文件目录
│   └── _redirects          # 静态网站重定向规则
│
├── 📰 articles/            # 文章HTML文件
│   ├── wechat-*.html       # 各篇文章的静态HTML
│   └── ...
│
├── 🖼️ images/              # 图片资源
│   ├── [article_id]/       # 按文章ID分类的图片
│   └── ...
│
├── 📋 posts/               # 文章数据
│   ├── articles.json       # 文章数据JSON
│   └── posts.json          # 文章列表JSON
│
├── 🚀 启动脚本
│   ├── 启动管理后台.bat    # Windows批处理启动脚本
│   ├── 启动管理后台.sh     # Linux/Mac Shell启动脚本
│   └── build_exe.py        # 可执行文件构建脚本
│
└── 🎨 静态资源
    ├── favicon.ico         # 网站图标
    └── favicon.png         # 网站图标PNG
```

## 🗂️ 文件分类说明

### 核心文件
- **index.html** - 网站主页，白蓝色像素风设计
- **article.html** - 文章详情页模板
- **styles.css** - 网站样式文件，包含像素风CSS
- **script.js** - 前端JavaScript，处理文章列表和筛选
- **server.py** - Flask后端服务器，提供API接口
- **crawler.py** - 微信文章爬虫，负责抓取文章内容

### 管理后台
- **admin.html** - 管理后台界面
- **launcher.html** - 启动页面

### 文档 (docs/)
所有项目相关文档都整理在此目录下，便于维护和查阅。

### 脚本 (scripts/)
- **build_simple.py** - 网站构建脚本，生成静态HTML文件
- **start_gui.py** - GUI启动脚本
- **简单启动.py** - 简化的启动脚本

### 配置文件 (config/)
- **_redirects** - 静态网站重定向规则

### 数据文件
- **articles/** - 每篇文章的静态HTML文件
- **images/** - 按文章ID分类的图片资源
- **posts/** - 文章数据JSON文件

## 🚀 使用方法

### 启动管理后台
```bash
python3 server.py
```
然后访问 `http://localhost:8888/admin.html`

### 构建静态网站
```bash
python3 scripts/build_simple.py
```

### 部署到EdgeOne Pages
1. 运行构建脚本
2. 推送代码到GitHub
3. EdgeOne Pages自动部署

## 📝 维护说明

- 新增文章通过管理后台添加
- 修改样式直接编辑 `styles.css`
- 修改功能编辑对应的JavaScript文件
- 文档更新请修改 `docs/` 目录下的对应文件
