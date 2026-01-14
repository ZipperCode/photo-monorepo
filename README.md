# 照片收录管理系统 (Photo Collection System)

一个基于 Web 的照片收录管理系统，用户通过输入收录码上传照片，管理员在后台查看、管理和批量下载所有照片。

## ✨ 特性

- 🎫 **收录码系统** - 管理员创建唯一收录码，用户通过收录码上传
- 📤 **批量上传** - 支持拖拽、多文件选择、实时进度显示
- 🎨 **美观的管理后台** - 现代化设计，流畅的操作体验
- ⬇️ **灵活下载** - 单张下载 / 批量下载 / 一键下载全部
- 🗑️ **批量管理** - 支持批量删除和一键清空
- 🐳 **Docker 部署** - 一键启动，快速部署

## 🛠️ 技术栈

### 前端
- **Vue 3** - 渐进式 JavaScript 框架 (Composition API)
- **TypeScript** - 类型安全
- **Vite** - 极速开发体验
- **Tailwind CSS** - 实用优先的 CSS 框架
- **Element Plus** - Vue 3 组件库
- **Pinia** - Vue 状态管理
- **Vue Router** - 路由管理

### 后端
- **FastAPI** - 现代高性能 Web 框架
- **Python 3.11+** - 异步编程支持
- **Beanie ODM** - MongoDB 异步 ODM (基于 Motor)
- **Pillow** - 图片处理
- **JWT** - 身份认证
- **uv** - 快速 Python 包管理器

### Monorepo 工具
- **Nx** - 任务编排和缓存
- **pnpm** - 高效的 Node.js 包管理器
- **Schema-First** - OpenAPI → TypeScript 类型生成

### 数据库 & 部署
- **MongoDB 7.0** - NoSQL 文档数据库
- **Mongo Express** - MongoDB Web 管理界面
- **Docker** - 容器化部署
- **Nginx** - 反向代理

## 📂 项目结构

```
photo-monorepo/
├── apps/
│   ├── web/                    # Vue 3 用户前端 (port 5173)
│   ├── admin/                  # Vue 3 管理后台 (port 5174)
│   └── server/                 # FastAPI 后端 (port 8000)
├── packages/
│   ├── ui/                     # 共享 Vue 组件库
│   ├── configs/                # 共享配置 (ESLint, Tailwind, Vite)
│   └── schema/                 # OpenAPI schema 和 TypeScript 类型
├── infrastructure/
│   ├── docker/                 # Dockerfiles
│   └── scripts/                # 工具脚本
├── storage/                    # 本地文件存储 (gitignored)
├── .spec-workflow/             # 项目规范文档
├── docker-compose.yml          # 服务编排 (6 个服务)
├── pnpm-workspace.yaml         # pnpm 工作区配置
├── nx.json                     # Nx 任务编排配置
└── README.md                   # 本文件
```

## 🚀 快速开始

### 环境要求

- **Node.js** >= 20.0.0
- **pnpm** >= 8.0.0
- **Python** >= 3.11
- **Docker** & **Docker Compose**
- **uv** (Python 包管理器) - `pip install uv`

### 一键启动 (Docker)

```bash
# 1. 克隆仓库
git clone git@github.com:ZipperCode/photo-monorepo.git
cd photo-monorepo

# 2. 复制并配置环境变量
cp .env.example .env
# 编辑 .env 设置密码: MONGO_PASSWORD, JWT_SECRET

# 3. 启动所有服务 (6 个容器)
docker-compose up -d

# 4. 访问应用
# 用户前端: http://localhost:5173
# 管理后台: http://localhost:5174
# API 文档: http://localhost:8000/docs
# Mongo Express: http://localhost:8081
# Nginx 入口: http://localhost:80
```

### 手动开发（不使用 Docker）

#### 安装依赖
```bash
# 安装 Node.js 依赖 (使用 pnpm)
pnpm install
```

#### 后端开发
```bash
cd apps/server
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -e .

# 创建 .env 文件并配置 MongoDB 连接
cp .env.example .env

# 启动后端
uvicorn app.main:app --reload
# 访问 http://localhost:8000
# API 文档: http://localhost:8000/docs
```

#### 前端开发 (Web)
```bash
cd apps/web
pnpm dev
# 访问 http://localhost:5173
```

#### 前端开发 (Admin)
```bash
cd apps/admin
pnpm dev
# 访问 http://localhost:5174
```

#### 使用 Nx 运行所有服务
```bash
# 一键启动所有开发服务
pnpm dev

# 构建所有应用
pnpm build

# 类型同步 (从 FastAPI 生成 TypeScript 类型)
pnpm type-sync
```

## 📋 实施进度

### 9 个实施阶段

| 阶段 | 名称 | 优先级 | 状态 |
|------|------|--------|------|
| 1 | 基础设施搭建 | 关键 | ✅ 已完成 |
| 2 | 认证系统 | 高 | ⏳ 待开始 |
| 3 | 收录码管理 | 关键 | ⏳ 待开始 |
| 4 | 照片上传系统 | 关键 | ⏳ 待开始 |
| 5 | 管理后台界面设计 ⭐ | 关键 (重点) | ⏳ 待开始 |
| 6 | 统计与数据展示 | 中 | ⏳ 待开始 |
| 7 | 搜索筛选与优化 | 中 | ⏳ 待开始 |
| 8 | 测试与文档 | 高 | ⏳ 待开始 |
| 9 | 生产部署 | 关键 | ⏳ 待开始 |

**当前状态**: ✅ Phase 1 完成 - 现代化 Monorepo 基础设施已搭建

### Phase 1 完成内容

✅ **Monorepo 架构**
- Nx 任务编排配置
- pnpm 工作区管理
- 共享包结构 (ui, configs, schema)

✅ **后端 (FastAPI + Beanie ODM)**
- FastAPI 应用框架
- Beanie ODM 集成
- MongoDB 连接管理
- 健康检查端点
- CORS 中间件

✅ **前端 (Vue 3 双应用)**
- Web 用户前端 (port 5173)
- Admin 管理后台 (port 5174)
- Element Plus 组件库
- Vue Router + Pinia
- Tailwind CSS 样式

✅ **Docker 容器化**
- 6 个服务编排 (MongoDB, Mongo Express, Server, Web, Admin, Nginx)
- 开发环境热重载
- Nginx 反向代理配置

✅ **Schema-First 开发**
- OpenAPI schema 生成
- TypeScript 类型自动生成
- 前后端类型同步机制

详细的实施计划和任务清单请查看：
- **实施计划**: `.claude/plans/delegated-watching-cray.md`
- **任务清单**: `.spec-workflow/specs/IMPLEMENTATION-CHECKLIST.md`
- **续工指南**: `CONTINUATION-GUIDE.md`

## 📖 文档

### 核心文档
- [续工指南](./CONTINUATION-GUIDE.md) - 如何继续项目开发
- [实施总览](./.spec-workflow/specs/README.md) - 所有阶段概述
- [设计汇总](./.spec-workflow/specs/ALL-PHASES-DESIGN-SUMMARY.md) - 技术决策和组件设计
- [任务清单](./.spec-workflow/specs/IMPLEMENTATION-CHECKLIST.md) - 可执行的任务列表

### 项目上下文（AI 辅助开发）
- [快速参考](./.context/QUICK-REFERENCE.md) - 2 分钟项目概览
- [完整上下文](./.context/PROJECT-CONTEXT.md) - 15 分钟深度理解
- [上下文系统](./.context/README.md) - 上下文管理系统说明

> 💡 **AI 开发提示**: 使用 `.context/` 目录中的文档可以让 AI 助手（Claude、GPT 等）更准确地理解项目架构和技术决策。

## 🎨 UI/UX 设计

本项目重点打造美观专业的管理后台界面：

- ✅ 现代化设计风格
- ✅ 响应式布局（移动/平板/桌面）
- ✅ 流畅的交互动画
- ✅ 优雅的配色方案
- ✅ 清晰的操作反馈

设计指导使用 **ui-ux-pro-max** 技能提供。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**创建时间**: 2026-01-13
**项目状态**: 📝 规划完成，待开始实施
**仓库地址**: https://github.com/ZipperCode/photo-monorepo
