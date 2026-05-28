"""
conftest.py - Shared pytest fixtures.

A fixture is a helper that provides setup data to a test. pytest
finds this file automatically and makes the fixtures available in
every test by name.
"""

import pytest
from sqlmodel import SQLModel
from sqlalchemy import create_engine

from etf_app.data_access.dao import ETFDAO
from etf_app.domain.models import ETF


@pytest.fixture
def dao():
    """A fresh ETFDAO using an in-memory SQLite for each test.

    In-memory means the database lives only in RAM and disappears
    after the test. The real etf_app.db is never touched.

    We use yield + engine.dispose() so every database connection is
    closed cleanly after the test (no ResourceWarning).
    """
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    yield ETFDAO(engine)
    engine.dispose()


@pytest.fixture
def sample_etf():
    """A reusable ETF for unit tests of the forecast service."""
    return ETF(
        name="Test ETF", isin="CH0000000001", symbol="TEST",
        ter=0.20, kategorie="Welt", aktueller_kurs=100.00,
        erwartete_rendite=7.00,
    )
