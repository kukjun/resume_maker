"""
LangGraph Nodes - 이력서 코칭 대화 노드들
"""
import json
from typing import Optional
from sqlalchemy.orm import Session
from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage

from app.agents.state import ResumeCoachState
from app.agents.prompts import (
    RESUME_UPDATE_PROMPT,
    QUESTION_RESPONSE_PROMPT,
    COMPLETION_MESSAGE_PROMPT
)
from app.repositories import ResumeRepository, ConversationRepository
from app.models.schemas import ResumeExtraction, ResumeAnalysis


async def load_conversation_node(state: ResumeCoachState, db: Session) -> ResumeCoachState:
    """
    대화 세션과 이력서 데이터를 DB에서 로드
    """
    conversation_repo = ConversationRepository(db)
    resume_repo = ResumeRepository(db)

    # 대화 세션 조회
    conversation = conversation_repo.get_by_session_id(state["session_id"])

    if conversation:
        # 기존 세션 로드
        state["messages"] = conversation.messages
        state["current_question_index"] = conversation.current_question_index
        state["answered_count"] = conversation.answered_count
        state["is_completed"] = conversation.is_completed
    else:
        # 새 세션 생성
        conversation = conversation_repo.create(
            session_id=state["session_id"],
            user_id=state["user_id"],
            messages=[]
        )
        state["messages"] = []
        state["current_question_index"] = 0
        state["answered_count"] = 0
        state["is_completed"] = False

    # 최근 이력서 데이터 로드
    recent_resume = resume_repo.get_recent_resume_by_user_id(state["user_id"])

    if recent_resume:
        state["current_resume_data"] = recent_resume.data
        state["current_analysis"] = recent_resume.analysis

        # improvement_questions 추출
        if recent_resume.analysis:
            state["improvement_questions"] = recent_resume.analysis.get("improvement_questions", [])
        else:
            state["improvement_questions"] = []
    else:
        raise ValueError(f"사용자 {state['user_id']}의 이력서를 찾을 수 없습니다.")

    return state


async def update_resume_node(state: ResumeCoachState, db: Session) -> ResumeCoachState:
    """
    사용자 답변을 기반으로 이력서 업데이트
    (기존 이력서 데이터 + 질문 + 답변) → LLM → 업데이트된 이력서
    """
    if not state.get("user_answer") or not state.get("current_question"):
        # 답변이 없으면 업데이트 스킵
        return state

    try:
        # 현재 질문과 답변
        current_question = state["current_question"]
        user_answer = state["user_answer"]

        # 기존 이력서 데이터
        resume_json = json.dumps(state["current_resume_data"], ensure_ascii=False, indent=2)

        # LLM으로 업데이트
        model = init_chat_model("gpt-4o-mini", temperature=0.3)

        system_prompt = RESUME_UPDATE_PROMPT.format(
            resume_data=resume_json,
            question=current_question.get("question", ""),
            answer=user_answer
        )

        response = model.invoke([SystemMessage(content=system_prompt)])
        json_content = response.content

        # JSON 파싱
        if not isinstance(json_content, str):
            raise ValueError(f"LLM 응답이 문자열이 아닙니다: {type(json_content)}")

        # 마크다운 코드블록 제거
        if json_content.startswith("```"):
            json_content = json_content.split("```")[1]
            if json_content.startswith("json"):
                json_content = json_content[4:].strip()

        # Pydantic 객체로 검증
        updated_resume = ResumeExtraction.model_validate_json(json_content)

        # 상태 업데이트
        state["current_resume_data"] = updated_resume.model_dump()

        # DB에 저장
        resume_repo = ResumeRepository(db)
        recent_resume = resume_repo.get_recent_resume_by_user_id(state["user_id"])

        if recent_resume:
            recent_resume.data = state["current_resume_data"]  # type: ignore
            resume_repo.update(resume_id=recent_resume.id, resume_data=recent_resume)

        # 카운터 증가 (답변 후)
        state["answered_count"] += 1
        state["current_question_index"] += 1

        print(f"✅ Resume updated with answer to question {state['current_question_index'] - 1}, total answered: {state['answered_count']}")

    except Exception as e:
        print(f"⚠️ Resume update failed: {str(e)}")
        # 업데이트 실패해도 대화는 계속 진행

    return state


async def select_question_node(state: ResumeCoachState) -> ResumeCoachState:
    """
    다음 질문 선택
    """
    improvement_questions = state.get("improvement_questions", [])
    current_index = state.get("current_question_index", 0)

    # 질문이 남아있고, 5개 미만이면 다음 질문 선택
    if current_index < len(improvement_questions) and state["answered_count"] < 5:
        state["current_question"] = improvement_questions[current_index]
        state["is_completed"] = False
    else:
        # 질문이 없거나 5개 완료
        state["current_question"] = None
        state["is_completed"] = True

    return state


async def generate_response_node(state: ResumeCoachState) -> ResumeCoachState:
    """
    자연스러운 응답 생성
    """
    current_question = state.get("current_question")

    if not current_question:
        # 질문이 없으면 완료 메시지
        return state

    try:
        # LLM으로 자연스러운 응답 생성
        model = init_chat_model("gpt-4o-mini", temperature=0.7)

        system_prompt = QUESTION_RESPONSE_PROMPT.format(
            category=current_question.get("category", ""),
            question=current_question.get("question", ""),
            purpose=current_question.get("purpose", "")
        )

        response = model.invoke([SystemMessage(content=system_prompt)])

        state["response"] = response.content

    except Exception as e:
        # 응답 생성 실패하면 질문 그대로 사용
        state["response"] = current_question.get("question", "")

    return state


async def completion_node(state: ResumeCoachState) -> ResumeCoachState:
    """
    대화 완료 메시지 생성
    """
    answered_count = state.get("answered_count", 0)
    improvement_questions = state.get("improvement_questions", [])

    # 완료 사유 결정
    if answered_count >= 5:
        completion_reason = "5개 질문 완료"
    elif len(improvement_questions) == 0:
        completion_reason = "개선할 부분이 없습니다"
    else:
        completion_reason = "모든 질문 완료"

    try:
        # LLM으로 완료 메시지 생성
        model = init_chat_model("gpt-4o-mini", temperature=0.7)

        system_prompt = COMPLETION_MESSAGE_PROMPT.format(
            completion_reason=completion_reason
        )

        response = model.invoke([SystemMessage(content=system_prompt)])

        state["response"] = response.content

    except Exception as e:
        # 응답 생성 실패하면 기본 메시지
        state["response"] = f"감사합니다! {completion_reason}. 업데이트된 이력서를 확인해보세요."

    state["is_completed"] = True

    return state


async def save_conversation_node(state: ResumeCoachState, db: Session) -> ResumeCoachState:
    """
    대화 상태를 DB에 저장
    """
    conversation_repo = ConversationRepository(db)

    # 메시지 추가
    if state.get("user_answer"):
        state["messages"].append({
            "role": "user",
            "content": state["user_answer"]
        })

    if state.get("response"):
        state["messages"].append({
            "role": "assistant",
            "content": state["response"]
        })

    # DB 업데이트
    conversation_repo.update(
        session_id=state["session_id"],
        messages=state["messages"],
        current_question_index=state["current_question_index"],
        answered_count=state["answered_count"],
        is_completed=state["is_completed"]
    )

    return state


def should_continue(state: ResumeCoachState) -> str:
    """
    대화 계속 여부 결정 (라우팅 함수)
    """
    # 5개 질문 완료 또는 질문이 없으면 종료
    if state["is_completed"]:
        return "complete"

    # 계속 진행
    return "continue"
