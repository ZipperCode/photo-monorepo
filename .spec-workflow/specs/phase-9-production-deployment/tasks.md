# Tasks Document - Phase 9: Production Deployment

## Docker Optimization Tasks

- [ ] 9.1. Create production Dockerfile for backend
  - File: apps/api/Dockerfile.prod
  - Implement multi-stage build
  - Optimize image size
  - Use non-root user
  - Purpose: Production-ready backend image
  - _Requirements: 9.1_
  - _Prompt: Role: DevOps Engineer with Docker expertise | Task: Create production Dockerfile following requirement 9.1. Use multi-stage build (builder + runtime), alpine base image, non-root user, health check. | Restrictions: Minimize image size, use non-root user, include health check, optimize layers | Success: Image is small and secure, builds successfully, health check works_

- [ ] 9.2. Create production Dockerfile for frontend
  - File: apps/web/Dockerfile.prod
  - Implement multi-stage build (build + nginx)
  - Optimize build output
  - Purpose: Production-ready frontend image
  - _Requirements: 9.1_
  - _Prompt: Role: DevOps Engineer with Docker and frontend expertise | Task: Create production Dockerfile following requirement 9.1. Use multi-stage build (node builder + nginx), optimize Vite build, configure nginx for SPA. | Restrictions: Minimize image size, optimize build, configure nginx correctly, handle SPA routing | Success: Image is small, build is optimized, nginx serves correctly_

- [ ] 9.3. Create production docker-compose
  - File: docker-compose.prod.yml
  - Configure production services
  - Add health checks and restart policies
  - Purpose: Production deployment configuration
  - _Requirements: 9.1_
  - _Prompt: Role: DevOps Engineer with Docker Compose expertise | Task: Create production docker-compose following requirement 9.1. Configure all services with health checks, restart policies, resource limits, production environment variables. | Restrictions: Use production images, configure health checks, set restart policies, use secrets for sensitive data | Success: All services configured correctly, health checks work, auto-restart enabled_

## HTTPS Configuration Tasks

- [ ] 9.4. Configure Nginx with SSL
  - File: infrastructure/nginx/nginx.prod.conf
  - Add SSL configuration
  - Configure Let's Encrypt certificate paths
  - Add HTTP to HTTPS redirect
  - Purpose: Enable HTTPS
  - _Requirements: 9.2_
  - _Prompt: Role: DevOps Engineer with Nginx and SSL expertise | Task: Configure Nginx for HTTPS following requirement 9.2. Add SSL configuration with Let's Encrypt certificate paths, HTTP to HTTPS redirect, security headers. | Restrictions: Use strong SSL settings, redirect HTTP to HTTPS, add security headers, configure for Let's Encrypt | Success: HTTPS works correctly, HTTP redirects, SSL configuration is secure_

- [ ] 9.5. Create Let's Encrypt setup script
  - File: scripts/setup-ssl.sh
  - Automate certificate generation
  - Configure auto-renewal
  - Purpose: Automate SSL certificate management
  - _Requirements: 9.2_
  - _Prompt: Role: DevOps Engineer with Let's Encrypt expertise | Task: Create SSL setup script following requirement 9.2. Automate certbot certificate generation, configure auto-renewal cron job. | Restrictions: Use certbot, configure auto-renewal, handle errors gracefully, test renewal | Success: Script generates certificates successfully, auto-renewal configured, renewal works_

## Backup Tasks

- [ ] 9.6. Create MongoDB backup script
  - File: scripts/backup-mongodb.sh
  - Implement mongodump with timestamp
  - Add retention policy (30 days)
  - Purpose: Automate database backups
  - _Requirements: 9.3_
  - _Prompt: Role: DevOps Engineer with MongoDB backup expertise | Task: Create backup script following requirement 9.3. Use mongodump to backup MongoDB, add timestamp to backup filename, implement 30-day retention policy. | Restrictions: Use mongodump, add timestamps, clean old backups, handle errors, log results | Success: Backups created successfully, retention policy works, errors logged_

- [ ] 9.7. Configure backup cron job
  - File: scripts/setup-backup-cron.sh
  - Schedule daily backups
  - Configure error notifications
  - Purpose: Automate backup scheduling
  - _Requirements: 9.3_
  - _Prompt: Role: DevOps Engineer with cron expertise | Task: Configure backup cron job following requirement 9.3. Schedule daily backups (e.g., 2 AM), configure error notifications. | Restrictions: Use cron, schedule appropriately, handle errors, send alerts on failure | Success: Cron job scheduled correctly, backups run daily, errors trigger alerts_

## Monitoring and Logging Tasks

- [ ] 9.8. Configure structured logging
  - Files: apps/api/app/core/logging.py
  - Implement JSON structured logging
  - Add log levels and context
  - Purpose: Enable centralized log analysis
  - _Requirements: 9.4_
  - _Prompt: Role: DevOps Engineer with logging expertise | Task: Configure structured logging following requirement 9.4. Implement JSON logging format, add context (request_id, user_id), configure log levels. | Restrictions: Use JSON format, include context, configure levels appropriately, avoid logging sensitive data | Success: Logs are structured and parseable, context included, sensitive data excluded_

- [ ] 9.9. Add health check endpoints
  - File: apps/api/app/api/v1/health.py
  - Implement /health endpoint
  - Check database connectivity
  - Purpose: Enable monitoring and health checks
  - _Requirements: 9.4_
  - _Prompt: Role: Backend Developer with health check expertise | Task: Create health check endpoint following requirement 9.4. Implement /health endpoint that checks database connectivity, returns status and version. | Restrictions: No authentication required, check critical dependencies, return appropriate status codes, include version info | Success: Health check works correctly, database connectivity verified, monitoring can use endpoint_

- [ ] 9.10. Create environment template
  - File: .env.production.template
  - Document all environment variables
  - Add production defaults
  - Purpose: Guide production configuration
  - _Requirements: 9.1_
  - _Prompt: Role: DevOps Engineer | Task: Create environment template following requirement 9.1. Document all required environment variables with descriptions, add production defaults (where safe), include security notes. | Restrictions: Never include actual secrets, provide clear descriptions, mark required vs optional, include security warnings | Success: Template is comprehensive, all variables documented, security notes included_

