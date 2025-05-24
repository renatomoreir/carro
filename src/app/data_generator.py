import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from src.app.util import limpar_json

load_dotenv(dotenv_path="/mnt/dados/gitlab/carro/src/.env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)


def pergunta_carro(prompt):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        print(f"❌ Erro ao gerar conteúdo com Gemini: {e}")
        return None


def gerar_carros(marca="", ano="", combustivel=""):

    prompt = f"""
    Aja como um especialista em veículos.

    Gere uma lista com 100 carros fictícios com as informações abaixo, possivel considerar marca: {marca}, ano: {ano} e combustivel: {combustivel} informado.
    Caso não tenha informações, gere informações fictícias apenas com a considerar marca: {marca}. 
    Retorne **apenas o JSON puro**, sem nenhum texto adicional, markdown ou crases.

    Formato do JSON esperado:
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

    json_data = pergunta_carro(prompt)

    if not json_data:
        return []

    try:
        json_data_limpo = limpar_json(json_data)
        carros_dict = json.loads(json_data_limpo)
    except json.JSONDecodeError:
        print("Erro ao decodificar o JSON:", json_data)
        return []

    if not isinstance(carros_dict, dict) or "carros" not in carros_dict:
        print("O JSON não está no formato esperado:", carros_dict)
        return []

    carros = carros_dict["carros"]
    
    return carros