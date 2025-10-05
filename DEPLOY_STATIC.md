# EdgeOne Pages 部署说明

## 🚀 部署方式：纯静态文件

这个项目现在使用**纯静态文件**部署，不需要任何构建脚本。

### 📁 文件结构
```
/
├── index.html          # 白蓝色像素风主页
├── styles.css          # 白蓝色像素风样式
├── articles/           # 独立文章页面
│   ├── wechat-xxx.html
│   └── ...
├── posts/              # 文章数据
│   └── articles.json
├── images/             # 图片资源
│   ├── wechat-xxx/
│   └── ...
├── favicon.ico         # 网站图标
├── favicon.png         # 网站图标
└── edgeone.json        # EdgeOne Pages配置
```

### ⚙️ EdgeOne Pages 配置
- **构建命令**: 留空（不需要构建）
- **输出目录**: `/` (根目录)
- **部署分支**: `main`

### 🎨 设计特色
- **白蓝色像素风主题**
- **Press Start 2P 字体**
- **响应式设计**
- **修复的图片路径**

### 🔧 如果部署失败
1. 确保构建命令为空
2. 确保输出目录为 `/`
3. 手动触发重新部署
4. 清除CDN缓存

### 📝 更新流程
1. 修改文件
2. `git add .`
3. `git commit -m "更新说明"`
4. `git push origin main`
5. EdgeOne Pages自动部署
