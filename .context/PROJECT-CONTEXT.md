# Photo Collection Management System - Comprehensive Project Context

**Generated**: 2026-01-14T22:05:00Z
**Context Fingerprint**: `photo-monorepo-2026-01-14-initial`
**Last Commit**: `7c28e0a feat: 完成 Phase 1 基础设施搭建 - 现代化 Monorepo 架构`
**Project Status**: Phase 1 Complete (11% overall completion)

---

## 📋 Executive Summary

**Photo Collection Management System** is a modern, full-stack web application designed for photo collection management. Users upload photos via unique access codes, while administrators manage, view, and download photos through a beautiful dashboard interface.

### Quick Facts
- **Architecture**: Monorepo with microservices
- **Frontend**: Vue 3 + TypeScript + Tailwind CSS
- **Backend**: FastAPI (Python 3.11+) + MongoDB
- **Deployment**: Docker Compose (6 services)
- **Current Progress**: 11% (Phase 1 of 9 complete)
- **Repository**: https://github.com/ZipperCode/photo-monorepo

---

## 🎯 Project Overview

### Core Functionality
1. **User Side**: Simple access code input → batch photo upload with drag-and-drop
2. **Admin Side**: Beautiful dashboard → manage collections → view/download/delete photos

### Key Design Principles
- **Access Code System**: No user registration; access codes act as permission tokens
- **Admin-First UX**: Focus on creating a stunning, professional admin dashboard
- **Modern Stack**: Latest technologies for optimal developer experience
- **Docker-First**: One-command deployment for all environments
- **Schema-First**: OpenAPI → TypeScript type generation for type safety

---

## 🏗️ Architecture

### System Architecture Diagram
```
┌─────────────────────────────────────────────────────────────┐
│                         Nginx (Port 80)                      │
│                      Reverse Proxy Layer                     │
└────────────┬────────────────┬────────────────┬──────────────┘
             │                │                │
             ▼                ▼                ▼
    ┌────────────────┐ ┌────────────────┐ ┌─────────────────┐
    │  Vue 3 Web     │ │  Vue 3 Admin   │ │  FastAPI Server │
    │  Port 5173     │ │  Port 5174     │ │  Port 8000      │
    │  (User App)    │ │  (Admin App)   │ │  (API Backend)  │
    └────────────────┘ └────────────────┘ └────────┬─────────┘
                                                    │
                                    ┌───────────────┴───────────────┐
                                    │                               │
                                    ▼                               ▼
                            ┌───────────────┐              ┌────────────────┐
                            │  MongoDB 7.0  │              │ Storage System │
                            │  Port 27017   │              │ (Local Files)  │
                            └───────┬───────┘              └────────────────┘
                                    │
                                    ▼
                            ┌───────────────┐
                            │ Mongo Express │
                            │  Port 8081    │
                            │  (Admin UI)   │
                            └───────────────┘
```

### Technology Stack

#### Frontend
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Framework | Vue 3 | 3.4.0 | Composition API, reactive UI |
| Language | TypeScript | 5.3.2 | Type safety |
| Build Tool | Vite | 5.0.0 | Fast HMR, optimized builds |
| UI Library | Element Plus | 2.5.0 | Component library |
| CSS | Tailwind CSS | Latest | Utility-first styling |
| State | Pinia | Latest | Vue state management |
| Routing | Vue Router | Latest | Client-side routing |
| HTTP Client | Axios | 1.6.0 | API communication |

**Two Frontend Applications**:
1. **web** (Port 5173): User-facing upload interface
2. **admin** (Port 5174): Administrator dashboard

#### Backend
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Framework | FastAPI | Latest | Async Python web framework |
| Language | Python | 3.11+ | Backend logic |
| ODM | Beanie | Latest | MongoDB object-document mapper |
| Database Driver | Motor | Latest | Async MongoDB driver |
| Authentication | python-jose | Latest | JWT token generation |
| Password Hashing | passlib[bcrypt] | Latest | Secure password storage |
| Image Processing | Pillow | Latest | Thumbnail generation |
| Package Manager | uv | Latest | Fast Python package management |

#### Database & Infrastructure
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Database | MongoDB | 7.0 | NoSQL document store |
| Database UI | Mongo Express | Latest | Web-based MongoDB admin |
| Reverse Proxy | Nginx | Alpine | Load balancing, static serving |
| Containerization | Docker | Latest | Service isolation |
| Orchestration | Docker Compose | Latest | Multi-container management |

#### Monorepo Tools
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Task Orchestration | Nx | 18.0.0 | Monorepo build system |
| Package Manager | pnpm | 8.15.0 | Fast, efficient node modules |
| Workspace | pnpm workspaces | - | Monorepo package linking |
| Type Generation | OpenAPI → TS | - | Schema-first development |

---

## 📁 Project Structure

```
photo-monorepo/
├── apps/
│   ├── web/                           # Vue 3 User Frontend (Port 5173)
│   │   ├── src/
│   │   │   ├── main.ts               # Application entry point
│   │   │   ├── App.vue               # Root component
│   │   │   ├── router/               # Vue Router configuration
│   │   │   ├── stores/               # Pinia stores
│   │   │   ├── pages/                # Page components
│   │   │   ├── components/           # Reusable components
│   │   │   └── services/             # API service layer
│   │   ├── package.json
│   │   └── vite.config.ts
│   │
│   ├── admin/                         # Vue 3 Admin Dashboard (Port 5174)
│   │   ├── src/
│   │   │   ├── main.ts               # Application entry point
│   │   │   ├── App.vue               # Root component
│   │   │   ├── router/               # Vue Router (with auth guards)
│   │   │   ├── stores/               # Pinia stores (auth, photos)
│   │   │   ├── pages/                # Admin pages
│   │   │   │   ├── Dashboard.vue     # Main dashboard with stats
│   │   │   │   ├── CollectionDetail.vue  # Photo management
│   │   │   │   └── Login.vue         # Admin login
│   │   │   └── components/
│   │   │       └── admin/            # Admin-specific components
│   │   │           ├── PhotoGrid.vue
│   │   │           ├── PhotoCard.vue
│   │   │           ├── Lightbox.vue
│   │   │           ├── PhotoToolbar.vue
│   │   │           └── StatCard.vue
│   │   ├── package.json
│   │   └── vite.config.ts
│   │
│   └── server/                        # FastAPI Backend (Port 8000)
│       ├── app/
│       │   ├── main.py               # FastAPI application entry
│       │   ├── core/                 # Core functionality
│       │   │   ├── config.py         # Settings management
│       │   │   ├── database.py       # MongoDB connection
│       │   │   └── security.py       # JWT, password hashing
│       │   ├── models/               # Beanie ODM models
│       │   │   ├── user.py           # Admin user model
│       │   │   ├── collection.py     # Access code model
│       │   │   └── photo.py          # Photo metadata model
│       │   ├── schemas/              # Pydantic schemas
│       │   ├── api/
│       │   │   └── v1/               # API version 1
│       │   │       ├── auth.py       # Authentication endpoints
│       │   │       ├── collections.py # Access code validation
│       │   │       ├── photos.py     # Photo upload
│       │   │       └── admin.py      # Admin CRUD operations
│       │   ├── services/             # Business logic layer
│       │   │   ├── collection_service.py
│       │   │   ├── photo_service.py
│       │   │   ├── storage_service.py
│       │   │   └── image_service.py
│       │   └── utils/                # Utilities
│       │       └── code_generator.py # 6-char code generation
│       ├── pyproject.toml
│       └── uv.lock
│
├── packages/
│   ├── ui/                           # Shared Vue Component Library
│   │   ├── src/
│   │   │   ├── index.ts             # Component exports
│   │   │   └── components/          # Common components
│   │   └── package.json
│   │
│   ├── configs/                      # Shared Configuration
│   │   ├── eslint.config.js
│   │   ├── tailwind.config.base.js
│   │   ├── vite.config.base.ts
│   │   └── package.json
│   │
│   └── schema/                       # OpenAPI Schema & Types
│       ├── openapi.yaml              # API specification
│       ├── types.ts                  # Generated TypeScript types
│       └── package.json
│
├── infrastructure/
│   ├── docker/                       # Dockerfiles
│   │   ├── server/
│   │   │   └── Dockerfile            # Python backend
│   │   ├── web/
│   │   │   └── Dockerfile            # Web frontend
│   │   ├── admin/
│   │   │   └── Dockerfile            # Admin frontend
│   │   └── nginx/
│   │       └── nginx.conf            # Nginx configuration
│   └── scripts/                      # Utility scripts
│       ├── generate-types.js         # OpenAPI → TypeScript
│       └── backup-mongodb.sh         # Database backup
│
├── storage/                          # Local File Storage (gitignored)
│   ├── uploads/                      # Original photos
│   │   └── {collection_code}/
│   │       └── {year}/
│   │           └── {month}/
│   │               └── {uuid}_{filename}
│   └── thumbnails/                   # Generated thumbnails
│       └── {collection_code}/
│           └── {year}/
│               └── {month}/
│                   └── {uuid}_thumb.jpg
│
├── .spec-workflow/                   # Project Planning & Specs
│   ├── specs/
│   │   ├── README.md                 # All phases overview
│   │   ├── ALL-PHASES-DESIGN-SUMMARY.md
│   │   ├── IMPLEMENTATION-CHECKLIST.md
│   │   └── phase-1-infrastructure/
│   │       ├── requirements.md
│   │       └── design.md
│   ├── steering/                     # Steering documents
│   ├── templates/                    # Document templates
│   └── approvals/                    # Approval tracking
│
├── .context/                         # Context Management (NEW)
│   ├── project-context.json          # Structured context data
│   └── PROJECT-CONTEXT.md            # Human-readable context
│
├── docker-compose.yml                # Service Orchestration
├── pnpm-workspace.yaml               # Monorepo workspace config
├── nx.json                           # Nx task configuration
├── package.json                      # Root package.json
├── .env.example                      # Environment variables template
├── README.md                         # Project README
└── CONTINUATION-GUIDE.md             # How to continue development
```

---

## 🗄️ Database Schema

### Collections Table (Access Codes)
```javascript
{
  _id: ObjectId,                          // Primary key
  code: String,                           // 6-char alphanumeric (UNIQUE, case-insensitive)
  name: String,                           // Display name
  description: String,                    // Description
  status: "active" | "archived" | "closed", // Collection status
  settings: {
    allow_upload: Boolean,                // Upload enabled flag
    max_file_size: Number,                // Max file size in bytes
    allowed_extensions: [String]          // ["jpg", "png", "gif", "webp"]
  },
  statistics: {
    total_photos: Number,                 // Photo count
    total_size_bytes: Number,             // Total storage used
    last_upload_at: Date                  // Last upload timestamp
  },
  created_at: Date,                       // Creation timestamp
  created_by: String                      // Admin username
}

// Indexes: code (unique), status, created_at
```

### Photos Table (Photo Metadata)
```javascript
{
  _id: ObjectId,                          // Primary key
  collection_code: String,                // Foreign key to collections
  filename: String,                       // Original filename
  file_path: String,                      // Path to original file
  thumbnail_path: String,                 // Path to thumbnail
  file_size: Number,                      // File size in bytes
  mime_type: String,                      // MIME type (image/jpeg, etc.)
  dimensions: {
    width: Number,                        // Image width
    height: Number                        // Image height
  },
  uploaded_at: Date,                      // Upload timestamp
  uploader_info: {
    ip_address: String,                   // Uploader IP
    user_agent: String                    // Browser user agent
  },
  metadata: {
    exif_data: Object,                    // Full EXIF data
    camera_make: String,                  // Camera manufacturer
    camera_model: String                  // Camera model
  },
  processing_status: "pending" | "processed" | "failed", // Processing state
  is_deleted: Boolean                     // Soft delete flag
}

// Indexes: collection_code, uploaded_at, is_deleted
```

### Users Table (Admin Users)
```javascript
{
  _id: ObjectId,                          // Primary key
  username: String,                       // Unique username
  password_hash: String,                  // bcrypt hash (cost factor 12)
  role: String,                           // "admin"
  created_at: Date,                       // Account creation timestamp
  last_login_at: Date                     // Last login timestamp
}

// Indexes: username (unique)
```

---

## 🔌 API Endpoints

### Public Endpoints (No Authentication)

#### 1. Root Endpoint
```http
GET /
```
**Response**:
```json
{
  "message": "Welcome to Photo Collection Management System API",
  "version": "1.0.0",
  "environment": "development"
}
```

#### 2. Health Check
```http
GET /health
```
**Response**:
```json
{
  "status": "healthy"
}
```

#### 3. Validate Access Code
```http
POST /api/v1/collections/validate
Content-Type: application/json

{
  "code": "ABC123"
}
```
**Response**:
```json
{
  "valid": true,
  "collection": {
    "code": "ABC123",
    "name": "Summer Event 2026",
    "description": "Upload your summer photos here",
    "settings": {
      "allow_upload": true,
      "max_file_size": 10485760,
      "allowed_extensions": ["jpg", "jpeg", "png", "gif", "webp"]
    }
  }
}
```

#### 4. Upload Photos
```http
POST /api/v1/collections/{code}/photos
Content-Type: multipart/form-data

files: [File, File, ...]
```
**Response**:
```json
{
  "uploaded": [
    {
      "id": "60d5ec49f1b2c72b8c8e4f1a",
      "filename": "IMG_1234.jpg",
      "status": "success",
      "file_size": 2048576,
      "thumbnail_url": "/thumbnails/ABC123/2026/01/uuid_thumb.jpg"
    }
  ],
  "failed": []
}
```

---

### Authenticated Endpoints (JWT Required)

#### 5. Admin Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "securepassword"
}
```
**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

#### 6. Create Collection
```http
POST /api/v1/admin/collections
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Wedding Photos",
  "description": "Upload your wedding photos",
  "settings": {
    "allow_upload": true,
    "max_file_size": 10485760,
    "allowed_extensions": ["jpg", "jpeg", "png"]
  }
}
```
**Response**:
```json
{
  "id": "60d5ec49f1b2c72b8c8e4f1b",
  "code": "WED789",
  "name": "Wedding Photos",
  "created_at": "2026-01-14T22:00:00Z"
}
```

#### 7. List Collections (Paginated)
```http
GET /api/v1/admin/collections?page=1&limit=20
Authorization: Bearer {token}
```
**Response**:
```json
{
  "items": [
    {
      "id": "60d5ec49f1b2c72b8c8e4f1b",
      "code": "WED789",
      "name": "Wedding Photos",
      "statistics": {
        "total_photos": 156,
        "total_size_bytes": 320000000
      }
    }
  ],
  "total": 128,
  "page": 1,
  "limit": 20
}
```

#### 8. Get Collection Details
```http
GET /api/v1/admin/collections/{code}
Authorization: Bearer {token}
```

#### 9. Update Collection
```http
PATCH /api/v1/admin/collections/{code}
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Updated Name",
  "status": "archived"
}
```

#### 10. Delete Collection
```http
DELETE /api/v1/admin/collections/{code}
Authorization: Bearer {token}
```

#### 11. List Photos in Collection
```http
GET /api/v1/admin/collections/{code}/photos?page=1&limit=50
Authorization: Bearer {token}
```

#### 12. Download Single Photo
```http
GET /api/v1/admin/photos/{photo_id}/download
Authorization: Bearer {token}
```
**Response**: File stream

#### 13. Batch Download Photos (ZIP)
```http
POST /api/v1/admin/collections/{code}/photos/download
Authorization: Bearer {token}
Content-Type: application/json

{
  "photo_ids": ["id1", "id2", "id3"]
}
```
**Response**: ZIP file stream

#### 14. Download All Photos (ZIP)
```http
POST /api/v1/admin/collections/{code}/photos/download-all
Authorization: Bearer {token}
```
**Response**: ZIP file stream

#### 15. Delete Single Photo
```http
DELETE /api/v1/admin/photos/{photo_id}
Authorization: Bearer {token}
```

#### 16. Delete All Photos in Collection
```http
DELETE /api/v1/admin/collections/{code}/photos
Authorization: Bearer {token}
```
**Response**:
```json
{
  "success": true,
  "deleted_count": 156
}
```

#### 17. Get System Statistics
```http
GET /api/v1/admin/statistics
Authorization: Bearer {token}
```
**Response**:
```json
{
  "total_collections": 128,
  "total_photos": 5420,
  "total_storage_bytes": 2147483648,
  "active_collections": 98,
  "recent_uploads": [...]
}
```

---

## 🎨 UI/UX Design Specifications

### Design Philosophy
- **Style**: Modern Dashboard/Admin Panel
- **Color Scheme**: Professional blue-based palette
- **Framework**: Tailwind CSS (utility-first)
- **Icons**: Heroicons or Lucide (no emojis)
- **Design Tool**: ui-ux-pro-max skill for guidance

### Key Components

#### 1. StatCard (Statistics Card)
```vue
<StatCard
  title="Total Collections"
  value="128"
  icon="collection"
  trend="+12%"
  trendUp
/>
```
**Styling**:
- White background
- 8px border radius
- Subtle shadow (shadow-sm)
- Hover effect: enhanced shadow (shadow-md)
- Icon with gradient background
- Trend indicator with color coding (green/red)

#### 2. PhotoGrid (Responsive Photo Grid)
**Layout**:
```css
grid-cols-2 md:grid-cols-4 lg:grid-cols-6
gap-4
```
**Features**:
- 1:1 aspect ratio thumbnails
- Top-left checkbox overlay
- Hover mask with filename and size
- Top-right quick download button
- Smooth hover transitions

#### 3. PhotoToolbar (Batch Operations)
**Position**: Sticky top
**Styling**: Glassmorphism (translucent white blur)
**Actions**:
- Select All / Deselect All
- Selected count display
- Batch Download button
- Download All button
- Delete Selected button (with confirmation)
- Delete All button (with double confirmation)

#### 4. Lightbox (Full-Screen Viewer)
**Features**:
- Full-screen black background (rgba(0,0,0,0.9))
- Centered image with max viewport utilization
- Top toolbar: filename + close button
- Bottom toolbar: download + delete buttons
- Left/right navigation arrows
- Keyboard support: ESC (close), ← (previous), → (next)

### Responsive Breakpoints
- **Mobile**: < 768px (grid-cols-2)
- **Tablet**: 768px - 1024px (grid-cols-4)
- **Desktop**: > 1024px (grid-cols-6)

### Design Checklist
- [ ] Use ui-ux-pro-max skill for design guidance
- [ ] Unified color palette (Tailwind config)
- [ ] All interactive elements have hover/active states
- [ ] Use SVG icons (Heroicons/Lucide)
- [ ] All clickable elements have `cursor-pointer`
- [ ] Responsive layout (mobile/tablet/desktop)
- [ ] Lightbox keyboard navigation
- [ ] Dangerous operations require confirmation
- [ ] Loading states (skeleton screens)
- [ ] Empty states with helpful guidance

---

## 📈 Implementation Phases

### Overview
| Phase | Name | Priority | Status | Completion |
|-------|------|----------|--------|------------|
| 1 | Infrastructure Setup | Critical | ✅ Complete | 100% |
| 2 | Authentication System | High | ⏳ Pending | 0% |
| 3 | Access Code Management | Critical | ⏳ Pending | 0% |
| 4 | Photo Upload System | Critical | ⏳ Pending | 0% |
| 5 | Admin Dashboard UI ⭐ | Critical | ⏳ Pending | 0% |
| 6 | Statistics & Data Display | Medium | ⏳ Pending | 0% |
| 7 | Search, Filter, Optimization | Medium | ⏳ Pending | 0% |
| 8 | Testing & Documentation | High | ⏳ Pending | 0% |
| 9 | Production Deployment | Critical | ⏳ Pending | 0% |

**Overall Progress**: 11% (1 of 9 phases complete)

---

### Phase 1: Infrastructure Setup ✅ COMPLETE

**Deliverables**:
- ✅ Nx task orchestration configuration
- ✅ pnpm workspace management
- ✅ Shared packages structure (ui, configs, schema)
- ✅ FastAPI application framework
- ✅ Beanie ODM integration
- ✅ MongoDB connection management
- ✅ Health check endpoint
- ✅ CORS middleware
- ✅ Vue 3 dual applications (web + admin)
- ✅ Element Plus component library
- ✅ Vue Router + Pinia
- ✅ Tailwind CSS styling
- ✅ Docker Compose with 6 services
- ✅ Development environment hot reload
- ✅ Nginx reverse proxy configuration
- ✅ OpenAPI schema generation
- ✅ TypeScript type generation

**Verification**:
- ✅ `docker-compose up -d` starts all services
- ✅ API health check `/health` returns 200
- ✅ Frontend accessible at localhost:5173 and localhost:5174
- ✅ MongoDB connection successful

---

### Phase 2: Authentication System (NEXT)

**Key Features**:
- JWT authentication
- bcrypt password hashing (cost factor 12)
- Admin login endpoint
- Authentication middleware
- Token management (24h expiry)
- Frontend login page
- Auth store (Pinia)
- Route guards

**Components to Create**:
| Component | File Path | Purpose |
|-----------|-----------|---------|
| User Model | apps/server/app/models/user.py | Admin user data model |
| Security Utils | apps/server/app/core/security.py | JWT generation/verification, password hashing |
| Auth Endpoints | apps/server/app/api/v1/auth.py | POST /auth/login |
| Auth Middleware | apps/server/app/api/deps.py | Protect admin routes |
| Auth Store | apps/web/src/stores/auth.ts | Frontend auth state |
| Login Page | apps/web/src/pages/AdminLogin.vue | Admin login UI |

**API Endpoint**:
```http
POST /api/v1/auth/login
Request: { username, password }
Response: { access_token, token_type, expires_in }
```

**Security Measures**:
- bcrypt password hashing
- JWT with expiration
- Rate limiting (optional)
- Token stored in localStorage
- Route guards for admin pages

---

### Phase 3: Access Code Management

**Key Features**:
- 6-character alphanumeric code generation
- Random generation with uniqueness check
- Code validation endpoint
- Admin CRUD operations
- Code status management (active/archived/closed)

**Code Format**:
- Length: 6 characters
- Characters: A-Z, 0-9 (case-insensitive)
- Combination space: 36^6 ≈ 2.2 billion

**Components to Create**:
| Component | File Path | Purpose |
|-----------|-----------|---------|
| Collection Model | apps/server/app/models/collection.py | Access code data model |
| Code Generator | apps/server/app/utils/code_generator.py | Generate unique 6-char codes |
| Collection Service | apps/server/app/services/collection_service.py | Business logic |
| Collection Endpoints | apps/server/app/api/v1/collections.py | Validation endpoint |
| Admin Endpoints | apps/server/app/api/v1/admin.py | CRUD operations |
| Access Code Page | apps/web/src/pages/AccessCodePage.vue | User input UI |
| Collection Form | apps/web/src/components/admin/CollectionForm.vue | Create/edit UI |

---

### Phase 4: Photo Upload System

**Key Features**:
- Multipart/form-data upload
- Local file storage with structured paths
- Thumbnail generation (400x400)
- File validation (magic numbers + MIME)
- EXIF metadata extraction
- Drag-and-drop UI
- Upload progress tracking

**Storage Structure**:
```
storage/uploads/{collection_code}/{year}/{month}/{uuid}_{filename}
storage/thumbnails/{collection_code}/{year}/{month}/{uuid}_thumb.jpg
```

**Supported Formats**: JPG, JPEG, PNG, GIF, WebP

**Components to Create**:
| Component | File Path | Purpose |
|-----------|-----------|---------|
| Photo Model | apps/server/app/models/photo.py | Photo metadata model |
| Storage Service | apps/server/app/services/storage_service.py | File storage abstraction |
| Image Service | apps/server/app/services/image_service.py | Pillow thumbnail generation |
| Photo Service | apps/server/app/services/photo_service.py | Photo business logic |
| Upload Endpoint | apps/server/app/api/v1/photos.py | multipart/form-data handler |
| FileDropZone | apps/web/src/components/upload/FileDropZone.vue | Drag-drop area |
| UploadProgress | apps/web/src/components/upload/UploadProgress.vue | Progress bar |
| Upload Page | apps/web/src/pages/UploadPage.vue | User upload UI |

---

### Phase 5: Admin Dashboard UI Design ⭐ CRITICAL

**Focus**: Create a beautiful, professional admin dashboard

**Key Features**:
- Modern dashboard with statistics cards
- Responsive photo grid (2/4/6 columns)
- Photo selection with checkboxes
- Batch operations (download/delete)
- Lightbox with keyboard navigation
- Glassmorphism sticky toolbar
- Professional color scheme
- SVG icons (Heroicons/Lucide)

**Components to Create**:
| Component | File Path | Purpose |
|-----------|-----------|---------|
| Admin Dashboard | apps/web/src/pages/AdminDashboard.vue | Stats + collection list |
| Collection Detail | apps/web/src/pages/AdminCollectionDetail.vue | Photo management |
| PhotoGrid | apps/web/src/components/admin/PhotoGrid.vue | Responsive grid |
| PhotoCard | apps/web/src/components/admin/PhotoCard.vue | Single photo card |
| Lightbox | apps/web/src/components/admin/Lightbox.vue | Full-screen viewer |
| PhotoToolbar | apps/web/src/components/admin/PhotoToolbar.vue | Batch operations |
| StatCard | apps/web/src/components/admin/StatCard.vue | Statistics display |
| CollectionCard | apps/web/src/components/admin/CollectionCard.vue | Collection card |

**Design Tool**: Use `ui-ux-pro-max` skill for guidance

**UI Search Commands**:
```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "dashboard admin panel" --domain product
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "minimal clean professional modern" --domain style
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "dashboard admin" --domain color
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "professional modern clean" --domain typography
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "layout responsive component" --stack vue
```

---

### Phase 6: Statistics & Data Display

**Key Features**:
- Total collections count
- Total photos count
- Total storage usage
- Recent uploads list
- Collection activity statistics

**API Endpoint**:
```http
GET /api/v1/admin/statistics
```

---

### Phase 7: Search, Filter, and Optimization

**Key Features**:
- Filename search
- Date range filtering
- Database indexing optimization
- Image lazy loading
- Virtual scrolling for large lists

**Performance Targets**:
- First screen load < 2s
- Lazy loading saves 60% initial bandwidth
- Virtual scrolling supports 1000+ photos smoothly

---

### Phase 8: Testing & Documentation

**Testing Coverage Targets**:
- Backend unit tests > 80%
- Frontend component tests > 70%
- E2E tests for critical user flows

**Documentation**:
- [ ] API documentation (FastAPI auto-generated)
- [ ] User manual (upload flow)
- [ ] Admin manual (backend operations)
- [ ] Deployment guide (Docker)
- [ ] README.md (quick start)

---

### Phase 9: Production Deployment

**Key Features**:
- Multi-stage Docker builds
- Nginx HTTPS with Let's Encrypt
- MongoDB backup scripts
- Centralized logging
- Environment variable templates
- Monitoring and alerting

**Environment Variables**:
```bash
ENVIRONMENT=production
MONGODB_URL=mongodb://...
JWT_SECRET=random-secret-key
S3_BUCKET=photo-bucket  # Optional
```

---

## 🔑 Key Architectural Decisions

### 1. MongoDB over PostgreSQL
**Decision**: Use MongoDB 7.0 instead of PostgreSQL

**Rationale**:
- Document-oriented data model suits flexible photo metadata (EXIF data structure varies)
- Horizontal scalability for future growth
- Schema-less design enables rapid iteration
- Native support for nested documents (settings, metadata)

**Trade-offs**:
- Less ACID guarantees compared to PostgreSQL
- No complex joins (mitigated by denormalization)
- More memory usage for large datasets

**Impact Score**: 9/10

---

### 2. Local File Storage with S3 Abstraction Layer
**Decision**: Start with local file system, abstract for future S3 migration

**Rationale**:
- Lower initial cost for small deployments
- Simplified development setup (no AWS account needed)
- Easy to test and debug locally
- Storage service abstraction layer enables seamless future migration

**Trade-offs**:
- Limited scalability initially
- Manual backup required
- Single point of failure without distributed storage

**Impact Score**: 7/10

---

### 3. Access Code Model (No User Registration)
**Decision**: No user registration; access codes act as permission tokens

**Rationale**:
- Simplified user flow (no sign-up friction)
- Access codes provide natural permission boundaries
- Admin-created codes prevent abuse
- Reduces system complexity (no user management, email verification, etc.)

**Trade-offs**:
- No user tracking or personalization
- Limited audit trail (only IP addresses)
- Potential for access code sharing

**Impact Score**: 8/10

---

### 4. Nx + pnpm Monorepo
**Decision**: Use Nx for task orchestration with pnpm workspaces

**Rationale**:
- Unified codebase for frontend and backend type sharing
- Task caching speeds up builds (incremental builds)
- Shared packages reduce code duplication
- Consistent tooling and CI/CD pipeline

**Trade-offs**:
- Initial complexity for developers new to monorepos
- Learning curve for Nx CLI
- Larger repository size

**Impact Score**: 9/10

---

### 5. Admin Dashboard UI Priority
**Decision**: Focus on admin dashboard beauty over user-facing frontend

**Rationale**:
- Admin is primary user (frequent usage)
- Complex features need excellent UX (photo management, batch operations)
- Professional admin UI increases perceived quality
- User frontend is intentionally simple (just upload)

**Trade-offs**:
- Less polished user-facing frontend initially
- More development time on admin features

**Impact Score**: 7/10

---

## 🚀 Development Workflow

### Initial Setup
```bash
# 1. Clone repository
git clone https://github.com/ZipperCode/photo-monorepo.git
cd photo-monorepo

# 2. Install dependencies
pnpm install

# 3. Set up backend
cd apps/server
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -e .

# 4. Configure environment
cp .env.example .env
# Edit .env: MONGO_PASSWORD, JWT_SECRET
```

### Development Commands
```bash
# Run all dev servers (Nx orchestration)
pnpm dev

# Build all applications
pnpm build

# Type sync (OpenAPI → TypeScript)
pnpm type-sync

# Lint all code
pnpm lint

# Test all applications
pnpm test
```

### Individual Service Development
```bash
# Web frontend
cd apps/web
pnpm dev  # Port 5173

# Admin frontend
cd apps/admin
pnpm dev  # Port 5174

# Backend
cd apps/server
uvicorn app.main:app --reload  # Port 8000
```

### Docker Commands
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View service status
docker-compose ps

# View logs
docker-compose logs -f server
docker-compose logs -f web

# Restart specific service
docker-compose restart server
```

### Git Workflow
```bash
# Check status
git status

# Add changes
git add .

# Commit with conventional commits
git commit -m "feat: add photo upload functionality"

# Push to remote
git push origin main
```

**Branch Strategy**:
- `main` - Main branch (stable)
- `develop` - Development branch
- `feature/*` - Feature branches

---

## 🔐 Security Measures

### Authentication & Authorization
- **Password Hashing**: bcrypt with cost factor 12
- **JWT Tokens**: 24-hour expiration, signed with secret key
- **Token Storage**: localStorage (frontend)
- **Authentication Middleware**: Protects all admin routes
- **Route Guards**: Vue Router guards for admin pages

### File Upload Security
- **File Validation**: Magic number checking + MIME type verification
- **Size Limits**: Configurable per collection
- **Extension Whitelist**: Only allowed image formats
- **Path Traversal Prevention**: UUID-based filenames
- **Virus Scanning**: (Future consideration)

### API Security
- **CORS Configuration**: Specific allowed origins
- **Rate Limiting**: Login endpoint (planned)
- **Input Validation**: Pydantic schemas for all endpoints
- **SQL/NoSQL Injection**: Beanie ODM prevents injection attacks
- **XSS Protection**: Vue 3 auto-escapes templates

### Infrastructure Security
- **Environment Variables**: Sensitive data not in code
- **Docker Networks**: Isolated network for services
- **Nginx Reverse Proxy**: Hides backend infrastructure
- **HTTPS**: Let's Encrypt SSL (production)
- **Database Authentication**: MongoDB requires authentication

### Data Protection
- **Soft Deletes**: `is_deleted` flag instead of hard deletes
- **Backup Strategy**: Regular MongoDB backups (production)
- **Access Logs**: IP address and user agent tracking
- **Storage Separation**: Uploads and thumbnails in separate directories

---

## 📊 Performance Optimization

### Frontend Optimization
- **Lazy Loading**: Images loaded as they enter viewport
- **Virtual Scrolling**: For large photo lists (1000+ items)
- **Code Splitting**: Route-based code splitting with Vue Router
- **Asset Optimization**: Vite's production build optimizations
- **Thumbnail Strategy**: 400x400 thumbnails reduce initial bandwidth by ~60%

### Backend Optimization
- **Async/Await**: FastAPI's async capabilities for I/O operations
- **Database Indexing**:
  - `collection_code` (photos)
  - `uploaded_at` (photos)
  - `is_deleted` (photos)
  - `code` unique (collections)
  - `status` (collections)
- **Connection Pooling**: MongoDB Motor driver connection pooling
- **Response Pagination**: Limit 20-50 items per page

### Build Optimization
- **Nx Task Caching**: Incremental builds, only rebuild changed packages
- **pnpm**: Faster than npm/yarn, disk space efficient
- **Docker Layer Caching**: Multi-stage builds for smaller images

### Performance Targets
| Metric | Target | Current |
|--------|--------|---------|
| First Screen Load | < 2s | TBD |
| API Response Time | < 200ms | TBD |
| Thumbnail Generation | < 500ms | TBD |
| Batch Upload (10 photos) | < 5s | TBD |
| Database Query | < 100ms | TBD |

---

## 🔍 Monitoring & Observability

### Health Checks
- **API Health**: `GET /health`
- **Database Health**: MongoDB connection status
- **Storage Health**: Disk space monitoring

### Logging Strategy
```python
# Backend logging levels
logging.basicConfig(
    level=logging.INFO if settings.environment == "development" else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Metrics (Future)
- Total uploads per day
- Storage growth rate
- API endpoint response times
- Error rates
- Active collections

### Alerts (Future)
- Disk space < 10%
- API error rate > 5%
- Database connection failures
- Failed photo uploads

---

## 📚 Documentation Resources

### Internal Documentation
| Document | Location | Purpose |
|----------|----------|---------|
| Project README | `README.md` | Quick start guide |
| Continuation Guide | `CONTINUATION-GUIDE.md` | How to resume development |
| All Phases Summary | `.spec-workflow/specs/ALL-PHASES-DESIGN-SUMMARY.md` | Design decisions |
| Implementation Checklist | `.spec-workflow/specs/IMPLEMENTATION-CHECKLIST.md` | Task list |
| Phase 1 Requirements | `.spec-workflow/specs/phase-1-infrastructure/requirements.md` | Phase 1 requirements |
| Phase 1 Design | `.spec-workflow/specs/phase-1-infrastructure/design.md` | Phase 1 architecture |
| Project Context (JSON) | `.context/project-context.json` | Structured context data |
| Project Context (MD) | `.context/PROJECT-CONTEXT.md` | This document |

### External Documentation
- **FastAPI**: https://fastapi.tiangolo.com/
- **Vue 3**: https://vuejs.org/guide/introduction.html
- **Beanie ODM**: https://beanie-odm.dev/
- **MongoDB**: https://www.mongodb.com/docs/
- **Nx**: https://nx.dev/getting-started/intro
- **pnpm**: https://pnpm.io/
- **Element Plus**: https://element-plus.org/
- **Tailwind CSS**: https://tailwindcss.com/docs

---

## 🎯 Next Steps

### Immediate Actions (Phase 2)
1. Create User model with bcrypt password hashing
2. Implement JWT token generation and verification
3. Build login endpoint (`POST /api/v1/auth/login`)
4. Create authentication middleware for admin routes
5. Build admin login page (Vue 3)
6. Implement auth store (Pinia)
7. Add route guards to protect admin pages

### Short-Term Goals (Phase 3-4)
1. Implement access code generation (6-character alphanumeric)
2. Build access code validation endpoint
3. Create admin CRUD operations for collections
4. Implement photo upload endpoint with multipart/form-data
5. Build file storage service with local file system
6. Create thumbnail generation service (Pillow)
7. Extract EXIF metadata from photos
8. Build user upload page with drag-and-drop

### Mid-Term Goals (Phase 5-6)
1. Design and implement beautiful admin dashboard
2. Create responsive photo grid component
3. Build lightbox component with keyboard navigation
4. Implement batch operations (download/delete)
5. Add statistics cards to dashboard
6. Create collection activity tracking

### Long-Term Goals (Phase 7-9)
1. Add search and filtering capabilities
2. Optimize database with proper indexing
3. Implement image lazy loading and virtual scrolling
4. Write comprehensive tests (unit, integration, E2E)
5. Create complete documentation
6. Prepare production deployment with HTTPS
7. Set up monitoring and alerting

---

## 🤝 Collaboration & Knowledge Sharing

### Context Sharing
This document serves as the **comprehensive source of truth** for the project. Use it to:
- Onboard new developers
- Resume work after breaks
- Share project architecture with stakeholders
- Generate AI prompts for development assistance
- Document architectural decisions

### AI-Assisted Development
When working with AI assistants (Claude, GPT, etc.), provide this context:
```
Use the project context at .context/PROJECT-CONTEXT.md for comprehensive
understanding of the photo-monorepo architecture, technology stack, and
implementation phases.
```

### Version Control
- **Context Version**: 1.0
- **Last Updated**: 2026-01-14
- **Update Frequency**: After each major phase completion
- **Maintainer**: Project lead

---

## 🔗 Related Resources

### Repository
- **GitHub**: https://github.com/ZipperCode/photo-monorepo
- **Issues**: https://github.com/ZipperCode/photo-monorepo/issues
- **Pull Requests**: https://github.com/ZipperCode/photo-monorepo/pulls

### Design Assets
- **UI/UX Skill**: ui-ux-pro-max (for admin dashboard design)
- **Icon Library**: Heroicons (https://heroicons.com/)
- **Color Palette**: Professional blue-based (TBD in Phase 5)
- **Typography**: System fonts + custom pairings (TBD)

### CI/CD (Future)
- **GitHub Actions**: Automated testing and deployment
- **Docker Hub**: Container image registry
- **Production Server**: TBD

---

## 📝 Changelog

### 2026-01-14 - Initial Context Capture
- ✅ Phase 1 Complete: Infrastructure setup
- ✅ Created comprehensive project context documentation
- ✅ Documented all 9 implementation phases
- ✅ Captured architectural decisions and trade-offs
- ✅ Defined complete API endpoint specifications
- ✅ Established UI/UX design guidelines
- ✅ Set up context management system

### Next Update
- After Phase 2 completion: Authentication system

---

## 🎉 Conclusion

This **Photo Collection Management System** is a modern, well-architected full-stack application with a clear roadmap and comprehensive planning. Phase 1 is complete, establishing a solid foundation with:

- Monorepo structure (Nx + pnpm)
- Vue 3 dual frontends (web + admin)
- FastAPI backend with Beanie ODM
- MongoDB 7.0 database
- Docker Compose orchestration
- Schema-first development (OpenAPI → TypeScript)

The next 8 phases will build upon this foundation to create a beautiful, functional photo collection management system with a focus on an exceptional admin dashboard experience.

**Total Progress**: 11% (1 of 9 phases complete)
**Status**: ✅ Ready for Phase 2 (Authentication System)

---

*This context document is part of an intelligent context management system. For structured data, see `.context/project-context.json`.*

**Context Fingerprint**: `photo-monorepo-2026-01-14-initial`
**Generated**: 2026-01-14T22:05:00Z
**Format Version**: 1.0
