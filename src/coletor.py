import csv
import os
import logging

CAMINHO_CSV = os.path.join(os.path.dirname(__file__), '..', 'data', 'sensor_raw.csv')
CAMINHO_CHECKPOINT = os.path.join(os.path.dirname(__file__), '..', 'data', 'checkpoint.txt')

def ler_checkpoint():
    # retorna a última linha processada (0 = nenhuma)
    if not os.path.exists(CAMINHO_CHECKPOINT):
        return 0
    with open(CAMINHO_CHECKPOINT, 'r') as f:
        conteudo = f.read().strip()
        if conteudo:
            return int(conteudo)
        return 0

def salvar_checkpoint(numero_linha):
    with open(CAMINHO_CHECKPOINT, 'w') as f:
        f.write(str(numero_linha))

def coletar_novos_registros():
    if not os.path.exists(CAMINHO_CSV):
        logging.warning("Arquivo CSV não encontrado: " + CAMINHO_CSV)
        return []

    ultima_linha = ler_checkpoint()

    registros_novos = []
    # utf-8-sig remove BOM se existir (comum em CSV editado no Windows)
    with open(CAMINHO_CSV, 'r', newline='', encoding='utf-8-sig') as f:
        leitor = csv.DictReader(f)
        for i, linha in enumerate(leitor, start=1):
            # pula linhas já processadas
            if i <= ultima_linha:
                continue
            registros_novos.append(linha)

    if registros_novos:
        nova_posicao = ultima_linha + len(registros_novos)
        salvar_checkpoint(nova_posicao)

    logging.info(f"{len(registros_novos)} registros coletados do CSV")
    return registros_novos
