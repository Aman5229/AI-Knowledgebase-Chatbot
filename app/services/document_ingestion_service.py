from sqlalchemy.orm import Session
from app.models.chunk import Chunk
from app.services.embedding_service import EmbeddingService

class DocumentIngestionService:

  @staticmethod
  def save_chunks(db: Session, document_id: int, chunks: list[str]) -> None:
    for index, content in enumrate(chunks):
      embedding = EmbeddingService.create_embedding(content)
      chunk = Chunk(
        document_id=document_id,
        content=content,
        chunk_index=index,
        embedding=embedding
      )

      db.add(chunk)
