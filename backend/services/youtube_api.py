import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class YouTubeService:
    def __init__(self):
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.client_secrets_file = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE", "client_secrets.json")
        self.service = None

    def get_authenticated_service(self, client_id: str = None, client_secret: str = None, refresh_token: str = None):
        """
        Lógica para autenticação OAuth2. 
        Suporta Refresh Token para execução não-interativa (SaaS/GitHub Actions).
        """
        if self.service:
            return self.service

        # Se algum parâmetro for fornecido, tenta usar o fluxo de Refresh Token
        if refresh_token:
            if not client_id or not client_secret:
                raise ValueError("ERRO: Refresh Token detectado, mas YOUTUBE_CLIENT_ID ou SECRET estão ausentes no ambiente.")
                
            print(f"Usando Refresh Token para autenticação ({client_id[:5]}...)")
            from google.oauth2.credentials import Credentials
            credentials = Credentials(
                token=None,
                refresh_token=refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=client_id,
                client_secret=client_secret,
                scopes=self.scopes
            )
            self.service = build(self.api_service_name, self.api_version, credentials=credentials)
            return self.service

        # Fallback para fluxo interativo (Apenas uso local)
        if os.path.exists(self.client_secrets_file):
            print("Usando fluxo interativo local (client_secrets.json)...")
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                self.client_secrets_file, self.scopes)
            credentials = flow.run_local_server(port=8080, open_browser=False)
            self.service = build(self.api_service_name, self.api_version, credentials=credentials)
            return self.service
        
        raise ValueError(f"FALHA DE AUTENTICAÇÃO: Nenhum Refresh Token fornecido e '{self.client_secrets_file}' não encontrado.")

    def upload_video(self, file_path: str, title: str, description: str, tags: list = None):
        """
        Faz o upload do vídeo gerado para o YouTube.
        """
        youtube = self.get_authenticated_service()
        
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags or ["Shorts", "AI", "POV"],
                "categoryId": "22" # People & Blogs
            },
            "status": {
                "privacyStatus": "public" # Agora público para engajamento real
            }
        }
        
        insert_request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
        )
        
        response = insert_request.execute()
        return response.get("id")
