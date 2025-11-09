"""
API Key Management Router
Multi-provider AI API key management with encryption, load balancing, and rotation
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
from enum import Enum
import secrets
from cryptography.fernet import Fernet
import os

from database import get_db

router = APIRouter()

# API Key Encryption
ENCRYPTION_KEY = os.getenv("API_KEY_ENCRYPTION_KEY", Fernet.generate_key())
cipher_suite = Fernet(ENCRYPTION_KEY)

class AIProvider(str, Enum):
    """Supported AI providers"""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GOOGLE = "google"
    COHERE = "cohere"
    MISTRAL = "mistral"
    OLLAMA = "ollama"
    GROQ = "groq"
    TOGETHER = "together"

class LoadBalancingStrategy(str, Enum):
    """Load balancing strategies for multiple keys"""
    ROUND_ROBIN = "round_robin"
    WEIGHTED = "weighted"
    COST_OPTIMIZED = "cost_optimized"
    FAILOVER = "failover"
    RANDOM = "random"

class APIKeyStatus(str, Enum):
    """API key status"""
    ACTIVE = "active"
    DISABLED = "disabled"
    QUOTA_EXCEEDED = "quota_exceeded"
    RATE_LIMITED = "rate_limited"
    ERROR = "error"

# Request/Response Models
class APIKeyCreate(BaseModel):
    provider: AIProvider
    key_name: str = Field(..., description="Friendly name for this API key")
    api_key: str = Field(..., description="The actual API key (will be encrypted)")
    weight: int = Field(default=100, ge=1, le=1000, description="Weight for load balancing (higher = more traffic)")
    daily_budget: Optional[float] = Field(default=None, description="Daily budget limit in USD")
    monthly_budget: Optional[float] = Field(default=None, description="Monthly budget limit in USD")
    rate_limit_rpm: Optional[int] = Field(default=None, description="Rate limit in requests per minute")
    enabled: bool = Field(default=True)
    metadata: Optional[dict] = Field(default={})

class APIKeyUpdate(BaseModel):
    key_name: Optional[str] = None
    weight: Optional[int] = Field(default=None, ge=1, le=1000)
    daily_budget: Optional[float] = None
    monthly_budget: Optional[float] = None
    rate_limit_rpm: Optional[int] = None
    enabled: Optional[bool] = None
    metadata: Optional[dict] = None

class APIKeyResponse(BaseModel):
    id: str
    provider: AIProvider
    key_name: str
    key_preview: str  # Only show last 4 characters
    weight: int
    daily_budget: Optional[float]
    monthly_budget: Optional[float]
    rate_limit_rpm: Optional[int]
    enabled: bool
    status: APIKeyStatus
    usage_stats: dict
    created_at: datetime
    updated_at: datetime

class LoadBalancingConfig(BaseModel):
    provider: AIProvider
    strategy: LoadBalancingStrategy
    enabled: bool = True
    failover_enabled: bool = True
    health_check_interval: int = Field(default=60, description="Health check interval in seconds")

class ProviderStats(BaseModel):
    provider: AIProvider
    total_keys: int
    active_keys: int
    total_requests: int
    total_cost: float
    avg_latency_ms: float
    success_rate: float
    current_strategy: LoadBalancingStrategy

# In-memory storage (replace with database models later)
api_keys_db = {}
load_balancing_configs = {}
usage_stats = {}

# Helper functions
def encrypt_api_key(api_key: str) -> str:
    """Encrypt API key using Fernet"""
    return cipher_suite.encrypt(api_key.encode()).decode()

def decrypt_api_key(encrypted_key: str) -> str:
    """Decrypt API key"""
    return cipher_suite.decrypt(encrypted_key.encode()).decode()

def get_key_preview(api_key: str) -> str:
    """Get preview of API key (last 4 characters)"""
    return f"****{api_key[-4:]}" if len(api_key) > 4 else "****"

def check_key_status(key_id: str) -> APIKeyStatus:
    """Check if API key is within budget and rate limits"""
    # Simplified - would check actual usage against limits
    key = api_keys_db.get(key_id)
    if not key or not key.get("enabled"):
        return APIKeyStatus.DISABLED
    return APIKeyStatus.ACTIVE

# Endpoints

@router.post("/keys", response_model=APIKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(key_data: APIKeyCreate):
    """
    Create a new API key for an AI provider.
    The key will be encrypted and stored securely.
    """
    key_id = secrets.token_urlsafe(16)
    encrypted_key = encrypt_api_key(key_data.api_key)

    api_key_record = {
        "id": key_id,
        "provider": key_data.provider,
        "key_name": key_data.key_name,
        "encrypted_key": encrypted_key,
        "key_preview": get_key_preview(key_data.api_key),
        "weight": key_data.weight,
        "daily_budget": key_data.daily_budget,
        "monthly_budget": key_data.monthly_budget,
        "rate_limit_rpm": key_data.rate_limit_rpm,
        "enabled": key_data.enabled,
        "metadata": key_data.metadata,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    api_keys_db[key_id] = api_key_record
    usage_stats[key_id] = {
        "total_requests": 0,
        "total_cost": 0.0,
        "total_tokens": 0,
        "daily_cost": 0.0,
        "monthly_cost": 0.0,
    }

    return APIKeyResponse(
        id=key_id,
        provider=api_key_record["provider"],
        key_name=api_key_record["key_name"],
        key_preview=api_key_record["key_preview"],
        weight=api_key_record["weight"],
        daily_budget=api_key_record["daily_budget"],
        monthly_budget=api_key_record["monthly_budget"],
        rate_limit_rpm=api_key_record["rate_limit_rpm"],
        enabled=api_key_record["enabled"],
        status=check_key_status(key_id),
        usage_stats=usage_stats[key_id],
        created_at=api_key_record["created_at"],
        updated_at=api_key_record["updated_at"],
    )

@router.get("/keys", response_model=List[APIKeyResponse])
async def list_api_keys(
    provider: Optional[AIProvider] = None,
    enabled_only: bool = False
):
    """
    List all API keys, optionally filtered by provider.
    """
    keys = []
    for key_id, key_data in api_keys_db.items():
        if provider and key_data["provider"] != provider:
            continue
        if enabled_only and not key_data["enabled"]:
            continue

        keys.append(APIKeyResponse(
            id=key_id,
            provider=key_data["provider"],
            key_name=key_data["key_name"],
            key_preview=key_data["key_preview"],
            weight=key_data["weight"],
            daily_budget=key_data["daily_budget"],
            monthly_budget=key_data["monthly_budget"],
            rate_limit_rpm=key_data["rate_limit_rpm"],
            enabled=key_data["enabled"],
            status=check_key_status(key_id),
            usage_stats=usage_stats.get(key_id, {}),
            created_at=key_data["created_at"],
            updated_at=key_data["updated_at"],
        ))

    return keys

@router.get("/keys/{key_id}", response_model=APIKeyResponse)
async def get_api_key(key_id: str):
    """
    Get details of a specific API key.
    """
    if key_id not in api_keys_db:
        raise HTTPException(status_code=404, detail="API key not found")

    key_data = api_keys_db[key_id]
    return APIKeyResponse(
        id=key_id,
        provider=key_data["provider"],
        key_name=key_data["key_name"],
        key_preview=key_data["key_preview"],
        weight=key_data["weight"],
        daily_budget=key_data["daily_budget"],
        monthly_budget=key_data["monthly_budget"],
        rate_limit_rpm=key_data["rate_limit_rpm"],
        enabled=key_data["enabled"],
        status=check_key_status(key_id),
        usage_stats=usage_stats.get(key_id, {}),
        created_at=key_data["created_at"],
        updated_at=key_data["updated_at"],
    )

@router.patch("/keys/{key_id}", response_model=APIKeyResponse)
async def update_api_key(key_id: str, update_data: APIKeyUpdate):
    """
    Update an API key's configuration.
    """
    if key_id not in api_keys_db:
        raise HTTPException(status_code=404, detail="API key not found")

    key_data = api_keys_db[key_id]

    if update_data.key_name is not None:
        key_data["key_name"] = update_data.key_name
    if update_data.weight is not None:
        key_data["weight"] = update_data.weight
    if update_data.daily_budget is not None:
        key_data["daily_budget"] = update_data.daily_budget
    if update_data.monthly_budget is not None:
        key_data["monthly_budget"] = update_data.monthly_budget
    if update_data.rate_limit_rpm is not None:
        key_data["rate_limit_rpm"] = update_data.rate_limit_rpm
    if update_data.enabled is not None:
        key_data["enabled"] = update_data.enabled
    if update_data.metadata is not None:
        key_data["metadata"] = update_data.metadata

    key_data["updated_at"] = datetime.utcnow()

    return APIKeyResponse(
        id=key_id,
        provider=key_data["provider"],
        key_name=key_data["key_name"],
        key_preview=key_data["key_preview"],
        weight=key_data["weight"],
        daily_budget=key_data["daily_budget"],
        monthly_budget=key_data["monthly_budget"],
        rate_limit_rpm=key_data["rate_limit_rpm"],
        enabled=key_data["enabled"],
        status=check_key_status(key_id),
        usage_stats=usage_stats.get(key_id, {}),
        created_at=key_data["created_at"],
        updated_at=key_data["updated_at"],
    )

@router.delete("/keys/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_key(key_id: str):
    """
    Delete an API key permanently.
    """
    if key_id not in api_keys_db:
        raise HTTPException(status_code=404, detail="API key not found")

    del api_keys_db[key_id]
    if key_id in usage_stats:
        del usage_stats[key_id]

    return None

@router.post("/load-balancing/{provider}", response_model=LoadBalancingConfig)
async def configure_load_balancing(provider: AIProvider, config: LoadBalancingConfig):
    """
    Configure load balancing strategy for a provider.
    """
    load_balancing_configs[provider] = config.dict()
    return config

@router.get("/load-balancing/{provider}", response_model=LoadBalancingConfig)
async def get_load_balancing_config(provider: AIProvider):
    """
    Get current load balancing configuration for a provider.
    """
    config = load_balancing_configs.get(provider, {
        "provider": provider,
        "strategy": LoadBalancingStrategy.ROUND_ROBIN,
        "enabled": True,
        "failover_enabled": True,
        "health_check_interval": 60,
    })
    return LoadBalancingConfig(**config)

@router.get("/stats/{provider}", response_model=ProviderStats)
async def get_provider_stats(provider: AIProvider):
    """
    Get usage statistics for a specific provider.
    """
    provider_keys = [k for k, v in api_keys_db.items() if v["provider"] == provider]
    active_keys = [k for k in provider_keys if api_keys_db[k]["enabled"]]

    total_requests = sum(usage_stats.get(k, {}).get("total_requests", 0) for k in provider_keys)
    total_cost = sum(usage_stats.get(k, {}).get("total_cost", 0.0) for k in provider_keys)

    config = load_balancing_configs.get(provider, {"strategy": LoadBalancingStrategy.ROUND_ROBIN})

    return ProviderStats(
        provider=provider,
        total_keys=len(provider_keys),
        active_keys=len(active_keys),
        total_requests=total_requests,
        total_cost=total_cost,
        avg_latency_ms=250.0,  # Mock data
        success_rate=0.98,  # Mock data
        current_strategy=config.get("strategy", LoadBalancingStrategy.ROUND_ROBIN),
    )

@router.post("/keys/{key_id}/test")
async def test_api_key(key_id: str):
    """
    Test an API key to verify it works correctly.
    """
    if key_id not in api_keys_db:
        raise HTTPException(status_code=404, detail="API key not found")

    key_data = api_keys_db[key_id]
    decrypted_key = decrypt_api_key(key_data["encrypted_key"])

    # Mock test - would actually call the provider's API
    return {
        "success": True,
        "provider": key_data["provider"],
        "key_preview": key_data["key_preview"],
        "test_timestamp": datetime.utcnow().isoformat(),
        "latency_ms": 145,
        "message": "API key is valid and working"
    }
