from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.session_manager import session_manager

router = APIRouter()


class ChatMessage(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    is_complete: bool
    knowledge_base: dict = {}


@router.post("/message", response_model=ChatResponse)
async def send_message(chat: ChatMessage):
    """
    Agent와 대화 (꼬리질문에 답변)
    """
    try:
        # TODO: AI 문답 진행
        
        return


    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"메시지 처리 중 오류: {str(e)}")


@router.get("/status/{session_id}")
async def get_chat_status(session_id: str):
    """
    현재 대화 상태 조회
    """
    try:
        session = session_manager.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")

        return {
            "session_id": session_id,
            "is_complete": session.is_complete,
            "question_count": session.question_count
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"상태 조회 중 오류: {str(e)}")
