"""
pytest fixtures for tests
"""
import pytest
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from app.services.user_resume_service import user_resume_service


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    """테스트 fixtures 디렉토리 경로"""
    return Path(__file__).parent / "fixtures" / "data"


@pytest.fixture(scope="session")
def test_resume_path(fixtures_dir: Path) -> Path:
    """TEST_RESUME.pdf 경로"""
    return fixtures_dir / "TEST_RESUME.pdf"


@pytest.fixture(scope="session")
def test_career_path(fixtures_dir: Path) -> Path:
    """TEST_CAREER.pdf 경로"""
    return fixtures_dir / "TEST_CAREER.pdf"


@pytest.fixture(scope="session")
def resume_pdf_bytes(test_resume_path: Path) -> bytes:
    """TEST_RESUME.pdf를 bytes로 읽기"""
    if not test_resume_path.exists():
        pytest.skip(f"TEST_RESUME.pdf not found at {test_resume_path}")
    with open(test_resume_path, 'rb') as f:
        return f.read()


@pytest.fixture(scope="session")
def career_pdf_bytes(test_career_path: Path) -> bytes:
    """TEST_CAREER.pdf를 bytes로 읽기"""
    if not test_career_path.exists():
        pytest.skip(f"TEST_CAREER.pdf not found at {test_career_path}")
    with open(test_career_path, 'rb') as f:
        return f.read()


@pytest.fixture(scope="session")
def resume_documents(resume_pdf_bytes: bytes) -> List[Document]:
    """TEST_RESUME.pdf에서 추출한 Document 리스트 (캐시됨)"""
    return user_resume_service.extract_text_from_pdfs([resume_pdf_bytes])


@pytest.fixture(scope="session")
def career_documents(career_pdf_bytes: bytes) -> List[Document]:
    """TEST_CAREER.pdf에서 추출한 Document 리스트 (캐시됨)"""
    return user_resume_service.extract_text_from_pdfs([career_pdf_bytes])


@pytest.fixture(scope="session")
def all_documents(resume_pdf_bytes: bytes, career_pdf_bytes: bytes) -> List[Document]:
    """모든 PDF에서 추출한 Document 리스트 (캐시됨)"""
    return user_resume_service.extract_text_from_pdfs([resume_pdf_bytes, career_pdf_bytes])
