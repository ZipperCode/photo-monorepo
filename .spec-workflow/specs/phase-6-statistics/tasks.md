# Tasks Document - Phase 6: Statistics & Data Display

## Backend Tasks

- [ ] 6.1. Create statistics service
  - File: apps/api/app/services/statistics_service.py
  - Implement system statistics calculation using MongoDB aggregation
  - Add recent uploads query
  - Add collection statistics calculation
  - Purpose: Provide statistics calculation logic
  - _Leverage: apps/api/app/models/collection.py, apps/api/app/models/photo.py_
  - _Requirements: 6.1, 6.2, 6.3_
  - _Prompt: Role: Backend Developer with MongoDB aggregation expertise | Task: Create statistics service following requirements 6.1, 6.2, 6.3. Implement functions for system-wide statistics (total collections, photos, storage), recent uploads (last 10), collection-specific statistics. Use MongoDB aggregation for efficiency. | Restrictions: Use aggregation pipelines for performance, handle missing data gracefully, format storage sizes, cache results if possible | Success: Statistics are calculated accurately and efficiently, aggregation queries are optimized_

- [ ] 6.2. Create statistics endpoint
  - File: apps/api/app/api/v1/admin.py
  - Implement GET /api/v1/admin/statistics endpoint
  - Return system statistics and recent uploads
  - Protect with authentication
  - Purpose: Provide API for statistics data
  - _Leverage: apps/api/app/services/statistics_service.py_
  - _Requirements: 6.1, 6.2_
  - _Prompt: Role: API Developer with FastAPI expertise | Task: Create statistics endpoint following requirements 6.1, 6.2. Implement GET /api/v1/admin/statistics that returns system statistics and recent uploads. Require authentication. | Restrictions: Require authentication, handle calculation errors gracefully, return formatted data | Success: Endpoint returns accurate statistics, authentication enforced, response is well-structured_

## Frontend Tasks

- [ ] 6.3. Add statistics display to dashboard
  - File: apps/web/src/pages/AdminDashboard.vue
  - Fetch and display statistics from API
  - Add recent uploads section
  - Format numbers for display
  - Purpose: Display statistics on dashboard
  - _Leverage: apps/web/src/components/admin/StatCard.vue_
  - _Requirements: 6.1, 6.2_
  - _Prompt: Role: Frontend Developer with Vue 3 expertise | Task: Enhance AdminDashboard following requirements 6.1, 6.2. Fetch statistics from API, display using StatCard components, add recent uploads section with thumbnails. Format numbers (e.g., "1.2 GB", "1,234 photos"). | Restrictions: Handle loading state, format numbers for readability, show relative time for uploads, handle empty states | Success: Statistics display correctly, numbers are formatted well, recent uploads section is informative_

- [ ] 6.4. Add statistics to collection cards
  - File: apps/web/src/components/admin/CollectionCard.vue
  - Display photo count, storage, last upload time
  - Format statistics for display
  - Purpose: Show collection statistics in list
  - _Leverage: Tailwind CSS_
  - _Requirements: 6.3_
  - _Prompt: Role: Frontend Developer with Vue 3 expertise | Task: Create or enhance CollectionCard component following requirement 6.3. Display collection name, code, photo count, storage used, last upload time. Format numbers and dates. Use Tailwind CSS. | Restrictions: Format storage sizes, use relative time, handle missing data, make card clickable | Success: Collection cards display statistics clearly, formatting is consistent, cards are interactive_
