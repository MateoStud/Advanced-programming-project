"""
test_integration.py - Integration tests.

These tests cross layers: they save data via the DAO, then run the
ForecastService on it. They check that DAO + service fit together.
"""

import pytest

from etf_app.domain.models import ETF
from etf_app.services.forecast_service import ForecastService


# Test 12: save an ETF, then find it via list_all
def test_save_and_list(dao):
    etf = ETF(name="World ETF", isin="IE00B4L5Y983", symbol="IWDA",
              ter=0.20, kategorie="Welt", aktueller_kurs=95.0,
              erwartete_rendite=7.5)
    dao.create(etf)

    all_etfs = dao.list_all()
    assert len(all_etfs) == 1
    assert all_etfs[0].symbol == "IWDA"


# Test 13: forecast on a DB-loaded ETF
def test_forecast_on_loaded_etf(dao):
    """Save an ETF, load it from the DB, run the forecast on it."""
    dao.create(ETF(name="S&P 500 ETF", isin="US9229083632",
                   symbol="VOO", ter=0.03, kategorie="USA Large Cap",
                   aktueller_kurs=525.0, erwartete_rendite=8.5))

    etf = dao.list_all()[0]
    forecast = ForecastService().calculate(
        etf=etf, anlagebetrag=10000, jahre=20
    )

    # 8.5% - 0.03% TER = 8.47% over 20 years
    # 10'000 * (1.0847)^20 ≈ 50'838.51
    assert forecast.effektive_rendite == pytest.approx(8.47, abs=0.001)
    assert forecast.endwert == pytest.approx(50838.51, abs=0.1)


# Test 14: delete a saved ETF
def test_save_then_delete(dao):
    """Save an ETF, delete it, the list must be empty again."""
    saved = dao.create(ETF(
        name="Temp ETF", isin="CH0000000077", symbol="TMP",
        ter=0.10, kategorie="Test", aktueller_kurs=50.0,
        erwartete_rendite=5.0,
    ))
    assert len(dao.list_all()) == 1

    dao.delete(saved.id)
    assert dao.list_all() == []


# Test 15: forecast on multiple ETFs (comparison logic)
def test_forecast_on_multiple_etfs(dao):
    """Save two ETFs, run the forecast on both, compare."""
    dao.create(ETF(name="High Return ETF", isin="US0000000001",
                   symbol="HI", ter=0.05, kategorie="Test",
                   aktueller_kurs=100, erwartete_rendite=10.0))
    dao.create(ETF(name="Low Return ETF", isin="US0000000002",
                   symbol="LO", ter=0.05, kategorie="Test",
                   aktueller_kurs=100, erwartete_rendite=4.0))

    service = ForecastService()
    forecasts = [service.calculate(etf=e, anlagebetrag=1000, jahre=10)
                 for e in dao.list_all()]

    # The higher-return ETF must end up with the higher value.
    endwerte = sorted([f.endwert for f in forecasts])
    assert endwerte[1] > endwerte[0]
