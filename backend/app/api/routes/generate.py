from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import uuid
import os
import tempfile

router = APIRouter()

# 생성된 이력서를 임시 저장할 딕셔너리
generated_resumes = {}


class GenerateRequest(BaseModel):
    session_id: str
    jd_text: str


@router.post("/")
async def generate_resume(request: GenerateRequest):
    """
    JD 기반 맞춤형 이력서 생성
    """
    try:
        # TODO: 구현 필요
        return

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"이력서 생성 중 오류: {str(e)}")


@router.get("/download/{job_id}")
async def download_resume(job_id: str):
    """
    생성된 이력서 다운로드
    """
    # TODO: 구현 필요
    return 


@router.get("/preview/{job_id}")
async def preview_resume(job_id: str):
    """
    생성된 이력서 마크다운 미리보기
    """
    # TODO: 구현 필요
    return
