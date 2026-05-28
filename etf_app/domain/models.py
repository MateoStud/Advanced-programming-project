"""
models.py - The ETF data model.

SQLModel makes one class serve two purposes:
- a Python object (OOP), and
- a database table (ORM).

The Field(...) rules also validate the inputs: a negative price or an
empty name is rejected before the data even reaches the database.
"""

from typing import Optional
from sqlmodel import SQLModel, Field


class ETF(SQLModel, table=True):
    """An exchange traded fund."""

    # validate_assignment makes the Field() rules fire on creation.
    model_config = {"validate_assignment": True}

    id: Optional[int] = Field(default=None, primary_key=True)

    # Identification fields. min_length=2 stops empty inputs.
    name: str = Field(min_length=2, max_length=120)
    isin: str = Field(unique=True, min_length=12, max_length=12)
    symbol: str = Field(min_length=1, max_length=10)
    kategorie: str = Field(min_length=2, max_length=60)

    # Numeric fields with realistic bounds.
    ter: float = Field(ge=0.0, le=5.0)
    aktueller_kurs: float = Field(gt=0.0, le=100000.0)
    erwartete_rendite: float = Field(ge=-50.0, le=100.0)
