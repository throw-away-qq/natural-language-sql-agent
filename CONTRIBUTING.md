# Contributing to Natural Language SQL Agent

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the Issues section
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - System information (OS, Python version)

### Submitting Changes

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test thoroughly
5. Commit with clear messages: `git commit -m "Add feature: description"`
6. Push to your fork: `git push origin feature/your-feature-name`
7. Create a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use descriptive variable names
- Add docstrings to functions
- Comment complex logic
- Keep functions focused and small

### Testing

Before submitting:

- Test with multiple question types
- Verify both notebook and Streamlit app work
- Check for SQL injection vulnerabilities
- Ensure error handling works properly

## Areas for Contribution

### High Priority
- Support for additional database types (PostgreSQL, MySQL)
- Improved error messages
- Query result caching
- Multi-language support

### Medium Priority
- Unit tests
- Better prompt templates
- Performance optimization
- Query history feature

### Low Priority
- UI/UX improvements
- Additional example notebooks
- Documentation enhancements
- Video tutorials

## Development Setup

1. Clone your fork:
```bash
git clone https://github.com/YOUR-USERNAME/natural-language-sql-agent.git
```

2. Install development dependencies:
```bash
pip install -r requirements.txt
pip install pytest black flake8  # For testing and linting
```

3. Create a branch:
```bash
git checkout -b feature/your-feature
```

## Pull Request Guidelines

- Keep PRs focused on a single feature or fix
- Update documentation if needed
- Add tests for new features
- Ensure all tests pass
- Update CHANGELOG.md (if exists)

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on the code, not the person

## Questions?

Open an issue with the "question" label, and we'll help you out.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
