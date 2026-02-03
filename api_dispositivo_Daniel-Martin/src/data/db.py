from sqlmodel import create_engine, SQLModel, Session
from models.dispositivo import Dispositivo

db_user: str = "quevedo"  
db_password: str =  "1234"
db_server: str = "localhost" 
db_port: int = 3306  
db_name: str = "dispositivosdb"  

DATABASE_URL = "mysql+pymysql://quevedo:1234@localhost:3306/dispositivosdb"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Dispositivo(id=1, nombre="iPhone 15", marca="Apple", fecha_compra="2023-12-01"))
        session.add(Dispositivo(id=2, nombre="Galaxy S23", marca="Samsung", fecha_compra="2024-01-15"))
        session.commit()
        
        
        