import os
import time
import requests
import json
from google import genai
from google.genai import types
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

class AIEngine:
    def __init__(self, gemini_key: str = None, hf_key: str = None, runway_key: str = None):
        """
        Inicializa o motor de IA. 
        Em modo SaaS, as chaves são passadas dinamicamente.
        Se não fornecidas, tenta carregar do ambiente (.env).
        """
        self.gemini_key = gemini_key or os.getenv("GEMINI_API_KEY")
        self.hf_key = hf_key or os.getenv("HUGGINGFACE_API_KEY")
        self.runway_key = runway_key or os.getenv("RUNWAY_API_KEY")

        # Configuração Google AI Studio (Novo SDK google-genai)
        self.client = genai.Client(
            api_key=self.gemini_key,
            http_options={'api_version': 'v1beta'}
        )
        
        # Configuração Hugging Face Hub (Sempre vertical 9:16 para Shorts)
        self.hf_client = InferenceClient(
            model="black-forest-labs/FLUX.1-schnell",
            token=self.hf_key
        )

    def generate_story_script(self, user_input: str) -> dict:
        """
        Gera um roteiro simplificado (1 imagem, 1 script longo).
        """
        system_instruction = """
        You are an Elite YouTube Retention Specialist and Viral Scriptwriter (Style: MrBeast/MagnatesMedia).
        Your mission is to create a 'mini-documentary' premium script that stops the scroll.

        STORYTELLING STRATEGY (PT-BR):
        1. THE HOOK (0-3s): Start with a shocking fact, intriguing question, or bold claim. 
           Ex: "Você foi enganado toda sua vida..." or "O que aconteceu em 1945 mudaria tudo..."
        2. CURIOSITY LOOP: Reveal details gradually to keep the viewer watching.
        3. LANGUAGE: High-impact words, short sentences, professional/documentary tone.
        4. INFINITE LOOP: End the script so it connects perfectly back to the beginning hook.

        CINEMATIC VISUAL DIRECTION (English is OK for image_prompt):
        - Focus on: Hyper-realism, Chiaroscuro lighting (dramatic shadows), depth of field, epic POV angles.
        - Style: Cinema 4D, 8k, Unreal Engine 5 render style.

        CONSTRAINTS:
        - Max 1000 characters for 'full_script' (optimize ElevenLabs credits).
        - ALL generated text (title, full_script, description) MUST be in PORTUGUESE (PT-BR).
        - NO AI MENTIONS (robot, generated, etc.).

        Return ONLY a JSON:
        {
          "title": "Viral Catchy Title In PT-BR",
          "full_script": "The elite script in PT-BR (MAX 1000 chars)",
          "description": "SEO Description in PT-BR with #Shorts #History etc.",
          "image_prompt": "Epic cinematic visual prompt in English"
        }
        """
        
        prompt = f"Historical story about: {user_input}. Ensure the script is under 1000 characters and COMPLETELY in Portuguese (PT-BR)."
        
        # Modelos descobertos via client.models.list()
        models_to_try = [
            "gemini-2.5-flash",
            "gemini-2.5-pro",
            "gemini-1.5-flash",
            "gemini-2.0-flash"
        ]
        
        last_error = None
        # Máximo de 3 voltas na lista de modelos
        for attempt in range(3):
            for model_id in models_to_try:
                try:
                    print(f"Tentativa {attempt+1} - Gerando roteiro com {model_id}...")
                    response = self.client.models.generate_content(
                        model=model_id,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            response_mime_type="application/json"
                        )
                    )
                    print(f"Sucesso com {model_id}!")
                    return json.loads(response.text)
                except Exception as e:
                    error_msg = str(e)
                    print(f"Erro no modelo {model_id}: {error_msg}")
                    last_error = e
                    
                    if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                        import re
                        retry_match = re.search(r"retryDelay': '(\d+)s'", error_msg)
                        seconds = int(retry_match.group(1)) + 2 if retry_match else 30
                        print(f"Cota excedida. Aguardando {seconds} segundos...")
                        time.sleep(seconds)
                    elif "404" in error_msg or "NOT_FOUND" in error_msg:
                        print(f"Modelo {model_id} não suportado. Pulando...")
                    else:
                        time.sleep(5)
                    continue
        
        raise last_error

    def generate_audio(self, text: str, output_path: str = "narration.mp3", elevenlabs_key: str = None, voice_id: str = None):
        """
        Converte o texto em áudio usando ElevenLabs.
        Em modo SaaS, recebe a chave e o ID da voz do usuário.
        """
        print(f"Gerando narração com ElevenLabs...")
        from elevenlabs.client import ElevenLabs
        
        api_key = elevenlabs_key or os.getenv("ELEVENLABS_API_KEY")
        client = ElevenLabs(api_key=api_key)
        
        # ID da voz (Padrão: Bill se não fornecido)
        # Bill: pqHfZKP75CvOlQylNhV4
        selected_voice = voice_id or "pqHfZKP75CvOlQylNhV4" 
        
        audio_generator = client.text_to_speech.convert(
            text=text,
            voice_id=selected_voice,
            model_id="eleven_multilingual_v2"
        )
        
        # Salva o áudio
        print(f"Salvando áudio em: {output_path}")
        with open(output_path, "wb") as f:
            for chunk in audio_generator:
                f.write(chunk)
                
        print(f"Áudio concluído!")
        return output_path
        
    def generate_detailed_prompt(self, user_input: str) -> str:
        """
        Transforma a ideia do usuário em um prompt POV cinemático usando Gemini.
        Tenta vários modelos em caso de erro de cota ou indisponibilidade.
        """
        system_instruction = """
        You are an advanced AI specializing in transforming a short user-provided description into a hyper-realistic, cinematic first-person POV prompt.
        Format: Return ONLY a JSON with the key "prompt".
        Rules:
        - Strictly first-person POV (GoPro style).
        - Visible limbs in foreground (hands, feet).
        - Cinematic details (lighting, weather, textures).
        - Smooth transition from foreground to background.
        - Under 950 characters.
        """
        
        prompt = f"User POV Idea: {user_input}"
        
        # Lista de modelos para tentar (baseado no diagnóstico anterior)
        models_to_try = [
            "gemini-flash-latest",
            "gemini-pro-latest",
            "gemini-1.5-flash", 
            "gemini-2.0-flash"
        ]
        
        last_error = None
        for model_id in models_to_try:
            try:
                print(f"Tentando modelo Gemini: {model_id}...")
                response = self.client.models.generate_content(
                    model=model_id,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        response_mime_type="application/json"
                    )
                )
                result = json.loads(response.text)
                print(f"Sucesso com o modelo {model_id}!")
                return result.get("prompt", "")
            except Exception as e:
                last_error = e
                error_msg = str(e)
                if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                    print(f"Cota excedida para {model_id}. Tentando próximo...")
                elif "404" in error_msg or "NOT_FOUND" in error_msg:
                    print(f"Modelo {model_id} não encontrado. Tentando próximo...")
                else:
                    print(f"Erro inesperado com {model_id}: {error_msg}")
                continue
        
        print("CRÍTICO: Todos os modelos de prompt falharam.")
        raise last_error

    def generate_image(self, prompt: str) -> bytes:
        """
        Gera uma imagem base usando o modelo FLUX.1 através do huggingface_hub.
        """
        print("Gerando imagem com Flux (Hugging Face Client)...")
        # text_to_image retorna um objeto PIL.Image
        image = self.hf_client.text_to_image(prompt)
        
        # Converter PIL Image para bytes (JPEG)
        import io
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        return img_byte_arr.getvalue()

    def generate_video_task(self, image_bytes: bytes, prompt: str) -> str:
        """
        Gera um vídeo usando o Google Veo (via Gemini SDK).
        Diferente da Runway, o Veo exige que o arquivo seja upado primeiro.
        """
        print(f"Gerando vídeo com Google Veo ({prompt[:30]}...)...")
        
        # 1. Salvar imagem em arquivo temporário para upload
        temp_img_path = "temp_for_veo.jpg"
        with open(temp_img_path, "wb") as f:
            f.write(image_bytes)
            
        try:
            # 2. Upload do arquivo para o Google AI Studio
            print("Fazendo upload da imagem para o Google Cloud...")
            uploaded_file = self.client.files.upload(file=temp_img_path)
            
            # 3. Chamar a geração de vídeo
            model_id = "veo-3.1-generate-preview" 
            
            # Conforme assinatura detectada: image é argumento direto
            operation = self.client.models.generate_videos(
                model=model_id,
                prompt=prompt,
                image=types.Image(uri=uploaded_file.uri),
                config=types.GenerateVideosConfig(
                    aspect_ratio="9:16",
                    duration_seconds=5
                )
            )
            
            print(f"Vídeo solicitado (ID Operação: {operation.name}). Aguardando processamento...")
            return operation.name
            
        except Exception as e:
            print(f"Erro ao iniciar Veo: {e}")
            raise e
        finally:
            if os.path.exists(temp_img_path):
                os.remove(temp_img_path)

    def get_video_result(self, operation_name: str) -> str:
        """
        Aguarda a conclusão da operação do Veo e retorna o caminho do arquivo gerado.
        Nota: O SDK do Google pode baixar o arquivo diretamente.
        """
        import time
        
        while True:
            # Busca o status da operação
            op = self.client.operations.get(name=operation_name)
            
            if op.done:
                if op.error:
                    raise Exception(f"Erro na geração do Veo: {op.error}")
                
                # No Veo, o resultado geralmente é um objeto Video que contém a URI ou bytes
                # O SDK costuma lidar com o download se configurado, ou retorna a URI do Cloud Storage
                # Vamos extrair a URL de download
                result = op.response
                video_uri = result.video_samples[0].video_uri
                print(f"Vídeo pronto! Localizado em: {video_uri}")
                return video_uri
            
            print("Processando vídeo no Google Veo... Aguarde.")
            time.sleep(15)
