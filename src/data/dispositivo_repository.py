from sqlmodel import Session, select
from models.dispositivo import Dispositivo

class DispositivoRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def get_all_dispositivos(self) -> list[Dispositivo]:
        dispositivos = self.session.exec(select(Dispositivo)).all()
        return dispositivos   

    def get_dispositivo(self, dispositivo_id: int) -> Dispositivo:
        dispositivo = self.session.get(Dispositivo, dispositivo_id)
        return dispositivo

    def create_dispositivo(self, dispositivo: Dispositivo) -> Dispositivo:
        self.session.add(dispositivo)
        self.session.commit()
        self.session.refresh(dispositivo)
        return dispositivo

    def update_dispositivo(self, dispositivo_id: int, dispositivo_data: dict) -> Dispositivo:
        dispositivo = self.get_dispositivo(dispositivo_id)
        for key, value in dispositivo_data.items():
            setattr(dispositivo, key, value)
        self.session.commit()
        self.session.refresh(dispositivo)
        return dispositivo

    def delete_dispositivo(self, dispositivo_id: int) -> None:
        dispositivo = self.get_dispositivo(dispositivo_id)
        self.session.delete(dispositivo)
        self.session.commit()