from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

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
    return nome_arquivo
