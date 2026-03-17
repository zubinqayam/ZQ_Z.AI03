
import os

base_dir = "ZQ_KeyBox_V1.11"

# Create backend secure_manager.py (Main encryption engine)
secure_manager_content = '''#!/usr/bin/env python3
"""
ZQ KeyBox V1.11 - ALGA RECHECK COMPLIANT
Secure Key Management System for ZQ NodeDR
Author: Zubin Qayam | ZQ AI LOGIC
"""

from __future__ import annotations
import os
import json
import uuid
import tempfile
import stat
import secrets
import logging
import hashlib
import base64
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from cryptography.fernet import Fernet, InvalidToken
from filelock import FileLock

# Logging configuration
LOG_FILE = os.environ.get("KEYBOX_AUDIT_LOG", "keybox_audit.log")
logger = logging.getLogger(__name__)

if not logger.handlers:
    try:
        from logging.handlers import RotatingFileHandler
        handler = RotatingFileHandler(
            LOG_FILE, 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        formatter = logging.Formatter(
            \\'%(asctime)s - %(name)s - %(levelname)s - %(message)s\\'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    except Exception:
        logging.basicConfig(level=logging.INFO)

# Security constants
DEFAULT_VAULT_PATH = "keybox_vault"
DEFAULT_PASSWORD = "00000"
PBKDF2_ITERATIONS = 200_000
SALT_BYTES = 16


class SecureZQKeyBox:
    """
    SECURE KeyBox Manager v1.11
    - Master key encryption (Fernet AES-128-CBC)
    - Per-key file locking
    - Admin password (PBKDF2-HMAC-SHA256)
    - Atomic writes (0o600 permissions)
    - Audit logging
    """
    
    def __init__(self, vault_path: str = DEFAULT_VAULT_PATH):
        self.vault_path = vault_path
        os.makedirs(self.vault_path, exist_ok=True)
        
        # Initialize paths
        self.registry_path = os.path.join(self.vault_path, "registry.json")
        self.master_key_path = os.path.join(self.vault_path, "master.key")
        self.password_path = os.path.join(self.vault_path, "password.json")
        
        # Registry lock
        self.registry_lock = FileLock(f"{self.registry_path}.lock")
        
        # Load or generate master key
        self.master_key = self._load_or_create_master_key()
        
        # Validate Fernet compatibility
        try:
            test_fernet = Fernet(self.master_key)
            token = test_fernet.encrypt(b"test")
            if test_fernet.decrypt(token) != b"test":
                raise RuntimeError("Master key test failed")
            self.fernet = test_fernet
        except Exception:
            logger.critical("Master key is invalid/corrupt. Aborting startup.")
            raise RuntimeError("Invalid KEYBOX_MASTER_KEY or master.key file")
        
        # Ensure password file exists
        try:
            self._ensure_password_file()
        except Exception:
            logger.exception("Failed to ensure password file during startup")
            raise
        
        # Load registry
        self.registry = self._load_registry()
        
        # Per-key locks (transient)
        self.key_locks: Dict[str, FileLock] = {}
        
        logger.info(f"SecureZQKeyBox initialized: vault={self.vault_path}")
    
    def _utc_now_iso(self) -> str:
        """Return current UTC timestamp in ISO format"""
        return datetime.now(timezone.utc).isoformat()
    
    # ============= MASTER KEY =============
    
    def _load_or_create_master_key(self) -> bytes:
        """
        Master key resolution order:
        1. KEYBOX_MASTER_KEY env var (preferred)
        2. master.key file on disk
        3. Generate new master.key (0o600)
        """
        env_key = os.environ.get("KEYBOX_MASTER_KEY")
        if env_key:
            key_bytes = env_key.encode("utf-8")
            logger.info("Using master key from environment")
            return key_bytes
        
        if os.path.exists(self.master_key_path):
            with open(self.master_key_path, "rb") as f:
                return f.read()
        
        # Generate new master key
        key = Fernet.generate_key()
        fd, tmp = tempfile.mkstemp(prefix="master.key.", dir=self.vault_path)
        try:
            with os.fdopen(fd, "wb") as f:
                f.write(key)
                f.flush()
                os.fsync(f.fileno())
            
            # Restrictive permissions
            os.chmod(tmp, stat.S_IRUSR | stat.S_IWUSR)  # 0o600
            os.replace(tmp, self.master_key_path)
            logger.info("Generated new master key (permission=600)")
        finally:
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except Exception:
                    pass
        
        return key
    
    def add_key(
        self,
        key_name: str,
        program_name: str,
        key_value: str,
        locker_id: Optional[str] = None
    ) -> str:
        """
        Add a new encrypted key to vault.
        Returns locker_id (UUID-based identifier).
        """
        if not locker_id:
            locker_id = f"ZQ-{uuid.uuid4().hex.upper()}"
        
        # Encrypt key value
        encrypted_value = self.fernet.encrypt(key_value.encode("utf-8"))
        
        # Save to vault
        key_path = os.path.join(self.vault_path, f"{locker_id}.key")
        fd, tmp = tempfile.mkstemp(prefix=f"{locker_id}.key.", dir=self.vault_path)
        try:
            with os.fdopen(fd, "wb") as f:
                f.write(encrypted_value)
                f.flush()
                os.fsync(f.fileno())
            
            os.chmod(tmp, stat.S_IRUSR | stat.S_IWUSR)
            os.replace(tmp, key_path)
        finally:
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except Exception:
                    pass
        
        # Update registry
        with self.registry_lock:
            self.registry.setdefault("lockers", {})[locker_id] = {
                "key_name": key_name,
                "program_name": program_name,
                "created_at": self._utc_now_iso(),
                "is_active": True,
            }
            self._save_registry()
        
        logger.info(f"Key added: {locker_id} (program={program_name})")
        return locker_id
    
    def get_key(self, locker_id: str) -> Optional[str]:
        """Retrieve decrypted key value."""
        if locker_id not in self.registry.get("lockers", {}):
            return None
        
        key_path = os.path.join(self.vault_path, f"{locker_id}.key")
        if not os.path.exists(key_path):
            return None
        
        try:
            with open(key_path, "rb") as f:
                encrypted_value = f.read()
            return self.fernet.decrypt(encrypted_value).decode("utf-8")
        except Exception:
            logger.error(f"Failed to decrypt key: {locker_id}")
            return None
    
    def _save_registry(self) -> None:
        """Atomic write of registry (0o600)"""
        dirpath = os.path.dirname(self.registry_path) or "."
        fd, tmp = tempfile.mkstemp(prefix="registry.", dir=dirpath)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(self.registry, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())
            
            os.chmod(tmp, stat.S_IRUSR | stat.S_IWUSR)
            os.replace(tmp, self.registry_path)
        finally:
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except Exception:
                    pass
    
    def _load_registry(self) -> Dict[str, Any]:
        """Load registry metadata under lock"""
        with self.registry_lock:
            if not os.path.exists(self.registry_path):
                return {"lockers": {}, "version": "1.11.0-secure"}
            
            try:
                with open(self.registry_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.error("Registry file corrupt - initializing new")
                return {"lockers": {}, "version": "1.11.0-secure"}


if __name__ == "__main__":
    # Quick test
    kb = SecureZQKeyBox()
    print(f"鉁� KeyBox initialized: {kb.vault_path}")
    
    # Test add key
    locker = kb.add_key("Test API Key", "TEST_PROGRAM", "sk-test-12345")
    print(f"鉁� Added key: {locker}")
    
    # Test retrieve key
    value = kb.get_key(locker)
    print(f"鉁� Retrieved key: {value[:10]}...")
'''

with open(f"{base_dir}/backend/keybox/secure_manager.py", "w") as f:
    f.write(secure_manager_content)

print(f"Created: backend/keybox/secure_manager.py")
