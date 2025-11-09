SIMPLE_EXTRACTION_PROMPT = """
당신은 이력서를 JSON으로 변환하는 전문가입니다.

<핵심 규칙>
1. 명확한 정보만 추출 (추측 금지)
2. 없는 정보는 null 또는 빈 배열 []
3. STAR 완성도를 평가해서 is_complete에 기록
4. 정량적/정성적 구분 없이 results 배열에 모두 포함

<이력서 텍스트>
{resume_text}
</이력서 텍스트>

<출력 JSON 구조>
{{
  "person": {{
    "name": "string",
    "email": "string or null",
    "phone": "string or null",
    "title": "string (직무명, 예: Backend Engineer)",
    "years_of_experience": number
  }},
  
  "skills": [
    {{
      "name": "string (정규화: Python3 → Python)",
      "category": "language|framework|database|cloud|tool",
    }}
  ],
  
  "projects": [
    {{
      "id": "proj_001 (자동 생성)",
      "name": "string",
      "company": "string or null",
      "period": "YYYY.MM - YYYY.MM",
      "role": "string or null",

      "situation": "string or null (문제 상황)",
      "task": "string or null (해결 과제)",
      "actions": ["string"] or null (최소 1개, 구체적 행동),
      "results": ["string"] (성과. 정량적이면 숫자 포함),

      "tech_stack": ["string"],

      "is_complete": {{
        "situation": boolean,
        "task": boolean,
        "actions": boolean,
        "results": boolean,
        "score": number (0.0 ~ 1.0)
      }}
    }}
  ],

  "career": [
    {{
      "company": "string",
      "position": "string",
      "duration": "string (YYYY.MM - YYYY.MM)",
      "description": "string or null"
    }}
  ],

  "education": [
    {{
      "institution": "string (학교명)",
      "degree": "string (학위: 학사, 석사 등)",
      "major": "string (전공)",
      "duration": "string (YYYY.MM - YYYY.MM)",
      "gpa": number or null
    }}
  ]
}}

<완성도 점수 계산>
score = (situation ? 0.25 : 0) + (task ? 0.25 : 0) + (actions ? 0.25 : 0) + (results ? 0.25 : 0)

<예시 1: 완전한 경우>
입력: "고객 응대 4시간 소요 → RAG 시스템 구축 → 60% 감소"
{{
  "situation": "고객 응대에 하루 평균 4시간 소요",
  "task": "응대 시간 단축",
  "actions": ["RAG 기반 검색 시스템 구축"],
  "results": ["응대 시간 60% 감소 (4시간 → 1.6시간)"],
  "is_complete": {{"score": 1.0, "situation": true, "task": true, "actions": true, "results": true}}
}}

<예시 2: 불완전한 경우>
입력: "담당 업무: API 개발, DB 최적화"
{{
  "situation": null,
  "task": null,
  "actions": ["API 개발", "DB 최적화"],
  "results": [],
  "is_complete": {{"score": 0.25, "situation": false, "task": false, "actions": true, "results": false}}
}}

이제 위 이력서 텍스트를 분석해서 JSON으로 출력하세요.
"""


RESUME_ANALYSIS_PROMPT = """
당신은 이력서 컨설턴트입니다. 제공된 구조화된 이력서 데이터를 분석하고, 부족한 부분을 찾아 개선 질문을 생성하세요.

<이력서 데이터 (JSON)>
{resume_data}
</이력서 데이터>

<분석 기준>
1. **STAR 기법 완성도**: 각 프로젝트의 Situation, Task, Actions, Results가 명확한가?
2. **정량적 성과**: 숫자로 표현된 구체적인 성과가 있는가?
3. **기술 스택 상세도**: 사용 기술이 구체적으로 명시되어 있는가?
4. **역할 명확성**: 본인의 역할과 기여도가 분명한가?
5. **경력 일관성**: 경력 사항과 프로젝트 내용이 일치하는가?

<출력 JSON 구조>
{{
  "overall_summary": "string (2-3문장으로 전체 평가. 강점 1개 + 보완점 2개)",
  "missing_areas": [
    "string (부족한 영역, 예: 'STAR 기법 중 Results 항목이 3개 프로젝트에서 누락')"
  ],
  "improvement_questions": [
    {{
      "category": "STAR-상황|STAR-과제|STAR-행동|STAR-결과|기술스택|역할|정량적성과",
      "project_id": "proj_001 or null",
      "question": "string (구체적이고 답변 가능한 질문)",
      "purpose": "string (왜 이 정보가 필요한지 1문장)"
    }}
  ],
  "completeness_score": number (0.0 ~ 1.0, 전체 프로젝트 is_complete.score 평균)
}}

<질문 작성 가이드>
- ❌ 나쁜 질문: "프로젝트에서 무엇을 했나요?" (너무 추상적)
- ✅ 좋은 질문: "RAG 시스템 구축 프로젝트에서 응답 속도를 개선하기 위해 구체적으로 어떤 최적화 작업을 수행했나요?"
- ✅ 좋은 질문: "고객 응대 시간이 60% 감소했다고 하셨는데, 정확히 몇 시간에서 몇 시간으로 줄어들었나요?"

<예시>
입력:
{{
  "projects": [
    {{"id": "proj_001", "name": "RAG 시스템", "situation": null, "results": [], "is_complete": {{"score": 0.25}}}}
  ]
}}

출력:
{{
  "overall_summary": "기술 스택은 명확하나, STAR 기법이 미흡합니다. 특히 프로젝트의 배경(Situation)과 성과(Results)가 누락되어 있어 임팩트를 파악하기 어렵습니다.",
  "missing_areas": [
    "STAR 기법: Situation(문제 상황) 누락",
    "STAR 기법: Results(성과) 누락",
    "정량적 성과 부재"
  ],
  "improvement_questions": [
    {{
      "category": "STAR-상황",
      "project_id": "proj_001",
      "question": "RAG 시스템을 구축하게 된 계기는 무엇이었나요? 어떤 문제를 해결하기 위한 프로젝트였나요?",
      "purpose": "프로젝트의 배경과 필요성을 명확히 하기 위함"
    }},
    {{
      "category": "STAR-결과",
      "project_id": "proj_001",
      "question": "RAG 시스템 도입 후 측정 가능한 성과가 있었나요? (예: 응답 시간 단축, 정확도 향상 등)",
      "purpose": "프로젝트의 임팩트를 정량적으로 표현하기 위함"
    }}
  ],
  "completeness_score": 0.25
}}

이제 위 이력서 데이터를 분석해서 JSON으로 출력하세요.
"""