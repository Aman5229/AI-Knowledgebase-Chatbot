from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Query
from app.db.dependecies import get_db
from app.schemas.document import DocumentCreate, DocumentResponse, DocumentListResponse
from app.services.document_service import DocumentService
from typing import List

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/", response_model=DocumentResponse)
def create_document(
  document: DocumentCreate,
  db: Session = Depends(get_db),
):
  return DocumentService.create_document(db, document)

@router.get("/", response_model=DocumentListResponse)
def get_documents(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100),db: Session = Depends(get_db)):
  return DocumentService.get_documents(db, skip, limit)

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
  document = DocumentService.get_document(db, document_id)
  if document is None:
    raise HTTPException(status_code=404, detail="Document not found")
  return document

@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(document_id: int, document_data: DocumentCreate, db: Session = Depends(get_db)):
  document = DocumentService.update_document(db, document_id, document_data)
  if document is None:
    raise HTTPException(status_code=404, detail="Document not found")

  return document

@router.delete("/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
  deleted = DocumentService.delete_document(db, document_id)
  if not deleted:
    raise HTTPException(status_code=404, detail="Document not found")

  return {"message": "Document deleted successfully"}