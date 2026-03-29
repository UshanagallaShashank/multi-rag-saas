import json

from redis.asyncio import Redis

from ..config import settings

_redis: Redis | None = None

async def get_redis() -> Redis | None:
    # Return None if Redis is not configured
    if not settings.redis_url:
        return None
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis

async def cache_get(key: str) -> dict | None:
    # Return cached value, or None if Redis unavailable or key missing
    r = await get_redis()
    if r is None:
        return None
    val = await r.get(key)
    return json.loads(val) if val else None

async def cache_set(key: str, value: dict, ttl: int = 3600) -> None:
    # No-op if Redis unavailable, otherwise store with TTL
    r = await get_redis()
    if r is None:
        return
    await r.setex(key, ttl, json.dumps(value))
