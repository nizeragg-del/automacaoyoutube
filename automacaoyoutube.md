# Plano de Automação: YouTube Shorts IA (POV)

Este documento contém o plano para a criação da automação de vídeos curtos utilizando Inteligência Artificial.

## 1. Visão Geral
A ideia é criar um sistema que:
1. Recebe um tema ou "ideia" do usuário.
2. Usa **OpenAI (GPT-4o)** para expandir essa ideia em um roteiro/prompt cinemático POV.
3. Usa a API do **Hugging Face (Modelo FLUX.1)** para gerar uma imagem base de alta fidelidade.
4. Usa a API da **Runway (Gen-3 Alpha)** para animar essa imagem em um vídeo de 5 segundos.
5. Realiza a postagem automática no **YouTube** via API.

## 2. Tecnologias Propostas
- **Backend:** Python (FastAPI) para orquestração e processamento pesado.
- **Frontend:** Next.js para dashboard e visualização (foco em SaaS/venda futura).
- **Banco de Dados:** Supabase para Auth e Armazenamento de mídia.
- **Fila de Tarefas:** Celery + Redis para gerenciar execuções longas de IA.

## 3. Próximos Passos
1. **Configuração de API:** Obtenção das chaves (OpenAI, Hugging Face, Runway, Google Cloud).
2. **Protótipo Python:** Criar um script inicial que faz o fluxo completo de ponta a ponta sem interface.
3. **Plataforma Web:** Integrar o script em uma aplicação SaaS para monetização.

---
Para detalhes técnicos detalhados, veja o [plano de implementação](file:///C:/Users/ctb075/.gemini/antigravity/brain/cd2f4236-5b9e-482a-b4b6-14cad677405b/implementation_plan.md).

---
## 🚀 PROMPT PARA UPGRADE DO MOTOR (ENVIAR PARA O AGENTE)

"Atue como um Especialista em Retenção do YouTube e Roteirista Viral (Estilo MrBeast/MagnatesMedia). Sua missão é atualizar o motor de criação para gerar apenas conteúdo de elite.

### 📝 Estrutura do Roteiro (Storytelling de Alta Retenção):
1. **O Gancho (0-3s):** Deve começar com uma pergunta intrigante, um fato chocante ou uma afirmação polêmica. Ex: 'Você foi enganado...', 'O que ninguém te contou sobre...'. 
2. **O Loop de Curiosidade:** Mantenha o espectador preso revelando informações aos poucos.
3. **Linguagem:** Use palavras de alto impacto, frases curtas e tom profissional/documental.
4. **O Desfecho (Final):** Termine de forma a criar um 'loop infinito' para que o Short reinicie sem que a pessoa perceba.

### 🎥 Direção Visual (Cinema POV):
- **Prompts de Imagem:** Devem focar em hiper-realismo, profundidade de campo, iluminação dramática (chiaroscuro) e ângulos épicos.
- **Formato:** Sempre Vertical (9:16).

### 🛠️ Ajustes Técnicos do Motor:
- **SEM LEGENDAS:** Remova qualquer renderização de legenda estática do Remotion (focaremos na imagem e áudio puros por enquanto).
- **LIMITE ELEVENLABS:** Mantenha o roteiro abaixo de 1000 caracteres.
- **IDIOMA:** Todo o conteúdo gerado (título, roteiro, descrição) deve ser obrigatoriamente em PT-BR (Brasileiro). Prompts de imagem podem ser em Inglês.

**OBJETIVO:** Transformar cada vídeo em um 'mini-documentário' premium que force o usuário do YouTube a parar de dar scroll."
---