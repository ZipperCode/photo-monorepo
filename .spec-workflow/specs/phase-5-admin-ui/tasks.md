# Tasks Document - Phase 5: Complete Admin Management System

## Backend Tasks

### 5.1. User Management API

- [ ] 5.1.1. Create users API module
  - File: `apps/server/app/api/v1/users.py` (new file)
  - Purpose: Provide user management endpoints
  - Leverage: `apps/server/app/models/user.py`, `apps/server/app/api/deps.py`
  - Requirements: 5.3
  - Tasks:
    - Create router with authentication dependency
    - Add GET /api/v1/admin/users endpoint (list with pagination and search)
    - Add POST /api/v1/admin/users endpoint (create user)
    - Add PUT /api/v1/admin/users/:id endpoint (update user)
    - Add DELETE /api/v1/admin/users/:id endpoint (delete user)
    - Add DELETE /api/v1/admin/users endpoint (batch delete)
  - Success: All user CRUD endpoints working with proper authentication

- [ ] 5.1.2. Create user profile endpoints
  - File: `apps/server/app/api/v1/users.py`
  - Purpose: Provide user profile management
  - Requirements: 5.8
  - Tasks:
    - Add GET /api/v1/admin/profile endpoint (get current user)
    - Add PUT /api/v1/admin/profile endpoint (update profile)
    - Add PUT /api/v1/admin/profile/change-password endpoint (change password)
  - Success: Profile management working with validation

---

### 5.2. Photo Management API

- [ ] 5.2.1. Create photos API module
  - File: `apps/server/app/api/v1/photos.py` (new file)
  - Purpose: Provide photo management endpoints
  - Leverage: `apps/server/app/models/photo.py`, `apps/server/app/services/storage_service.py`
  - Requirements: 5.5, 5.6
  - Tasks:
    - Create router with authentication dependency
    - Add GET /api/v1/admin/photos endpoint (list all photos with pagination and filters)
    - Add GET /api/v1/admin/collections/:code/photos endpoint (list collection photos)
    - Add GET /api/v1/admin/photos/:id/download endpoint (download single photo)
    - Add DELETE /api/v1/admin/photos/:id endpoint (delete single photo)
  - Success: Photo listing and single operations working

- [ ] 5.2.2. Implement batch download endpoint
  - File: `apps/server/app/api/v1/photos.py`
  - Purpose: Enable batch photo download as ZIP
  - Requirements: 5.9, 5.13
  - Tasks:
    - Add POST /api/v1/admin/photos/download endpoint
    - Accept photo_ids array in request body
    - Generate ZIP file with selected photos
    - Stream ZIP response to avoid memory issues
    - Handle missing files gracefully
    - Set appropriate Content-Disposition headers
  - Success: Batch download generates correct ZIP with streaming

- [ ] 5.2.3. Implement batch delete endpoint
  - File: `apps/server/app/api/v1/photos.py`
  - Purpose: Enable batch photo deletion
  - Requirements: 5.9
  - Tasks:
    - Add DELETE /api/v1/admin/photos endpoint
    - Accept photo_ids array in request body
    - Perform soft delete on all photos
    - Return success and failure counts
  - Success: Batch delete with partial failure reporting

---

### 5.3. Statistics API

- [ ] 5.3.1. Create statistics endpoint
  - File: `apps/server/app/api/v1/admin.py` (enhance existing)
  - Purpose: Provide dashboard statistics
  - Requirements: 5.2
  - Tasks:
    - Add GET /api/v1/admin/statistics endpoint
    - Calculate today's statistics (collections, photos, storage)
    - Calculate total statistics (collections, photos, storage)
    - Generate upload trend data (last 7, 30, 90 days)
    - Generate storage distribution data (Top 10 collections)
    - Optimize queries with proper indexes
  - Success: Statistics endpoint returns accurate real-time data

---

### 5.4. Collection Management API Enhancement

- [ ] 5.4.1. Add batch delete collections endpoint
  - File: `apps/server/app/api/v1/collections.py` (enhance existing)
  - Purpose: Enable batch collection deletion
  - Requirements: 5.4
  - Tasks:
    - Add DELETE /api/v1/admin/collections endpoint
    - Accept codes array in request body
    - Perform soft delete on all collections
    - Return deleted count
  - Success: Batch delete collections working correctly

- [ ] 5.4.2. Add download collection photos endpoint
  - File: `apps/server/app/api/v1/collections.py`
  - Purpose: Download all photos in a collection as ZIP
  - Requirements: 5.4, 5.13
  - Tasks:
    - Add POST /api/v1/admin/collections/:code/download endpoint
    - Generate ZIP with all photos in collection
    - Stream ZIP response
    - Name file: {CODE}_照片合集_YYYYMMDD.zip
  - Success: Collection photos download generates ZIP

- [ ] 5.4.3. Enhance collections list with date filtering
  - File: `apps/server/app/api/v1/collections.py`
  - Purpose: Support date range filtering
  - Requirements: 5.4
  - Tasks:
    - Update GET /api/v1/admin/collections to accept date_from and date_to query params
    - Filter collections by created_at range
    - Add index on created_at if needed
  - Success: Date filtering working correctly

---

## Frontend Tasks

### 5.5. Layout and Navigation

- [ ] 5.5.1. Create AdminLayout component
  - File: `apps/admin/src/layouts/AdminLayout.vue` (new file)
  - Purpose: Main layout container with sidebar and header
  - Requirements: 5.1
  - Leverage: Element Plus, Tailwind CSS
  - Tasks:
    - Create layout structure (sidebar + header + content)
    - Integrate Sidebar component
    - Integrate Header component with UserDropdown
    - Add responsive behavior (mobile hamburger menu)
    - Add router-view for page content
  - Success: Layout displays correctly with sidebar and header

- [ ] 5.5.2. Create BlankLayout component
  - File: `apps/admin/src/layouts/BlankLayout.vue` (new file)
  - Purpose: Blank layout for login page
  - Requirements: 5.1
  - Tasks:
    - Create simple layout with router-view only
    - No sidebar or header
  - Success: Login page displays without sidebar/header

- [ ] 5.5.3. Create Sidebar component
  - File: `apps/admin/src/components/admin/Sidebar.vue` (new file)
  - Purpose: Left navigation menu
  - Requirements: 5.1
  - Leverage: Element Plus el-menu, Vue Router
  - Tasks:
    - Create menu with items (Dashboard, Users, Collections, Photos, Settings)
    - Add active route highlighting
    - Add logo and system title
    - Implement collapse on mobile
    - Style with dark background (#1e293b)
  - Success: Navigation menu functional and styled

- [ ] 5.5.4. Create Header component
  - File: `apps/admin/src/components/admin/Header.vue` (new file)
  - Purpose: Top header bar
  - Requirements: 5.1
  - Tasks:
    - Add logo and system title
    - Integrate UserDropdown component
    - Style with white background and fixed positioning
  - Success: Header displays user dropdown correctly

- [ ] 5.5.5. Create UserDropdown component
  - File: `apps/admin/src/components/admin/UserDropdown.vue` (new file)
  - Purpose: User dropdown menu with profile and logout
  - Requirements: 5.1
  - Leverage: Element Plus el-dropdown, Auth store
  - Tasks:
    - Display user avatar (first letter of username)
    - Display username
    - Create dropdown menu items (Profile, Change Password, Settings, Logout)
    - Implement logout with confirmation dialog
    - Navigate to profile page
  - Success: User dropdown functional with all menu items

- [ ] 5.5.6. Update router configuration
  - File: `apps/admin/src/router/index.ts` (update existing)
  - Purpose: Configure nested routes with layouts
  - Requirements: 5.1
  - Tasks:
    - Update route structure to use layouts (AdminLayout, BlankLayout)
    - Add nested routes for dashboard, users, collections, photos, settings
    - Update route guards for authentication
    - Add meta fields for titles and icons
  - Success: Navigation works correctly with new layout

---

### 5.6. Dashboard Components

- [ ] 5.6.1. Create StatCard component
  - File: `apps/admin/src/components/admin/StatCard.vue` (new file)
  - Purpose: Statistics display card
  - Requirements: 5.2
  - Leverage: Tailwind CSS
  - Tasks:
    - Create card with icon, title, value display
    - Add optional trend indicator (percentage up/down)
    - Add hover effect (slight lift with shadow)
    - Add click handler for navigation
    - Style with white background and rounded corners
  - Success: StatCard is reusable and visually appealing

- [ ] 5.6.2. Create UploadTrendChart component
  - File: `apps/admin/src/components/admin/UploadTrendChart.vue` (new file)
  - Purpose: Line chart showing upload trend
  - Requirements: 5.2
  - Leverage: ECharts 5.4+, vue-echarts 6.5+
  - Tasks:
    - Create line chart with ECharts
    - Add time range toggle (7/30/90 days)
    - Configure X-axis (date) and Y-axis (count)
    - Add hover tooltip with values
    - Add smooth animations
    - Emit chart-click event
  - Success: Chart displays upload trend correctly

- [ ] 5.6.3. Create StorageChart component
  - File: `apps/admin/src/components/admin/StorageChart.vue` (new file)
  - Purpose: Pie chart showing storage distribution
  - Requirements: 5.2
  - Leverage: ECharts 5.4+, vue-echarts 6.5+
  - Tasks:
    - Create pie chart with ECharts
    - Display Top 10 collections, group others as "Other"
    - Add percentage labels
    - Add legend on right side
    - Handle click on slice to navigate to collection
  - Success: Chart displays storage distribution correctly

- [ ] 5.6.4. Update Dashboard page
  - File: `apps/admin/src/pages/Dashboard.vue` (update existing)
  - Purpose: Main dashboard with statistics and charts
  - Requirements: 5.2
  - Leverage: StatCard, UploadTrendChart, StorageChart components
  - Tasks:
    - Integrate 4 StatCard components (today's collections, photos, storage, system overview)
    - Integrate UploadTrendChart component
    - Integrate StorageChart component
    - Fetch statistics from API
    - Handle loading states
    - Handle empty states
  - Success: Dashboard displays statistics and charts correctly

---

### 5.7. Data Table Components

- [ ] 5.7.1. Create DataTable component
  - File: `apps/admin/src/components/admin/DataTable.vue` (new file)
  - Purpose: Reusable data table with advanced features
  - Requirements: 5.11
  - Leverage: Element Plus el-table
  - Tasks:
    - Create table with column configuration
    - Add column visibility toggle (dialog with checkboxes)
    - Add sorting by column
    - Add pagination (20/50/100 per page)
    - Add multi-select with checkboxes
    - Add fixed action column
    - Add loading skeleton
    - Add empty state
    - Save column preferences to localStorage
  - Success: DataTable is reusable with all features working

---

### 5.8. Search Components

- [ ] 5.8.1. Create SearchBar component
  - File: `apps/admin/src/components/admin/SearchBar.vue` (new file)
  - Purpose: Search conditions input bar
  - Requirements: 5.12
  - Leverage: Element Plus (el-input, el-date-picker, el-button)
  - Tasks:
    - Add text search input with debounce (500ms)
    - Add date range picker
    - Add quick filter buttons (Today, 7 days, 30 days)
    - Add Search and Reset buttons
    - Implement collapsible on mobile
    - Emit search and reset events
  - Success: SearchBar functional with all input types

---

### 5.9. Photo Components

- [ ] 5.9.1. Create PhotoLightbox component
  - File: `apps/admin/src/components/admin/PhotoLightbox.vue` (new file)
  - Purpose: Full-screen photo preview dialog
  - Requirements: 5.7
  - Leverage: Tailwind CSS, Element Plus el-dialog
  - Tasks:
    - Create full-screen overlay (z-index: 9999)
    - Set black background (rgba(0,0,0,0.95))
    - Display image centered (max 90vw x 90vh)
    - Add bottom action bar (Download, Delete buttons)
    - Add ESC key handler to close
    - Add loading skeleton
    - Add error state for failed loads
    - Prevent body scroll when open
  - Success: Lightbox displays photos correctly with keyboard support

---

### 5.10. Form Components

- [ ] 5.10.1. Create UserForm component
  - File: `apps/admin/src/components/users/UserForm.vue` (new file)
  - Purpose: User create/edit form dialog
  - Requirements: 5.3
  - Leverage: Element Plus el-form, el-dialog
  - Tasks:
    - Create form with fields (Username, Password, Confirm Password, Role)
    - Add validation rules (username unique, password min 8 chars, password match)
    - Support both create and edit modes
    - Add success/error messages
    - Handle form submission
  - Success: UserForm creates and updates users correctly

---

### 5.11. User Management Pages

- [ ] 5.11.1. Create UserList page
  - File: `apps/admin/src/pages/users/UserList.vue` (new file)
  - Purpose: User management list page
  - Requirements: 5.3
  - Leverage: DataTable, SearchBar, UserForm components, users store
  - Tasks:
    - Integrate DataTable with user columns (select, username, role, created_at, last_login, actions)
    - Integrate SearchBar (search by username)
    - Integrate UserForm dialog (create/edit)
    - Implement batch delete functionality
    - Handle pagination
    - Handle create/edit/delete operations
    - Add "New User" button
  - Success: User management page fully functional

- [ ] 5.11.2. Create Profile page
  - File: `apps/admin/src/pages/users/Profile.vue` (new file)
  - Purpose: User profile center
  - Requirements: 5.8
  - Tasks:
    - Display current user information
    - Add edit username form
    - Add change password form (current password, new password, confirm)
    - Add validation
    - Add Save/Cancel buttons
    - Handle form submission
  - Success: Profile page updates user info and password correctly

- [ ] 5.11.3. Create users store
  - File: `apps/admin/src/stores/users.ts` (new file)
  - Purpose: Centralized user state management
  - Requirements: 5.3
  - Leverage: Pinia
  - Tasks:
    - Define state (users, loading, pagination)
    - Implement fetchUsers action
    - Implement createUser action
    - Implement updateUser action
    - Implement deleteUser action
    - Implement batchDelete action
  - Success: Users store manages all user operations

---

### 5.12. Collection Management Pages

- [ ] 5.12.1. Update CollectionList page
  - File: `apps/admin/src/pages/collections/CollectionList.vue` (enhance existing)
  - Purpose: Collection management with advanced features
  - Requirements: 5.4
  - Leverage: DataTable, SearchBar, CollectionForm components, collections store
  - Tasks:
    - Replace existing list with DataTable component
    - Add columns (select, index, code, name, status, created_at, photo_count, updated_at, actions)
    - Integrate SearchBar (search by code, date range)
    - Integrate CollectionForm dialog (enhance existing)
    - Implement batch delete functionality
    - Add click handler on collection code to copy to clipboard
    - Implement download ZIP functionality
    - Handle pagination
  - Success: Collection management page fully functional with all features

- [ ] 5.12.2. Create CollectionPhotos page
  - File: `apps/admin/src/pages/collections/CollectionPhotos.vue` (new file)
  - Purpose: Collection photo detail page
  - Requirements: 5.6
  - Route: /collections/:code/photos
  - Leverage: DataTable, SearchBar, PhotoLightbox components, photos store
  - Tasks:
    - Add collection info header (code, name, stats)
    - Add "Back to Collections" button
    - Integrate DataTable with photo columns
    - Integrate SearchBar (filter within collection)
    - Integrate PhotoLightbox component
    - Implement batch operations (download/delete)
    - Handle empty state with copy code button
  - Success: Collection photos page displays and manages photos correctly

---

### 5.13. Photo Management Pages

- [ ] 5.13.1. Create PhotoList page
  - File: `apps/admin/src/pages/photos/PhotoList.vue` (new file)
  - Purpose: All photos list page
  - Requirements: 5.5
  - Leverage: DataTable, SearchBar, PhotoLightbox components, photos store
  - Tasks:
    - Integrate DataTable with photo columns (select, index, preview, collection, filename, size, format, uploaded_at, updated_at, actions)
    - Integrate SearchBar (filter by collection, date range)
    - Integrate PhotoLightbox component
    - Implement thumbnail click to open lightbox
    - Implement batch download functionality
    - Implement batch delete functionality
    - Handle pagination
  - Success: All photos page displays and manages photos correctly

- [ ] 5.13.2. Create photos store
  - File: `apps/admin/src/stores/photos.ts` (new file)
  - Purpose: Centralized photo state management
  - Requirements: 5.5, 5.6, 5.9
  - Leverage: Pinia
  - Tasks:
    - Define state (photos, selectedIds, loading, pagination)
    - Implement fetchPhotos action with filters
    - Implement toggleSelection action
    - Implement selectAll action
    - Implement deselectAll action
    - Implement batchDownload action
    - Implement batchDelete action
  - Success: Photos store manages all photo operations

---

### 5.14. API Services

- [ ] 5.14.1. Create userService
  - File: `apps/admin/src/services/userService.ts` (new file)
  - Purpose: User API service layer
  - Requirements: 5.3
  - Leverage: Axios
  - Tasks:
    - Implement getUsers (list with pagination and search)
    - Implement createUser
    - Implement updateUser
    - Implement deleteUser
    - Implement batchDeleteUsers
    - Implement getProfile
    - Implement updateProfile
    - Implement changePassword
  - Success: All user API calls working correctly

- [ ] 5.14.2. Create photoService
  - File: `apps/admin/src/services/photoService.ts` (new file)
  - Purpose: Photo API service layer
  - Requirements: 5.5, 5.6
  - Leverage: Axios
  - Tasks:
    - Implement getPhotos (list all with filters)
    - Implement getCollectionPhotos
    - Implement downloadPhoto (single file)
    - Implement deletePhoto
    - Implement batchDownloadPhotos (ZIP)
    - Implement batchDeletePhotos
  - Success: All photo API calls working correctly

- [ ] 5.14.3. Update API service
  - File: `apps/admin/src/services/api.ts` (update existing)
  - Purpose: Enhance API service with new endpoints
  - Requirements: All
  - Tasks:
    - Add statistics endpoint
    - Add authentication headers to all requests
    - Enhance error handling
    - Add retry logic for failed requests
  - Success: API service handles all endpoints correctly

---

### 5.15. Dependencies

- [ ] 5.15.1. Install frontend dependencies
  - File: `apps/admin/package.json`
  - Purpose: Add required packages for Phase 5
  - Tasks:
    - Add echarts: ^5.4.0
    - Add vue-echarts: ^6.5.0
    - Run pnpm install
  - Success: All dependencies installed

---

## Task Dependencies

### Phase 5A - Layout (Week 1)
- 5.5.1 → 5.5.6 (Layout components and router)
- 5.15.1 (Dependencies)

### Phase 5B - Dashboard (Week 1)
- 5.6.1 → 5.6.4 (Dashboard components)
- 5.3.1 (Statistics API)

### Phase 5C - User Management (Week 2)
- 5.1.1 → 5.1.2 (User API)
- 5.7.1 (DataTable)
- 5.8.1 (SearchBar)
- 5.10.1 (UserForm)
- 5.11.1 → 5.11.3 (User pages and store)
- 5.14.1 (userService)

### Phase 5D - Collection Management (Week 2)
- 5.4.1 → 5.4.3 (Collection API enhancements)
- 5.12.1 → 5.12.2 (Collection pages)
- 5.14.3 (API service enhancements)

### Phase 5E - Photo Management (Week 3)
- 5.2.1 → 5.2.3 (Photo API)
- 5.9.1 (PhotoLightbox)
- 5.13.1 → 5.13.2 (Photo pages and store)
- 5.14.2 (photoService)

### Phase 5F - Testing and Optimization (Week 4)
- All previous tasks completed
- End-to-end testing
- Performance optimization
- Bug fixes

---

## Task Count Summary

**Backend Tasks**: 13
- User Management API: 2
- Photo Management API: 3
- Statistics API: 1
- Collection API Enhancement: 3
- Total: 9 files created/enhanced

**Frontend Tasks**: 32
- Layout and Navigation: 6
- Dashboard Components: 4
- Data Table Components: 1
- Search Components: 1
- Photo Components: 1
- Form Components: 1
- User Management Pages: 3
- Collection Management Pages: 2
- Photo Management Pages: 2
- API Services: 3
- Dependencies: 1
- Total: 25 files created/enhanced

**Total Tasks**: 45
- Backend: 13
- Frontend: 32

---

## Estimated Effort

- **Backend Tasks**: 13 tasks × 2 hours = 26 hours
- **Frontend Tasks**: 32 tasks × 3 hours = 96 hours
- **Integration and Testing**: 20 hours
- **Total**: ~142 hours (approximately 4 weeks for 1 developer)

---

## Completion Criteria

All tasks completed when:
- [ ] All backend API endpoints implemented and tested
- [ ] All frontend components created and integrated
- [ ] All pages functional with proper routing
- [ ] All stores managing state correctly
- [ ] All API services working with error handling
- [ ] All features in requirements.md passing acceptance criteria
- [ ] No TypeScript errors in production build
- [ ] Responsive design working on all devices
- [ ] All accessibility features implemented
