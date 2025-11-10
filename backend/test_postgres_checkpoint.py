"""
PostgreSQL Checkpointer 간단한 테스트
"""
import asyncio
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.runnables import RunnableConfig
from typing import Annotated
from typing_extensions import TypedDict
from operator import add

# State 정의
class State(TypedDict, total=False):
    foo: str
    bar: Annotated[list[str], add]

# 노드 함수들
def node_a(state: State):
    print("Node A 실행")
    return {"foo": "a", "bar": ["a"]}

def node_b(state: State):
    print("Node B 실행")
    return {"foo": "b", "bar": ["b"]}

# 테스트 실행
def test_graph():
    print("=== PostgreSQL Checkpointer 테스트 시작 ===\n")

    # PostgreSQL 연결 정보
    DATABASE_URL = "postgresql://resume_user:resume_password@localhost:5433/resume_maker"

    # with 블록 내에서 checkpointer 사용
    with PostgresSaver.from_conn_string(DATABASE_URL) as checkpointer:
        checkpointer.setup()  # 테이블 생성

        # StateGraph 생성
        workflow = StateGraph(State)
        workflow.add_node("node_a", node_a)
        workflow.add_node("node_b", node_b)
        workflow.add_edge(START, "node_a")
        workflow.add_edge("node_a", "node_b")
        workflow.add_edge("node_b", END)

        # 그래프 컴파일
        graph = workflow.compile(checkpointer=checkpointer)

        # 설정 (thread_id로 세션 관리)
        config: RunnableConfig = {"configurable": {"thread_id": "test-thread-1"}}

        # 첫 번째 실행
        print("📍 첫 번째 실행:")
        result1 = graph.invoke({"foo": "", "bar": []}, config)
        print(f"결과: {result1}\n")

        # 두 번째 실행 (같은 thread_id로 상태가 복원되는지 확인)
        print("📍 두 번째 실행 (같은 thread_id):")
        result2 = graph.invoke({"foo": "initial"}, config)
        print(f"결과: {result2}\n")

        # 다른 thread_id로 실행
        print("📍 세 번째 실행 (다른 thread_id):")
        config2: RunnableConfig = {"configurable": {"thread_id": "test-thread-2"}}
        result3 = graph.invoke({"foo": "", "bar": []}, config2)
        print(f"결과: {result3}\n")

        print("=== 테스트 완료 ===")

if __name__ == "__main__":
    test_graph()
