# Context Management System - Quick Reference

## 📂 Context Files Location

```
.context/
├── project-context.json      # Structured context data (machine-readable)
├── PROJECT-CONTEXT.md         # Comprehensive context (human-readable)
└── QUICK-REFERENCE.md         # This file
```

## 🚀 Quick Start for AI Agents

When resuming work on this project, read these files in order:

1. **`.context/QUICK-REFERENCE.md`** (this file) - 2 min overview
2. **`.context/PROJECT-CONTEXT.md`** - 15 min comprehensive understanding
3. **`CONTINUATION-GUIDE.md`** - How to continue development
4. **`.spec-workflow/specs/ALL-PHASES-DESIGN-SUMMARY.md`** - Design decisions

## 📊 Project Status at a Glance

- **Project**: Photo Collection Management System (photo-monorepo)
- **Type**: Full-Stack Web Application (Monorepo)
- **Progress**: 22% (Phase 2 of 9 complete)
- **Current Phase**: ✅ Phase 2 Complete → Ready for Phase 3
- **Last Commit**: `ae26d9a feat: 完成 Phase 2 认证系统实现 - JWT + Admin 登录`
- **Repository**: https://github.com/ZipperCode/photo-monorepo

## 🎯 What's Been Completed

### ✅ Phase 1: Infrastructure Setup (100%)
- Nx + pnpm monorepo structure
- Vue 3 dual frontends (web, admin)
- FastAPI backend with Beanie ODM
- MongoDB 7.0 database
- Docker Compose (6 services)
- OpenAPI → TypeScript type generation

### ✅ Phase 2: Authentication System (100%)
- JWT token authentication (24h expiry)
- bcrypt password hashing (cost factor 12)
- User model and database operations
- Authentication middleware
- Login API endpoints (/login, /me, /verify)
- Beautiful admin login page
- Route guards and auth state management
- Default admin user auto-creation

## 🎯 What's Next

### ⏳ Phase 3: Access Code Management (NEXT)
**Goal**: Implement 6-character access code system

**Key Tasks**:
1. Create Collection model (apps/server/app/models/collection.py)
2. Build code generator (apps/server/app/utils/code_generator.py)
3. Implement code validation endpoint (POST /api/v1/collections/validate)
4. Create admin CRUD endpoints
5. Build collection management UI

## 🏗️ Architecture Overview

```
User Frontend (Vue 3)  ─┐
                        │
Admin Frontend (Vue 3) ─┼─► Nginx ──► FastAPI ──► MongoDB
                        │                │
                        │                └──► Storage
                        └─► Port 80           (Local Files)
```

**Ports**:
- Web: 5173
- Admin: 5174
- API: 8000
- MongoDB: 27017
- Mongo Express: 8081
- Nginx: 80

## 🛠️ Tech Stack Summary

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3 + TypeScript + Vite + Tailwind + Element Plus |
| Backend | FastAPI + Python 3.11+ + Beanie ODM |
| Database | MongoDB 7.0 |
| Monorepo | Nx + pnpm |
| Deployment | Docker Compose |

## 📁 Key Directories

```
apps/
  ├── web/          # User frontend (port 5173)
  ├── admin/        # Admin dashboard (port 5174)
  └── server/       # FastAPI backend (port 8000)
packages/
  ├── ui/           # Shared Vue components
  ├── configs/      # Shared configs
  └── schema/       # OpenAPI types
infrastructure/
  └── docker/       # Dockerfiles
storage/
  ├── uploads/      # Photo storage
  └── thumbnails/   # Generated thumbnails
```

## 🚦 Common Commands

### Development
```bash
pnpm install              # Install all dependencies
pnpm dev                  # Run all dev servers (Nx)
pnpm build                # Build all apps
pnpm type-sync            # Generate TypeScript types from OpenAPI
```

### Docker
```bash
docker-compose up -d      # Start all services
docker-compose down       # Stop all services
docker-compose logs -f    # View logs
```

### Git
```bash
git status                # Check status
git add .                 # Stage changes
git commit -m "message"   # Commit
git push                  # Push to remote
```

## 📋 9 Implementation Phases

1. ✅ **Infrastructure Setup** - Complete
2. ✅ **Authentication System** - Complete
3. ⏳ **Access Code Management** - Next
4. ⏳ **Photo Upload System**
5. ⏳ **Admin Dashboard UI** ⭐ (重点)
6. ⏳ **Statistics & Data Display**
7. ⏳ **Search & Optimization**
8. ⏳ **Testing & Documentation**
9. ⏳ **Production Deployment**

## 🎨 Design Focus: Phase 5

**Phase 5 is critical**: Beautiful admin dashboard with:
- Modern dashboard design
- Responsive photo grid (2/4/6 columns)
- Batch operations (download/delete)
- Lightbox viewer with keyboard navigation
- Professional blue-based color scheme
- Use **ui-ux-pro-max** skill for design guidance

## 🔑 Key Architectural Decisions

1. **MongoDB over PostgreSQL**: Flexible schema for photo metadata
2. **Local Storage with S3 Abstraction**: Start simple, migrate later
3. **Access Codes (No Registration)**: Simplified user flow
4. **Nx Monorepo**: Unified codebase, shared types
5. **Admin UI Priority**: Focus on admin dashboard beauty

## 📚 Essential Documentation

| Document | Purpose |
|----------|---------|
| `.context/PROJECT-CONTEXT.md` | Comprehensive project context |
| `.context/project-context.json` | Structured context data |
| `README.md` | Quick start guide |
| `CONTINUATION-GUIDE.md` | How to resume development |
| `.spec-workflow/specs/ALL-PHASES-DESIGN-SUMMARY.md` | Design decisions |
| `.spec-workflow/specs/IMPLEMENTATION-CHECKLIST.md` | Task checklist |

## 🎯 How to Resume Development

### For AI Agents
1. Read `.context/PROJECT-CONTEXT.md` for full understanding
2. Check current phase status above
3. Read phase-specific requirements in `.spec-workflow/specs/`
4. Start implementing next phase tasks

### For Developers
1. Read `CONTINUATION-GUIDE.md`
2. Review `.context/PROJECT-CONTEXT.md`
3. Set up development environment (see Quick Start)
4. Start Phase 3 implementation

## 🔍 Context Search Tips

### For AI Agents
When searching for information:
- **API Endpoints**: Check `.context/project-context.json` → `api_endpoints`
- **Database Schema**: Check `.context/PROJECT-CONTEXT.md` → "Database Schema"
- **Architecture**: Check `.context/PROJECT-CONTEXT.md` → "Architecture"
- **Tech Stack**: Check `.context/PROJECT-CONTEXT.md` → "Technology Stack"
- **Design Patterns**: Check `.spec-workflow/specs/ALL-PHASES-DESIGN-SUMMARY.md`

## 🧠 Knowledge Graph

**Key Relationships**:
- `apps/web` → `apps/server` (REST API via Axios)
- `apps/admin` → `apps/server` (REST API via Axios)
- `apps/server` → `mongodb` (Beanie ODM via Motor)
- `apps/server` → `storage/uploads` (Local filesystem)
- `packages/schema` → `apps/web`, `apps/admin` (TypeScript types)
- `packages/ui` → `apps/web`, `apps/admin` (Shared components)

## 📊 Progress Tracking

| Metric | Value |
|--------|-------|
| Phases Complete | 2 / 9 |
| Overall Progress | 22% |
| Code Files Created | ~65 |
| API Endpoints Implemented | 3 |
| Components Implemented | 3 |
| Database Collections | 1 (users) |

**Default Admin Credentials**:
- Username: `admin`
- Password: `admin123456`
- ⚠️ CHANGE IN PRODUCTION

## 🎉 Success Criteria

Project will be considered complete when:
- ✅ All 9 phases implemented
- ✅ Beautiful admin dashboard operational
- ✅ Photo upload working with thumbnails
- ✅ Batch download/delete functional
- ✅ Tests passing (>70% coverage)
- ✅ Docker one-command deployment
- ✅ Documentation complete
- ✅ Production-ready

## 🔐 Security Highlights

- bcrypt password hashing (cost factor 12)
- JWT tokens (24h expiry)
- File validation (magic numbers + MIME)
- CORS configuration
- Authentication middleware
- Input validation (Pydantic)

## 🚀 Performance Targets

- First screen load: < 2s
- API response: < 200ms
- Thumbnail generation: < 500ms
- Lazy loading: 60% bandwidth savings
- Virtual scrolling: 1000+ photos smooth

## 💡 Tips for AI Agents

### When Starting a New Phase
1. Read phase requirements from `.spec-workflow/specs/phase-X-*/requirements.md`
2. Check design document `.spec-workflow/specs/phase-X-*/design.md`
3. Review API endpoints in `.context/project-context.json`
4. Reference similar patterns from previous phases

### When Stuck
1. Check `.context/PROJECT-CONTEXT.md` for architectural decisions
2. Review `.spec-workflow/specs/ALL-PHASES-DESIGN-SUMMARY.md`
3. Search codebase for similar implementations
4. Ask user for clarification

### Best Practices
- Always read context files before starting
- Update context after completing major features
- Keep API endpoints consistent with design
- Follow existing code patterns
- Use TypeScript types from `packages/schema`

## 📞 Need Help?

- **Project Context**: `.context/PROJECT-CONTEXT.md`
- **Design Decisions**: `.spec-workflow/specs/ALL-PHASES-DESIGN-SUMMARY.md`
- **Task List**: `.spec-workflow/specs/IMPLEMENTATION-CHECKLIST.md`
- **Git Issues**: https://github.com/ZipperCode/photo-monorepo/issues

---

**Last Updated**: 2026-01-15
**Context Version**: 2.0
**Status**: ✅ Phase 2 Complete - Ready for Phase 3
**Context Fingerprint**: `photo-monorepo-2026-01-15-phase2-complete`
