"""
SQLAlchemy Database Models
"""

from sqlalchemy import JSON, DateTime, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from datetime import datetime

class Base(DeclarativeBase):
    pass


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[str | None] = mapped_column(String, index=True, nullable=True, comment="사용자 ID (추후 인증 구현 시 사용)")
    data: Mapped[dict] = mapped_column(JSON, nullable=False, comment="ResumeExtraction Pydantic 모델의 JSON")
    analysis: Mapped[dict | None] = mapped_column(JSON,ensure_ascii=False ,nullable=True, comment="ResumeAnalysis Pydantic 모델의 JSON")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


    def __repr__(self):
        return f"<Resume(id={self.id}, user_id={self.user_id}, created_at={self.created_at})>"
