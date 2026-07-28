from fastapi import FastAPI
from app.api.v1.endpoints.document import router as document_router
from app.api.v1.endpoints.user import router as user_router

app  = FastAPI()

app.include_router(document_router)
app.include_router(user_router)

@app.get("/")
async def root():
  return {"message": "Welcome to AI knowledge chatbot"}