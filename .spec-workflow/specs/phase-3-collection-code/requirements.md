# Requirements Document - Phase 3: Collection Code Management

## Introduction

Phase 3 implements the collection code management system, which is the core feature enabling administrators to create unique 6-character codes for photo collection events. Users can validate these codes to access upload functionality, while administrators can manage codes through CRUD operations.

## Alignment with Product Vision

This feature is central to the product's purpose: enabling event-based photo collection through simple, shareable codes. It supports the goal of making photo collection accessible without requiring user registration.

## Requirements

### Requirement 3.1: Collection Code Generation

**User Story:** As an administrator, I want to generate unique 6-character collection codes, so that I can create new photo collection events.

#### Acceptance Criteria

1. WHEN administrator creates collection THEN system SHALL generate unique 6-character alphanumeric code
2. WHEN code is generated THEN system SHALL verify uniqueness in database before assignment
3. IF code collision occurs THEN system SHALL regenerate until unique code is found
4. WHEN code is displayed THEN system SHALL use uppercase format for consistency

### Requirement 3.2: Collection Code Validation

**User Story:** As a user, I want to validate a collection code, so that I can access the photo upload interface.

#### Acceptance Criteria

1. WHEN user submits code THEN system SHALL validate code case-insensitively
2. IF code exists and status is "active" THEN system SHALL return collection details
3. IF code does not exist or status is not "active" THEN system SHALL return error
4. WHEN validation succeeds THEN system SHALL return collection name, description, and upload settings

### Requirement 3.3: Collection CRUD Operations

**User Story:** As an administrator, I want to create, read, update, and delete collections, so that I can manage photo collection events.

#### Acceptance Criteria

1. WHEN administrator creates collection THEN system SHALL store name, description, and settings
2. WHEN administrator updates collection THEN system SHALL preserve code and creation metadata
3. WHEN administrator deletes collection THEN system SHALL mark as deleted (soft delete)
4. WHEN administrator lists collections THEN system SHALL support pagination and filtering

### Requirement 3.4: Collection Settings

**User Story:** As an administrator, I want to configure collection settings, so that I can control upload behavior.

#### Acceptance Criteria

1. WHEN collection is created THEN system SHALL allow configuration of allow_upload flag
2. WHEN collection is created THEN system SHALL allow configuration of max_file_size limit
3. WHEN collection is created THEN system SHALL allow configuration of allowed_extensions list
4. IF allow_upload is false THEN system SHALL reject upload attempts with clear message

### Requirement 3.5: Collection Statistics

**User Story:** As an administrator, I want to view collection statistics, so that I can monitor collection activity.

#### Acceptance Criteria

1. WHEN photos are uploaded THEN system SHALL update total_photos count
2. WHEN photos are uploaded THEN system SHALL update total_size_bytes
3. WHEN photo is uploaded THEN system SHALL update last_upload_at timestamp
4. WHEN administrator views collection THEN system SHALL display current statistics

## Non-Functional Requirements

### Code Architecture and Modularity
- **Single Responsibility Principle**: Separate code generation, validation, CRUD operations, and statistics into distinct modules
- **Modular Design**: Code generator should be reusable and testable independently
- **Dependency Management**: Collection service should not depend on photo service
- **Clear Interfaces**: Define clear contracts between API, service, and repository layers

### Performance
- Code generation should complete in < 50ms
- Code validation should complete in < 20ms (database indexed lookup)
- Collection listing should support pagination for large datasets
- Database queries should use indexes for code lookups

### Security
- Collection codes should be case-insensitive for user convenience
- Deleted collections should not be accessible via validation endpoint
- Only authenticated administrators can perform CRUD operations
- Code generation should use cryptographically secure random source

### Reliability
- Code generation should handle collision gracefully with retry logic
- Database operations should be atomic (create/update/delete)
- Soft delete should preserve data for audit purposes
- Statistics updates should be transactional with photo uploads

### Usability
- Collection codes should avoid ambiguous characters (0/O, 1/I/l)
- Validation errors should provide clear, user-friendly messages
- Admin interface should provide search and filter capabilities
- Collection status should be clearly indicated (active/archived/closed)
