from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from sqlalchemy import ForeignKey, func
from sqlalchemy import String, DateTime

class Document(Base):
  __tablename__ = "documents"

  id: Mapped[int] = mapped_column(primary_key=True)
  title: Mapped[str] = mapped_column(String(255), nullable=False)
  filename: Mapped[str] = mapped_column(String(255),nullable=False)
  content_type: Mapped[str] = mapped_column(String(100), nullable=False)
  uploaded_at: Mapped[str] =  mapped_column(DateTime(timezone=True), server_default=func.now())

  user_id = mapped_column(ForeignKey("users.id"))
  user = relationship("User", back_populates="documents")
