import os
from services.youtube_api import YouTubeService
from dotenv import load_dotenv

load_dotenv()

def post_existing_video():
    video_path = "final_story.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Erro: O arquivo {video_path} não foi encontrado!")
        return

    print(f"🚀 Preparando para postar o vídeo existente: {video_path}")
    
    # Metadados para o vídeo de Atlântida
    title = "O Segredo de Atlântida: A Cidade Perdida Encontrada?"
    description = "Descubra a verdade sobre a maior lenda de todos os tempos. #Atlântida #História #Mistério #Shorts"
    tags = ["Atlântida", "História", "Mistério", "Curiosidades", "Shorts"]

    youtube = YouTubeService()
    
    try:
        print("\n--- [PASSO ÚNICO] Autenticando e Fazendo Upload ---")
        video_id = youtube.upload_video(
            file_path=video_path,
            title=title,
            description=description,
            tags=tags
        )
        print(f"\n✅ SUCESSO TOTAL!")
        print(f"Vídeo postado com ID: {video_id}")
        print(f"Link: https://www.youtube.com/watch?v={video_id}")
    except Exception as e:
        print(f"❌ Erro no upload do YouTube: {e}")

if __name__ == "__main__":
    post_existing_video()
