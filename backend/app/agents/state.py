"""
LangGraph State Definition
"""
from typing import TypedDict, Optional, List
from app.models.schemas import ResumeExtraction, ResumeAnalysis, ImprovementQuestion


class ResumeCoachState(TypedDict):
    """
    이력서 코칭 대화 상태

    LangGraph에서 사용하는 상태 정의
    """
    # 세션 정보
    session_id: str
    user_id: str

    # 대화 정보
    messages: List[dict]  # [{role: str, content: str}]
    user_answer: Optional[str]  # 사용자의 현재 답변

    # 이력서 데이터
    current_resume_data: Optional[dict]  # ResumeExtraction의 dict 형태
    current_analysis: Optional[dict]  # ResumeAnalysis의 dict 형태

    # 질문 관리
    improvement_questions: List[dict]  # ImprovementQuestion의 dict 리스트
    current_question_index: int
    current_question: Optional[dict]  # 현재 질문 (ImprovementQuestion)

    # 진행 상태
    answered_count: int
    is_completed: bool

    # 응답
    response: Optional[str]  # 사용자에게 보낼 응답 메시지
