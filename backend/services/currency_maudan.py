import httpx 
from cachetools import TTLCache 
from datetime import datetime 


_rate_cache = TTLCache(maxsize=10, ttl=600)

BASE_URL = "https://api.exchangerate-api.com/v4/latest"

async def get_exchange_rates(base_currency: str) -> dict:


    cache_key = base_currency.upper() 

    if cache_key in _rate_cache: 
        return _rate_cache[cache_key]
    

    async with httpx.AsyncClient() as client: 
        response = await client.get(f"{BASE_URL}/{base_currency}", timeout = 10.0) 
        response.raise_for_status() 
        data = response.json() 

    
    rates = data["rates"]
    _rate_cache[cache_key] = rates 
    return rates 


async def convert_currency(
        from_currency: str, 
        to_currency: str, 
         amount:float
) -> dict: 
        
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
        
        rate = rates[to_currency]
        converted = round(amount * rate, 4)

        return {
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount": amount,
        "converted_amount": converted,
        "rate": rate,
        "timestamp": datetime.utcnow().isoformat()
        }
        
        