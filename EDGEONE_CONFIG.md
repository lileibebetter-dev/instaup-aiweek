# EdgeOne Pages 配置说明

## 🚀 部署配置

### 构建设置
- **构建命令**: `python3 build_edgeone.py`
- **输出目录**: `/` (根目录)
- **部署分支**: `main`

### 构建脚本功能
`build_edgeone.py` 脚本会：

1. **生成白蓝色像素风主页** (`index.html`)
2. **创建白蓝色像素风样式** (`styles.css`)
3. **修复文章图片路径** - 将所有图片路径从 `images/xxx.jpg` 改为 `../images/xxx.jpg`
4. **生成独立文章页面** - 每篇文章都有独立的HTML文件在 `articles/` 目录

### 文件结构
```
/
├── index.html          # 白蓝色像素风主页
├── styles.css          # 白蓝色像素风样式
├── articles/           # 独立文章页面
│   ├── article1.html
│   ├── article2.html
│   └── ...
├── posts/              # 文章数据
│   └── articles.json
├── images/             # 图片资源
│   ├── wechat-xxx/
│   └── ...
├── favicon.ico         # 网站图标
└── favicon.png         # 网站图标
```

## 🎨 设计特色

### 白蓝色像素风主题
- **主色调**: `#2196f3` (蓝色)
- **辅助色**: `#1976d2` (深蓝色)
- **强调色**: `#64b5f6` (浅蓝色)
- **背景色**: `#ffffff` (白色)
- **字体**: Press Start 2P (像素风字体)

### 功能特性
- ✅ 响应式设计
- ✅ 实时搜索功能
- ✅ 像素风动画效果
- ✅ 修复图片路径问题
- ✅ 独立文章页面
- ✅ SEO友好

## 🔧 故障排除

### 如果EdgeOne Pages没有更新：
1. 检查构建命令是否正确设置为 `python3 build_edgeone.py`
2. 检查输出目录是否设置为 `/`
3. 检查部署分支是否设置为 `main`
4. 手动触发重新部署
5. 清除CDN缓存

### 如果图片不显示：
1. 确保 `images/` 目录已正确部署
2. 检查图片路径是否为 `../images/xxx.jpg` 格式
3. 检查浏览器控制台是否有404错误

## 📝 更新流程

1. 修改文章内容或样式
2. 运行 `python3 build_edgeone.py` 测试
3. `git add .`
4. `git commit -m "更新说明"`
5. `git push origin main`
6. EdgeOne Pages自动重新部署

## 🎯 预期效果

部署成功后，你应该看到：
- 白蓝色像素风界面
- 所有文章图片正常显示
- 文章详情页面完整加载
- 响应式设计在不同设备上正常显示
