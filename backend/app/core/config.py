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
    langchain_tracing_v2: bool = False
    langchain_endpoint: str = "https://api.smith.langchain.com"
    langchain_api_key: Optional[str] = None
    langchain_project: str = "resume-maker"

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
settings = Settings()


def setup_langsmith():
    """
    LangSmith 설정
    환경 변수가 설정되어 있으면 LangSmith 추적을 활성화합니다.
    """
    if settings.langchain_tracing_v2 and settings.langchain_api_key:
        os.environ["LANGCHAIN_TRACING_V2"] = str(settings.langchain_tracing_v2)
        os.environ["LANGCHAIN_ENDPOINT"] = settings.langchain_endpoint
        os.environ["LANGCHAIN_API_KEY"] = settings.langchain_api_key
        os.environ["LANGCHAIN_PROJECT"] = settings.langchain_project
        print(f"✅ LangSmith 추적 활성화: 프로젝트 '{settings.langchain_project}'")
    else:
        print("ℹ️  LangSmith 추적 비활성화 (API 키가 설정되지 않음)")
