import logging

# ranges válidos pra cada sensor
RANGES = {
    'tensao': (200.0, 250.0),
    'corrente': (0.0, 20.0),
    'temperatura': (-10.0, 120.0),
    'rotacao': (0, 3600),
    'vibracao': (0.0, 20.0),
}

def validar_registro(registro):
    # converte strings pra números e verifica ranges
    try:
        registro['tensao'] = float(registro['tensao'])
        registro['corrente'] = float(registro['corrente'])
        registro['temperatura'] = float(registro['temperatura'])
        registro['rotacao'] = int(registro['rotacao'])
        registro['vibracao'] = float(registro['vibracao'])
    except (ValueError, KeyError, TypeError) as e:
        registro['valido'] = False
        registro['observacao'] = "Erro ao converter valores: " + str(e)
        return registro

    # verifica cada sensor contra o range
    problemas = []
    for campo, (minimo, maximo) in RANGES.items():
        valor = registro[campo]
        if valor < minimo or valor > maximo:
            problemas.append(f"{campo} fora do range: {valor}")

    if problemas:
        registro['valido'] = False
        registro['observacao'] = "; ".join(problemas)
    else:
        registro['valido'] = True
        registro['observacao'] = ""

    return registro

def normalizar(registros):
    resultados = []
    aprovados = 0
    rejeitados = 0

    for reg in registros:
        reg = validar_registro(reg)
        resultados.append(reg)
        if reg['valido']:
            aprovados += 1
        else:
            rejeitados += 1

    logging.info(f"Normalização: {aprovados} aprovados, {rejeitados} rejeitados")
    return resultados
