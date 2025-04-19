from typing import List, Dict, Any
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os
from ..config.settings import settings

class RAGProcessor:
    def __init__(self):
        print("RAGProcessor 초기화 시작")
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-ada-002",
            api_key=settings.OPENAI_API_KEY
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        
        self.vector_store = None
        self._load_vector_store()
        print("RAGProcessor 초기화 완료")
    
    def _load_vector_store(self):
        """벡터 스토어 로드 또는 생성"""
        print(f"벡터 스토어 경로: {settings.VECTOR_STORE_PATH}")
        # 디렉토리가 없으면 생성
        os.makedirs(settings.VECTOR_STORE_PATH, exist_ok=True)
        print(f"벡터 스토어 디렉토리 생성됨: {os.path.exists(settings.VECTOR_STORE_PATH)}")
        
        if os.path.exists(os.path.join(settings.VECTOR_STORE_PATH, "index.faiss")):
            print("기존 벡터 스토어 로드")
            self.vector_store = FAISS.load_local(
                settings.VECTOR_STORE_PATH,
                self.embeddings
            )
        else:
            print("새로운 벡터 스토어 생성")
            self.vector_store = FAISS.from_texts(
                ["Initial document"],
                self.embeddings
            )
            self.vector_store.save_local(settings.VECTOR_STORE_PATH)
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """새로운 문서 추가"""
        print(f"문서 추가 시작: {len(documents)}개의 문서")
        docs = []
        for doc in documents:
            text = f"Subject: {doc['subject']}\nFrom: {doc['sender']}\nDate: {doc['date']}\n\n{doc['body']}"
            # 텍스트를 청크로 분할하고 Document 객체 생성
            chunks = self.text_splitter.split_text(text)
            print(f"문서 분할: {len(chunks)}개의 청크")
            for chunk in chunks:
                docs.append(Document(
                    page_content=chunk,
                    metadata={
                        "subject": doc['subject'],
                        "sender": doc['sender'],
                        "date": doc['date']
                    }
                ))
        
        if docs:  # 문서가 있는 경우에만 추가
            print(f"벡터 스토어에 {len(docs)}개의 문서 추가")
            self.vector_store.add_documents(docs)
            self.vector_store.save_local(settings.VECTOR_STORE_PATH)
            print("벡터 스토어 저장 완료")
        else:
            print("추가할 문서가 없음")
    
    def search(self, query: str, k: int = 3) -> List[Document]:
        """관련 문서 검색"""
        return self.vector_store.similarity_search(query, k=k) 