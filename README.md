# 🤖 Bot de Gerenciamento Avançado Discord

Este é um bot completo para gerenciamento de servidores Discord, focado em registro de membros com aprovação, bot de presença em call e sistema de elenco dinâmico.

## 🚀 Funcionalidades

-   **🔐 Registro Interativo**: Painel com botão e formulário (Modal) para novos membros.
-   **📝 Aprovação Administrativa**: Canal exclusivo para aprovar ou recusar membros, com atribuição automática de cargos.
-   **🔊 Bot de Presença (Voice)**:
    -   O bot entra automaticamente em um canal de voz configurado.
    -   Fica **Full Mutado** (Mute e Deafen) para não consumir banda e apenas marcar presença ("Enfeite de Call").
-   **🎭 Elenco Dinâmico**: Embed atualizado automaticamente a cada 20 segundos mostrando quem está Online, Offline ou em Call.
-   **⚙️ Configuração Centralizada**: Painel interativo (`!chupetinha`) para configurar tudo sem mexer em código.
-   **📜 Logs Detalhados**: Registro de todas as ações em um canal de logs.

## 🛠️ Instalação

1.  **Requisitos**:
    -   Python 3.8+
    -   Conta de Desenvolvedor Discord (Bot Token)

2.  **Instalar Dependências**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configurar Token**:
    -   Abra o arquivo `.env`.
    -   Coloque seu token: `DISCORD_TOKEN=SEU_TOKEN_AQUI`.

4.  **Iniciar o Bot**:
    ```bash
    python main.py
    ```

## ⚙️ Configuração (!chupetinha)

Para configurar o bot, basta usar **hum único comando** se você for Administrador:

```
!chupetinha
```

Isso abrirá um **Painel de Controle** com botões:

1.  **📺 Configurar Canais**: Selecione nos menus onde cada sistema deve funcionar.
    -   *Selecione Canal de Voz (Bot 24h)*: O canal onde o bot ficará conectado.
2.  **👔 Configurar Cargos**: Defina qual cargo o membro ganha ao ser aprovado e qual cargo define quem aparece no elenco.

## 📖 Como Usar

### 1. Preparar o Registro
Vá até o canal de registro configurado e digite:
```
!setup_registro
```
O bot enviará o painel fixo com o botão "Iniciar Registro".

### 2. Preparar o Elenco
Vá até o canal de elenco configurado e digite:
```
!setup_elenco
```
O bot enviará a mensagem que será atualizada automaticamente a cada 20 segundos.

### 3. Controle do Bot na Call
-   **Automático**: O bot tenta entrar no canal configurado ao iniciar ou se cair.
-   **Manual**:
    -   `!botcall entrar`: Força o bot a tentar entrar no canal configurado novamente.

## 📂 Estrutura do Projeto

-   `main.py`: Arquivo principal.
-   `cogs/`: Módulos do bot (Registro, Admin, Logs, etc).
-   `utils/database.py`: Gerenciamento do banco de dados SQLite (`bot_data.db`).

---
Desenvolvido com ❤️ e Python.
