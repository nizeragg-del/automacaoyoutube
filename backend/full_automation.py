import os
import json
import subprocess
import time
from services.ai_engine import AIEngine
from services.youtube_api import YouTubeService
from dotenv import load_dotenv

load_dotenv()

def run_story_automation(idea, gemini_key=None, hf_key=None, elevenlabs_key=None, voice_id=None, yt_client_id=None, yt_client_secret=None, yt_refresh_token=None):
    # Inicializa serviços com chaves dinâmicas (Suporte SaaS)
    engine = AIEngine(gemini_key=gemini_key, hf_key=hf_key)
    youtube = YouTubeService()
    
    # Caminhos do Remotion (Agora na raiz do repo)
    remotion_dir = os.getcwd()
    public_dir = os.path.join(remotion_dir, "public")
    
    # 0. Autenticação Antecipada
    print("\n--- [0] Autenticando no YouTube ---")
    try:
        youtube.get_authenticated_service(
            client_id=yt_client_id, 
            client_secret=yt_client_secret, 
            refresh_token=yt_refresh_token
        )
        print("Autenticação concluída com sucesso!")
    except Exception as e:
        print(f"❌ ERRO CRÍTICO: Falha na autenticação do YouTube. Abortando para salvar créditos.")
        print(f"Detalhes: {e}")
        return

    # 1. Gerar o Roteiro e Cenas
    print(f"\n--- [1] Gerando Roteiro de História para: {idea} ---")
    story = engine.generate_story_script(idea)
    print(f"Roteiro '{story['title']}' criado com sucesso.")

    # 2. Gerar Narração (ElevenLabs)
    print("\n--- [2] Gerando Narração (ElevenLabs) ---")
    audio_filename = "narration.mp3"
    audio_path = os.path.join(public_dir, audio_filename)
    engine.generate_audio(
        story['full_script'], 
        audio_path, 
        elevenlabs_key=elevenlabs_key, 
        voice_id=voice_id
    )

    # 3. Gerar Imagem Única
    print("\n--- [3] Gerando Imagem Principal ---")
    image_bytes = engine.generate_image(story['image_prompt'])
    image_filename = "main_story_image.jpg"
    image_path = os.path.join(public_dir, image_filename)
    
    with open(image_path, "wb") as f:
        f.write(image_bytes)

    # 4. Preparar Dados para o Remotion
    print("\n--- [4] Renderizando Vídeo (Remotion) ---")
    
    # Calcular duração dinâmica do áudio para o Remotion
    from mutagen.mp3 import MP3
    audio_info = MP3(audio_path)
    audio_duration_secs = int(audio_info.info.length)
    fps = 30
    duration_frames = (audio_duration_secs * fps) + fps # Adiciona 1 segundo de lambuja
    print(f"Duração detectada: {audio_duration_secs}s ({duration_frames} frames)")

    story_data = {
        "image": image_filename,
        "text": story['title'],
        "audio": audio_filename,
        "durationInFrames": duration_frames
    }
    
    props_path = os.path.join(public_dir, "story_props.json")
    with open(props_path, "w", encoding="utf-8") as f:
        json.dump(story_data, f, indent=2)

    # Executar Renderização do Remotion
    output_video = os.path.join(os.getcwd(), "final_story.mp4")
    
    render_cmd = f'npx remotion render src/index.ts StoryVideo "{output_video}" --props=public/story_props.json --duration={duration_frames}'
    
    print(f"Iniciando renderização no diretório: {remotion_dir}")
    try:
        # No Linux, shell=True funciona melhor com uma string única
        subprocess.run(render_cmd, cwd=remotion_dir, check=True, shell=True)
        
        # Validação crucial: o arquivo realmente existe?
        if not os.path.exists(output_video):
            raise FileNotFoundError(f"Remotion terminou sem gerar o arquivo em: {output_video}")
            
        print(f"Vídeo renderizado e verificado com sucesso: {output_video}")
    except Exception as e:
        print(f"Erro na renderização ou verificação do Remotion: {e}")
        return

    # 5. Fazer o Upload para o YouTube
    print("\n--- [5] Fazendo Upload para o YouTube ---")
    title = story['title']
    description = story.get('description', f"{title}\n\n#História #Curiosidades #Shorts")
    
    try:
        video_id = youtube.upload_video(
            file_path=output_video,
            title=title,
            description=description,
            tags=["História", "Especial", "Shorts", "Incrivel"]
        )
        print(f"\n✅ SUCESSO TOTAL!")
        print(f"Vídeo postado com ID: {video_id}")
        print(f"Link: https://www.youtube.com/watch?v={video_id}")
    except Exception as e:
        print(f"Erro no upload do YouTube: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Motor de Automação Viral SaaS")
    parser.add_argument("--idea", help="Tema do vídeo")
    parser.add_argument("--gemini_key", help="Gemini API Key")
    parser.add_argument("--hf_key", help="Hugging Face Token")
    parser.add_argument("--elevenlabs_key", help="ElevenLabs API Key")
    parser.add_argument("--voice_id", help="ID da Voz ElevenLabs")
    parser.add_argument("--yt_client_id", help="YouTube Client ID")
    parser.add_argument("--yt_client_secret", help="YouTube Client Secret")
    parser.add_argument("--yt_refresh_token", help="YouTube Refresh Token")

    args = parser.parse_args()

    # Se não passado via argumento, tenta via input (para uso local legado)
    idea = args.idea or input("Digite o tema para sua história: ")
    
    if idea:
        run_story_automation(
            idea,
            gemini_key=args.gemini_key,
            hf_key=args.hf_key,
            elevenlabs_key=args.elevenlabs_key,
            voice_id=args.voice_id,
            yt_client_id=args.yt_client_id,
            yt_client_secret=args.yt_client_secret,
            yt_refresh_token=args.yt_refresh_token
        )
