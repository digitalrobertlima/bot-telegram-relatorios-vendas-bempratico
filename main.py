import subprocess
import time
import csv
import os
from datetime import datetime
from dotenv import load_dotenv
from fazerLogin import iniciar_navegador, fazer_login
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def salvar_dados_em_csv(data, vendas):
    """
    Salva os dados de vendas em um arquivo CSV dentro da pasta csv_exports.

    Parâmetros:
    data (str): Data no formato para nome do arquivo.
    vendas (list): Lista de listas contendo dados de vendas.
    """
    # Garante que a pasta csv_exports existe
    pasta_exports = "csv_exports"
    if not os.path.exists(pasta_exports):
        os.makedirs(pasta_exports)

    data_formatada = data.replace("/", "-")  # Substitui barras por hífens para o nome do arquivo
    nome_arquivo = f"vendas_{data_formatada}.csv"
    caminho_completo = os.path.join(pasta_exports, nome_arquivo)
    
    with open(caminho_completo, mode='w', newline='', encoding='utf-8') as arquivo:
        escritor_csv = csv.writer(arquivo)
        escritor_csv.writerow(["Produto", "Quantidade", "Valor"])  # Cabeçalho do arquivo CSV
        for venda in vendas:
            escritor_csv.writerow(venda)  # Escreve os dados de cada venda
    print(f"Dados salvos em {caminho_completo}")

def obter_intervalo_dias():
    """
    Solicita ao usuário um intervalo de dias do mês para extração de dados.

    Retorno:
    tuple: (dia_inicio, dia_fim) - Intervalo de dias selecionado pelo usuário.
    """
    while True:
        try:
            dia_inicio = int(input("Digite o dia inicial do intervalo (1-31): "))
            dia_fim = int(input("Digite o dia final do intervalo (1-31): "))
            if 1 <= dia_inicio <= 31 and 1 <= dia_fim <= 31 and dia_inicio <= dia_fim:
                return dia_inicio, dia_fim
            else:
                print("Dias inválidos. Por favor, insira valores entre 1 e 31 e o dia inicial deve ser menor ou igual ao dia final.")
        except ValueError:
            print("Entrada inválida. Por favor, insira números inteiros.")

def main():
    """
    Função principal que realiza login, navega na página de vendas,
    extrai dados para um intervalo específico e salva em arquivos CSV.
    """
    load_dotenv()
    pin_instalacao = os.getenv("PIN_LOGIN") or input("Qual será o PIN para Login? ")
    senha_instalacao = os.getenv("SENHA_INSTALACAO") or input("Qual será a senha de instalação? ")
    
    # Solicita o intervalo de dias do mês
    dia_inicio, dia_fim = obter_intervalo_dias()
    
    # Inicia o navegador e faz login
    driver = iniciar_navegador()
    fazer_login(driver, pin_instalacao, senha_instalacao)

    # Acessa a página do relatório de vendas
    time.sleep(5)
    driver.get("https://app6.bempratico.com.br/?p=0a8b16d6b3&s=report_center_vendas")

    # Seleciona o mês desejado
    mes = driver.find_element(By.XPATH, '//*[@id="index_body"]/form[2]/center/div/div/center/div[7]')
    mes.click()

    # Aguarda até que os elementos estejam visíveis
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="index_body"]/form[2]/center/center/div[1]/div[7]/div[3]'))
    )
    container_vendas = driver.find_element(By.XPATH, '//*[@id="index_body"]/form[2]/center/center/div[1]/div[7]/div[3]')
    datas_vendas = container_vendas.find_elements(By.TAG_NAME, 'a')

    for link in datas_vendas:
        data_text = link.text
        if data_text:
            dia = int(data_text.split("/")[0])  # Extrai o dia da data no formato DD/MM
            if dia_inicio <= dia <= dia_fim:
                print(f'Extraindo vendas para a data: {data_text}')
                # Re-localiza o link antes de clicar para evitar StaleElementReferenceException
                link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, data_text))
                )
                link.click()

                # Aguarda a página carregar completamente
                time.sleep(5)
                vendas = []

                # Extrai dados das vendas
                linhas_pedidos = driver.find_elements(By.XPATH, '//*[@id="classe_forms"]/tbody/tr')

                for linha in linhas_pedidos:
                    colunas = linha.find_elements(By.XPATH, './/td')
                    if len(colunas) >= 2:  # Verifica se a linha tem pelo menos 2 colunas
                        produto_col = colunas[1].find_element(By.XPATH, './/table/tbody/tr/td[2]').text
                        quantidade_col = colunas[1].find_element(By.XPATH, './/table/tbody/tr/td[1]').text
                        valor_col = colunas[1].find_element(By.XPATH, './/table/tbody/tr/td[4]').text
                        vendas.append([produto_col, quantidade_col, valor_col])

                # Salva os dados em um arquivo CSV
                salvar_dados_em_csv(data_text, vendas)

                # Volta à lista de datas
                time.sleep(2)
                driver.back()

                # Recarrega a lista de links de datas para a próxima iteração
                container_vendas = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="index_body"]/form[2]/center/center/div[1]/div[7]/div[3]'))
                )
                datas_vendas = container_vendas.find_elements(By.TAG_NAME, 'a')

    print('Fim do salvamento de vendas')
    time.sleep(10)  # Aguarda 10 segundos
    driver.quit()  # Fecha o navegador

    # Executa o script do Telegram
    subprocess.run(["python", "listarTelegram.py"])

if __name__ == "__main__":
    main()
