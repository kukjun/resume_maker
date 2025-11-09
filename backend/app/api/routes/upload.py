from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.services.user_resume_service import UserResumeService
from app.database import get_db
import uuid

router = APIRouter()


@router.post("/resume")
async def upload_resume(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
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


        # PDF 파일들을 bytes로 읽기
        pdf_contents = [await file.read() for file in files]

        # UserResumeService 인스턴스 생성
        user_resume_service = UserResumeService(db)

        # 임시 user_id (추후 인증 구현 시 실제 user_id 사용)
        user_id = "1"

        # 세션 ID 생성
        session_id = f"session-{uuid.uuid4()}"

        # 이력서 처리 및 저장
        is_done = await user_resume_service.create_user_resume(
            pdf_contents=pdf_contents,
            user_id=user_id
        )

        if not is_done:
            raise HTTPException(status_code=500, detail="이력서 처리 실패")


        analyze_resume = await user_resume_service.analyze_resume(user_id=user_id)
        first_question = analyze_resume.overall_summary


        return {
            "session_id": session_id,
            "user_id": user_id,
            "first_question": first_question,
            "files_processed": len(files),
            "filenames": [file.filename for file in files]
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"업로드 처리 중 오류: {str(e)}")

