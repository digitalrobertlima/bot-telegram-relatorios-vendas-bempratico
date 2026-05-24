# 📦 Relatório de Vendas Automatizado com Integração Telegram

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Selenium](https://img.shields.io/badge/selenium-4.x-green.svg)
![Telegram API](https://img.shields.io/badge/telegram-api-blue.svg)

Este sistema é uma ferramenta de automação desenvolvida para extrair dados de vendas de forma eficiente do sistema **Bem Prático**, processar essas informações para gerar insights de reabastecimento e notificar os gestores via **Telegram**, incluindo a entrega de um relatório detalhado em PDF.

## 🚀 Funcionalidades

- **Automação de Login**: Realiza o fluxo completo de autenticação (E-mail $\rightarrow$ Senha $\rightarrow$ PIN) utilizando Selenium WebDriver.
- **Extração Totalmente Automatizada**: O intervalo de datas é configurado via arquivo `.env`, eliminando a necessidade de interação manual no terminal.
- **Persistência Organizada**: Exporta as vendas de cada dia para arquivos CSV individuais dentro da pasta `csv_exports/`, mantendo a raiz do projeto limpa.
- **Análise de Dados Modular**: Consolida as vendas de múltiplos dias, tratando diferentes unidades de medida (como "Kg") e normalizando quantidades.
- **Inteligência de Reabastecimento**: Identifica automaticamente os produtos mais vendidos no período selecionado.
- **Notificações em Tempo Real**: Envia via Telegram a lista dos top produtos para reabastecimento.
- **Relatórios Profissionais**: Gera automaticamente um arquivo PDF formatado em modo paisagem com a lista detalhada de itens a repor.

## 🛠️ Arquitetura do Sistema

O sistema foi refatorado para seguir o princípio de responsabilidade única, dividindo a lógica em módulos independentes:

1.  **Autenticação (`fazerLogin.py`)**: Inicia o navegador e realiza o login no portal.
2.  **Orquestração de Extração (`main.py`)**: 
    - Lê as configurações de data do `.env`.
    - Navega até o centro de relatórios e realiza o *scraping*.
    - Salva os dados brutos em `csv_exports/`.
3.  **Processamento de Dados (`csv_processor.py`)**:
    - Lê todos os CSVs da pasta de exportação.
    - Agrega totais de vendas e identifica o intervalo de datas processado.
4.  **Geração de Documentos (`pdf_generator.py`)**:
    - Transforma os dados processados em um relatório PDF profissional via `reportlab`.
5.  **Comunicação (`telegram_notifier.py`)**:
    - Interface com a API do Telegram para envio de mensagens de texto e arquivos PDF.
6.  **Fluxo de Notificação (`listarTelegram.py`)**:
    - Coordena a ponte entre o processador de CSVs, o gerador de PDF e o notificador do Telegram.

## 📦 Instalação e Configuração

### 1. Pré-requisitos
- Python 3.x instalado.
- Google Chrome instalado.
- Bot do Telegram criado via `@BotFather`.

### 2. Clonando o Repositório
```bash
git clone https://github.com/digitalrobertlima/realtorio_vendas_telegram.git
cd realtorio_vendas_telegram
```

### 3. Dependências
```bash
pip install -r requirements.txt
```

### 4. Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com as seguintes chaves:
```env
# Credenciais de Login do Sistema
EMAIL_LOGIN=seu_email@exemplo.com
SENHA_INSTALACAO=sua_senha_de_instalacao
PIN_LOGIN=seu_pin_de_login

# Configurações do Bot do Telegram
TELEGRAM_TOKEN=seu_token_do_bot_aqui
TELEGRAM_CHAT_ID=seu_chat_id_aqui

# Automação do Intervalo de Datas
DIA_INICIAL=1
DIA_FINAL=31
```

## 📖 Como Utilizar

Para iniciar o processo completo, execute:

```bash
python main.py
```

**Fluxo Automático:**
1. O sistema lê as datas do `.env`.
2. Realiza o login e extrai as vendas para `csv_exports/`.
3. Processa os arquivos, gera o PDF `lista-repor.pdf`.
4. Envia o resumo e o PDF para o Telegram.

## 📂 Estrutura de Arquivos

| Arquivo | Descrição |
| :--- | :--- |
| `main.py` | Ponto de entrada e orquestrador de extração. |
| `fazerLogin.py` | Lógica de autenticação via Selenium. |
| `csv_processor.py` | Lógica de leitura e agregação de dados CSV. |
| `pdf_generator.py` | Lógica de criação do relatório PDF. |
| `telegram_notifier.py` | Interface de comunicação com a API do Telegram. |
| `listarTelegram.py` | Orquestrador do fluxo de processamento $\rightarrow$ PDF $\rightarrow$ Telegram. |
| `csv_exports/` | Pasta onde ficam armazenados os CSVs de vendas. |
| `requirements.txt` | Lista de dependências do projeto. |

## ⚖️ Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
