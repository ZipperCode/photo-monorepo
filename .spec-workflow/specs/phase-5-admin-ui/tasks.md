# Tasks Document - Phase 5: Admin UI Design

## Backend Tasks

- [ ] 5.1. Create admin photo list endpoint
  - File: apps/api/app/api/v1/admin.py
  - Implement GET /api/v1/admin/collections/{code}/photos endpoint
  - Add pagination support
  - Protect with authentication
  - Purpose: Provide API for admin photo listing
  - _Leverage: apps/api/app/models/photo.py, apps/api/app/api/deps.py_
  - _Requirements: 5.2_
  - _Prompt: Role: API Developer with FastAPI expertise | Task: Create admin photo list endpoint following requirement 5.2. Implement GET /api/v1/admin/collections/{code}/photos with pagination (page, limit), sorting by uploaded_at desc, authentication required. Return photo list with metadata. | Restrictions: Require authentication, implement pagination, validate collection exists, return thumbnails for grid display | Success: Endpoint returns paginated photo list, authentication enforced, performance optimized with indexes_

- [ ] 5.2. Create batch download endpoint
  - File: apps/api/app/api/v1/admin.py
  - Implement POST /api/v1/admin/collections/{code}/photos/download endpoint
  - Generate ZIP file with selected photos
  - Stream ZIP to avoid memory issues
  - Purpose: Enable batch photo download
  - _Leverage: apps/api/app/services/storage_service.py_
  - _Requirements: 5.4_
  - _Prompt: Role: Backend Developer with file streaming expertise | Task: Create batch download endpoint following requirement 5.4. Implement POST endpoint that accepts photo_ids array, creates ZIP file with selected photos, streams ZIP response. Use streaming to handle large downloads. | Restrictions: Require authentication, validate photo ownership, stream ZIP generation, handle missing files gracefully, set appropriate headers | Success: Endpoint generates ZIP correctly, streaming works for large files, errors handled gracefully_

- [ ] 5.3. Create download-all endpoint
  - File: apps/api/app/api/v1/admin.py
  - Implement POST /api/v1/admin/collections/{code}/photos/download-all endpoint
  - Generate ZIP with all collection photos
  - Stream ZIP response
  - Purpose: Enable one-click download all
  - _Leverage: apps/api/app/services/storage_service.py_
  - _Requirements: 5.5_
  - _Prompt: Role: Backend Developer with file streaming expertise | Task: Create download-all endpoint following requirement 5.5. Implement POST endpoint that downloads all photos in collection as ZIP, streams response. Similar to batch download but for all photos. | Restrictions: Require authentication, validate collection exists, stream ZIP, handle large collections efficiently | Success: Endpoint downloads all photos correctly, streaming works, performance acceptable for large collections_

- [ ] 5.4. Create delete-all endpoint
  - File: apps/api/app/api/v1/admin.py
  - Implement DELETE /api/v1/admin/collections/{code}/photos endpoint
  - Delete all photos in collection
  - Return deleted count
  - Purpose: Enable one-click delete all
  - _Leverage: apps/api/app/models/photo.py_
  - _Requirements: 5.5_
  - _Prompt: Role: Backend Developer with database operations expertise | Task: Create delete-all endpoint following requirement 5.5. Implement DELETE endpoint that soft-deletes all photos in collection, returns deleted count. | Restrictions: Require authentication, use soft delete, validate collection exists, return deleted count | Success: Endpoint deletes all photos correctly, soft delete preserves data, count is accurate_

## Frontend Tasks

- [ ] 5.5. Create StatCard component
  - File: apps/web/src/components/admin/StatCard.vue
  - Implement reusable statistics card
  - Add icon, title, value, trend display
  - Purpose: Display key metrics on dashboard
  - _Leverage: Tailwind CSS, Heroicons_
  - _Requirements: 5.1_
  - _Prompt: Role: Frontend Developer with Vue 3 and component design expertise | Task: Create StatCard component following requirement 5.1. Build card with icon, title, value, optional trend indicator. Use Tailwind CSS for styling, Heroicons for icons. | Restrictions: Make component reusable, support different icon types, handle large numbers gracefully, use consistent styling | Success: Component is reusable and visually appealing, displays statistics clearly_

- [ ] 5.6. Create PhotoCard component
  - File: apps/web/src/components/admin/PhotoCard.vue
  - Implement photo card with checkbox and hover overlay
  - Add click handlers for selection and view
  - Purpose: Display individual photo in grid
  - _Leverage: Tailwind CSS_
  - _Requirements: 5.2, 5.4_
  - _Prompt: Role: Frontend Developer with Vue 3 expertise | Task: Create PhotoCard component following requirements 5.2, 5.4. Build card with thumbnail, checkbox (top-left), hover overlay (filename, size), click to open lightbox. Use Tailwind CSS. | Restrictions: Support selection state, emit events for select/click, show hover overlay only on hover, optimize image loading | Success: Card is interactive and responsive, selection works, hover effects are smooth_

- [ ] 5.7. Create PhotoGrid component
  - File: apps/web/src/components/admin/PhotoGrid.vue
  - Implement responsive grid layout
  - Integrate PhotoCard components
  - Purpose: Display photos in responsive grid
  - _Leverage: apps/web/src/components/admin/PhotoCard.vue_
  - _Requirements: 5.2_
  - _Prompt: Role: Frontend Developer with responsive design expertise | Task: Create PhotoGrid component following requirement 5.2. Build responsive grid (grid-cols-2 md:grid-cols-4 lg:grid-cols-6), render PhotoCard for each photo, handle selection state. | Restrictions: Use Tailwind responsive classes, support lazy loading, handle empty state, emit selection events | Success: Grid is responsive across devices, lazy loading works, empty state is clear_

- [ ] 5.8. Create Lightbox component
  - File: apps/web/src/components/admin/Lightbox.vue
  - Implement full-screen photo viewer
  - Add keyboard navigation (ESC, arrows)
  - Add download/delete buttons
  - Purpose: View photos in full-screen
  - _Leverage: Tailwind CSS_
  - _Requirements: 5.3_
  - _Prompt: Role: Frontend Developer with modal and keyboard handling expertise | Task: Create Lightbox component following requirement 5.3. Build full-screen viewer with navigation (prev/next), keyboard support (ESC, arrows), download/delete buttons. Use Tailwind CSS. | Restrictions: Support keyboard navigation, handle edge cases (first/last photo), emit events for actions, prevent body scroll when open | Success: Lightbox is functional, keyboard navigation works, user experience is smooth_

- [ ] 5.9. Create PhotoToolbar component
  - File: apps/web/src/components/admin/PhotoToolbar.vue
  - Implement sticky toolbar with batch actions
  - Add select all, download, delete buttons
  - Purpose: Provide batch operation controls
  - _Leverage: Tailwind CSS_
  - _Requirements: 5.4, 5.5_
  - _Prompt: Role: Frontend Developer with Vue 3 expertise | Task: Create PhotoToolbar component following requirements 5.4, 5.5. Build sticky toolbar with select all/none, selected count, batch download, download all, delete selected, delete all buttons. Use glassmorphism style. | Restrictions: Show only when photos exist, disable buttons when no selection, confirm dangerous actions, use sticky positioning | Success: Toolbar is functional and visually appealing, batch actions work correctly_

- [ ] 5.10. Create AdminDashboard page
  - File: apps/web/src/pages/AdminDashboard.vue
  - Implement dashboard with statistics and collection list
  - Integrate StatCard components
  - Purpose: Main admin landing page
  - _Leverage: apps/web/src/components/admin/StatCard.vue_
  - _Requirements: 5.1_
  - _Prompt: Role: Frontend Developer with dashboard design expertise | Task: Create AdminDashboard page following requirement 5.1. Build dashboard with stat cards (collections, photos, storage), collection list with cards, empty state. Use Tailwind CSS. | Restrictions: Fetch statistics from API, handle loading state, show empty state if no collections, make collection cards clickable | Success: Dashboard is functional and informative, statistics display correctly, navigation works_

- [ ] 5.11. Create AdminCollectionDetail page
  - File: apps/web/src/pages/AdminCollectionDetail.vue
  - Integrate PhotoGrid, PhotoToolbar, Lightbox
  - Implement selection state management
  - Handle batch operations
  - Purpose: Collection photo management page
  - _Leverage: PhotoGrid, PhotoToolbar, Lightbox components_
  - _Requirements: 5.2, 5.3, 5.4, 5.5_
  - _Prompt: Role: Frontend Developer with state management expertise | Task: Create AdminCollectionDetail page following requirements 5.2-5.5. Integrate PhotoGrid, PhotoToolbar, Lightbox components, manage selection state, implement batch download/delete with API calls. | Restrictions: Handle selection state correctly, confirm delete operations, show loading states, handle API errors gracefully | Success: Page is fully functional, all batch operations work, user experience is smooth and intuitive_

