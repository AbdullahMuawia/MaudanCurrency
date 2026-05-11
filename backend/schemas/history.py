from pydantic import BaseModel
from datetime import datetime

class HistoryItem(BaseModel):
    id: int
    from_currency: str
    to_currency: str
    amount: float
    converted_amount: float
    rate: float
    created_at: datetime

    # This tells Pydantic to read data from SQLAlchemy objects
    # Without this, Pydantic would only accept plain dictionaries
    model_config = {"from_attributes": True}


class HistoryResponse(BaseModel):
    items: list[HistoryItem]
    total: int