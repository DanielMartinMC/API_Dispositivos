from sqlmodel import create_engine, SQLModel, Session
from models.dispositivo import Dispositivo
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    db_user: str = os.getenv("DB_USER", "daniel") 
    db_password: str = os.getenv("DB_PASSWORD", "1234")
    db_server: str = os.getenv("DB_SERVER", "fastapi-db-postgres") 
    db_port: int = os.getenv("DB_PORT", 5432)  
    db_name: str = os.getenv("DB_NAME", "dispositivos_db")
    DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
    
else:
    print("Using provided DATABASE_URL")
    
     
engine = create_engine(os.getenv("DATABASE_URL", DATABASE_URL))

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Dispositivo(id=1, nombre="iPhone 15", marca="Apple", modelo="Base", fecha_compra="2023-12-01"))
        session.add(Dispositivo(id=2, nombre="Galaxy S23", marca="Samsung", modelo="Base", fecha_compra="2024-01-15"))
        session.add(Dispositivo(id=3, nombre="iPhone 17 Pro", marca="Apple", modelo="Pro", fecha_compra="2025-11-17"))
        session.add(Dispositivo(id=4, nombre="iPhone 12", marca="Apple", modelo="Base", fecha_compra="2020-03-10"))
        session.commit()
        
        
        