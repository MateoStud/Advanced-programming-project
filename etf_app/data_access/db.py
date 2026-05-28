"""
db.py - Database facade.

This class hides all the database setup behind one simple interface:
- create the engine (the connection to SQLite),
- create the tables,
- seed the initial 10 ETFs if the table is empty.

Design pattern: Facade. The rest of the app does not need to know
about engines, schemas or seeders - it only uses Database.
"""

from pathlib import Path
from sqlmodel import SQLModel, Session, create_engine, select

from etf_app.domain.models import ETF
from etf_app.data_access.seed import seed_etfs


class Database:
    """Facade around the SQLite database."""

    def __init__(self, url: str = "sqlite:///data/etf_app.db"):
        # Make sure the data/ folder exists for the SQLite file.
        Path("data").mkdir(exist_ok=True)

        # check_same_thread=False because NiceGUI runs in threads.
        self.engine = create_engine(
            url, connect_args={"check_same_thread": False}
        )

    def init(self) -> None:
        """Create all tables and add the 10 starter ETFs if empty."""
        SQLModel.metadata.create_all(self.engine)
        with Session(self.engine) as session:
            # Only seed when the table is empty (idempotent).
            if session.exec(select(ETF)).first() is None:
                seed_etfs(session)
                session.commit()
