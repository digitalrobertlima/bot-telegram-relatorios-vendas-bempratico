# 📦 Relatório de Vendas Automatizado com Integração Telegram

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Selenium](https://img.shields.io/badge/selenium-4.x-green.svg)
![Telegram API](https://img.shields.io/badge/telegram-api-blue.svg)

Este sistema é uma ferramenta de automação desenvolvida para extrair dados de vendas de forma eficiente do sistema **Bem Prático**, processar essas informações para gerar insights de reabastecimento e notificar os gestores via **Telegram**, incluindo a entrega de um relatório detalhado em PDF.

## 🚀 Funcionalidades

- **Automação de Login**: Realiza o fluxo completo de autenticação (E-mail $\rightarrow$ Senha $\rightarrow$ PIN) utilizando Selenium WebDriver.
- **Extração Dinâmica de Dados**: Permite que o usuário defina um intervalo de dias para a extração de relatórios de vendas.
- **Persistência em CSV**: Exporta as vendas de cada dia para arquivos CSV individuais (`vendas_DD-MM-YYYY.csv`), garantindo a integridade dos dados brutos.
- **Análise de Dados**: Consolida as vendas de múltiplos dias, tratando diferentes unidades de medida (como "Kg") e normalizando quantidades.
- **Inteligência de Reabastecimento**: Identifica automaticamente os produtos mais vendidos no período selecionado.
- **Notificações em Tempo Real**: Envia via Telegram a lista dos top produtos para reabastecimento.
- **Relatórios Profissionais**: Gera automaticamente um arquivo PDF formatado em modo paisagem com a lista detalhada de itens a repor.

## 🛠️ Arquitetura do Sistema

O fluxo de execução segue a seguinte pipeline:

1.  **Módulo de Autenticação (`fazerLogin.py`)**: Inicia o navegador e realiza o login no portal.
2.  **Módulo de Extração (`main.py`)**: 
    - Navega até o centro de relatórios.
    - Filtra as datas conforme escolha do usuário.
    - Faz o *scraping* das tabelas de pedidos.
    - Salva os dados em arquivos `.csv`.
3.  **Módulo de Processamento e Notificação (`listarTelegram.py`)**:
    - Lê todos os CSVs gerados.
    - Agrega as quantidades totais por produto.
    - Ordena os produtos por volume de vendas.
    - Gera um PDF profissional via `reportlab`.
    - Envia a mensagem de resumo e o PDF via Telegram Bot API.

## 📦 Instalação e Configuração

### 1. Pré-requisitos
- Python 3.x instalado.
- Google Chrome instalado (o driver é gerenciado automaticamente pelo `webdriver-manager`).
- Um Bot do Telegram criado via `@BotFather` (para obter o Token).
- O seu `Chat ID` do Telegram.

### 2. Clonando o Repositório
```bash
git clone https://github.com/digitalrobertlima/realtorio_vendas_telegram.git
cd realtorio_vendas_telegram
```

### 3. Dependências
Recomenda-se o uso de um ambiente virtual:
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

### 4. Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`:
```env
# Credenciais de Login do Sistema
EMAIL_LOGIN=seu_email@exemplo.com
SENHA_INSTALACAO=sua_senha_de_instalacao
PIN_LOGIN=seu_pin_de_login

# Configurações do Bot do Telegram
TELEGRAM_TOKEN=seu_token_do_bot_aqui
TELEGRAM_CHAT_ID=seu_chat_id_aqui
```

## 📖 Como Utilizar

Para iniciar o processo de extração e notificação, execute o script principal:

```bash
python main.py
```

**Passo a passo durante a execução:**
1. O sistema solicitará o **PIN de Login** e a **Senha** (caso não estejam no `.env`).
2. O sistema solicitará o **dia inicial** e o **dia final** do intervalo de vendas (ex: início 1, fim 5 para pegar a primeira semana do mês).
3. O navegador abrirá automaticamente, fará o login, extrairá os dados e fechará.
4. Ao final, você receberá no seu Telegram a lista de reabastecimento e o PDF `lista-repor.pdf`.

## 📂 Estrutura de Arquivos

| Arquivo | Descrição |
| :--- | :--- |
| `main.py` | Ponto de entrada do sistema e orquestrador de extração. |
| `fazerLogin.py` | Lógica de autenticação via Selenium. |
| `listarTelegram.py` | Processamento de CSVs, geração de PDF e integração com API do Telegram. |
| `requirements.txt` | Lista de dependências do projeto. |
| `.env` | Configurações sensíveis e credenciais (não versionado). |
| `testeBot.py` | Script utilitário para testar a conexão com o bot. |
| `debug_run.py` | Script para testes de execução e depuração. |

## ⚖️ Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
