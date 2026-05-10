import logging
import os
import sys

# adiciona o diretório src ao path
sys.path.insert(0, os.path.dirname(__file__))

from persistencia import inicializar_banco, cadastrar_ativo
from agendador import iniciar

def configurar_logging():
    caminho_log = os.path.join(os.path.dirname(__file__), '..', 'logs', 'execucao.log')

    # garante que o diretório de logs existe
    os.makedirs(os.path.dirname(caminho_log), exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(caminho_log, encoding='utf-8'),
            logging.StreamHandler(sys.stdout),
        ]
    )

def main():
    configurar_logging()
    logging.info("Bot RPA iniciado")

    # inicializa o banco e cadastra o motor
    inicializar_banco()
    cadastrar_ativo("MOTOR-001", "WEG", 5.0, 220.0)

    # inicia o agendador (loop infinito)
    iniciar()

if __name__ == '__main__':
    main()
