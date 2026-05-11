from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from database.connection import get_db
from database.models import ConversionHistory
from schemas.history import HistoryResponse, HistoryItem

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/api", tags=["history"])


@router.get("/history", response_model=HistoryResponse)
@limiter.limit("20/minute")
async def get_history(
    request: Request,
    db: Session = Depends(get_db),
    limit: int = 20,       # query param: /api/history?limit=10
    offset: int = 0        # query param: /api/history?offset=20 (pagination)
):
    """
    Returns the last N conversions.
    Supports pagination via limit/offset query parameters.
    """
    # Query the database — SQLAlchemy translates this to:
    # SELECT * FROM conversion_history ORDER BY created_at DESC LIMIT 20 OFFSET 0
    items = (
        db.query(ConversionHistory)
        .order_by(ConversionHistory.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    total = db.query(ConversionHistory).count()

    return HistoryResponse(
        items=[HistoryItem.model_validate(item) for item in items],
        total=total
    )