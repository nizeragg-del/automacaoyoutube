# Plano de Transição: Automação Elite para SaaS Multi-Usuário

Este documento detalha o passo a passo técnico para transformar seu motor local em uma plataforma escalável onde qualquer usuário pode usar suas próprias chaves de API.

## 1. Onde o motor deve rodar?
Para um SaaS com Dashboard, existem duas opções:

- **Opção A (VPS/Render.com):** O motor fica ligado 24/7. Quando o usuário clica em "Criar Agora", o vídeo começa na hora. É o mais rápido para o usuário.
- **Opção B (GitHub Actions):** Gratuito, mas tem um pequeno atraso (cerca de 1 min) para iniciar o job. Ótimo para vídeos agendados.

**Recomendação:** Iniciar com um **Worker em VPS** (DigitalOcean/Render/Railway) para garantir que o Remotion consiga renderizar rápido.

---

## 2. Passo a Passo da Adaptação (Cronograma)

### Fase 1: Desacoplamento do Motor (Brain Surgery)
Antes de ir para a web, o Python precisa parar de depender do arquivo `.env`.
- **Tarefa:** Modificar `ai_engine.py`, `elevenlabs_api.py` e `youtube_api.py` para aceitarem as chaves como variáveis (Dependency Injection).
- **Resultado:** O motor se torna "burro" e precisa que o Dashboard diga qual chave usar a cada execução.

### Fase 2: Supabase como Cérebro Central
- **Tarefa:** Criar tabelas no Supabase:
    - `profiles`: Guarda as chaves (criptografadas) e preferências de cada usuário.
    - `videos`: Guarda o histórico, links e status (Pendente, Gerando, Postado).
    - `schedules`: Guarda os dias e horários de postagem.

### Fase 3: Dashboard em Next.js (Dashboard Elite)
- **Tarefa:** Criar a interface visual:
    - Login seguro via Google/Email.
    - Tela de Configuração de Chaves (Key Management).
    - Botão "Pânico" (Criar Agora) e Painel de Agendamento.

### Fase 4: O "Orquestrador" (API Gateway)
- **Tarefa:** Criar um pequeno servidor em **FastAPI** que:
    - Recebe o clique do Dashboard.
    - Busca as chaves do usuário no banco.
    - Dispara o `full_automation.py` no servidor de vídeo.

### Fase 5: Automação de Agendamento (The Cron)
- **Tarefa:** Configurar um serviço (ex: GitHub Action ou Cron Job) que a cada 5 minutos olha a tabela `schedules`. 
- Se encontrar um vídeo marcado para agora, ele envia o comando para o Motor.

---

## 3. Resumo da Estrutura Final (Stack)

| Componente | Tecnologia | Papel |
| :--- | :--- | :--- |
| **Interface** | Next.js + Tailwind | Onde o usuário controla tudo. |
| **Banco/Auth** | Supabase | Guarda dados, chaves e usuários. |
| **Cérebro (Motor)** | Python + Remotion | Faz o trabalho pesado de IA e Vídeo. |
| **Hospedagem** | Vercel (Front) + VPS (Motor) | Garante que tudo rode na nuvem. |

---

## Próximo Passo Sugerido:
Deseja que eu comece a **Fase 1** (preparar o código Python para receber chaves externas) ou prefere focar em criar o **Dashboard** inicial primeiro?
