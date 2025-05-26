import os
import socket
from dotenv import load_dotenv

from ..app.mcp_protocol import processar_mcp

load_dotenv()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((os.getenv("SOCKET_HOST"), int(os.getenv("SOCKET_PORT"))))
    s.listen()
    print("Servidor MCP aguardando conexões...")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Conectado por {addr}")
            try:
                while True:
                    data = conn.recv(16384)
                    if not data:
                        break
                    resposta = processar_mcp(data.decode())
                    conn.sendall(resposta.encode())
            except ConnectionResetError:
                print(f"Conexão resetada pelo cliente: {addr}")
            except Exception as e:
                print(f"Erro inesperado: {e}")