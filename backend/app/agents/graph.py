"""
LangGraph Workflow - 이력서 코칭 대화 그래프
"""
from langgraph.graph import StateGraph, END
from sqlalchemy.orm import Session

from app.agents.state import ResumeCoachState
from app.agents.nodes import (
    load_conversation_node,
    update_resume_node,
    select_question_node,
    generate_response_node,
    completion_node,
    save_conversation_node,
    should_continue
)


def create_resume_coach_graph(db: Session):
    """
    이력서 코칭 대화 그래프 생성

    Args:
        db: SQLAlchemy 세션

    Returns:
        Compiled LangGraph
    """
    # StateGraph 생성
    workflow = StateGraph(ResumeCoachState)

    # async 래퍼 함수들 정의 (db를 클로저로 캡처)
    async def _load_conversation(state):
        return await load_conversation_node(state, db)

    async def _update_resume(state):
        return await update_resume_node(state, db)

    async def _select_question(state):
        return await select_question_node(state)

    async def _generate_response(state):
        return await generate_response_node(state)

    async def _completion(state):
        return await completion_node(state)

    async def _save_conversation(state):
        return await save_conversation_node(state, db)

    # 노드 추가
    workflow.add_node("load_conversation", _load_conversation)
    workflow.add_node("update_resume", _update_resume)
    workflow.add_node("select_question", _select_question)
    workflow.add_node("generate_response", _generate_response)
    workflow.add_node("completion", _completion)
    workflow.add_node("save_conversation", _save_conversation)

    # 엣지 추가
    # 1. 시작: load_conversation
    workflow.set_entry_point("load_conversation")

    # 2. load_conversation → update_resume (사용자 답변이 있으면 업데이트)
    workflow.add_edge("load_conversation", "update_resume")

    # 3. update_resume → select_question (다음 질문 선택)
    workflow.add_edge("update_resume", "select_question")

    # 4. select_question → 조건부 분기
    workflow.add_conditional_edges(
        "select_question",
        should_continue,
        {
            "continue": "generate_response",  # 질문 계속
            "complete": "completion"  # 완료
        }
    )

    # 5. generate_response → save_conversation
    workflow.add_edge("generate_response", "save_conversation")

    # 6. completion → save_conversation
    workflow.add_edge("completion", "save_conversation")

    # 7. save_conversation → END
    workflow.add_edge("save_conversation", END)

    # 그래프 컴파일
    return workflow.compile()


async def run_resume_coach(
    session_id: str,
    user_id: str,
    user_answer: str,
    db: Session
) -> dict:
    """
    이력서 코칭 대화 실행

    Args:
        session_id: 세션 ID
        user_id: 사용자 ID
        user_answer: 사용자 답변
        db: SQLAlchemy 세션

    Returns:
        dict: {
            "response": str,  # 응답 메시지
            "is_completed": bool,  # 대화 완료 여부
            "answered_count": int,  # 답변한 질문 수
            "current_question_index": int  # 현재 질문 인덱스
        }
    """
    # 초기 상태 생성
    initial_state: ResumeCoachState = {
        "session_id": session_id,
        "user_id": user_id,
        "user_answer": user_answer,
        "messages": [],
        "current_resume_data": None,
        "current_analysis": None,
        "improvement_questions": [],
        "current_question_index": 0,
        "current_question": None,
        "answered_count": 0,
        "is_completed": False,
        "response": None
    }

    # 그래프 생성 및 실행
    graph = create_resume_coach_graph(db)
    result = await graph.ainvoke(initial_state)

    # 결과 반환 (카운터는 update_resume_node에서 이미 증가됨)
    return {
        "response": result.get("response", ""),
        "is_completed": result.get("is_completed", False),
        "answered_count": result.get("answered_count", 0),
        "current_question_index": result.get("current_question_index", 0)
    }
