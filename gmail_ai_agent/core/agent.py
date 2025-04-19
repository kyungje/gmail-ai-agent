from typing import Dict, Any, TypedDict, Annotated, Sequence
from langgraph.graph import Graph, StateGraph
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from .email_processor import EmailProcessor
from .llm_processor import LLMProcessor
from .rag_processor import RAGProcessor
from ..config.settings import settings

class AgentState(TypedDict):
    messages: Sequence[BaseMessage]
    email_content: str
    question: str
    response: str

class EmailAgent:
    def __init__(self):
        self.email_processor = EmailProcessor()
        self.llm_processor = LLMProcessor()
        print(f"RAG_ENABLED 설정값: {settings.RAG_ENABLED}")
        
        # RAG 활성화 여부에 따라 RAG 프로세서 초기화
        self.rag_processor = None
        if settings.RAG_ENABLED:
            print("RAG 기능 활성화 - 벡터 스토어 초기화 중...")
            self.rag_processor = RAGProcessor()
            print("RAG 기능 활성화 완료")
        else:
            print("RAG 기능 비활성화")
        
        # 도구 정의
        self.tools = [
            self.get_emails,
            self.process_email,
            self.search_emails
        ]
        
        # 그래프 정의
        self.workflow = self._create_workflow()
    
    def get_emails(self, tool_input: str = "") -> str:
        """이메일 목록을 가져옵니다."""
        try:
            emails = self.email_processor.get_emails(max_results=10)
            print(f"이메일 가져옴: {len(emails)}개")
            
            # RAG 프로세서가 활성화되어 있으면 이메일을 벡터 스토어에 추가
            if self.rag_processor:
                print("RAG 프로세서로 이메일 추가 시작")
                # 이메일을 RAG에 추가할 수 있는 형식으로 변환
                email_docs = []
                for email in emails:
                    email_doc = {
                        'subject': email.get('subject', ''),
                        'sender': email.get('from', ''),
                        'date': email.get('date', ''),
                        'body': email.get('body', '')
                    }
                    email_docs.append(email_doc)
                
                # 벡터 스토어에 이메일 추가
                self.rag_processor.add_documents(email_docs)
                print("RAG 프로세서로 이메일 추가 완료")
            else:
                print("RAG 프로세서가 비활성화되어 있음")
            
            return str(emails)
        except Exception as e:
            print(f"이메일 처리 중 오류 발생: {str(e)}")
            return str(e)
    
    def process_email(self, email_content: str, question: str) -> str:
        """이메일 내용을 분석하고 질문에 답변합니다."""
        try:
            # 이메일 내용이 너무 길 경우 잘라내기
            max_tokens = 80000  
            if len(email_content) > max_tokens:
                email_content = email_content[:max_tokens] + "... (이하 생략)"
            
            return self.llm_processor.process_email(email_content, question)
        except Exception as e:
            return str(e)
    
    def search_emails(self, tool_input: str) -> str:
        """RAG를 사용하여 관련 이메일을 검색합니다."""
        try:
            if not self.rag_processor:
                return "RAG가 비활성화되어 있습니다."
            results = self.rag_processor.search(tool_input)
            
            # 검색 결과를 사람이 읽기 쉬운 형태로 변환
            formatted_results = []
            for i, doc in enumerate(results, 1):
                formatted_result = f"[이메일 {i}]\n"
                formatted_result += f"제목: {doc.metadata['subject']}\n"
                formatted_result += f"발신자: {doc.metadata['sender'] or '(발신자 없음)'}\n"
                formatted_result += f"날짜: {doc.metadata['date']}\n"
                formatted_result += f"내용: {doc.page_content}\n"
                formatted_results.append(formatted_result)
            
            if not formatted_results:
                return "검색 결과가 없습니다."
            
            return "\n\n".join(formatted_results)
        except Exception as e:
            return str(e)
    
    def _create_workflow(self) -> Graph:
        """작업 흐름 그래프 생성"""
        workflow = StateGraph(AgentState)
        
        # 노드 정의
        def get_emails_node(state):
            result = self.get_emails("")
            return {"email_content": result}
            
        def process_email_node(state):
            result = self.process_email(state["email_content"], state["question"])
            return {"response": result}
            
        def search_emails_node(state):
            result = self.search_emails(state["question"])
            return {"response": result}

        def end_node(state):
            return state
        
        workflow.add_node("get_emails", get_emails_node)
        workflow.add_node("process_email", process_email_node)
        workflow.add_node("end", end_node)
        

        workflow.add_edge("get_emails", "process_email")
        
        # RAG가 활성화되어 있을 때만 search_emails 노드 추가
        if self.rag_processor:
            workflow.add_node("search_emails", search_emails_node)
            workflow.add_edge("process_email", "search_emails")
            workflow.add_edge("search_emails", "end")
        else:
            workflow.add_edge("process_email", "end")
        
        # 시작 노드와 종료 노드 설정
        workflow.set_entry_point("get_emails")
        workflow.set_finish_point("end")
        
        return workflow.compile()
    
    def run(self, question: str) -> str:
        """에이전트 실행"""
        try:
            # 초기 상태 설정
            state = {
                "messages": [HumanMessage(content=question)],
                "email_content": "",
                "question": question,
                "response": ""
            }
            
            # 워크플로우 실행
            result = self.workflow.invoke(state)
            return result["response"]
        except Exception as e:
            return f"에이전트 실행 중 오류가 발생했습니다: {str(e)}" 