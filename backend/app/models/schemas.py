from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class PersonalInfo(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None

class Project(BaseModel):
    name: str
    description: str
    duration: str
    technologies: List[str]
    achievements: List[str]
    role: Optional[str] = None

class Career(BaseModel):
    company: str
    position: str
    duration: str
    description: Optional[str] = None
    projects: List[Project] = []

class Education(BaseModel):
    institution: str
    degree: str
    major: str
    duration: str
    gpa: Optional[float] = None

class KnowledgeBaseSchema(BaseModel):
    """
    사용자의 지식 베이스 구조
    """
    personal_info: PersonalInfo
    careers: List[Career]
    skills: List[str]
    education: List[Education]
    certifications: List[str] = []
    awards: List[str] = []
    languages: List[Dict[str, str]] = []  # [{"language": "English", "level": "Fluent"}]
    metadata: Dict[str, Any] = {}
    updated_at: datetime = datetime.now()

class JDAnalysis(BaseModel):
    """
    JD 분석 결과
    """
    required_skills: List[str]
    preferred_skills: List[str]
    key_responsibilities: List[str]
    company_info: Optional[str] = None
    position: str
    seniority_level: Optional[str] = None

class SessionData(BaseModel):
    """
    세션 데이터
    """
    session_id: str
    resume_text: str = ""  # 원본 이력서 텍스트
    knowledge_base: Dict[str, Any] = {}  # 지식베이스 (유연한 구조)
    conversation_history: List[Dict[str, str]] = []  # 대화 히스토리
    question_count: int = 0
    is_complete: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
