import json
import os
import redis


REDIS_HOST = os.getenv("REDIS_HOST", "redis_db")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_URL = (os.getenv("REDIS_URL") or "").strip().strip('"').strip("'")
VALID_REDIS_SCHEMES = ("redis://", "rediss://", "unix://")
CACHE_PREFIX = os.getenv("CACHE_PREFIX", "bitcoin-viewer")


def _build_client() -> redis.Redis:
    base_kwargs = {
        "decode_responses": True,
        "socket_connect_timeout": 2,
        "socket_timeout": 2,
        "health_check_interval": 30,
    }

    if REDIS_URL and REDIS_URL.lower().startswith(VALID_REDIS_SCHEMES):
        return redis.Redis.from_url(REDIS_URL, **base_kwargs)

    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        password=REDIS_PASSWORD,
        **base_kwargs,
    )


redis_client = _build_client()


def build_cache_key(*parts: str) -> str:
    safe_parts = [str(part).strip().lower() for part in parts if str(part).strip()]
    return f"{CACHE_PREFIX}:{':'.join(safe_parts)}"


def cache_get_json(key: str):
    try:
        raw = redis_client.get(key)
        if not raw:
            return None
        return json.loads(raw)
    except Exception:
        return None


def cache_set_json(key: str, value, ttl_seconds: int = 60) -> bool:
    try:
        redis_client.setex(key, int(ttl_seconds), json.dumps(value))
        return True
    except Exception:
        return False
