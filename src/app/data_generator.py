import os
import json
from google import genai
from dotenv import load_dotenv
from src.app.util import limpar_json

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


def pergunta_carro(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-05-20",
            contents=prompt
        )

        return response.text

    except Exception as e:
        print(f"Erro ao gerar conteúdo com Gemini: {e}")
        return None


def gerar_carros_em_lotes(marca, ano, combustivel, total=100, lote=20):
    carros = []

    for i in range(0, total, lote):
        prompt = f"""
                Aja como um especialista em veículos.

                Gere uma lista com {lote} carros fictícios com as informações abaixo. Considere as informações fornecidas, se disponíveis:
                - Marca: {marca}
                - Ano: {ano}
                - Combustível: {combustivel}

                Se alguma informação não for fornecida, gere valores fictícios baseando-se apenas na marca (se informada).

                Retorne **apenas o JSON puro**, com aspas **duplas**, e **sem markdown ou caracteres escapados** (\\n, \\t, \\r).

                Formato esperado:

                {{
                "carros": [
                    {{
                        "marca": "string",
                        "modelo": "string",
                        "ano": "int",
                        "motorizacao": "string",
                        "combustivel": "string",
                        "cor": "string",
                        "quilometragem": "float",
                        "portas": "integer",
                        "transmissao": "string",
                        "preco": "float"
                    }}
                ]
                }}
                """

        # Aqui você chamaria a API do ChatGPT ou outro modelo com o prompt acima
        resposta = pergunta_carro(prompt)

        try:
            json_carro = limpar_json(resposta)
            dados = json.loads(json_carro)
            carros.extend(dados.get("carros", []))
        except json.JSONDecodeError as e:
            print(f"Erro ao processar lote {i}: {e}")
            continue

    return {"carros": carros}
