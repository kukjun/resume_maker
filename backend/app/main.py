from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.routes import upload, chat, knowledge, generate
from app.core.config import setup_langsmith
from app.database.config import init_db

# 환경 변수 로드
load_dotenv()

# LangSmith 초기화 (추적 활성화)
setup_langsmith()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🚀 앱 시작 시
    print("🚀 Initializing database...")
    init_db()
    yield
    # 🧹 앱 종료 시 (optional)
    print("🧹 Shutting down...")


app = FastAPI(
    lifespan=lifespan,
    title="Resume Maker API",
    description="AI-powered resume customization service",
    version="1.0.0"
)


# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js 개발 서버
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["knowledge"])
app.include_router(generate.router, prefix="/api/generate", tags=["generate"])

@app.get("/")
async def root():
    return {"message": "Resume Maker API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
