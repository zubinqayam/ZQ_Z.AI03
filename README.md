# ZQ KeyBox V1.11 - Integration Guide

## Integrating with ZQ NodeDR

### Quick Start

```typescript
// src/services/keybox.service.ts
import { invoke } from '@tauri-apps/api';

class KeyBoxService {
  async authenticate(password: string): Promise<boolean> {
    return await invoke<boolean>('verify_password', { password });
  }

  async addKey(keyName: string, program: string, value: string) {
    return await invoke<string>('add_key', {
      keyName,
      programName: program,
      keyValue: value
    });
  }

  async getKey(lockerId: string): Promise<string | null> {
    return await invoke<string>('get_key', { lockerId });
  }
}

export const keybox = new KeyBoxService();
```

---

## Integration Patterns

### 1. ZQ Agents Integration

```python
# backend/agents/openai_agent.py
from backend.keybox.secure_manager import SecureZQKeyBox

class OpenAIAgent:
    def __init__(self):
        self.keybox = SecureZQKeyBox()
        self.api_key = None

    def initialize(self, locker_id: str):
        self.api_key = self.keybox.get_key(locker_id)
        if not self.api_key:
            raise ValueError(f"Key not found: {locker_id}")

    def chat(self, prompt: str):
        # Use self.api_key to call OpenAI API
        ...
```

---

### 2. Configuration Management

```typescript
// src/config/keybox.config.ts
export const KEYBOX_CONFIG = {
  programs: {
    ZQ_AGENTS: {
      keys: ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY'],
      required: true
    },
    ZQ_TASKMASTER: {
      keys: ['NOTION_API_KEY'],
      required: false
    },
    ZQ_CONNECTER: {
      keys: ['GITHUB_TOKEN', 'LINEAR_TOKEN'],
      required: true
    }
  }
};
```

---

### 3. Initialization Flow

```typescript
// src/main.tsx
import { keybox } from './services/keybox.service';

async function initializeApp() {
  // 1. Authenticate user
  const password = await promptPassword();
  const authenticated = await keybox.authenticate(password);

  if (!authenticated) {
    throw new Error('Authentication failed');
  }

  // 2. Load required keys
  const lockers = await keybox.listLockers();

  // 3. Initialize agents
  for (const locker of lockers) {
    if (locker.program_name === 'ZQ_AGENTS') {
      await initializeAgent(locker.locker_id);
    }
  }

  // 4. Start application
  startApp();
}
```

---

## Backend Integration

### FastAPI Integration

```python
# backend/api/keybox_router.py
from fastapi import APIRouter, HTTPException, Depends
from backend.keybox.secure_manager import SecureZQKeyBox
from pydantic import BaseModel

router = APIRouter(prefix="/api/keybox")
keybox = SecureZQKeyBox()

class AddKeyRequest(BaseModel):
    key_name: str
    program_name: str
    key_value: str

@router.post("/add")
async def add_key(req: AddKeyRequest, user=Depends(verify_admin)):
    locker_id = keybox.add_key(
        req.key_name,
        req.program_name,
        req.key_value
    )
    return {"locker_id": locker_id}

@router.get("/list")
async def list_lockers(user=Depends(verify_admin)):
    return {"lockers": keybox.list_lockers()}
```

---

### Environment Variables

```bash
# .env
KEYBOX_MASTER_KEY=base64_encoded_key_here
KEYBOX_VAULT_PATH=/secure/path/to/vault
KEYBOX_AUDIT_LOG=/var/log/keybox_audit.log
```

---

## UI Integration

### React Component

```tsx
// src/components/KeyBoxManager.tsx
import React, { useState, useEffect } from 'react';
import { keybox } from '../services/keybox.service';

export const KeyBoxManager: React.FC = () => {
  const [lockers, setLockers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadKeys();
  }, []);

  const loadKeys = async () => {
    try {
      const data = await keybox.listLockers();
      setLockers(data);
    } catch (error) {
      console.error('Failed to load keys:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="keybox-manager">
      {loading ? (
        <p>Loading keys...</p>
      ) : (
        <KeyList lockers={lockers} onRefresh={loadKeys} />
      )}
    </div>
  );
};
```

---

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy with KeyBox

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup KeyBox
        env:
          KEYBOX_MASTER_KEY: ${{ secrets.KEYBOX_MASTER_KEY }}
        run: |
          pip install -r requirements.txt
          python backend/keybox/setup.py

      - name: Deploy
        run: |
          npm run build
          npm run deploy
```

---

## Docker Integration

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Create vault directory
RUN mkdir -p /app/keybox_vault &&     chmod 700 /app/keybox_vault

# Set environment
ENV KEYBOX_MASTER_KEY=${KEYBOX_MASTER_KEY}
ENV KEYBOX_VAULT_PATH=/app/keybox_vault

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Testing Integration

```python
# tests/test_keybox_integration.py
import pytest
from backend.keybox.secure_manager import SecureZQKeyBox

@pytest.fixture
def keybox():
    kb = SecureZQKeyBox(vault_path="test_vault")
    yield kb
    # Cleanup
    import shutil
    shutil.rmtree("test_vault")

def test_add_and_retrieve_key(keybox):
    locker_id = keybox.add_key(
        "Test Key",
        "TEST_PROGRAM",
        "secret_value_123"
    )

    retrieved = keybox.get_key(locker_id)
    assert retrieved == "secret_value_123"

def test_password_verification(keybox):
    assert keybox.verify_password("00000")  # Default
    assert not keybox.verify_password("wrong")
```

---

## Troubleshooting

### Common Issues

**Issue:** "Master key not found"
```bash
# Solution: Generate new master key
export KEYBOX_MASTER_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
```

**Issue:** "Permission denied on vault files"
```bash
# Solution: Fix permissions
chmod 700 keybox_vault
chmod 600 keybox_vault/*.key
```

**Issue:** "Decryption failed"
```bash
# Solution: Check master key integrity
python backend/keybox/cli.py verify-master-key
```

---

For more information:
- [API Reference](API.md)
- [Security Guide](SECURITY.md)
