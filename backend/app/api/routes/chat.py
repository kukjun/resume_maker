from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.agents import run_resume_coach

router = APIRouter()


class ChatMessage(BaseModel):
    session_id: str
    user_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    is_completed: bool
    answered_count: int
    current_question_index: int


@router.post("/message", response_model=ChatResponse)
async def send_message(chat: ChatMessage, db: Session = Depends(get_db)):
    """
    Agent와 대화 (꼬리질문에 답변)

    Args:
        chat: 채팅 메시지 (session_id, user_id, message)
        db: DB 세션

    Returns:
        ChatResponse: {
            response: 응답 메시지,
            is_completed: 대화 완료 여부,
            answered_count: 답변한 질문 수,
            current_question_index: 현재 질문 인덱스
        }
    """
    try:
        # LangGraph 대화 실행
        result = await run_resume_coach(
            session_id=chat.session_id,
            user_id=chat.user_id,
            user_answer=chat.message,
            db=db
        )

        return ChatResponse(
            response=result["response"],
            is_completed=result["is_completed"],
            answered_count=result["answered_count"],
            current_question_index=result["current_question_index"]
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"메시지 처리 중 오류: {str(e)}")


@router.get("/status/{session_id}")
async def get_chat_status(session_id: str, db: Session = Depends(get_db)):
    """
    현재 대화 상태 조회

    Args:
        session_id: 세션 ID
        db: DB 세션

    Returns:
        dict: 대화 상태 정보
    """
    try:
        from app.repositories import ConversationRepository

        conversation_repo = ConversationRepository(db)
        conversation = conversation_repo.get_by_session_id(session_id)

        if not conversation:
            raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")

        return {
            "session_id": conversation.session_id,
            "user_id": conversation.user_id,
            "is_completed": conversation.is_completed,
            "answered_count": conversation.answered_count,
            "current_question_index": conversation.current_question_index,
            "message_count": len(conversation.messages)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"상태 조회 중 오류: {str(e)}")
