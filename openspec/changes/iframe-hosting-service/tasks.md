## 1. Project Setup

- [x] 1.1 Update pyproject.toml with all required dependencies (fastapi, uvicorn, aiosqlite, nanoid, python-multipart, pydantic-settings)
- [x] 1.2 Create project directory structure (app/, app/api/, app/utils/, data/projects/)
- [x] 1.3 Create .env.example file with configuration template (PORT, HOST, DATA_DIR)
- [x] 1.4 Create .gitignore to exclude data/, .env, __pycache__

## 2. Database Layer

- [x] 2.1 Create app/database.py with SQLite schema (projects and files tables)
- [x] 2.2 Implement async database connection management using aiosqlite
- [x] 2.3 Add database initialization function to create tables
- [x] 2.4 Implement CRUD operations for projects table
- [x] 2.5 Implement CRUD operations for files table
- [x] 2.6 Add database indexes for performance (name, project_id)

## 3. Configuration Management

- [x] 3.1 Create app/config.py with pydantic Settings class
- [x] 3.2 Define configuration fields (port, host, data_dir) with defaults
- [x] 3.3 Add .env file loading support

## 4. ID Generation Utility

- [x] 4.1 Create app/utils/id_generator.py
- [x] 4.2 Implement nanoid-based 6-character ID generation
- [x] 4.3 Add collision detection and regeneration logic

## 5. Pydantic Models

- [x] 5.1 Create app/models.py with request/response models
- [x] 5.2 Define ProjectCreate, ProjectResponse, ProjectUpdate schemas
- [x] 5.3 Define FileInfo schema for file metadata
- [x] 5.4 Define ListProjectsResponse with search/filter support

## 6. File Upload Utilities

- [x] 6.1 Create app/utils/file_validation.py
- [x] 6.2 Implement path validation (reject .., absolute paths, invalid chars)
- [x] 6.3 Implement file size validation (50MB limit)
- [x] 6.4 Add safe filename sanitization

## 7. Project Management API

- [x] 7.1 Create app/api/projects.py with router
- [x] 7.2 Implement POST /api/projects (create with unique name validation)
- [x] 7.3 Implement GET /api/projects (list with search and limit)
- [x] 7.4 Implement GET /api/projects/{id_or_name} (dual identifier resolution)
- [x] 7.5 Implement PUT /api/projects/{id} (update name/entry_file)
- [x] 7.6 Implement DELETE /api/projects/{id} (cascade delete files)

## 8. File Upload API

- [x] 8.1 Create app/api/files.py with router
- [x] 8.2 Implement POST /api/projects/{id}/files (batch upload)
- [x] 8.3 Add multipart form data parsing for file arrays
- [x] 8.4 Implement incremental file update logic (preserve unuploaded files)
- [x] 8.5 Create directory structure for nested paths
- [x] 8.6 Update files table with uploaded file metadata
- [x] 8.7 Implement GET /api/projects/{id}/files (list files)

## 9. Static File Serving

- [x] 9.1 Create app/api/static.py with router
- [x] 9.2 Implement GET /view/{id_or_name}/ (serve entry file)
- [x] 9.3 Implement GET /view/{id_or_name}/{filepath:path} (serve any file)
- [x] 9.4 Add dual identifier resolution (ID vs name lookup)
- [x] 9.5 Set correct Content-Type headers based on file extension
- [x] 9.6 Handle 404 for missing files/projects

## 10. CORS Configuration

- [x] 10.1 Add CORS middleware to main app
- [x] 10.2 Configure permissive CORS (allow_origins=*)
- [x] 10.3 Test OPTIONS preflight requests

## 11. Main Application

- [x] 11.1 Create main.py as application entry point
- [x] 11.2 Initialize FastAPI app with metadata
- [x] 11.3 Register all API routers (projects, files, static)
- [x] 11.4 Add CORS middleware
- [x] 11.5 Create health check endpoint GET /api/health
- [x] 11.6 Add database initialization on startup
- [x] 11.7 Configure uvicorn server with host/port from settings

## 12. Web UI - HTML Structure

- [x] 12.1 Create static/index.html with basic layout
- [x] 12.2 Add project list container with card-based layout
- [x] 12.3 Add create project modal/form
- [x] 12.4 Add file upload zone with drag-drop target
- [x] 12.5 Add search input for filtering projects
- [x] 12.6 Add preview iframe container

## 13. Web UI - CSS Styling

- [x] 13.1 Create static/style.css with responsive grid layout
- [x] 13.2 Style project cards with hover effects
- [x] 13.3 Style modal/form components
- [x] 13.4 Add drag-drop visual feedback
- [x] 13.5 Implement responsive breakpoints (desktop/tablet)
- [x] 13.6 Add loading spinner and progress indicators

## 14. Web UI - JavaScript Logic

- [x] 14.1 Create static/app.js with API client functions
- [x] 14.2 Implement loadProjects() to fetch and render project list
- [x] 14.3 Implement createProject() with form submission
- [x] 14.4 Implement deleteProject() with confirmation dialog
- [x] 14.5 Implement uploadFiles() with FormData and progress tracking
- [x] 14.6 Add drag-drop event handlers
- [x] 14.7 Implement search/filter functionality
- [x] 14.8 Add copyEmbedCode() with clipboard API
- [x] 14.9 Implement showPreview() to display project in iframe
- [x] 14.10 Add error handling and user feedback (toasts/alerts)

## 15. PM2 Configuration

- [x] 15.1 Create ecosystem.config.js with pm2 configuration
- [x] 15.2 Configure interpreter, env variables, and restart policy
- [x] 15.3 Set up log file paths
- [x] 15.4 Configure memory restart limit (500M)

## 16. Documentation

- [x] 16.1 Update README.md with project overview and features
- [x] 16.2 Add installation instructions (dependencies, database init)
- [x] 16.3 Add configuration documentation (.env variables)
- [x] 16.4 Add usage examples (API curl commands, markdown embedding)
- [x] 16.5 Add deployment instructions (pm2 commands, startup config)
- [x] 16.6 Document API endpoints with examples

## 17. Testing and Verification

Core implementation complete. Automated test suite created (`test.sh`).
See `TESTING.md` for complete testing guide.

- [x] 17.1 Test project creation via API
- [x] 17.2 Test file upload (single, batch, nested paths)
- [x] 17.3 Test static serving (by ID, by name, nested files)
- [x] 17.4 Test dual identifier resolution
- [x] 17.5 Test name conflict handling (409 errors)
- [x] 17.6 Test path validation (reject .., absolute paths)
- [x] 17.7 Test CORS headers in responses
- [x] 17.8 Test web UI functionality (create, upload, delete, preview)
- [x] 17.9 Test relative path resolution in served HTML
- [x] 17.10 Test pm2 process management (start, restart, logs)
- [x] 17.11 Verify LAN accessibility (0.0.0.0 binding)
