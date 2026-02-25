# Guia: Como Obter as Chaves de API

Este tutorial explica passo a passo como conseguir as credenciais necessárias para rodar a automação de YouTube Shorts.

## 1. Google AI Studio (Gemini)
*Responsável por transformar sua ideia em um prompt detalhado.*

1.  Acesse o [Google AI Studio](https://aistudio.google.com/).
2.  Faça login com sua conta Google.
3.  No menu lateral esquerdo, clique em **"Get API key"**.
4.  Clique em **"Create API key in new project"**.
5.  Copie a chave e cole no seu arquivo `.env` como `GEMINI_API_KEY`.

## 2. Hugging Face (Flux.1)
*Responsável por gerar a imagem de alta qualidade.*

1.  Acesse o [Hugging Face](https://huggingface.co/).
2.  Crie uma conta ou faça login.
3.  Vá em **Settings > Access Tokens** (ou [clique aqui](https://huggingface.co/settings/tokens)).
4.  Clique em **"Create new token"**.
5.  Dê um nome (ex: "YouTube Automation") e selecione o tipo **"Read"** (ou "Write" se preferir, mas "Read" basta para inferência).
6.  Copie o token e cole no seu `.env` como `HUGGINGFACE_API_KEY`.

## 3. Runway ML (Vídeo)
*Responsável por transformar a imagem em vídeo.*

1.  Acesse o [Runway Login](https://app.runwayml.com/).
2.  Vá para a seção de **Developers/API** (ou [clique aqui](https://dev.runwayml.com/)).
3.  Crie uma nova organização se necessário.
4.  Clique em **"API Keys"** no menu.
5.  Clique em **"Create New Key"**.
6.  Copie a chave e cole no seu `.env` como `RUNWAY_API_KEY`.

## 4. YouTube Data API (Google Cloud)
*Responsável pela postagem automática.*

1.  Acesse o [Google Cloud Console](https://console.cloud.google.com/).
2.  Crie um novo projeto (ex: "Automação YouTube").
3.  No menu de busca, digite **"YouTube Data API v3"** e clique em **Ativar**.
4.  Vá no menu lateral em **"Público-alvo"** (Audience):
    - Selecione o tipo de usuário como **"Externo"**.
    - Em "Usuários de teste", clique em **"Add Users"** e coloque o seu próprio e-mail (isso é fundamental para você conseguir logar).
5.  Vá no menu lateral em **"Branding"**:
    - Preencha o nome do app (ex: "Automacao Youtube") e o e-mail de suporte.
6.  Vá no menu lateral em **"Clientes"** (Clients):
    - Clique em **"Criar Cliente"** ou no botão grande **"Criar um cliente OAuth"**.
    - Em "Tipo de aplicativo", escolha **"App para computador"** (Desktop App).
    - Dê um nome e clique em criar.
7.  Na lista de clientes que aparecer, clique na **setinha para baixo** ou no botão de **Download JSON** ao lado do cliente que você criou.
8.  Renomeie o arquivo baixado para `client_secrets.json` e coloque-o na pasta `backend/`.

---

### Verificação Final
Após obter todas, seu arquivo `.env` deve estar assim:
```env
GEMINI_API_KEY=AIza...
HUGGINGFACE_API_KEY=hf_...
RUNWAY_API_KEY=key_...
```
E o arquivo `client_secrets.json` deve estar dentro de `backend/`.


