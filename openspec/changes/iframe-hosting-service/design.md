## Context

Building a lightweight HTTP service to host HTML content for embedding in markdown via iframes. The service needs to support CRUD operations, dual-access patterns (ID and name), batch file uploads, and LAN accessibility. Target deployment is a Linux cloud server with pm2 for process management. Expected scale is dozens of projects, each containing HTML and supporting assets (JSON, CSS, images).

## Goals / Non-Goals

**Goals:**
- Provide simple RESTful API for project and file management
- Support dual access: `/view/abc123/` (ID) and `/view/my-project/` (name)
- Enable batch file uploads with directory structure preservation
- Serve HTML with proper CORS for iframe embedding
- Include web UI for project administration
- Ensure 24/7 availability via pm2
- Support dynamic asset loading (fetch JSON from served HTML)
- Allow configurable port with 0.0.0.0 binding for LAN access

**Non-Goals:**
- User authentication/authorization (single-tenant deployment)
- Real-time collaboration or version control
- Server-side rendering or HTML generation
- CDN integration or global distribution
- Advanced monitoring beyond pm2 logs

## Decisions

### 1. Web Framework: FastAPI

**Choice:** FastAPI over Flask/Starlette

**Rationale:**
- Built-in async support for file uploads and database operations
- Automatic OpenAPI documentation (useful for API exploration)
- Pydantic validation reduces boilerplate
- Static file serving included
- Modern Python 3.14 compatibility

**Alternatives considered:**
- Flask: More mature but lacks async and auto-documentation
- Starlette: Lightweight but less batteries-included

### 2. Database: SQLite with aiosqlite

**Choice:** SQLite over PostgreSQL/MySQL

**Rationale:**
- Scale fits perfectly (dozens of projects)
- Single-file database simplifies backup
- Zero configuration/maintenance overhead
- aiosqlite provides async compatibility with FastAPI
- File-based storage aligns with lightweight goal

**Schema:**
```sql
projects (id, name UNIQUE, created_at, updated_at, entry_file)
files (id, project_id, filename, size, uploaded_at)
```

**Alternatives considered:**
- JSON file: Concurrent writes risky, no query flexibility
- PostgreSQL: Overkill for this scale, adds infrastructure complexity

### 3. ID Generation: nanoid (6 characters)

**Choice:** Short random IDs over UUID/auto-increment

**Rationale:**
- Compact URLs: `/view/k3x9p2/` vs `/view/550e8400-e29b-41d4-a716-446655440000/`
- Sufficient entropy for dozens of projects (56B+ combinations)
- URL-friendly character set

**Alternatives considered:**
- UUID: Too long for human-friendly URLs
- Auto-increment: Sequential IDs leak scale information

### 4. Dual Access Pattern

**Choice:** Support both `/view/{id}/` and `/view/{name}/` with name→id lookup

**Rationale:**
- IDs prevent conflicts (name changes don't break embeds)
- Names improve readability in markdown source
- Lookup overhead negligible at this scale (indexed query)

**Implementation:**
```python
# Route handler checks if param is valid ID, else treats as name
if is_valid_id(param):
    project = get_by_id(param)
else:
    project = get_by_name(param)
```

### 5. File Upload Strategy: Incremental Update

**Choice:** Batch upload with incremental updates (not full replacement)

**Rationale:**
- Preserves files not included in upload
- Supports partial updates (just update data.json)
- Reduces bandwidth for large projects

**API:**
```
POST /api/projects/{id}/files
Content-Type: multipart/form-data
files: [file1, file2, ...]
```

Files with same path are overwritten; others preserved.

**Alternatives considered:**
- Full replacement: Risky (accidental deletions) and inefficient
- Single file uploads: Too many round-trips for initial upload

### 6. Directory Structure Preservation

**Choice:** Support nested paths in filenames

**Implementation:**
```python
# Upload with filename="assets/style.css"
# Stored at data/projects/{id}/assets/style.css
# Accessible at /view/{id}/assets/style.css
```

Safe path validation prevents directory traversal attacks.

### 7. Entry File Resolution

**Choice:** Configurable entry file (default: index.html)

**Rationale:**
- Flexibility for non-standard entry points
- `/view/{id}/` auto-serves entry file
- Explicit paths still work: `/view/{id}/main.html`

Stored in projects table: `entry_file` column.

### 8. CORS Configuration

**Choice:** Permissive CORS for iframe embedding

**Configuration:**
```python
CORSMiddleware(
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Rationale:**
- No authentication means no CSRF risk
- Content designed for public embedding
- Simplifies development and usage

**Future:** Can restrict origins if deployment context changes.

### 9. Web UI Technology

**Choice:** Single-page static HTML + vanilla JS

**Rationale:**
- No build step required
- Served by same FastAPI server
- Minimal dependencies (fetch API + DOM manipulation)
- Fast load times

**Features:**
- Project list with search
- Create/delete projects
- File upload (drag-drop + file picker)
- Copy embed code snippet
- Preview iframe

**Alternatives considered:**
- React/Vue: Overkill, adds build complexity
- Server-side templates: Less interactive UX

### 10. Configuration Management

**Choice:** Environment variables + .env file

**Configuration:**
```bash
PORT=8000
HOST=0.0.0.0
DATA_DIR=./data
```

**Rationale:**
- 12-factor app compliance
- Easy override in different environments
- pydantic-settings provides type-safe parsing

### 11. Process Management: pm2

**Choice:** pm2 over systemd service

**Rationale:**
- Simpler configuration (ecosystem.config.js)
- Better logging (pm2 logs with auto-rotation)
- Cross-platform (works on macOS for dev)
- Process monitoring dashboard (pm2 monit)

**Configuration:**
```javascript
{
  name: 'iframe-server',
  script: 'main.py',
  interpreter: 'python3',
  instances: 1,
  autorestart: true,
  max_memory_restart: '500M'
}
```

**Alternatives considered:**
- systemd: Linux-only, more verbose config
- supervisor: Similar to pm2 but Python-specific

## Risks / Trade-offs

### Risk: Name conflicts on project creation
→ **Mitigation:** Return 409 Conflict, require unique names (enforced by DB constraint)

### Risk: Directory traversal via malicious filenames
→ **Mitigation:** Validate paths (reject `..`, absolute paths, non-printable chars)

### Risk: Unbounded file uploads (disk exhaustion)
→ **Mitigation:**
- Limit total upload size per request (e.g., 50MB)
- Monitor disk usage via pm2/system alerts
- Future: Add per-project quota

### Risk: SQLite lock contention under concurrent writes
→ **Mitigation:**
- aiosqlite handles locking
- Scale (dozens of projects) means low write frequency
- Read-heavy workload (serving files)

### Trade-off: No authentication
→ **Accepted:** Single-tenant deployment, trust environment (LAN/VPN)
→ **Future:** Add API key if multi-tenant needed

### Trade-off: No versioning/history
→ **Accepted:** Simplicity over complexity
→ **Workaround:** User can back up data/ directory

### Risk: pm2 process death without restart
→ **Mitigation:**
- autorestart: true in pm2 config
- pm2 startup for boot persistence
- Health check endpoint: GET /api/health

## Migration Plan

**Initial Deployment:**

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   npm install -g pm2
   ```

2. Initialize database:
   ```bash
   python -m app.database init  # Creates schema
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit PORT, HOST, DATA_DIR
   ```

4. Start with pm2:
   ```bash
   pm2 start ecosystem.config.js
   pm2 save
   pm2 startup  # Enable boot persistence
   ```

5. Verify:
   ```bash
   curl http://localhost:8000/api/health
   pm2 logs iframe-server
   ```

**Rollback Strategy:**
- Stop pm2: `pm2 stop iframe-server`
- data/ directory preserves all content (portable)
- Restore previous version and restart

**Monitoring:**
- pm2 status: `pm2 list`
- Logs: `pm2 logs iframe-server --lines 100`
- Resource usage: `pm2 monit`

## Open Questions

None at this stage. Design is finalized based on exploration phase discussions.
