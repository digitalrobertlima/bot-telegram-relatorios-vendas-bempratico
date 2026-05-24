import os
import csv
import requests
from datetime import datetime
from collections import defaultdict
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from dotenv import load_dotenv

load_dotenv()

# Variáveis globais
topVendas = 15  # Número de produtos para a lista de sugestão de reabastecimento
telegram_token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

def enviar_mensagem_telegram(mensagem):
    """
    Envia uma mensagem para o chat especificado no Telegram.
    
    Parâmetros:
    mensagem (str): Mensagem a ser enviada.
    """
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": mensagem,
        "parse_mode": "Markdown"  # Para formatar a mensagem com Markdown
    }
    response = requests.post(url, data=payload)
    return response.json()

def enviar_arquivo_telegram(caminho_arquivo):
    """
    Envia um arquivo PDF para o chat especificado no Telegram.
    
    Parâmetros:
    caminho_arquivo (str): Caminho completo para o arquivo a ser enviado.
    """
    url = f"https://api.telegram.org/bot{telegram_token}/sendDocument"
    with open(caminho_arquivo, 'rb') as f:
        files = {
            'document': f
        }
        payload = {
            "chat_id": chat_id
        }
        response = requests.post(url, files=files, data=payload)
    return response.json()

def gerar_pdf(produtos_ordenados, data_inicio, data_fim, nome_arquivo="lista-repor.pdf"):
    """
    Gera um arquivo PDF com a lista de produtos mais vendidos, em formato paisagem
    e com quebra de linha automática.
    
    Parâmetros:
    produtos_ordenados (list): Lista de tuplas com produto e quantidade vendida.
    data_inicio (str): Data de início do relatório.
    data_fim (str): Data de fim do relatório.
    nome_arquivo (str): Nome do arquivo PDF a ser criado.
    """
    doc = SimpleDocTemplate(nome_arquivo, pagesize=landscape(letter))
    styles = getSampleStyleSheet()
    elementos = []

    # Título
    titulo = Paragraph("Lista de Produtos para Reabastecimento", styles['Title'])
    elementos.append(titulo)
    elementos.append(Spacer(1, 12))

    # Intervalo de Datas
    intervalo = Paragraph(f"Este relatório compreende as datas de {data_inicio} até {data_fim}", styles['Normal'])
    elementos.append(intervalo)
    elementos.append(Spacer(1, 20))

    # Tabela de Dados
    dados = [["#", "Produto", "Quantidade Vendida"]]  # Cabeçalho
    for i, (produto, quantidade) in enumerate(produtos_ordenados, 1):
        dados.append([str(i), produto, str(quantidade)])

    tabela = Table(dados, colWidths=[30, 450, 100])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elementos.append(tabela)
    doc.build(elementos)
    print(f"PDF '{nome_arquivo}' gerado com sucesso.")

def ler_arquivos_csv(diretorio):
    """
    Lê todos os arquivos CSV no diretório especificado e retorna um dicionário com 
    a quantidade total vendida de cada produto e o intervalo de datas.
    
    Parâmetros:
    diretorio (str): Caminho para o diretório contendo os arquivos CSV.

    Retorno:
    tuple: (vendas_totais, data_inicio, data_fim)
    """
    vendas_totais = defaultdict(int)
    datas = []

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".csv") and arquivo.startswith("vendas_"):
            # Extrai a data do nome do arquivo: vendas_DD-MM-YYYY.csv
            data_str = arquivo.replace("vendas_", "").replace(".csv", "").replace("-", "/")
            datas.append(data_str)
            
            caminho_arquivo = os.path.join(diretorio, arquivo)
            with open(caminho_arquivo, mode='r', encoding='utf-8') as f:
                leitor_csv = csv.reader(f)
                next(leitor_csv)  # Pula o cabeçalho
                for linha in leitor_csv:
                    if len(linha) < 2: continue
                    produto, quantidade, _ = linha
                    
                    if "Kg" in quantidade:
                        quantidade_val = quantidade.replace('Kg', '').replace(' ', '').replace(',', '.').replace('x', '')
                        try:
                            quantidade_val = round(float(quantidade_val))
                        except ValueError:
                            print(f"Erro ao converter quantidade para o produto '{produto}': '{quantidade}'")
                            continue
                    else:
                        try:
                            quantidade_val = int(quantidade.split(' ')[0].replace(',', ''))
                        except ValueError:
                            continue
                    
                    vendas_totais[produto] += quantidade_val

    # Ordena as datas para pegar a primeira e a última
    # Como estão em formato DD/MM/YYYY, precisamos de um parse básico para ordenar
    try:
        datas_ordenadas = sorted(datas, key=lambda x: datetime.strptime(x, "%d/%m/%Y"))
        data_inicio = datas_ordenadas[0] if datas_ordenadas else "N/A"
        data_fim = datas_ordenadas[-1] if datas_ordenadas else "N/A"
    except Exception:
        data_inicio = "N/A"
        data_fim = "N/A"

    return vendas_totais, data_inicio, data_fim

def sugerir_reabastecimento(vendas_totais, data_inicio, data_fim, limite=10):
    """
    Sugere produtos para reabastecimento com base nos itens mais vendidos.
    
    Parâmetros:
    vendas_totais (dict): Dicionário com produtos e suas quantidades totais vendidas.
    data_inicio (str): Data de início do relatório.
    data_fim (str): Data de fim do relatório.
    limite (int): Número de produtos a sugerir para reabastecimento.
    """
    produtos_ordenados = sorted(vendas_totais.items(), key=lambda item: item[1], reverse=True)

    mensagem = f"Os {limite} produtos mais vendidos que você deve considerar reabastecer são:\n"
    for i, (produto, quantidade) in enumerate(produtos_ordenados[:limite], 1):
        mensagem += f"{i}. Produto: {produto} | Quantidade Vendida: {quantidade}\n"

    # Envia a mensagem para o Telegram
    enviar_mensagem_telegram(mensagem)

    # Gera e envia o PDF com a lista de produtos
    nome_pdf = "lista-repor.pdf"
    gerar_pdf(produtos_ordenados[:limite], data_inicio, data_fim, nome_arquivo=nome_pdf)
    enviar_arquivo_telegram(nome_pdf)

def main():
    diretorio = "."  # Diretório atual
    vendas_totais, data_inicio, data_fim = ler_arquivos_csv(diretorio)
    sugerir_reabastecimento(vendas_totais, data_inicio, data_fim, limite=topVendas)

if __name__ == "__main__":
    main()
