"""
database.py
-----------
Verantwortlich fuer die Verbindung zur SQLite-Datenbank.
Hier wird die Engine erstellt und die Tabellen werden generiert.

Erklaerung:
- Die Engine ist die Verbindung zwischen Python und der Datenbank-Datei.
- create_db_and_tables() liest alle SQLModel-Klassen mit table=True und
  erstellt automatisch die passenden Tabellen, falls sie noch nicht existieren.
"""

from sqlmodel import SQLModel, Session, create_engine

# Die Datenbank wird als Datei "etf.db" im Projektordner gespeichert.
DATABASE_URL = "sqlite:///etf.db"

# echo=False -> SQL-Befehle nicht in der Konsole ausgeben.
# Auf True setzen, falls man beim Debuggen die SQL-Statements sehen will.
engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables() -> None:
    """Erstellt alle Tabellen, die in models.py mit table=True definiert sind."""
    # Wichtig: models muss importiert sein, damit SQLModel die Klassen kennt.
    import models  # noqa: F401
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """Liefert eine neue Session, die mit 'with' verwendet werden sollte."""
    return Session(engine)
