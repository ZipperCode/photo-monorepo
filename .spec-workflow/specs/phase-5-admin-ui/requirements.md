# Requirements Document - Phase 5: Complete Admin Management System

## Introduction

Phase 5 creates a comprehensive admin management system with modern, minimalist design (dark sidebar + white content area). This phase implements a complete dashboard with user management, collection management, and photo management features.

## Alignment with Product Vision

This feature supports administrators as the primary users of the system, providing efficient tools for managing users, collections, and photos through a unified, professional interface with focus on usability, visual appeal, and productivity.

## Design Philosophy

**Visual Style**: Modern minimalist with professional color scheme
- **Sidebar**: Dark (#1e293b) with clear navigation hierarchy
- **Content Area**: Light (#f8fafc) with white cards for content
- **Accent Colors**: Blue primary, semantic colors for actions
- **Typography**: Clean, readable with proper hierarchy
- **Spacing**: Consistent padding and margins for visual breathing room

## Requirements

### Requirement 5.1: Admin Layout System

**User Story:** As an administrator, I want a unified admin interface with sidebar navigation and user menu, so that I can navigate between different management sections efficiently.

#### Acceptance Criteria

1. WHEN admin logs in THEN system SHALL display layout with left sidebar navigation and top header
2. WHEN sidebar is displayed THEN system SHALL show menu items: Dashboard, Users, Collections, Photos, Settings
3. WHEN menu item is clicked THEN system SHALL navigate to corresponding page and highlight active item
4. WHEN user avatar is clicked THEN system SHALL show dropdown with Profile, Change Password, Settings, Logout
5. WHEN on mobile device THEN system SHALL collapse sidebar to hamburger menu
6. WHEN logout is clicked THEN system SHALL show confirmation dialog
7. WHEN page content overflows THEN system SHALL enable scrolling in content area only (sidebar and header remain fixed)

### Requirement 5.2: Enhanced Dashboard

**User Story:** As an administrator, I want a dashboard showing key statistics and recent activity, so that I can monitor system activity at a glance.

#### Acceptance Criteria

1. WHEN administrator visits dashboard THEN system SHALL display 4 statistics cards (today's collections, today's photos, today's storage, system overview)
2. WHEN statistics cards are displayed THEN system SHALL show accurate real-time data from database
3. WHEN card is clicked THEN system SHALL navigate to corresponding management page
4. WHEN upload trend chart is displayed THEN system SHALL show line chart with daily upload counts
5. WHEN time range toggle is clicked (7/30/90 days) THEN system SHALL update chart data
6. WHEN storage distribution chart is displayed THEN system SHALL show pie chart with Top 10 collections
7. WHEN chart section is clicked THEN system SHALL navigate to corresponding collection
8. IF no data exists THEN system SHALL show empty state with call-to-action

### Requirement 5.3: User Management Module

**User Story:** As an administrator, I want to manage admin users with complete CRUD operations, so that I can control who has access to the system.

#### Acceptance Criteria

1. WHEN viewing user list THEN system SHALL display paginated table with columns: select, username, role, created_at, last_login, actions
2. WHEN searching by username THEN system SHALL filter results in real-time (debounce 500ms)
3. WHEN column header is clicked THEN system SHALL sort data by that column
4. WHEN column settings button is clicked THEN system SHALL show dialog to toggle column visibility
5. WHEN creating new user THEN system SHALL validate username uniqueness and password (min 8 chars)
6. WHEN editing user THEN system SHALL allow updating username and role
7. WHEN deleting user THEN system SHALL require confirmation with username displayed
8. WHEN multiple users are selected THEN system SHALL enable batch delete button
9. WHEN batch delete is confirmed THEN system SHALL delete all selected users
10. WHEN pagination controls are used THEN system SHALL support page sizes: 20, 50, 100 per page

### Requirement 5.4: Collection Management Module

**User Story:** As an administrator, I want advanced collection management with search, filtering, and bulk operations, so that I can efficiently manage large numbers of collections.

#### Acceptance Criteria

1. WHEN viewing collection list THEN system SHALL display table with columns: select, index, code, name, status, created_at, photo_count, updated_at, actions
2. WHEN searching by collection code THEN system SHALL support fuzzy search
3. WHEN date range filter is applied THEN system SHALL show collections created within selected range
4. WHEN quick filter is clicked (today/7 days/30 days) THEN system SHALL apply date range automatically
5. WHEN collection code is clicked THEN system SHALL copy code to clipboard and show success message
6. WHEN "view photos" button is clicked THEN system SHALL navigate to collection photos page
7. WHEN "download" button is clicked THEN system SHALL generate ZIP file and trigger download with loading indicator
8. WHEN "delete" button is clicked THEN system SHALL show double confirmation dialog with photo count
9. WHEN first confirmation is shown THEN system SHALL display "确定要删除收录码 ABC123 吗？"
10. WHEN second confirmation is shown THEN system SHALL display "此操作将删除该收录码下的 156 张照片，且不可恢复。请再次确认。"
11. WHEN creating new collection THEN system SHALL auto-generate unique 6-character code
12. WHEN multiple collections are selected THEN system SHALL enable batch delete
13. WHEN pagination is used THEN system SHALL maintain selected state across pages

### Requirement 5.5: Photo Management - All Photos Page

**User Story:** As an administrator, I want to view all photos in a data table with search and filters, so that I can find and manage specific photos efficiently.

#### Acceptance Criteria

1. WHEN viewing all photos THEN system SHALL display table with columns: select, index, preview (80x80 thumbnail), collection, filename, size, format, uploaded_at, updated_at, actions
2. WHEN collection filter is selected THEN system SHALL show photos only from that collection
3. WHEN date range filter is applied THEN system SHALL show photos uploaded within selected range
4. WHEN thumbnail is clicked THEN system SHALL open lightbox dialog with original image
5. WHEN lightbox is open THEN system SHALL support ESC key to close
6. WHEN lightbox is open THEN system SHALL show download and delete buttons
7. WHEN "download" button in table is clicked THEN system SHALL download original photo file
8. WHEN "delete" button in table is clicked THEN system SHALL show confirmation dialog
9. WHEN multiple photos are selected THEN system SHALL show selected count in toolbar
10. WHEN "batch download" is clicked THEN system SHALL generate ZIP file with loading indicator
11. WHEN "batch delete" is clicked THEN system SHALL show confirmation with selected count
12. WHEN filename exceeds column width THEN system SHALL truncate with ellipsis
13. WHEN column settings is used THEN system SHALL remember user preferences in localStorage
14. WHEN pagination is used THEN system SHALL show 20/50/100 per page options

### Requirement 5.6: Photo Management - Collection Photos Page

**User Story:** As an administrator, I want to view photos within a specific collection with context, so that I can manage photos for that collection efficiently.

#### Acceptance Criteria

1. WHEN visiting collection photos page THEN system SHALL display collection info header (code, name, stats)
2. WHEN "back to collections" button is clicked THEN system SHALL navigate to collections list
3. WHEN photos are displayed THEN system SHALL use same table structure as all photos page
4. WHEN collection stats are shown THEN system SHALL display: total photos, total storage, last upload time
5. WHEN no photos exist THEN system SHALL show empty state with copy code button
6. WHEN search/filter is used THEN system SHALL apply within current collection only

### Requirement 5.7: Photo Preview Lightbox

**User Story:** As an administrator, I want to preview photos in full-screen lightbox, so that I can examine photos in detail and perform quick actions.

#### Acceptance Criteria

1. WHEN photo thumbnail is clicked THEN system SHALL open full-screen lightbox overlay
2. WHEN lightbox opens THEN system SHALL set background to rgba(0,0,0,0.95)
3. WHEN image is loading THEN system SHALL display skeleton screen
4. WHEN image loads successfully THEN system SHALL center image with max 90vw x 90vh
5. WHEN ESC key is pressed THEN system SHALL close lightbox
6. WHEN download button is clicked THEN system SHALL download original photo
7. WHEN delete button is clicked THEN system SHALL show confirmation then delete
8. WHEN lightbox is open THEN system SHALL prevent body scroll
9. WHEN lightbox closes THEN system SHALL restore body scroll

### Requirement 5.8: User Profile Management

**User Story:** As an administrator, I want to update my profile and change password, so that I can maintain my account security.

#### Acceptance Criteria

1. WHEN visiting profile page THEN system SHALL display current user information
2. WHEN username is updated THEN system SHALL validate uniqueness and save
3. WHEN changing password THEN system SHALL require current password for verification
4. WHEN new password is entered THEN system SHALL validate minimum 8 characters
5. WHEN passwords don't match THEN system SHALL show validation error
6. WHEN profile is saved successfully THEN system SHALL show success message
7. WHEN password is changed successfully THEN system SHALL require re-login

### Requirement 5.9: Batch Operations

**User Story:** As an administrator, I want to perform batch operations on multiple items, so that I can manage large datasets efficiently.

#### Acceptance Criteria

1. WHEN multiple items are selected THEN system SHALL display floating or sticky toolbar
2. WHEN select all is clicked THEN system SHALL select all items on current page
3. WHEN deselect all is clicked THEN system SHALL clear all selections
4. WHEN batch download is clicked THEN system SHALL show "正在打包 X 个文件，请稍候..." loading
5. WHEN batch delete is clicked THEN system SHALL show confirmation: "确定要删除选中的 X 项吗？"
6. WHEN batch operation completes successfully THEN system SHALL show success message with count
7. WHEN batch operation partially fails THEN system SHALL show error details
8. WHEN batch operation is in progress THEN system SHALL disable all action buttons

### Requirement 5.10: Responsive Design

**User Story:** As an administrator, I want the admin interface to work on all devices, so that I can manage the system from desktop, tablet, or mobile.

#### Acceptance Criteria

1. WHEN on desktop (>1024px) THEN system SHALL show full sidebar with 240px width
2. WHEN on tablet (768-1024px) THEN system SHALL show full sidebar with 240px width
3. WHEN on mobile (<768px) THEN system SHALL collapse sidebar to hamburger menu
4. WHEN sidebar is collapsed on mobile THEN system SHALL show overlay when menu is open
5. WHEN table is viewed on mobile THEN system SHALL enable horizontal scroll
6. WHEN chart is viewed on mobile THEN system SHALL adjust height and maintain readability
7. WHEN screen is resized THEN system SHALL adjust layout smoothly without breaking functionality

### Requirement 5.11: Data Table Features

**User Story:** As an administrator, I want advanced table features like sorting, column configuration, and pagination, so that I can customize data presentation.

#### Acceptance Criteria

1. WHEN column header is clicked THEN system SHALL toggle sort order (asc/desc/unsorted)
2. WHEN sort indicator is shown THEN system SHALL display arrow icon
3. WHEN column settings dialog is opened THEN system SHALL show all available columns with checkboxes
4. WHEN column visibility is toggled THEN system SHALL save preference to localStorage
5. WHEN page size is changed THEN system SHALL reload data with new limit
6. WHEN page number is changed THEN system SHALL navigate to requested page
7. WHEN data is loading THEN system SHALL show skeleton screen in table body
8. WHEN table has no data THEN system SHALL show friendly empty state illustration

### Requirement 5.12: Search and Filtering

**User Story:** As an administrator, I want powerful search and filtering capabilities, so that I can quickly find specific data.

#### Acceptance Criteria

1. WHEN search input has text THEN system SHALL apply filter after 500ms debounce
2. WHEN search is cleared THEN system SHALL reset to show all data
3. WHEN date range picker is used THEN system SHALL apply start and end date filters
4. WHEN quick filter button is clicked THEN system SHALL auto-fill date range
5. WHEN multiple filters are active THEN system SHALL apply all filters (AND logic)
6. WHEN filter results in no matches THEN system SHALL show "no results" message
7. WHEN search is in progress THEN system SHALL show loading indicator

### Requirement 5.13: ZIP Download Operations

**User Story:** As an administrator, I want to download multiple photos as ZIP file, so that I can archive or share photos efficiently.

#### Acceptance Criteria

1. WHEN batch download is clicked THEN system SHALL request ZIP generation from API
2. WHEN ZIP generation starts THEN system SHALL show "正在打包，请稍候..." message
3. WHEN ZIP file is ready THEN system SHALL trigger browser download
4. WHEN single collection download is clicked THEN system SHALL name file: "{CODE}_照片合集_YYYYMMDD.zip"
5. WHEN batch photo download is clicked THEN system SHALL name file: "照片批量下载_YYYYMMDD_HHMMSS.zip"
6. WHEN ZIP generation fails THEN system SHALL show error message with retry option
7. WHEN ZIP file is large THEN system SHALL stream download to avoid memory issues

### Requirement 5.14: Error Handling and User Feedback

**User Story:** As an administrator, I want clear error messages and feedback, so that I understand what went wrong and how to fix it.

#### Acceptance Criteria

1. WHEN API request fails THEN system SHALL show error message with description
2. WHEN network error occurs THEN system SHALL show "网络错误，请检查连接"
3. WHEN validation fails THEN system SHALL highlight form field with error message
4. WHEN operation succeeds THEN system SHALL show success toast message
5. WHEN operation is in progress THEN system SHALL show loading indicator
6. WHEN unauthorized access is attempted THEN system SHALL redirect to login
7. WHEN file upload fails THEN system SHALL show specific error (size, format, etc.)

## Non-Functional Requirements

### Code Architecture and Modularity
- **Single Responsibility Principle**: Separate layout, components, pages, and stores
- **Modular Design**: Components should be reusable and composable
- **Dependency Management**: Use Pinia stores for state management, minimize prop drilling
- **Clear Interfaces**: Define clear props and events for all components
- **Layered Architecture**: Separate presentation (components), business logic (stores), and data access (services)

### Performance
- Dashboard statistics should load within 2 seconds
- Tables should support 1000+ rows with pagination
- Images should use lazy loading for better performance
- ZIP generation should stream for large files
- Charts should render smoothly with animations
- Search should debounce to avoid excessive API calls

### Security
- All admin operations require JWT authentication
- Tokens expire after 24 hours
- Passwords hashed with bcrypt (cost factor 12)
- Delete operations require confirmation
- Batch operations validate permissions
- CORS configured for specific origins
- Input sanitization on all forms

### Reliability
- Failed operations should show clear error messages
- Partial batch operation failures should be reported
- Network errors should have retry mechanism
- Data validation on both client and server
- Graceful degradation for unsupported features

### Usability
- Consistent design language across all pages
- All interactive elements should have hover states
- Keyboard shortcuts support (ESC for dialogs)
- Loading states for all async operations
- Empty states guide users to next actions
- Success/error messages are clear and actionable
- Responsive design works on all devices
- Accessibility features (ARIA labels, focus management)

### Maintainability
- TypeScript for type safety
- Clear component naming and file structure
- Reusable components (DataTable, SearchBar, etc.)
- Centralized API service layer
- Pinia stores for state management
- Environment-based configuration
- Comprehensive code comments

## Data Models

### Statistics Response
```typescript
interface Statistics {
  today: {
    new_collections: number
    new_photos: number
    upload_size_bytes: number
  }
  total: {
    collections: number
    photos: number
    storage_bytes: number
  }
  upload_trend: Array<{
    date: string  // YYYY-MM-DD
    count: number
  }>
  storage_distribution: Array<{
    collection_code: string
    size_bytes: number
    percentage: number
  }>
}
```

### User List Item
```typescript
interface User {
  id: string
  username: string
  role: 'admin' | 'user'
  created_at: string
  last_login: string | null
}
```

### Collection List Item
```typescript
interface Collection {
  id: string
  code: string
  name: string
  description: string
  status: 'active' | 'archived' | 'closed'
  created_at: string
  photo_count: number
  updated_at: string
}
```

### Photo List Item
```typescript
interface Photo {
  id: string
  collection_code: string
  filename: string
  file_size: number
  mime_type: string
  dimensions: {
    width: number
    height: number
  }
  uploaded_at: string
  updated_at: string
  thumbnail_path: string
  file_path: string
}
```

## API Endpoints

### Statistics
- `GET /api/v1/admin/statistics` - Get dashboard statistics

### User Management
- `GET /api/v1/admin/users?page=1&limit=20&search=keyword` - List users
- `POST /api/v1/admin/users` - Create user
- `PUT /api/v1/admin/users/:id` - Update user
- `DELETE /api/v1/admin/users/:id` - Delete user
- `DELETE /api/v1/admin/users` - Batch delete users
- `GET /api/v1/admin/profile` - Get current user
- `PUT /api/v1/admin/profile` - Update profile
- `PUT /api/v1/admin/profile/change-password` - Change password

### Collection Management
- `GET /api/v1/admin/collections?page=1&limit=20&code=ABC&date_from=YYYY-MM-DD&date_to=YYYY-MM-DD` - List collections
- `POST /api/v1/admin/collections` - Create collection
- `PUT /api/v1/admin/collections/:code` - Update collection
- `DELETE /api/v1/admin/collections/:code` - Delete collection
- `DELETE /api/v1/admin/collections` - Batch delete collections
- `POST /api/v1/admin/collections/:code/download` - Download all photos as ZIP
- `GET /api/v1/admin/collections/:code/photos?page=1&limit=20` - Get collection photos

### Photo Management
- `GET /api/v1/admin/photos?page=1&limit=20&collection=ABC&date_from=YYYY-MM-DD` - List all photos
- `POST /api/v1/admin/photos/download` - Batch download photos as ZIP
- `DELETE /api/v1/admin/photos` - Batch delete photos
- `GET /api/v1/admin/photos/:id/download` - Download single photo
- `DELETE /api/v1/admin/photos/:id` - Delete single photo

## Dependencies

### Frontend
- Vue 3.4+ (Composition API)
- TypeScript 5.3+
- Element Plus 2.5+ (UI components)
- ECharts 5.4+ (Charts)
- vue-echarts 6.5+ (Vue 3 ECharts wrapper)
- Pinia (State management)
- Vue Router 4+ (Routing)
- Axios 1.6+ (HTTP client)
- Tailwind CSS (Styling)

### Backend
- FastAPI (Python framework)
- Beanie ODM (MongoDB)
- python-jose (JWT)
- passlib (Password hashing)
- Pillow (Image processing)
- aiofiles (Async file operations)
- zipfile (ZIP generation - standard library)

## Success Metrics

1. All pages load within 2 seconds on standard connection
2. All CRUD operations work correctly with proper validation
3. Batch operations handle 100+ items without performance issues
4. All charts render correctly with accurate data
5. Responsive design works on mobile, tablet, and desktop
6. Zero TypeScript errors in production build
7. All accessibility features pass WCAG 2.1 AA standards
8. User can complete common workflows in under 10 clicks
