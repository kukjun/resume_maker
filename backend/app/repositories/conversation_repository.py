"""
Conversation Repository - 대화 세션 저장 로직
"""
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database.models import Conversation


class ConversationRepository:
    """대화 세션 저장/조회 Repository"""

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        session_id: str,
        user_id: str,
        messages: Optional[List[dict]] = None
    ) -> Conversation:
        """
        새로운 대화 세션 생성

        Args:
            session_id: 세션 ID
            user_id: 사용자 ID
            messages: 초기 메시지 리스트 (Optional)

        Returns:
            Conversation: 생성된 Conversation 모델
        """
        db_conversation = Conversation(
            session_id=session_id,
            user_id=user_id,
            messages=messages or [],
            current_question_index=0,
            answered_count=0,
            is_completed=False
        )

        self.db.add(db_conversation)
        self.db.commit()
        self.db.refresh(db_conversation)

        return db_conversation

    def get_by_session_id(self, session_id: str) -> Optional[Conversation]:
        """
        세션 ID로 대화 조회

        Args:
            session_id: 세션 ID

        Returns:
            Conversation or None
        """
        return self.db.query(Conversation).filter(
            Conversation.session_id == session_id
        ).first()

    def get_by_user_id(self, user_id: str) -> List[Conversation]:
        """
        사용자 ID로 대화 목록 조회

        Args:
            user_id: 사용자 ID

        Returns:
            List[Conversation]
        """
        return self.db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(Conversation.created_at.desc()).all()

    def update(
        self,
        session_id: str,
        messages: Optional[List[dict]] = None,
        current_question_index: Optional[int] = None,
        answered_count: Optional[int] = None,
        is_completed: Optional[bool] = None
    ) -> Optional[Conversation]:
        """
        대화 세션 업데이트

        Args:
            session_id: 세션 ID
            messages: 업데이트할 메시지 리스트
            current_question_index: 현재 질문 인덱스
            answered_count: 답변한 질문 수
            is_completed: 대화 완료 여부

        Returns:
            Conversation or None
        """
        db_conversation = self.get_by_session_id(session_id)
        if not db_conversation:
            return None

        if messages is not None:
            db_conversation.messages = messages  # type: ignore
        if current_question_index is not None:
            db_conversation.current_question_index = current_question_index  # type: ignore
        if answered_count is not None:
            db_conversation.answered_count = answered_count  # type: ignore
        if is_completed is not None:
            db_conversation.is_completed = is_completed  # type: ignore

        self.db.commit()
        self.db.refresh(db_conversation)

        return db_conversation

    def delete(self, session_id: str) -> bool:
        """
        대화 세션 삭제

        Args:
            session_id: 세션 ID

        Returns:
            bool: 삭제 성공 여부
        """
        db_conversation = self.get_by_session_id(session_id)
        if not db_conversation:
            return False

        self.db.delete(db_conversation)
        self.db.commit()

        return True
