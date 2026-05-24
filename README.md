# Relatório de Vendas e Integração com Telegram

Este projeto automatiza a extração de dados de vendas de um sistema online e salva essas informações em arquivos CSV. Além disso, há integração com o Telegram para envio de relatórios.

## Funcionalidades

- **Extração de dados de vendas**: Extração de vendas dentro de um intervalo de dias especificado pelo usuário.
- **Salvamento de dados**: As vendas são salvas em arquivos CSV, com o formato `vendas_DD-MM-YYYY.csv`.
- **Integração com Telegram**: Após o salvamento das vendas, o script `listarTelegram.py` é executado para enviar os dados pelo Telegram.

## Pré-requisitos

- Python 3.x
- Bibliotecas necessárias (instalar via `pip`):
  - `selenium`
  - `webdriver-manager`
  - `reportlab`

### Instalação das bibliotecas

Execute qualquer um dos seguintes comandos para instalar as dependências:

```Opção 1
pip install selenium webdriver-manager reportlab
```
```Opção 2
pip install -r requirements.txt
```
A segunda opção pode não estar funcionando corretamente

## Arquivos do Projeto

- `fazerLogin.py`: Contém as funções para iniciar o navegador e fazer login no sistema.
- `listarTelegram.py`: Script responsável por enviar relatórios via Telegram.
- `main.py`: Script principal que realiza a extração de dados e coordena as outras partes do projeto.
- `testeBot.py`: Script de teste para interação com o bot do Telegram.
- `README.md`: Este arquivo de documentação.

## Como Executar

1. Clone este repositório para sua máquina local:
   
   ```bash
   git clone https://github.com/digitalrobertlima/realtorio_vendas_telegram.git
   ```

2. Navegue até o diretório do projeto:

   ```
   cd realtorio_vendas_telegram
   ```

3. Execute o script principal:

   ```
   python main.py
   ```

4. Insira o **PIN de login** quando solicitado e o intervalo de dias para extração das vendas.

## Detalhes Técnicos

- **Login automático**: O login é feito automaticamente através do `fazerLogin.py`, utilizando o PIN fornecido pelo usuário.
- **Extração de dados**: O script acessa a página de relatórios de vendas e coleta dados de vendas para os dias selecionados.
- **Salvamento em CSV**: Cada venda é salva em um arquivo CSV com os campos "Produto", "Quantidade" e "Valor".
- **Execução de script do Telegram**: Após o salvamento dos dados, o script `listarTelegram.py` é executado para enviar as vendas extraídas via Telegram.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
