from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from schemas.conversion import ConversionRequest, ConversionResponse
from services.currency_maudan import convert_currency, get_exchange_rates
from database.connection import get_db
from database.models import ConversionHistory

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/api", tags=["currency"])


@router.post("/convert", response_model=ConversionResponse)
@limiter.limit("30/minute")
async def convert(request: Request, body: ConversionRequest, db: Session = Depends(get_db)):
    # Depends(get_db) is FastAPI's dependency injection:
    # FastAPI automatically opens a DB session, passes it here, and closes it after
    try:
        result = await convert_currency(
            from_currency=body.from_currency,
            to_currency=body.to_currency,
            amount=body.amount
        )

        # Save to database
        record = ConversionHistory(
            from_currency=result["from_currency"],
            to_currency=result["to_currency"],
            amount=result["amount"],
            converted_amount=result["converted_amount"],
            rate=result["rate"]
        )
        db.add(record)      # stage the insert
        db.commit()         # write to database
        db.refresh(record)  # reload the record (gets the auto-generated id and timestamp)

        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()       # undo any partial changes if something went wrong
        raise HTTPException(status_code=503, detail="Currency service unavailable.")


@router.get("/currencies")
@limiter.limit("10/minute")
async def list_currencies(request: Request):
    try:
        rates = await get_exchange_rates("USD")
        return {"currencies": sorted(rates.keys())}
    except Exception:
        raise HTTPException(status_code=503, detail="Could not fetch currency list.")