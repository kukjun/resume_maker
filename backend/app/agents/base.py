"""
Agent 추상화 인터페이스
LangGraph, CrewAI 등 다양한 Agent 프레임워크를 교체 가능하게 함
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from pydantic import BaseModel


class InterviewResult(BaseModel):
    """인터뷰 결과"""
    question: str
    is_complete: bool
    knowledge_base: Dict[str, Any]


class ResumeGenerationResult(BaseModel):
    """이력서 생성 결과"""
    resume_text: str
    resume_markdown: str


class BaseAgent(ABC):
    """Agent 기본 인터페이스"""

    @abstractmethod
    async def analyze_resume(self, resume_text: str, session_id: str) -> str:
        """
        이력서 분석 및 첫 질문 생성

        Args:
            resume_text: PDF에서 추출한 이력서 텍스트
            session_id: 세션 ID

        Returns:
            첫 번째 질문
        """
        pass

    @abstractmethod
    async def process_answer(
        self,
        session_id: str,
        user_answer: str
    ) -> InterviewResult:
        """
        사용자 답변 처리 및 다음 질문 생성

        Args:
            session_id: 세션 ID
            user_answer: 사용자의 답변

        Returns:
            InterviewResult (다음 질문, 완료 여부, 지식베이스)
        """
        pass

    @abstractmethod
    async def get_knowledge_base(self, session_id: str) -> Dict[str, Any]:
        """
        현재 수집된 지식베이스 조회

        Args:
            session_id: 세션 ID

        Returns:
            지식베이스 딕셔너리
        """
        pass

    @abstractmethod
    async def generate_resume(
        self,
        session_id: str,
        jd_text: str
    ) -> ResumeGenerationResult:
        """
        JD 기반 맞춤형 이력서 생성

        Args:
            session_id: 세션 ID
            jd_text: Job Description 텍스트

        Returns:
            ResumeGenerationResult (이력서 텍스트, 마크다운)
        """
        pass
