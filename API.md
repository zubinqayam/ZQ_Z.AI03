# Contributing to ZQ KeyBox

Thank you for your interest in contributing to ZQ KeyBox! 馃帀

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/ZQ_KeyBox.git`
3. Create a feature branch: `git checkout -b feature/amazing-feature`
4. Make your changes
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

## Development Guidelines

### Code Style

- **Python**: Follow PEP 8, use `black` for formatting
- **TypeScript**: Follow ESLint rules
- **Rust**: Follow `rustfmt` conventions

### Security Requirements

- 鈿狅笍 **NEVER commit secrets or vault files**
- 鈿狅笍 **Always use encrypted storage for credentials**
- 鈿狅笍 **Add security review for crypto code changes**

### Testing

```bash
# Python tests
pytest backend/tests/

# TypeScript tests
npm test

# Security audit
python backend/keybox/security_audit.py
```

### Commit Messages

Follow conventional commits:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation
- `security:` Security improvements
- `test:` Testing

Example: `feat: add HSM support for master key storage`

## Pull Request Process

1. Update documentation
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

## Security Vulnerabilities

**DO NOT** open public issues for security vulnerabilities.

Email: zubin.qayam@outlook.com with subject "SECURITY: ZQ KeyBox"

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
