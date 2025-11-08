# Resume Maker

AI 기반 맞춤형 이력서 생성 서비스

## 프로젝트 구조

```
resume_maker/
├── backend/                    # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py            # FastAPI 메인 애플리케이션
│   │   ├── api/
│   │   │   └── routes/        # API 라우트
│   │   │       ├── upload.py  # 파일 업로드
│   │   │       ├── chat.py    # 채팅/대화
│   │   │       ├── knowledge.py # 지식베이스 관리
│   │   │       └── generate.py # 이력서 생성
│   │   ├── agents/
│   │   │   ├── langgraph/     # LangGraph 구현
│   │   │   └── crewai/        # CrewAI 구현
│   │   ├── services/          # 비즈니스 로직
│   │   └── models/            # 데이터 모델
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/                   # Next.js 프론트엔드
    ├── app/
    │   ├── page.tsx           # 홈페이지
    │   ├── upload/            # PDF 업로드
    │   ├── chat/              # AI 인터뷰
    │   ├── knowledge/         # 지식베이스 편집
    │   └── generate/          # 이력서 생성
    ├── components/            # 재사용 컴포넌트
    ├── lib/
    │   └── api.ts            # API 클라이언트
    ├── package.json
    └── .env.local.example
```

## 기능

### 1. 이력서 업로드 및 분석
- PDF 이력서/경력기술서 업로드
- AI Agent가 자동 분석

### 2. 인터랙티브 인터뷰
- Agent가 꼬리질문을 통해 세부 정보 수집
- 충분한 정보를 얻을 때까지 반복

### 3. 지식 베이스 관리
- 수집된 정보를 구조화하여 저장
- 사용자가 직접 수정 가능

### 4. JD 맞춤형 이력서 생성
- Job Description 입력 (텍스트 또는 URL)
- 지식 베이스 기반 맞춤형 이력서 생성
- PDF 다운로드

## 기술 스택

### Backend
- **FastAPI**: 웹 프레임워크
- **LangGraph**: Agent 워크플로우 (기본)
- **CrewAI**: Agent 구현 (추가 옵션)
- **LangChain**: LLM 통합
- **PyPDF2**: PDF 처리

### Frontend
- **Next.js 14**: React 프레임워크
- **TypeScript**: 타입 안정성
- **Tailwind CSS**: 스타일링
- **shadcn/ui**: UI 컴포넌트 (선택 사항)
- **Axios**: HTTP 클라이언트

## 시작하기

### Backend 설정

```bash
cd backend

# 가상환경 생성 (Python 3.10+)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일에 API 키 입력

# 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend 설정

```bash
cd frontend

# 의존성 설치
npm install

# 환경 변수 설정
cp .env.local.example .env.local

# 개발 서버 실행
npm run dev
```

## API 엔드포인트

### Upload
- `POST /api/upload/resume` - 이력서 업로드
- `POST /api/upload/portfolio` - 포트폴리오 업로드

### Chat
- `POST /api/chat/message` - 메시지 전송
- `POST /api/chat/stream` - 스트리밍 응답
- `GET /api/chat/status/{session_id}` - 대화 상태 조회

### Knowledge
- `GET /api/knowledge/{session_id}` - 지식베이스 조회
- `PUT /api/knowledge/update` - 지식베이스 업데이트
- `POST /api/knowledge/rebuild/{session_id}` - 지식베이스 재구축

### Generate
- `POST /api/generate/` - 이력서 생성
- `GET /api/generate/status/{job_id}` - 생성 상태 확인
- `GET /api/generate/download/{job_id}` - 이력서 다운로드
- `POST /api/generate/advice` - 이력서 조언

## MVP 스코프

### 기능 1: 지식 베이스 구축
- 이력서 PDF 업로드
- Agent가 꼬리질문 (자동으로 충분성 판단)
- 지식 베이스 저장 (in-memory)

### 기능 2: JD 맞춤형 이력서 생성
- JD 입력 (텍스트 or URL)
- 지식 베이스 기반 이력서 생성
- PDF 출력

### 옵션 기능
- LinkedIn, Wanted 등 외부 툴 연동
- Web crawling (firecrawl, playwright)

## 다음 단계

- [ ] LangGraph Agent 구현
- [ ] LLM 통합 (OpenAI/Anthropic)
- [ ] PDF 생성 고도화
- [ ] 지식 베이스 구조 최적화
- [ ] 데이터베이스 연동 (PostgreSQL + JSONB)
- [ ] 인증/세션 관리
- [ ] CrewAI 버전 구현

## 팀

- **국준 (Jude)**: LangGraph, CrewAI
- **세호**: Autogen, Haystack
- **유림**: Haystack, LangGraph
- **준환**: CrewAI, Autogen
