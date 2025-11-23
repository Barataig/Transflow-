# TransFlow — Sistema de Processamento de Corridas (FastAPI + RabbitMQ + MongoDB + Redis)

Este projeto implementa um sistema distribuído de gerenciamento de corridas utilizando:
- **FastAPI** — API principal para cadastro das corridas  
- **RabbitMQ** — Mensageria para envio dos eventos de corrida finalizada  
- **MongoDB** — Armazenamento permanente das corridas  
- **Redis** — Armazenamento rápido do saldo de motoristas  
- **Worker Async** — Responsável por consumir mensagens e atualizar banco + Redis  

---

## 1. Arquitetura Geral do Sistema

                ┌────────────────────────┐
                │        CLIENTE         │
                │  (POST /corridas)       │
                └────────────┬───────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │    FASTAPI     │
                    │  (Producer)    │
                    └───────┬────────┘
                            │ envia evento
                            ▼
                    ┌──────────────────┐
                    │    RabbitMQ      │
                    │    Exchange      │
                    └────────┬─────────┘
                             │ entrega mensagem
                             ▼
                    ┌──────────────────┐
                    │    CONSUMER      │
                    │  (Worker Async)  │
                    └──────┬──────┬────┘
                           │      │
           atualiza saldo │      │ insere corrida
                           ▼      ▼
               ┌─────────────┐   ┌──────────────┐
               │    REDIS    │   │   MONGODB     │
               │ saldo moto. │   │ persistência  │
               └─────────────┘   └──────────────┘

---

## 2. Requisitos

Docker
Docker Compose
Python 3.11+ (opcional)


---

## 3. Estrutura do Projeto

transflow/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
│
└── src/
├── main.py # API FastAPI
├── producer.py # Envio de mensagens RabbitMQ
├── consumer.py # Worker consumidor
│
├── models/
│ └── corrida_model.py # Pydantic Models
│
└── database/
├── mongo_client.py # MongoDB
└── redis_client.py # Redis

---

## 4. Variáveis de Ambiente Necessárias

Crie um arquivo `.env` na raiz:

MONGO_URL=mongodb://mongo:27017/
MONGO_DB_NAME=transflow

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

RABBITMQ_URL=amqp://rabbitmq:5672
EXCHANGE_NAME=corridas_exchange
QUEUE_NAME=corridas_queue

---

## 5. Instalação e Execução

### 5.1. Construir e subir os contêineres

docker compose up --build -d

Serviços disponibilizados:
API FastAPI → http://localhost:8000

RabbitMQ UI → http://localhost:15672
 (user: guest / pass: guest)
MongoDB → porta 27017
Redis → porta 6379

---

## 6. Testando o Sistema

### 6.1. Criar uma corrida (POST)
---


Use Postman, Thunder Client ou curl:

POST http://localhost:8000/corridas

Content-Type: application/json

Body:

```json
{
  "id_corrida": "12345",
  "passageiro": {
    "nome": "João da Silva",
    "telefone": "21999999999"
  },
  "motorista": {
    "nome": "Carlos Almeida",
    "nota": 4.9
  },
  "origem": "Maricá",
  "destino": "Niterói",
  "valor_corrida": 37.50,
  "forma_pagamento": "pix"
}

Se tudo estiver funcionando:

A API salva no MongoDB

Envia evento ao RabbitMQ

O Consumer recebe

Atualiza saldo no Redis

Grava a corrida no MongoDB


# 7. Conferindo os Resultados
## 7.1. Ver saldo atualizado no Redis

Entre no container:

docker exec -it redis redis-cli


Cheque o saldo:

GET saldo:Carlos Almeida

### 7.2. Ver as corridas no MongoDB

Entre no container:

docker exec -it mongo mongosh


Liste as corridas:

use transflow
db.corridas.find().pretty()

8. Logs do Worker
docker logs consumer -f