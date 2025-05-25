import json

from src.app.data_generator import gerar_carros_em_lotes
from src.app.database import SQLAlchemy
from src.app.database import Carro

def processar_mcp(msg_json):
    filtros = json.loads(msg_json)
    sqlalchemy = SQLAlchemy()
    
    while True:
        query = sqlalchemy.session().query(Carro)
        if 'marca' in filtros and filtros['marca'] != "":
            query = query.filter(Carro.marca.ilike(f"%{filtros['marca']}%"))

        if 'ano' in filtros and filtros['ano'] != 0:
            query = query.filter(Carro.ano == filtros['ano'])

        if 'combustivel' in filtros and filtros['combustivel'] != "":
            query = query.filter(Carro.combustivel.ilike(f"%{filtros['combustivel']}%"))

        carros = query.limit(100).all()
        if carros:
            break

        print("\nGerando lotes de carros:")
        carros = gerar_carros_em_lotes(filtros.get('marca'), filtros.get('ano'), filtros.get('combustivel'))
        print("\nSalvando lotes de carros:")
        sqlalchemy.inserir_carros(carros.get("carros", []))
        if not carros:
            return json.dumps([])

    return json.dumps([{
        'marca': c.marca,
        'modelo': c.modelo,
        'ano': c.ano,
        'cor': c.cor,
        'quilometragem': c.quilometragem,
        'preco': c.preco
    } for c in carros])