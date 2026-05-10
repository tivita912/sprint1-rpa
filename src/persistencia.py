import sqlite3
import os
import logging
from datetime import datetime

CAMINHO_BANCO = os.path.join(os.path.dirname(__file__), '..', 'data', 'monitor.db')

def conectar():
    return sqlite3.connect(CAMINHO_BANCO)

def inicializar_banco():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ativos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag TEXT UNIQUE,
            fabricante TEXT,
            potencia_cv REAL,
            tensao_nominal REAL,
            data_cadastro TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ativo_id INTEGER,
            timestamp TEXT,
            tensao REAL,
            corrente REAL,
            temperatura REAL,
            rotacao INTEGER,
            vibracao REAL,
            valido INTEGER,
            observacao TEXT,
            data_processamento TEXT,
            FOREIGN KEY (ativo_id) REFERENCES ativos(id)
        )
    ''')

    conexao.commit()
    conexao.close()
    logging.info("Banco de dados inicializado")

def cadastrar_ativo(tag, fabricante, potencia, tensao):
    conexao = conectar()
    cursor = conexao.cursor()
    agora = datetime.now().isoformat()
    cursor.execute(
        'INSERT OR IGNORE INTO ativos (tag, fabricante, potencia_cv, tensao_nominal, data_cadastro) VALUES (?, ?, ?, ?, ?)',
        (tag, fabricante, potencia, tensao, agora)
    )
    conexao.commit()
    conexao.close()
    if cursor.rowcount > 0:
        logging.info(f"Ativo cadastrado: {tag}")

def buscar_ativo_id(cursor, tag):
    cursor.execute('SELECT id FROM ativos WHERE tag = ?', (tag,))
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    return None

def inserir_medicao(conexao, cursor, registro):
    tag = registro.get('tag')
    if not tag:
        logging.warning("Registro sem tag, pulando")
        return

    ativo_id = buscar_ativo_id(cursor, tag)
    if ativo_id is None:
        logging.warning(f"Ativo não encontrado: {tag}")
        return

    agora = datetime.now().isoformat()
    valido_int = 1 if registro['valido'] else 0

    cursor.execute('''
        INSERT INTO medicoes (ativo_id, timestamp, tensao, corrente, temperatura, rotacao, vibracao, valido, observacao, data_processamento)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        ativo_id,
        registro['timestamp'],
        registro['tensao'],
        registro['corrente'],
        registro['temperatura'],
        registro['rotacao'],
        registro['vibracao'],
        valido_int,
        registro['observacao'],
        agora,
    ))

def inserir_lote(registros):
    if not registros:
        return

    conexao = conectar()
    cursor = conexao.cursor()

    contador = 0
    for registro in registros:
        inserir_medicao(conexao, cursor, registro)
        contador += 1

    conexao.commit()
    conexao.close()
    logging.info(f"{contador} medições inseridas no banco")
