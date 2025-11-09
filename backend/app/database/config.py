"""
Database Configuration
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.database.models import Base

import os

# 데이터베이스 URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://resume_user:resume_password@localhost:5433/resume_maker"
)

# SQLAlchemy Engine 생성
engine = create_engine(
    DATABASE_URL,
    echo=True,  # SQL 로그 출력 (개발 환경)
    pool_pre_ping=True,  # 연결 유효성 검사
)

# SessionLocal 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    데이터베이스 세션 생성 (FastAPI Dependency)

    Yields:
        Session: SQLAlchemy 세션
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    데이터베이스 테이블 초기화
    """
    Base.metadata.create_all(bind=engine)
