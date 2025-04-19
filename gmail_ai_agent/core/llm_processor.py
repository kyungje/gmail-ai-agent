from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from ..config.settings import settings

class LLMProcessor:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=settings.OPENAI_MODEL_NAME,
            api_key=settings.OPENAI_API_KEY
        )
        
        self.system_prompt = """당신은 이메일 분석 전문가입니다. 
        주어진 이메일 내용을 분석하고 사용자의 질문에 대해 정확하고 상세하게 답변해주세요.
        답변할 때는 다음 사항을 고려하세요:
        1. 이메일의 주요 내용을 요약
        2. 중요한 정보나 행동이 필요한 사항 강조
        3. 맥락에 맞는 구체적인 답변 제공
        4. 필요한 경우 추가적인 조치나 팁 제공"""
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{question}\n\n이메일 내용:\n{email_content}")
        ])
        
        self.chain = (
            {"email_content": RunnablePassthrough(), "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
    
    def process_email(self, email_content: str, question: str) -> str:
        """이메일 내용을 분석하고 질문에 답변"""
        return self.chain.invoke({
            "email_content": email_content,
            "question": question
        }) 
        