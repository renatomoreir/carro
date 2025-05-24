import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
load_dotenv(dotenv_path="/mnt/dados/gitlab/carro/src/.env")

Base = declarative_base()

class Carro(Base):
    __tablename__ = 'carros'

    id = Column(Integer, primary_key=True)
    marca = Column(String)
    modelo = Column(String)
    ano = Column(Integer)
    motorizacao = Column(String)
    combustivel = Column(String)
    cor = Column(String)
    quilometragem = Column(Float)
    portas = Column(Integer)
    transmissao = Column(String)
    preco = Column(Float)

class SQLAlchemy:
    def __init__(self):
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.db_name = os.getenv("DB_NAME")
        self.url_conexao = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        self._create_database_if_not_exists()

        try:
            self.engine = create_engine(self.url_conexao, pool_pre_ping=True, pool_recycle=3600)
            Base.metadata.create_all(self.engine)
            self.session = scoped_session(sessionmaker(bind=self.engine))
        except SQLAlchemyError as e:
            print(f"Erro ao conectar com o banco de dados: {e}")


    def _create_database_if_not_exists(self):
        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()

            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (self.db_name,))
            exists = cursor.fetchone()

            if not exists:
                cursor.execute(f'CREATE DATABASE "{self.db_name}"')
                print(f"✅ Banco '{self.db_name}' criado.")

            cursor.close()
            conn.close()
        except psycopg2.Error as e:
            print(f"Erro ao verificar/criar o banco de dados: {e}")
   

    def inserir_carros(self, carros):
        for dado in carros:
            carro = Carro(
                marca=dado.get('marca'),
                modelo=dado.get('modelo'),
                ano=dado.get('ano'),
                motorizacao=dado.get('motorizacao'),
                combustivel=dado.get('combustivel'),
                cor=dado.get('cor'),
                quilometragem=dado.get('quilometragem'),
                portas=dado.get('portas'),
                transmissao=dado.get('transmissao'),
                preco=dado.get('preco')
            )
            self.session.merge(carro)

        self.session.commit()