"""
Resume Repository - 데이터베이스 저장 로직
"""
from sqlalchemy.orm import Session
from typing import Optional
from app.database.models import Resume
from app.models.schemas import ResumeExtraction


class ResumeRepository:
    """이력서 저장/조회 Repository"""

    def __init__(self, db: Session):
        self.db = db

    def save(self, resume_data: ResumeExtraction, user_id: Optional[str] = None) -> Resume:
        """
        이력서 데이터를 데이터베이스에 저장

        Args:
            resume_data: ResumeExtraction Pydantic 모델
            user_id: 사용자 ID (Optional)

        Returns:
            Resume: 저장된 Resume 모델
        """
        # Pydantic 모델을 dict로 변환
        resume_dict = resume_data.model_dump()

        # Resume 엔티티 생성
        db_resume = Resume(
            user_id=user_id,
            data=resume_dict
        )

        # 데이터베이스에 저장
        self.db.add(db_resume)
        self.db.commit()
        self.db.refresh(db_resume)

        return db_resume

    def get_by_id(self, resume_id: int) -> Optional[Resume]:
        """
        ID로 이력서 조회

        Args:
            resume_id: 이력서 ID

        Returns:
            Resume or None
        """
        return self.db.query(Resume).filter(Resume.id == resume_id).first()

    def get_by_user_id(self, user_id: str) -> list[Resume]:
        """
        사용자 ID로 이력서 목록 조회

        Args:
            user_id: 사용자 ID

        Returns:
            List[Resume]
        """
        return self.db.query(Resume).filter(Resume.user_id == user_id).all()
    
    def get_recent_resume_by_user_id(self, user_id: Optional[str] = None) -> Optional[Resume]:
        """
        사용자 ID로 이력서 목록 조회

        Args:
            user_id: 사용자 ID

        Returns:
            List[Resume]
        """
        return self.db.query(Resume).filter(Resume.user_id == user_id).order_by(Resume.created_at).first()

    def update(self, resume_id: int, resume_data: Resume) -> Optional[Resume]:
        """
        이력서 데이터 업데이트

        Args:
            resume_id: 이력서 ID
            resume_data: 업데이트할 ResumeExtraction 데이터

        Returns:
            Resume or None
        """
        db_resume = self.get_by_id(resume_id)
        if not db_resume:
            return None

        # 데이터 업데이트
        db_resume = resume_data  # type: ignore

        self.db.commit()
        self.db.refresh(db_resume)

        return db_resume

    def delete(self, resume_id: int) -> bool:
        """
        이력서 삭제

        Args:
            resume_id: 이력서 ID

        Returns:
            bool: 삭제 성공 여부
        """
        db_resume = self.get_by_id(resume_id)
        if not db_resume:
            return False

        self.db.delete(db_resume)
        self.db.commit()

        return True
