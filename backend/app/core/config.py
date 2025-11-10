"""
Application configuration
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # LLM API Keys
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"

    # LangSmith (Optional)
    LANGSMITH_TRACING: bool = False
    LANGSMITH_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGSMITH_API_KEY: Optional[str] = None
    LANGSMITH_PROJECT: str = "resume-maker"
    DATABASE_URL: Optional[str] = None

    # FastAPI
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # CORS
    cors_origins: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # 추가 필드 무시


# Settings instance
settings = Settings()  # type: ignore


def setup_langsmith():
    """
    LangSmith 설정
    환경 변수가 설정되어 있으면 LangSmith 추적을 활성화합니다.
    """
    if settings.LANGSMITH_TRACING and settings.LANGSMITH_API_KEY:
        os.environ["LANGSMITH_TRACING"] = str(settings.LANGSMITH_TRACING)
        os.environ["LANGSMITH_ENDPOINT"] = settings.LANGSMITH_ENDPOINT
        os.environ["LANGSMITH_API_KEY"] = settings.LANGSMITH_API_KEY
        os.environ["LANGSMITH_PROJECT"] = settings.LANGSMITH_PROJECT
        print(f"✅ LangSmith 추적 활성화: 프로젝트 '{settings.LANGSMITH_PROJECT}'")
    else:
        print("ℹ️  LangSmith 추적 비활성화 (API 키가 설정되지 않음)")
