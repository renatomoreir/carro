import os
import json
import socket
from dotenv import load_dotenv
load_dotenv(dotenv_path="/mnt/dados/gitlab/carro/src/.env")


class MCPClient:
    def __init__(self, host=os.getenv("SOCKET_HOST"), port=int(os.getenv("SOCKET_PORT"))):
        self.host = host
        self.port = port

    def enviar_requisicao(self, mensagem: dict) -> list:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(mensagem.encode())
            resposta = s.recv(16384)
        return json.loads(resposta.decode())