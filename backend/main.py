from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from routers.convert import router as convert_router
from routers.history import router as history_router   
from database.connection import engine                  
from database import models                             
from routers.auth import router as auth_router

# Create all tables when the app starts
# If the table already exists, this does nothing (safe to call every time)
models.Base.metadata.create_all(bind=engine)        

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Maudan Currency API", version="2.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(convert_router)
app.include_router(history_router)                  

@app.get("/health")
def health():
    return {"status": "ok"}