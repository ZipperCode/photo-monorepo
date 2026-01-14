# Schema Package

This package contains the auto-generated TypeScript types from the FastAPI OpenAPI schema.

## Usage

1. Start the FastAPI backend
2. Run `pnpm --filter @photo/schema generate` to generate types
3. Import types in your frontend code:

```typescript
import type { components, paths } from '@photo/schema'
```

## Type Generation

Types are generated using `openapi-typescript` from the OpenAPI schema exported by FastAPI.
