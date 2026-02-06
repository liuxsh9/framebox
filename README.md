# framebox

[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight, self-hosted service for hosting HTML content embeddable via iframes in Markdown documents. Perfect for embedding interactive charts, visualizations, and rich content in documentation, blogs, and notes.

## ✨ Features

- 🚀 **Simple REST API** - CRUD operations for HTML projects
- 🔄 **Dual Access** - Access content by short ID or friendly name
- 📦 **Batch Upload** - Upload multiple files at once with directory structure support
- 🎨 **Web UI** - Beautiful management interface with drag-drop uploads
- 🌐 **CORS Ready** - Configured for seamless iframe embedding
- 🔒 **Secure** - Path traversal protection and file size limits
- ⚡ **Fast** - Built with FastAPI and async SQLite
- 🛠️ **Easy Deploy** - PM2 ready with auto-restart and logging

## 🎯 Use Cases

- Embed interactive charts (ECharts, D3.js) in Markdown documentation
- Host HTML visualizations for note-taking apps (Obsidian, Notion)
- Serve dynamic content in static site generators
- Share interactive demos and prototypes
- Embed custom HTML widgets in blogs and wikis

## 📦 Quick Start

### Prerequisites

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/framebox.git
cd framebox

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv pip install -e .

# Copy environment template
cp .env.example .env
```

### Run

```bash
# Start the server
./start.sh

# Or manually
uv run python main.py
```

Server will be available at `http://localhost:8001`

- **Web UI**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs
- **Health Check**: http://localhost:8001/api/health

## 📖 Usage

### Web Interface

1. Open http://localhost:8001 in your browser
2. Click **"Create Project"** to create a new HTML project
3. **Drag and drop** files or use the upload button
4. Click **"Preview"** to see your content
5. Click **"Embed"** to copy the iframe code

### API Examples

#### Create a Project

```bash
curl -X POST http://localhost:8001/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "my-chart", "entry_file": "index.html"}'

# Response
{
  "id": "k3x9p2",
  "name": "my-chart",
  "created_at": "2024-02-06T10:30:00Z",
  "updated_at": "2024-02-06T10:30:00Z",
  "entry_file": "index.html"
}
```

#### Upload Files

```bash
curl -X POST http://localhost:8001/api/projects/k3x9p2/files \
  -F "files=@index.html" \
  -F "files=@data.json" \
  -F "files=@assets/style.css;filename=assets/style.css"
```

#### Embed in Markdown

```markdown
<!-- By ID -->
<iframe src="http://your-server:8001/view/k3x9p2/" width="800" height="600"></iframe>

<!-- By name -->
<iframe src="http://your-server:8001/view/my-chart/" width="800" height="600"></iframe>
```

### Dynamic Asset Loading

Your HTML files can reference other assets using relative paths:

```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="./style.css">
</head>
<body>
    <div id="chart"></div>
    <script>
        // Fetch data dynamically
        fetch('./data.json')
            .then(r => r.json())
            .then(data => renderChart(data));
    </script>
</body>
</html>
```

All paths are automatically resolved relative to your project.

## 🏗️ Architecture

```
framebox/
├── app/                    # Application code
│   ├── api/               # API routes
│   │   ├── projects.py    # Project CRUD
│   │   ├── files.py       # File upload/management
│   │   └── static.py      # Static file serving
│   ├── utils/             # Utilities
│   │   ├── id_generator.py      # Short ID generation
│   │   └── file_validation.py  # Security validation
│   ├── config.py          # Configuration
│   ├── database.py        # SQLite operations
│   └── models.py          # Pydantic models
├── static/                # Web UI
│   ├── index.html
│   ├── style.css
│   └── app.js
├── data/                  # Storage (auto-created)
│   ├── framebox.db        # SQLite database
│   └── projects/          # Project files
├── main.py               # Entry point
├── start.sh              # Quick start script
├── test.sh               # Test suite
├── ecosystem.config.js   # PM2 configuration
└── pyproject.toml        # Dependencies
```

## 🚀 Production Deployment

### Using PM2

```bash
# Install PM2
npm install -g pm2

# Start service
pm2 start ecosystem.config.js

# Save process list
pm2 save

# Enable startup on boot
pm2 startup
```

### Using Docker (Coming Soon)

```bash
docker-compose up -d
```

### Configuration

Environment variables (`.env` file):

```bash
PORT=8001          # Server port
HOST=0.0.0.0       # Bind address (0.0.0.0 for LAN access)
DATA_DIR=./data    # Data storage directory
```

## 🧪 Testing

Run the automated test suite:

```bash
# Start server
uv run python main.py &

# Run tests
./test.sh

# Stop server
pkill -f "uv run python"
```

The test suite covers:
- ✅ Project CRUD operations
- ✅ File upload (single, batch, nested paths)
- ✅ Static file serving (by ID and name)
- ✅ CORS headers
- ✅ Security validation (path traversal, file size)
- ✅ Dual identifier resolution

See [TESTING.md](TESTING.md) for detailed testing guide.

## 📚 API Reference

### Projects

- `POST /api/projects` - Create a new project
- `GET /api/projects` - List all projects (supports `?search=query&limit=N`)
- `GET /api/projects/{id_or_name}` - Get project by ID or name
- `PUT /api/projects/{id}` - Update project metadata
- `DELETE /api/projects/{id}` - Delete project

### Files

- `POST /api/projects/{id}/files` - Upload files (multipart/form-data)
- `GET /api/projects/{id}/files` - List project files

### Static Serving

- `GET /view/{id_or_name}/` - Serve project entry file
- `GET /view/{id_or_name}/{filepath}` - Serve specific file

### System

- `GET /api/health` - Health check

Full interactive API documentation available at `/docs` when server is running.

## 🔒 Security

- **Path Traversal Protection** - Validates all file paths
- **File Size Limits** - 50MB per upload request
- **Safe Filenames** - Rejects invalid characters and patterns
- **Incremental Updates** - Preserves files not included in upload
- **CORS Configured** - Ready for iframe embedding

**Note**: This server is designed for trusted environments. For public deployments, consider adding authentication.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Uses [nanoid](https://github.com/puyuan/py-nanoid) for short ID generation
- Package management by [uv](https://github.com/astral-sh/uv)

## 📧 Support

- 🐛 [Issue Tracker](https://github.com/yourusername/framebox/issues)
- 💬 [Discussions](https://github.com/yourusername/framebox/discussions)
- 📖 [Documentation](https://github.com/yourusername/framebox/wiki)

---

Made with ❤️ for the Markdown community
