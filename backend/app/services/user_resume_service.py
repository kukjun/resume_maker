import tempfile
import os
import json

from typing import List, Optional
from sqlalchemy.orm import Session
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage
from app.core.prompts import SIMPLE_EXTRACTION_PROMPT, RESUME_ANALYSIS_PROMPT
from app.models.schemas import ResumeExtraction, ResumeAnalysis
from app.repositories import ResumeRepository
from app.database.models import Resume


class UserResumeService:
    """
    사용자 이력서 관련 서비스
    """

    def __init__(self, db: Session):
        """
        초기화

        Args:
            db: SQLAlchemy 세션
        """
        self.db = db
        self.resume_repo = ResumeRepository(db)
        
    async def create_user_resume(self, pdf_contents: List[bytes], user_id: Optional[str] = None) -> bool:
        """
        사용자 이력서 생성 및 저장

        Args:
            pdf_contents: 이력서 PDF 파일들의 bytes 리스트
            user_id: 사용자 ID (Optional)

        Returns:
            Resume: 저장된 Resume 객체
        """
        # 1. PDF에서 텍스트 추출
        documents = await self.extract_text_from_pdfs(pdf_contents)

        # 2. 이력서 지식 베이스 생성
        resume_data = await self.create_resume_knowledge_base(documents)

        # 3. 데이터베이스에 저장
        await self.save_resume_knowledge_base(resume_data, user_id)
        
        return True
    
    async def save_resume_knowledge_base(
        self,
        resume_data: ResumeExtraction,
        user_id: Optional[str] = None
    ) -> Resume:
        """
        이력서 지식 베이스를 데이터베이스에 저장

        Args:
            resume_data: ResumeExtraction Pydantic 객체
            user_id: 사용자 ID (Optional)

        Returns:
            Resume: 저장된 Resume 객체
        """
        try:
            saved_resume = self.resume_repo.save(resume_data, user_id)
            print(f"✅ Resume saved to database with ID: {saved_resume.id}")
            return saved_resume
        except Exception as e:
            raise ValueError(f"이력서 저장 실패: {str(e)}")
    
    async def create_resume_knowledge_base(self, documents: List[Document]) -> ResumeExtraction:
        """
        이력서 문서들로 지식 베이스 생성

        Args:
            documents: 이력서에서 추출한 Document 리스트

        Returns:
            ResumeExtraction: 구조화된 이력서 정보
        """
        try:
            # Documents 문서를 잘 정리해서 OPENAI API로 SYSTEM PROMPT로 넘겨줌.
            # JSON 구조를 써서 결과를 가져올 수 있도록 하는데, 요구사항으로 원하는 DATA 구조를 같이 제공함.

            contents = "\n\n".join([doc.page_content for doc in documents])
            model = init_chat_model("gpt-4o-mini", temperature=0.3)

            system_prompt = SIMPLE_EXTRACTION_PROMPT.format(
                resume_text=contents
            )
            conversations = [
                SystemMessage(content=system_prompt),
            ]

            response = model.invoke(conversations)

            # JSON 문자열을 Pydantic 객체로 변환
            json_content = response.content
            print(f"LLM Response Content:\n{json_content}")

            # 타입 체크: 문자열이 아니면 에러
            if not isinstance(json_content, str):
                raise ValueError(f"LLM 응답이 문자열이 아닙니다: {type(json_content)}")

            # JSON 문자열에서 마크다운 코드블록 제거 (```json ... ``` 형식)
            if json_content.startswith("```"):
                json_content = json_content.split("```")[1]
                if json_content.startswith("json"):
                    json_content = json_content[4:].strip()

            # JSON 파싱 후 Pydantic 객체 생성
            resume_data = ResumeExtraction.model_validate_json(json_content)

            print("📝 Extracted Resume Data:", resume_data)

            return resume_data

        except Exception as e:
            raise ValueError(f"이력서 지식 베이스 생성 실패: {str(e)}")
        
        

    async def extract_text_from_pdfs(self, pdf_contents: List[bytes]) -> List[Document]:
        """
        PDF 파일(들)에서 텍스트 추출 및 병합
        단일 또는 여러 PDF 모두 처리 가능

        Args:
            pdf_contents: PDF 파일들의 bytes 리스트

        Returns:
            Document 객체 리스트
        """
        try:
            if not pdf_contents:
                raise ValueError("PDF 파일이 없습니다.")

            all_documents = []

            for idx, pdf_content in enumerate(pdf_contents):
                # bytes를 임시 파일로 저장 (PyPDFLoader는 파일 경로만 받음)
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(pdf_content)
                    tmp_file_path = tmp_file.name

                try:
                    # PyPDFLoader로 PDF 로드
                    loader = PyPDFLoader(tmp_file_path)
                    documents = loader.load()

                    # 각 문서에 메타데이터 추가 (어떤 PDF에서 왔는지)
                    for doc in documents:
                        doc.metadata['source_pdf_index'] = idx

                    all_documents.extend(documents)

                finally:
                    # 임시 파일 삭제
                    if os.path.exists(tmp_file_path):
                        os.unlink(tmp_file_path)

            return all_documents

        except Exception as e:
            raise ValueError(f"PDF 텍스트 추출 실패: {str(e)}")


    async def load_resume_from_pdf(self, file_path: str) -> List[Document]:
        """
        PDF 파일 경로에서 이력서 로드

        Args:
            file_path: PDF 파일 경로

        Returns:
            Document 객체 리스트
        """
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            return documents
        except Exception as e:
            raise ValueError(f"이력서 로드 실패: {str(e)}")

    async def analyze_resume(self, user_id: Optional[str] = None) -> ResumeAnalysis:
        """
        사용자 이력서 분석 후 개선 질문 리스트 반환

        Args:
            user_id: 사용자 ID (Optional)

        Returns:
            ResumeAnalysis: 분석 결과 (요약, 부족한 영역, 개선 질문 리스트)
        """
        try:
            # 1. 최근 이력서 데이터 가져오기
            recent_resume = self.resume_repo.get_recent_resume_by_user_id(user_id)

            if not recent_resume:
                raise ValueError(f"사용자 ID {user_id}의 이력서를 찾을 수 없습니다.")

            # 2. Resume.data를 JSON 문자열로 변환
            resume_json = json.dumps(recent_resume.data, ensure_ascii=False, indent=2)

            # 3. LLM으로 분석
            model = init_chat_model("gpt-4o-mini", temperature=0.3)

            system_prompt = RESUME_ANALYSIS_PROMPT.format(
                resume_data=resume_json
            )
            conversations = [
                SystemMessage(content=system_prompt),
            ]

            response = model.invoke(conversations)

            # 4. JSON 파싱
            json_content = response.content
            print(f"LLM Analysis Response:\n{json_content}")

            # 타입 체크
            if not isinstance(json_content, str):
                raise ValueError(f"LLM 응답이 문자열이 아닙니다: {type(json_content)}")

            # 마크다운 코드블록 제거
            if json_content.startswith("```"):
                json_content = json_content.split("```")[1]
                if json_content.startswith("json"):
                    json_content = json_content[4:].strip()

            # Pydantic 객체 생성
            analysis_result = ResumeAnalysis.model_validate_json(json_content)

            resume_analysis = analysis_result.model_dump()
            recent_resume.analysis = resume_analysis
            
            self.resume_repo.update(resume_id=recent_resume.id, resume_data=recent_resume)

            print("📊 Resume Analysis Result:", analysis_result)

            return analysis_result

        except Exception as e:
            raise ValueError(f"이력서 분석 실패: {str(e)}")