import csv
import os
import time
import random
from datetime import datetime

CAMINHO_CSV = os.path.join(os.path.dirname(__file__), '..', 'data', 'sensor_raw.csv')
TAG_MOTOR = "MOTOR-001"
INTERVALO = 5  # segundos entre medições
FREQUENCIA_FALHA = 20  # a cada N medições, gera uma com valor estranho

def garantir_csv_com_cabecalho():
    cabecalho_esperado = ['timestamp', 'tag', 'tensao', 'corrente', 'temperatura', 'rotacao', 'vibracao']

    # se o arquivo não existe, cria com cabeçalho
    if not os.path.exists(CAMINHO_CSV):
        with open(CAMINHO_CSV, 'w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            escritor.writerow(cabecalho_esperado)
        return

    # se existe, verifica se o cabeçalho está correto
    with open(CAMINHO_CSV, 'r', encoding='utf-8') as f:
        primeira_linha = f.readline().strip()

    campos = primeira_linha.split(',')
    if campos == cabecalho_esperado:
        return

    # cabeçalho ausente ou errado, recria o arquivo
    print("[SIMULADOR] Cabeçalho do CSV ausente ou incorreto, recriando arquivo")
    with open(CAMINHO_CSV, 'w', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f)
        escritor.writerow(cabecalho_esperado)

def gerar_medicao_normal():
    return {
        'timestamp': datetime.now().isoformat(),
        'tag': TAG_MOTOR,
        'tensao': round(random.uniform(215.0, 225.0), 2),
        'corrente': round(random.uniform(4.0, 7.0), 2),
        'temperatura': round(random.uniform(40.0, 80.0), 1),
        'rotacao': random.randint(1750, 1800),
        'vibracao': round(random.uniform(0.0, 5.0), 2),
    }

def gerar_medicao_com_falha():
    medicao = gerar_medicao_normal()
    # escolhe um sensor pra ter valor estranho
    sensor_com_falha = random.choice(['tensao', 'temperatura', 'vibracao'])
    if sensor_com_falha == 'tensao':
        medicao['tensao'] = 9999.99
    elif sensor_com_falha == 'temperatura':
        medicao['temperatura'] = -50.0
    else:
        medicao['vibracao'] = 99.99
    return medicao

def escrever_no_csv(medicao):
    with open(CAMINHO_CSV, 'a', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f)
        escritor.writerow([
            medicao['timestamp'],
            medicao['tag'],
            medicao['tensao'],
            medicao['corrente'],
            medicao['temperatura'],
            medicao['rotacao'],
            medicao['vibracao'],
        ])

def main():
    garantir_csv_com_cabecalho()
    contador = 0
    print("[SIMULADOR] Iniciando simulação do motor " + TAG_MOTOR)

    while True:
        contador += 1

        # a cada 20 medições, gera uma com falha
        if contador % FREQUENCIA_FALHA == 0:
            medicao = gerar_medicao_com_falha()
        else:
            medicao = gerar_medicao_normal()

        escrever_no_csv(medicao)
        print(f"[SIMULADOR] Medição #{contador} gerada: tensao={medicao['tensao']}, "
              f"corrente={medicao['corrente']}, temp={medicao['temperatura']}, "
              f"rotacao={medicao['rotacao']}, vibracao={medicao['vibracao']}")

        time.sleep(INTERVALO)

if __name__ == '__main__':
    main()
