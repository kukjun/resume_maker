from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


# ========================================
# 새로운 구조화된 이력서 스키마 (SIMPLE_EXTRACTION_PROMPT 기반)
# ========================================

class SkillCategory(str, Enum):
    """기술 카테고리"""
    LANGUAGE = "language"
    FRAMEWORK = "framework"
    DATABASE = "database"
    CLOUD = "cloud"
    TOOL = "tool"


class PersonInfo(BaseModel):
    """개인 정보"""
    name: Optional[str] = Field(description="이름")
    email: Optional[str] = Field(default=None, description="이메일 주소")
    phone: Optional[str] = Field(default=None, description="전화번호")
    title: Optional[str] = Field(description="직무명, 예: Backend Engineer")
    years_of_experience: int = Field(description="경력 년수")


class Skill(BaseModel):
    """기술 스택"""
    name: str = Field(description="정규화된 기술명 (예: Python3 → Python)")
    category: SkillCategory = Field(description="기술 카테고리")


class STARCompleteness(BaseModel):
    """STAR 완성도 평가"""
    situation: bool = Field(description="상황(Situation) 포함 여부")
    task: bool = Field(description="과제(Task) 포함 여부")
    actions: bool = Field(description="행동(Actions) 포함 여부")
    results: bool = Field(description="결과(Results) 포함 여부")
    score: float = Field(ge=0.0, le=1.0, description="완성도 점수 (0.0 ~ 1.0)")


class ProjectInfo(BaseModel):
    """프로젝트 정보"""
    id: str = Field(description="자동 생성 ID (예: proj_001)")
    name: str = Field(description="프로젝트명")
    company: Optional[str] = Field(default=None, description="회사명")
    period: str = Field(description="YYYY.MM - YYYY.MM 형식")
    role: Optional[str] = Field(default=None, description="역할")

    # STAR 기법
    situation: Optional[str] = Field(default=None, description="문제 상황")
    task: Optional[str] = Field(default=None, description="해결 과제")
    actions: List[str] = Field(default_factory=list, description="구체적 행동 (최소 1개)")
    results: List[str] = Field(default_factory=list, description="성과 (정량적이면 숫자 포함)")

    tech_stack: List[str] = Field(default_factory=list, description="사용 기술 스택")

    is_complete: STARCompleteness = Field(description="STAR 완성도")

class Career(BaseModel):
    company: str
    position: str
    duration: str
    description: Optional[str] = None

class Education(BaseModel):
    institution: str
    degree: str
    major: str
    duration: str
    gpa: Optional[float] = None


class ResumeExtraction(BaseModel):
    """이력서 추출 결과 (SIMPLE_EXTRACTION_PROMPT의 JSON 구조)"""
    person: PersonInfo = Field(description="개인 정보")
    skills: List[Skill] = Field(description="기술 스택 목록")
    projects: List[ProjectInfo] = Field(description="프로젝트 목록")
    career: List[Career] = Field(default_factory=list, description="경력 사항")
    education: List[Education] = Field(default_factory=list, description="학력 사항")


# ========================================
# 이력서 분석 결과 스키마
# ========================================

class ImprovementQuestion(BaseModel):
    """개선 질문"""
    category: str = Field(description="질문 카테고리 (예: STAR-상황, STAR-결과, 기술스택 등)")
    project_id: Optional[str] = Field(default=None, description="관련 프로젝트 ID (프로젝트 관련 질문인 경우)")
    question: str = Field(description="구체적인 질문 내용")
    purpose: str = Field(description="이 질문의 목적 (왜 필요한지)")


class ResumeAnalysis(BaseModel):
    """이력서 분석 결과"""
    overall_summary: str = Field(description="전체 이력서 평가 요약 (강점과 약점)")
    missing_areas: List[str] = Field(description="부족한 영역 목록 (예: STAR 기법 미흡, 정량적 성과 부족 등)")
    improvement_questions: List[ImprovementQuestion] = Field(description="보완을 위한 질문 리스트")
    completeness_score: float = Field(ge=0.0, le=1.0, description="전체 완성도 점수 (0.0 ~ 1.0)")
