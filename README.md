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
- **Vue 3** - 渐进式 JavaScript 框架
- **TypeScript** - 类型安全
- **Vite** - 极速开发体验
- **Tailwind CSS** - 实用优先的 CSS 框架
- **Pinia** - Vue 状态管理
- **Vue Router** - 路由管理

### 后端
- **FastAPI** - 现代高性能 Web 框架
- **Python 3.11+** - 异步编程支持
- **Motor** - MongoDB 异步驱动
- **Pillow** - 图片处理
- **JWT** - 身份认证

### 数据库 & 部署
- **MongoDB 7.0** - NoSQL 文档数据库
- **Docker** - 容器化部署
- **Nginx** - 反向代理

## 📂 项目结构

```
photo-monorepo/
├── apps/
│   ├── web/                    # Vue 3 前端应用
│   └── api/                    # FastAPI 后端应用
├── infrastructure/             # Docker 配置
├── .spec-workflow/             # 项目规范文档
│   └── specs/                  # 实施规范
│       ├── README.md           # 总览
│       ├── ALL-PHASES-DESIGN-SUMMARY.md
│       └── IMPLEMENTATION-CHECKLIST.md
├── CONTINUATION-GUIDE.md       # 续工指南
└── README.md                   # 本文件
```

## 🚀 快速开始

### 环境要求

- Node.js 18+
- Python 3.11+
- Docker & Docker Compose
- Git

### 开发环境搭建

```bash
# 1. 克隆仓库
git clone git@github.com:ZipperCode/photo-monorepo.git
cd photo-monorepo

# 2. 复制环境变量模板
cp .env.example .env

# 3. 启动所有服务 (Docker)
docker-compose up -d

# 4. 访问应用
# 前端: http://localhost:80
# API 文档: http://localhost:8000/docs
# MongoDB: localhost:27017
```

### 手动开发（不使用 Docker）

#### 前端开发
```bash
cd apps/web
npm install
npm run dev
# 访问 http://localhost:5173
```

#### 后端开发
```bash
cd apps/api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# 访问 http://localhost:8000
```

## 📋 实施进度

### 9 个实施阶段

| 阶段 | 名称 | 优先级 | 状态 |
|------|------|--------|------|
| 1 | 基础设施搭建 | 关键 | ⏳ 待开始 |
| 2 | 认证系统 | 高 | ⏳ 待开始 |
| 3 | 收录码管理 | 关键 | ⏳ 待开始 |
| 4 | 照片上传系统 | 关键 | ⏳ 待开始 |
| 5 | 管理后台界面设计 ⭐ | 关键 (重点) | ⏳ 待开始 |
| 6 | 统计与数据展示 | 中 | ⏳ 待开始 |
| 7 | 搜索筛选与优化 | 中 | ⏳ 待开始 |
| 8 | 测试与文档 | 高 | ⏳ 待开始 |
| 9 | 生产部署 | 关键 | ⏳ 待开始 |

**当前状态**: 📝 规划完成，待开始实施

详细的实施计划和任务清单请查看：
- **实施计划**: `.claude/plans/iridescent-juggling-pearl.md`
- **任务清单**: `.spec-workflow/specs/IMPLEMENTATION-CHECKLIST.md`
- **续工指南**: `CONTINUATION-GUIDE.md`

## 📖 文档

- [续工指南](./CONTINUATION-GUIDE.md) - 如何继续项目开发
- [实施总览](./.spec-workflow/specs/README.md) - 所有阶段概述
- [设计汇总](./.spec-workflow/specs/ALL-PHASES-DESIGN-SUMMARY.md) - 技术决策和组件设计
- [任务清单](./.spec-workflow/specs/IMPLEMENTATION-CHECKLIST.md) - 可执行的任务列表

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
