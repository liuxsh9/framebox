# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-02-06

### Added
- Initial release of iframe-server
- REST API for HTML project management (CRUD operations)
- Dual access mode: by short ID or friendly name
- Batch file upload with directory structure support
- Web-based management UI with drag-drop uploads
- Static file serving with CORS headers
- Project preview in iframe
- One-click embed code copying
- Security features: path traversal protection, file size limits
- SQLite database with async operations
- Short ID generation using nanoid
- PM2 configuration for production deployment
- Automated test suite with 18 test cases
- Comprehensive documentation (README, TESTING, CONTRIBUTING)
- Quick start script (start.sh)
- Environment configuration via .env file
- LAN access support (0.0.0.0 binding)

### Security
- Path validation to prevent directory traversal
- File size limit (50MB per upload)
- Safe filename sanitization
- Incremental file updates (non-destructive)

### Documentation
- Complete README with usage examples
- Testing guide (TESTING.md)
- Contributing guidelines (CONTRIBUTING.md)
- API documentation via FastAPI auto-generated docs
- MIT License

[0.1.0]: https://github.com/yourusername/iframe-server/releases/tag/v0.1.0
