from crewai import Agent, Task, Crew, Process

# TODO: CrewAI 구현 (추후)
"""
CrewAI 기반 구현
- Resume Analyzer Agent
- Question Generator Agent
- Knowledge Builder Agent
- Resume Generator Agent
"""

def create_resume_analyzer_agent():
    """
    이력서 분석 Agent
    """
    return Agent(
        role='Resume Analyzer',
        goal='이력서에서 핵심 정보를 추출하고 부족한 부분을 파악',
        backstory='당신은 경력 컨설턴트입니다.',
        verbose=True,
        allow_delegation=False
    )

def create_question_generator_agent():
    """
    질문 생성 Agent
    """
    return Agent(
        role='Question Generator',
        goal='사용자의 경력을 더 잘 이해하기 위한 효과적인 질문 생성',
        backstory='당신은 인터뷰 전문가입니다.',
        verbose=True,
        allow_delegation=False
    )

def create_resume_writer_agent():
    """
    이력서 작성 Agent
    """
    return Agent(
        role='Resume Writer',
        goal='JD에 최적화된 이력서 작성',
        backstory='당신은 전문 이력서 작성 컨설턴트입니다.',
        verbose=True,
        allow_delegation=False
    )

# TODO: Crew 구성
