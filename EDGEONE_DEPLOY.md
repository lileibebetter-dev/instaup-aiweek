# EdgeOne Pages 部署说明

## 当前状态
✅ 所有静态文件已准备就绪
✅ 文章HTML文件已生成
✅ 图片资源已完整

## EdgeOne Pages 配置

### 方法1：直接部署（推荐）
1. **登录EdgeOne Pages控制台**
2. **选择"手动上传"方式**
3. **将以下文件/目录上传到网站根目录：**
   ```
   / (根目录)
   ├── index.html          # 主页
   ├── article.html        # 文章详情页模板
   ├── styles.css          # 样式文件
   ├── script.js           # JavaScript文件
   ├── favicon.ico         # 网站图标
   ├── favicon.png         # 网站图标
   ├── articles/           # 文章HTML文件目录
   │   ├── wechat-6_WXtwXtrj_hCuEsRy52OA.html
   │   ├── wechat-UzMV7zWxBELAS-T7mIonUA.html
   │   └── ... (共6篇文章)
   ├── posts/              # 文章数据目录
   │   ├── articles.json
   │   └── posts.json
   └── images/             # 图片资源目录
       ├── 6_WXtwXtrj_hCuEsRy52OA/
       ├── wechat-aIltul1-Pb8Oz7hrfWC8dA/
       └── ... (所有图片目录)
   ```

### 方法2：Git集成部署
1. **在EdgeOne Pages控制台启用Git集成**
2. **连接到GitHub仓库：`lileibebetter-dev/instaup-aiweek`**
3. **配置设置：**
   - **分支：** `main`
   - **构建命令：** `python3 create_static_site.py`
   - **输出目录：** `/` (根目录)
   - **安装命令：** `pip install -r requirements.txt`

## 常见问题排查

### 1. 网站显示空白
- ✅ 检查 `index.html` 是否在根目录
- ✅ 检查 `styles.css` 和 `script.js` 是否存在
- ✅ 检查浏览器控制台是否有错误

### 2. 文章详情页显示空白
- ✅ 检查 `articles/` 目录是否存在
- ✅ 检查 `posts/articles.json` 是否存在
- ✅ 检查图片路径是否正确

### 3. 图片无法加载
- ✅ 检查 `images/` 目录是否完整上传
- ✅ 检查图片文件名是否匹配

## 测试步骤
1. **访问主页** - 应该看到文章列表
2. **点击文章** - 应该跳转到文章详情页
3. **检查图片** - 所有图片应该正常显示
4. **检查链接** - 返回首页和查看原文链接应该正常

## 更新流程
1. **本地修改文章或添加新文章**
2. **运行 `python3 create_static_site.py`**
3. **提交并推送代码到Git**
4. **EdgeOne Pages会自动重新部署**

## 联系支持
如果遇到问题，请提供：
1. EdgeOne Pages控制台的错误日志
2. 浏览器控制台的错误信息
3. 具体的错误描述
