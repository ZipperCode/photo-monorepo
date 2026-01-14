# Tasks Document - Phase 7: Search & Optimization

## Backend Tasks

- [ ] 7.1. Add database indexes
  - File: apps/api/app/models/photo.py
  - Add indexes on filename and uploaded_at fields
  - Add compound index for collection_code + uploaded_at
  - Purpose: Optimize query performance
  - _Leverage: MongoDB indexing_
  - _Requirements: 7.3_
  - _Prompt: Role: Database Engineer with MongoDB expertise | Task: Add database indexes following requirement 7.3. Create indexes on photo.filename (text index), photo.uploaded_at, compound index on (collection_code, uploaded_at). | Restrictions: Use appropriate index types, test index performance, ensure indexes are created on startup | Success: Indexes improve query performance significantly, queries use indexes correctly_

- [ ] 7.2. Enhance photo list endpoint with search/filter
  - File: apps/api/app/api/v1/admin.py
  - Add search parameter for filename filtering
  - Add date_from and date_to parameters
  - Optimize query with indexes
  - Purpose: Enable search and filtering
  - _Leverage: apps/api/app/models/photo.py_
  - _Requirements: 7.1, 7.2_
  - _Prompt: Role: API Developer with query optimization expertise | Task: Enhance photo list endpoint following requirements 7.1, 7.2. Add search (filename), date_from, date_to query parameters. Use MongoDB text search and date range queries with indexes. | Restrictions: Use indexes for performance, validate parameters, maintain pagination, handle empty results | Success: Search and filtering work correctly, queries are fast, pagination maintained_

## Frontend Tasks

- [ ] 7.3. Add search input to collection detail page
  - File: apps/web/src/pages/AdminCollectionDetail.vue
  - Add search input with debouncing (300ms)
  - Trigger API call on search change
  - Purpose: Enable photo search
  - _Leverage: Vue 3 composables for debouncing_
  - _Requirements: 7.1_
  - _Prompt: Role: Frontend Developer with Vue 3 expertise | Task: Add search functionality following requirement 7.1. Create search input with 300ms debouncing, trigger API call with search parameter, update photo grid with results. | Restrictions: Debounce input, show loading state, handle empty results, clear search functionality | Success: Search works smoothly, debouncing prevents excessive API calls, UX is responsive_

- [ ] 7.4. Add date range filter
  - File: apps/web/src/pages/AdminCollectionDetail.vue
  - Add date range picker component
  - Trigger API call on date change
  - Purpose: Enable date filtering
  - _Requirements: 7.2_
  - _Prompt: Role: Frontend Developer with form handling expertise | Task: Add date range filtering following requirement 7.2. Create date range picker, trigger API call with date_from/date_to parameters, update photo grid. | Restrictions: Validate date range, handle timezone correctly, show loading state, clear filter functionality | Success: Date filtering works correctly, UX is intuitive, timezone handling is correct_

- [ ] 7.5. Implement lazy loading for images
  - File: apps/web/src/components/admin/PhotoCard.vue
  - Add Intersection Observer for lazy loading
  - Load images only when visible
  - Purpose: Optimize initial page load
  - _Requirements: 7.3_
  - _Prompt: Role: Frontend Developer with performance optimization expertise | Task: Implement lazy loading following requirement 7.3. Use Intersection Observer API to load images only when they enter viewport. Show placeholder while loading. | Restrictions: Use native Intersection Observer, handle loading errors, show loading state, optimize for performance | Success: Images load only when visible, initial page load is significantly faster, smooth scrolling maintained_
