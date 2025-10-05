# EdgeOne Pages 部署说明

## 部署步骤

### 方法1：手动上传
1. 将 public/ 目录下的所有文件上传到EdgeOne Pages的根目录
2. 确保文件结构如下：
   ```
   /
   ├── index.html
   ├── article.html
   ├── styles.css
   ├── script.js
   ├── posts/
   │   └── articles.json
   ├── images/
   │   └── [各种图片目录]
   └── articles/
       └── [各文章HTML文件]
   ```

### 方法2：Git集成
1. 在EdgeOne Pages控制台启用Git集成
2. 连接到你的GitHub仓库
3. 设置构建命令：`python3 build_static_site.py`
4. 设置输出目录：`public`

## 注意事项
- 确保所有图片文件都已正确上传
- 检查文章链接是否正确
- 测试所有页面是否正常显示

## 更新流程
1. 本地修改文章或添加新文章
2. 运行 `python3 deploy_to_edgeone.py`
3. 将 public/ 目录内容上传到EdgeOne Pages
4. 或者推送代码到Git仓库（如果使用Git集成）
