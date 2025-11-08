from typing import Dict, Optional
from app.models.schemas import SessionData
import uuid

class SessionManager:
    """
    In-memory 세션 관리 (추후 Redis나 DB로 전환 가능)
    """
    def __init__(self):
        self.sessions: Dict[str, SessionData] = {}

    def create_session(self) -> str:
        """새 세션 생성"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = SessionData(session_id=session_id)
        return session_id

    def get_session(self, session_id: str) -> Optional[SessionData]:
        """세션 조회"""
        return self.sessions.get(session_id)

    def update_session(self, session_id: str, data: SessionData):
        """세션 업데이트"""
        self.sessions[session_id] = data

    def delete_session(self, session_id: str):
        """세션 삭제"""
        if session_id in self.sessions:
            del self.sessions[session_id]

# 전역 세션 매니저 인스턴스
session_manager = SessionManager()
