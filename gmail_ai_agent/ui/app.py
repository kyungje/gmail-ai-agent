import streamlit as st
import requests
from typing import List, Dict, Any

# API 엔드포인트 설정
API_URL = "http://localhost:8001"

def main():
    st.title("📧 Gmail AI Assistant")
    st.markdown("""
    이 앱은 Gmail 이메일을 분석하고 질문에 답변해주는 AI 어시스턴트입니다.
    """)
    
    # 사이드바 설정
    st.sidebar.title("설정")
    max_emails = st.sidebar.slider("가져올 이메일 수", 1, 20, 10)
    
    # 메인 컨텐츠
    question = st.text_input("이메일에 대해 궁금한 점을 물어보세요:")
    
    if st.button("질문하기"):
        if question:
            try:
                response = requests.post(
                    f"{API_URL}/ask",
                    json={"question": question}
                )
                
                if response.status_code == 200:
                    answer = response.json()["answer"]
                    st.markdown("### 답변")
                    st.write(answer)
                else:
                    st.error("API 요청 중 오류가 발생했습니다.")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")
        else:
            st.warning("질문을 입력해주세요.")

if __name__ == "__main__":
    main() 