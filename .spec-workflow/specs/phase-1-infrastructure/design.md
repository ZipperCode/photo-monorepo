# 阶段 1: 基础设施搭建 - 设计文档

## 概述

建立一个基于 Monorepo 的照片收录管理系统基础架构，采用前后端分离的架构设计，使用 Docker 实现容器化部署。前端使用 Vue 3 + Vite + TypeScript + Tailwind CSS，后端使用 FastAPI + MongoDB，所有服务通过 Docker Compose 编排管理。

## 指导文档对齐

### 技术标准 (tech.md)
- 前端框架: Vue 3 (Composition API)
- 构建工具: Vite
- 后端框架: FastAPI
- 数据库: MongoDB (Motor 异步驱动)
- 容器化: Docker + Docker Compose
- 样式框架: Tailwind CSS

### 项目结构 (structure.md)
遵循 Monorepo 结构，前后端分离在 `apps/` 目录下，基础设施配置在 `infrastructure/` 目录下。

## 代码复用分析

### 现有组件利用
此阶段为项目初始化阶段，无现有代码可复用。

### 集成点
- **Docker Network**: 所有容器通过自定义网络 `photo-network` 通信
- **Volume 持久化**: MongoDB 数据和本地文件存储通过 volume 持久化
- **Nginx 反向代理**: 统一入口，路由前后端请求

## 架构

### 整体架构图

```mermaid
graph TB
    Client[浏览器客户端] -->|HTTP| Nginx[Nginx 反向代理]
    Nginx -->|/| Web[Vue 3 前端]
    Nginx -->|/api| API[FastAPI 后端]
    API -->|Motor| MongoDB[(MongoDB 数据库)]
    API -->|文件系统| Storage[本地存储]

    subgraph Docker Network
        Nginx
        Web
        API
        MongoDB
    end
```

### 模块化设计原则
- **单文件职责**: main.py 仅负责应用启动，config.py 仅负责配置管理，database.py 仅负责数据库连接
- **组件隔离**: 前后端完全独立，可分别开发和部署
- **服务层分离**: 数据访问层 (database.py)、配置层 (config.py)、应用层 (main.py) 清晰分离

## 组件和接口

### 组件 1: Vue 3 前端应用 (apps/web)
- **目的**: 提供用户界面和交互
- **接口**:
  - HTTP API 调用 (通过 axios/fetch)
  - 路由导航 (Vue Router)
  - 状态管理 (Pinia stores)
- **依赖**: Vite, Vue Router, Pinia, Tailwind CSS, TypeScript
- **复用**: 无（新建项目）

### 组件 2: FastAPI 后端应用 (apps/api)
- **目的**: 提供 RESTful API 服务
- **接口**:
  - `GET /health` - 健康检查
  - `GET /docs` - API 文档 (Swagger UI)
  - CORS 中间件 - 跨域支持
- **依赖**: FastAPI, Uvicorn, Motor, Pydantic
- **复用**: 无（新建项目）

### 组件 3: MongoDB 数据库
- **目的**: 持久化存储业务数据
- **接口**: MongoDB 协议 (27017 端口)
- **依赖**: Motor (Python 异步驱动)
- **复用**: 官方 MongoDB Docker 镜像

### 组件 4: Nginx 反向代理
- **目的**: 统一入口，路由前后端请求
- **接口**:
  - `/` -> Vue 前端 (5173 端口)
  - `/api` -> FastAPI 后端 (8000 端口)
- **依赖**: Nginx Alpine 镜像
- **复用**: 官方 Nginx 配置模板

### 组件 5: 配置管理 (apps/api/app/core/config.py)
- **目的**: 集中管理应用配置
- **接口**:
  - `Settings` Pydantic 模型
  - `get_settings()` 函数
- **依赖**: Pydantic, python-dotenv
- **复用**: Pydantic BaseSettings 模式

### 组件 6: 数据库连接 (apps/api/app/core/database.py)
- **目的**: 管理 MongoDB 连接生命周期
- **接口**:
  - `connect_to_mongo()` - 建立连接
  - `close_mongo_connection()` - 关闭连接
  - `get_database()` - 获取数据库实例
- **依赖**: Motor
- **复用**: Motor 官方连接模式

## 数据模型

### 配置模型 (Settings)
```python
class Settings(BaseSettings):
    # 应用配置
    app_name: str = "Photo Collection System"
    environment: str = "development"

    # MongoDB 配置
    mongodb_url: str
    mongodb_db_name: str = "photo_system"

    # 存储配置
    storage_type: str = "local"
    storage_path: str = "./storage"

    # 安全配置
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expires_minutes: int = 1440  # 24 hours

    # CORS 配置
    cors_origins: list[str] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"
```

## 项目目录结构

```
photo-monorepo/
├── apps/
│   ├── web/                    # Vue 3 前端
│   │   ├── src/
│   │   │   ├── assets/
│   │   │   ├── components/
│   │   │   ├── composables/
│   │   │   ├── pages/
│   │   │   ├── router/
│   │   │   ├── stores/
│   │   │   ├── services/
│   │   │   ├── App.vue
│   │   │   └── main.ts
│   │   ├── public/
│   │   ├── index.html
│   │   ├── package.json
│   │   ├── vite.config.ts
│   │   ├── tailwind.config.js
│   │   └── tsconfig.json
│   │
│   └── api/                    # FastAPI 后端
│       ├── app/
│       │   ├── api/
│       │   │   └── v1/
│       │   ├── core/
│       │   │   ├── config.py
│       │   │   └── database.py
│       │   ├── models/
│       │   ├── schemas/
│       │   ├── services/
│       │   ├── main.py
│       │   └── __init__.py
│       ├── requirements.txt
│       └── .env.example
│
├── infrastructure/
│   ├── docker/
│   │   ├── api/
│   │   │   └── Dockerfile
│   │   ├── web/
│   │   │   └── Dockerfile
│   │   └── nginx/
│   │       ├── Dockerfile
│       └── nginx.conf
│   └── scripts/
│       └── init-db.sh
│
├── storage/                    # 本地存储 (gitignored)
│   ├── uploads/
│   └── thumbnails/
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## 错误处理

### 错误场景

1. **场景: MongoDB 连接失败**
   - **处理**: 记录详细错误日志，重试 3 次（间隔 2 秒），最终失败则退出应用
   - **用户影响**: API 服务无法启动，返回 503 Service Unavailable

2. **场景: 环境变量缺失**
   - **处理**: 使用默认值或抛出 ValidationError，记录警告日志
   - **用户影响**: 配置不当可能导致功能异常

3. **场景: Docker 容器启动失败**
   - **处理**: Docker Compose 显示错误日志，容器自动重启（最多 3 次）
   - **用户影响**: 服务暂时不可用

4. **场景: Nginx 反向代理配置错误**
   - **处理**: Nginx 配置测试失败，容器无法启动
   - **用户影响**: 无法通过 80 端口访问应用

## Docker Compose 配置

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:7.0
    container_name: photo-mongo
    restart: unless-stopped
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD}
    volumes:
      - mongo_data:/data/db
    networks:
      - photo-network

  api:
    build:
      context: ./apps/api
      dockerfile: ../../infrastructure/docker/api/Dockerfile
    container_name: photo-api
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://admin:${MONGO_PASSWORD}@mongodb:27017/photo_system?authSource=admin
      - STORAGE_PATH=/app/storage
      - JWT_SECRET=${JWT_SECRET}
      - ENVIRONMENT=development
    volumes:
      - ./apps/api:/app
      - ./storage:/app/storage
    depends_on:
      - mongodb
    networks:
      - photo-network
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  web:
    build:
      context: ./apps/web
      dockerfile: ../../infrastructure/docker/web/Dockerfile
    container_name: photo-web
    restart: unless-stopped
    ports:
      - "5173:5173"
    environment:
      - VITE_API_URL=http://localhost:8000/api/v1
    volumes:
      - ./apps/web:/app
      - /app/node_modules
    networks:
      - photo-network
    command: npm run dev -- --host

  nginx:
    image: nginx:alpine
    container_name: photo-nginx
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - ./infrastructure/docker/nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - api
      - web
    networks:
      - photo-network

volumes:
  mongo_data:

networks:
  photo-network:
    driver: bridge
```

## 测试策略

### 单元测试
- 后端: 使用 pytest 测试配置加载和数据库连接逻辑
- 前端: 使用 Vitest 测试基础组件渲染

### 集成测试
- Docker Compose 启动测试: 验证所有容器成功启动
- 健康检查测试: 验证 API `/health` 端点响应正常
- 网络通信测试: 验证容器间可以正常通信

### 端到端测试
- 访问 http://localhost:80 验证 Nginx 正常工作
- 访问 http://localhost:8000/docs 验证 API 文档可访问
- 访问 http://localhost:5173 验证前端页面可访问
