# 技术标准文档 (Technical Standards)

## 技术栈选择

### 前端技术栈

#### 核心框架
- **Vue 3** (Composition API)
  - 理由: 渐进式框架，学习曲线平缓，生态成熟
  - 版本: ^3.4.0

#### 构建工具
- **Vite**
  - 理由: 极速开发体验，HMR 快速，官方推荐
  - 版本: ^5.0.0

#### 类型系统
- **TypeScript**
  - 理由: 类型安全，减少运行时错误
  - 版本: ^5.3.0

#### UI 组件库
- **Element Plus**
  - 理由: 成熟的 Vue 3 组件库，组件丰富
  - 版本: ^2.5.0

#### 样式方案
- **Tailwind CSS**
  - 理由: 原子化 CSS，快速开发，易于维护
  - 版本: ^3.4.0

#### 状态管理
- **Pinia**
  - 理由: Vue 3 官方推荐，API 简洁
  - 版本: ^2.1.0

#### 路由管理
- **Vue Router**
  - 理由: Vue 官方路由，功能完善
  - 版本: ^4.2.0

### 后端技术栈

#### Web 框架
- **FastAPI**
  - 理由: 高性能，自动生成 API 文档，异步支持
  - 版本: >=0.109.0

#### 数据库 ODM
- **Beanie**
  - 理由: 基于 Pydantic，类型安全，异步支持
  - 版本: >=1.24.0

#### 数据库
- **MongoDB 7.0**
  - 理由: 灵活的文档存储，适合照片元数据
  - 驱动: Motor (异步)

#### 图片处理
- **Pillow**
  - 理由: Python 标准图片处理库
  - 版本: >=10.2.0

#### 认证
- **JWT**
  - 理由: 无状态认证，适合 API
  - 库: python-jose

### Monorepo 工具

#### 任务编排
- **Nx**
  - 理由: 强大的任务编排，支持多语言
  - 版本: ^18.0.0

#### 包管理器
- **pnpm** (Node.js)
  - 理由: 快速，节省磁盘空间
  - 版本: >=8.0.0

- **uv** (Python)
  - 理由: 10-100x 更快的包管理
  - 安装: pip install uv

### 开发工具

#### 代码质量
- **ESLint** - JavaScript/TypeScript 代码检查
- **Prettier** - 代码格式化
- **Black** - Python 代码格式化

#### 测试框架
- **Vitest** - Vue 组件测试
- **pytest** - Python 单元测试

### 部署方案

#### 容器化
- **Docker** - 应用容器化
- **Docker Compose** - 本地开发编排

#### 反向代理
- **Nginx** - 生产环境反向代理

## 技术决策

### Schema-First 开发
- FastAPI 自动生成 OpenAPI schema
- 使用 openapi-typescript 生成 TypeScript 类型
- 确保前后端类型同步

### 异步优先
- 后端使用 async/await
- 数据库使用异步驱动 (Motor/Beanie)
- 提升并发性能

### 类型安全
- 前端使用 TypeScript
- 后端使用 Pydantic
- 减少运行时错误

## 编码规范

### 命名约定
- **文件名**: kebab-case (photo-list.vue)
- **组件名**: PascalCase (PhotoList)
- **函数名**: camelCase (getUserPhotos)
- **常量**: UPPER_SNAKE_CASE (MAX_FILE_SIZE)

### 目录结构
- 按功能模块组织
- 共享代码放在 packages/
- 应用代码放在 apps/

### Git 提交规范
- feat: 新功能
- fix: 修复 bug
- docs: 文档更新
- style: 代码格式
- refactor: 重构
- test: 测试
- chore: 构建/工具

## 性能标准

- API 响应时间 < 200ms
- 前端首屏加载 < 2s
- 图片上传速度 < 3s/张
- Docker 启动时间 < 30s
