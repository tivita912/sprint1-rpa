import time
import logging
import schedule

from coletor import coletar_novos_registros
from normalizador import normalizar
from persistencia import inserir_lote

def executar_ciclo():
    try:
        logging.info("Iniciando ciclo de coleta")

        # coleta registros novos do CSV
        registros_crus = coletar_novos_registros()
        if not registros_crus:
            logging.info("Nenhum registro novo encontrado")
            return

        # normaliza e valida
        registros_normalizados = normalizar(registros_crus)

        # persiste no banco
        inserir_lote(registros_normalizados)

        logging.info("Ciclo de coleta finalizado com sucesso")

    except Exception as e:
        logging.error(f"Erro no ciclo de coleta: {e}")

def iniciar():
    # agenda o ciclo pra rodar a cada 10 segundos
    schedule.every(10).seconds.do(executar_ciclo)

    # roda o primeiro ciclo imediatamente
    executar_ciclo()

    logging.info("Agendador iniciado - ciclo a cada 10 segundos")
    while True:
        schedule.run_pending()
        time.sleep(1)
