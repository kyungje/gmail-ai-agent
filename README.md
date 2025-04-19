# Gmail AI Agent

Gmail AI Agent는 Gmail API를 활용하여 이메일을 자동으로 처리하고 분석하는 AI 기반 이메일 관리 도구입니다.

## 주요 기능

- Gmail 이메일 자동 검색 및 분석
- 이메일 내용 기반 질문 답변
- 이메일 분류 및 우선순위 설정
- 이메일 요약 및 핵심 정보 추출

## 설치 방법

### 1. 필수 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. Google Cloud Console 설정

1. [Google Cloud Console](https://console.cloud.google.com/)에 접속합니다.
2. 새 프로젝트를 생성하거나 기존 프로젝트를 선택합니다.
3. "API 및 서비스" > "사용자 인증 정보"로 이동합니다.
4. "사용자 인증 정보 만들기" > "OAuth 클라이언트 ID"를 선택합니다.
5. 애플리케이션 유형으로 "데스크톱 앱"을 선택합니다.
6. 이름을 입력하고 "만들기"를 클릭합니다.
7. 클라이언트 ID와 클라이언트 보안 비밀번호를 다운로드합니다.

### 3. 환경 변수 설정

`.env` 파일을 생성하고 다음 정보를 입력합니다:

```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL_NAME=gpt-4o-mini
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret
GMAIL_REDIRECT_URI=http://localhost:8001
```

### 4. Gmail API 활성화

1. Google Cloud Console에서 "API 및 서비스" > "라이브러리"로 이동합니다.
2. "Gmail API"를 검색하고 선택합니다.
3. "사용" 버튼을 클릭하여 API를 활성화합니다.

## 사용 방법

### 1. 서버 실행

```bash
uvicorn gmail_ai_agent.api.main:app --port 8001
```

### 2. Gmail 인증

1. 서버가 시작되면 자동으로 브라우저가 열리고 Google 로그인 페이지가 표시됩니다.
2. Gmail 계정으로 로그인합니다.
3. 필요한 권한을 승인합니다.
4. 인증이 완료되면 자동으로 토큰이 저장됩니다.

### 3. API 엔드포인트

#### 이메일 검색
```bash
curl -X POST "http://localhost:8000/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "검색할 키워드"}'
```

#### 이메일 분석
```bash
curl -X POST "http://localhost:8000/analyze" \
     -H "Content-Type: application/json" \
     -d '{"email_id": "이메일 ID", "question": "질문 내용"}'
```

### 4. Streamlit UI 실행:
```bash
streamlit run gmail_ai_agent/ui/app.py
```

## 보안 고려사항

1. `.env` 파일은 절대 공개 저장소에 커밋하지 마세요.
2. `token.pickle` 파일은 개인 인증 정보를 포함하므로 안전하게 보관하세요.
3. Google Cloud Console에서 API 키와 보안 비밀번호를 정기적으로 교체하세요.

## 문제 해결

### 인증 오류 발생 시

1. `token.pickle` 파일을 삭제하고 다시 인증을 시도하세요.
2. Google Cloud Console에서 OAuth 동의 화면을 확인하세요.
3. 리디렉션 URI가 올바르게 설정되어 있는지 확인하세요.

### API 오류 발생 시

1. Google Cloud Console에서 API 할당량을 확인하세요.
2. 필요한 API가 모두 활성화되어 있는지 확인하세요.
3. 클라이언트 ID와 보안 비밀번호가 올바른지 확인하세요.
