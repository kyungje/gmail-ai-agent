from typing import List, Dict, Any
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle
from ..config.settings import settings

class EmailProcessor:
    def __init__(self):
        self.creds = None
        self.service = None
        self._setup_gmail_service()

    def _setup_gmail_service(self):
        """Gmail API 서비스 설정"""
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(
                    {
                        "installed": {
                            "client_id": settings.GMAIL_CLIENT_ID,
                            "client_secret": settings.GMAIL_CLIENT_SECRET,
                            "redirect_uris": settings.GMAIL_REDIRECT_URI,
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token"
                        }
                    },
                    SCOPES
                )
                self.creds = flow.run_local_server(port=8001, redirect_uri_trailing_slash=False)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        # 캐시 비활성화 옵션 추가
        self.service = build('gmail', 'v1', credentials=self.creds, cache_discovery=False)

    def get_emails(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """이메일 목록 가져오기"""
        results = self.service.users().messages().list(
            userId='me',
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        email_list = []
        
        for message in messages:
            msg = self.service.users().messages().get(
                userId='me',
                id=message['id'],
                format='full'
            ).execute()
            
            headers = msg['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
            
            # 이메일 본문 추출
            body = ''
            if 'parts' in msg['payload']:
                for part in msg['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        body = part['body']['data']
                        break
            
            email_list.append({
                'id': message['id'],
                'subject': subject,
                'sender': sender,
                'date': date,
                'body': body
            })
        
        return email_list 