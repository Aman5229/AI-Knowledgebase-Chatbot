from sqlalchemy.orm import Session
from app.models.document import Document
from app.schemas.document import DocumentUpdate
from sqlalchemy import select, func
from app.storage.storage import save_file

class DocumentService:
  @staticmethod
  def upload_document(db, user, title, file):
    stored_filename, _ = save_file(file)

    document = Document(
        title=title,
        filename=stored_filename,
        content_type=file.content_type,
        user_id=user.id,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document

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

    return True
