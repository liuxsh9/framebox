# Contributing to iframe-server

Thank you for your interest in contributing to iframe-server! This document provides guidelines and instructions for contributing.

## 🚀 Getting Started

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub
   git clone https://github.com/yourusername/iframe-server.git
   cd iframe-server
   ```

2. **Set up development environment**
   ```bash
   # Install uv
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install dependencies
   uv pip install -e .

   # Copy environment template
   cp .env.example .env
   ```

3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🧪 Testing

Before submitting a PR, ensure all tests pass:

```bash
# Start the server
uv run python main.py &

# Run the test suite
./test.sh

# Stop the server
pkill -f "uv run python"
```

## 📝 Code Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and modular

## 🔍 Pull Request Process

1. **Update documentation** if you're adding new features
2. **Add tests** for new functionality
3. **Ensure all tests pass** before submitting
4. **Update README.md** if needed
5. **Write clear commit messages**:
   ```
   feat: Add user authentication
   fix: Resolve CORS header issue
   docs: Update API examples
   test: Add file upload tests
   ```

## 🐛 Bug Reports

When filing a bug report, please include:

- **Description**: Clear description of the issue
- **Steps to Reproduce**: Detailed steps to reproduce the behavior
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: OS, Python version, browser (if UI related)
- **Logs**: Relevant error messages or logs

## 💡 Feature Requests

We welcome feature requests! Please include:

- **Use Case**: Why is this feature needed?
- **Proposed Solution**: How should it work?
- **Alternatives**: Other approaches you've considered
- **Additional Context**: Any other relevant information

## 📋 Project Structure

```
iframe-server/
├── app/                 # Core application
│   ├── api/            # API route handlers
│   ├── utils/          # Utility functions
│   ├── config.py       # Configuration
│   ├── database.py     # Database operations
│   └── models.py       # Data models
├── static/             # Web UI files
├── tests/              # Test files (future)
└── docs/               # Documentation (future)
```

## 🎯 Areas for Contribution

We'd love help with:

- **Testing**: Expand test coverage
- **Documentation**: Improve guides and examples
- **UI/UX**: Enhance the web interface
- **Performance**: Optimize database queries and file operations
- **Security**: Audit and improve security measures
- **Docker**: Add Docker and docker-compose support
- **Authentication**: Add optional authentication layer
- **Internationalization**: Add multi-language support

## 📜 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Keep discussions on-topic and professional

## 📧 Questions?

- Open an [Issue](https://github.com/yourusername/iframe-server/issues) for bugs
- Start a [Discussion](https://github.com/yourusername/iframe-server/discussions) for questions
- Check existing issues before creating new ones

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to iframe-server! 🎉
