import os
import csv
from datetime import datetime
from collections import defaultdict

def ler_arquivos_csv(diretorio="csv_exports"):
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

    if not os.path.exists(diretorio):
        print(f"Diretório {diretorio} não encontrado.")
        return {}, "N/A", "N/A"

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".csv") and arquivo.startswith("vendas_"):
            # Extrai a data do nome do arquivo: vendas_DD-MM-YYYY.csv
            data_str = arquivo.replace("vendas_", "").replace(".csv", "").replace("-", "/")
            datas.append(data_str)
            
            caminho_arquivo = os.path.join(diretorio, arquivo)
            with open(caminho_arquivo, mode='r', encoding='utf-8') as f:
                leitor_csv = csv.reader(f)
                try:
                    next(leitor_csv)  # Pula o cabeçalho
                except StopIteration:
                    continue
                    
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
                            # Tenta pegar apenas a parte numérica antes de espaços
                            quantidade_val = int(quantidade.split(' ')[0].replace(',', ''))
                        except ValueError:
                            continue
                    
                    vendas_totais[produto] += quantidade_val

    # Ordena as datas para pegar a primeira e a última
    try:
        datas_ordenadas = sorted(datas, key=lambda x: datetime.strptime(x, "%d/%m/%Y"))
        data_inicio = datas_ordenadas[0] if datas_ordenadas else "N/A"
        data_fim = datas_ordenadas[-1] if datas_ordenadas else "N/A"
    except Exception:
        data_inicio = "N/A"
        data_fim = "N/A"

    return vendas_totais, data_inicio, data_fim
