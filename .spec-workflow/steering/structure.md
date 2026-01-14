# 项目结构文档 (Project Structure)

## Monorepo 架构

本项目采用 Monorepo 架构，使用 pnpm workspace 和 Nx 进行管理。

## 目录结构

```
photo-monorepo/
├── apps/                       # 应用程序
│   ├── web/                    # 用户前端
│   ├── admin/                  # 管理后台
│   └── server/                 # 后端 API
├── packages/                   # 共享包
│   ├── ui/                     # UI 组件库
│   ├── configs/                # 共享配置
│   └── schema/                 # 类型定义
├── infrastructure/             # 基础设施
│   ├── docker/                 # Docker 配置
│   └── scripts/                # 工具脚本
├── storage/                    # 本地存储
├── .spec-workflow/             # 规范文档
└── .claude/                    # Claude 配置
```

## 应用程序 (apps/)

### apps/web/ - 用户前端
```
web/
├── src/
│   ├── assets/         # 静态资源
│   ├── components/     # Vue 组件
│   ├── composables/    # 组合式函数
│   ├── pages/          # 页面组件
│   ├── router/         # 路由配置
│   ├── stores/         # Pinia 状态
│   ├── services/       # API 服务
│   ├── App.vue         # 根组件
│   └── main.ts         # 入口文件
├── public/             # 公共资源
├── index.html          # HTML 模板
├── vite.config.ts      # Vite 配置
├── tsconfig.json       # TS 配置
└── package.json        # 依赖配置
```

### apps/admin/ - 管理后台
```
admin/
├── src/
│   ├── assets/
│   ├── components/
│   ├── composables/
│   ├── pages/
│   ├── router/
│   ├── stores/
│   ├── services/
│   ├── App.vue
│   └── main.ts
├── public/
├── index.html
├── vite.config.ts
├── tsconfig.json
└── package.json
```

### apps/server/ - 后端 API
```
server/
├── app/
│   ├── api/            # API 路由
│   │   └── v1/         # API v1
│   ├── core/           # 核心模块
│   │   ├── config.py   # 配置
│   │   └── database.py # 数据库
│   ├── models/         # 数据模型
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # 业务逻辑
│   └── main.py         # 应用入口
├── pyproject.toml      # Python 配置
└── .env.example        # 环境变量模板
```

## 共享包 (packages/)

### packages/ui/ - UI 组件库
```
ui/
├── src/
│   ├── components/     # 共享组件
│   └── index.ts        # 导出文件
└── package.json
```

### packages/configs/ - 共享配置
```
configs/
├── eslint.config.js    # ESLint 配置
├── tailwind.config.js  # Tailwind 配置
├── vite.config.base.ts # Vite 基础配置
└── package.json
```

### packages/schema/ - 类型定义
```
schema/
├── openapi.json        # OpenAPI schema (生成)
├── types.ts            # TS 类型 (生成)
└── package.json
```

## 基础设施 (infrastructure/)

### infrastructure/docker/
```
docker/
├── server/
│   └── Dockerfile      # 后端容器
├── web/
│   └── Dockerfile      # Web 容器
├── admin/
│   └── Dockerfile      # Admin 容器
└── nginx/
    └── nginx.conf      # Nginx 配置
```

### infrastructure/scripts/
```
scripts/
└── generate-openapi.sh # 生成 OpenAPI schema
```

## 配置文件

### 根目录配置
- `pnpm-workspace.yaml` - pnpm 工作区
- `nx.json` - Nx 配置
- `package.json` - 根 package.json
- `docker-compose.yml` - Docker 编排
- `.env.example` - 环境变量模板
- `.gitignore` - Git 忽略规则

## 命名规范

### 文件命名
- 组件文件: PascalCase (PhotoCard.vue)
- 工具文件: kebab-case (format-date.ts)
- 配置文件: kebab-case (vite.config.ts)

### 目录命名
- 全部使用 kebab-case
- 复数形式: components/, services/, models/

## 依赖管理

### Workspace 协议
- 使用 `workspace:*` 引用内部包
- 示例: `"@photo/ui": "workspace:*"`

### 版本管理
- 锁定主要版本
- 定期更新依赖
- 使用 pnpm 锁文件
