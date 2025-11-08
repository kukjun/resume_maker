import tempfile
import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


class UserResumeService:
    """
    사용자 이력서 관련 서비스
    """

    def __init__(self):
        """초기화"""
        pass
    
    def create_resume_knowledge_base(self, documents: List[Document]):
        """
        이력서 문서들로 지식 베이스 생성 (추후 구현)

        Args:
            documents: 이력서에서 추출한 Document 리스트

        Returns:
            지식 베이스 객체 (구현 필요)
        """
        
        # Documents 문서를 잘 정리해서 OPENAI API로 SYSTEM PROMPT로 넘겨줌.
        # JSON 구조를 써서 결과를 가져올 수 있도록 하는데, 요구사항으로 원하는 DATA 구조를 같이 제공함.
        
        
        pass
        
        

    def extract_text_from_pdfs(self, pdf_contents: List[bytes]) -> List[Document]:
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

    def load_resume_from_pdf(self, file_path: str) -> List[Document]:
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


user_resume_service = UserResumeService()