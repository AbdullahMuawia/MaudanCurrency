from pydantic import BaseModel, field_validator

class ConversionRequest(BaseModel):
    from_currency: str 
    to_currency: str 
    amount:float 

    @field_validator('from_currency', 'to_currency')
    def must_uppercase(cls, v): 
        return v.upper() 
    
    @field_validator('amount')
    def must_positive(cls, v): 
        if v <= 0: 
            raise ValueError("Amount must be greater than zero")
        return v
    
class ConversionResponse(BaseModel): 
    from_currency: str 
    to_currency: str 
    amount: float 
    converted_amount: float 
    rate: float 
    timestamp: str 

