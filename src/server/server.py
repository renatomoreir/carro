import os
import sys
import socket
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.app.mcp_protocol import processar_mcp
from dotenv import load_dotenv
load_dotenv(dotenv_path="/mnt/dados/gitlab/carro/src/.env")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((os.getenv("SOCKET_HOST"), int(os.getenv("SOCKET_PORT"))))
    s.listen()
    print("Servidor MCP aguardando conexões...")

    conn, addr = s.accept()
    with conn:
        print(f"Conectado por {addr}")
        while True:
            data = conn.recv(4096)
            if not data:
                break
            resposta = processar_mcp(data.decode())
            conn.sendall(resposta.encode())