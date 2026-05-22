"""
etf_dao.py
----------
Data Access Object fuer ETFs.

Ein DAO trennt den Datenbank-Zugriff von der restlichen Logik.
Der Rest der Anwendung ruft hier nur Methoden auf wie create() oder get_all()
und muss sich nicht um SQL oder Sessions kuemmern.
"""

from sqlmodel import Session, select
from models import ETF


class ETFDAO:
    """Stellt die CRUD-Operationen fuer die ETF-Tabelle bereit."""

    def __init__(self, session: Session):
        # Die Session wird von aussen reingegeben (Dependency Injection).
        # So koennen wir z.B. fuer Tests eine andere Session verwenden.
        self.session = session

    def create(self, name: str, isin: str, symbol: str, ter: float,
               kategorie: str, aktueller_kurs: float,
               erwartete_rendite: float) -> ETF:
        """Legt einen neuen ETF in der Datenbank an."""
        etf = ETF(
            name=name, isin=isin, symbol=symbol, ter=ter,
            kategorie=kategorie, aktueller_kurs=aktueller_kurs,
            erwartete_rendite=erwartete_rendite,
        )
        self.session.add(etf)
        self.session.commit()
        self.session.refresh(etf)  # holt die generierte id zurueck
        return etf

    def get_all(self) -> list[ETF]:
        """Liefert alle ETFs aus der Datenbank."""
        return list(self.session.exec(select(ETF)).all())

    def get_by_id(self, etf_id: int) -> ETF | None:
        """Sucht einen ETF anhand seiner id."""
        return self.session.get(ETF, etf_id)

    def get_by_isin(self, isin: str) -> ETF | None:
        """Sucht einen ETF anhand seiner ISIN (eindeutig)."""
        statement = select(ETF).where(ETF.isin == isin)
        return self.session.exec(statement).first()

    def update(self, etf: ETF) -> ETF:
        """Speichert Aenderungen an einem ETF."""
        self.session.add(etf)
        self.session.commit()
        self.session.refresh(etf)
        return etf

    def delete(self, etf: ETF) -> None:
        """Loescht einen ETF."""
        self.session.delete(etf)
        self.session.commit()
