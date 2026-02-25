# Tutorial: Geração de Vídeos via GitHub Actions (Viral Engine)

Este documento explica como utilizar o workflow `viral_generate.yml` para criar vídeos diretamente do GitHub.

## 1. Como Usar o Workflow

Diferente de workflows automáticos, o `Viral Engine Generation` solicita as chaves de API no momento do disparo. Isso permite que você use credenciais diferentes para testes rápidos.

### Passos para disparar:

1. Vá até a aba **Actions** no seu repositório GitHub.
2. Selecione **Viral Engine Generation** no menu à esquerda.
3. Clique no botão **Run workflow**.
4. Preencha os campos solicitados:
   - **Tema do vídeo**: A ideia central (ex: "Curiosidades sobre o Espaço").
   - **Gemini API Key**: Sua chave do Google Gemini.
   - **Hugging Face Token**: Seu segredo do HF para imagens.
   - **ElevenLabs API Key**: Sua chave para voz.
   - **ID da Voz**: O ID da voz desejada (ex: `pqHfZKP75CvOlQylNhV4`).
   - **Dados YouTube**: Credenciais OAuth2 (Client ID, Secret e Refresh Token).
5. Clique em **Run workflow**.

## 2. Recomendação de Segurança

Embora este workflow peça os inputs manuais, recomendamos que para uso constante você utilize os **GitHub Secrets** para não precisar digitar as chaves todas as vezes. 

> [!TIP]
> Se desejar que eu modifique o workflow para ler de `secrets` automaticamente em vez de `inputs`, me avise!

## 3. O que acontece na execução?

O GitHub irá:
1. Instalar o Node.js e dependências do **Remotion-app**.
2. Instalar o Python e dependências do **Backend**.
3. Rodar o script `full_automation.py` que orquestra a criação total e o upload para o YouTube.

Acompanhe o progresso clicando na execução ativa para ver os logs em tempo real.
