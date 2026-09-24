from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Query
from app.db.dependencies import get_db
from app.schemas.document import DocumentResponse, DocumentListResponse, DocumentUpdate
from app.services.document_service import DocumentService
from app.auth.dependencies import get_current_user
from app.models.user import User
from fastapi import UploadFile, File, Form

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", response_model=DocumentResponse)
def upload_document(title: str = Form(...), file: UploadFile= File(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
 return DocumentService.upload_document(db=db, user=user, title=title, file=file)

@router.get("/", response_model=DocumentListResponse)
def get_documents(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100),db: Session = Depends(get_db)):
  return DocumentService.get_documents(db, skip, limit)

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
  document = DocumentService.get_document(db, document_id)
  if document is None:
    raise HTTPException(status_code=404, detail="Document not found")
  return document

@router.patch("/{document_id}", response_model=DocumentResponse)
def update_document(document_id: int, document_data: DocumentUpdate, db: Session = Depends(get_db)):
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
