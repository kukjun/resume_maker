"""
LangGraph Workflow - 이력서 코칭 대화 그래프
"""
from math import e
from langgraph.graph import StateGraph, END
from sqlalchemy.orm import Session

from app.agents.state import ResumeCoachState
from app.agents.nodes import (
    load_resume_node,
    update_resume_node,
    select_question_node,
    generate_response_node,
    completion_node,
    should_continue
)

from langgraph.checkpoint.postgres import PostgresSaver

from app.database.config import DATABASE_URL

def create_resume_coach_graph(db: Session):
    """
    이력서 코칭 대화 그래프 생성

    Args:
        db: SQLAlchemy 세션

    Returns:
        Compiled LangGraph
    """
    
    try:
        with PostgresSaver.from_conn_string(DATABASE_URL) as checkpointer:
            # checkpointer.setup()
            # StateGraph 생성
            builder = StateGraph(ResumeCoachState)
            
            


            # 그래프 컴파일
            return builder.compile(checkpointer=checkpointer)
    except Exception as e:
        print(e)
        raise e
        
        


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
    # 초기 상태 생성 (PostgresSaver가 상태를 자동 관리)
    initial_state: ResumeCoachState = {
        "session_id": session_id,
        "user_id": user_id,
        "user_answer": user_answer,
        "current_resume_data": None,
        "current_analysis": None,
        "improvement_questions": [],
        "current_question_index": 0,
        "current_question": None,
        "answered_count": 0,
        "is_completed": False,
        "response": None
    }

    # 그래프 생성 및 실행 (thread_id로 세션 관리)
    graph = create_resume_coach_graph(db)
    config = {"configurable": {"thread_id": session_id}}
    result = await graph.ainvoke(initial_state, config)

    # 결과 반환
    return {
        "response": result.get("response", ""),
        "is_completed": result.get("is_completed", False),
        "answered_count": result.get("answered_count", 0),
        "current_question_index": result.get("current_question_index", 0)
    }
