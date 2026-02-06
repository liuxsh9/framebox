## Why

Markdown documents often need to embed rich interactive HTML content (charts, diagrams, visualizations) via iframes. Currently, there's no lightweight solution to host and manage these HTML files with a simple API. Users need a dedicated service that can host multiple HTML projects, provide easy CRUD operations, ensure high availability, and support dynamic asset loading (like JSON data files fetched at runtime).

## What Changes

- Create a new FastAPI-based HTTP server for hosting HTML projects embeddable in markdown via iframes
- Implement RESTful API for project and file management (create, read, update, delete)
- Add dual-access static serving (by project ID or user-friendly name)
- Build a web-based management UI for visual project administration
- Support batch file uploads with directory structure preservation
- Configure for 0.0.0.0 binding (LAN access) with customizable port
- Set up pm2-based process management for production deployment on Linux

## Capabilities

### New Capabilities
- `project-management`: CRUD operations for HTML projects with dual ID/name lookup
- `file-upload`: Batch file upload with incremental updates and directory structure support
- `static-serving`: Serve HTML projects via iframe-friendly URLs with automatic entry file resolution
- `web-ui`: Browser-based management interface for project administration

### Modified Capabilities
<!-- No existing capabilities are being modified -->

## Impact

- **New project**: No existing code affected
- **Dependencies**: Adds FastAPI, uvicorn, aiosqlite, nanoid, python-multipart, pydantic-settings
- **Infrastructure**: Requires SQLite database and file storage directory
- **Deployment**: Requires pm2 on Linux cloud server
- **Network**: Service runs on configurable port (default 8000) bound to 0.0.0.0 for LAN access
