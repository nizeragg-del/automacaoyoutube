# 📺 Guia: Como obter as Credenciais do YouTube

Para que a ViralEngine poste vídeos automaticamente, você precisa de 3 itens do Google: `Client ID`, `Client Secret` e o temido `Refresh Token`.

## Passo 1: Criar o Projeto no Google Cloud
1. Vá para o [Google Cloud Console](https://console.cloud.google.com/).
2. Crie um novo projeto chamado `ViralEngine`.
3. No menu lateral, vá em **APIs e Serviços > Biblioteca**.
4. Procure por **YouTube Data API v3** e clique em **Ativar**.

## Passo 2: Configurar a Tela de Consentimento (OAuth Consent Screen)
1. Vá em **APIs e Serviços > Tela de consentimento OAuth**.
2. Escolha **External** (Externo) e clique em Criar.
3. Preencha apenas os campos obrigatórios (Nome do app, e-mail de suporte).
4. Em **Escopos (Scopes)**, adicione: `.../auth/youtube.upload`.
5. **IMPORTANTE**: Em "Usuários de teste", adicione o seu próprio e-mail do Gmail que será o dono do canal.

## Passo 3: Criar as Credenciais
1. Vá em **APIs e Serviços > Credenciais**.
2. Clique em **Criar Credenciais > ID do cliente OAuth**.
3. Escolha **Aplicativo da Web**.
4. Em **Origens JavaScript autorizadas**, adicione: `https://developers.google.com`
5. Em **URIs de redirecionamento autorizados**, adicione exatamente: `https://developers.google.com/oauthplayground` (sem barra no final)
6. Clique em Criar. Você terá o seu **Client ID** e **Client Secret**.

## Passo 4: Pegar o Refresh Token (O segredo)
Como não queremos que você faça login toda hora, precisamos desse "token infinito".
1. Acesse o [OAuth 2.0 Playground](https://developers.google.com/oauthplayground/).
2. Clique no ícone de engrenagem (Configurações) no canto superior direito.
3. Marque a caixa **Use your own OAuth credentials**.
4. Cole seu **Client ID** e **Client Secret**.
5. Na lista à esquerda, procure por **YouTube Data API v3** e selecione `https://www.googleapis.com/auth/youtube.upload`.
6. Clique em **Authorize APIs**. Faça login com sua conta do canal.
7. Clique em **Exchange authorization code for tokens**.
8. Pronto! O campo **Refresh Token** aparecerá na tela. Copie e cole no Dashboard.
