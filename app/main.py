from fastapi import FastAPI
from app.routes import scan

app = FastAPI()
app.include_router(scan.router)

@app.get("/")
async def root():
    return {"status": "Stoqr backend running"}