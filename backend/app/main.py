from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import analysis

app = FastAPI(
    title="JANUA Financial Analysis API",
    description="API para análise financeira baseada em Excel",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://janua.pt",
        "https://www.janua.pt",
        "https://*.janua.pt"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analysis.router, prefix="/api", tags=["analysis"])

@app.get("/")
async def root():
    return {
        "message": "JANUA Financial Analysis API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "janua-financial-api"}
