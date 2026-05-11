from fastapi import APIRouter, HTTPException
from schemas.conversion import ConversionRequest, ConversionResponse 
from services.currency_maudan import convert_currency, get_exchange_rates

router = APIRouter(prefix="/api", tags=["Maudan"])


@router.post("/convert", response_model=ConversionResponse)

async def convert(request: ConversionRequest):
    try: 
        result = await convert_currency( 
        from_currency = request.from_currency,
        to_currency= request.to_currency,
        amount = request.amount
    )
        return result 
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code = 503, detail="Currency service unavailable. Try again later.")
    

@router.get("/currencies")

async def list_currencies(): 

    try:
        rates = await get_exchange_rates("USD")
        return {"currencies": sorted(rates.keys())}
    except Exception:
        raise HTTPException(status_code = 503, detail = "Could not fetch currency list.")