import os
import json
import redis.asyncio as redis
import httpx
from datetime import datetime

# Connect to Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

CACHE_TTL = 600   # 10 minutes in seconds
BASE_URL   = "https://api.exchangerate-api.com/v4/latest"


async def get_exchange_rates(base_currency: str) -> dict:
    cache_key = f"rates:{base_currency.upper()}"

    # Try Redis first
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)   # Redis stores strings, so we parse JSON back to dict

    # Cache miss — fetch from API
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/{base_currency}", timeout=10.0)
        response.raise_for_status()
        data = response.json()

    rates = data["rates"]

    # Store in Redis with TTL
    # json.dumps converts the dict to a string for Redis storage
    await redis_client.setex(cache_key, CACHE_TTL, json.dumps(rates))

    return rates


async def convert_currency(from_currency: str, to_currency: str, amount: float) -> dict:
    if from_currency == to_currency:
        return {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": amount,
            "converted_amount": amount,
            "rate": 1.0,
            "timestamp": datetime.utcnow().isoformat()
        }

    rates = await get_exchange_rates(from_currency)

    if to_currency not in rates:
        raise ValueError(f"Currency '{to_currency}' is not supported.")

    rate      = rates[to_currency]
    converted = round(amount * rate, 4)

    return {
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount": amount,
        "converted_amount": converted,
        "rate": rate,
        "timestamp": datetime.utcnow().isoformat()
    }