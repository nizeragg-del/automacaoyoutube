# Guia de Configuração: Motor de Automação Viral 🤖

Este repositório contém o "motor" que gera os vídeos e faz o upload para o YouTube. Ele foi desenhado para rodar no **GitHub Actions**, eliminando a necessidade de um servidor próprio.

## 🛠️ Passo 1: Configuração das APIs (SaaS/Admin)

Como você é o dono do SaaS, você precisa configurar os segredos no Dashboard para que o motor funcione para seus usuários.

### 1. GitHub Personal Access Token (PAT)
O Dashboard precisa de permissão para "dar o play" no GitHub Actions.
1. Vá em [GitHub Settings > Developer Settings > Personal Access Tokens (classic)](https://github.com/settings/tokens).
2. Gere um novo token com as permissões: `workflow` e `repo`.
3. Salve este token; você irá colá-lo na página de **Settings** do seu Dashboard.

### 2. Repositório do Motor
No Dashboard, no campo "Repositório", coloque o caminho: `nizeragg-del/automacaoyoutube`.

---

## 🔑 Passo 2: Credenciais do Usuário (Painel de Controle)

Cada usuário (inclusive você, no início) deve preencher estas chaves no Dashboard para que o vídeo seja gerado com o crédito/canal dele:

1.  **Gemini API Key**: Gerada no [Google AI Studio](https://aistudio.google.com/).
2.  **ElevenLabs API Key**: No seu perfil do ElevenLabs.
3.  **YouTube Client ID / Secret / Refresh Token**: Obtidos via Google Cloud Console (veja o `api_tutorial.md` para o passo a passo de como conseguir o Refresh Token).

---

## ☁️ Passo 3: Como o Fluxo Funciona (Cloud Step)

1.  O **Dashboard** recebe a ideia do usuário.
2.  O **Dashboard** chama a API do GitHub e aciona o workflow em `.github/workflows/viral_generate.yml`.
3.  O **GitHub Actions** recebe todas as chaves como parâmetros.
4.  O vídeo é renderizado em um servidor do GitHub.
5.  O upload é feito diretamente para o canal do usuário usando o **Refresh Token**.

---

## 🚀 Solução de Problemas
*   **Ação não dispara?** Verifique se o seu GitHub PAT tem permissão de `workflow`.
*   **Erro de áudio/imagem?** Verifique se as chaves da Gemini ou ElevenLabs têm créditos.
*   **Erro no Upload?** O YouTube Refresh Token pode ter expirado ou o Client ID está incorreto.

---

> [!TIP]
> O motor é totalmente independente. Você pode atualizar o código aqui (ex: mudar o estilo do vídeo no Remotion) e o Dashboard passará a usar a versão nova instantaneamente!
