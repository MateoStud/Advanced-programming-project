"""
test_db.py - Database tests.

Each test gets a fresh in-memory SQLite via the `dao` fixture, so
no test writes to the real etf_app.db.
"""

import pytest
from pydantic import ValidationError

from etf_app.domain.models import ETF
from etf_app.data_access.dao import DuplicateISINError


def _make_etf(isin="CH0000000001", name="Test ETF"):
    """Helper to build a valid ETF object for the tests."""
    return ETF(name=name, isin=isin, symbol="TST", ter=0.20,
               kategorie="Welt", aktueller_kurs=100.0,
               erwartete_rendite=7.0)


# Test 7: list_all returns saved ETFs
def test_list_all_returns_saved_etfs(dao):
    dao.create(_make_etf(isin="CH0000000001", name="Alpha ETF"))
    dao.create(_make_etf(isin="CH0000000002", name="Beta ETF"))

    all_etfs = dao.list_all()
    assert len(all_etfs) == 2


# Test 8: create assigns an id
def test_create_assigns_id(dao):
    saved = dao.create(_make_etf())
    assert saved.id is not None
    # Round-trip: load it back via get_by_id
    loaded = dao.get_by_id(saved.id)
    assert loaded.isin == "CH0000000001"


# Test 9: duplicate ISIN raises DuplicateISINError
def test_duplicate_isin_raises(dao):
    dao.create(_make_etf(isin="CH0000000001"))
    with pytest.raises(DuplicateISINError):
        dao.create(_make_etf(isin="CH0000000001", name="Other ETF"))


# Test 10: delete removes the ETF
def test_delete_removes_etf(dao):
    saved = dao.create(_make_etf())
    dao.delete(saved.id)
    assert dao.get_by_id(saved.id) is None


# Test 11: model validation rejects bad input
def test_model_validation_rejects_bad_input():
    """The Field() rules in models.py reject invalid data before
    it ever reaches the database.
    """
    # Negative price
    with pytest.raises(ValidationError):
        ETF(name="Bad ETF", isin="CH0000000003", symbol="BAD",
            ter=0.1, kategorie="Test", aktueller_kurs=-5.0,
            erwartete_rendite=5.0)

    # Empty name (min_length=2)
    with pytest.raises(ValidationError):
        ETF(name="", isin="CH0000000004", symbol="ZZ",
            ter=0.1, kategorie="Welt", aktueller_kurs=10.0,
            erwartete_rendite=5.0)

    # Wrong ISIN length (must be 12)
    with pytest.raises(ValidationError):
        ETF(name="Short ISIN ETF", isin="ABC", symbol="ZZ",
            ter=0.1, kategorie="Welt", aktueller_kurs=10.0,
            erwartete_rendite=5.0)
