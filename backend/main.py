from fastapi import FastAPI  
from fastapi.middleware.cors import CORSMiddleware
from routers.convert import router 


app = FastAPI(
    title="Maudan Currency API", 
    description="Real-time currency conversion powered by live exchange rates.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]

)

app.include_router(router)

@app.get("/health")
def health(): 
    return{"status": "ok"}