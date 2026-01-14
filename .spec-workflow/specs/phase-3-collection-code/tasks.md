# Tasks Document - Phase 3: Collection Code Management

## Backend Tasks

- [ ] 3.1. Create code generator utility
  - File: apps/api/app/utils/code_generator.py
  - Implement random code generation with cryptographic randomness
  - Implement uniqueness verification with database check
  - Add retry logic for collision handling
  - Purpose: Generate unique 6-character collection codes
  - _Leverage: apps/api/app/core/database.py_
  - _Requirements: 3.1_
  - _Prompt: Role: Backend Developer with cryptography expertise | Task: Implement code generator following requirement 3.1. Create functions for generating random 6-character alphanumeric codes using secrets module, verify uniqueness against database, implement retry logic (max 10 attempts) for collisions. Avoid ambiguous characters (0/O, 1/I/l). | Restrictions: Use secrets module only for randomness, uppercase all codes, handle collision gracefully, fail after 10 retries, exclude ambiguous characters | Success: Codes are cryptographically random, uniqueness is verified, collisions handled with retry, codes are uppercase and unambiguous_

- [ ] 3.2. Create Collection data model
  - File: apps/api/app/models/collection.py
  - Define Collection Pydantic models
  - Implement database operations (CRUD)
  - Add MongoDB indexes for code field
  - Purpose: Provide data layer for collection management
  - _Leverage: apps/api/app/core/database.py_
  - _Requirements: 3.3, 3.4, 3.5_
  - _Prompt: Role: Backend Developer with MongoDB and Pydantic expertise | Task: Create Collection model following requirements 3.3, 3.4, 3.5. Define Pydantic models for Collection with all fields (code, name, description, status, settings, statistics), implement CRUD operations, add unique index on code field (case-insensitive). | Restrictions: Ensure code uniqueness, validate all inputs, implement soft delete (is_deleted flag), handle database errors gracefully, index code field for fast lookups | Success: Model is well-defined, CRUD operations work correctly, code uniqueness enforced, soft delete implemented, queries are optimized with indexes_

- [ ] 3.3. Create collection service layer
  - File: apps/api/app/services/collection_service.py
  - Implement business logic for collection operations
  - Add code validation logic
  - Implement statistics update functions
  - Purpose: Provide business logic layer for collections
  - _Leverage: apps/api/app/models/collection.py, apps/api/app/utils/code_generator.py_
  - _Requirements: 3.2, 3.5_
  - _Prompt: Role: Backend Developer with service architecture expertise | Task: Create collection service following requirements 3.2, 3.5. Implement validate_code function (case-insensitive, check status), create_collection with code generation, update_statistics for photo uploads. | Restrictions: Validate code case-insensitively, check collection status before allowing access, update statistics atomically, handle errors gracefully | Success: Service layer encapsulates business logic, validation works correctly, statistics updates are atomic and accurate_

- [ ] 3.4. Create public validation endpoint
  - File: apps/api/app/api/v1/collections.py
  - Implement POST /api/v1/collections/validate endpoint
  - Add request/response models
  - Integrate with collection service
  - Purpose: Allow users to validate collection codes
  - _Leverage: apps/api/app/services/collection_service.py_
  - _Requirements: 3.2_
  - _Prompt: Role: API Developer with FastAPI expertise | Task: Create validation endpoint following requirement 3.2. Implement POST /api/v1/collections/validate that accepts code, validates using service layer, returns collection details if valid. | Restrictions: No authentication required, return 404 for invalid codes, return 403 for closed collections, validate input format | Success: Endpoint validates codes correctly, returns appropriate status codes, error messages are user-friendly_

- [ ] 3.5. Create admin CRUD endpoints
  - File: apps/api/app/api/v1/admin.py
  - Implement collection CRUD endpoints (POST, GET, PATCH, DELETE)
  - Add pagination support for list endpoint
  - Protect with authentication middleware
  - Purpose: Allow administrators to manage collections
  - _Leverage: apps/api/app/api/deps.py, apps/api/app/services/collection_service.py_
  - _Requirements: 3.3_
  - _Prompt: Role: API Developer with FastAPI and authentication expertise | Task: Create admin CRUD endpoints following requirement 3.3. Implement POST /admin/collections (create), GET /admin/collections (list with pagination), GET /admin/collections/{code} (detail), PATCH /admin/collections/{code} (update), DELETE /admin/collections/{code} (soft delete). Protect all with get_current_user dependency. | Restrictions: Require authentication for all endpoints, implement pagination (page, limit), validate all inputs, use soft delete, return appropriate status codes | Success: All CRUD operations work correctly, authentication is enforced, pagination works, soft delete preserves data_

## Frontend Tasks

- [ ] 3.6. Create access code input page
  - File: apps/web/src/pages/AccessCodePage.vue
  - Implement code input form with validation
  - Add code validation API call
  - Handle validation success/error states
  - Purpose: Allow users to enter and validate collection codes
  - _Leverage: apps/web/src/services/api.ts, Tailwind CSS_
  - _Requirements: 3.2_
  - _Prompt: Role: Frontend Developer with Vue 3 and form handling expertise | Task: Create access code input page following requirement 3.2. Build form with 6-character code input (uppercase display), submit button, validation API call, success redirect to upload page, error message display. Use Tailwind CSS for styling. | Restrictions: Convert input to uppercase for display, validate format before API call, show loading state during validation, display clear error messages, redirect on success | Success: Code input is user-friendly, validation works correctly, errors are clear, successful validation redirects to upload page_

- [ ] 3.7. Create admin collection management form
  - File: apps/web/src/components/admin/CollectionForm.vue
  - Implement create/edit form for collections
  - Add form fields for name, description, settings
  - Integrate with admin CRUD API
  - Purpose: Allow administrators to create and edit collections
  - _Leverage: apps/web/src/stores/auth.ts, Tailwind CSS_
  - _Requirements: 3.3, 3.4_
  - _Prompt: Role: Frontend Developer with Vue 3 and form management expertise | Task: Create collection management form following requirements 3.3, 3.4. Build form with fields for name, description, status, allow_upload, max_file_size, allowed_extensions. Support both create and edit modes. Display generated code after creation. Use Tailwind CSS. | Restrictions: Validate all inputs, show loading state during API calls, display generated code prominently, handle errors gracefully, support both create and edit modes | Success: Form is functional for both create and edit, validation works, generated code is displayed clearly, API integration works correctly_
