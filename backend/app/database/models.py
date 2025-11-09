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
    analysis: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="ResumeAnalysis Pydantic 모델의 JSON")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


    def __repr__(self):
        return f"<Resume(id={self.id}, user_id={self.user_id}, created_at={self.created_at})>"


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False, comment="세션 ID")
    user_id: Mapped[str] = mapped_column(String, index=True, nullable=False, comment="사용자 ID")

    # 대화 상태
    messages: Mapped[list] = mapped_column(JSON, nullable=False, comment="대화 히스토리 [{role: str, content: str}]")
    current_question_index: Mapped[int] = mapped_column(default=0, nullable=False, comment="현재 질문 인덱스")
    answered_count: Mapped[int] = mapped_column(default=0, nullable=False, comment="답변한 질문 수")
    is_completed: Mapped[bool] = mapped_column(default=False, nullable=False, comment="대화 종료 여부")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Conversation(id={self.id}, session_id={self.session_id}, answered_count={self.answered_count})>"
