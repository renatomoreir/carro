# Desafio Técnico – Vaga de Desenvolvedor Python | C2S

```Avaliar sua capacidade de aprender coisas novas, com foco em tecnologias que talvez você ainda não tenha usado, e também seu domínio de Python```

## Passos para Execução Local

### Baixar o Docker Desktop
```Acesse o site oficial e baixe o instalador para Windows:

https://www.docker.com/get-started

Dê duplo-clique em Docker Desktop Installer.exe, Siga o assistente: Marque a opção Use WSL 2 instead of Hyper-V (recomendado), Aceite os termos e clique em Install, Aguarde baixar componentes e configurar tudo.

docker version
```

### Clonagem do Repositório

```bash
git clone https://github.com/renatomoreir/carro.git
```

### Backend

#### Subir o Projeto
```bash WINDOWS

abrir o termina Win+R >> powershell
cd .\carro\

docker compose up -d
docker ps -a

python -m venv venv
.\venv\Scripts\activate
pip install -r .\requirements.txt  
python.exe -m pip install --upgrade pip
pip install --upgrade google-genai

.\executar.bat


```

```bash LINUX
cd carro/

sudo docker compose up -d
sudo docker ps -a

python -m venv venv
source venv/bin/activate
pip install -r .\requirements.txt  
python src/app/agent.py && python src/server/server.py 

```

#### Build e Deploy
- o Back End em Python estará rodando em terminal
- O Bando de Dados em Postgres estará rodando em http://localhost:5432

```
DB_HOST = 'localhost'
DB_PORT = 5432
DB_USER = 'postgres'
DB_PASSWORD = 'root'
DB_NAME = 'db_carros'
```

## Estrutura do Banco de Dados

### Bancndo de Dados db_carros e Tabela carros
```sql

CREATE DATABASE db_carros;

CREATE TABLE carros(
    id SERIAL NOT NULL,
    marca varchar,
    modelo varchar,
    ano integer,
    motorizacao varchar,
    combustivel varchar,
    cor varchar,
    quilometragem double precision,
    portas integer,
    transmissao varchar,
    preco double precision,
    PRIMARY KEY(id)
);
```

## Documentação da arquitetura

carro/
│
├── src/
│   ├── app/
│   │    ├── agent.py
│   │    ├── data_generator.py
│   │    ├── database.py
│   │    ├── mcp_protocol..py
│   │    └── util.py
│   ├── client/
│   │    └── client.py
│   ├── server/
│   │    └── server.py
│   ├── .env
│   └── requirements.txt
├── docker-compose.yml
└── README.md


## run debugger usando vscode launch.json
/.vscode/launch.json

{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Socket",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/carro/src/server/server.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}/carro/"
        },
        {
            "name": "Client",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/carro/src/app/agent.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}/carro/"
        },
        
    ],
    "compounds": [
    {
      "name": "Carro",
      "configurations": ["Client", "Socket"]
    }
  ]
}