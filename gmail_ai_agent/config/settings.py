from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_MODEL_NAME: str = "gpt-4o-mini"
    GMAIL_CLIENT_ID: str
    GMAIL_CLIENT_SECRET: str
    GMAIL_REDIRECT_URI: str
    VECTOR_STORE_PATH: str = "data/vector_store"
    RAG_ENABLED: bool = True
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    class Config:
        env_file = ".env"
        case_sensitive = True

# .env 파일 직접 읽기
env_file_path = os.path.join(os.getcwd(), '.env')
print(f".env 파일 경로: {env_file_path}")
print(f".env 파일 존재: {os.path.exists(env_file_path)}")

if os.path.exists(env_file_path):
    with open(env_file_path, 'r') as f:
        env_content = f.read()
        print("\n.env 파일 내용:")
        print(env_content)
        
        # .env 파일에서 RAG_ENABLED 값 직접 추출
        rag_enabled_in_env = False
        for line in env_content.splitlines():
            if line.startswith("RAG_ENABLED="):
                value = line.split("=", 1)[1].strip().lower()
                rag_enabled_in_env = value in ["true", "1", "yes", "y", "on"]
                print(f".env 파일 내 RAG_ENABLED 값: {value} -> {rag_enabled_in_env}")
                break

settings = Settings()

# 환경 변수 무시하고 .env 파일 값 강제 적용
if os.path.exists(env_file_path):
    settings.RAG_ENABLED = rag_enabled_in_env

print(f"최종 settings.RAG_ENABLED: {settings.RAG_ENABLED}")