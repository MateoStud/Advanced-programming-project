"""
models.py
---------
Das Datenmodell der Anwendung.

Wir verwenden SQLModel: Damit ist eine Klasse gleichzeitig
- ein Python-Objekt (OOP) und
- eine Tabelle in der Datenbank (ORM).

Ein ETF speichert seinen aktuellen Kurs und die vom Benutzer geschaetzte
jaehrliche Rendite. Daraus rechnen wir die zukuenftige Wertentwicklung aus.
"""

from sqlmodel import SQLModel, Field


class ETF(SQLModel, table=True):
    """Repraesentiert einen ETF mit Stammdaten und Annahmen zur Rendite."""
    id: int | None = Field(default=None, primary_key=True)
    name: str
    isin: str = Field(unique=True)         # ISIN ist immer eindeutig
    symbol: str                            # z.B. "VWRL"
    ter: float                             # Total Expense Ratio in Prozent
    kategorie: str                         # z.B. "Welt", "Schwellenlaender"
    aktueller_kurs: float                  # heutiger Kurs in CHF/EUR/USD
    erwartete_rendite: float               # erwartete jaehrliche Rendite in %
