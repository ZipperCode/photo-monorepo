# 照片收录管理系统 - 实施任务清单

## 使用说明

本文档提供了所有 9 个阶段的任务清单，每个任务都标注了文件路径、依赖关系和验收标准。

### 任务标记说明
- ⏳ **待完成**: 任务尚未开始
- 🔄 **进行中**: 任务正在执行
- ✅ **已完成**: 任务已完成并验证
- 🚫 **已阻塞**: 任务被依赖阻塞

---

## 阶段 1: 基础设施搭建

### 1.1 初始化项目结构
- ⏳ 创建 Monorepo 根目录结构
  ```bash
  mkdir -p apps/web apps/api infrastructure/docker/{api,web,nginx} infrastructure/scripts storage/{uploads,thumbnails}
  ```
  - **验收**: 目录结构符合设计文档

### 1.2 初始化 Vue 3 前端项目
- ⏳ 使用 Vite 创建 Vue 3 项目
  ```bash
  cd apps/web
  npm create vite@latest . -- --template vue-ts
  ```
- ⏳ 安装依赖
  ```bash
  npm install vue-router@4 pinia tailwindcss postcss autoprefixer @heroicons/vue axios
  npx tailwindcss init -p
  ```
- ⏳ 配置 Tailwind CSS
  - 文件: `apps/web/tailwind.config.js`
  - 文件: `apps/web/src/index.css`
- ⏳ 配置 Vue Router
  - 文件: `apps/web/src/router/index.ts`
- ⏳ 配置 Pinia
  - 文件: `apps/web/src/main.ts`
- ⏳ 配置 Vite
  - 文件: `apps/web/vite.config.ts`
- **验收**: `npm run dev` 启动成功，页面可访问

### 1.3 初始化 FastAPI 后端项目
- ⏳ 创建 Python 虚拟环境
  ```bash
  cd apps/api
  python -m venv venv
  source venv/bin/activate  # Windows: venv\Scripts\activate
  ```
- ⏳ 创建 requirements.txt
  ```
  fastapi==0.104.1
  uvicorn[standard]==0.24.0
  motor==3.3.2
  pydantic==2.5.0
  pydantic-settings==2.1.0
  python-multipart==0.0.6
  python-jose[cryptography]==3.3.0
  passlib[bcrypt]==1.7.4
  pillow==10.1.0
  python-dotenv==1.0.0
  ```
- ⏳ 创建项目结构
  ```bash
  mkdir -p app/api/v1 app/core app/models app/schemas app/services
  touch app/__init__.py app/main.py
  ```
- ⏳ 创建 `app/main.py` (应用入口)
  - 功能: FastAPI 应用实例，CORS 配置，健康检查端点
  - **验收**: `uvicorn app.main:app --reload` 启动成功

### 1.4 配置管理和数据库连接
- ⏳ 创建 `app/core/config.py` (配置管理)
  - 使用 Pydantic Settings
  - 从 .env 加载环境变量
- ⏳ 创建 `app/core/database.py` (数据库连接)
  - Motor 异步连接
  - 连接池管理
  - 连接/断开生命周期
- ⏳ 创建 `.env.example` 模板
- **验收**: 应用启动时成功连接 MongoDB

### 1.5 Docker 配置
- ⏳ 创建 `infrastructure/docker/api/Dockerfile`
  - 多阶段构建
  - 安装 Python 依赖
- ⏳ 创建 `infrastructure/docker/web/Dockerfile`
  - Node.js 基础镜像
  - 构建 Vue 应用
- ⏳ 创建 `infrastructure/docker/nginx/nginx.conf`
  - 反向代理配置
  - 路由规则: / -> web, /api -> api
- ⏳ 创建 `docker-compose.yml`
  - 定义 4 个服务: mongodb, api, web, nginx
  - 配置网络和卷
- ⏳ 创建 `.gitignore`
  - 忽略: .env, storage/, node_modules/, venv/, __pycache__/
- **验收**: `docker-compose up -d` 所有服务启动成功

### 1.6 验证和测试
- ⏳ 测试 MongoDB 连接
  ```bash
  docker exec -it photo-mongo mongosh -u admin -p password123
  ```
- ⏳ 测试 API 健康检查
  ```bash
  curl http://localhost:8000/health
  ```
- ⏳ 测试前端页面访问
  - 浏览器访问: http://localhost:5173
- ⏳ 测试 Nginx 反向代理
  - 浏览器访问: http://localhost:80
- **验收**: 所有测试通过

### 1.7 文档编写
- ⏳ 创建 `README.md`
  - 项目简介
  - 快速开始指南
  - 环境要求
  - 启动步骤
- **验收**: 开发者可根据 README 在 5 分钟内启动项目

---

## 阶段 2: 认证系统

### 2.1 后端认证实现
- ⏳ 创建 `app/models/user.py` (User 模型)
  - 字段: username, email, hashed_password, role, is_active
- ⏳ 创建 `app/schemas/user.py` (Pydantic schemas)
  - UserCreate, UserLogin, UserResponse
- ⏳ 创建 `app/core/security.py` (安全工具)
  - `hash_password()` - bcrypt 哈希
  - `verify_password()` - 密码验证
  - `create_access_token()` - JWT 生成
  - `decode_access_token()` - JWT 验证
- ⏳ 创建 `app/api/v1/auth.py` (认证端点)
  - `POST /auth/login` - 登录端点
- ⏳ 创建 `app/api/deps.py` (依赖注入)
  - `get_current_user()` - 从 token 获取当前用户
  - `require_admin()` - 管理员权限检查
- ⏳ 创建初始管理员用户脚本
  - 文件: `infrastructure/scripts/create-admin.py`
- **验收**: 可以使用 curl 测试登录获取 token

### 2.2 前端认证实现
- ⏳ 创建 `apps/web/src/stores/auth.ts` (Auth Store)
  - State: token, user, isAuthenticated
  - Actions: login(), logout(), checkAuth()
- ⏳ 创建 `apps/web/src/services/api.ts` (HTTP 客户端)
  - Axios 实例
  - 自动附加 Authorization header
  - 错误处理拦截器
- ⏳ 创建 `apps/web/src/pages/AdminLogin.vue` (登录页面)
  - 表单: 用户名 + 密码
  - 提交后调用 login API
  - 成功后跳转到管理后台
- ⏳ 配置路由守卫
  - 文件: `apps/web/src/router/index.ts`
  - 检查认证状态
  - 未认证重定向到登录页
- **验收**: 可以登录并跳转到管理后台

---

## 阶段 3: 收录码管理

### 3.1 后端收录码实现
- ⏳ 创建 `app/models/collection.py` (Collection 模型)
- ⏳ 创建 `app/schemas/collection.py` (Pydantic schemas)
- ⏳ 创建 `app/utils/code_generator.py` (收录码生成器)
  - 生成 6 位字母数字
  - 唯一性检查
- ⏳ 创建 `app/services/collection_service.py` (业务逻辑)
  - 创建收录码
  - 验证收录码
  - 更新统计信息
- ⏳ 创建 `app/api/v1/collections.py` (用户端点)
  - `POST /collections/validate` - 验证收录码
- ⏳ 扩展 `app/api/v1/admin.py` (管理端点)
  - `POST /admin/collections` - 创建收录码
  - `GET /admin/collections` - 列出收录码
  - `GET /admin/collections/{code}` - 获取详情
  - `PATCH /admin/collections/{code}` - 更新收录码
  - `DELETE /admin/collections/{code}` - 删除收录码
- **验收**: API 测试通过

### 3.2 前端收录码实现
- ⏳ 创建 `apps/web/src/stores/collection.ts` (Collection Store)
- ⏳ 创建 `apps/web/src/services/collectionService.ts` (API 调用)
- ⏳ 创建 `apps/web/src/pages/AccessCodePage.vue` (收录码输入页)
  - 输入框 + 验证按钮
  - 验证成功跳转到上传页
- ⏳ 创建 `apps/web/src/components/admin/CollectionForm.vue` (表单组件)
  - 创建/编辑收录码
  - 配置设置项
- ⏳ 扩展 `apps/web/src/pages/AdminDashboard.vue` (管理首页)
  - 显示收录码列表
  - 创建收录码按钮
- **验收**: 可以创建收录码并验证

---

## 阶段 4: 照片上传系统

### 4.1 后端照片上传实现
- ⏳ 创建 `app/models/photo.py` (Photo 模型)
- ⏳ 创建 `app/schemas/photo.py` (Pydantic schemas)
- ⏳ 创建 `app/services/storage_service.py` (存储服务)
  - `save_file()` - 保存文件
  - `get_file()` - 获取文件
  - `delete_file()` - 删除文件
  - 支持本地存储和 S3 切换
- ⏳ 创建 `app/services/image_service.py` (图片处理)
  - `generate_thumbnail()` - 生成缩略图 (Pillow)
  - `extract_exif()` - 提取 EXIF 数据
  - `validate_image()` - 验证图片文件
- ⏳ 创建 `app/services/photo_service.py` (照片服务)
  - 处理上传流程
  - 异步处理图片
- ⏳ 扩展 `app/api/v1/photos.py` (照片端点)
  - `POST /collections/{code}/photos` - 上传照片
  - `GET /photos/{photo_id}/original` - 获取原图
  - `GET /photos/{photo_id}/thumbnail` - 获取缩略图
- **验收**: 可以上传照片并生成缩略图

### 4.2 前端照片上传实现
- ⏳ 创建 `apps/web/src/composables/useUpload.ts` (上传逻辑)
  - 文件选择
  - 批量上传
  - 进度跟踪
- ⏳ 创建 `apps/web/src/components/upload/FileDropZone.vue` (拖拽区域)
  - 拖拽上传
  - 点击选择文件
  - 文件预览
- ⏳ 创建 `apps/web/src/components/upload/UploadProgress.vue` (进度组件)
  - 每个文件独立进度条
  - 上传状态显示
- ⏳ 创建 `apps/web/src/pages/UploadPage.vue` (上传页面)
  - 整合拖拽和进度组件
  - 成功提示
- **验收**: 可以拖拽上传多张照片，显示进度

---

## 阶段 5: 管理后台界面设计 ⭐

### 5.1 UI/UX 设计准备
- ⏳ 使用 ui-ux-pro-max 搜索设计指导
  ```bash
  python3 .claude/skills/ui-ux-pro-max/scripts/search.py "dashboard admin panel" --domain product
  python3 .claude/skills/ui-ux-pro-max/scripts/search.py "minimal clean professional modern" --domain style
  python3 .claude/skills/ui-ux-pro-max/scripts/search.py "dashboard admin" --domain color
  python3 .claude/skills/ui-ux-pro-max/scripts/search.py "professional modern clean" --domain typography
  python3 .claude/skills/ui-ux-pro-max/scripts/search.py "layout responsive component" --stack vue
  ```
- ⏳ 配置 Tailwind 主题
  - 文件: `apps/web/tailwind.config.js`
  - 定义颜色、字体、间距
- ⏳ 安装图标库
  ```bash
  npm install @heroicons/vue
  ```

### 5.2 后端批量操作 API
- ⏳ 扩展 `app/api/v1/admin.py` (管理端点)
  - `GET /admin/collections/{code}/photos` - 列出照片
  - `GET /admin/photos/{photo_id}/download` - 单张下载
  - `POST /admin/collections/{code}/photos/download` - 批量下载
  - `POST /admin/collections/{code}/photos/download-all` - 一键下载全部
  - `DELETE /admin/photos/{photo_id}` - 删除单张
  - `DELETE /admin/collections/{code}/photos` - 一键删除全部
- ⏳ 实现 ZIP 打包下载
  - 使用 Python zipfile
  - 流式传输
- **验收**: API 测试通过

### 5.3 前端通用组件
- ⏳ 创建 `apps/web/src/components/common/Button.vue`
  - 支持不同变体: primary, secondary, danger
  - 支持加载状态
  - 支持图标
- ⏳ 创建 `apps/web/src/components/common/Modal.vue`
  - 遮罩层
  - 关闭按钮
  - 动画效果
- ⏳ 创建 `apps/web/src/components/common/Card.vue`
  - 白色背景
  - 圆角阴影
  - Hover 效果
- ⏳ 创建 `apps/web/src/components/common/Toast.vue`
  - 成功/错误/警告提示
  - 自动消失

### 5.4 管理后台组件
- ⏳ 创建 `apps/web/src/components/admin/StatCard.vue` (统计卡片)
  - 图标 + 数值 + 标签 + 趋势
- ⏳ 创建 `apps/web/src/components/admin/CollectionCard.vue` (收录码卡片)
  - 显示码、名称、照片数
  - 快速操作按钮
- ⏳ 创建 `apps/web/src/components/admin/PhotoGrid.vue` (照片网格)
  - 响应式网格
  - 多选功能
- ⏳ 创建 `apps/web/src/components/admin/PhotoCard.vue` (照片卡片)
  - 缩略图 + 复选框
  - Hover 遮罩
  - 快速下载按钮
- ⏳ 创建 `apps/web/src/components/admin/PhotoToolbar.vue` (工具栏)
  - 全选/取消全选
  - 批量下载
  - 一键下载全部
  - 删除按钮
- ⏳ 创建 `apps/web/src/components/admin/Lightbox.vue` (灯箱)
  - 全屏显示
  - 左右导航
  - 下载/删除按钮
  - 键盘支持

### 5.5 管理后台页面
- ⏳ 扩展 `apps/web/src/pages/AdminDashboard.vue` (首页)
  - 统计卡片
  - 收录码列表
  - 搜索筛选
- ⏳ 创建 `apps/web/src/pages/AdminCollectionDetail.vue` (详情页)
  - 收录码信息
  - 照片网格
  - 工具栏
  - 灯箱

### 5.6 样式优化
- ⏳ 添加动画效果
  - 页面切换: fade-in
  - 模态框: scale + fade
  - 列表项删除: slide-out
- ⏳ 添加响应式设计
  - 移动端: 单列布局
  - 平板: 2-3 列网格
  - 桌面: 4-6 列网格
- ⏳ 添加加载状态
  - 骨架屏
  - 进度条
- ⏳ 添加空状态
  - 无数据提示
  - 引导操作按钮
- **验收**: 界面美观，操作流畅，响应式正常

---

## 阶段 6: 统计与数据展示

### 6.1 后端统计实现
- ⏳ 创建 `app/api/v1/admin.py` 统计端点
  - `GET /admin/statistics` - 获取统计数据
- ⏳ 实现数据聚合
  - 使用 MongoDB 聚合管道
  - 计算总数、总大小、最近上传
- **验收**: 统计数据准确

### 6.2 前端统计展示
- ⏳ 更新 `AdminDashboard.vue`
  - 显示统计卡片
  - 图表展示（可选）
- **验收**: 数据实时刷新

---

## 阶段 7: 搜索筛选与优化

### 7.1 搜索筛选实现
- ⏳ 扩展照片列表 API
  - 支持 search 参数（文件名）
  - 支持 date_from/date_to 参数
- ⏳ 创建 `apps/web/src/components/admin/FilterBar.vue`
  - 搜索输入框
  - 日期选择器
- **验收**: 搜索筛选正常工作

### 7.2 性能优化
- ⏳ 添加数据库索引
  - collection_code + uploaded_at
  - is_deleted
- ⏳ 实现图片懒加载
  - 使用 Intersection Observer
- ⏳ 实现虚拟滚动（可选）
  - 使用 vue-virtual-scroller
- **验收**: 性能测试通过

---

## 阶段 8: 测试与文档

### 8.1 后端测试
- ⏳ 创建 `apps/api/tests/` 目录结构
- ⏳ 编写单元测试（pytest）
  - 配置管理测试
  - 数据库连接测试
  - 服务层测试
- ⏳ 编写集成测试
  - API 端点测试
  - 文件上传测试
- **验收**: 测试覆盖率 > 70%

### 8.2 前端测试
- ⏳ 配置 Vitest
- ⏳ 编写组件测试
  - 通用组件测试
  - 业务组件测试
- **验收**: 测试覆盖率 > 60%

### 8.3 文档编写
- ⏳ API 文档（FastAPI 自动生成）
- ⏳ 用户手册
- ⏳ 管理员手册
- ⏳ 部署指南
- **验收**: 文档完整清晰

---

## 阶段 9: 生产部署

### 9.1 生产配置
- ⏳ 创建 `docker-compose.prod.yml`
  - 生产环境配置
  - 移除 volume 映射（代码打包到镜像）
- ⏳ 优化 Dockerfile
  - 多阶段构建
  - 减小镜像大小
- ⏳ 配置 Nginx HTTPS
  - SSL 证书配置
  - HTTP 重定向到 HTTPS
- **验收**: 生产环境启动成功

### 9.2 备份和监控
- ⏳ 创建 MongoDB 备份脚本
  - 文件: `infrastructure/scripts/backup.sh`
  - 定时任务配置
- ⏳ 配置日志收集（可选）
  - 集中式日志
  - 错误告警
- **验收**: 备份和监控正常运行

---

## 总进度追踪

### 阶段完成状态
- [ ] 阶段 1: 基础设施搭建 (0/7 完成)
- [ ] 阶段 2: 认证系统 (0/2 完成)
- [ ] 阶段 3: 收录码管理 (0/2 完成)
- [ ] 阶段 4: 照片上传系统 (0/2 完成)
- [ ] 阶段 5: 管理后台界面 (0/6 完成)
- [ ] 阶段 6: 统计与数据展示 (0/2 完成)
- [ ] 阶段 7: 搜索筛选与优化 (0/2 完成)
- [ ] 阶段 8: 测试与文档 (0/3 完成)
- [ ] 阶段 9: 生产部署 (0/2 完成)

### 总体进度
**0% 完成** (0/28 子阶段)

---

**最后更新**: 2026-01-13
