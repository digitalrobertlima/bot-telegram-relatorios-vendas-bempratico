import os
from csv_processor import ler_arquivos_csv
from pdf_generator import gerar_pdf
from telegram_notifier import enviar_mensagem_telegram, enviar_arquivo_telegram

# Configurações
TOP_VENDAS = 15  # Número de produtos para a lista de sugestão de reabastecimento

def sugerir_reabastecimento(vendas_totais, data_inicio, data_fim, limite=10):
    """
    Orquestra a sugestão de reabastecimento: 
    Ordena dados, gera mensagem, cria PDF e envia via Telegram.
    """
    # Ordena os produtos por quantidade vendida (descendente)
    produtos_ordenados = sorted(vendas_totais.items(), key=lambda item: item[1], reverse=True)
    top_produtos = produtos_ordenados[:limite]

    # 1. Monta a mensagem de resumo
    mensagem = f"Os {limite} produtos mais vendidos que você deve considerar reabastecer são:\n"
    for i, (produto, quantidade) in enumerate(top_produtos, 1):
        mensagem += f"{i}. Produto: {produto} | Quantidade Vendida: {quantidade}\n"

    # 2. Envia a mensagem para o Telegram
    print("Enviando resumo para o Telegram...")
    enviar_mensagem_telegram(mensagem)

    # 3. Gera o PDF com a lista de produtos
    nome_pdf = "lista-repor.pdf"
    print("Gerando PDF...")
    gerar_pdf(top_produtos, data_inicio, data_fim, nome_arquivo=nome_pdf)

    # 4. Envia o PDF para o Telegram
    print("Enviando PDF para o Telegram...")
    enviar_arquivo_telegram(nome_pdf)

def main():
    # Define o diretório onde os CSVs estão localizados
    diretorio_csv = "csv_exports"
    
    print("Processando arquivos CSV...")
    vendas_totais, data_inicio, data_fim = ler_arquivos_csv(diretorio_csv)
    
    if not vendas_totais:
        print("Nenhuma venda encontrada para processar.")
        return

    print(f"Processamento concluído. Período: {data_inicio} a {data_fim}")
    sugerir_reabastecimento(vendas_totais, data_inicio, data_fim, limite=TOP_VENDAS)

if __name__ == "__main__":
    main()
