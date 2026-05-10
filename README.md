# Sprint RPA - Coleta e Registro de Dados de Motor Industrial

Projeto de automação (RPA) para coleta, validação e registro de dados de um motor elétrico industrial 220V. Um simulador gera dados de sensores IoT em CSV e um bot RPA coleta, normaliza e persiste os dados em SQLite com agendamento periódico.

## Como rodar com Docker

```bash
docker-compose up --build
# Aguarde alguns segundos para os dados serem gerados e coletados
# Para ver os logs: docker-compose logs -f coletor
```

## Como rodar sem Docker

Terminal 1 - Simulador:
```bash
pip install -r requirements.txt
python src/simulador.py
```

Terminal 2 - Bot RPA:
```bash
python src/main.py
```

## Estrutura do projeto

```
sprint-rpa/
├── src/
│   ├── simulador.py         # gera dados do motor e escreve em CSV
│   ├── coletor.py           # lê CSV e retorna registros novos
│   ├── normalizador.py      # valida ranges e converte unidades
│   ├── persistencia.py      # SQLite: cria tabelas, insere, consulta
│   ├── agendador.py         # schedule.every().do() em loop
│   └── main.py              # entry point do bot RPA
├── data/
│   ├── sensor_raw.csv       # arquivo gerado pelo simulador
│   └── monitor.db           # banco SQLite
├── logs/
│   └── execucao.log         # log de execução
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Tecnologias

- Python 3.11
- SQLite3
- schedule (agendamento)
- Docker + Docker Compose
