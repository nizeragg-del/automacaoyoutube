import os
import sys
import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# Reutilizar o motor principal da pasta backend
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from full_automation import run_story_automation

load_dotenv()

def main():
    # 1. Conexão ao Supabase
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") # Usar service role para varrer automações de todos
    
    if not supabase_url or not supabase_key:
        print("❌ ERRO: Faltam as credenciais do Supabase (URL ou KEY)")
        return
        
    supabase: Client = create_client(supabase_url, supabase_key)
    
    # 2. Dia Atual (Fuso Horário BRASÍLIA - GMT-3)
    # Garante que o motor veja o mesmo "hoje" que o usuário no Brasil, ignorando o horário UTC do servidor
    brasil_tz = datetime.timezone(datetime.timedelta(hours=-3))
    agora_br = datetime.datetime.now(brasil_tz)
    
    # datetime.weekday(): 0=Segunda, 6=Domingo. Convertemos para 0=Dom, 6=Sáb
    python_weekday = agora_br.weekday()
    current_day = (python_weekday + 1) % 7 
    
    print(f"\n🚀 Iniciando Varredura do Piloto Automático... (Hora Local BR: {agora_br.strftime('%H:%M:%S')})")
    print(f"📅 Dia da Semana Identificado: {current_day} (0=Dom, 1=Seg, 2=Ter, 3=Qua...)")
    
    # Pequeno log de debug (mascarado)
    if supabase_key:
        print(f"🔑 Chave Supabase finaliza com: ...{supabase_key[-6:]}")
    else:
        print("❌ Chave Supabase NÃO encontrada.")

    try:
        # Busca TODAS as rotinas sem filtro '.eq' para evitar bugs de parsing de Boolean do Postgres no Python
        response = supabase.table('automations').select('*').execute()
        all_routines = response.data
        
        print(f"  -> Total de rotinas cadastradas no BD: {len(all_routines)}")
        
        routines_today = []
        for routine in all_routines:
            is_active = routine.get('is_active', False)
            theme = routine.get('theme', 'Sem Tema')
            
            # Validação flexível de Boolean (True, 'true', 'True', 1)
            is_really_active = is_active is True or str(is_active).lower() == 'true' or str(is_active) == '1'
            
            if not is_really_active:
                print(f"  -> [{theme}] IGNORADA: is_active={is_active} (Usuário pausou a automação)")
                continue
                
            raw_days = routine.get('days_of_week', [])
            
            # Usar regex para extrair qualquer número não importando se veio string '{"1","2"}' ou JSON list
            import re
            numbers = re.findall(r'\d+', str(raw_days))
            days = [int(n) for n in numbers]
            
            print(f"  -> [{theme}] Dias capturados: {days} | Hoje: {current_day}")
            
            if current_day in days:
                routines_today.append(routine)
                
        print(f"✅ Encontradas {len(routines_today)} rotinas programadas para ação HOJE.")
        
        # 3. Execução do Piloto
        for idx, routine in enumerate(routines_today):
            user_id = routine['user_id']
            theme = routine['theme']
            
            print(f"\n---------------------------------------------------")
            print(f"🔥 [Rotina {idx+1}/{len(routines_today)}] Preparando execução para Usuário: {user_id}")
            print(f"Tema Base: {theme}")
            
            # Buscar os tokens API do usuário na tabela profile (onde a vercel salvou)
            # Para isso o projeto no Supabase deve permitir ler "profiles"
            # Vamos buscar os tokens salvos (Ex: youtube_refresh_token)
            
            profile_res = supabase.table('profiles').select('*').eq('id', user_id).execute()
            if not profile_res.data:
                print("⚠️ Usuário não encontrado no banco de dados. Pulando...")
                continue
                
            profile = profile_res.data[0]
            
            yt_refresh_token = profile.get('yt_refresh_token')
            gemini_api_key = profile.get('gemini_api_key') or os.environ.get('GEMINI_API_KEY')
            hf_key = profile.get('huggingface_api_key') or os.environ.get('HUGGINGFACE_API_KEY')
            elevenlabs_key = profile.get('elevenlabs_api_key') or os.environ.get('ELEVENLABS_API_KEY')
            
            if not yt_refresh_token:
                print("⚠️ Usuário não conectou a conta do YouTube (Refresh Token ausente). Pulando...")
                continue
                
            # Pedir para o motor gerar o conteúdo e o script e enviar
            # Uma boa ideia seria passar o Tema, mas pedir algo único para o Gemini usando a Random Seed ou instruções 
            print("🎬 Dando a ordem de IGNIÇÃO para o motor...")
            
            # Chama a função existente da Automação 
            run_story_automation(
                idea=theme,
                gemini_key=gemini_api_key,
                hf_key=hf_key,
                elevenlabs_key=elevenlabs_key,
                yt_client_id=os.environ.get('YOUTUBE_CLIENT_ID'),
                yt_client_secret=os.environ.get('YOUTUBE_CLIENT_SECRET'),
                yt_refresh_token=yt_refresh_token,
                supabase_url=supabase_url,
                supabase_key=supabase_key
            )
            
            print(f"✅ Rotina do usuário {user_id} processada com sucesso!")
            
    except Exception as e:
        print(f"❌ ERRO FATAL no Motor Automático: {e}")

if __name__ == "__main__":
    main()
