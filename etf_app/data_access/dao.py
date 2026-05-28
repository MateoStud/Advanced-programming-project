"""
dao.py - Data Access Object for the ETF table.

The DAO hides all database details from the rest of the app. The
rest of the app calls list_all() or create() and never sees any SQL.

OOP demo: BaseDAO is the parent class with the engine and a helper
to open sessions. ETFDAO inherits from it and adds ETF-specific
methods.
"""

from typing import List, Optional

from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from etf_app.domain.models import ETF


# Custom exception so the UI can catch a clear, named error.
class DuplicateISINError(Exception):
    """Raised when an ETF with the same ISIN already exists."""


class BaseDAO:
    """Parent class. Holds the engine and creates sessions."""

    def __init__(self, engine: Engine):
        self.engine = engine

    def session(self) -> Session:
        return Session(self.engine)


class ETFDAO(BaseDAO):
    """DAO for the ETF table - inherits engine + session() from BaseDAO."""

    def list_all(self) -> List[ETF]:
        """Return all ETFs sorted by name."""
        with self.session() as s:
            return list(s.exec(select(ETF).order_by(ETF.name)).all())

    def get_by_id(self, etf_id: int) -> Optional[ETF]:
        """Get one ETF by id, or None."""
        with self.session() as s:
            return s.get(ETF, etf_id)

    def create(self, etf: ETF) -> ETF:
        """Save a new ETF. Raises DuplicateISINError on duplicate ISIN."""
        with self.session() as s:
            try:
                s.add(etf)
                s.commit()
                s.refresh(etf)
                return etf
            except IntegrityError as e:
                s.rollback()
                raise DuplicateISINError(
                    f"Ein ETF mit ISIN {etf.isin} existiert bereits."
                ) from e

    def delete(self, etf_id: int) -> None:
        """Delete the ETF with the given id. No-op if not found."""
        with self.session() as s:
            etf = s.get(ETF, etf_id)
            if etf is not None:
                s.delete(etf)
                s.commit()
