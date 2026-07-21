from sqlalchemy.orm import Session
from app.models.document import Document
from app.schemas.document import DocumentCreate
from sqlalchemy import select

class DocumentService:
  @staticmethod
  def create_document(db: Session, document_data: DocumentCreate) -> Document:
    document = Document(
      title= document_data.title,
      filename= document_data.filename
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document

  @staticmethod
  def get_documents(db: Session) -> list[Document]:
    stmt = select(Document)
    result = db.execute(stmt)
    documents = result.scalars().all()

    return documents

  @staticmethod
  def get_document(db:Session, document_id: int) -> Document | None:
    stmt = select(Document).where(Document.id == document_id)
    result = db.execute(stmt)
    document = result.scalar_one_or_none()

    return document

  @staticmethod
  def update_document(db:Session, document_id:  int, document_data: DocumentCreate) -> Document | None:
    stmt = select(Document).where(Document.id == document_id)
    result = db.execute(stmt)
    document = result.scalar_one_or_none()

    if document is None:
      return None

    document.title = document_data.title
    document.filename = document_data.filename

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
