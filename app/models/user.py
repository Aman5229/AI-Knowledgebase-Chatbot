from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

class User(Base):
  __tablename__ = "users"
  id: Mapped[int] = mapped_column(primary_key=True)
  email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
  password_hash:  Mapped[str] = mapped_column(String(255),nullable=False)
  documents: Mapped[list["Document"]] = relationship("Document", back_populates="user")

  def __repr__(self):
    return f"<User id={self.id}, email='{self.email}'>"
