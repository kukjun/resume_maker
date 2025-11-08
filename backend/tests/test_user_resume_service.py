"""
UserResumeService 테스트 (pytest 형식)
"""
from typing import List
from langchain_core.documents import Document
from app.services.user_resume_service import user_resume_service


class TestExtractTextFromPdfs:
    """PDF 텍스트 추출 테스트"""

    def test_extract_single_pdf(self, resume_pdf_bytes: bytes):
        """단일 PDF에서 텍스트 추출"""
        # Given: TEST_RESUME.pdf bytes
        # When: extract_text_from_pdfs 호출
        documents = user_resume_service.extract_text_from_pdfs([resume_pdf_bytes])

        # Then: Document가 정상적으로 추출됨
        assert len(documents) > 0, "Document가 하나도 추출되지 않았습니다"
        assert all(isinstance(doc, Document) for doc in documents), "모든 객체가 Document 타입이어야 합니다"

        # 전체 텍스트 길이 확인
        total_chars = sum(len(doc.page_content) for doc in documents)
        assert total_chars > 0, "텍스트가 추출되지 않았습니다"

        # 결과 출력
        print(f"\n📄 추출된 Document 개수: {len(documents)}개")
        print(f"📊 총 텍스트 길이: {total_chars:,}자")

    def test_extract_multiple_pdfs(
        self,
        resume_pdf_bytes: bytes,
        career_pdf_bytes: bytes,
    ):
        """여러 PDF를 한 번에 처리"""
        # Given: 두 개의 다른 PDF bytes
        pdf_contents = [resume_pdf_bytes, career_pdf_bytes]

        # When: extract_text_from_pdfs 호출
        documents = user_resume_service.extract_text_from_pdfs(pdf_contents)

        # Then: 모든 PDF에서 Document가 추출됨
        assert len(documents) > 0, "Document가 하나도 추출되지 않았습니다"
        assert len(documents) >= len(pdf_contents), "PDF 개수보다 적은 Document가 추출되었습니다"

        # 각 PDF에서 Document가 추출되었는지 확인
        for pdf_idx in range(len(pdf_contents)):
            docs_from_pdf = [doc for doc in documents if doc.metadata.get('source_pdf_index') == pdf_idx]
            assert len(docs_from_pdf) > 0, f"PDF {pdf_idx + 1}에서 Document가 추출되지 않았습니다"

        # 결과 출력
        total_chars = sum(len(doc.page_content) for doc in documents)
        print(f"\n📄 총 {len(pdf_contents)}개 PDF에서 추출된 Document 개수: {len(documents)}개")
        print(f"📊 총 텍스트 길이: {total_chars:,}자")

        # PDF별 상세 정보
        pdf_names = ["TEST_RESUME.pdf", "TEST_CAREER.pdf"]
        for pdf_idx in range(len(pdf_contents)):
            docs_from_pdf = [doc for doc in documents if doc.metadata.get('source_pdf_index') == pdf_idx]
            chars_from_pdf = sum(len(doc.page_content) for doc in docs_from_pdf)
            pdf_name = pdf_names[pdf_idx] if pdf_idx < len(pdf_names) else f"PDF {pdf_idx + 1}"
            print(f"\n📄 {pdf_name}: {len(docs_from_pdf)}개 Document, {chars_from_pdf:,}자")


class TestDocumentStructure:
    """Document 구조 검증 테스트"""

    def test_document_has_required_metadata(self, resume_documents: List[Document]):
        """Document가 필수 메타데이터를 포함하는지 확인"""
        # Given: resume_documents fixture
        # When/Then: 각 Document가 필수 메타데이터를 가지고 있음
        for doc in resume_documents:
            assert 'source' in doc.metadata, "source 메타데이터가 없습니다"
            assert 'page' in doc.metadata, "page 메타데이터가 없습니다"
            assert 'source_pdf_index' in doc.metadata, "source_pdf_index 메타데이터가 없습니다"

    def test_document_has_content(self, resume_documents: List[Document]):
        """Document가 내용을 포함하는지 확인"""
        # Given: resume_documents fixture
        # When/Then: 모든 Document가 텍스트 내용을 가지고 있음
        for doc in resume_documents:
            assert isinstance(doc.page_content, str), "page_content가 문자열이 아닙니다"
            assert len(doc.page_content) > 0, "page_content가 비어있습니다"

    def test_document_page_numbers(self, resume_documents: List[Document]):
        """Document의 페이지 번호가 순차적인지 확인"""
        # Given: resume_documents fixture
        # When: 페이지 번호 추출
        page_numbers = [doc.metadata.get('page') for doc in resume_documents]

        # Then: 페이지 번호가 0부터 시작하는 순차적인 숫자
        assert page_numbers == list(range(len(resume_documents))), "페이지 번호가 순차적이지 않습니다"

    def test_source_pdf_index_consistency(self, all_documents: List[Document]):
        """여러 PDF의 source_pdf_index가 올바른지 확인"""
        # Given: all_documents fixture (2개의 PDF)
        # When: source_pdf_index 추출
        pdf_indices = set(doc.metadata.get('source_pdf_index') for doc in all_documents)

        # Then: 0과 1만 존재
        assert pdf_indices == {0, 1}, "source_pdf_index가 올바르지 않습니다"


class TestDocumentFixtures:
    """Document fixtures 테스트"""

    def test_resume_documents_fixture(self, resume_documents: List[Document]):
        """resume_documents fixture가 올바르게 생성되는지 확인"""
        assert len(resume_documents) > 0, "resume_documents가 비어있습니다"
        print(f"\n✅ resume_documents: {len(resume_documents)}개 Document")

    def test_career_documents_fixture(self, career_documents: List[Document]):
        """career_documents fixture가 올바르게 생성되는지 확인"""
        assert len(career_documents) > 0, "career_documents가 비어있습니다"
        print(f"\n✅ career_documents: {len(career_documents)}개 Document")

    def test_all_documents_fixture(self, all_documents: List[Document]):
        """all_documents fixture가 올바르게 생성되는지 확인"""
        assert len(all_documents) > 0, "all_documents가 비어있습니다"

        # 두 개의 PDF에서 온 Document인지 확인
        pdf_indices = set(doc.metadata.get('source_pdf_index') for doc in all_documents)
        assert len(pdf_indices) == 2, "두 개의 PDF에서 추출되어야 합니다"

        print(f"\n✅ all_documents: {len(all_documents)}개 Document (from {len(pdf_indices)} PDFs)")

    def test_fixtures_are_cached(self, resume_documents: List[Document]):
        """Fixtures가 캐시되는지 확인 (session scope)"""
        # Given: resume_documents fixture
        # When: 같은 fixture를 다시 요청
        documents_again = resume_documents

        # Then: 같은 객체 (캐시됨)
        assert documents_again is resume_documents, "Fixture가 캐시되지 않았습니다"

