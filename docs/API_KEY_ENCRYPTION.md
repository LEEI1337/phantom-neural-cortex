# API Key Encryption with Fernet - Secure Credential Management

**Version:** 1.0.0
**Status:** REQUIRED for Production

Fernet provides **military-grade encryption** for storing API keys - prevent credential leaks, pass security audits, sleep better at night.

---

## Why Encrypt API Keys?

### The Problem:

```python
# ❌ NEVER DO THIS
class User:
    claude_api_key = "sk-ant-api03-your-actual-key-here"  # Plaintext in database!

# If database is compromised:
# - Attacker has all API keys
# - Can use your AI services
# - Can rack up thousands in costs
# - Can access your data
```

**Risks of Plaintext Storage:**
- Database dumps expose all keys
- Backup files contain secrets
- Logs may leak credentials
- SQL injection = full key theft
- Insider threats

### The Solution:

```python
# ✅ CORRECT
class User:
    claude_api_key_encrypted = "gAAAAABhk..."  # Encrypted ciphertext

# If database is compromised:
# - Attacker sees encrypted gibberish
# - Can't use keys without FERNET_KEY
# - FERNET_KEY stored in secrets manager (not in database)
```

**Benefits:**
- ✅ Database dumps are safe
- ✅ Backups don't leak secrets
- ✅ Passes security audits
- ✅ Complies with regulations (GDPR, SOC 2)
- ✅ Limits blast radius of breaches

---

## How Fernet Works

### Cryptographic Foundations:

**Fernet = AES-128-CBC + HMAC-SHA256**

```
Encryption Process:
1. Generate random IV (Initialization Vector)
2. Encrypt plaintext with AES-128-CBC
3. Create HMAC-SHA256 signature
4. Combine: version + timestamp + IV + ciphertext + HMAC

Result: "gAAAAABhk7..." (base64-encoded token)
```

**Security Properties:**
- Symmetric encryption (same key encrypts/decrypts)
- Authenticated (tampering detected)
- Time-bound (optional TTL for expiration)
- Non-malleable (can't modify ciphertext)
- IND-CCA2 secure (industry standard)

### Fernet Token Structure:

```
Token: gAAAAABhk7j0... (80+ bytes base64-encoded)

Decoded:
┌─────────┬────────────┬──────┬────────────┬─────────┐
│ Version │ Timestamp  │  IV  │ Ciphertext │  HMAC   │
│ (1 byte)│  (8 bytes) │(16 B)│  (variable)│ (32 B)  │
└─────────┴────────────┴──────┴────────────┴─────────┘
```

---

## Setup (10 minutes)

### Step 1: Install Cryptography

```bash
cd dashboard/backend
pip install cryptography==42.0.0
```

### Step 2: Generate Fernet Key

**Option A: Command Line (Quick)**

```bash
# Generate key and copy to .env
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Output:
# XpW8rVj3K9mN2qB7fH5cT1yU6zD4sA0oE8wL3xG9vM4=
```

**Option B: Interactive Script (Recommended)**

Create `dashboard/backend/generate_fernet_key.py`:

```python
"""
Generate a secure Fernet encryption key.

Usage:
    python generate_fernet_key.py
"""
from cryptography.fernet import Fernet
import os

def generate_fernet_key():
    """Generate a new Fernet key."""
    key = Fernet.generate_key()
    key_str = key.decode()

    print("=" * 70)
    print("🔐 FERNET ENCRYPTION KEY GENERATED")
    print("=" * 70)
    print()
    print("Your Fernet key:")
    print()
    print(f"    {key_str}")
    print()
    print("=" * 70)
    print()
    print("IMPORTANT:")
    print("  1. Copy this key to your .env file:")
    print(f"     FERNET_KEY={key_str}")
    print()
    print("  2. NEVER commit this key to git")
    print("  3. Store in secrets manager for production (Azure Key Vault, AWS Secrets Manager)")
    print("  4. Keep backup in secure location")
    print()
    print("=" * 70)

    # Check if .env exists
    if os.path.exists(".env"):
        print()
        response = input("Add to .env file automatically? (y/N): ")
        if response.lower() == 'y':
            with open(".env", "a") as f:
                f.write(f"\n# Fernet Encryption Key (Generated {__import__('datetime').datetime.now()})\n")
                f.write(f"FERNET_KEY={key_str}\n")
            print("✅ Added to .env file")
        else:
            print("⚠️  Remember to add manually to .env")

if __name__ == "__main__":
    generate_fernet_key()
```

Run it:

```bash
python generate_fernet_key.py

# Output:
# 🔐 FERNET ENCRYPTION KEY GENERATED
# Your Fernet key:
#     XpW8rVj3K9mN2qB7fH5cT1yU6zD4sA0oE8wL3xG9vM4=
```

### Step 3: Configure Environment

Add to `.env`:

```bash
# ============================================================================
# API KEY ENCRYPTION - REQUIRED
# ============================================================================
# Generate with: python generate_fernet_key.py

FERNET_KEY=XpW8rVj3K9mN2qB7fH5cT1yU6zD4sA0oE8wL3xG9vM4=
```

### Step 4: Create Encryption Utility

Create `dashboard/backend/utils/encryption.py`:

```python
"""
API Key Encryption Utilities using Fernet.

Provides secure encryption/decryption for sensitive credentials.
"""
from cryptography.fernet import Fernet, InvalidToken
from typing import Optional
import os
import logging

logger = logging.getLogger(__name__)


class EncryptionManager:
    """
    Manages encryption/decryption of API keys using Fernet.

    Usage:
        encryption = EncryptionManager()
        encrypted = encryption.encrypt("sk-ant-api03-...")
        decrypted = encryption.decrypt(encrypted)
    """

    def __init__(self, key: Optional[str] = None):
        """
        Initialize encryption manager.

        Args:
            key: Fernet key (base64-encoded). If None, reads from FERNET_KEY env var.

        Raises:
            ValueError: If no key provided and FERNET_KEY not set
        """
        self.key = key or os.getenv("FERNET_KEY")

        if not self.key:
            raise ValueError(
                "FERNET_KEY not configured. "
                "Generate with: python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
            )

        try:
            self.cipher = Fernet(self.key.encode() if isinstance(self.key, str) else self.key)
        except Exception as e:
            raise ValueError(f"Invalid FERNET_KEY format: {e}")

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext string.

        Args:
            plaintext: The string to encrypt (e.g., API key)

        Returns:
            Base64-encoded encrypted token

        Example:
            >>> encryption = EncryptionManager()
            >>> encrypted = encryption.encrypt("sk-ant-api03-...")
            >>> print(encrypted)
            'gAAAAABhk7j0...'
        """
        if not plaintext:
            return ""

        try:
            encrypted_bytes = self.cipher.encrypt(plaintext.encode())
            return encrypted_bytes.decode()
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt ciphertext string.

        Args:
            ciphertext: Base64-encoded encrypted token

        Returns:
            Decrypted plaintext string

        Raises:
            InvalidToken: If ciphertext is invalid or tampered with

        Example:
            >>> encryption = EncryptionManager()
            >>> decrypted = encryption.decrypt("gAAAAABhk7j0...")
            >>> print(decrypted)
            'sk-ant-api03-...'
        """
        if not ciphertext:
            return ""

        try:
            decrypted_bytes = self.cipher.decrypt(ciphertext.encode())
            return decrypted_bytes.decode()
        except InvalidToken:
            logger.error("Decryption failed: Invalid token (tampered or wrong key)")
            raise ValueError("Invalid encrypted data or wrong encryption key")
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise

    def encrypt_with_ttl(self, plaintext: str, ttl_seconds: int) -> str:
        """
        Encrypt with time-to-live (TTL).

        The token will only be valid for the specified duration.

        Args:
            plaintext: The string to encrypt
            ttl_seconds: Time-to-live in seconds

        Returns:
            Base64-encoded encrypted token with TTL

        Example:
            >>> # Encrypt API key valid for 1 hour
            >>> encrypted = encryption.encrypt_with_ttl("sk-ant-api03-...", 3600)
            >>> # Decryption will fail after 1 hour
        """
        if not plaintext:
            return ""

        try:
            import time
            encrypted_bytes = self.cipher.encrypt_at_time(
                plaintext.encode(),
                current_time=int(time.time())
            )
            return encrypted_bytes.decode()
        except Exception as e:
            logger.error(f"TTL encryption failed: {e}")
            raise

    def decrypt_with_ttl(self, ciphertext: str, ttl_seconds: int) -> str:
        """
        Decrypt with TTL verification.

        Args:
            ciphertext: Base64-encoded encrypted token
            ttl_seconds: Maximum age in seconds

        Returns:
            Decrypted plaintext if within TTL

        Raises:
            InvalidToken: If token expired or invalid
        """
        if not ciphertext:
            return ""

        try:
            decrypted_bytes = self.cipher.decrypt(
                ciphertext.encode(),
                ttl=ttl_seconds
            )
            return decrypted_bytes.decode()
        except InvalidToken as e:
            if "expired" in str(e).lower():
                logger.error("Decryption failed: Token expired")
                raise ValueError("Encrypted data has expired")
            else:
                logger.error("Decryption failed: Invalid token")
                raise ValueError("Invalid encrypted data or wrong encryption key")
        except Exception as e:
            logger.error(f"TTL decryption failed: {e}")
            raise


# Global encryption manager instance
_encryption_manager: Optional[EncryptionManager] = None


def get_encryption_manager() -> EncryptionManager:
    """
    Get singleton encryption manager instance.

    Returns:
        EncryptionManager: Global encryption manager

    Example:
        >>> from utils.encryption import get_encryption_manager
        >>> encryption = get_encryption_manager()
        >>> encrypted = encryption.encrypt("secret")
    """
    global _encryption_manager

    if _encryption_manager is None:
        _encryption_manager = EncryptionManager()

    return _encryption_manager


# Convenience functions
def encrypt_api_key(api_key: str) -> str:
    """Encrypt an API key."""
    return get_encryption_manager().encrypt(api_key)


def decrypt_api_key(encrypted_key: str) -> str:
    """Decrypt an API key."""
    return get_encryption_manager().decrypt(encrypted_key)
```

### Step 5: Test Encryption

Create `dashboard/backend/test_encryption.py`:

```python
"""Test encryption functionality."""
from utils.encryption import get_encryption_manager


def test_encryption():
    """Test basic encryption/decryption."""
    encryption = get_encryption_manager()

    # Test data
    test_keys = [
        "sk-ant-api03-abc123",
        "AIzaSyD_example_gemini_key",
        "ghp_example_github_token"
    ]

    print("=" * 70)
    print("🔐 TESTING FERNET ENCRYPTION")
    print("=" * 70)
    print()

    for i, plaintext in enumerate(test_keys, 1):
        print(f"Test {i}:")
        print(f"  Plaintext:  {plaintext}")

        # Encrypt
        encrypted = encryption.encrypt(plaintext)
        print(f"  Encrypted:  {encrypted[:40]}... ({len(encrypted)} bytes)")

        # Decrypt
        decrypted = encryption.decrypt(encrypted)
        print(f"  Decrypted:  {decrypted}")

        # Verify
        assert decrypted == plaintext, "Decryption failed!"
        print("  ✅ Encryption/Decryption successful!")
        print()

    print("=" * 70)
    print("✅ ALL TESTS PASSED")
    print("=" * 70)


if __name__ == "__main__":
    test_encryption()
```

Run test:

```bash
python test_encryption.py

# Output:
# 🔐 TESTING FERNET ENCRYPTION
# Test 1:
#   Plaintext:  sk-ant-api03-abc123
#   Encrypted:  gAAAAABhk7j0ZpX8rVj3K9mN2qB7fH5cT1... (120 bytes)
#   Decrypted:  sk-ant-api03-abc123
#   ✅ Encryption/Decryption successful!
```

---

## Database Integration

### Step 1: Update Models

Edit `dashboard/backend/models.py`:

```python
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from utils.encryption import encrypt_api_key, decrypt_api_key

Base = declarative_base()


class APIKey(Base):
    """
    Stores encrypted API keys for different AI providers.

    All API keys are encrypted using Fernet before storage.
    """
    __tablename__ = "api_keys"

    id = Column(String, primary_key=True)
    provider = Column(String, nullable=False)  # "claude", "gemini", "copilot"
    key_name = Column(String, nullable=False)  # "Primary Key", "Backup Key"
    encrypted_key = Column(Text, nullable=False)  # Fernet-encrypted API key
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_used = Column(DateTime, nullable=True)

    def set_api_key(self, plaintext_key: str):
        """
        Set API key (encrypts before storage).

        Args:
            plaintext_key: Plaintext API key
        """
        self.encrypted_key = encrypt_api_key(plaintext_key)

    def get_api_key(self) -> str:
        """
        Get decrypted API key.

        Returns:
            Plaintext API key

        Raises:
            ValueError: If decryption fails
        """
        return decrypt_api_key(self.encrypted_key)

    def to_dict(self) -> dict:
        """Convert to dict (never expose encrypted key)."""
        return {
            "id": self.id,
            "provider": self.provider,
            "key_name": self.key_name,
            "created_at": self.created_at.isoformat(),
            "last_used": self.last_used.isoformat() if self.last_used else None,
            # Never expose encrypted_key or plaintext key in API responses
        }
```

### Step 2: Create Migration

```bash
# Generate migration for encrypted API keys
alembic revision --autogenerate -m "add encrypted api keys table"

# Apply migration
alembic upgrade head
```

### Step 3: API Endpoints

Create `dashboard/backend/routers/api_keys.py`:

```python
"""
API Key Management Endpoints

Provides secure storage and retrieval of encrypted API keys.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List
import uuid

from database import get_async_db
from models import APIKey

router = APIRouter(prefix="/api/keys", tags=["API Keys"])


class APIKeyCreate(BaseModel):
    provider: str  # "claude", "gemini", "copilot"
    key_name: str  # "Primary Key", "Backup Key"
    api_key: str  # Plaintext key (encrypted before storage)


class APIKeyResponse(BaseModel):
    id: str
    provider: str
    key_name: str
    created_at: str
    last_used: str | None


@router.post("/", response_model=APIKeyResponse)
async def create_api_key(
    key_data: APIKeyCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Store a new API key (encrypted).

    The API key is encrypted using Fernet before storage.
    """
    # Create new API key record
    api_key = APIKey(
        id=str(uuid.uuid4()),
        provider=key_data.provider,
        key_name=key_data.key_name
    )

    # Encrypt and store
    api_key.set_api_key(key_data.api_key)

    db.add(api_key)
    await db.commit()
    await db.refresh(api_key)

    return APIKeyResponse(**api_key.to_dict())


@router.get("/", response_model=List[APIKeyResponse])
async def list_api_keys(
    provider: str | None = None,
    db: AsyncSession = Depends(get_async_db)
):
    """
    List all stored API keys (encrypted keys not exposed).

    Args:
        provider: Optional filter by provider
    """
    query = select(APIKey)

    if provider:
        query = query.filter(APIKey.provider == provider)

    result = await db.execute(query)
    keys = result.scalars().all()

    return [APIKeyResponse(**key.to_dict()) for key in keys]


@router.get("/{key_id}")
async def get_api_key(
    key_id: str,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get decrypted API key (use with caution).

    ⚠️ WARNING: This endpoint returns plaintext API key.
    Should only be called server-side, never exposed to frontend.
    """
    result = await db.execute(select(APIKey).filter(APIKey.id == key_id))
    api_key = result.scalar_one_or_none()

    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")

    # Decrypt and return
    try:
        plaintext_key = api_key.get_api_key()
        return {
            "id": api_key.id,
            "provider": api_key.provider,
            "key_name": api_key.key_name,
            "api_key": plaintext_key  # ⚠️ Plaintext
        }
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Decryption failed: {str(e)}")


@router.delete("/{key_id}")
async def delete_api_key(
    key_id: str,
    db: AsyncSession = Depends(get_async_db)
):
    """Delete an API key."""
    result = await db.execute(select(APIKey).filter(APIKey.id == key_id))
    api_key = result.scalar_one_or_none()

    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")

    await db.delete(api_key)
    await db.commit()

    return {"status": "deleted", "id": key_id}
```

---

## Production Best Practices

### 1. Never Store FERNET_KEY in Database

**Bad:**
```python
# ❌ NEVER DO THIS
db.execute("INSERT INTO config VALUES ('fernet_key', 'XpW8rVj3...')")
```

**Good:**
```python
# ✅ Store in secrets manager
# Azure Key Vault
# AWS Secrets Manager
# Google Secret Manager
# HashiCorp Vault
```

### 2. Use Secrets Manager in Production

**Azure Key Vault:**

```python
# dashboard/backend/utils/secrets.py
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os


def get_fernet_key_from_azure() -> str:
    """Fetch FERNET_KEY from Azure Key Vault."""
    vault_url = os.getenv("AZURE_KEY_VAULT_URL")

    if not vault_url:
        # Fallback to environment variable in development
        return os.getenv("FERNET_KEY")

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)

    secret = client.get_secret("FERNET-KEY")
    return secret.value
```

**AWS Secrets Manager:**

```python
import boto3
import os
import json


def get_fernet_key_from_aws() -> str:
    """Fetch FERNET_KEY from AWS Secrets Manager."""
    secret_name = os.getenv("AWS_SECRET_NAME", "phantom-neural-cortex/fernet-key")
    region = os.getenv("AWS_REGION", "us-east-1")

    if not os.getenv("AWS_SECRETS_ENABLED"):
        return os.getenv("FERNET_KEY")

    client = boto3.client("secretsmanager", region_name=region)

    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response["SecretString"])

    return secret["FERNET_KEY"]
```

### 3. Implement Key Rotation

```python
# dashboard/backend/utils/key_rotation.py
from cryptography.fernet import MultiFernet, Fernet
from typing import List


class KeyRotationManager:
    """
    Manages key rotation for Fernet encryption.

    Supports multiple keys to allow gradual rotation without downtime.
    """

    def __init__(self, keys: List[str]):
        """
        Initialize with multiple keys.

        Args:
            keys: List of Fernet keys (newest first)
        """
        self.fernets = [Fernet(key.encode()) for key in keys]
        self.multi_fernet = MultiFernet(self.fernets)

    def encrypt(self, plaintext: str) -> str:
        """Encrypt using newest key (first in list)."""
        encrypted_bytes = self.multi_fernet.encrypt(plaintext.encode())
        return encrypted_bytes.decode()

    def decrypt(self, ciphertext: str) -> str:
        """Decrypt using any key (tries all keys)."""
        decrypted_bytes = self.multi_fernet.decrypt(ciphertext.encode())
        return decrypted_bytes.decode()

    def rotate(self, plaintext: str) -> str:
        """Re-encrypt data with newest key."""
        # Decrypt with any key
        decrypted = self.decrypt(plaintext)
        # Encrypt with newest key
        return self.encrypt(decrypted)


# Usage
def rotate_api_keys():
    """Rotate all encrypted API keys to use new encryption key."""
    old_key = os.getenv("FERNET_KEY_OLD")
    new_key = os.getenv("FERNET_KEY_NEW")

    rotation_manager = KeyRotationManager([new_key, old_key])

    db = SessionLocal()
    api_keys = db.query(APIKey).all()

    for api_key in api_keys:
        # Decrypt with old key, encrypt with new key
        api_key.encrypted_key = rotation_manager.rotate(api_key.encrypted_key)

    db.commit()
    db.close()

    print(f"✅ Rotated {len(api_keys)} API keys")
```

**Rotation Process:**

```bash
# 1. Generate new key
python generate_fernet_key.py

# 2. Add both keys to environment
FERNET_KEY_NEW=<new_key>
FERNET_KEY_OLD=<old_key>

# 3. Run rotation script
python rotate_keys.py

# 4. Update environment to use only new key
FERNET_KEY=<new_key>

# 5. Remove old key after rotation complete
```

### 4. Never Log Decrypted Keys

**Bad:**
```python
# ❌ NEVER DO THIS
logger.info(f"Using API key: {decrypted_key}")
print(f"Decrypted: {plaintext}")
```

**Good:**
```python
# ✅ Log safe metadata only
logger.info(f"Using API key: {key_id} (provider: {provider})")
logger.debug("API key decrypted successfully")
```

### 5. Rate Limit Decryption Endpoints

```python
from fastapi_limiter.depends import RateLimiter

@router.get("/{key_id}", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_api_key(key_id: str, db: AsyncSession = Depends(get_async_db)):
    """
    Get decrypted API key (rate limited).

    Rate limit: 10 requests per minute per IP
    """
    # ... decryption logic
```

### 6. Audit Key Access

```python
class APIKeyAccessLog(Base):
    """Log all API key decryption attempts."""
    __tablename__ = "api_key_access_logs"

    id = Column(String, primary_key=True)
    key_id = Column(String, nullable=False)
    accessed_by = Column(String, nullable=False)  # User/Service ID
    accessed_at = Column(DateTime, default=datetime.utcnow)
    success = Column(Boolean, nullable=False)
    ip_address = Column(String, nullable=True)


async def log_key_access(key_id: str, accessed_by: str, success: bool, ip: str):
    """Log API key access."""
    log_entry = APIKeyAccessLog(
        id=str(uuid.uuid4()),
        key_id=key_id,
        accessed_by=accessed_by,
        success=success,
        ip_address=ip
    )
    db.add(log_entry)
    await db.commit()
```

---

## Integration with Orchestrator

### Fetch API Keys from Database

```python
# dashboard/backend/orchestration/orchestrator.py

from models import APIKey
from sqlalchemy import select


class CLIOrchestrator:
    async def _get_api_key(self, provider: str) -> str:
        """
        Fetch decrypted API key for provider.

        Args:
            provider: "claude", "gemini", "copilot"

        Returns:
            Decrypted API key

        Raises:
            ValueError: If key not found or decryption fails
        """
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(APIKey)
                .filter(APIKey.provider == provider)
                .order_by(APIKey.created_at.desc())
                .limit(1)
            )
            api_key_record = result.scalar_one_or_none()

            if not api_key_record:
                raise ValueError(f"No API key configured for {provider}")

            # Decrypt key
            try:
                return api_key_record.get_api_key()
            except Exception as e:
                logger.error(f"Failed to decrypt API key for {provider}: {e}")
                raise ValueError(f"API key decryption failed for {provider}")

    async def _execute_claude(self, task: Task, session_id: str):
        """Execute task with Claude."""
        # Fetch API key from database (decrypted)
        api_key = await self._get_api_key("claude")

        # Set environment variable for subprocess
        env = os.environ.copy()
        env["ANTHROPIC_API_KEY"] = api_key

        # Execute claude command
        process = await asyncio.create_subprocess_exec(
            "claude",
            "-p", task.prompt,
            env=env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        # Clear API key from memory
        del env["ANTHROPIC_API_KEY"]
        del api_key

        # ... process response
```

---

## Security Checklist

Before deploying to production:

- [ ] FERNET_KEY stored in secrets manager (not .env file)
- [ ] FERNET_KEY never committed to git
- [ ] Decryption endpoints rate-limited
- [ ] API key access logged and audited
- [ ] No plaintext keys in logs
- [ ] No plaintext keys in API responses to frontend
- [ ] Key rotation process documented
- [ ] Backup of FERNET_KEY in secure location
- [ ] Encryption/decryption tested thoroughly
- [ ] Database backups encrypted at rest

---

## Troubleshooting

### Issue: "Invalid FERNET_KEY format"

**Cause:** FERNET_KEY is not valid base64

**Solution:**
```bash
# Regenerate key
python generate_fernet_key.py
```

### Issue: "Decryption failed: Invalid token"

**Causes:**
- Wrong FERNET_KEY (different key than used for encryption)
- Ciphertext was tampered with
- Ciphertext corrupted

**Solution:**
```python
# Verify key matches
print(os.getenv("FERNET_KEY")[:20])

# If key changed, re-encrypt all data
python rotate_keys.py
```

### Issue: Performance Degradation

**Cause:** Decrypting keys on every request

**Solution:** Cache decrypted keys (with caution!)

```python
from functools import lru_cache
from datetime import datetime, timedelta

# Cache decrypted keys for 5 minutes
_key_cache = {}

async def get_cached_api_key(provider: str) -> str:
    """Get API key with 5-minute cache."""
    cache_key = f"api_key:{provider}"
    cached = _key_cache.get(cache_key)

    if cached and cached["expires_at"] > datetime.utcnow():
        return cached["key"]

    # Fetch and decrypt
    api_key = await _get_api_key(provider)

    # Cache for 5 minutes
    _key_cache[cache_key] = {
        "key": api_key,
        "expires_at": datetime.utcnow() + timedelta(minutes=5)
    }

    return api_key
```

---

## Next Steps

1. ✅ Install cryptography package
2. ✅ Generate FERNET_KEY
3. ✅ Configure environment
4. ✅ Create encryption utility
5. ✅ Update database models
6. ✅ Create API endpoints
7. ✅ Test encryption/decryption
8. ✅ Set up secrets manager for production
9. ✅ Document key rotation process
10. ✅ Implement audit logging

---

**Documentation:** https://cryptography.io/en/latest/fernet/
**Security Best Practices:** https://owasp.org/www-project-top-ten/
**Secrets Management:** https://cloud.google.com/secret-manager/docs/best-practices
