"""
LangGraph State Definition
"""
import operator
from typing import Annotated, TypedDict, Optional, List
from langchain.messages import AnyMessage


class ResumeCoachState(TypedDict):
    """
    이력서 코칭 대화 상태

    LangGraph에서 사용하는 상태 정의
    """
    thread_id: str
    user_id: str

    # 대화 정보
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int
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
