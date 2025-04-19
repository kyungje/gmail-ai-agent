from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ..core.agent import EmailAgent
from ..config.settings import settings
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Gmail AI Agent API")
agent = EmailAgent()

class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    try:
        logger.info(f"Received question: {request.question}")
        answer = agent.run(request.question)
        logger.info("Successfully processed question")
        return QuestionResponse(answer=answer)
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}