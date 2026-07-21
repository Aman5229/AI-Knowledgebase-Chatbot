from fastapi import FastAPI
from app.api.v1.endpoints.document import router as document_router

app  = FastAPI()

app.include_router(document_router)

@app.get("/")
async def root():
  return {"message": "Welcome to AI knowledge chatbot"}