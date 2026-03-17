
import os
import zipfile
from datetime import datetime

base_dir = "ZQ_KeyBox_V1.11"

# Create requirements.txt
requirements_content = """# ZQ KeyBox V1.11 - Python Dependencies

# Core Security
cryptography==41.0.7
filelock==3.13.1

# Backend Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3

# Database & Storage
python-dotenv==1.0.0

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3
pytest-cov==4.1.0

# Development
black==24.1.1
flake8==7.0.0
mypy==1.8.0
"""

with open(f"{base_dir}/requirements.txt", "w") as f:
    f.write(requirements_content)

# Create package.json
package_json_content = """{
  "name": "zq-keybox",
  "version": "1.11.0",
  "description": "Secure Key Management System for ZQ NodeDR",
  "author": "Zubin Qayam <zubin.qayam@outlook.com>",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/zubinqayam/ZQ_KeyBox.git"
  },
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "tauri": "tauri",
    "tauri:dev": "tauri dev",
    "tauri:build": "tauri build",
    "test": "vitest",
    "lint": "eslint src --ext ts,tsx"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@tauri-apps/api": "^1.5.3",
    "lucide-react": "^0.303.0"
  },
  "devDependencies": {
    "@tauri-apps/cli": "^1.5.9",
    "@types/react": "^18.2.48",
    "@types/react-dom": "^18.2.18",
    "@vitejs/plugin-react": "^4.2.1",
    "typescript": "^5.3.3",
    "vite": "^5.0.11",
    "vitest": "^1.2.0"
  }
}
"""

with open(f"{base_dir}/package.json", "w") as f:
    f.write(package_json_content)

# Create .gitignore
gitignore_content = """# KeyBox Vault (NEVER COMMIT SECRETS!)
keybox_vault/
*.key
password.json
keybox_audit.log

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
venv/
env/
ENV/

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Tauri
src-tauri/target/
src-tauri/Cargo.lock

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
htmlcov/
.pytest_cache/

# Environment
.env
.env.local
"""

with open(f"{base_dir}/.gitignore", "w") as f:
    f.write(gitignore_content)

# Create LICENSE
license_content = """MIT License

Copyright (c) 2025 Zubin Qayam | ZQ AI LOGIC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

with open(f"{base_dir}/LICENSE", "w") as f:
    f.write(license_content)

# Create CONTRIBUTING.md
contributing_content = """# Contributing to ZQ KeyBox

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
"""

with open(f"{base_dir}/CONTRIBUTING.md", "w") as f:
    f.write(contributing_content)

print("鉁� Created requirements.txt")
print("鉁� Created package.json")
print("鉁� Created .gitignore")
print("鉁� Created LICENSE")
print("鉁� Created CONTRIBUTING.md")
