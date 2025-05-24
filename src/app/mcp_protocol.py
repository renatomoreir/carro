import json

from src.app.data_generator import gerar_carros
from src.app.database import SQLAlchemy
from src.app.database import Carro

def processar_mcp(msg_json):
    filtros = json.loads(msg_json)
    sqlalchemy = SQLAlchemy()
    
    while True:
        query = sqlalchemy.session().query(Carro)
        if 'marca' in filtros:
            query = query.filter(Carro.marca.ilike(f"%{filtros['marca']}%"))
        if 'ano' in filtros:
            query = query.filter(Carro.ano == filtros['ano'])
        if 'combustivel' in filtros:
            query = query.filter(Carro.combustivel.ilike(f"%{filtros['combustivel']}%"))

        carros = query.all()
        if carros:
            break

        carros = gerar_carros(filtros.get('marca'), filtros.get('ano'), filtros.get('combustivel'))
        sqlalchemy.inserir_carros(carros)
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