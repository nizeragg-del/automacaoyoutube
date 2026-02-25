# Roadmap: Automação Total e Escala (Viral Engine SaaS)

Este documento descreve as possibilidades técnicas para transformar o motor atual em uma plataforma de criação de conteúdo automatizada e escalável.

## 1. Automação via GitHub Actions (The "Cron" Bot)
Sim, é totalmente possível e recomendado para rodar sem custo de servidor fixo.

### Como funcionaria:
- **Trigger Agendado:** O GitHub roda o script `full_automation.py` todos os dias em um horário específico (ex: 10:00 AM).
- **Trigger por Input:** Você preenche um formulário no próprio GitHub com o "Tema do Dia" e ele dispara a criação.
- **Persistência:** Uso de **GitHub Secrets** para chaves de API e **GitHub Artifacts** (ou Supabase) para salvar o vídeo final antes do upload.

> [!TIP]
> **Instalação do Remotion no Github Actions:** O GitHub Actions suporta ambientes Linux/Windows onde podemos instalar o Node.js e renderizar o vídeo via linha de comando, exatamente como fizemos localmente.

---

## 2. Dashboard de Configuração (Frontend Elite)
Podemos criar uma interface web moderna (Next.js + Tailwind) para controlar o motor.

### Funcionalidades Propostas:
- **Configuração de Voz:** Escolher narradores do ElevenLabs via interface.
- **Ajuste de Prompt "Mestre":** Editar as instruções de retenção (Hook/Loop) sem mexer no código Python.
- **Histórico de Vídeos:** Uma galeria com todos os vídeos gerados e seus links do YouTube.
- **Controle de Créditos:** Gráficos mostrando o consumo de Gemini, ElevenLabs e Hugging Face.
- **Botão "Criar Agora":** Um campo de texto simples para disparar o processo com um clique.

---

## 3. Arquitetura de Produção (SaaS Ready)
Para escalar para múltiplos canais ou venda como serviço:

1. **Backend API (FastAPI):** O motor atual vira uma API que recebe requisições.
2. **Worker Queue (Celery/Redis):** Gerencia a fila de renderização (evita que o site trave enquanto o vídeo é gerado).
3. **Database (Supabase):** Guarda os metadados (Títulos, Descrições, IDs dos vídeos).
4. **Storage (Supabase Storage):** Armazena as imagens e áudios gerados para consulta futura.

---

## 4. Possibilidades de Novos Motores
- **Legendas Dinâmicas:** Implementar um motor que gera legendas que "pulam" na tela (estilo Alex Hormozi) usando transcrição do áudio (Whisper AI).
- **Multi-Cenas:** Evoluir de 1 imagem para múltiplas cenas variando conforme o roteiro progride.
- **Multi-Plataforma:** Postagem simultânea em TikTok e Instagram Reels.

---

## 5. Arquitetura SaaS (Multi-Usuário)
Transformar o motor em um SaaS (Software as a Service) onde cada usuário tem sua "instância" isolada.

### Gestão de APIs Próprias ("Bring Your Own Key"):
- **Dashboard de Configuração:** Uma tela de "Configurações de API" onde o usuário insere suas próprias chaves:
    - `GEMINI_API_KEY`
    - `HUGGINGFACE_API_KEY`
    - `ELEVENLABS_API_KEY`
- **Isolamento:** O sistema salvará as chaves de forma criptografada no banco de dados (Supabase Auth/Vault).
- **Custo Zero para Você:** Com essa abordagem, o custo de geração de conteúdo recai sobre as contas de API de cada usuário, eliminando seu risco financeiro como dono da plataforma.

---

## 6. Sistema de Agendamento (Scheduler)
Permitir que o usuário programe a postagem automática para dias e horários específicos.

### Como funcionaria:
- **Interface de Calendário:** O usuário escolhe: "Toda Terça e Quinta às 18:00".
- **Fila de Execução:** O Cloud Function ou um Worker (Celery) verifica o banco de dados a cada minuto e dispara o motor quando o horário for atingido.
- **Preview de Agendamento:** O usuário pode deixar "na fila" temas como: "História 1 - Terça", "História 2 - Quarta".

---

## 7. O que muda no Motor? (Modificações Técnicas)
Para suportar essas mudanças, o motor precisará de um "upgrade de flexibilidade":

1. **Injeção de Dependência:** As funções de IA e YouTube não lerão mais do arquivo `.env` estático. Elas passarão a receber as chaves como argumentos de função, vindo diretamente do banco de dados do usuário logado.
2. **Webhooks de Status:** O motor enviará alertas para o Dashboard (ex: "Renderizando...", "Upload concluído com sucesso") para que o usuário acompanhe em tempo real.
3. **Database Integration:** O script Python precisará se comunicar com o Supabase para carregar o "Tema do Dia" agendado e as preferências de voz do usuário.

---
**Status Atual:** Protótipo Local (Sucesso) -> **Fase 2:** Automação SaaS / BYO API Keys.
