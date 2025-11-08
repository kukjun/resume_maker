from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.services.session_manager import session_manager

router = APIRouter()


@router.post("/resume")
async def upload_resume(files: List[UploadFile] = File(...)):
    """
    이력서 PDF 업로드 및 분석 시작 (여러 파일 지원)
    """
    try:
        # 파일 검증
        if not files:
            raise HTTPException(status_code=400, detail="업로드할 파일이 없습니다.")

        # PDF 파일 형식 검증
        for file in files:
            if not file.content_type == "application/pdf":
                raise HTTPException(
                    status_code=400,
                    detail=f"'{file.filename}'은(는) PDF 파일이 아닙니다."
                )
                
        

        # 세션 생성
        session_id = session_manager.create_session()

        # TODO: 추출된 텍스트로 첫 질문 생성
        first_question = "이력서가 업로드되었습니다. 어떤 부분을 개선하고 싶으신가요?"

        return {
            "session_id": session_id,
            "first_question": first_question,
            "files_processed": len(files),
            "filenames": [file.filename for file in files]
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"업로드 처리 중 오류: {str(e)}")

