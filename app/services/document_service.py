from sqlalchemy.orm import Session
from app.models.document import Document
from app.schemas.document import DocumentUpdate
from sqlalchemy import select, func
from app.storage.storage import save_file, delete_file
from app.services.pdf_service import PDFService
from app.models.chunk import Chunk
from app.services.chunk_service import ChunkingService

class DocumentService:
  @staticmethod
  def upload_document(db, user, title, file):
    stored_filename, file_path = save_file(file)

    try:
      text = PDFService.extract_text(file_path)
      chunks = ChunkingService.split_text(text)

      document = Document(
          title=title,
          filename=stored_filename,
          content_type=file.content_type,
          content=text,
          user_id=user.id,
      )

      db.add(document)
      db.flush()

      for index, chunk_text in enumerate(chunks):
        chunk = Chunk(document_id=document.id, content=chunk_text, chunk_index=index)

        db.add(chunk)
      
      db.commit()
      db.refresh(document)

      return document
    except Exception:
      db.rollback()
      delete_file(stored_filename)
      raise

  @staticmethod
  def get_documents(db: Session, skip, limit) -> list[Document]:
    stmt = select(Document).offset(skip).limit(limit)
    result = db.execute(stmt)
    documents = result.scalars().all()
    total = db.scalar(select(func.count()).select_from(Document))

    return {
        "items": documents,
        "total": total,
        "skip": skip,
        "limit": limit,
    }

  @staticmethod
  def get_document(db:Session, document_id: int) -> Document | None:
    stmt = select(Document).where(Document.id == document_id)
    result = db.execute(stmt)
    document = result.scalar_one_or_none()

    return document

  @staticmethod
  def update_document(db: Session, document_id: int, document_data: DocumentUpdate) -> Document | None:
    stmt = select(Document).where(Document.id == document_id)
    result = db.execute(stmt)
    document = result.scalar_one_or_none()

    if document is None:
      return None

    document.title = document_data.title

    db.commit()
    db.refresh(document)

    return document

  @staticmethod
  def delete_document(db: Session, document_id: int) -> bool:
    stmt = select(Document).where(Document.id == document_id)
    result = db.execute(stmt)
    document = result.scalar_one_or_none()
    if document is None:
      return False

    db.delete(document)
    db.commit()

    delete_file(document.filename)

    return True
