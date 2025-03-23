# Contributing to Wallgen

Thank you for your interest in contributing to Wallgen! This document provides guidelines and instructions to help you contribute effectively to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Contribution Workflow](#contribution-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Communication](#communication)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone. Please:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** to your local machine
3. **Set up the development environment** as described below
4. **Create a new branch** for your feature or bug fix
5. **Make your changes** following our coding standards
6. **Test your changes** thoroughly
7. **Submit a pull request** with a clear description of the changes

## Development Environment

### Prerequisites

- Python 3.8 or higher
- Git
- UV package manager (recommended) or pip

### Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/wallgen.git
cd wallgen

# Set up virtual environment
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows

# Install dependencies
uv pip install -r requirements.txt

# Install development dependencies
uv pip install -r requirements-dev.txt
```

### Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests/test_wallpaper_generator.py
```

## Contribution Workflow

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│               │     │               │     │               │
│  Fork Repo    │────>│  Create Issue │────>│Create Branch  │
│               │     │               │     │               │
└───────────────┘     └───────────────┘     └───────────────┘
        │                                           │
        │                                           ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│               │     │               │     │               │
│ Submit PR     │<────│  Run Tests    │<────│ Make Changes  │
│               │     │               │     │               │
└───────────────┘     └───────────────┘     └───────────────┘
        │
        ▼
┌───────────────┐     ┌───────────────┐
│               │     │               │
│ Address Review│────>│  PR Merged    │
│               │     │               │
└───────────────┘     └───────────────┘
```

1. **Create an issue** describing the feature/bug before starting work
2. **Create a new branch** with a descriptive name:
   - Feature: `feature/your-feature-name`
   - Bug fix: `fix/issue-description`
   - Documentation: `docs/what-you-documented`
3. **Make your changes** in small, logical commits
4. **Test your changes** thoroughly
5. **Push your branch** and submit a pull request
6. **Respond to feedback** and make necessary adjustments

## Coding Standards

We follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code. Additionally:

### Style Guidelines

- Use 4 spaces for indentation (not tabs)
- Maximum line length of 100 characters
- Use meaningful variable and function names
- Add docstrings to all functions, classes, and modules
- Use type hints where appropriate
- Follow the existing code style when making changes

### Code Quality Tools

We use several tools to ensure code quality:

- **Black**: Code formatter
- **isort**: Import sorter
- **flake8**: Style guide enforcer
- **mypy**: Type checker

Run these tools before submitting a pull request:

```bash
# Format code
black .

# Sort imports
isort .

# Check style
flake8

# Check types
mypy .
```

## Testing Guidelines

- Write tests for all new features and bug fixes
- Ensure all tests pass before submitting a pull request
- Aim for high test coverage
- Use descriptive test names (test_what_it_does_when_condition)
- Keep tests independent and isolated

## Documentation

- Update documentation for any API changes
- Add docstrings to all public functions, classes, and modules
- Follow the documentation template and formatting guidelines
- Include code examples where appropriate
- Make sure all links are valid
- Check spelling and grammar

## Pull Request Process

1. **Update the README.md** if needed with details of changes
2. **Update the CHANGELOG.md** with details of changes
3. **Verify that all CI checks pass**
4. **Fill out the PR template** completely
5. **Request review** from maintainers
6. **Address all review comments**
7. **Ensure your PR branch is up-to-date** with the main branch before merging

### PR Template

When creating a pull request, please include:

- **Title**: Clear and descriptive
- **Description**: What the PR does
- **Related Issue**: Link to the issue it addresses
- **Type of Change**: (Bug fix, feature, documentation, etc.)
- **Testing**: How you tested your changes
- **Screenshots**: If applicable
- **Checklist**: Confirmation of completed items

## Communication

- **Issues**: Use for bugs, feature requests, and discussions
- **Pull Requests**: Use for code contributions
- **Discussions**: Use for general questions and ideas

---

Thank you for contributing to Wallgen! Your time and expertise help make this project better for everyone.

<div align="center">
<img src="asset/logo/gemini.svg" alt="Logo" width="64" height="64">

Documentation last updated: 2024-03-24
</div> 