import os
import sys
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.app.data_generator import pergunta_carro
from src.client.client import MCPClient


cliente = MCPClient()


def conversar():
    print("Olá! Sou seu assistente de busca de carros.")
    filtros = {}
    
    validadores = [validar_marca, validar_ano, validar_combustivel]
    for validador in validadores:
        validado, filtros = validador(filtros)
        if not validado:
            return

    resultados = cliente.enviar_requisicao(json.dumps(filtros))

    print("\n🚗 Resultados Encontrados:")
    for carro in resultados:
        print(f"{carro['marca']} {carro['modelo']} ({carro['ano']}) - {carro['cor']}, {carro['quilometragem']} km, R$ {carro['preco']:,.2f}")


def validar_marca(filtros):
    filtros['marca'] = input( "Tem alguma marca preferida? ")
    prompt = f"{filtros['marca']} é uma marca de carro? responta com true ou false em formato boolean"
    if 'False' in pergunta_carro(prompt):
        print(f" a palavra {filtros['marca']} não e reconhecida. tente novamente!")
        return False, {}
    else:
        return True, filtros


def validar_ano(filtros):
    filtros['ano'] = 0
    entrada_ano = input("Ano desejado? (ou pressione Enter para ignorar): ")
    if entrada_ano.strip():
        filtros['ano'] = int(entrada_ano)
    if filtros['ano']:
        prompt = f"{filtros['ano']} é um ano do calendario? responta com true ou false em formato boolean"
        if 'False' in pergunta_carro(prompt):
            print(f" a palavra {filtros['ano']} não e reconhecida. tente novamente!")
            return False, {}
    return True, filtros


def validar_combustivel(filtros):
    filtros['combustivel'] = input("Combustível preferido? (ex: Flex, Gasolina) ")
    if filtros['combustivel']:
        prompt = f"{filtros['combustivel']} é um combustivel de automovel? responta com true ou false em formato boolean"
        if 'False' in pergunta_carro(prompt):
            print(f" a palavra {filtros['combustivel']} não e reconhecida. tente novamente!")
            return False, {}
    return True, filtros
    

if __name__ == "__main__":
    while True:
        try:
            conversar()
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            continuar = input("Deseja fazer outra busca? (s/n): ")
            if continuar.lower() != 's':
                break
