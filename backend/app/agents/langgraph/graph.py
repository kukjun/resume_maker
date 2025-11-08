from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    """
    LangGraph Agent의 상태 정의
    """
    messages: Annotated[Sequence[BaseMessage], operator.add]
    resume_text: str
    knowledge_base: dict
    current_question: str
    question_count: int
    is_sufficient: bool  # 충분한 정보를 얻었는지
    jd_text: str
    generated_resume: str

# TODO: Agent 노드 정의
def analyze_resume(state: AgentState):
    """
    이력서 PDF 텍스트 분석
    """
    # TODO: LLM으로 이력서 분석
    # TODO: 초기 지식 베이스 구축
    return state

def generate_question(state: AgentState):
    """
    꼬리질문 생성
    """
    # TODO: 현재 지식 베이스 기반으로 부족한 부분 파악
    # TODO: 적절한 질문 생성
    return state

def process_answer(state: AgentState):
    """
    사용자 답변 처리 및 지식 베이스 업데이트
    """
    # TODO: 답변 내용 파싱
    # TODO: 지식 베이스 업데이트
    return state

def check_sufficiency(state: AgentState):
    """
    정보가 충분한지 판단
    """
    # TODO: LLM으로 충분성 판단
    if state["question_count"] >= 10:  # 임시: 10개 질문 후 종료
        return "sufficient"
    return "continue"

def generate_resume_from_jd(state: AgentState):
    """
    JD 기반 맞춤형 이력서 생성
    """
    # TODO: JD 분석
    # TODO: 지식 베이스와 매칭
    # TODO: 이력서 생성
    return state

# TODO: LangGraph 워크플로우 구성
def create_interview_graph():
    """
    이력서 인터뷰 그래프 생성
    """
    workflow = StateGraph(AgentState)

    # 노드 추가
    workflow.add_node("analyze_resume", analyze_resume)
    workflow.add_node("generate_question", generate_question)
    workflow.add_node("process_answer", process_answer)

    # 엣지 정의
    workflow.set_entry_point("analyze_resume")
    workflow.add_edge("analyze_resume", "generate_question")
    workflow.add_edge("process_answer", "generate_question")

    # 조건부 엣지
    workflow.add_conditional_edges(
        "generate_question",
        check_sufficiency,
        {
            "sufficient": END,
            "continue": "process_answer"
        }
    )

    return workflow.compile()

def create_resume_generation_graph():
    """
    이력서 생성 그래프
    """
    workflow = StateGraph(AgentState)

    workflow.add_node("generate_resume", generate_resume_from_jd)
    workflow.set_entry_point("generate_resume")
    workflow.add_edge("generate_resume", END)

    return workflow.compile()
