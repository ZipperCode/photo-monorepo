# Tasks Document - Phase 4: Photo Upload System

## Backend Tasks

- [ ] 4.1. Create storage service abstraction
  - File: apps/api/app/services/storage_service.py
  - Implement local file storage operations
  - Add async file save/delete/get functions
  - Create storage path structure
  - Purpose: Provide abstraction layer for file storage
  - _Leverage: apps/api/app/core/config.py_
  - _Requirements: 4.3_
  - _Prompt: Role: Backend Developer with async file handling expertise | Task: Implement storage service following requirement 4.3. Create async functions for saving files (with UUID naming), deleting files, getting file URLs. Use storage path pattern: storage/uploads/{code}/{year}/{month}/{uuid}_{filename}. Use aiofiles for async operations. | Restrictions: Sanitize filenames, prevent path traversal, ensure directory creation, handle storage errors gracefully, use UUID for uniqueness | Success: Storage service works correctly, files are stored in correct paths, filenames are sanitized, async operations are efficient_

- [ ] 4.2. Create image processing service
  - File: apps/api/app/services/image_service.py
  - Implement thumbnail generation with Pillow
  - Add EXIF metadata extraction
  - Add image dimension detection
  - Purpose: Handle image processing operations
  - _Leverage: apps/api/app/services/storage_service.py_
  - _Requirements: 4.4, 4.5_
  - _Prompt: Role: Backend Developer with image processing expertise | Task: Implement image service following requirements 4.4, 4.5. Create functions for generating 400x400 thumbnails (maintain aspect ratio), extracting EXIF data (camera make/model/timestamp), getting image dimensions. Use Pillow library. | Restrictions: Handle missing EXIF gracefully, maintain aspect ratio for thumbnails, handle corrupted images, log errors but don't fail upload | Success: Thumbnails are generated correctly, EXIF extraction works, errors are handled gracefully, processing is efficient_

- [ ] 4.3. Create Photo data model
  - File: apps/api/app/models/photo.py
  - Define Photo Pydantic models
  - Implement database operations (create, list, delete)
  - Add MongoDB indexes for collection_code and uploaded_at
  - Purpose: Provide data layer for photo management
  - _Leverage: apps/api/app/core/database.py_
  - _Requirements: 4.3, 4.4, 4.5_
  - _Prompt: Role: Backend Developer with MongoDB expertise | Task: Create Photo model following requirements 4.3, 4.4, 4.5. Define Pydantic models with all fields (collection_code, filename, paths, size, mime_type, dimensions, metadata, uploader_info). Implement CRUD operations, add indexes on collection_code and uploaded_at. | Restrictions: Validate all inputs, implement soft delete, handle database errors, optimize queries with indexes | Success: Model is well-defined, database operations work correctly, indexes improve query performance_

- [ ] 4.4. Create photo service orchestration layer
  - File: apps/api/app/services/photo_service.py
  - Implement upload workflow orchestration
  - Add file validation logic (type, size, extension)
  - Integrate storage, image, and collection services
  - Purpose: Orchestrate complete upload workflow
  - _Leverage: apps/api/app/services/storage_service.py, apps/api/app/services/image_service.py, apps/api/app/services/collection_service.py_
  - _Requirements: 4.1, 4.2_
  - _Prompt: Role: Backend Developer with workflow orchestration expertise | Task: Create photo service following requirements 4.1, 4.2. Implement upload_photos function that validates files (magic number check, size, extension), stores files, generates thumbnails, extracts EXIF, creates database records, updates collection statistics. Handle partial failures gracefully. | Restrictions: Validate by magic number not extension, rollback on storage failure, process files in parallel where possible, update statistics atomically | Success: Upload workflow is complete and robust, validation is thorough, partial failures handled correctly, statistics updated accurately_

- [ ] 4.5. Create photo upload endpoint
  - File: apps/api/app/api/v1/photos.py
  - Implement POST /api/v1/collections/{code}/photos endpoint
  - Handle multipart/form-data file uploads
  - Return upload results with success/failure details
  - Purpose: Provide API endpoint for photo uploads
  - _Leverage: apps/api/app/services/photo_service.py_
  - _Requirements: 4.1_
  - _Prompt: Role: API Developer with FastAPI and file upload expertise | Task: Create upload endpoint following requirement 4.1. Implement POST /api/v1/collections/{code}/photos that accepts multipart/form-data with multiple files, validates collection code, calls photo service, returns results with uploaded/failed lists. | Restrictions: No authentication required, validate collection exists and allows uploads, handle large files efficiently, return detailed error messages | Success: Endpoint handles multi-file uploads correctly, returns clear results, errors are informative_

## Frontend Tasks

- [ ] 4.6. Create drag-and-drop upload component
  - File: apps/web/src/components/upload/FileDropZone.vue
  - Implement drag-and-drop area for file selection
  - Add file preview before upload
  - Support multiple file selection
  - Purpose: Provide user-friendly file selection interface
  - _Leverage: Tailwind CSS_
  - _Requirements: 4.1_
  - _Prompt: Role: Frontend Developer with Vue 3 and drag-and-drop expertise | Task: Create drag-and-drop component following requirement 4.1. Build drop zone with visual feedback (hover state), file input fallback, file preview list, remove file functionality. Use Tailwind CSS for styling. | Restrictions: Support multiple files, show file size and type, validate file types client-side, provide clear visual feedback | Success: Drop zone is intuitive and responsive, file preview works correctly, user experience is smooth_

- [ ] 4.7. Create upload progress component
  - File: apps/web/src/components/upload/UploadProgress.vue
  - Implement real-time progress tracking for each file
  - Show upload status (pending, uploading, success, failed)
  - Display overall progress summary
  - Purpose: Provide visual feedback during upload
  - _Leverage: Tailwind CSS_
  - _Requirements: 4.1_
  - _Prompt: Role: Frontend Developer with Vue 3 and progress tracking expertise | Task: Create upload progress component following requirement 4.1. Build progress bars for each file, status indicators (pending/uploading/success/failed), overall progress summary, cancel upload functionality. Use Tailwind CSS. | Restrictions: Update progress in real-time, handle upload errors gracefully, show clear status for each file, provide cancel option | Success: Progress tracking is accurate and real-time, status indicators are clear, user can monitor upload progress effectively_

- [ ] 4.8. Create upload page with integration
  - File: apps/web/src/pages/UploadPage.vue
  - Integrate FileDropZone and UploadProgress components
  - Implement upload API call with FormData
  - Handle upload results and display summary
  - Purpose: Provide complete upload interface for users
  - _Leverage: apps/web/src/components/upload/FileDropZone.vue, apps/web/src/components/upload/UploadProgress.vue_
  - _Requirements: 4.1_
  - _Prompt: Role: Frontend Developer with Vue 3 and API integration expertise | Task: Create upload page following requirement 4.1. Integrate drop zone and progress components, implement upload API call using FormData, handle responses (success/failed lists), display upload summary. | Restrictions: Validate collection code before upload, handle network errors, show clear success/failure messages, allow retry for failed uploads | Success: Upload page is fully functional, API integration works correctly, user experience is smooth and informative_
